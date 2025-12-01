"""Fetch the GitHub profile README and save it for the About page."""

from __future__ import annotations

import pathlib
import sys

import requests


RAW_README_URL = "https://raw.githubusercontent.com/beomdo-park/beomdo-park/main/README.md"
TARGET_PATH = pathlib.Path("assets/profile-readme.md")


def download_readme() -> str:
    """Return the remote README contents."""

    response = requests.get(RAW_README_URL, timeout=10)
    response.raise_for_status()
    return response.text.rstrip() + "\n"


def main() -> int:
    try:
        content = download_readme()
    except requests.RequestException as exc:
        print(f"Failed to download README: {exc}", file=sys.stderr)
        return 1

    TARGET_PATH.parent.mkdir(parents=True, exist_ok=True)
    TARGET_PATH.write_text(content, encoding="utf-8")
    print(f"Saved profile README to {TARGET_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())