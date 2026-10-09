from pathlib import Path
import os,subprocess,json,hashlib,concurrent.futures
R=Path(__file__).resolve().parent.parent;root=R/'work/rc6/Riviera_EN_v0.115_S462_RC6_GITHUB_SOURCE';q=R/'work/qa_current';state=root/'sources/Riviera_S457_FULL_SOURCE/analysis/PW3/savestates/PW3_05_second_battle_in_progress.mss';em=R/'work/emulator/Mesen'
def run(v):
 out=q/f'battle_cpu_{v}';out.mkdir(exist_ok=True);rom=R/('work/private/Riviera_S459_RC3.wsc' if v=='rc3' else 'work/private/Riviera_S462_RC6_build.wsc');env=dict(os.environ,QA_OUT=str(out),QA_STATE=str(state),LD_PRELOAD='/usr/lib/x86_64-linux-gnu/libstdc++.so.6');cmd=[str(em),'--testRunner','--timeout=15','--enableStdout','--doNotSaveSettings','--debug.scriptWindow.allowIoOsAccess=true',str(q/'battle_replay_cpu.lua'),str(rom)]
 with (out/'mesen.log').open('w') as log:rc=subprocess.run(cmd,env=env,cwd=em.parent,stdout=log,stderr=subprocess.STDOUT,timeout=25).returncode
 report={'exit':rc,'rom_sha256':hashlib.sha256(rom.read_bytes()).hexdigest(),'state_sha256':hashlib.sha256(state.read_bytes()).hexdigest(),'command':cmd,'access_method':'SAVESTATE','state_origin':'S457 PW3 second battle route','rom_writes':0};(out/'RUN.json').write_text(json.dumps(report,indent=2));print(v,rc,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:list(e.map(run,['rc3','rc6']))
