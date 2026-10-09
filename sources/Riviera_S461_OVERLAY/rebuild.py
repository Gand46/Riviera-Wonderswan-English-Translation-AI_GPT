#!/usr/bin/env python3
"""Rebuild S461 RC5 from the clean Japanese ROM through packaged sources."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from build_s461 import build


JP_SHA = "62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921"
RC4_SHA = "931e5cfec6e60fe3ad2b48b192b38bfd071d1a3b2453ddac3e1c271fb8da3c7d"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument("clean_jp")
parser.add_argument("--out", required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
clean = Path(args.clean_jp).resolve()
assert sha(clean.read_bytes()) == JP_SHA, "Wrong clean Japanese source ROM"

with tempfile.TemporaryDirectory(prefix="riviera_s461_") as temp:
    rc4_path = Path(temp) / "s460_rc4.wsc"
    subprocess.run(
        [
            sys.executable,
            str(root.parent / "Riviera_S460_OVERLAY/rebuild_all_sources.py"),
            str(clean),
            "--out",
            str(rc4_path),
        ],
        check=True,
    )
    rc4 = rc4_path.read_bytes()
    assert sha(rc4) == RC4_SHA
    rc5, report = build(rc4)

destination = Path(args.out)
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_bytes(rc5)
report.update(
    {
        "source_chain": "JP clean -> S456 -> S457 -> S458 -> S459 -> S460 -> S461",
        "source_jp_sha256": JP_SHA,
        "intermediate_rc4_sha256": RC4_SHA,
        "bps_used": False,
        "result": "PASS",
    }
)
destination.with_suffix(".full-source-rebuild.json").write_text(
    json.dumps(report, indent=2, ensure_ascii=False) + "\n"
)
print("S461_FULL_SOURCE_REBUILD_OK", sha(rc5))
