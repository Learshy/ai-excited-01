#!/usr/bin/env python3
"""ai-excited-01 entry (Python 3.13, standard library only).

The entry image is entry.png beside this file, and the program copies it
byte-for-byte to /output/entry.png. Fully deterministic: a plain file copy,
no network, no randomness, no timestamps, no dependence on anything but
the file sitting next to this script.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", OUT_DIR / "entry.png")


if __name__ == "__main__":
    main()
