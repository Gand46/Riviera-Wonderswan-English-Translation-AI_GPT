#!/usr/bin/env python3
"""Portable entry point for the complete S441-S462 source rebuild."""
from __future__ import annotations
import argparse, hashlib, subprocess, sys
from pathlib import Path

EXPECTED_SOURCE = "62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921"
EXPECTED_TARGET = "b8aa59568a860c229751f504e2b5e9cd81d21909507e9f685c6f3797f18c1204"

def sha256(path: Path) -> str:
    digest=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda:handle.read(1024*1024),b""):digest.update(chunk)
    return digest.hexdigest()

def main():
    parser=argparse.ArgumentParser();parser.add_argument("clean_jp")
    parser.add_argument("--out",default="build/Riviera_EN_v0.115_S462_RC6.wsc")
    args=parser.parse_args();root=Path(__file__).resolve().parent
    clean=Path(args.clean_jp).resolve();destination=Path(args.out).resolve()
    assert sha256(clean)==EXPECTED_SOURCE,"Wrong clean Japanese ROM"
    subprocess.run([sys.executable,str(root/"sources/Riviera_S462_OVERLAY/rebuild.py"),str(clean),"--out",str(destination)],check=True)
    assert sha256(destination)==EXPECTED_TARGET,"Unexpected RC6 output"
    print("RC6_FULL_SOURCE_REBUILD_OK",EXPECTED_TARGET)

if __name__=="__main__":main()
