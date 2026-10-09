#!/usr/bin/env python3
"""Remove embedded ROMs recursively, updating hash identities without disabling guards.
Only works on the supplied deliverable archive and S457 RELEASE.json.
"""
from pathlib import Path
import argparse,hashlib,io,json,os,shutil,tempfile,zipfile,time,copy
BAD={'.ws','.wsc','.gba','.rom','.bios'}
TEXT={'.json','.py','.md','.txt','.csv','.tsv','.lua','.yaml','.yml','.toml','.ini','.sh','.bat','.ps1','.sha256'}
report={'removed':[],'archives':[],'text_updates':[],'zip_count':0,'strategy':'Recursive removal; exact SHA256 identity replacement; source/ROM hash guards preserved.'}
changes={}
def sha(data):return hashlib.sha256(data).hexdigest()
def fsha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def process(path,label):
 report['zip_count']+=1;oldhash=fsha(path)
 with tempfile.TemporaryDirectory(prefix='sanitize_zip_') as td:
  td=Path(td);replacements={};removed=set();infos=[]
  with zipfile.ZipFile(path) as z:
   infos=z.infolist()
   for idx,i in enumerate(infos):
    ext=Path(i.filename).suffix.lower()
    if ext in BAD and not i.is_dir():
     b=z.read(i);removed.add(i.filename);report['removed'].append({'member':label+'!'+i.filename,'bytes':len(b),'sha256':sha(b)});continue
    if ext=='.zip' and not i.is_dir():
     child=td/f'child_{idx}.zip'
     with z.open(i) as src,child.open('wb') as dst:shutil.copyfileobj(src,dst)
     changed=process(child,label+'!'+i.filename)
     if changed:replacements[i.filename]=child
   texts={}
   for i in infos:
    if i.filename not in removed and Path(i.filename).suffix.lower() in TEXT and not i.is_dir():
     b=z.read(i)
     try:b.decode('utf-8')
     except UnicodeDecodeError:continue
     texts[i.filename]=[b,b]
   for iteration in range(12):
    altered=False
    for name,(original,current) in texts.items():
     updated=current
     for old,new in changes.items():updated=updated.replace(old.encode(),new.encode())
     if updated!=current:
      changes[sha(current)]=sha(updated);texts[name][1]=updated;altered=True
    if not altered:break
   else:raise RuntimeError('Hash reference convergence failed in '+label)
   for name,(original,updated) in texts.items():
    if original!=updated:
     fn=td/f'text_{len(replacements)}';fn.write_bytes(updated);replacements[name]=fn
     changes[sha(original)]=sha(updated)
     report['text_updates'].append({'member':label+'!'+name,'old_sha256':sha(original),'new_sha256':sha(updated)})
   if not removed and not replacements:return False
   output=td/'updated.zip'
   with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as target:
    target.comment=z.comment
    for i in infos:
     if i.filename in removed:continue
     # Preserve names, dates, attributes; recompute CRC/length and compression.
     zi=copy.copy(i);zi._compresslevel=1
     with target.open(zi,'w',force_zip64=True) as dst:
      if i.filename in replacements:
       with replacements[i.filename].open('rb') as src:shutil.copyfileobj(src,dst)
      else:
       with z.open(i) as src:shutil.copyfileobj(src,dst)
  newhash=fsha(output);sizeold=Path(path).stat().st_size;sizenew=output.stat().st_size
  shutil.copyfile(output,path)
 changes[oldhash]=newhash
 report['archives'].append({'archive':label,'old_sha256':oldhash,'new_sha256':newhash,'old_bytes':sizeold,'new_bytes':sizenew})
 print('SANITIZED',Path(label.split('!')[-1]).name,flush=True)
 return True
def audit(path,label):
 with zipfile.ZipFile(path) as z:
  for i in z.infolist():
   if not i.is_dir() and Path(i.filename).suffix.lower() in BAD:raise AssertionError('ROM remains '+label+'!'+i.filename)
   if i.filename.lower().endswith('.zip'):
    with tempfile.NamedTemporaryFile(suffix='.zip') as f:
     with z.open(i) as src:shutil.copyfileobj(src,f)
     f.flush();audit(f.name,label+'!'+i.filename)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('archive');p.add_argument('--release',required=True);p.add_argument('--report',required=True);a=p.parse_args();start=time.monotonic()
 archive=Path(a.archive);release=Path(a.release);before=fsha(archive)
 spec=json.loads(release.read_text());assert spec['upstream_sha256']==before
 process(archive,archive.name)
 assert changes.get(before)==fsha(archive)
 b=release.read_bytes();after=b.replace(before.encode(),changes[before].encode());assert after!=b;release.write_bytes(after)
 report['outer_release']={'path':str(release),'old_sha256':sha(b),'new_sha256':sha(after),'old_upstream_sha256':before,'new_upstream_sha256':fsha(archive)}
 audit(archive,archive.name)
 report.update(result='PASS',recursive_forbidden_members=0,removed_members=len(report['removed']),removed_unique_payloads=len({x['sha256'] for x in report['removed']}),seconds=time.monotonic()-start,rebuild_status='PENDING')
 Path(a.report).write_text(json.dumps(report,indent=2)+'\n');print('SANITIZATION_PASS',report['removed_members'],'members',report['zip_count'],'ZIPs',flush=True)
