#!/usr/bin/env python3
"""Rebuild S460 RC4 through the full packaged historical source chain."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile

from build_s460 import build

JP_SHA = "62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921"
RC3_SHA = "c79079537ea5f66cf74f94d48afc3da14dd9db1f8458156d337f5e0107c111dd"
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

with tempfile.TemporaryDirectory(prefix="riviera_s460_") as temp:
    rc3_path = Path(temp) / "s459_rc3.wsc"
    subprocess.run([
        sys.executable,
        str(root.parent / "Riviera_S459_OVERLAY/rebuild.py"),
        str(clean),
        "--out",
        str(rc3_path),
    ], check=True)
    rc3 = rc3_path.read_bytes()
    assert sha(rc3) == RC3_SHA
    rc4, report = build(rc3)

assert sha(rc4) == RC4_SHA
dest = Path(args.out)
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_bytes(rc4)
report.update({
    "source_chain": "JP clean -> S456 cumulative source -> S457 -> S458 -> S459 -> S460",
    "source_jp_sha256": JP_SHA,
    "intermediate_rc3_sha256": RC3_SHA,
    "bps_used": False,
    "result": "PASS",
})
dest.with_suffix(".full-source-rebuild.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
print("S460_FULL_SOURCE_REBUILD_OK", sha(rc4))
