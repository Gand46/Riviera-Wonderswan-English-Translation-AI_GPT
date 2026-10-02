"""Rebuild clean Japanese ROM through full S457 sources and guarded S458 fixes."""
from pathlib import Path
import argparse,subprocess,sys,json,tempfile
from build_s458 import build,sha
p=argparse.ArgumentParser();p.add_argument('clean');p.add_argument('--out',required=True);a=p.parse_args()
root=Path(__file__).resolve().parent
clean=Path(a.clean).resolve();assert sha(clean.read_bytes())=='62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921'
with tempfile.TemporaryDirectory(prefix='riviera_s458_') as tmp:
    s457=Path(tmp)/'S457.wsc'
    subprocess.run([sys.executable,str(root.parent/'Riviera_S457_FULL_SOURCE/scripts/rebuild_s457.py'),str(clean),'--out',str(s457)],check=True)
    out,report=build(s457.read_bytes())
dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(out)
report.update(source_chain='Clean JP -> complete cumulative S456 sources -> S457 -> S458',bps_used=False,result='PASS')
dest.with_suffix('.source-rebuild.json').write_text(json.dumps(report,indent=2)+'\n');print('S458_SOURCE_REBUILD_OK',sha(out))
