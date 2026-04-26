"""Week 4 prototype: edge-aware decoder ablations vs MWPM at d=3.

Builds the four variants we want to put in the week-4 post and measures
how much each upgrade narrows the gap to PyMatching.
  v0: TinyGraphDecoder (week 3 baseline, no edge_attr, no boundary)
  v1: + boundary node
  v2: + boundary node + NNConv (edge_attr-aware)
  v3: + boundary node + NNConv + scaled (hidden 128, 3 layers, 100k shots)

Goal: confirm each variant trains, fits in CPU time budget, and produces
believable numbers before transcribing into the .qmd.
"""

import time
import numpy as np
import stim
import torch
import torch.nn as nn
import torch.nn.functional as F
import pymatching
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GraphConv, NNConv, global_add_pool, global_mean_pool


DISTANCE = 3
ROUNDS = 3
NOISE = 0.005
N_SHOTS_BASE = 30_000     # for v0..v2
N_SHOTS_SCALED = 100_000  # for v3
EPOCHS_BASE = 15
EPOCHS_SCALED = 12
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


def build_static_graph(circuit, with_boundary: bool):
    dem = circuit.detector_error_model(decompose_errors=True)
    num_detectors = dem.num_detectors
    num_nodes = num_detectors + (1 if with_boundary else 0)
    boundary_idx = num_detectors  # only valid if with_boundary

    coords_dict = circuit.get_detector_coordinates()
    coord_arr = np.zeros((num_nodes, 3), dtype=np.float32)
    for i in range(num_detectors):
        c = coords_dict.get(i, [0.0, 0.0, 0.0])
        coord_arr[i, : len(c)] = c
    if with_boundary:
        # Place the boundary node at the centroid so coord features stay sane.
        coord_arr[boundary_idx] = coord_arr[:num_detectors].mean(axis=0)

    edge_p = {}

    def add_edge(a, b, p):
        if a == b:
            return
        a, b = (a, b) if a < b else (b, a)
        prev = edge_p.get((a, b))
        edge_p[(a, b)] = p if prev is None else prev * (1 - p) + p * (1 - prev)

    for instr in dem.flattened():
        if instr.type != "error":
            continue
        p = instr.args_copy()[0]
        if p <= 0.0:
            continue

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
            if len(comp) == 2:
                add_edge(comp[0], comp[1], p)
            elif len(comp) == 1 and with_boundary:
                add_edge(comp[0], boundary_idx, p)
            # 3-체 이상은 여전히 보류 (다음 주 숙제)

    edges = list(edge_p.keys())
    weights = [-np.log(max(edge_p[e], 1e-12)) for e in edges]

    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    edge_attr = torch.tensor(weights, dtype=torch.float32).unsqueeze(1)
    edge_index = torch.cat([edge_index, edge_index.flip(0)], dim=1)
    edge_attr = torch.cat([edge_attr, edge_attr], dim=0)
    return edge_index, edge_attr, coord_arr, num_nodes, num_detectors


def make_dataset(detection_events, observable_flips, edge_index, edge_attr,
                 coord_arr, num_nodes, num_detectors, rounds):
    t_norm = (coord_arr[:, 2] / max(rounds - 1, 1)).astype(np.float32)
    xy = coord_arr[:, :2]
    xy_norm = ((xy - xy.mean(axis=0)) / (xy.std(axis=0) + 1e-6)).astype(np.float32)
    n = detection_events.shape[0]
    dataset = []
    is_boundary = num_nodes != num_detectors
    for i in range(n):
        det = np.zeros(num_nodes, dtype=np.float32)
        det[:num_detectors] = detection_events[i].astype(np.float32)
        # boundary node detection bit stays 0; rely on a flag feature instead.
        flag = np.zeros(num_nodes, dtype=np.float32)
        if is_boundary:
            flag[num_detectors] = 1.0
        x = np.stack([det, t_norm, xy_norm[:, 0], xy_norm[:, 1], flag], axis=1)
        dataset.append(Data(
            x=torch.from_numpy(x),
            edge_index=edge_index,
            edge_attr=edge_attr,
            y=torch.tensor([float(observable_flips[i, 0])], dtype=torch.float32),
        ))
    return dataset


class GraphConvDecoder(nn.Module):
    def __init__(self, in_dim=5, hidden=64, n_layers=2):
        super().__init__()
        dims = [in_dim] + [hidden] * n_layers
        self.convs = nn.ModuleList(
            GraphConv(dims[i], dims[i + 1]) for i in range(n_layers)
        )
        self.head = nn.Sequential(
            nn.Linear(2 * hidden, hidden),
            nn.ReLU(inplace=True),
            nn.Linear(hidden, 1),
        )

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch
        for conv in self.convs:
            x = F.relu(conv(x, edge_index))
        g = torch.cat([global_mean_pool(x, batch), global_add_pool(x, batch)], dim=1)
        return self.head(g).squeeze(-1)


class NNConvDecoder(nn.Module):
    def __init__(self, in_dim=5, hidden=64, edge_dim=1, n_layers=2):
        super().__init__()
        self.lift = nn.Linear(in_dim, hidden)
        self.convs = nn.ModuleList()
        for _ in range(n_layers):
            edge_mlp = nn.Sequential(
                nn.Linear(edge_dim, 32),
                nn.ReLU(inplace=True),
                nn.Linear(32, hidden * hidden),
            )
            self.convs.append(NNConv(hidden, hidden, edge_mlp, aggr="mean"))
        self.head = nn.Sequential(
            nn.Linear(2 * hidden, hidden),
            nn.ReLU(inplace=True),
            nn.Linear(hidden, 1),
        )

    def forward(self, data):
        x, edge_index, edge_attr, batch = (
            data.x, data.edge_index, data.edge_attr, data.batch
        )
        x = F.relu(self.lift(x))
        for conv in self.convs:
            x = F.relu(conv(x, edge_index, edge_attr))
        g = torch.cat([global_mean_pool(x, batch), global_add_pool(x, batch)], dim=1)
        return self.head(g).squeeze(-1)


def train_eval(model, train_set, val_set, epochs, label, device):
    train_loader = DataLoader(train_set, batch_size=BATCH, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=1024, shuffle=False)
    model = model.to(device)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.BCEWithLogitsLoss()

    def epoch(loader, train):
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

    t0 = time.time()
    last_va_ler = None
    for ep in range(1, epochs + 1):
        tr_loss, tr_ler = epoch(train_loader, True)
        va_loss, va_ler = epoch(val_loader, False)
        last_va_ler = va_ler
        if ep == 1 or ep % 3 == 0 or ep == epochs:
            print(f"  [{label}] ep {ep:02d} | tr {tr_loss:.4f}/{tr_ler:.4%}"
                  f" | va {va_loss:.4f}/{va_ler:.4%}")
    elapsed = time.time() - t0

    # Inference time (val only).
    t0 = time.time()
    with torch.no_grad():
        for batch in val_loader:
            batch = batch.to(device)
            _ = model(batch)
    inf_s = time.time() - t0

    n_params = sum(p.numel() for p in model.parameters())
    return {"label": label, "ler": last_va_ler, "params": n_params,
            "train_s": elapsed, "inf_s": inf_s}


def run_variant(label, *, with_boundary, conv, hidden, n_layers,
                n_shots, epochs, det_base, obs_base, det_scaled, obs_scaled,
                circuit, device, results):
    print(f"\n=== {label} (boundary={with_boundary}, conv={conv}, "
          f"hidden={hidden}, layers={n_layers}, shots={n_shots}) ===")
    edge_index, edge_attr, coord_arr, num_nodes, num_detectors = build_static_graph(
        circuit, with_boundary=with_boundary
    )
    print(f"  graph: nodes={num_nodes}, edges(directed)={edge_index.shape[1]}")

    if n_shots == N_SHOTS_BASE:
        det, obs = det_base, obs_base
    else:
        det, obs = det_scaled, obs_scaled
    dataset = make_dataset(det, obs, edge_index, edge_attr,
                           coord_arr, num_nodes, num_detectors, ROUNDS)
    n_train = int(0.9 * n_shots)
    train_set, val_set = dataset[:n_train], dataset[n_train:]

    if conv == "GraphConv":
        model = GraphConvDecoder(in_dim=5, hidden=hidden, n_layers=n_layers)
    else:
        model = NNConvDecoder(in_dim=5, hidden=hidden, edge_dim=1, n_layers=n_layers)
    out = train_eval(model, train_set, val_set, epochs=epochs,
                     label=label, device=device)
    results.append(out)


def main():
    torch.manual_seed(0)
    np.random.seed(0)

    circuit = build_circuit()
    print(f"detectors={circuit.num_detectors}, observables={circuit.num_observables}")

    sampler = circuit.compile_detector_sampler()
    t0 = time.time()
    det_base, obs_base = sampler.sample(shots=N_SHOTS_BASE, separate_observables=True)
    det_scaled, obs_scaled = sampler.sample(shots=N_SHOTS_SCALED, separate_observables=True)
    print(f"sampled {N_SHOTS_BASE}+{N_SHOTS_SCALED} shots in {time.time()-t0:.2f}s")

    matcher = pymatching.Matching.from_detector_error_model(
        circuit.detector_error_model(decompose_errors=True)
    )
    # MWPM measured on the val slice of the BASE dataset to keep apples-to-apples
    # with v0..v2; v3 has its own bigger val slice but the MWPM number is
    # circuit-level and shouldn't depend much on which val slice.
    n_train = int(0.9 * N_SHOTS_BASE)
    val_det = det_base[n_train:]
    val_obs = obs_base[n_train:]
    t0 = time.time()
    pred_mwpm = matcher.decode_batch(val_det)
    mwpm_inf_s = time.time() - t0
    mwpm_ler = float(np.mean(np.any(pred_mwpm != val_obs, axis=1)))
    raw_ler = float(val_obs.mean())
    print(f"raw LER (val) = {raw_ler:.4%}")
    print(f"MWPM LER (val) = {mwpm_ler:.4%} (inf {mwpm_inf_s*1000:.1f} ms)")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"device={device}")

    results = []
    common = dict(det_base=det_base, obs_base=obs_base,
                  det_scaled=det_scaled, obs_scaled=obs_scaled,
                  circuit=circuit, device=device, results=results)

    run_variant("v0 GraphConv (no boundary)", with_boundary=False,
                conv="GraphConv", hidden=64, n_layers=2,
                n_shots=N_SHOTS_BASE, epochs=EPOCHS_BASE, **common)
    run_variant("v1 GraphConv +boundary", with_boundary=True,
                conv="GraphConv", hidden=64, n_layers=2,
                n_shots=N_SHOTS_BASE, epochs=EPOCHS_BASE, **common)
    run_variant("v2 NNConv +boundary", with_boundary=True,
                conv="NNConv", hidden=64, n_layers=2,
                n_shots=N_SHOTS_BASE, epochs=EPOCHS_BASE, **common)
    run_variant("v3 NNConv +boundary scaled", with_boundary=True,
                conv="NNConv", hidden=128, n_layers=3,
                n_shots=N_SHOTS_SCALED, epochs=EPOCHS_SCALED, **common)

    print("\n=== summary ===")
    print(f"{'variant':<32} {'LER':>8} {'params':>8} {'train_s':>8} {'inf_ms':>8}")
    print(f"{'MWPM':<32} {mwpm_ler:>8.4%} {'-':>8} {'-':>8} {mwpm_inf_s*1000:>8.1f}")
    for r in results:
        print(f"{r['label']:<32} {r['ler']:>8.4%} {r['params']:>8d} "
              f"{r['train_s']:>8.1f} {r['inf_s']*1000:>8.1f}")


if __name__ == "__main__":
    main()
