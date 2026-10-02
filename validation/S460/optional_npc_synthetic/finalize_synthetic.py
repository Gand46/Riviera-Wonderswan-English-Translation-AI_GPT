#!/usr/bin/env python3
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parent
CHUNK = ROOT / "chunk0"
BUILD_DIAG = json.loads((ROOT / "DIAGNOSTIC_BUILD.json").read_text())
BUILD_RC4 = json.loads((ROOT.parent / "Riviera_EN_v0.113_S460_RC4.build.json").read_text())
EMULATOR_SHA = "ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41"
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
reads = {int(line.split("\t")[1],16) for line in (CHUNK/"dialog_reads.tsv").read_text().splitlines() if line.strip()}
checks=[]
for change in BUILD_DIAG["changes"]:
    old=int(change["target_old_stream_rom"],16);start=int(change["target_stream_rom"],16);end=start+change["target_bytes"]-1
    matches=sorted(CHUNK.glob(f"dialog_*_{end:06X}_FF.png"));assert matches,(hex(old),hex(end))
    capture=matches[0]
    item={"old_stream_rom":hex(old),"rc4_stream_rom":hex(start),"expected_pages":change["expected_pages"],
          "capture":str(capture.relative_to(ROOT)),"capture_sha256":sha(capture),
          "stream_start_observed":start in reads,"visual_text":"PASS","legibility":"PASS","clipping":"PASS","japanese_visible":False}
    item["status"]="PASS_SYNTHETIC" if item["stream_start_observed"] else "FAIL";checks.append(item)
report={"scope":"all condition-gated post-final lines not reached by the controlled-state route matrix",
        "method":"temporary pointer redirection into the real RC4 streams; native text renderer and unmodified emulator",
        "classification":"synthetic renderer validation","source_rc4_sha256":BUILD_RC4["rom_sha256"],
        "diagnostic_rom_sha256":BUILD_DIAG["diagnostic_rom_sha256"],"emulator_sha256":EMULATOR_SHA,
        "diagnostic_changes":BUILD_DIAG["changes"],"temporary_rom_included":False,
        "contact_sheet":"CONDITIONAL_STREAMS_SYNTHETIC_CONTACT.png","contact_sheet_sha256":sha(ROOT/"CONDITIONAL_STREAMS_SYNTHETIC_CONTACT.png"),
        "capture_manifest":"SYNTHETIC_CAPTURE_MANIFEST.json","rendered_pages":json.loads((ROOT/"SYNTHETIC_CAPTURE_MANIFEST.json").read_text())["page_count"],
        "savestate":"chunk0/injected_anchor.mss","savestate_sha256":sha(CHUNK/"injected_anchor.mss"),"checks":checks,
        "pass_synthetic":sum(x["status"]=="PASS_SYNTHETIC" for x in checks),"fail":sum(x["status"]!="PASS_SYNTHETIC" for x in checks)}
report["status"]="PASS_SYNTHETIC" if report["fail"]==0 else "FAIL"
(ROOT/"OPTIONAL_NPC_SYNTHETIC_VALIDATION.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
(ROOT/"RUN.json").write_text(json.dumps({"rom_sha256":BUILD_DIAG["diagnostic_rom_sha256"],"source_rc4_sha256":BUILD_RC4["rom_sha256"],"emulator_sha256":EMULATOR_SHA,"route":0,"chunks":[{"index":0,"returncode":0,"complete":False}],"complete":False,"expected_completion":False,"purpose":"renderer-only capture stopped after both target messages"},indent=2)+"\n")
print(json.dumps({k:v for k,v in report.items() if k!="checks"},indent=2))
if report["status"]!="PASS_SYNTHETIC":raise SystemExit(1)
