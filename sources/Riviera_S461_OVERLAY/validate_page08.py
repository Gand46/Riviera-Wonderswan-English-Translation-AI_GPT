#!/usr/bin/env python3
"""Validate the single credit page changed by S461.

The recognizer searches all native A-Z/a-z glyph combinations and permitted
inter-glyph gaps.  It does not receive the intended name as an input.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path

from PIL import Image


RC4_SHA = "931e5cfec6e60fe3ad2b48b192b38bfd071d1a3b2453ddac3e1c271fb8da3c7d"
RC5_SHA = "2eaeb2c90ca2ef62d858a887fa1ee2091d680b17366bf5dd07d642d0fc8171bf"
BLOCK_START = 0x7FEDE0
BLOCK_END = 0x7FF4EA
FONT_START = 0x5534BC
FONT_END = FONT_START + 52 * 50
SURFACE = 0x59E0
ROW_Y = 36
ROW_HEIGHT = 10


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def page_address(x: int, y: int) -> int:
    return SURFACE + (y // 8 * 12 + x // 8) * 32 + y % 8 * 4 + x % 8 // 2


def page_pixel(ram: bytes, x: int, y: int) -> bool:
    value = ram[page_address(x, y)]
    return ((value >> (4 if x % 2 == 0 else 0)) & 0x0F) != 0


def glyph(rom: bytes, character: str):
    index = ord(character) - 65 if character.isupper() else ord(character) - 97 + 26
    address = FONT_START + index * 50
    raw = rom[address:address + 50]
    pixels = [
        [
            ((raw[(y * 10 + x) // 2] >> (4 if x % 2 == 0 else 0)) & 0x0F) == 6
            for x in range(10)
        ]
        for y in range(10)
    ]
    occupied = [x for row in pixels for x, value in enumerate(row) if value]
    return tuple(tuple(row[min(occupied):max(occupied) + 1]) for row in pixels)


def recognize(rom: bytes, ram: bytes):
    templates = {character: glyph(rom, character) for character in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"}
    columns = [x for x in range(96) if any(page_pixel(ram, x, ROW_Y + y) for y in range(ROW_HEIGHT))]
    assert columns
    start = min(columns)
    end = max(columns) + 1

    def matches(x, template):
        width = len(template[0])
        return x + width <= 96 and all(
            page_pixel(ram, x + x_offset, ROW_Y + y) == template[y][x_offset]
            for y in range(10)
            for x_offset in range(width)
        )

    def blank(first, exclusive_end):
        return all(
            not page_pixel(ram, x, ROW_Y + y)
            for x in range(first, exclusive_end)
            for y in range(10)
        )

    @lru_cache(None)
    def visit(x):
        candidates = []
        for character, template in templates.items():
            width = len(template[0])
            if not matches(x, template):
                continue
            next_x = x + width
            if next_x == end:
                candidates.append(character)
            for gap, separator in ((1, ""), (4, " ")):
                if next_x + gap <= end and blank(next_x, next_x + gap):
                    candidates.extend(character + separator + tail for tail in visit(next_x + gap))
        return tuple(candidates)

    return list(visit(start)), start, end


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rc4")
    parser.add_argument("rc5")
    parser.add_argument("rc4_page_bin")
    parser.add_argument("rc5_page_bin")
    parser.add_argument("rc5_hook_guard")
    parser.add_argument("rc5_zoom_png")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    rc4 = Path(args.rc4).read_bytes()
    rc5 = Path(args.rc5).read_bytes()
    old_page = Path(args.rc4_page_bin).read_bytes()
    new_page = Path(args.rc5_page_bin).read_bytes()
    guard = json.loads(Path(args.rc5_hook_guard).read_text())
    zoom = Image.open(args.rc5_zoom_png)

    assert sha(rc4) == RC4_SHA and sha(rc5) == RC5_SHA
    assert len(rc4) == len(rc5) == 0x800000
    assert int.from_bytes(rc5[-2:], "little") == sum(rc5[:-2]) & 0xFFFF
    assert rc4[FONT_START:FONT_END] == rc5[FONT_START:FONT_END]

    rom_diff = {index for index, (before, after) in enumerate(zip(rc4, rc5)) if before != after}
    rom_allowed = set(range(BLOCK_START, BLOCK_END)) | {0x7FFFFE, 0x7FFFFF}
    assert rom_diff and not rom_diff - rom_allowed

    page_diff = {index for index, (before, after) in enumerate(zip(old_page, new_page)) if before != after}
    row_allowed = {
        page_address(x, y)
        for y in range(ROW_Y, ROW_Y + ROW_HEIGHT)
        for x in range(96)
    }
    assert page_diff and not page_diff - row_allowed
    assert guard["register_errors"] == guard["unexpected_writes"] == 0

    candidates, start, end = recognize(rc5, new_page)
    assert candidates == ["Shinya Fukao"]
    assert zoom.size == (384, 576)
    left_margin = start
    right_margin = 96 - end
    assert left_margin == right_margin == 14

    report = {
        "stage": "S461",
        "gate": "RC5-CREDITS-PAGE-08",
        "result": "PASS",
        "access_method": "WRAM_POKE_NATIVE_ROM_ROUTINES",
        "natural_progression": False,
        "page": 8,
        "role": "Tuning",
        "rc4_rom_sha256": RC4_SHA,
        "rc5_rom_sha256": RC5_SHA,
        "rc4_page_sha256": sha(old_page),
        "rc5_page_sha256": sha(new_page),
        "page_bytes": len(new_page),
        "page_changed_bytes": len(page_diff),
        "page_diff_scope": {
            "result": "PASS",
            "row_y": ROW_Y,
            "row_height": ROW_HEIGHT,
            "outside_expected_row": len(page_diff - row_allowed),
        },
        "renderer_guard": {
            "result": "PASS",
            "register_errors": guard["register_errors"],
            "unexpected_writes": guard["unexpected_writes"],
            "pixel_write_events": guard["pixel_write_events"],
        },
        "native_font": {
            "result": "PASS",
            "sha256": sha(rc5[FONT_START:FONT_END]),
            "changed": False,
        },
        "independent_context_free_recognition": {
            "result": "PASS",
            "method": "EXACT_NATIVE_GLYPH_DYNAMIC_PROGRAMMING",
            "alphabet": "A-Z,a-z",
            "candidate_count": len(candidates),
            "candidates": candidates,
        },
        "layout": {
            "result": "PASS",
            "ink_bounds_x": [start, end],
            "left_margin": left_margin,
            "right_margin": right_margin,
            "row_pitch": 10,
            "overlap": False,
            "clipping": False,
        },
        "representative_scale": {
            "result": "PASS",
            "scale": "4x nearest-neighbor",
            "dimensions": list(zoom.size),
            "artifact": "credits_replay/page_08/runtime/zoom.png",
        },
        "rom_diff": {
            "result": "PASS",
            "changed_bytes": len(rom_diff),
            "unexpected_changed_bytes": len(rom_diff - rom_allowed),
            "allowed_compressed_block": [hex(BLOCK_START), hex(BLOCK_END)],
            "checksum_range": ["0x7ffffe", "0x800000"],
        },
        "regression": {
            "result": "PASS",
            "renderer_changed": False,
            "font_changed": False,
            "hooks_changed": False,
            "animation_tables_changed": False,
            "other_credit_pages_changed_by_rom_diff_domain": False,
        },
    }
    destination = Path(args.out)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
