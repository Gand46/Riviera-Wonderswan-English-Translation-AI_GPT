#!/usr/bin/env python3
"""Build S460 RC4: translate every reachable post-final event dialogue branch."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


BASE_SHA = "c79079537ea5f66cf74f94d48afc3da14dd9db1f8458156d337f5e0107c111dd"
ALLOCATION_START = 0x7CED22
ALLOCATION_LIMIT = 0x7D0000
HOOK_GUARDS = {
    0x7521F2: bytes.fromhex("e972b39090"),
    0x75D567: bytes.fromhex(
        "e916158a720e81ff1ad4721081ffe5d87202eb0832ffff4420e9744c80fb8a74f3b701ff4420e9674c"
    ),
}
DISPATCH_EXTENSION_ROM = 0x75EAF1
DISPATCH_EXTENSION_OLD = bytes.fromhex("ebd1ffffffffffffffff")
# For ES=C000, preserve all former compact ranges and add the reserved free tail
# [ED22,10000). The free tail is dedicated to S460, so no upper CMP is needed.
DISPATCH_EXTENSION_NEW = bytes.fromhex("eb0081ff22ed7299ebe1")

# Pointer-field ROM offset -> original stream ROM offset.
OWNERS = {
    # Common reunion, Elendia messages, dinner and choice.
    0x793563:0x7C17DD, 0x793568:0x7C17E4, 0x79356D:0x7C17EA,
    0x793573:0x7C17F0, 0x793578:0x7C17F6, 0x79357F:0x7C17FC,
    0x793583:0x7C1801, 0x793595:0x7C1816, 0x7935A1:0x7C1825,
    0x7935B4:0x7C182B, 0x7935C7:0x7C183B, 0x7935D3:0x7C1855,
    0x7935D7:0x7C1873, 0x7935DB:0x7C1886, 0x7935DF:0x7C188E,
    0x7935E3:0x7C18A5, 0x7935E7:0x7C18C6, 0x793623:0x7C18DE,
    0x793639:0x7C1912, 0x79365A:0x7C1954, 0x79365E:0x7C196B,
    0x793681:0x7C197F, 0x793685:0x7C199D, 0x79369D:0x7C19B3,
    0x7936B3:0x7C19DE, 0x7936C9:0x7C1A1D, 0x7936E8:0x7C1A4F,
    0x793717:0x7C1A7D, 0x79371B:0x7C1A93, 0x793722:0x7C1AB8,
    0x793726:0x7C1AD6, 0x79372A:0x7C1AE7, 0x793742:0x7C1AFB,
    0x793758:0x7C1B34, 0x793779:0x7C1B79, 0x79377D:0x7C1B9C,
    0x793781:0x7C1BC1, 0x793785:0x7C1BDE, 0x79379E:0x7C1BEA,
    0x7937F6:0x7C1C29, 0x7937FF:0x7C1C3A, 0x793803:0x7C1C48,
    0x793807:0x7C1C63, 0x79380E:0x7C1C71, 0x793812:0x7C1C91,
    0x793816:0x7C1CB7, 0x79381A:0x7C1CE8, 0x79381E:0x7C1CF0,
    0x793822:0x7C1CFC, 0x793826:0x7C1D02, 0x79382D:0x7C1D0F,
    0x793834:0x7C1D49, 0x793838:0x7C1D69, 0x79383C:0x7C1D83,
    0x793840:0x7C1DA7, 0x793844:0x7C1DB9, 0x793848:0x7C1DC0,
    0x79384F:0x7C1DEA, 0x793853:0x7C1E37, 0x793857:0x7C1E3E,
    0x79385B:0x7C1E50, 0x79385F:0x7C1E71, 0x793863:0x7C1E78,
    0x793867:0x7C1EBA,
    # Lina.
    0x79394F:0x7C1EC7, 0x79395D:0x7C1EEC, 0x793966:0x7C1EF9,
    0x79398B:0x7C1F08, 0x7939A3:0x7C1F0E,
    # Fia.
    0x7939CC:0x7C1F20, 0x7939E2:0x7C1F42, 0x7939E7:0x7C1F4B,
    0x7939F0:0x7C1F77, 0x7939F4:0x7C1F7D, 0x7939FD:0x7C1F8E,
    0x793A04:0x7C1FB0, 0x793A08:0x7C1FC4, 0x793A0C:0x7C1FDA,
    # Cierra.
    0x793A3F:0x7C1FE4, 0x793A4D:0x7C2010, 0x793A5B:0x7C2022,
    0x793A60:0x7C202B, 0x793A64:0x7C204D, 0x793A6F:0x7C2054,
    0x793A73:0x7C205D, 0x793A89:0x7C2062, 0x793A90:0x7C207B,
    # Serene.
    0x793AB9:0x7C2095, 0x793AFB:0x7C20A3, 0x793B00:0x7C20AA,
    0x793B04:0x7C20BB, 0x793B0D:0x7C20C4, 0x793B11:0x7C20E6,
    0x793B15:0x7C210A, 0x793B1E:0x7C2123,
    # Neutral / Asgard.
    0x793B3F:0x7C212B, 0x793B50:0x7C214C, 0x793B54:0x7C2163,
    0x793B58:0x7C2181, 0x793B5C:0x7C218B, 0x793B60:0x7C21A6,
    0x793B64:0x7C21CD,
}

# Each inner tuple is one rendered page; each string is one rendered line.
TEXT = {
0x7C17DD:(("......?",),), 0x7C17E4:(("Fia!",),), 0x7C17EA:(("Lina!",),),
0x7C17F0:(("Serene!",),), 0x7C17F6:(("Cierra!",),), 0x7C17FC:(("Rose!",),),
0x7C1801:(("Everyone...","We made it!"),),
0x7C1816:(("...Huh?","I am alive..."),), 0x7C1825:(("Where are we?",),),
0x7C182B:(("It is Elendia!",),),
0x7C183B:(("We made it...","back alive."),),
0x7C1855:(("Thank goodness!",),),
0x7C1873:(("It was Ursula.","She saved us."),),
0x7C1886:(("You are right.",),), 0x7C188E:(("Riviera is","peaceful now!"),),
0x7C18A5:(("Yeah...",),("No more Seth...",),("No more","judgment."),("It is all over.",)),
0x7C18C6:(("Riviera is free","at last!"),),
0x7C18DE:(("Master Ein!","You are safe!"),("You are a true","hero.")),
0x7C1912:(("Elendia exists","because of you."),("Thank you, Ein,","from my heart.")),
0x7C1954:(("Our hero, Ein!",),), 0x7C196B:(("Umm... Thanks,","mister."),),
0x7C197F:(("Glad we have a","tomorrow."),),
0x7C199D:(("No more fear","of demons!"),),
0x7C19B3:(("The winds have","calmed..."),("We owe it all","to you, Ein.")),
0x7C19DE:(("It began when","we found you..."),("I am glad this","ended well!")),
0x7C1A1D:(("The sun is nice","and warm. Nya."),("Purr... I hope","this will last.")),
0x7C1A4F:(("Oh, Ein! ❤",),), 0x7C1A7D:(("You beat all","those demons..."),),
0x7C1A93:(("You are so","awesome!"),),
0x7C1AB8:(("You got so far","by luck..."),("But you are not","so bad.")),
0x7C1AD6:(("......!",),), 0x7C1AE7:(("Meute says","thank you, too."),),
0x7C1AFB:(("So, Elendia is","saved."),("I cheered from","the mine.")),
0x7C1B34:(("Knowledge turns","into treasure"),("through action.","Now tell me"),("what you saw.",)),
0x7C1B79:(("No more demons!","I can focus on"),("my experiments.",)),
0x7C1B9C:(("Now I can leave","for supplies ★"),),
0x7C1BC1:(("Bring me three","dried bats!"),),
0x7C1BDE:(("I should have","kept quiet..."),),
0x7C1BEA:(("Were my weapons","useful?"),("Need anything?","I will make it!")),
0x7C1C29:(("Welcome home,","Ein!"),), 0x7C1C3A:(("You are late!",),),
0x7C1C48:(("Serene, pass me","the seasoning?"),),
0x7C1C63:(("Okay. This one?",),),
0x7C1C71:(("Here it is: a","cake made with"),("the best fruit","in Elendia.")),
0x7C1C91:(("Yummy! It looks","so good..."),("Just one bite!",)),
0x7C1CB7:(("No, not yet!",),("Ein gets the","first bite."),("That is my","decision.")),
0x7C1CE8:(("Why?",),), 0x7C1CF0:(("W-Well...","Because..."),),
0x7C1CFC:(("Because why?",),), 0x7C1D02:(("Uh... No reason",),),
0x7C1D0F:(("Oh, the cake is","already done?"),),
0x7C1D49:(("More heat...","Fire!!"),),
0x7C1D69:(("Cierra! Fire!","It is burning!"),),
0x7C1D83:(("Oops... Now?",),("Flood spell...",)),
0x7C1DA7:(("It will ruin","our house!"),), 0x7C1DB9:(("Oh dear...",),),
0x7C1DC0:(("Stop talking!","Put it out!"),("The whole house","will burn down!")),
0x7C1DEA:(("It has already","been a month..."),("It all seems","so surreal."),("We made it back","alive.")),
0x7C1E37:(("I know what","you mean."),), 0x7C1E3E:(("Still...",),),
0x7C1E50:(("I still have","no voice!"),),
0x7C1E71:(("........",),),
0x7C1E78:(("So...",),("What will you","do now?"),("Back to Asgard","or stay here?")),
0x7C1EBA:(("Me? Well...",),),

# Lina route.
0x7C1EC7:(("Ein! Over here!",),("The treasure is","this way!")),
0x7C1EEC:(("Careful, Lina!",),), 0x7C1EF9:(("Stop worrying!",),),
0x7C1F08:(("Lina!",),), 0x7C1F0E:(("Hee hee...","Oopsie ♪"),),
# Fia route.
0x7C1F20:(("Ancient spirits","binding Riviera"),("guard our land.",)),
0x7C1F42:(("Ein!",),),
0x7C1F4B:(("It is thanks to","you, Fia."),("No demons have","appeared here.")),
0x7C1F77:(("No...",),), 0x7C1F7D:(("Thanks to you,","Ein."),),
0x7C1F8E:(("No. I did","nothing."),("You are strong,","Fia.")),
0x7C1FB0:(("May this peace","last forever."),),
0x7C1FC4:(("It will, if we","work hard."),),
0x7C1FDA:(("Yes... You are","right."),),
# Cierra route.
0x7C1FE4:(("A new herb...",),("I have never","seen it before."),("It may create","new magic.")),
0x7C2010:(("Ein, look!","A great find!"),), 0x7C2022:(("A new herb?",),),
0x7C202B:(("A ten-year leap","for magic!"),),
0x7C204D:(("Really?",),), 0x7C2054:(("I just need to","test it..."),),
0x7C205D:(("Huh?",),), 0x7C2062:(("Cough... Did it","work? Cough..."),),
0x7C207B:(("Huh!? No clue.",),("What was wrong?",)),
# Serene route.
0x7C2095:(("Take that!",),), 0x7C20A3:(("Ein!",),),
0x7C20AA:(("Was that all,","Serene?"),), 0x7C20BB:(("I think so...",),),
0x7C20C4:(("Nearby towns","can live safely"),),
0x7C20E6:(("Demons remain","in Riviera."),("But one day...",)),
0x7C210A:(("We can end them","for good."),),
0x7C2123:(("Darn right!","We sure will!"),),
# Neutral / Asgard route.
0x7C212B:(("Ein, there was","another demon"),("sighting in","Riviera.")),
0x7C214C:(("All right...",),("Time to use my","Einherjar--")),
0x7C2163:(("Easy, Ein.",),("Let the Sprites","handle it.")),
0x7C2181:(("Oh, r-right...",),),
0x7C218B:(("Now hurry!",),("Your report is","due today.")),
0x7C21A6:(("Okay. We should","do what we can."),),
0x7C21CD:(("Do not worry.",),("Riviera belongs","to the Sprites.")),
}


PUNCT = {"-":0x142,"❤":0x143,"'":0x149,"!":0x14A,"?":0x14B,":":0x14C,
         "—":0x150,"♪":0x151,"★":0x152,"(":0x157,")":0x158,"…":0x159,
         ",":0x15B,".":0x15D}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def glyph(ch: str) -> int:
    if ch == " ": return 0x08A
    if "0" <= ch <= "9": return 0x104 + ord(ch) - ord("0")
    if "A" <= ch <= "Z": return 0x10E + ord(ch) - ord("A")
    if "a" <= ch <= "z": return 0x128 + ord(ch) - ord("a")
    return PUNCT[ch]


def compact_char(ch: str) -> bytes:
    g = glyph(ch)
    if g == 0x08A: return bytes([g])
    assert 0x100 <= g <= 0x1FF
    low = g & 0xFF
    assert low not in range(0xA2, 0xAA) and low not in (0xFE, 0xFF)
    return bytes([low])


def encode_pages(pages) -> bytes:
    out = bytearray()
    for p_i, page in enumerate(pages):
        assert 1 <= len(page) <= 2, (p_i, page)
        if p_i: out += b"\xFE\x00"
        for l_i, line in enumerate(page):
            assert len(line) <= 15, (len(line), line)
            assert "'" not in line, ("apostrophe forbidden by prior visual QA", line)
            if l_i: out.append(0xA9)
            for ch in line: out += compact_char(ch)
    out.append(0xFF)
    return bytes(out)


def read_stream(rom: bytes, start: int) -> bytes:
    pos = start
    while True:
        c = rom[pos]
        pos += 2 if c == 0xFE or 0xA2 <= c <= 0xA8 else 1
        if c == 0xFF:
            return rom[start:pos]
        assert pos < len(rom), hex(start)


def build(base: bytes):
    assert len(base) == 0x800000 and sha(base) == BASE_SHA
    assert int.from_bytes(base[-2:], "little") == sum(base[:-2]) & 0xFFFF
    assert set(OWNERS.values()) == set(TEXT), (set(OWNERS.values()) - set(TEXT), set(TEXT) - set(OWNERS.values()))
    for off, expected in HOOK_GUARDS.items():
        assert base[off:off+len(expected)] == expected, (hex(off), "compact hook guard")
    assert base[ALLOCATION_START:ALLOCATION_LIMIT] == b"\xFF" * (ALLOCATION_LIMIT-ALLOCATION_START)

    out = bytearray(base)
    allowed = set()
    assert base[DISPATCH_EXTENSION_ROM:DISPATCH_EXTENSION_ROM+len(DISPATCH_EXTENSION_OLD)] == DISPATCH_EXTENSION_OLD
    out[DISPATCH_EXTENSION_ROM:DISPATCH_EXTENSION_ROM+len(DISPATCH_EXTENSION_NEW)] = DISPATCH_EXTENSION_NEW
    allowed.update(range(DISPATCH_EXTENSION_ROM,DISPATCH_EXTENSION_ROM+len(DISPATCH_EXTENSION_NEW)))
    cursor = ALLOCATION_START
    rows = []
    for owner, old_start in OWNERS.items():
        assert int.from_bytes(base[owner:owner+2], "little") == old_start & 0xFFFF, hex(owner)
        opcode = base[owner-2]
        if opcode not in (0x66,0x67):
            opcode = base[owner-3]
        assert opcode in (0x63,0x65,0x66,0x67), (hex(owner), hex(opcode))
        old = read_stream(base, old_start)
        data = encode_pages(TEXT[old_start])
        assert cursor + len(data) <= ALLOCATION_LIMIT
        out[cursor:cursor+len(data)] = data
        out[owner:owner+2] = (cursor & 0xFFFF).to_bytes(2,"little")
        allowed.update(range(cursor,cursor+len(data)))
        allowed.update((owner,owner+1))
        rows.append({
            "owner_rom":hex(owner), "opcode":hex(opcode),
            "old_stream_rom":hex(old_start), "old_bytes":len(old), "old_sha256":sha(old),
            "new_stream_rom":hex(cursor), "new_bytes":len(data), "new_sha256":sha(data),
            "pages":[list(p) for p in TEXT[old_start]],
        })
        cursor += len(data)

    out[-2:] = (sum(out[:-2]) & 0xFFFF).to_bytes(2,"little")
    allowed.update((len(out)-2,len(out)-1))
    diff = {i for i,(a,b) in enumerate(zip(base,out)) if a != b}
    assert diff and not diff-allowed, sorted(diff-allowed)[:10]
    report = {
        "stage":"S460", "version":"v0.113 RC4", "base_sha256":BASE_SHA,
        "rom_sha256":sha(out), "rom_size":len(out),
        "checksum":f"{int.from_bytes(out[-2:],'little'):04X}",
        "allocation_start":hex(ALLOCATION_START), "allocation_exclusive_end":hex(cursor),
        "allocation_bytes":cursor-ALLOCATION_START,
        "translated_streams":len(rows), "translated_pages":sum(len(v) for v in TEXT.values()),
        "changed_bytes":len(diff), "unexpected_changed_bytes":0,
        "compact_hook_entry_unchanged":True, "compact_dispatch_extended":True,
        "compact_dispatch_reserved_extent":["0xED22","0x10000"],
        "apostrophe_glyph_avoided":True,
        "translations":rows,
    }
    return bytes(out), report


def main():
    p=argparse.ArgumentParser()
    p.add_argument("rc3")
    p.add_argument("--out",required=True)
    a=p.parse_args()
    output,report=build(Path(a.rc3).read_bytes())
    dest=Path(a.out); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(output)
    dest.with_suffix(".build.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(report,indent=2,ensure_ascii=False))


if __name__ == "__main__":
    main()
