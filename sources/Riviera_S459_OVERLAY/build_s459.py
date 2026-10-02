"""Four ending page rebalances and scoped Chapter 8 dialogue on exact S458."""
from pathlib import Path
import argparse
import hashlib
import json

BASE_SHA='d4a0ea07c879b709eab959bf93d9fe625a9737f74bfe0b4305a0c33047dfd84f'
STREAMS={
 'epilogue_000':(0x6681FA,360,'7f602009965fcef8ff6300c831d7c4c6305fc0800fa93ab63676e0f987824ee7',2),
 'epilogue_003':(0x662BE2,425,'b74ecf6d2f4e2e74181d3c689caff81a3cb42876490963cb3a35430ecfdd6532',3),
 'epilogue_009':(0x667C1D,397,'0283910ae85cef1726cd1d968be80d146871334875f1ccf721ea88c92898fe35',2),
 'epilogue_011':(0x662888,430,'a6d18a2d1eee0ef22e11d053850cd7fc6e929951258f4f5ad6c19ad47bf1626b',2),
}
OWNERS={'epilogue_000':0x793883,'epilogue_003':0x7939AB,'epilogue_009':0x793B26,'epilogue_011':0x793B6C}
CH8_ALLOCATION=0x7FFC34
CH8_GUARDS=[
 ('Darknage_intro',0x79CB0C,0x7F8FE9,46,'18847df4828ac9608e863f245139d51bccb3d47f12ae301b9853607f2814aa61',('The Underworld', 'You may not\nexist here.')),
 ('Darknage_identity',0x79CB18,0x7F902C,41,'ef352cdcbf504b6c9843862c5c9c44bd3b13ea653271a25815f66a78194b0391',('I am Hades.','I am the\nabyssal dark,','sealed in this\nworld.')),
 ('Ein_Hades_echo',0x79CB1C,0x7F9055,7,'a1b0afdb1c16713f7ffaca96c5939cec9baa4e05aedacdc0dca2fc296a85ed3f',('Hades...',)),
 ('Ein_dark_king',0x79CB20,0x7F905C,22,'9879405a920a7d66386d4a53972d138155520e60b8fa90ac9aa8acad57e85dd5',('The Dark King','who defied\nthe gods...?')),
 ('Darknage_threat',0x79CB24,0x7F9072,37,'b12e9807b36354a864b586ed335d962dd9f27e30c2d4e396229c97c6afade89e',('You touched the\nroot of evil.','Curse your fate\nas you die!')),
 ('Cierra_warning',0x79CB35,0x7F9097,19,'c1dc6bdf1b6849aadd7aa9315498838815633192a532b90599a65ecfb0e0bb96',('Ein! Here he\ncomes!',)),
 ('Ein_response',0x79CB39,0x7F90AA,22,'d921636b44ae7fb608766fec7e9d9fff4b65aaf5b904e81d293a8302a218004e',('We cannot run.\nLet us fight!',)),
]

def sha(b):return hashlib.sha256(b).hexdigest()

def tokens(raw):
    pos=0
    while pos<len(raw):
        c=raw[pos];length=2 if c==0xFE or 0xA2<=c<=0xA8 else 1
        yield pos,c,raw[pos:pos+length]
        pos+=length
    assert pos==len(raw)

def text_only(raw):
    return b''.join(t for _,c,t in tokens(raw) if c not in (0xA9,0xFE))

def encode_text(text):
    punct={"'":0x149,'!':0x14A,'?':0x14B,'.':0x15D,',':0x15B,'-':0x142}
    out=bytearray()
    for char in text:
        if char=='\n':out.append(0xA9);continue
        if char==' ':out.append(0x8A);continue
        if '0'<=char<='9':glyph=0x104+ord(char)-ord('0')
        elif 'A'<=char<='Z':glyph=0x10E+ord(char)-ord('A')
        elif 'a'<=char<='z':glyph=0x128+ord(char)-ord('a')
        else:glyph=punct[char]
        out.extend((0xA2,glyph&255))
    return bytes(out)

def rebalance(raw,page):
    controls=[pos for pos,c,t in tokens(raw) if c==0xFE and t==b'\xFE\x00']
    assert len(controls)>=page
    old_control=controls[page-1]
    previous=controls[page-2]+2 if page>1 else 0
    breaks=[pos for pos,c,t in tokens(raw) if c==0xA9 and previous<=pos<old_control]
    assert len(breaks)==8,(page,breaks)
    split=breaks[5]  # six lines on penultimate page, remaining lines move to last
    new=raw[:split]+b'\xFE\x00'+raw[split+1:old_control]+b'\xA9'+raw[old_control+2:]
    assert len(new)==len(raw) and text_only(raw)==text_only(new)
    assert new.count(b'\xFE\x00')==raw.count(b'\xFE\x00')
    assert new.endswith(b'\xFF') and new!=raw
    return new,split,old_control

def build(base):
    assert len(base)==0x800000 and sha(base)==BASE_SHA
    assert int.from_bytes(base[-2:],'little')==sum(base[:-2])&0xFFFF
    out=bytearray(base);changes=[];allowed=set()
    for name,(start,length,digest,page) in STREAMS.items():
        old=base[start:start+length]
        assert sha(old)==digest,(name,sha(old))
        assert old[-1]==0xFF and base[start+length]!=0xFF
        owner=OWNERS[name]
        assert int.from_bytes(base[owner:owner+2],'little')==start-0x660000,(name,'owner')
        new,split,old_control=rebalance(old,page)
        out[start:start+length]=new
        allowed.update(range(start,start+length))
        changes.append({'id':name,'start':hex(start),'bytes':length,'old_sha256':digest,'new_sha256':sha(new),'page_break_moved_from':hex(start+old_control),'page_break_moved_to':hex(start+split),'pages':old.count(b'\xFE\x00')+1,'text_glyph_bytes_identical':True})
    ch8=[];cursor=CH8_ALLOCATION
    assert base[CH8_ALLOCATION:0x7FFF00]==b'\xFF'*(0x7FFF00-CH8_ALLOCATION),'allocation not blank'
    assert base[0x79CB10:0x79CB12]==bytes.fromhex('80c0'),'Fia S458 guard'
    assert base[0x79CB14:0x79CB16]==bytes.fromhex('2590'),'Ein pause guard'
    for name,owner,old_start,length,digest,pages in CH8_GUARDS:
        assert sha(base[old_start:old_start+length])==digest,name
        assert base[old_start+length-1]==0xFF
        assert int.from_bytes(base[owner:owner+2],'little')==old_start-0x7F0000,name
        for page_text in pages:
            assert "'" not in page_text,(name,'unapproved apostrophe glyph in dialogue')
            assert all(len(line)<=17 for line in page_text.split('\n')),(name,page_text)
            assert len(page_text.split('\n'))<=2,name
        data=b'\xFE\x00'.join(encode_text(page) for page in pages)+b'\xFF'
        assert cursor+len(data)<=0x7FFF00,'Chapter 8 allocation exhausted'
        out[cursor:cursor+len(data)]=data
        out[owner:owner+2]=(cursor-0x7F0000).to_bytes(2,'little')
        allowed.update(range(cursor,cursor+len(data)));allowed.update(range(owner,owner+2))
        ch8.append({'name':name,'owner_rom':hex(owner),'old_stream_rom':hex(old_start),'new_stream_rom':hex(cursor),'new_bytes':len(data),'new_sha256':sha(data),'pages':len(pages),'english_text':list(pages),'old_stream_sha256':digest})
        cursor+=len(data)
    out[-2:]=(sum(out[:-2])&0xFFFF).to_bytes(2,'little');allowed.update([len(base)-2,len(base)-1])
    diff={i for i,(a,b) in enumerate(zip(base,out)) if a!=b}
    assert diff and not diff-allowed
    for name,(start,length,digest,page) in STREAMS.items():
        assert base[OWNERS[name]:OWNERS[name]+2]==out[OWNERS[name]:OWNERS[name]+2]
    report={'base_sha256':BASE_SHA,'rom_sha256':sha(out),'checksum':f'{int.from_bytes(out[-2:],"little"):04X}','changed_bytes':len(diff),'unexpected_changed_bytes':0,'epilogue_glyphs_and_semantics_unchanged':True,'epilogue_operations':changes,'chapter8_translations':ch8,'allocation_exclusive_end':hex(cursor),'release_classification':'EXPERIMENTAL_INTERNAL_TEST','final_approved':False}
    return bytes(out),report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('rc2');p.add_argument('--out',required=True);a=p.parse_args()
    out,report=build(Path(a.rc2).read_bytes());dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(out);dest.with_suffix('.build.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
