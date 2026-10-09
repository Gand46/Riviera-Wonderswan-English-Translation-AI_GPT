#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {"MANIFEST_SHA256.json", "SHA256SUMS.txt"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


files = []
for path in sorted(item for item in ROOT.rglob("*") if item.is_file()):
    relative = path.relative_to(ROOT).as_posix()
    if relative in EXCLUDED or "/__pycache__/" in f"/{relative}/":
        continue
    files.append({"path": relative, "size": path.stat().st_size, "sha256": sha256(path)})

(ROOT / "MANIFEST_SHA256.json").write_text(
    json.dumps(
        {
            "schema": "riviera-github-source-manifest-v1",
            "version": "v0.116 S463 RC7",
            "final_approved": False,
            "file_count": len(files),
            "files": files,
        },
        indent=2,
        ensure_ascii=False,
    )
    + "\n",
    encoding="utf-8",
)
(ROOT / "SHA256SUMS.txt").write_text(
    "".join(f"{record['sha256']}  {record['path']}\n" for record in files),
    encoding="utf-8",
)
print("MANIFESTS_OK", len(files))
