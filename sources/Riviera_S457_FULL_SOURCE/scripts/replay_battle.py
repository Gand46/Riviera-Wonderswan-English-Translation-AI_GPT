from pathlib import Path
import argparse,os,subprocess,json
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('mesen');p.add_argument('rom');p.add_argument('--out',default=str(R/'battle_replay'));a=p.parse_args()
exe=Path(a.mesen).resolve();rom=Path(a.rom).resolve();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);env=os.environ.copy()
profile=exe.parent/'settings.json'
if not profile.exists():profile.write_text('{}\n')
if os.name=='posix':
 lib=subprocess.check_output(['g++','-print-file-name=libstdc++.so.6'],text=True).strip();env['LD_PRELOAD']=lib+(':'+env['LD_PRELOAD']if env.get('LD_PRELOAD')else '')
env.update(MESEN_MULTI_DIR=str(out),MESEN_LUA_REPORT=str(out/'report.json'),MESEN_STATE_PATH=str(R/'qa/checkpoints/ACTION_PRE_DRAW.mss'))
with(out/'mesen.log').open('w')as log:subprocess.run([str(exe),'--testRunner','--timeout=60','--enableStdout','--doNotSaveSettings','--debug.scriptWindow.allowIoOsAccess=true',str(R/'scripts/qa_battle.lua'),str(rom)],cwd=exe.parent,env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=70)
assert json.loads((out/'report.json').read_text())['capture_complete'];print('2500 frames completed from checkpoint')
