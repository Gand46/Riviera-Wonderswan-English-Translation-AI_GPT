#!/usr/bin/env python3
"""Portable entry point for the complete S441-S461 source rebuild."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess
import sys


EXPECTED_SOURCE = "62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921"
EXPECTED_TARGET = "2eaeb2c90ca2ef62d858a887fa1ee2091d680b17366bf5dd07d642d0fc8171bf"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("clean_jp", help="Clean Japanese Riviera WSC ROM")
    parser.add_argument(
        "--out",
        default="build/Riviera_EN_v0.114_S461_RC5.wsc",
        help="Output path",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    clean = Path(args.clean_jp).resolve()
    destination = Path(args.out).resolve()
    assert sha256(clean) == EXPECTED_SOURCE, "Wrong clean Japanese ROM"

    subprocess.run(
        [
            sys.executable,
            str(root / "sources/Riviera_S461_OVERLAY/rebuild.py"),
            str(clean),
            "--out",
            str(destination),
        ],
        check=True,
    )
    assert sha256(destination) == EXPECTED_TARGET, "Unexpected RC5 output"
    print("RC5_FULL_SOURCE_REBUILD_OK", EXPECTED_TARGET)


if __name__ == "__main__":
    main()
