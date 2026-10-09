from pathlib import Path
import sys,json,hashlib,collections,shutil
R=Path(__file__).resolve().parents[1]
P=R/'deliver/Riviera_EN_v0.111_S458_RC2_FULL_PACKAGE'
sys.path.insert(0,str(P/'sources/Riviera_S457_FULL_SOURCE/scripts/vendor'))
from ws_patch_tools import bps
sha=lambda x:hashlib.sha256(x).hexdigest()
jp=(R/'work_jp/Riviera - Yakusoku no Chi Riviera (Japan).wsc').read_bytes()
rc=(R/'root_global/Riviera_EN_v0.111_S458_RC2.wsc').read_bytes()
assert sha(rc)=='d4a0ea07c879b709eab959bf93d9fe625a9737f74bfe0b4305a0c33047dfd84f'
p=bps.create(jp,rc,metadata='Riviera WSC English v0.111 S458 RC2; EXPERIMENTAL_INTERNAL_TEST; clean JP -> RC2')
(P/'patches/Riviera_EN_v0.111_S458_RC2_CUMULATIVE_FROM_JP.bps').write_bytes(p)
checks={'roundtrip_byte_exact':bps.apply(jp,p)==rc,'checksum_valid':sum(rc[:-2])&65535==int.from_bytes(rc[-2:],'little')}
for name,src,patch in [('wrong_source',rc,p),('truncated',jp,p[:-17]),('corrupt',jp,p[:50]+bytes([p[50]^1])+p[51:])]:
 try:bps.apply(src,patch);checks[name+'_rejected']=False
 except (ValueError,IndexError):checks[name+'_rejected']=True
assert all(checks.values())
report={'result':'PASS','source_sha256':sha(jp),'target_sha256':sha(rc),'bps_sha256':sha(p),'checks':checks,'applicator':'packaged ws_patch_tools.bps','independent_applicator':'NOT_VALIDATED'}
(P/'validation/BPS_ROUNDTRIP.json').write_text(json.dumps(report,indent=2)+'\n')
rows=json.loads((P/'sources/Riviera_S457_FULL_SOURCE/analysis/PW2/RESOURCE_MATRIX_1766.json').read_text())
changes=[]
for r in rows:
 start,end=int(r['physical_start'],16),int(r['physical_end_exclusive'],16)
 new=sha(rc[start:end])
 if new!=r['stored_sha256']:
  assert start<=0x662925<end,'Unexpected changed resource'
  changes.append({'stable_id':r['stable_id'],'start':hex(start),'end_exclusive':hex(end),'rc1_sha256':r['stored_sha256'],'rc2_sha256':new,'reason':'epilogue_011 spelling correction at 0x662925'})
  r['stored_sha256']=new
 r['s458_hash_match']=True
report={'result':'PASS','resource_count':len(rows),'unchanged':len(rows)-len(changes),'intentionally_updated':changes,'rom_sha256':sha(rc),'scope':'Historical physical intervals, not exhaustive pointer or linguistic/visual approval','coverage_dimensions':{k:dict(collections.Counter(r[k] for r in rows)) for k in ['linguistic_status','visual_status','runtime_status','translation_status']}}
(P/'validation/RESOURCE_1766_REGRESSION.json').write_text(json.dumps(report,indent=2)+'\n')
(P/'validation/RESOURCE_MATRIX_1766_RC2.json').write_text(json.dumps(rows,indent=2)+'\n')
shutil.copy2(R/'root_global/Riviera_EN_v0.111_S458_RC2.build.json',P/'validation/BUILD_S458.json')
print(json.dumps({'bps_sha256':sha(p),'resource_changes':changes,'checks':checks},indent=2))
