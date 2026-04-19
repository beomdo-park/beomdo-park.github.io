"""Sanity check for the week-3 ROQET pipeline before wiring it into Quarto.

Goal: prove that
  1) DEM -> edge_index/edge_attr extraction handles 2-body decomposed mechanisms
  2) per-shot Data construction works
  3) TinyGraphDecoder trains and val LER goes down
on a small budget so the qmd render finishes in a reasonable time.
"""

import time
import numpy as np
import stim
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GraphConv, global_add_pool, global_mean_pool
import pymatching


DISTANCE = 3
ROUNDS = 3
NOISE = 0.005
N_SHOTS = 30_000
EPOCHS = 15
BATCH = 512
LR = 3e-3


def build_circuit():
    return stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=DISTANCE,
        rounds=ROUNDS,
        after_clifford_depolarization=NOISE,
        after_reset_flip_probability=NOISE,
        before_measure_flip_probability=NOISE,
        before_round_data_depolarization=NOISE,
    )


def build_static_graph(circuit: stim.Circuit):
    dem = circuit.detector_error_model(decompose_errors=True)
    num_detectors = dem.num_detectors

    coords_dict = circuit.get_detector_coordinates()
    coord_arr = np.zeros((num_detectors, 3), dtype=np.float32)
    for i in range(num_detectors):
        c = coords_dict.get(i, [0.0, 0.0, 0.0])
        coord_arr[i, : len(c)] = c

    edge_set = {}
    for instr in dem.flattened():
        if instr.type != "error":
            continue
        p = instr.args_copy()[0]
        if p <= 0.0:
            continue
        # Decomposed targets are split by separators into 2-body components.
        component, components = [], []
        for t in instr.targets_copy():
            if t.is_separator():
                if component:
                    components.append(component)
                component = []
            elif t.is_relative_detector_id():
                component.append(t.val)
        if component:
            components.append(component)

        for comp in components:
            if len(comp) != 2:
                continue
            a, b = sorted(comp)
            w = -np.log(max(p, 1e-12))
            # If two mechanisms produce the same edge, combine probabilities.
            prev = edge_set.get((a, b))
            if prev is None:
                edge_set[(a, b)] = p
            else:
                # p_combined = p1*(1-p2) + p2*(1-p1)
                edge_set[(a, b)] = prev * (1 - p) + p * (1 - prev)

    edges = list(edge_set.keys())
    weights = [-np.log(max(edge_set[e], 1e-12)) for e in edges]

    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    edge_attr = torch.tensor(weights, dtype=torch.float32).unsqueeze(1)
    # Make undirected explicitly.
    edge_index = torch.cat([edge_index, edge_index.flip(0)], dim=1)
    edge_attr = torch.cat([edge_attr, edge_attr], dim=0)
    return edge_index, edge_attr, coord_arr


def shot_to_data(det_bits, obs_bit, edge_index, edge_attr, t_norm, xy_norm):
    x = np.stack(
        [det_bits.astype(np.float32), t_norm, xy_norm[:, 0], xy_norm[:, 1]], axis=1
    )
    return Data(
        x=torch.from_numpy(x),
        edge_index=edge_index,
        edge_attr=edge_attr,
        y=torch.tensor([float(obs_bit)], dtype=torch.float32),
    )


class TinyGraphDecoder(nn.Module):
    def __init__(self, in_dim=4, hidden=64):
        super().__init__()
        self.conv1 = GraphConv(in_dim, hidden)
        self.conv2 = GraphConv(hidden, hidden)
        self.head = nn.Sequential(
            nn.Linear(2 * hidden, hidden),
            nn.ReLU(inplace=True),
            nn.Linear(hidden, 1),
        )

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        # mean + sum pooling captures both "what kind of pattern" and "how many fired"
        g = torch.cat([global_mean_pool(x, batch), global_add_pool(x, batch)], dim=1)
        return self.head(g).squeeze(-1)


def main():
    torch.manual_seed(0)
    np.random.seed(0)

    circuit = build_circuit()
    print(f"detectors={circuit.num_detectors}, observables={circuit.num_observables}")

    edge_index, edge_attr, coord_arr = build_static_graph(circuit)
    print(f"edges (directed) = {edge_index.shape[1]}")

    sampler = circuit.compile_detector_sampler()
    t0 = time.time()
    det, obs = sampler.sample(shots=N_SHOTS, separate_observables=True)
    print(f"sampled {N_SHOTS} shots in {time.time()-t0:.2f}s")

    # PyMatching baseline.
    matcher = pymatching.Matching.from_detector_error_model(
        circuit.detector_error_model(decompose_errors=True)
    )
    pred = matcher.decode_batch(det)
    mwpm_ler = float(np.mean(np.any(pred != obs, axis=1)))
    raw_ler = float(obs.mean())
    print(f"raw LER={raw_ler:.4%}  MWPM LER={mwpm_ler:.4%}")

    # Pre-compute coord normalisation once.
    t_norm = (coord_arr[:, 2] / max(ROUNDS - 1, 1)).astype(np.float32)
    xy = coord_arr[:, :2]
    xy_norm = ((xy - xy.mean(axis=0)) / (xy.std(axis=0) + 1e-6)).astype(np.float32)

    t0 = time.time()
    dataset = [
        shot_to_data(det[i], obs[i, 0], edge_index, edge_attr, t_norm, xy_norm)
        for i in range(N_SHOTS)
    ]
    print(f"built {len(dataset)} Data objects in {time.time()-t0:.2f}s")

    n_train = int(0.9 * N_SHOTS)
    train_set, val_set = dataset[:n_train], dataset[n_train:]
    train_loader = DataLoader(train_set, batch_size=BATCH, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=1024, shuffle=False)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = TinyGraphDecoder().to(device)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.BCEWithLogitsLoss()

    def run_epoch(loader, train):
        model.train(train)
        total_loss, total_correct, total = 0.0, 0, 0
        for batch in loader:
            batch = batch.to(device)
            logit = model(batch)
            loss = loss_fn(logit, batch.y)
            if train:
                opt.zero_grad()
                loss.backward()
                opt.step()
            pred = (logit.sigmoid() > 0.5).float()
            total_loss += loss.item() * batch.num_graphs
            total_correct += (pred == batch.y).sum().item()
            total += batch.num_graphs
        return total_loss / total, 1 - total_correct / total

    for epoch in range(1, EPOCHS + 1):
        t0 = time.time()
        tr_loss, tr_ler = run_epoch(train_loader, True)
        va_loss, va_ler = run_epoch(val_loader, False)
        print(
            f"epoch {epoch:02d} | train loss {tr_loss:.4f} / LER {tr_ler:.4%}"
            f" | val loss {va_loss:.4f} / LER {va_ler:.4%} | {time.time()-t0:.1f}s"
        )


if __name__ == "__main__":
    main()
