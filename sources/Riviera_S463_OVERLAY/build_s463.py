#!/usr/bin/env python3
"""S463: one verified credit name, within the existing page-09 allocation.

Native glyphs and packed2/RLE codec follow S461. A shortest-stream encoder
uses the same existing decoder grammar; no decoder or font bytes change.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

BASE_SHA = 'b8aa59568a860c229751f504e2b5e9cd81d21909507e9f685c6f3797f18c1204'
SOURCE = 0x7FF4EA
CAPACITY = 1223
OLD_PACKED_SHA = 'e082fe4259bd0e87c1f6d89d12727399f7ce4e26744556e22ea407b06684fa4e'
OLD_RAW_SHA = 'a433dcc69f4495bed9ec45764be73b6dd66c200e7cacd075cb7f91b3163da948'
FONT = 0x5534BC
LINES = ['Makoto Shibasaki', 'Satoshi Oshita', 'Takashi Shoji',
         'Nobuyuki', 'Hashimoto', 'Takuji Nakamura', 'Masashi Umeda',
         'Toshimitsu Sakairi']
OWNERS = [0, 1, 2, 3, 3, 4, 5, 6]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def decode(data):
    raw = bytearray()
    i = 0
    while i < len(data) and data[i]:
        count = data[i]
        i += 1
        if count & 128:
            raw.extend(b'\0' * (count & 127))
        else:
            assert i + count <= len(data)
            raw.extend(data[i:i+count])
            i += count
    assert i < len(data) and data[i] == 0
    return bytes(raw), i + 1

def unpack2(raw):
    pal = [0, 2, 6, 0]
    return bytes(pal[(v >> j) & 3] | pal[(v >> (j+2)) & 3] << 4
                 for v in raw for j in (0, 4))

def pack2(raw):
    pal = {0: 0, 2: 1, 6: 2}
    return bytes(pal[raw[i] & 15] | pal[raw[i] >> 4] << 2
                 | pal[raw[i+1] & 15] << 4 | pal[raw[i+1] >> 4] << 6
                 for i in range(0, len(raw), 2))

def encode_shortest(raw):
    """Exact minimum length for literals(1..127), zero runs(1..127), end(0)."""
    n = len(raw)
    costs = [n*2+1] * (n+1)
    choices = [None] * n
    costs[n] = 1
    for i in range(n-1, -1, -1):
        for k in range(1, min(127, n-i)+1):
            candidate = 1+k+costs[i+k]
            if candidate < costs[i]:
                costs[i], choices[i] = candidate, (k, False)
        for k in range(1, min(127, n-i)+1):
            if raw[i+k-1]:
                break
            candidate = 1+costs[i+k]
            if candidate < costs[i]:
                costs[i], choices[i] = candidate, (k, True)
    output = bytearray()
    i = 0
    while i < n:
        count, zero = choices[i]
        output.append(count | (128 if zero else 0))
        if not zero:
            output.extend(raw[i:i+count])
        i += count
    output.append(0)
    assert len(output) == costs[0] and decode(output)[0] == raw
    return bytes(output)

def pixel_address(x, y):
    return (y//8*12+x//8)*32+y%8*4+x%8//2

def native_glyph(rom, c):
    assert c.isascii() and c.isalpha()
    index = ord(c)-65 if c.isupper() else ord(c)-97+26
    address = FONT+index*50
    data = rom[address:address+50]
    grid = [[((data[(y*10+x)//2] >> (4 if x%2 == 0 else 0)) & 15) == 6
             for x in range(10)] for y in range(10)]
    columns = [x for row in grid for x, value in enumerate(row) if value]
    glyph = [row[min(columns):max(columns)+1] for row in grid]
    return glyph, {'character': c, 'address': hex(address), 'sha256': sha(data),
                   'width': len(glyph[0]), 'height': 10}

def render(rom):
    raw = bytearray(96*48)
    glyphs = {c: native_glyph(rom, c) for c in set(''.join(LINES)) if c != ' '}
    metrics = []
    for row, line in enumerate(LINES):
        width = sum(3 if c == ' ' else len(glyphs[c][0][0])+1 for c in line)-1
        assert width <= 94
        x = (96-width)//2
        y = 6+row*10
        assert y+10 <= 96
        metrics.append({'text': line, 'x': x, 'y': y, 'width': width,
                        'height': 10, 'line_owner': OWNERS[row], 'gap': 1})
        for c in line:
            if c == ' ':
                x += 3
                continue
            pixels, _ = glyphs[c]
            for yy, values in enumerate(pixels):
                for xx, value in enumerate(values):
                    if value:
                        raw[pixel_address(x+xx, y+yy)] |= 6 << (4 if (x+xx)%2 == 0 else 0)
            x += len(pixels[0])+1
    return bytes(raw), metrics, [glyphs[c][1] for c in sorted(glyphs)]

def build(base):
    assert len(base) == 0x800000 and sha(base) == BASE_SHA, 'RC6 identity mismatch'
    assert int.from_bytes(base[-2:], 'little') == sum(base[:-2]) & 65535
    old = base[SOURCE:SOURCE+CAPACITY]
    assert sha(old) == OLD_PACKED_SHA
    decoded, consumed = decode(old)
    assert consumed == CAPACITY and sha(unpack2(decoded)) == OLD_RAW_SHA
    raw, metrics, glyphs = render(base)
    packed = encode_shortest(pack2(raw))
    assert len(packed) <= CAPACITY and unpack2(decode(packed)[0]) == raw
    output = bytearray(base)
    output[SOURCE:SOURCE+CAPACITY] = packed + b'\xff'*(CAPACITY-len(packed))
    output[-2:] = (sum(output[:-2]) & 65535).to_bytes(2, 'little')
    changed = [i for i, (a,b) in enumerate(zip(base, output)) if a != b]
    unexpected = [i for i in changed if not (SOURCE <= i < SOURCE+CAPACITY or i >= len(base)-2)]
    assert not unexpected
    assert output[FONT:FONT+52*50] == base[FONT:FONT+52*50]
    report = {'stage': 'S463', 'version': 'v0.116 RC7', 'base_sha256': BASE_SHA,
              'rom_sha256': sha(output), 'rom_size': len(output),
              'checksum': f'{int.from_bytes(output[-2:], "little"):04X}',
              'changed_bytes': len(changed), 'unexpected_changed_offsets': len(unexpected),
              'allowed_ranges': [[hex(SOURCE), hex(SOURCE+CAPACITY)], ['0x7ffffe','0x800000']],
              'credit': {'page': 9, 'block': 'CREDIT-7A3D29', 'original': '橋本信之',
                         'reading': 'Nobuyuki Hashimoto', 'destination_wram': '0x5b60',
                         'old_compressed_length': CAPACITY, 'new_compressed_length': len(packed),
                         'old_compressed_sha256': OLD_PACKED_SHA, 'new_compressed_sha256': sha(packed),
                         'old_raw_sha256': OLD_RAW_SHA, 'new_raw_sha256': sha(raw),
                         'height': 96, 'line_pitch': 10, 'metrics': metrics, 'glyphs': glyphs},
              'font_changed': False, 'decoder_changed': False, 'hooks_changed': False,
              'animation_tables_changed': False, 'page_duration_changed': False,
              'other_credit_pages_changed': False, 'gameplay_code_changed': False,
              'remaining_name': '高津利恵', 'final_approved': False}
    return bytes(output), report

def main():
    p = argparse.ArgumentParser()
    p.add_argument('rc6')
    p.add_argument('--out', required=True)
    args = p.parse_args()
    output, report = build(Path(args.rc6).read_bytes())
    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(output)
    dest.with_suffix('.build.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'credit'}, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
