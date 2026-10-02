"""Verify repository identities, GitHub file limits and prohibited file types."""
from __future__ import annotations

import hashlib
import io
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BPS_SHA256 = "0d90bce872e7383497b90ef6051bf197260eb2ddc1ea4dd9c2d63c36c0e40504"
UPSTREAM_SHA256 = "1e2f381ef0186d5763dc762047db1978f8eff520351f3cdd70db5eb3d78db9b7"
FORBIDDEN = {".wsc", ".ws", ".rom", ".gba", ".gb", ".gbc", ".bios", ".srm", ".sav", ".mss"}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_zip(data: bytes, label: str, depth: int = 0) -> int:
    if depth > 24:
        raise SystemExit(f"ERROR: unexpected archive depth: {label}")
    count = 1
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for entry in archive.infolist():
            if entry.is_dir():
                continue
            name = entry.filename.lower()
            if Path(name).suffix in FORBIDDEN or name.endswith((".state", ".eep", ".pyc")):
                raise SystemExit(f"ERROR: prohibited nested file: {label}/{entry.filename}")
            if entry.file_size == 8_388_608 and not name.endswith((".csv", ".json", ".jsonl")):
                raise SystemExit(f"ERROR: ROM-sized nested file needs review: {label}/{entry.filename}")
            if name.endswith(".zip"):
                count += inspect_zip(archive.read(entry), f"{label}/{entry.filename}", depth + 1)
    return count


def main() -> int:
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    forbidden = [path.relative_to(ROOT) for path in files if path.suffix.lower() in FORBIDDEN]
    oversized = [(path.relative_to(ROOT), path.stat().st_size) for path in files if path.stat().st_size >= 100_000_000]
    if forbidden:
        raise SystemExit(f"ERROR: prohibited files: {forbidden}")
    if oversized:
        raise SystemExit(f"ERROR: GitHub-incompatible files: {oversized}")
    bps = ROOT / "patches" / "Riviera_EN_v0.112_S459_RC3_CUMULATIVE_FROM_JP.bps"
    if bps.stat().st_size != 284345 or file_sha256(bps) != BPS_SHA256:
        raise SystemExit("ERROR: cumulative BPS identity mismatch")
    parts = sorted((ROOT / "source" / "Riviera_S457_FULL_SOURCE" / "upstream").glob("*.zip.part*"))
    if len(parts) != 4:
        raise SystemExit("ERROR: expected four S456 source chunks")
    digest = hashlib.sha256()
    total = 0
    for part in parts:
        data = part.read_bytes()
        digest.update(data)
        total += len(data)
    if total != 145694256 or digest.hexdigest() != UPSTREAM_SHA256:
        raise SystemExit("ERROR: S456 source archive chunks do not reconstruct the expected archive")
    nested = inspect_zip(b"".join(part.read_bytes() for part in parts), "S456")
    print(f"PASS: {len(files)} files; no ROM/BIOS/save files; all files below 100 MB")
    print(f"PASS: cumulative BPS {BPS_SHA256}")
    print(f"PASS: cumulative S456 source archive {UPSTREAM_SHA256}; {nested} nested ZIPs scanned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
