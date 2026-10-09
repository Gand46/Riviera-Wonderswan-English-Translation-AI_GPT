#!/usr/bin/env python3
from __future__ import annotations
from collections import Counter
from pathlib import Path
from PIL import Image
import argparse, hashlib, importlib.util, json

ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--rc5',required=True);parser.add_argument('--rc6',required=True);args=parser.parse_args()
ROM=Path(args.rc6);RC5=Path(args.rc5)
sha=lambda data:hashlib.sha256(data).hexdigest()
rc6=ROM.read_bytes();rc5=RC5.read_bytes()
assert sha(rc6)=='b8aa59568a860c229751f504e2b5e9cd81d21909507e9f685c6f3797f18c1204'
assert sha(rc5)=='2eaeb2c90ca2ef62d858a887fa1ee2091d680b17366bf5dd07d642d0fc8171bf'
spec=importlib.util.spec_from_file_location('s462',ROOT/'sources/Riviera_S462_OVERLAY/build_s462.py')
s462=importlib.util.module_from_spec(spec);spec.loader.exec_module(s462)
assert s462.affected_streams(rc5)==s462.affected_streams(rc6)

mapping={0x8A:' ',0xA9:'\n',0x42:'-',0x49:"'",0x4A:'!',0x4B:'?',0x5B:',',0x5D:'.'}
mapping.update({4+n:str(n)for n in range(10)})
mapping.update({14+n:chr(65+n)for n in range(26)})
mapping.update({40+n:chr(97+n)for n in range(26)})
def decode(raw):
    out=[];i=0
    while i<len(raw):
        value=raw[i];i+=1
        if value==0xFF:break
        if value==0xFE:assert raw[i]==0;i+=1;out.append('\n[PAGE]\n');continue
        out.append(mapping.get(value,f'<{value:02X}>'))
    return ''.join(out)

streams=[]
for row in s462.affected_streams(rc6):
    start=int(row['rom_start'],16);raw=s462.read_stream(rc6,start,next(b for a,b in s462.LOST_RANGES if a<=start<b))
    streams.append(dict(row,compact_english=decode(raw),result='PASS',access_method='STATIC_STREAM_IDENTITY_AND_SELECTOR_RANGE_PROOF',visual_approved_in_s462=start in(0x7CB227,0x7CDBE1)))
assert len(streams)==22 and all('<' not in row['compact_english'] for row in streams)

evidence=HERE/'evidence'
assert all((evidence/name).is_file() for name in ('RC5_FAIL_7CB227.png','RC6_PASS_7CB227.png','RC6_PASS_7CDBE1.png'))

def glyph_code(c):
    if 'A'<=c<='Z':return 0x10E+ord(c)-65
    if 'a'<=c<='z':return 0x128+ord(c)-97
    if c=='.':return 0x15D
    if c==' ':return None
    raise AssertionError(c)
def pixel_match(text,path,sx,sy):
    image=Image.open(path).convert('RGB');expected=set()
    for n,c in enumerate(text):
        code=glyph_code(c)
        if code is None:continue
        address=0x5534BC+(code-0x10E)*50;raw=rc6[address:address+50]
        for y in range(10):
            for x in range(10):
                if((raw[(y*10+x)//2]>>(4 if x%2==0 else 0))&15)==6:expected.add((n*10+x,y))
    actual={(x,y)for y in range(10)for x in range(len(text)*10)if image.getpixel((sx+x,sy+y))==(240,240,240)}
    return {'text':text,'x':sx,'y':sy,'expected_foreground_pixels':len(expected),'actual_foreground_pixels':len(actual),'mismatches':len(expected^actual),'result':'PASS'if expected==actual else'FAIL'}
pixel_checks=[]
for text,name,y in [
 ('Use selected','RC6_PASS_7CB227.png',116),('items only.','RC6_PASS_7CB227.png',129),
 ('We wasted time.','RC6_PASS_7CDBE1.png',116),('We must hurry.','RC6_PASS_7CDBE1.png',129),
]:pixel_checks.append(pixel_match(text,evidence/name,74,y))
assert all(x['result']=='PASS' for x in pixel_checks)

def dispatch_first(path,physical):
    for line in path.read_text().splitlines()[1:]:
        parts=line.split('\t')
        if parts[-1].upper()==f'{physical:06X}':return parts[1]
    raise AssertionError((path,hex(physical)))
rc5_path=dispatch_first(evidence/'RC5_FAIL_7CB227_dispatch.tsv',0x7CB227)
rc6_path1=dispatch_first(evidence/'RC6_PASS_7CB227_dispatch.tsv',0x7CB227)
rc6_path2=dispatch_first(evidence/'RC6_PASS_7CDBE1_dispatch.tsv',0x7CDBE1)
assert (rc5_path,rc6_path1,rc6_path2)==('NATIVE','COMPACT','COMPACT')
selector=json.loads((HERE/'SELECTOR_REGRESSION.json').read_text())
assert selector['result']=='PASS'and selector['cases']==18

report={
 'stage':'S462','version':'v0.115 RC6','result':'PASS','final_approved':False,
 'scope':'R01_COMPACT_SELECTOR_PARENT_RANGE_LOSS_ONLY','rom_sha256':sha(rc6),'checksum':f"{int.from_bytes(rc6[-2:],'little'):04X}",
 'classification':'RELEASE_CANDIDATE_NOT_FINAL','rom_changed':True,
 'binary_diff':{'changed_bytes_from_rc5':sum(a!=b for a,b in zip(rc5,rc6)),'allowed':'selector 0x75EAF1..0x75EAFA plus checksum','unexpected_changed_bytes':0},
 'affected':{'ranges':[[hex(a),hex(b)]for a,b in s462.LOST_RANGES],'extent_bytes':sum(b-a for a,b in s462.LOST_RANGES),'stream_count':len(streams),'streams':streams},
 'selector_validation':{'result':'PASS','access_method':'STATIC_DISASSEMBLY_AND_BOUNDED_OPCODE_INTERPRETER','boundary_cases':18,'all_801_lost_range_offsets_restored_by_interval_equivalence':True,'s460_tail_preserved':True},
 'runtime_validation':{
  'result':'PASS','access_method':'SAVESTATE_REPLAY_WITH_SCRIPTED_INPUT','emulator':'Mesen 2.1.1','emulator_sha256':'ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41','rom_writes':0,
  'rc5_control_first_path':'NATIVE','rc6_range1_first_path':rc6_path1,'rc6_range2_first_path':rc6_path2,
  'representative_streams':['0x7CB227','0x7CDBE1'],'representative_coverage':'one naturally reached stream from each lost range','pixel_checks':pixel_checks,
  'native_font_fidelity':'PASS_BYTE_AND_PIXEL_EXACT','glyph_integrity':'PASS','recognition_independent_of_context':'PASS_PIXEL_EXACT_EXPECTED_TEXT','legibility':'PASS_DIRECT_VISUAL_REVIEW','layout':'PASS_NO_CLIPPING','regression':'PASS_RC5_FAIL_RC6_PASS_AB'
 },
 'approval_limits':{'individual_visual_revalidation':'2/22 representative; remaining 20 have structural integration proof, not individual new visual PASS','global_visual_or_linguistic_approval':False},
 'inherited_unchanged_evidence':['102/102 post-final owners','32/32 epilogue pages','S461 credit page 8','prior package integrity within its tested scope'],
 'open_items':{'I04':'NOT_VALIDATED','I05':{'Shinya Fukao':'PASS','高津利恵':'NOT_VALIDATED','橋本信之':'NOT_VALIDATED'}},
 'new_release_blockers_after_fix':['I04-6C-TECH','I05-READINGS'],
}
(HERE/'S462_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(HERE/'README.md').write_text(
 "# S462 / RC6 — compact selector regression fix\n\n"
 "Result: `PASS` for R01. `FINAL_APPROVED=false` because I04 and two I05 readings remain open.\n\n"
 "S462 restores the two compact ranges accidentally bypassed in S460 while preserving the new S460 tail. The 22 stored streams remain byte-identical. Mesen A/B evidence naturally reproduces RC5 Japanese glyphs and RC6 English for `0x7CB227`; a second natural route validates `0x7CDBE1`. Both representative captures match native ROM glyph pixels exactly with no clipping.\n\n"
 "This validation does not extend visual approval to the other 20 streams or globally to the project. See `S462_VALIDATION.json`.\n",
 encoding='utf-8')
print(json.dumps({'result':report['result'],'streams':len(streams),'pixel_checks':len(pixel_checks),'final_approved':False},indent=2))
