#!/usr/bin/env python3
"""Rebuild the complete S463 source chain from clean Japanese Riviera."""
import argparse, hashlib, json, subprocess, sys, tempfile
from pathlib import Path
from build_s463 import build

JP_SHA='62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921'
p=argparse.ArgumentParser();p.add_argument('clean_jp');p.add_argument('--out',required=True)
a=p.parse_args();clean=Path(a.clean_jp).resolve();dest=Path(a.out).resolve()
if clean==dest:raise SystemExit('Source and output must be different files')
assert hashlib.sha256(clean.read_bytes()).hexdigest()==JP_SHA,'Wrong Japanese ROM'
root=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='riviera_s463_') as td:
    rc6=Path(td)/'s462.wsc'
    subprocess.run([sys.executable,str(root.parent/'Riviera_S462_OVERLAY/rebuild.py'),str(clean),'--out',str(rc6)],check=True)
    output,report=build(rc6.read_bytes())
dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(output)
report.update(source_chain='Clean JP -> S441 -> cumulative S462 sources -> S463',bps_used=False,result='PASS',source_jp_sha256=JP_SHA)
dest.with_suffix('.full-source-rebuild.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print('S463_FULL_SOURCE_REBUILD_OK',hashlib.sha256(output).hexdigest())
