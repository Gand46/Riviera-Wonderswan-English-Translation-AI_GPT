#!/usr/bin/env python3
"""Validate GitHub package cleanliness, identities and split source transport."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_BPS = "89e0ad8f6ccce32122e467be1211943b5641ad18ede44301fb1e4a6b1789eee4"
MAX_GITHUB_FILE = 100 * 1024 * 1024
FORBIDDEN_EXTENSIONS = {
    ".dll", ".exe", ".ieeprom", ".pyc", ".rom", ".sav", ".so", ".srm", ".ws", ".wsc"
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", help="Optional report path relative to the repository root")
    args = parser.parse_args()

    failures: list[str] = []
    manifest_names = {"MANIFEST_SHA256.json", "SHA256SUMS.txt"}
    files = [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and path.relative_to(ROOT).as_posix() not in manifest_names
    ]
    for path in files:
        relative = path.relative_to(ROOT)
        if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
            failures.append(f"forbidden file: {relative}")
        if path.stat().st_size >= MAX_GITHUB_FILE:
            failures.append(f"file reaches GitHub 100 MiB limit: {relative}")
        if "__pycache__" in path.parts or "work" in path.parts:
            failures.append(f"generated path: {relative}")

    bps = ROOT / "patches/Riviera_EN_v0.114_S461_RC5_CUMULATIVE_FROM_JP.bps"
    if not bps.is_file() or sha256(bps) != EXPECTED_BPS:
        failures.append("RC5 cumulative BPS hash mismatch")

    parts_dir = ROOT / "sources/Riviera_S457_FULL_SOURCE/upstream_parts"
    parts_manifest = json.loads((parts_dir / "UPSTREAM_PARTS.json").read_text(encoding="utf-8"))
    combined = hashlib.sha256()
    combined_size = 0
    for record in parts_manifest["parts"]:
        part = parts_dir / record["name"]
        if not part.is_file():
            failures.append(f"missing source part: {record['name']}")
            continue
        if part.stat().st_size != record["size"] or sha256(part) != record["sha256"]:
            failures.append(f"source part mismatch: {record['name']}")
        with part.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                combined.update(chunk)
                combined_size += len(chunk)
    if combined_size != parts_manifest["assembled_size"]:
        failures.append("assembled source size mismatch")
    if combined.hexdigest() != parts_manifest["assembled_sha256"]:
        failures.append("assembled source hash mismatch")

    release = json.loads((ROOT / "release/RELEASE.json").read_text(encoding="utf-8"))
    if release.get("version") != "v0.114 S461 RC5" or release.get("final_approved") is not False:
        failures.append("release state mismatch")

    result = {
        "result": "FAIL" if failures else "PASS",
        "version": "v0.114 S461 RC5",
        "final_approved": False,
        "files_checked": len(files),
        "largest_file_bytes": max(path.stat().st_size for path in files),
        "cumulative_bps_sha256": sha256(bps) if bps.is_file() else None,
        "assembled_s456_source_sha256": combined.hexdigest(),
        "failures": failures,
    }
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.write_report:
        report_path = (ROOT / args.write_report).resolve()
        assert report_path.is_relative_to(ROOT.resolve())
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
