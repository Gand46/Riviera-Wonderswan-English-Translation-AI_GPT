import argparse,json,os,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('state');p.add_argument('frames',type=int);p.add_argument('inputs',help='JSON array of [button,start,end,period,width]');p.add_argument('--timeout',type=int,default=50);p.add_argument('--rom',default=str(ROOT/'build/Riviera_v099_S446.wsc'));p.add_argument('--access');p.add_argument('--mesen',default=os.getenv('MESEN_PATH',str(ROOT.parent/'work/mesen/Mesen')));a=p.parse_args()
out=ROOT/'evidence'/a.name;out.mkdir(parents=True,exist_ok=True)
inputs=json.loads(a.inputs)
(out/'inputs.json').write_text(json.dumps(inputs,indent=2))
(out/'inputs.lua').write_text('return '+str(inputs).replace('[','{').replace(']','}')+'\n')
parent=Path(a.state).resolve().parent/'report.json'
access=a.access or ('controlled_native_screen_entry' if os.environ.get('QA_EXT','').endswith('team_native.lua') else json.loads(parent.read_text()).get('access','checkpoint_and_scripted_input') if parent.exists() else 'checkpoint_and_scripted_input')
env=dict(os.environ,QA_ACCESS=access,QA_OUT=str(out),QA_STATE=str(Path(a.state).resolve()),QA_FRAMES=str(a.frames),QA_INPUT=str(out/'inputs.lua'),QA_RANGES=str(ROOT/'scripts/residual_ranges.lua'))
cmd=['bash',str(ROOT/'scripts/run_mesen_lua_qa.sh'),str(Path(a.mesen).resolve()),str(Path(a.rom).resolve()),str(ROOT/'scripts/route.lua'),str(a.timeout)]
(out/'invocation.json').write_text(json.dumps({'command':cmd,'state':env['QA_STATE'],'frames':a.frames,'rom_sha256':hashlib.sha256(Path(a.rom).read_bytes()).hexdigest(),'access':access,'extension':os.environ.get('QA_EXT')},indent=2))
with (out/'run.log').open('w') as f:r=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=a.timeout+10)
print(a.name,'exit',r.returncode,(out/'report.json').read_text() if (out/'report.json').exists() else (out/'run.log').read_text()[-3000:])
