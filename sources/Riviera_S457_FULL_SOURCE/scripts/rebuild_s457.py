#!/usr/bin/env python3
"""Rebuild S457 from the clean JP ROM and split cumulative S456 sources."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

from build_s457 import build, sha


ROOT = Path(__file__).resolve().parents[1]
PARTS_DIR = ROOT / "upstream_parts"
PARTS_MANIFEST = PARTS_DIR / "UPSTREAM_PARTS.json"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assemble_upstream(destination: Path) -> None:
    manifest = json.loads(PARTS_MANIFEST.read_text(encoding="utf-8"))
    with destination.open("wb") as output:
        for record in manifest["parts"]:
            part = PARTS_DIR / record["name"]
            assert part.stat().st_size == record["size"], f"Wrong part size: {part.name}"
            assert file_sha256(part) == record["sha256"], f"Wrong part hash: {part.name}"
            with part.open("rb") as source:
                shutil.copyfileobj(source, output, 1024 * 1024)
    assert destination.stat().st_size == manifest["assembled_size"]
    assert file_sha256(destination) == manifest["assembled_sha256"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("clean", help="Clean Japanese Riviera WSC ROM")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    clean = Path(args.clean).resolve()
    spec = json.loads((ROOT / "source/RELEASE.json").read_text(encoding="utf-8"))
    assert sha(clean.read_bytes()) == spec["clean_sha256"], "Wrong clean JP ROM"

    with tempfile.TemporaryDirectory(prefix="riviera_s457_") as temporary:
        temp = Path(temporary)
        archive = temp / "Riviera_S456_Fuentes_Completas_BPS_QA.zip"
        assemble_upstream(archive)
        assert file_sha256(archive) == spec["upstream_sha256"]

        extracted = temp / "S456"
        with zipfile.ZipFile(archive) as upstream:
            for item in upstream.infolist():
                assert (extracted / item.filename).resolve().is_relative_to(extracted.resolve())
            upstream.extractall(extracted)

        base = temp / "rebuilt_S456.wsc"
        subprocess.run(
            [
                sys.executable,
                str(extracted / "Riviera_S456_FULL_SOURCE/scripts/rebuild_s456.py"),
                str(clean),
                "--out",
                str(base),
            ],
            check=True,
        )
        output, report = build(base.read_bytes())

    destination = Path(args.out)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(output)
    destination.with_suffix(".rebuild.json").write_text(
        json.dumps(
            {
                "source_chain": "CLEAN_JP -> cumulative S456 sources -> S457",
                "upstream_transport": "three GitHub-safe parts, hash-verified and assembled in a temporary directory",
                "bps_used": False,
                "rom_sha256": sha(output),
                "result": "PASS",
                "builder_report": report,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print("S457_SOURCE_REBUILD_OK", sha(output))


if __name__ == "__main__":
    main()
