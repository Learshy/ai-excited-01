#!/usr/bin/env python3
"""ai-excited-01 entry (Python 3.13, standard library only).

The entry image is entry.png beside this file, and the program copies it
byte-for-byte to /output/entry.png. Fully deterministic: a plain file copy,
no network, no randomness, no timestamps, no dependence on anything but
the file sitting next to this script.

The copy is atomic (temp file in the output dir + rename) so an interrupted
run never leaves a half-written entry.png behind, and a missing source file
fails loudly instead of producing a silent empty output.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
SOURCE = HERE / "entry.png"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    if not SOURCE.is_file():
        print(f"error: entry image missing: {SOURCE}", file=sys.stderr)
        raise SystemExit(1)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    target = OUT_DIR / "entry.png"
    tmp = OUT_DIR / ".entry.png.tmp"
    shutil.copyfile(SOURCE, tmp)
    os.replace(tmp, target)
    if _sha256(target) != _sha256(SOURCE):
        print("error: copied entry.png does not match the source", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
