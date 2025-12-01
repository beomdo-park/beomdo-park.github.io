"""Fetch the GitHub profile README and derive a summary for the About page."""

from __future__ import annotations

import pathlib
import sys

import requests


RAW_README_URL = "https://raw.githubusercontent.com/beomdo-park/beomdo-park/main/README.md"
FULL_PATH = pathlib.Path("assets/profile-readme.md")
SUMMARY_PATH = pathlib.Path("assets/profile-summary.md")

SUMMARY_START_MARKERS = ["## 👀 About Me", "<h2>👀 About Me"]
SUMMARY_END_MARKERS = ["## 🤔 Github Stats", "## 📈 GitHub Trophies", "## 📬 Contact"]


def download_readme() -> str:
    """Return the remote README contents."""

    response = requests.get(RAW_README_URL, timeout=10)
    response.raise_for_status()
    return response.text.rstrip() + "\n"


def _find_marker(lines: list[str], markers: list[str]) -> int | None:
    for idx, line in enumerate(lines):
        if any(marker in line for marker in markers):
            return idx
    return None


def extract_summary(full_text: str) -> str:
    """Return the subset used on the About page.

    Cut from the About Me header through Activities, but stop
    before Github Stats / Trophies / Contact sections.
    """

    lines = full_text.splitlines()

    # 1) 먼저 About Me 시작 위치를 찾는다.
    start = _find_marker(lines, SUMMARY_START_MARKERS)
    if start is None:
        return full_text

    # 2) 시작 지점부터 Stats/Trophies/Contact 중 하나가 나오기 전까지를 사용한다.
    end_rel = _find_marker(lines[start:], SUMMARY_END_MARKERS)
    slice_end = start + end_rel if end_rel is not None else len(lines)

    # 3) 이 구간 안에서 README 최상단에서 쓰던 래핑 <div>의 닫는 </div> 만 제거
    slice_lines = lines[start:slice_end]
    cleaned_lines: list[str] = []
    for line in slice_lines:
        if line.strip() == "</div>":
            continue
        cleaned_lines.append(line)

    summary = "\n".join(cleaned_lines).strip()
    return summary + "\n" if summary else full_text


def main() -> int:
    try:
        content = download_readme()
    except requests.RequestException as exc:
        print(f"Failed to download README: {exc}", file=sys.stderr)
        return 1

    FULL_PATH.parent.mkdir(parents=True, exist_ok=True)
    FULL_PATH.write_text(content, encoding="utf-8")
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

    summary = extract_summary(content)
    SUMMARY_PATH.write_text(summary, encoding="utf-8")

    print(
        "Saved profile README to {full} and summary to {summary}".format(
            full=FULL_PATH,
            summary=SUMMARY_PATH,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())