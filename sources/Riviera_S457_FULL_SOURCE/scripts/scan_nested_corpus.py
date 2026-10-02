#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import io
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
START = ROOT / "source/Riviera_S457_FULL_SOURCE/upstream/Riviera_S456_Fuentes_Completas_BPS_QA.zip"
OUT = ROOT / "mined_corpus"
KEYWORDS = re.compile(
    r"(1436|bank66|corpus|resources_current|i03_uses|pointer_checks|"
    r"owners_requiring_context|manual_rows|items\.json$|auditoria_estado|"
    r"phase5_master_ledger|phase5_known_families|s398_summary|"
    r"coverage_gaps|known_resources|technical_residues|residues47|"
    r"classification_47)",
    re.IGNORECASE,
)
MAX_SELECTED_BYTES = 8 * 1024 * 1024


def safe_name(stage: int, member: str, payload: bytes) -> str:
    base = Path(member).name
    digest = hashlib.sha256(member.encode()).hexdigest()[:12]
    return f"{stage:02d}_{digest}_{base}"


def scan_zip(source: Path | bytes, stage: int) -> tuple[bytes | None, dict[str, object]]:
    handle = source if isinstance(source, Path) else io.BytesIO(source)
    selected: list[dict[str, object]] = []
    with zipfile.ZipFile(handle) as archive:
        infos = archive.infolist()
        for info in infos:
            if info.is_dir() or info.file_size > MAX_SELECTED_BYTES or not KEYWORDS.search(info.filename):
                continue
            payload = archive.read(info)
            name = safe_name(stage, info.filename, payload)
            (OUT / name).write_bytes(payload)
            selected.append(
                {
                    "member": info.filename,
                    "output": name,
                    "bytes": len(payload),
                    "sha256": hashlib.sha256(payload).hexdigest(),
                }
            )
        upstream = [
            info for info in infos
            if not info.is_dir() and info.filename.lower().endswith(".zip")
            and ("upstream" in info.filename.lower() or "fuentes_completas" in info.filename.lower())
        ]
        next_info = max(upstream, key=lambda item: item.file_size, default=None)
        next_bytes = archive.read(next_info) if next_info else None
        report = {
            "stage": stage,
            "entries": len(infos),
            "all_members": [info.filename for info in infos] if stage >= 16 else None,
            "selected": selected,
            "next_member": next_info.filename if next_info else None,
            "next_bytes": len(next_bytes) if next_bytes else 0,
        }
    return next_bytes, report


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    reports: list[dict[str, object]] = []
    source: Path | bytes = START
    for stage in range(30):
        next_bytes, report = scan_zip(source, stage)
        reports.append(report)
        print(stage, report["entries"], len(report["selected"]), report["next_member"])
        if next_bytes is None:
            break
        source = next_bytes
    (OUT / "SCAN_REPORT.json").write_text(
        json.dumps(reports, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
