#!/usr/bin/env python3
"""Verify the S457 binary, cumulative patches, and the bounded B4 evidence."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET_SHA = "80ff36655d83956d96b634adafc685fa4379da326c3d45099dedcb73ef72a951"
BASE_SHA = "b6ae03cda1be9d1742ca7aae3cfc32fe389c3fd51e9e3bc5b4929ff3653dcdc1"
CLEAN_SHA = "62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921"
FONT_START = 0x5534BC
FONT_LEN = 52 * 50


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_builder():
    spec = importlib.util.spec_from_file_location("build_s457", ROOT / "scripts/build_s457.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def apply_ips(source: bytes, patch: bytes) -> bytes:
    assert patch[:5] == b"PATCH"
    pos = 5
    out = bytearray(source)
    while patch[pos:pos + 3] != b"EOF":
        offset = int.from_bytes(patch[pos:pos + 3], "big")
        size = int.from_bytes(patch[pos + 3:pos + 5], "big")
        pos += 5
        if size:
            payload = patch[pos:pos + size]
            pos += size
        else:
            run = int.from_bytes(patch[pos:pos + 2], "big")
            payload = patch[pos + 2:pos + 3] * run
            pos += 3
        end = offset + len(payload)
        if end > len(out):
            out.extend(b"\0" * (end - len(out)))
        out[offset:end] = payload
    return bytes(out)


def file_hashes(folder: Path, pattern: str) -> dict[str, str]:
    return {p.name: sha(p.read_bytes()) for p in sorted(folder.glob(pattern))}


def check_evidence(evidence: Path, release: dict) -> dict:
    credit_root = evidence / "credits"
    comparison = json.loads((ROOT / "analysis/B4/CREDIT_RUNTIME_COMPARISON.json").read_text())
    assert len(comparison) == 13
    assert [x["page"] for x in comparison if x["changed_bytes"]] == [0, 2, 4, 5]
    allowed_by_page = {0: (0x59E0, 3840), 2: (0x59E0, 1920), 4: (0x5B60, 1536), 5: (0x59E0, 6144)}
    credit_results = []
    for page in range(13):
        a = credit_root / "S456" / f"page_{page:02d}" / "runtime"
        b = credit_root / "S457" / f"page_{page:02d}" / "runtime"
        guard = json.loads((b / "hook_guard.json").read_text())
        assert guard["register_errors"] == guard["unexpected_writes"] == 0
        old = (a / f"page_{page:02d}.bin").read_bytes()
        new = (b / f"page_{page:02d}.bin").read_bytes()
        assert len(old) == len(new) == 65536
        changed = [i for i, pair in enumerate(zip(old, new)) if pair[0] != pair[1]]
        expected = comparison[page]
        assert len(changed) == expected["changed_bytes"]
        if page in allowed_by_page:
            start, length = allowed_by_page[page]
            assert changed and min(changed) >= start and max(changed) < start + length
        else:
            assert not changed
        # The two animation-table destinations remain exact for every page.
        assert old[0xD6A3:0xD7C3] == new[0xD6A3:0xD7C3]
        assert old[0xC962:0xCA82] == new[0xC962:0xCA82]
        credit_results.append({"page": page, "changed_bytes": len(changed), "guards": "PASS"})

    blind = json.loads((ROOT / "analysis/B4/GLYPH_BLIND_TRANSCRIPTION.json").read_text())
    assert blind["all_11_correct"] is True and blind["runtime_capital_i_samples"] == 4

    baseline = json.loads((ROOT / "analysis/B4/BATTLE_FRAME_HASHES_S455.json").read_text())
    battle = file_hashes(evidence / "battle/S457", "frame_*.png")
    assert len(battle) == 83 and battle == baseline
    battle_report = json.loads((evidence / "battle/S457/report.json").read_text())
    assert battle_report["capture_complete"] is True and battle_report["frames"] == 2500

    intro_old = file_hashes(evidence / "intro/S456", "frame_*.png")
    intro_new = file_hashes(evidence / "intro/S457", "frame_*.png")
    assert len(intro_old) == len(intro_new) == 15 and intro_old == intro_new
    for version in ("S456", "S457"):
        report = json.loads((evidence / f"intro/{version}/report.json").read_text())
        assert report["passed"] is True and report["captures"] == 15 and report["end_frame"] == 4800

    team = json.loads((evidence / "team/controlled/report.json").read_text())
    assert team == {
        "frames": 362,
        "saved": True,
        "positive_read_control": True,
        "rom_mutated": False,
        "access": "controlled_native_screen_entry",
    }
    assert (evidence / "team/controlled/frame_00360.png").is_file()

    return {
        "credits": {"pages": 13, "changed_pages": [0, 2, 4, 5], "guards": "PASS", "details": credit_results},
        "isolated_glyphs": "PASS_11_OF_11",
        "battle": "PASS_83_OF_83_EXACT_TO_S455",
        "prologue": "PASS_15_OF_15_EXACT_S456_TO_S457",
        "team_edit": "PASS_CONTROLLED_NATIVE_SCREEN_ENTRY",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("clean", type=Path)
    ap.add_argument("base_s456", type=Path)
    ap.add_argument("candidate_s457", type=Path)
    ap.add_argument("rebuilt_s457", type=Path)
    ap.add_argument("--evidence", type=Path, default=ROOT / "evidence")
    ap.add_argument("--output", type=Path, default=ROOT / "analysis/B4/VERIFICATION_S457.json")
    args = ap.parse_args()

    clean = args.clean.read_bytes()
    base = args.base_s456.read_bytes()
    candidate = args.candidate_s457.read_bytes()
    rebuilt = args.rebuilt_s457.read_bytes()
    assert len(clean) == len(base) == len(candidate) == len(rebuilt) == 8388608
    assert sha(clean) == CLEAN_SHA and sha(base) == BASE_SHA
    assert sha(candidate) == sha(rebuilt) == TARGET_SHA
    assert int.from_bytes(candidate[-2:], "little") == sum(candidate[:-2]) & 0xFFFF == 0xD44D

    release = json.loads((ROOT / "source/RELEASE.json").read_text())
    assert release["target_sha256"] == TARGET_SHA and release["checksum"] == "D44D"
    builder = load_builder()
    built, built_meta = builder.build(base)
    assert built == candidate and built_meta["target_sha256"] == TARGET_SHA

    sys.path.insert(0, str(ROOT / "scripts/vendor"))
    from ws_patch_tools import bps
    bps_result = bps.apply(clean, (ROOT / "patches/Riviera_CLEAN_JP_to_v0110_S457_cumulative.bps").read_bytes())
    ips_result = apply_ips(clean, (ROOT / "patches/Riviera_CLEAN_JP_to_v0110_S457_cumulative.ips").read_bytes())
    assert bps_result == ips_result == candidate

    diffs = [i for i, pair in enumerate(zip(base, candidate)) if pair[0] != pair[1]]
    allowed = set(range(release["stub_address"], release["owned_region_end"]))
    for block in release["older_blocks"]:
        allowed.update(range(block["source"], block["source"] + block["length"]))
    allowed.update(range(len(candidate) - 2, len(candidate)))
    assert len(diffs) == release["changed_bytes"] == 7361 and set(diffs) <= allowed
    assert base[FONT_START:FONT_START + FONT_LEN] == candidate[FONT_START:FONT_START + FONT_LEN]
    assert sha(candidate[FONT_START:FONT_START + FONT_LEN]) == release["native_font_sha256"]
    hook = json.loads((ROOT / "source/S455_RELEASE.json").read_text())["hook"]
    assert base[hook:hook + 16] == candidate[hook:hook + 16]

    animation = [b for b in release["blocks"] if b["kind"] == "animation_table"]
    prior = {b["id"]: b["sha256"] for b in json.loads((ROOT / "source/S455_RELEASE.json").read_text())["blocks"] if b["kind"] == "animation_table"}
    assert animation and all(b["sha256"] == prior[b["id"]] for b in animation)

    evidence_result = check_evidence(args.evidence, release)
    result = {
        "stage": "S457",
        "version": "0.110",
        "result": "PASS_SCOPED_B4_PARTIAL",
        "binary": {
            "clean_sha256": sha(clean),
            "base_sha256": sha(base),
            "target_sha256": sha(candidate),
            "source_rebuild_exact": True,
            "bps_roundtrip_exact": True,
            "ips_roundtrip_exact": True,
            "checksum": "D44D",
            "changed_bytes": len(diffs),
            "unexpected_changed_offsets": 0,
            "global_font_changed": False,
            "dispatch_hook_changed": False,
            "animation_payloads_changed": False,
        },
        "runtime": evidence_result,
        "scope": {
            "capital_i_issue": "RESOLVED_IN_FOUR_COMPILED_CREDIT_GRAPHICS",
            "word_level_blind_review": "NOT_VALIDATED",
            "team_edit_natural_progression": "NOT_VALIDATED",
            "dialogue_tutorial_surface_matrix": "PARTIAL",
            "global_visual_approved": False,
            "global_final_approved": False,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print("S457_VERIFY_OK", TARGET_SHA)


if __name__ == "__main__":
    main()
