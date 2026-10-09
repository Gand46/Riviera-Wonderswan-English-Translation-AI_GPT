#!/usr/bin/env python3
"""S462/RC6: restore the pre-S460 compact ranges while retaining S460's tail."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


BASE_SHA = "2eaeb2c90ca2ef62d858a887fa1ee2091d680b17366bf5dd07d642d0fc8171bf"
PATCH_ROM = 0x75EAF1
RC5_PREIMAGE = bytes.fromhex("eb0081ff22ed7299ebe1")
# cmp di,ED22; jae compact (EADC); otherwise resume the former range table
# at EAC4.  The final FF bytes restore the unused padding.
RC6_POSTIMAGE = bytes.fromhex("81ff22ed73e5ebcbffff")
LOST_RANGES = ((0x7CB227, 0x7CB529), (0x7CDBE1, 0x7CDC00))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_stream(rom: bytes, start: int, limit: int) -> bytes:
    pos = start
    while pos < limit:
        value = rom[pos]
        pos += 2 if value == 0xFE or 0xA2 <= value <= 0xA8 else 1
        if value == 0xFF:
            return rom[start:pos]
    raise AssertionError(f"unterminated stream at {start:#x}")


def affected_streams(rom: bytes) -> list[dict[str, object]]:
    rows = []
    for start, end in LOST_RANGES:
        cursor = start
        while cursor < end:
            if rom[cursor] == 0xFF:
                cursor += 1
                continue
            raw = read_stream(rom, cursor, end)
            rows.append({"rom_start": hex(cursor), "bytes": len(raw), "sha256": sha(raw)})
            cursor += len(raw)
    assert len(rows) == 22
    return rows


def build(base: bytes) -> tuple[bytes, dict[str, object]]:
    assert len(base) == 0x800000 and sha(base) == BASE_SHA, "RC5 identity mismatch"
    assert int.from_bytes(base[-2:], "little") == sum(base[:-2]) & 0xFFFF
    assert base[PATCH_ROM:PATCH_ROM + len(RC5_PREIMAGE)] == RC5_PREIMAGE
    before_streams = affected_streams(base)

    out = bytearray(base)
    out[PATCH_ROM:PATCH_ROM + len(RC6_POSTIMAGE)] = RC6_POSTIMAGE
    out[-2:] = (sum(out[:-2]) & 0xFFFF).to_bytes(2, "little")

    allowed = set(range(PATCH_ROM, PATCH_ROM + len(RC6_POSTIMAGE))) | {len(out) - 2, len(out) - 1}
    diff = {i for i, (old, new) in enumerate(zip(base, out)) if old != new}
    assert diff and not diff - allowed, sorted(diff - allowed)[:10]
    assert affected_streams(out) == before_streams, "text data changed"
    report = {
        "stage": "S462",
        "version": "v0.115 RC6",
        "base_sha256": BASE_SHA,
        "rom_sha256": sha(out),
        "rom_size": len(out),
        "checksum": f"{int.from_bytes(out[-2:], 'little'):04X}",
        "patch_rom": hex(PATCH_ROM),
        "preimage_hex": RC5_PREIMAGE.hex(),
        "postimage_hex": RC6_POSTIMAGE.hex(),
        "changed_bytes": len(diff),
        "changed_offsets": [hex(i) for i in sorted(diff)],
        "unexpected_changed_bytes": 0,
        "affected_stream_count": len(before_streams),
        "affected_streams_byte_identical": True,
        "lost_ranges_restored": [[hex(a), hex(b)] for a, b in LOST_RANGES],
        "new_s460_tail_preserved": ["0x7CED22", "0x7D0000"],
        "final_approved": False,
    }
    return bytes(out), report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rc5")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    output, report = build(Path(args.rc5).read_bytes())
    destination = Path(args.out)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(output)
    destination.with_suffix(".build.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
