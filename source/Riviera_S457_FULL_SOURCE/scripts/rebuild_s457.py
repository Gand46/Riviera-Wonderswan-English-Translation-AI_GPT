"""Rebuild clean JP through cumulative S456 sources, then apply S457 sources.

The S456 source archive is stored as GitHub-safe chunks.  This script streams
the chunks into a temporary ZIP, verifies the original archive hash, and never
leaves a reconstructed 155 MB file in the working tree.
"""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,tempfile,zipfile
from build_s457 import build,sha
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('clean');p.add_argument('--out',default=str(R/'build/Riviera_v0110_S457.wsc'));a=p.parse_args();clean=Path(a.clean).resolve();spec=json.loads((R/'source/RELEASE.json').read_text());assert sha(clean.read_bytes())==spec['clean_sha256']
parts=sorted((R/'upstream').glob('Riviera_S456_Full_Source_BPS_QA.zip.part*'))
assert parts,'Missing S456 source archive chunks'
with tempfile.TemporaryDirectory(prefix='riviera_s457_') as tmp:
 z=Path(tmp)/'Riviera_S456_Fuentes_Completas_BPS_QA.zip'
 with z.open('wb') as dst:
  for part in parts: dst.write(part.read_bytes())
 assert sha(z.read_bytes())==spec['upstream_sha256'],'S456 source archive hash mismatch'
 d=Path(tmp)/'S456';d.mkdir()
 with zipfile.ZipFile(z)as q:
  for item in q.infolist():assert(d/item.filename).resolve().is_relative_to(d.resolve())
  q.extractall(d)
 base=Path(tmp)/'rebuilt_S456.wsc';subprocess.run([sys.executable,str(d/'Riviera_S456_FULL_SOURCE/scripts/rebuild_s456.py'),str(clean),'--out',str(base)],check=True)
 out,report=build(base.read_bytes())
o=Path(a.out);o.parent.mkdir(parents=True,exist_ok=True);o.write_bytes(out);o.with_suffix('.rebuild.json').write_text(json.dumps({'source_chain':'CLEAN_JP -> cumulative S456 sources -> S457','bps_used':False,'rom_sha256':sha(out),'result':'PASS'},indent=2)+'\n');print('S457_SOURCE_REBUILD_OK',sha(out))
