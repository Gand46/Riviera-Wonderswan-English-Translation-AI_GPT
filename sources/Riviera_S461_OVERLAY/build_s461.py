#!/usr/bin/env python3
"""Build S461 RC5: replace one verified Japanese credit with its Latin reading.

Only the compiled page-08 credit graphic is rebuilt.  The native ROM font,
credit renderer, hooks, animation tables, and every other credit page remain
byte-identical to RC4.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


BASE_SHA = "931e5cfec6e60fe3ad2b48b192b38bfd071d1a3b2453ddac3e1c271fb8da3c7d"
BLOCK_ID = "CREDIT-7A3C8D"
BLOCK_SOURCE = 0x7FEDE0
BLOCK_DESTINATION = 0x59E0
BLOCK_HEIGHT = 128
OLD_COMPRESSED_LENGTH = 1802
OLD_COMPRESSED_SHA = "bf49c532eca027d0c6396a5fe4cbe5b13513da52f80828e4d07ac4b31f223047"
OLD_RAW_SHA = "1a580dc716f3ddd24959ff67b9fca8082130029d551f25a086450e0895dc4f4d"
ROW_Y = 36
ROW_HEIGHT = 10
ROM_FONT_START = 0x5534BC
ROM_FONT_LENGTH = 52 * 50
READING = "Shinya Fukao"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unrle(data: bytes) -> bytes:
    out = bytearray()
    i = 0
    while data[i]:
        count = data[i]
        i += 1
        if count & 0x80:
            out += b"\0" * (count & 0x7F)
        else:
            out += data[i:i + count]
            i += count
    assert i == len(data) - 1
    return bytes(out)


def rle(raw: bytes) -> bytes:
    out = bytearray()
    i = 0
    while i < len(raw):
        zero = raw[i] == 0
        j = i + 1
        while j < len(raw) and j - i < 127 and (raw[j] == 0) == zero:
            j += 1
        out.append((0x80 if zero else 0) + (j - i))
        if not zero:
            out += raw[i:j]
        i = j
    return bytes(out) + b"\0"


def unpack2(raw: bytes) -> bytes:
    palette = [0, 2, 6, 0]
    return bytes(
        palette[(value >> shift) & 3] | palette[(value >> (shift + 2)) & 3] << 4
        for value in raw
        for shift in (0, 4)
    )


def pack2(raw: bytes) -> bytes:
    palette = {0: 0, 2: 1, 6: 2}
    assert len(raw) % 2 == 0
    return bytes(
        palette[raw[i] & 0x0F]
        | palette[raw[i] >> 4] << 2
        | palette[raw[i + 1] & 0x0F] << 4
        | palette[raw[i + 1] >> 4] << 6
        for i in range(0, len(raw), 2)
    )


def pixel_address(x: int, y: int) -> int:
    return (y // 8 * 12 + x // 8) * 32 + y % 8 * 4 + x % 8 // 2


def set_pixel(raw: bytearray, x: int, y: int, value: int) -> None:
    address = pixel_address(x, y)
    shift = 4 if x % 2 == 0 else 0
    raw[address] = (raw[address] & ~(0x0F << shift)) | (value << shift)


def native_glyph(rom: bytes, character: str):
    index = ord(character) - 65 if character.isupper() else ord(character) - 97 + 26
    address = ROM_FONT_START + index * 50
    glyph_raw = rom[address:address + 50]
    pixels = [
        [
            ((glyph_raw[(y * 10 + x) // 2] >> (4 if x % 2 == 0 else 0)) & 0x0F) == 6
            for x in range(10)
        ]
        for y in range(10)
    ]
    populated = [x for row in pixels for x, value in enumerate(row) if value]
    cropped = [row[min(populated):max(populated) + 1] for row in pixels]
    return cropped, {
        "character": character,
        "address": hex(address),
        "raw_sha256": sha(glyph_raw),
        "width": len(cropped[0]),
        "height": 10,
    }


def build(base: bytes):
    assert len(base) == 0x800000 and sha(base) == BASE_SHA, "RC4 identity mismatch"
    assert int.from_bytes(base[-2:], "little") == sum(base[:-2]) & 0xFFFF

    old_packed = base[BLOCK_SOURCE:BLOCK_SOURCE + OLD_COMPRESSED_LENGTH]
    assert sha(old_packed) == OLD_COMPRESSED_SHA
    raw = bytearray(unpack2(unrle(old_packed)))
    assert len(raw) == BLOCK_HEIGHT * 48 and sha(raw) == OLD_RAW_SHA

    for y in range(ROW_Y, ROW_Y + ROW_HEIGHT):
        for x in range(96):
            set_pixel(raw, x, y, 0)

    glyphs = {character: native_glyph(base, character) for character in set(READING) if character != " "}
    width = sum(3 if character == " " else len(glyphs[character][0][0]) + 1 for character in READING) - 1
    x = (96 - width) // 2
    start_x = x
    glyph_records = {}
    for character in READING:
        if character == " ":
            x += 3
            continue
        pixels, record = glyphs[character]
        glyph_records[character] = record
        for y_offset, row in enumerate(pixels):
            for x_offset, value in enumerate(row):
                if value:
                    set_pixel(raw, x + x_offset, ROW_Y + y_offset, 6)
        x += len(pixels[0]) + 1

    new_raw = bytes(raw)
    new_packed = rle(pack2(new_raw))
    assert len(new_packed) <= OLD_COMPRESSED_LENGTH
    assert unpack2(unrle(new_packed)) == new_raw

    out = bytearray(base)
    out[BLOCK_SOURCE:BLOCK_SOURCE + OLD_COMPRESSED_LENGTH] = (
        new_packed + b"\xFF" * (OLD_COMPRESSED_LENGTH - len(new_packed))
    )
    out[-2:] = (sum(out[:-2]) & 0xFFFF).to_bytes(2, "little")

    allowed = set(range(BLOCK_SOURCE, BLOCK_SOURCE + OLD_COMPRESSED_LENGTH)) | {len(out) - 2, len(out) - 1}
    changed = [index for index, (before, after) in enumerate(zip(base, out)) if before != after]
    assert changed and not set(changed) - allowed
    assert out[ROM_FONT_START:ROM_FONT_START + ROM_FONT_LENGTH] == base[ROM_FONT_START:ROM_FONT_START + ROM_FONT_LENGTH]

    report = {
        "stage": "S461",
        "version": "v0.114 RC5",
        "base_sha256": BASE_SHA,
        "rom_sha256": sha(out),
        "rom_size": len(out),
        "checksum": f"{int.from_bytes(out[-2:], 'little'):04X}",
        "changed_bytes": len(changed),
        "unexpected_changed_offsets": 0,
        "allowed_ranges": [
            {"start": hex(BLOCK_SOURCE), "exclusive_end": hex(BLOCK_SOURCE + OLD_COMPRESSED_LENGTH)},
            {"start": hex(len(out) - 2), "exclusive_end": hex(len(out))},
        ],
        "credit_change": {
            "page": 8,
            "role": "Tuning",
            "block_id": BLOCK_ID,
            "destination_wram": hex(BLOCK_DESTINATION),
            "original": "深尾伸也",
            "reading": READING,
            "row_y": ROW_Y,
            "row_height": ROW_HEIGHT,
            "width": width,
            "x": start_x,
            "old_raw_sha256": OLD_RAW_SHA,
            "new_raw_sha256": sha(new_raw),
            "old_compressed_length": OLD_COMPRESSED_LENGTH,
            "new_compressed_length": len(new_packed),
            "old_compressed_sha256": OLD_COMPRESSED_SHA,
            "new_compressed_sha256": sha(new_packed),
            "glyphs": [glyph_records[key] for key in sorted(glyph_records)],
        },
        "native_font_sha256": sha(base[ROM_FONT_START:ROM_FONT_START + ROM_FONT_LENGTH]),
        "native_font_changed": False,
        "credit_renderer_changed": False,
        "credit_hooks_changed": False,
        "animation_tables_changed": False,
        "other_credit_pages_changed": False,
        "final_approved": False,
    }
    return bytes(out), report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rc4")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    result, report = build(Path(args.rc4).read_bytes())
    destination = Path(args.out)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(result)
    destination.with_suffix(".build.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
