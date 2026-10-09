#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import stat
import zipfile


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT.parent / f"{ROOT.name}.zip"
TIMESTAMP = (2026, 10, 2, 0, 0, 0)

with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(item for item in ROOT.rglob("*") if item.is_file()):
        relative = (Path(ROOT.name) / path.relative_to(ROOT)).as_posix()
        info = zipfile.ZipInfo(relative, TIMESTAMP)
        executable = path.name in {"BUILD.command", "build_rc5.py", "build_rc6.py", "verify_package.py"} or path.parent.name == "tools"
        info.external_attr = (stat.S_IFREG | (0o755 if executable else 0o644)) << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        with path.open("rb") as source, archive.open(info, "w") as destination:
            while chunk := source.read(1024 * 1024):
                destination.write(chunk)
print(OUTPUT)
