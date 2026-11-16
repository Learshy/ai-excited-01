#!/usr/bin/env python3
"""Koi entry for ai-excited-01.

Writes the generated picture (entry.png, sitting next to this script)
to /output/entry.png, byte for byte. Standard library only.

The picture is staged in a throwaway file inside the destination folder
and moved into place, so a run cut short mid-copy can never leave a
half-written picture behind. A missing picture stops the run with a
message on stderr and a nonzero exit, and the finished copy is hashed
and checked against the original before the program reports success.

When run outside the grading container, set MAKEFUN_OUTPUT_DIR to the
folder that should receive the picture, e.g.:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PICTURE = HERE / "entry.png"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def sha256_file(path):
    """Hex SHA-256 of a file, read in 1 MiB blocks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(1 << 20)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not PICTURE.is_file():
        print("error: entry picture missing or not a file: " + str(PICTURE), file=sys.stderr)
        sys.exit(1)
    wanted = sha256_file(PICTURE)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    final = OUT_DIR / "entry.png"
    draft = OUT_DIR / ".entry.png.part"
    if draft.exists():
        draft.unlink()  # leftover from a run cut short before its rename
    shutil.copyfile(PICTURE, draft)
    os.replace(draft, final)
    if sha256_file(final) != wanted:
        print("error: written picture differs from the source", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
