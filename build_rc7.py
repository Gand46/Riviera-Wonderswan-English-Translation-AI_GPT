#!/usr/bin/env python3
"""Portable clean-JP to S463 RC7 cumulative-source entry point."""
import argparse,hashlib,subprocess,sys
from pathlib import Path
SOURCE='62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921'
TARGET='933cfcd5ea40f0f1d960338e78dc60ead6d8e5c280ea28bc69007f55ed2cc7aa'
p=argparse.ArgumentParser();p.add_argument('clean_jp');p.add_argument('--out',default='build/Riviera_EN_v0.116_S463_RC7.wsc')
a=p.parse_args();root=Path(__file__).resolve().parent
clean=Path(a.clean_jp).resolve();dest=Path(a.out).resolve()
if clean==dest:raise SystemExit('Source and output must be different files')
assert hashlib.sha256(clean.read_bytes()).hexdigest()==SOURCE,'Wrong clean Japanese ROM'
subprocess.run([sys.executable,str(root/'sources/Riviera_S463_OVERLAY/rebuild.py'),str(clean),'--out',str(dest)],check=True)
assert hashlib.sha256(dest.read_bytes()).hexdigest()==TARGET,'Unexpected S463 output'
print('RC7_FULL_SOURCE_REBUILD_OK',TARGET)
