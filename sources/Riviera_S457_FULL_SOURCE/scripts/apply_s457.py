from pathlib import Path
import argparse,json,sys,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts/vendor'));from ws_patch_tools import bps
p=argparse.ArgumentParser();p.add_argument('clean');p.add_argument('--out',default=str(R/'build/Riviera_v0110_S457.wsc'));a=p.parse_args();b=Path(a.clean).read_bytes();s=json.loads((R/'source/RELEASE.json').read_text());assert hashlib.sha256(b).hexdigest()==s['clean_sha256'];b=bps.apply(b,(R/'patches/Riviera_CLEAN_JP_to_v0110_S457_cumulative.bps').read_bytes());assert hashlib.sha256(b).hexdigest()==s['target_sha256'];o=Path(a.out);o.parent.mkdir(parents=True,exist_ok=True);o.write_bytes(b);print('S457_BPS_OK')
