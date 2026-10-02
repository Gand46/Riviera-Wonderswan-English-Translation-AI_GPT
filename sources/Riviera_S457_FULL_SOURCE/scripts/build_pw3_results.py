#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEL = ROOT / "deliverables"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(name: str, value: object) -> None:
    (DEL / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


routes = {
    "stage": "PW3",
    "budget": {
        "route_families_max": 3,
        "frames_per_route_max": 20000,
        "retries_per_route_max": 2,
        "new_selected_checkpoints_max": 12,
    },
    "route_1": {
        "purpose": "Arranque en frío y navegación hacia DATA:1",
        "attempts": [
            {"path": "evidence/route_01_cold_data1", "requested_frames": 2400, "result": "SRAM_LOAD_EXACT_TITLE_NAV_OPENED_EXTRA"},
            {"path": "evidence/route_01_retry_data1", "requested_frames": 3000, "result": "TITLE_NAV_OPENED_EXTRA"},
            {"path": "evidence/route_01_retry2_title_nav", "requested_frames": 960, "result": "ONE_FRAME_DOWN_STILL_ADVANCED_TWO_MENU_ROWS"},
        ],
        "sram_sha256_expected": "6c63b110e4b1c84dedc727f87971fa531bfd615307075e4c3e6891400774c1e0",
        "sram_loaded_byte_exact": True,
        "data1_ui_reacquired_in_pw3": False,
        "interpretation": "Input polling repeats the title direction within one emulated frame. This is an automation synchronization issue, not a ROM defect. PW3 therefore continues from the previously validated natural DATA:1 descendant checkpoint.",
    },
    "route_2": {
        "purpose": "Progresión natural desde Start 1-1 hasta el primer combate y su salida",
        "segments": [
            {"path": "evidence/route_02_area_progress", "requested_frames": 5200},
            {"path": "evidence/route_02_retry_finish_advance", "requested_frames": 14800},
        ],
        "requested_frames_total": 20000,
        "result": "PASS_NATURAL_FIRST_BATTLE_AND_VICTORY_POSTDIALOGUE",
        "cart_write_callbacks": 0,
        "rom_mutated": False,
    },
    "route_3": {
        "purpose": "Progresión natural posterior al primer combate hacia el siguiente encuentro",
        "attempts": [
            {"path": "evidence/route_03_sparse_progress", "requested_frames": 20000, "result": "SECOND_ENCOUNTER_ITEM_SELECT"},
            {"path": "evidence/route_03_retry_fast", "requested_frames": 20000, "result": "SECOND_BATTLE_IN_PROGRESS"},
        ],
        "furthest_natural_milestone": "Start 1-1, second encounter, battle in progress",
        "team_edit_seen": False,
        "rom_mutated": False,
    },
    "limits_respected": True,
}
write_json("ROUTE_EXECUTION_PW3.json", routes)

runtime = [
    {"id": "RT-01", "surface": "SRAM cold load", "access": "cold boot", "evidence": "route_01_cold_data1/cart_loaded.sav", "result": "PASS_BYTE_EXACT", "visual": "NOT_APPLICABLE", "note": "32 KiB SHA-256 matches the recovered native save."},
    {"id": "RT-02", "surface": "DATA:1 save screen", "access": "natural inherited checkpoint", "evidence": "captures/01_DATA1_save_screen.png", "result": "PASS_RUNTIME", "visual": "PASS_LEGIBLE", "note": "AREA 1-1 and saved slot are legible."},
    {"id": "RT-03", "surface": "Start menu", "access": "natural DATA:1 descendant", "evidence": "captures/02_start_menu.png", "result": "PASS_RUNTIME", "visual": "PASS_LEGIBLE", "note": "Memorial, Next Area and Save are stable."},
    {"id": "RT-04", "surface": "Map movement", "access": "natural", "evidence": "captures/03_map_movement.png", "result": "PASS_RUNTIME", "visual": "PASS_LEGIBLE", "note": "MOVE overlay and sprites remain stable."},
    {"id": "RT-05", "surface": "Dialogue", "access": "natural", "evidence": "captures/04_dialogue.png", "result": "PASS_RUNTIME", "visual": "PASS_LEGIBLE", "note": "Portrait, speaker name and text fit."},
    {"id": "RT-06", "surface": "Enemy tutorial", "access": "natural", "evidence": "captures/05_enemy_tutorial.png", "result": "PASS_RUNTIME", "visual": "PASS_LEGIBLE", "note": "Enemy overlay and tutorial dialogue are stable."},
    {"id": "RT-07", "surface": "Item Select / inventory", "access": "natural", "evidence": "captures/06_item_select.png", "result": "PASS_RUNTIME", "visual": "PASS_LEGIBLE", "note": "Lorelei and Einherjar fit the list."},
    {"id": "RT-08", "surface": "First battle HUD", "access": "natural", "evidence": "captures/07_first_battle.png", "result": "PASS_RUNTIME", "visual": "PASS_LEGIBLE", "note": "Action, target and item labels remain inside their regions."},
    {"id": "RT-09", "surface": "Victory", "access": "natural", "evidence": "captures/08_victory.png", "result": "PASS_RUNTIME", "visual": "PASS_LEGIBLE", "note": "Triumph transition completes normally."},
    {"id": "RT-10", "surface": "Post-battle dialogue", "access": "natural", "evidence": "captures/09_postbattle_dialogue.png", "result": "PASS_RUNTIME", "visual": "PASS_LEGIBLE", "note": "Dialogue advances with sparse synchronized input."},
    {"id": "RT-11", "surface": "Quest interface", "access": "natural", "evidence": "captures/10_quest_ui.png", "result": "PASS_RUNTIME", "visual": "PASS_LEGIBLE", "note": "Pillar label and quest prompt are stable."},
    {"id": "RT-12", "surface": "NPC dialogue", "access": "natural", "evidence": "captures/11_hector_dialogue.png", "result": "PASS_RUNTIME", "visual": "PASS_LEGIBLE", "note": "Hector portrait/name/dialogue are readable."},
    {"id": "RT-13", "surface": "Second Item Select", "access": "natural", "evidence": "captures/12_second_item_select.png", "result": "PASS_RUNTIME", "visual": "PASS_LEGIBLE", "note": "Lorelei, Einherjar and Potion fit with counts."},
    {"id": "RT-14", "surface": "Second battle HUD", "access": "natural", "evidence": "captures/13_second_battle.png", "result": "PASS_RUNTIME", "visual": "PASS_LEGIBLE", "note": "Devastator remains inside the action box in this reached case."},
    {"id": "RT-15", "surface": "Team Edit", "access": "controlled native screen entry (inherited)", "evidence": "captures/14_team_edit_controlled_reference.png", "result": "PASS_CONTROLLED_REFERENCE", "visual": "PASS_LEGIBLE", "note": "Diagnostic reference only; does not grant natural I20 PASS."},
]
write_json("RUNTIME_MATRIX_PW3.json", runtime)
with (DEL / "RUNTIME_MATRIX_PW3.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(runtime[0]))
    w.writeheader()
    w.writerows(runtime)

states = []
for p in sorted((DEL / "savestates").glob("*.mss")):
    states.append({"file": p.name, "bytes": p.stat().st_size, "sha256": sha256(p)})
state_catalog = {
    "stage": "PW3",
    "selected_in_package": len(states),
    "new_selected": 4,
    "inherited_input_checkpoint_copied": 1,
    "prior_cumulative_selected": 49,
    "cumulative_selected_after_pw3": 53,
    "limit": 12,
    "items": states,
}
write_json("SAVESTATE_CATALOG_PW3.json", state_catalog)

verification = {
    "stage": "PW3",
    "clean_jp_sha256": "62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921",
    "s457_sha256": "80ff36655d83956d96b634adafc685fa4379da326c3d45099dedcb73ef72a951",
    "rebuilt_s457_sha256": sha256(ROOT / "verification/Riviera_S457_rebuilt.wsc"),
    "bps_applied_s457_sha256": sha256(ROOT / "verification/Riviera_S457_from_bps.wsc"),
    "cumulative_bps_sha256": "e4bda7c628316fb92978f33ffc136c7f480f2a885f0b606be46e09b7c2335cef",
    "source_rebuild_byte_exact": True,
    "bps_apply_byte_exact": True,
    "rom_modified_in_pw3": False,
    "checksum": "D44D",
}
write_json("BINARY_VERIFICATION_PW3.json", verification)

gates = {
    "stage": "PW3",
    "budget_consumed": "3/5",
    "I20_NATURAL_TEAM": {
        "result": "NOT_VALIDATED",
        "reason": "Natural progression reached the second battle of Start 1-1 but Team Edit did not appear within three bounded routes.",
        "controlled_reference": "PASS_LEGIBLE_NOT_NATURAL",
    },
    "I11_I18_GLOBAL_QA": {
        "result": "PARTIAL_RUNTIME_PASS",
        "reachable_surfaces": "PASS_13_NATURAL_SURFACES_LEGIBLE",
        "global_visual_approved": False,
        "reason": "Representative reachable surfaces pass; the 1,766-resource visual universe was not naturally executed.",
    },
    "I22_LATE_SCENES": {
        "result": "DEFERRED",
        "furthest_milestone": "Start 1-1 second battle",
        "within_two_reproducible_milestones": False,
    },
    "PW5_activation": False,
    "HIGH_SCORE": "DEFERRED_UNCHANGED",
    "defects_demonstrated": 0,
    "rom_changes": 0,
    "next_stage": "PW4",
}
write_json("PW3_GATE_RESULTS.json", gates)

summary = {
    "stage": "PW3",
    "status": "COMPLETED",
    "budget_consumed": "3/5",
    "natural_surfaces_legible": 13,
    "selected_savestates_in_package": 5,
    "new_selected_savestates": 4,
    "farthest_natural_milestone": "Start 1-1 second battle in progress",
    "I20": "NOT_VALIDATED",
    "global_visual_qa": "PARTIAL_RUNTIME_PASS",
    "PW5_activated": False,
    "rom_changed": False,
    "next_stage": "PW4",
}
write_json("PW3_SUMMARY.json", summary)

report = """# Riviera Work Pt1.5 — PW3 Rutas naturales cortas y QA visual dirigida

**Fecha:** 2026-09-25  
**Estado:** `PW3 COMPLETADA` — presupuesto consumido `3/5`  
**ROM modificada:** no  
**Siguiente etapa:** `PW4 — Consolidación y dictamen de alcance Work`

## Resultado ejecutivo

PW3 agotó las tres rutas acotadas y sus reintentos útiles. La progresión natural reproducible avanzó desde el checkpoint descendiente de `DATA:1` hasta el segundo combate de `Start 1-1`. Se validaron en ejecución y por lectura directa las superficies alcanzables de guardado, Start, mapa, diálogos, tutorial, selección de objetos, combate, victoria, Quest y diálogo de NPC.

No apareció Team Edit por progresión ordinaria. La captura controlada heredada sigue siendo legible, pero no concede el cierre natural: `I20-NATURAL-TEAM = NOT_VALIDATED`. El hito alcanzado no deja I22 a dos hitos reproducibles, por lo que PW5 no se activa.

No se demostró ningún defecto nuevo de traducción o renderizado. S457 permanece byte idéntica y se conserva el mismo BPS acumulativo.

## Presupuesto ejecutado

| Ruta | Resultado | Presupuesto |
| --- | --- | --- |
| 1 · arranque en frío | La SRAM de 32 KiB cargó byte a byte; la automatización del menú saltó dos filas y abrió Extra Contents. Se clasifica como sincronización de entrada, no defecto de ROM. | 3 intentos acotados; sin exceder 20.000 cuadros por intento |
| 2 · DATA:1/Start 1-1 | Start → mapa → diálogo → tutorial → Item Select → primer combate → victoria → diálogo posterior. | 5.200 + 14.800 = 20.000 cuadros |
| 3 · continuación natural | Quest, Hector, segundo Item Select y segundo combate. | 20.000 cuadros; un reintento de 20.000 |

Se seleccionaron cuatro estados nuevos y se copió el checkpoint de entrada heredado: cinco estados en el paquete, 53 seleccionados acumulativos. El límite era 12 nuevos.

## QA runtime

La matriz `RUNTIME_MATRIX_PW3.csv/json` registra 13 superficies naturales legibles y una referencia controlada de Team Edit. La aprobación es representativa y alcanzable, no global: la matriz PW2 de 1.766 recursos no se convierte artificialmente en 1.766 PASS visuales.

Las cadenas visibles `Lorelei`, `Einherjar`, `Potion` y `Devastator` caben en los cuadros alcanzados. Los diálogos, nombres de hablante, indicadores y transiciones antes/después permanecen estables. No hubo escrituras de ROM; las rutas naturales registraron cero callbacks de escritura a SRAM durante los tramos observados.

## Puertas

| Puerta | Resultado PW3 | Motivo |
| --- | --- | --- |
| I20-NATURAL-TEAM | `NOT_VALIDATED` | Team Edit no apareció antes del segundo combate de 1-1. |
| I11-I18-GLOBAL-QA | `PARTIAL_RUNTIME_PASS` | 13 superficies naturales alcanzables pasan; no hay cobertura visual total. |
| I22-LATE-SCENES | `DEFERRED` | Sin checkpoint tardío auténtico ni proximidad a dos hitos. |
| HIGH-SCORE | `DEFERRED_UNCHANGED` | Fuera del presupuesto por decisión previa. |

## Verificación binaria

- ROM japonesa limpia: `62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921`.
- S457, reconstrucción por fuentes y aplicación BPS: `80ff36655d83956d96b634adafc685fa4379da326c3d45099dedcb73ef72a951`.
- BPS acumulativo: `e4bda7c628316fb92978f33ffc136c7f480f2a885f0b606be46e09b7c2335cef`.
- Checksum WonderSwan: `0xD44D`.

## Decisión

PW3 se cierra sin parche nuevo. PW4 debe consolidar la cadena reproducible, repetir BPS/Save/Continue/cold boot en el alcance ya demostrado y emitir el dictamen ordinario con cada puerta en `PASS`, `NOT_VALIDATED` o `DEFERRED`. PW5 permanece desactivada.
"""
(DEL / "Riviera_PW3_Rutas_Naturales_y_QA_Visual.md").write_text(report, encoding="utf-8")

print("PW3_RESULTS_BUILT")
