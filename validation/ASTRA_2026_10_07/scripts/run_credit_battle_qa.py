from pathlib import Path
import os,subprocess,json,hashlib,time,concurrent.futures
R=Path(__file__).resolve().parent.parent;root=R/'work/rc6/Riviera_EN_v0.115_S462_RC6_GITHUB_SOURCE';qa=R/'work/qa_current';em=R/'work/emulator/Mesen'
credit=qa/'credits_replay.lua';credit.write_text((R/'work/audit459/Riviera_S459_RC3_Auditoria_Astra_Japones/scripts/original/credits_probe.lua').read_text().replace('f>=2100','f>=4500'))
battle=qa/'battle_replay.lua';battle.write_text('''local out=assert(os.getenv('QA_OUT'));local state=assert(os.getenv('QA_STATE'));local loaded=false;local f=0
local function w(p,d)local h=assert(io.open(out..'/'..p,'wb'));h:write(d);h:close()end
local cb;cb=emu.addMemoryCallback(function()local h=assert(io.open(state,'rb'));local d=h:read('*a');h:close();emu.loadSavestate(d);loaded=true;emu.removeMemoryCallback(cb,emu.callbackType.exec,0,0xfffff)end,emu.callbackType.exec,0,0xfffff)
emu.addEventCallback(function()local t={};if f>=60 and f%37<3 then t.a=true end;emu.setInput(t,0)end,emu.eventType.inputPolled)
emu.addEventCallback(function()f=f+1;if f%300==0 or f==1 then w(string.format('frame_%04d.png',f),emu.takeScreenshot())end;if f==1200 then w('END.mss',emu.createSavestate());local t={};for a=0,65535 do t[#t+1]=string.char(emu.read(a,emu.memType.wsWorkRam))end;w('final_wram.bin',table.concat(t));w('RESULT.json','{"frames":1200,"access_method":"SAVESTATE","rom_writes":0}');emu.stop(0)end end,emu.eventType.endFrame)
''')
cs=root/'validation/S460/final_routes/final_route0_full/chunk2/checkpoint_02000.mss';bs=root/'sources/Riviera_S457_FULL_SOURCE/analysis/PW3/savestates/PW3_05_second_battle_in_progress.mss'
jobs=[('credits_rc6','S462_RC6_build',credit,cs,True),('battle_rc3','S459_RC3',battle,bs,False),('battle_rc6','S462_RC6_build',battle,bs,False)]
def run(j):
 name,romstem,lua,state,iscredit=j;out=qa/name;out.mkdir(exist_ok=True);rom=R/f'work/private/Riviera_{romstem}.wsc';env=dict(os.environ,LD_PRELOAD='/usr/lib/x86_64-linux-gnu/libstdc++.so.6')
 if iscredit:env.update(ASTRA_OUT=str(out),ASTRA_RESUME=str(state))
 else:env.update(QA_OUT=str(out),QA_STATE=str(state))
 cmd=[str(em),'--testRunner','--timeout=30','--enableStdout','--doNotSaveSettings','--debug.scriptWindow.allowIoOsAccess=true',str(lua),str(rom)];t=time.monotonic()
 with (out/'mesen.log').open('w') as log:rc=subprocess.run(cmd,env=env,cwd=em.parent,stdout=log,stderr=subprocess.STDOUT,timeout=40).returncode
 rep={'exit':rc,'seconds':time.monotonic()-t,'rom_sha256':hashlib.sha256(rom.read_bytes()).hexdigest(),'state':str(state),'state_sha256':hashlib.sha256(state.read_bytes()).hexdigest(),'access_method':'SAVESTATE','state_origin':'S460 synthetic ending' if iscredit else 'S457 PW3 gameplay route','command':cmd,'rom_writes':0};(out/'RUN.json').write_text(json.dumps(rep,indent=2));print(name,rc,flush=True);return rep
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:results=list(ex.map(run,jobs))
(qa/'CREDIT_BATTLE_RUNS.json').write_text(json.dumps(results,indent=2));assert all(x['exit']==0 for x in results)
