"""Build Riviera English v0.112-S459-RC3 from cumulative sources."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
JP_SHA256 = "62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921"
RC3_SHA256 = "c79079537ea5f66cf74f94d48afc3da14dd9db1f8458156d337f5e0107c111dd"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("clean_jp", type=Path)
    parser.add_argument("output", nargs="?", type=Path, default=ROOT / "build" / "Riviera-English-v0.112-S459-RC3.wsc")
    args = parser.parse_args()
    source = args.clean_jp.resolve()
    output = args.output.resolve()
    if sha256(source) != JP_SHA256:
        raise SystemExit("ERROR: the source is not the required clean Japanese ROM")
    if output == source:
        raise SystemExit("ERROR: output must be different from the source ROM")
    if output.exists():
        raise SystemExit("ERROR: output already exists")
    output.parent.mkdir(parents=True, exist_ok=True)
    rebuild = ROOT / "source" / "Riviera_S459_OVERLAY" / "rebuild.py"
    subprocess.run([sys.executable, str(rebuild), str(source), "--out", str(output)], check=True)
    actual = sha256(output)
    if actual != RC3_SHA256:
        output.unlink(missing_ok=True)
        raise SystemExit(f"ERROR: unexpected RC3 output hash: {actual}")
    print(f"PASS: {output}")
    print(f"SHA-256: {actual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
