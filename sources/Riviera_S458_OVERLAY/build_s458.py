"""Guarded S458 data-only corrections over exact S457; no renderer/font change."""
from pathlib import Path
import argparse,hashlib,json
BASE='80ff36655d83956d96b634adafc685fa4379da326c3d45099dedcb73ef72a951'
TARGET='d4a0ea07c879b709eab959bf93d9fe625a9737f74bfe0b4305a0c33047dfd84f'
def sha(b):return hashlib.sha256(b).hexdigest()
def build(src):
    assert len(src)==0x800000 and sha(src)==BASE,'S457 identity mismatch'
    operations=[
      (0x6610D3,b'\xff'*9,bytes.fromhex('a219a228a219a228ff'),'Terminated LaLa name; S402 reclaimed slack'),
      *[(o,bytes.fromhex('8bfb'),bytes.fromhex('d310'),'collection240 LaLa owner') for o in (0x65D45B,0x65D460,0x65D465)],
      (0x7FC080,b'\xff'*38,bytes.fromhex('a212a230a235a25da25da25da9a224a22fa22ca239a22c8aa228a239a22c8aa23ea22ca24bff'),'Fia: Ein... / Where are we?'),
      (0x79CB10,bytes.fromhex('1790'),bytes.fromhex('80c0'),'Chapter8 first Fia dialogue owner'),
      (0x66291A,bytes.fromhex('a230a235a23aa22ca237a22ca239a228a229a233a22c'),bytes.fromhex('a230a235a23aa22ca237a228a239a228a229a233a22c'),'epilogue_011: inseperable -> inseparable'),
    ]
    assert src[0x7F9017:0x7F9025].hex()=='53575d78a2eba259090919a247ff'
    assert src[0x7FC073:0x7FC078].hex()=='ea60b000f0','S450 stub guard'
    out=bytearray(src);allowed=set();ranges=[]
    for off,old,new,reason in operations:
        assert len(old)==len(new) and src[off:off+len(old)]==old,(hex(off),'precondition')
        s=set(range(off,off+len(new)));assert not s&allowed,'overlap';allowed|=s
        out[off:off+len(new)]=new
        ranges.append(dict(offset=hex(off),length=len(new),before=old.hex(),after=new.hex(),reason=reason))
    out[-2:]=(sum(out[:-2])&65535).to_bytes(2,'little');allowed|={len(src)-2,len(src)-1}
    changed=[i for i,(a,b) in enumerate(zip(src,out)) if a!=b]
    assert not set(changed)-allowed and sha(out)==TARGET
    assert out[0x66FB93:0x66FC12]==src[0x66FB93:0x66FC12]
    report=dict(stage='v0.111-S458-RC2',status='EXPERIMENTAL_INTERNAL_TEST',base_sha256=BASE,rom_sha256=sha(out),bytes_changed=len(changed),unexpected_changed_offsets=0,checksum=f'{int.from_bytes(out[-2:],"little"):04X}',operations=ranges,shared_font_or_renderer_changed=False,final_approved=False)
    return bytes(out),report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('base');p.add_argument('--out',required=True);a=p.parse_args()
    out,report=build(Path(a.base).read_bytes());dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(out);dest.with_suffix('.build.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
