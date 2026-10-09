#!/usr/bin/env python3
"""Bounded opcode-level regression test for every C000 selector interval."""
from pathlib import Path
import argparse, hashlib, json

PATCH=0x75EAF1
S459=bytes.fromhex("ebd1ffffffffffffffff")
RC5=bytes.fromhex("eb0081ff22ed7299ebe1")
RC6=bytes.fromhex("81ff22ed73e5ebcbffff")
BOUNDS=(0,0x3D3,0x435,0xEA4,0xB227,0xB529,0xDBE1,0xDC00,0xED22,0x10000)

def execute(rom,di):
    # The real entry at 75EA80 pushes AX before dispatching to the C000 arm.
    pc=0x75EAE0;ax=0;cf=zf=False;stack=[0];path=[]
    word=lambda p:int.from_bytes(rom[p:p+2],"little")
    signed=lambda value,bits:value-(1<<bits) if value&(1<<(bits-1)) else value
    for _ in range(60):
        path.append(hex(pc))
        if pc in (0x75D57B,0x75D583):return ("NATIVE" if pc==0x75D57B else "COMPACT"),path
        op=rom[pc]
        if op==0x50:stack.append(ax);pc+=1
        elif op==0x58:ax=stack.pop();pc+=1
        elif rom[pc:pc+2]==b"\x89\xf8":ax=di;pc+=2
        elif op==0x3D:rhs=word(pc+1);cf,zf=ax<rhs,ax==rhs;pc+=3
        elif rom[pc:pc+2]==b"\x81\xff":rhs=word(pc+2);cf,zf=di<rhs,di==rhs;pc+=4
        elif op in (0x72,0x73,0x74,0xEB):
            take=op==0xEB or op==0x72 and cf or op==0x73 and not cf or op==0x74 and zf
            delta=signed(rom[pc+1],8);pc+=2
            if take:pc+=delta
        elif op==0xE9:delta=signed(word(pc+1),16);pc+=3+delta
        else:raise AssertionError((hex(pc),hex(op)))
    raise AssertionError("instruction budget exceeded")

def main():
    p=argparse.ArgumentParser();p.add_argument("rc5");p.add_argument("rc6");p.add_argument("--out",required=True);a=p.parse_args()
    before=bytearray(Path(a.rc5).read_bytes());after=Path(a.rc6).read_bytes();old=bytearray(before)
    assert before[PATCH:PATCH+10]==RC5 and after[PATCH:PATCH+10]==RC6
    old[PATCH:PATCH+10]=S459
    rows=[]
    for lo,hi in zip(BOUNDS,BOUNDS[1:]):
        for value in sorted({lo,hi-1}):
            base,_=execute(old,value);broken,_=execute(before,value);fixed,path=execute(after,value)
            rows.append({"di":hex(value),"pre_s460":base,"rc5":broken,"rc6":fixed,"rc6_path":path})
            assert fixed==base or value>=0xED22 and fixed=="COMPACT"
    assert execute(after,0xB227)[0]==execute(after,0xB528)[0]=="COMPACT"
    assert execute(after,0xDBE1)[0]==execute(after,0xDBFF)[0]=="COMPACT"
    assert execute(after,0xED22)[0]==execute(after,0xFFFF)[0]=="COMPACT"
    restored=0
    for lo,hi in ((0xB227,0xB529),(0xDBE1,0xDC00)):
        for value in range(lo,hi):
            assert execute(old,value)[0]=='COMPACT'
            assert execute(before,value)[0]=='NATIVE'
            assert execute(after,value)[0]=='COMPACT'
            restored+=1
    assert restored==801
    report={"result":"PASS","method":"BOUNDED_OPCODE_INTERPRETER","cases":len(rows),"rows":rows,
            "exhaustive_lost_range_offsets":restored,
            "rc5_sha256":hashlib.sha256(before).hexdigest(),"rc6_sha256":hashlib.sha256(after).hexdigest()}
    Path(a.out).write_text(json.dumps(report,indent=2)+"\n")
    print("SELECTOR_TEST_PASS",len(rows))
if __name__=="__main__":main()
