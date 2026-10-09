from pathlib import Path
import subprocess,os,json,time,hashlib,concurrent.futures,shutil
R=Path(__file__).resolve().parent.parent;src=R/'work/rc6/Riviera_EN_v0.115_S462_RC6_GITHUB_SOURCE';qa=R/'work/qa_current/stable';qa.mkdir(exist_ok=True);emu=R/'work/emulator/Mesen'
emu.chmod(0o755);(emu.parent/'settings.json').write_text('{}')
lua=qa/'ending_bind.lua';lua.write_text('local captureHoldUntil=0\n'+(R/'work/audit459/Riviera_S459_RC3_Auditoria_Astra_Japones/scripts/original/ending_bind.lua').read_text().replace('f>=5 and f%8==0','f>=5 and f>=captureHoldUntil and f%8==0').replace('pendingShot={frame=f+1,owner=currentOwner};','captureHoldUntil=f+8;pendingShot={frame=f+6,owner=currentOwner};').replace('if f==6000 then','if f==7200 then'))
# Trace the compact/native selection with no mutation of emulated ROM or text.
with lua.open('a') as f:f.write('''\nlocal ds=assert(io.open(out..'/dispatch.tsv','w'));ds:write('frame\\tpath\\tes\\tdi\\n')
local function dpath(k)local s=emu.getState();if s['cpu.es']==0xC000 and s['cpu.di']>=0xED22 then ds:write(string.format('%d\\t%s\\t%04X\\t%04X\\n',f,k,s['cpu.es'],s['cpu.di']));ds:flush()end end
emu.addMemoryCallback(function()dpath('NATIVE')end,emu.callbackType.exec,0x5D57B)
emu.addMemoryCallback(function()dpath('COMPACT')end,emu.callbackType.exec,0x5D583)
''')
boot=src/'sources/Riviera_S457_FULL_SOURCE/scripts/qa_intro_bounded.lua'
jobs=[('ending_route0','S462_RC6_build',lua,0,False)]+[(f'late_route{n}','S462_RC6_build',lua,n,True) for n in range(1,6)]
def run(job):
 name,romname,script,route,late=job;out=qa/name;out.mkdir(exist_ok=True);rom=R/f'work/private/Riviera_{romname}.wsc';env=dict(os.environ,LD_PRELOAD='/usr/lib/x86_64-linux-gnu/libstdc++.so.6')
 if route is None:env.update(MESEN_MULTI_DIR=str(out),MESEN_LUA_REPORT=str(out/'result.json'),MESEN_CAPTURE_PATH=str(out/'final.png'))
 else:env.update(I23_OUT=str(out),I23_ROUTE=str(route),I23_LATE=str(int(late)))
 cmd=[str(emu),'--testRunner','--timeout=40','--enableStdout','--doNotSaveSettings','--debug.scriptWindow.allowIoOsAccess=true',str(script),str(rom)];start=time.monotonic()
 with (out/'mesen.log').open('w') as log:
  try:code=subprocess.run(cmd,cwd=emu.parent,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=48).returncode
  except subprocess.TimeoutExpired:code=124
 rep={'exit':code,'elapsed_seconds':round(time.monotonic()-start,2),'rom_sha256':hashlib.sha256(rom.read_bytes()).hexdigest(),'command':cmd,'access_method':'SCRIPTED_NATURAL' if route is None else 'SYNTHETIC_STATE','route':route,'late_subset':late,'rom_writes':0,'images':len(list(out.glob('*.png'))),'owner_captures':len(list(out.glob('owner*.png')))}
 (out/'RUN.json').write_text(json.dumps(rep,indent=2));print(name,code,rep['owner_captures'],flush=True);return rep
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:results=list(e.map(run,jobs))
(qa/'RUNTIME_RUNS.json').write_text(json.dumps(results,indent=2))
assert all(x['exit']==0 for x in results)
