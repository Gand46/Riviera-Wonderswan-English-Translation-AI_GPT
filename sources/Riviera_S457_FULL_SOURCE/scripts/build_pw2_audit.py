#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "recovered_pw1/pw2_inputs"
MINED = ROOT / "mined_corpus"
ROM_PATH = ROOT / "rom/Riviera_v0110_S457_PW2.wsc"
OUT = ROOT / "deliverables"
EXPECTED_ROM_SHA256 = "80ff36655d83956d96b634adafc685fa4379da326c3d45099dedcb73ef72a951"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(name: str, payload: object) -> None:
    (OUT / name).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def label_for(resource: dict) -> str:
    labels = [str(value) for value in resource.get("labels_from_sources", []) if value]
    return " | ".join(labels)


def width_proxy(text: str) -> int:
    if not text:
        return 0
    return max(
        sum(3 if char == " " else 6 for char in line)
        for line in text.splitlines() or [text]
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rom = ROM_PATH.read_bytes()
    rom_sha = hashlib.sha256(rom).hexdigest()
    assert rom_sha == EXPECTED_ROM_SHA256, rom_sha

    # S456 is the current 1,766-resource inventory. It differs from the S455
    # PW1 seed only in the documented Rapier correction and matches S457 fully.
    resources = read_json(MINED / "00_2634183fbfdb_RESOURCES_CURRENT.json")
    uses = read_json(INPUT / "I03_USES.json")
    pointer_checks = read_json(INPUT / "POINTER_CHECKS.json")
    context_owners = read_json(INPUT / "OWNERS_REQUIRING_CONTEXT.json")
    residues = read_json(MINED / "01_d7ce2834402c_RESIDUES47_CURRENT.json")
    historical_ledger = MINED / "16_64010c03e830_PHASE5_MASTER_LEDGER_S431.csv"

    assert len(resources) == 1766
    assert len(uses) == 3418
    assert len(pointer_checks) == 3325
    assert len(context_owners) == 93
    assert len(residues) == 47

    uses_by_resource: dict[str, list[dict]] = defaultdict(list)
    uses_by_id = {row["id"]: row for row in uses}
    for row in uses:
        uses_by_resource[row["resource_id"]].append(row)
    context_ids = {row["id"] for row in context_owners}

    matrix = []
    hash_mismatches = []
    for resource in sorted(resources, key=lambda row: (row["start"], row["id"])):
        start = int(resource["start"])
        end = int(resource["end_exclusive"])
        assert 0 <= start < end <= len(rom), resource["id"]
        current_hash = hashlib.sha256(rom[start:end]).hexdigest()
        hash_ok = current_hash == resource["stored_sha256"]
        if not hash_ok:
            hash_mismatches.append(resource["id"])
        bound_uses = uses_by_resource.get(resource["id"], [])
        consumers = sorted(
            {consumer for use in bound_uses for consumer in use.get("consumer_ids", [])}
        )
        label = label_for(resource)
        proxy = width_proxy(label)
        matrix.append(
            {
                "stable_id": resource["id"],
                "kind": resource["kind"],
                "physical_start": f"0x{start:06X}",
                "physical_end_exclusive": f"0x{end:06X}",
                "bank": f"0x{start // 0x10000:02X}",
                "bank_offset": f"0x{start % 0x10000:04X}",
                "stored_bytes": end - start,
                "stored_sha256": resource["stored_sha256"],
                "s457_hash_match": hash_ok,
                "source_text": "UNAVAILABLE_HISTORICAL" if resource["kind"] in {"TEXT", "SCRIPT"} else "N/A",
                "integrated_label": label,
                "family_sources": ";".join(resource.get("source_documents", [])),
                "use_count": len(bound_uses),
                "owner_ids": ";".join(use["id"] for use in bound_uses),
                "consumer_ids": ";".join(consumers),
                "needs_context": any(use["id"] in context_ids for use in bound_uses),
                "width_proxy_max_line_px": proxy,
                "overflow_risk_estimate": "NEEDS_VISUAL_WIDTH" if resource["kind"] == "TEXT" and proxy > 96 else "NO_FLAG",
                "linguistic_status": resource.get("linguistic_status", "NOT_INDEXED"),
                "visual_status": resource.get("visual_status", "NOT_INDEXED"),
                "runtime_status": resource.get("runtime_status", "NOT_INDEXED"),
                "translation_status": resource.get("translation_status", "NOT_INDEXED"),
                "integration_status": resource.get("integration_status", "NOT_INDEXED"),
            }
        )
    assert not hash_mismatches, hash_mismatches

    fields = list(matrix[0])
    with (OUT / "RESOURCE_MATRIX_1766.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(matrix)
    write_json("RESOURCE_MATRIX_1766.json", matrix)

    current_direct_records = []
    for use in uses:
        encoded = use.get("table_bytes")
        owner = use.get("owner_physical")
        if not encoded or owner is None:
            continue
        expected = bytes.fromhex(encoded)
        actual = rom[owner : owner + len(expected)]
        current_direct_records.append(
            {
                "id": use["id"],
                "owner": f"0x{owner:06X}",
                "expected_hex": encoded,
                "actual_hex": actual.hex(),
                "match": actual == expected,
            }
        )
    assert len(current_direct_records) == 147
    assert all(row["match"] for row in current_direct_records)
    assert all(row["match"] for row in pointer_checks)
    pointer_result = {
        "result": "PASS_STATIC_SCOPED",
        "rom_sha256": rom_sha,
        "inherited_pointer_checks": len(pointer_checks),
        "inherited_pointer_mismatches": sum(not row["match"] for row in pointer_checks),
        "s457_direct_table_records_checked": len(current_direct_records),
        "s457_direct_table_record_mismatches": sum(not row["match"] for row in current_direct_records),
        "context_owner_uses": len(context_owners),
        "note": "3,325 family-aware pointer checks remain valid in the inherited ledger; 147 records with retained raw table bytes were independently byte-checked on S457. The 93 ownerless-context uses remain a context queue, not pointer failures.",
        "direct_records": current_direct_records,
    }
    write_json("POINTER_AUDIT.json", pointer_result)

    interval_groups: dict[tuple[int, int], list[str]] = defaultdict(list)
    hash_groups: dict[str, list[str]] = defaultdict(list)
    for resource in resources:
        interval_groups[(resource["start"], resource["end_exclusive"])].append(resource["id"])
        hash_groups[resource["stored_sha256"]].append(resource["id"])
    no_i03 = [resource for resource in resources if resource["id"] not in uses_by_resource]
    duplicate_hashes = [
        {"sha256": key, "resource_ids": ids}
        for key, ids in sorted(hash_groups.items()) if len(ids) > 1
    ]
    inventory_result = {
        "result": "PASS_STATIC_WITH_OPEN_CONSUMER_EDGES",
        "resource_count": len(resources),
        "resource_hash_matches": len(resources) - len(hash_mismatches),
        "resource_hash_mismatches": hash_mismatches,
        "duplicate_interval_groups": sum(len(ids) > 1 for ids in interval_groups.values()),
        "duplicate_content_hash_groups": len(duplicate_hashes),
        "duplicate_content_hashes": duplicate_hashes,
        "resources_with_i03_edges": len(resources) - len(no_i03),
        "resources_without_i03_edges": len(no_i03),
        "without_i03_by_kind": dict(Counter(row["kind"] for row in no_i03)),
        "without_i03_ids": [row["id"] for row in no_i03],
        "note": "Without an I03 edge means consumer linkage is absent from this inventory; it does not prove the resource is unused or orphaned in the ROM.",
    }
    write_json("INVENTORY_ORPHAN_DUPLICATE_AUDIT.json", inventory_result)

    residue_counts = Counter(row["status"] for row in residues)
    unresolved_residues = [row for row in residues if row["status"] == "UNRESOLVED_TECHNICAL_NOT_CONFIRMED_TEXT"]
    assert {row["id"] for row in unresolved_residues} == {"CP932-15939", "CP932-15968"}
    residue_result = {
        "result": "45_CLASSIFIED_2_NOT_VALIDATED",
        "total": len(residues),
        "by_status": dict(residue_counts),
        "translation_debt_confirmed": 0,
        "unresolved_ids": [row["id"] for row in unresolved_residues],
        "rom_changed": False,
        "items": residues,
    }
    write_json("RESIDUAL_AUDIT_47.json", residue_result)

    risk_rows = [row for row in matrix if row["overflow_risk_estimate"] != "NO_FLAG"]
    visual_rows = [row for row in matrix if "PASS" not in row["visual_status"] and "APPROVED" not in row["visual_status"]]
    context_resources = sorted(
        {uses_by_id[row["id"]]["resource_id"] for row in context_owners if row["id"] in uses_by_id}
    )
    qa_queues = {
        "PASS_STATIC": {
            "count": len(matrix),
            "basis": "S457 stored interval hash equals the current S456 inventory; this is not linguistic or visual approval.",
            "ids": [row["stable_id"] for row in matrix],
        },
        "NEEDS_CONTEXT": {
            "use_count": len(context_owners),
            "resource_count": len(context_resources),
            "use_ids": sorted(context_ids),
            "resource_ids": context_resources,
        },
        "NEEDS_VISUAL": {
            "count": len(visual_rows),
            "ids": [row["stable_id"] for row in visual_rows],
        },
        "OVERFLOW_ESTIMATE": {
            "count": len(risk_rows),
            "basis": "Conservative label proxy over 96 px on one line; a triage flag only, because consumer rectangles vary.",
            "items": [
                {"id": row["stable_id"], "label": row["integrated_label"], "proxy_px": row["width_proxy_max_line_px"]}
                for row in risk_rows
            ],
        },
        "TECHNICAL_DATA": {
            "resource_count": sum(row["kind"] in {"RAW", "CREDIT_STREAM"} for row in resources),
            "resource_ids": [row["id"] for row in resources if row["kind"] in {"RAW", "CREDIT_STREAM"}],
            "classified_residual_ids": [row["id"] for row in residues if row not in unresolved_residues],
        },
        "UNRESOLVED": {
            "cases": [
                "CORPUS-1436-ROW-INDEX",
                "BANK66-595-KEY-SUBSET",
                "CP932-15939",
                "CP932-15968",
                "READING-高津 利恵",
                "READING-深尾 伸也",
                "READING-橋本 信之",
            ]
        },
    }
    write_json("QA_QUEUES.json", qa_queues)

    # Exactly sixty manual triage entries: all seven critical cases, eighteen
    # context owners, twenty consumer-edge gaps stratified by kind, and fifteen
    # highest width-risk/long-label resources.
    review = []
    for case, decision in [
        ("CORPUS-1436-ROW-INDEX", "NOT_VALIDATED_NO_RESOURCE_LEVEL_INDEX"),
        ("BANK66-595-KEY-SUBSET", "NOT_VALIDATED_NO_KEY_LEVEL_OVERLAP"),
        ("CP932-15939", "NOT_VALIDATED_TECHNICAL"),
        ("CP932-15968", "NOT_VALIDATED_TECHNICAL"),
        ("READING-高津 利恵", "READING_UNVERIFIED"),
        ("READING-深尾 伸也", "READING_UNVERIFIED"),
        ("READING-橋本 信之", "READING_UNVERIFIED"),
    ]:
        review.append({"case": case, "stratum": "CRITICAL", "decision": decision, "next": "External row index, consumer evidence, or primary identity source required."})
    for row in sorted(context_owners, key=lambda item: item["id"])[:18]:
        review.append({"case": row["id"], "stratum": "CONTEXT_OWNER", "decision": "NEEDS_CONTEXT", "next": row["reason"]})
    by_kind: dict[str, list[dict]] = defaultdict(list)
    for resource in no_i03:
        by_kind[resource["kind"]].append(resource)
    for kind, take in [("LZ", 8), ("RAW", 6), ("CREDIT_STREAM", 6)]:
        for resource in sorted(by_kind[kind], key=lambda item: item["id"])[:take]:
            review.append({"case": resource["id"], "stratum": f"NO_I03_{kind}", "decision": "NEEDS_CONSUMER_EDGE", "next": "Trace owner/consumer; absence from I03 does not prove orphan or unused."})
    already = {row["case"] for row in review}
    long_rows = sorted(matrix, key=lambda row: (-row["width_proxy_max_line_px"], row["stable_id"]))
    for row in long_rows:
        if row["stable_id"] in already:
            continue
        review.append({"case": row["stable_id"], "stratum": "WIDTH_VISUAL", "decision": "NEEDS_VISUAL", "next": f"Validate real consumer rectangle; proxy={row['width_proxy_max_line_px']} px."})
        if len(review) == 60:
            break
    assert len(review) == 60
    with (OUT / "MANUAL_REVIEW_60.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["case", "stratum", "decision", "next"])
        writer.writeheader()
        writer.writerows(review)

    with historical_ledger.open(encoding="utf-8", newline="") as handle:
        ledger = list(csv.DictReader(handle))
    main_row = next(row for row in ledger if row["id"] == "P5-001")
    bank66_row = next(row for row in ledger if row["id"] == "P5-002")
    corpus_result = {
        "gate": "CORPUS-1436",
        "result": "NOT_VALIDATED",
        "historical_main_total": int(main_row["defined_total"]),
        "historical_bank66_total": int(bank66_row["defined_total"]),
        "aggregate_subset_claim_preserved": True,
        "resource_level_1436_rows_recovered": 0,
        "bank66_key_level_overlap_rows_proven": 0,
        "prohibition_applied": "No synthetic HIST-0001..HIST-1436 rows were generated because they would lack real addresses, pointers, source text and consumer identity.",
        "real_inventory_delivered": {
            "resources": len(resources),
            "used_by_i03": len(resources) - len(no_i03),
            "without_i03_edge": len(no_i03),
            "uses": len(uses),
            "pointer_checks": len(pointer_checks),
        },
        "evidence_needed_to_pass": [
            "The v0.25 editable row-level index, or an equivalent dump with stable key and physical owner per row.",
            "A 595-key Bank66 list cross-referenced against those same 1,436 keys.",
            "Original and integrated text fields or a reproducible decoder for each row.",
        ],
    }
    write_json("CORPUS_1436_RECONCILIATION.json", corpus_result)

    text_audits = {}
    for bank in ("66", "7A", "7C"):
        payload = read_json(ROOT / f"TEXT_AUDIT_BANK{bank}.json")
        text_audits[bank] = {
            "summary": payload["summary"],
            "unchanged_from_jp": sum(row.get("unchanged_from_original") is True for row in payload["candidates"]),
            "changed_vs_jp": sum(row.get("unchanged_from_original") is False for row in payload["candidates"]),
            "interpretation": "Heuristic CP932 hits are triage only; custom font/graphics bytes cause false positives and cannot grant linguistic PASS.",
        }
    write_json("TEXT_AUDIT_INTERPRETATION.json", text_audits)

    gate_results = {
        "iteration": "PW2",
        "status": "COMPLETED",
        "consumed": "2/5",
        "rom_changed": False,
        "rom_sha256": rom_sha,
        "gates": [
            {"gate": "S457_IDENTITY", "result": "PASS"},
            {"gate": "RESOURCE_MATRIX_1766", "result": "PASS_STATIC"},
            {"gate": "POINTER_AUDIT", "result": "PASS_STATIC_SCOPED"},
            {"gate": "RESIDUAL_47", "result": "45_CLASSIFIED_2_NOT_VALIDATED"},
            {"gate": "CORPUS-1436", "result": "NOT_VALIDATED"},
            {"gate": "BANK66-595", "result": "NOT_VALIDATED_KEY_LEVEL"},
            {"gate": "GLOBAL_VISUAL_QA", "result": "NOT_VALIDATED"},
        ],
        "manual_review_rows": len(review),
        "next_iteration": "PW3",
        "high_score": "DEFERRED_OUT_OF_SCOPE",
    }
    write_json("PW2_GATE_RESULTS.json", gate_results)

    summary = {
        "rom_sha256": rom_sha,
        "resources": len(resources),
        "hash_matches": len(resources),
        "uses": len(uses),
        "pointer_checks": len(pointer_checks),
        "context_uses": len(context_owners),
        "without_i03_edge": len(no_i03),
        "width_flags": len(risk_rows),
        "residuals_classified": len(residues) - len(unresolved_residues),
        "residuals_unresolved": len(unresolved_residues),
        "manual_review": len(review),
        "corpus_1436": "NOT_VALIDATED",
        "rom_changed": False,
    }
    write_json("PW2_SUMMARY.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
