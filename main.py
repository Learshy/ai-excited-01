#!/usr/bin/env python3
"""Golden Koi — ai-excited-01 entry.

Copies the entry image (entry.png, next to this script) byte-for-byte to
/output/entry.png. Python 3.13 standard library only: no network, no
randomness, no timestamps — the output is a pure function of the input file,
so repeated runs produce identical bytes.

The copy lands in a temporary file inside the output directory and is then
renamed into place, so an interrupted run can never leave a half-written
image behind. A missing source aborts loudly instead of yielding an empty
output, and the finished file is hashed and compared with the source before
the program exits.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
IMAGE = BASE / "entry.png"
DEST = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def digest_of(path: Path) -> str:
    """SHA-256 hex digest of a file, streamed in 1 MiB chunks."""
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(1 << 20)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


def main() -> None:
    if not IMAGE.is_file():
        print(f"error: source image not found: {IMAGE}", file=sys.stderr)
        raise SystemExit(1)
    source_hash = digest_of(IMAGE)
    DEST.mkdir(parents=True, exist_ok=True)
    out_path = DEST / "entry.png"
    staging = DEST / ".entry.png.tmp"
    shutil.copyfile(IMAGE, staging)
    os.replace(staging, out_path)
    if digest_of(out_path) != source_hash:
        print("error: output image does not match the source", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
