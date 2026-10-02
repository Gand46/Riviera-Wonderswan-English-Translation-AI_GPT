"""Apply the cumulative RC3 BPS to the identified clean Japanese ROM."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "source" / "Riviera_S457_FULL_SOURCE" / "scripts" / "vendor"))
from ws_patch_tools.bps import apply  # noqa: E402

JP_SHA256 = "62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921"
BPS_SHA256 = "0d90bce872e7383497b90ef6051bf197260eb2ddc1ea4dd9c2d63c36c0e40504"
RC3_SHA256 = "c79079537ea5f66cf74f94d48afc3da14dd9db1f8458156d337f5e0107c111dd"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("clean_jp", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    source_path = args.clean_jp.resolve()
    output_path = args.output.resolve()
    if source_path == output_path:
        raise SystemExit("ERROR: output must be different from the source ROM")
    if output_path.exists():
        raise SystemExit("ERROR: output already exists")
    source = source_path.read_bytes()
    if digest(source) != JP_SHA256:
        raise SystemExit("ERROR: the source is not the required clean Japanese ROM")
    patch = (ROOT / "patches" / "Riviera_EN_v0.112_S459_RC3_CUMULATIVE_FROM_JP.bps").read_bytes()
    if digest(patch) != BPS_SHA256:
        raise SystemExit("ERROR: cumulative BPS hash mismatch")
    result = apply(source, patch)
    if digest(result) != RC3_SHA256:
        raise SystemExit("ERROR: patched output does not match RC3")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(result)
    print(f"PASS: {output_path}")
    print(f"SHA-256: {RC3_SHA256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
