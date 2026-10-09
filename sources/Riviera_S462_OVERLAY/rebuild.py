#!/usr/bin/env python3
"""Rebuild S462/RC6 from the clean Japanese ROM through cumulative sources."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from build_s462 import build


JP_SHA = "62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921"
RC5_SHA = "2eaeb2c90ca2ef62d858a887fa1ee2091d680b17366bf5dd07d642d0fc8171bf"
sha = lambda data: hashlib.sha256(data).hexdigest()

parser = argparse.ArgumentParser()
parser.add_argument("clean_jp")
parser.add_argument("--out", required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
clean = Path(args.clean_jp).resolve()
assert sha(clean.read_bytes()) == JP_SHA, "Wrong clean Japanese source ROM"

with tempfile.TemporaryDirectory(prefix="riviera_s462_") as temporary:
    rc5_path = Path(temporary) / "s461_rc5.wsc"
    subprocess.run(
        [sys.executable, str(root.parent / "Riviera_S461_OVERLAY/rebuild.py"),
         str(clean), "--out", str(rc5_path)], check=True
    )
    rc5 = rc5_path.read_bytes()
    assert sha(rc5) == RC5_SHA
    rc6, report = build(rc5)

destination = Path(args.out)
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_bytes(rc6)
report.update({
    "source_chain": "JP clean -> S456 -> S457 -> S458 -> S459 -> S460 -> S461 -> S462",
    "source_jp_sha256": JP_SHA,
    "intermediate_rc5_sha256": RC5_SHA,
    "bps_used": False,
    "result": "PASS",
})
destination.with_suffix(".full-source-rebuild.json").write_text(
    json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)
print("S462_FULL_SOURCE_REBUILD_OK", sha(rc6))
