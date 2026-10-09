#!/usr/bin/env python3
"""Rebuild S460 RC4 from the exact clean Japanese ROM and packaged sources."""
from pathlib import Path
import argparse
import hashlib
import json
import sys

from build_s460 import build

JP_SHA = "62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921"
RC3_SHA = "c79079537ea5f66cf74f94d48afc3da14dd9db1f8458156d337f5e0107c111dd"
RC4_SHA = "931e5cfec6e60fe3ad2b48b192b38bfd071d1a3b2453ddac3e1c271fb8da3c7d"
RC3_PATCH = "Riviera_EN_v0.112_S459_RC3_CUMULATIVE_FROM_JP.bps"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument("clean_jp")
parser.add_argument("--out", required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
package = root.parent.parent
vendor = package / "sources/Riviera_S457_FULL_SOURCE/scripts/vendor"
sys.path.insert(0, str(vendor))
from ws_patch_tools import bps  # noqa: E402

clean = Path(args.clean_jp).read_bytes()
assert sha(clean) == JP_SHA, "Wrong clean Japanese source ROM"
patch_path = package / "patches" / RC3_PATCH
rc3 = bps.apply(clean, patch_path.read_bytes())
assert sha(rc3) == RC3_SHA, "Packaged RC3 base did not rebuild exactly"
rc4, report = build(rc3)
assert sha(rc4) == RC4_SHA, "S460 output identity mismatch"

dest = Path(args.out)
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_bytes(rc4)
report.update({
    "source_chain": "JP clean -> packaged S459 cumulative BPS -> S460 source overlay",
    "source_jp_sha256": JP_SHA,
    "intermediate_rc3_sha256": RC3_SHA,
    "bps_used_for_prior_base": True,
    "s460_built_from_source": True,
    "result": "PASS",
})
dest.with_suffix(".source-rebuild.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
print("S460_SOURCE_REBUILD_OK", sha(rc4))
