#!/usr/bin/env python3
"""Reveal and compare the mapping after the visual transcript is hash-locked."""
from pathlib import Path
import hashlib, json, unicodedata

ROOT = Path(__file__).resolve().parent
BUILD = json.loads((ROOT.parent / "Riviera_EN_v0.113_S460_RC4.build.json").read_text())

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def norm(text):
    value = unicodedata.normalize("NFC", text).replace("\r\n", "\n")
    value = value.replace("…", "...").replace("∼", "~").replace("—", "-")
    return "\n".join(line.rstrip() for line in value.strip().split("\n"))

lock = json.loads((ROOT / "TRANSCRIPTION_LOCK.json").read_text())
transcript = ROOT / lock["transcription_file"]
mapping = ROOT / lock["mapping_file"]
assert sha(transcript) == lock["transcription_sha256"]
assert sha(mapping) == lock["mapping_sha256_at_lock"]
visible = {row["blind_id"]: row for row in json.loads(transcript.read_text())}
sealed = json.loads(mapping.read_text())
assert len(visible) == len(sealed) == 32
rows = []
for expected in sealed:
    observed = visible[expected["blind_id"]]
    match = norm(observed["visible_transcription"]) == norm(expected["expected"])
    passed = match and observed["legibility"] == "PASS" and observed["clipping"] == "PASS" and observed["japanese_visible"] is False
    rows.append({
        "blind_id": expected["blind_id"], "stream": expected["stream"], "page": expected["page"],
        "boundary_rom": expected["boundary_rom"], "capture_sha256": expected["capture_sha256"],
        "visible_transcription": observed["visible_transcription"], "expected_after_reveal": expected["expected"],
        "visual_text_match": match, "legibility": observed["legibility"], "clipping": observed["clipping"],
        "japanese_visible": observed["japanese_visible"], "status": "PASS" if passed else "FAIL",
    })
report = {
    "scope": "32 unique full-screen epilogue pages across all ending routes",
    "method": "screenshots from the exact RC4 were randomized; visible text and layout were reviewed and hash-locked before the source mapping was revealed",
    "independence": "blind visual reading independent from the encoded source table; this is a second QA pass, not a claim of a separate human reviewer",
    "rom_sha256": BUILD["rom_sha256"], "transcription_sha256": lock["transcription_sha256"],
    "sealed_mapping_sha256": lock["mapping_sha256_at_lock"], "pages_total": len(rows),
    "pages_pass": sum(x["status"] == "PASS" for x in rows), "text_mismatches": sum(not x["visual_text_match"] for x in rows),
    "legibility_failures": sum(x["legibility"] != "PASS" for x in rows), "clipping_failures": sum(x["clipping"] != "PASS" for x in rows),
    "pages_with_visible_japanese": sum(bool(x["japanese_visible"]) for x in rows),
    "status": "PASS" if all(x["status"] == "PASS" for x in rows) else "FAIL",
    "normalization_used_for_comparison": {"ellipsis": "… equals ...", "wave_dash": "∼ equals ~", "em_dash": "— equals -", "reason": "plain-text equivalents only; line breaks and all letters had to match"},
    "rows": rows,
}
(ROOT / "BLIND_COMPARISON.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
(ROOT / "EPILOGUE_32_SECOND_READING.json").write_text(json.dumps({k:v for k,v in report.items() if k != "rows"}, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({k:v for k,v in report.items() if k != "rows"}, indent=2, ensure_ascii=False))
if report["status"] != "PASS": raise SystemExit(1)
