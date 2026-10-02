"""Re-run the 13 full native credit page probes using Mesen 2.1.1. Linux validated."""
from pathlib import Path
import argparse,subprocess,os,shutil,json
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('mesen');p.add_argument('rom');p.add_argument('--out',default=str(R/'qa_replay'));p.add_argument('--pages',default=','.join(map(str,range(13))));a=p.parse_args();exe=Path(a.mesen).resolve();rom=Path(a.rom).resolve();out=Path(a.out).resolve();env=os.environ.copy()
profile=exe.parent/'settings.json'
if not profile.exists():profile.write_text('{}\n')
if os.name=='posix':
 lib=subprocess.check_output(['g++','-print-file-name=libstdc++.so.6'],text=True).strip();assert Path(lib).is_file();env['LD_PRELOAD']=lib+(':'+env['LD_PRELOAD']if env.get('LD_PRELOAD')else '')
for i in map(int,a.pages.split(',')):
 q=out/f'page_{i:02d}';shutil.copytree(R/'qa/probes'/q.name/'inputs',q/'inputs',dirs_exist_ok=True);(q/'runtime').mkdir(exist_ok=True);env['I04_ROOT']=str(q)
 with(q/'mesen.log').open('w')as log:subprocess.run([str(exe),'--testRunner','--timeout=40','--enableStdout','--doNotSaveSettings','--debug.scriptWindow.allowIoOsAccess=true',str(R/'scripts/qa_native_probe.lua'),str(rom)],cwd=exe.parent,env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=50)
 assert json.loads((q/'runtime/native_probe_result.json').read_text())['cases_executed']==1
 print(q.name,'OK',flush=True)
