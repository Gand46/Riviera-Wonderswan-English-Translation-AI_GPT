"""Rebuild S459 RC3 cumulatively from the exact clean Japanese WSC ROM."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from build_s459 import build,sha

JP_SHA='62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921'
p=argparse.ArgumentParser();p.add_argument('clean_jp');p.add_argument('--out',required=True);a=p.parse_args()
root=Path(__file__).resolve().parent
clean=Path(a.clean_jp).resolve()
assert sha(clean.read_bytes())==JP_SHA,'Wrong clean Japanese source ROM'
with tempfile.TemporaryDirectory(prefix='riviera_s459_') as tmp:
    s458=Path(tmp)/'s458.wsc'
    subprocess.run([sys.executable,str(root.parent/'Riviera_S458_OVERLAY/rebuild.py'),str(clean),'--out',str(s458)],check=True)
    out,report=build(s458.read_bytes())
dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(out)
report.update(source_chain='JP clean -> S456 cumulative source -> S457 -> S458 -> S459',source_jp_sha256=JP_SHA,bps_used=False,result='PASS')
dest.with_suffix('.source-rebuild.json').write_text(json.dumps(report,indent=2)+'\n')
print('S459_SOURCE_REBUILD_OK',sha(out))
