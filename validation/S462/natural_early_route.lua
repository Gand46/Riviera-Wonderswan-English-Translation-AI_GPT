-- Read-only natural replay from the existing PW3 checkpoint.
local out=assert(os.getenv('QA_OUT'))
local source=assert(os.getenv('QA_STATE'))
local maxf=tonumber(os.getenv('QA_FRAMES') or '5200')
local f=0;local loaded=false;local lid;local pending={};local reads={};local dispatch={};local captured={};local hold=false;local hold_start=nil
local function wf(p,d) local h=assert(io.open(p,'wb'));h:write(d);h:close() end
local h=assert(io.open(source,'rb'));local state=h:read('*a');h:close()
lid=emu.addMemoryCallback(function()
 if not loaded then loaded=true;emu.loadSavestate(state) end
end,emu.callbackType.exec,0,0xfffff)
local starts={
 [0x7CB227]=true,[0x7CB240]=true,[0x7CB266]=true,[0x7CB27B]=true,[0x7CB2B2]=true,
 [0x7CB2B7]=true,[0x7CB2C6]=true,[0x7CB2DE]=true,[0x7CB336]=true,[0x7CB353]=true,
 [0x7CB36F]=true,[0x7CB390]=true,[0x7CB3D0]=true,[0x7CB3ED]=true,[0x7CB409]=true,
 [0x7CB41B]=true,[0x7CB42A]=true,[0x7CB44E]=true,[0x7CB49F]=true,[0x7CB4BC]=true,
 [0x7CB507]=true,[0x7CDBE1]=true,
}
local function observe(a,v)
 if not loaded then return end
 local physical=a+0x700000
 reads[#reads+1]=string.format('%d\t%06X\t%X',f,physical,v)
 if starts[physical] and not captured[physical] then pending[f+150]=physical;hold=true;hold_start=hold_start or f end
end
emu.addMemoryCallback(observe,emu.callbackType.read,0x7CB227,0x7CB528,emu.cpuType.ws,emu.memType.wsPrgRom)
emu.addMemoryCallback(observe,emu.callbackType.read,0x7CDBE1,0x7CDBFF,emu.cpuType.ws,emu.memType.wsPrgRom)
local function dispatchHit(kind)
 if not loaded then return end
 local s=emu.getState();local p=0x7C0000+s['cpu.di']
 if (p>=0x7CB227 and p<0x7CB529)or(p>=0x7CDBE1 and p<0x7CDC00)then
  dispatch[#dispatch+1]=string.format('%d\t%s\t%04X\t%04X\t%06X',f,kind,s['cpu.es'],s['cpu.di'],p)
 end
end
emu.addMemoryCallback(function()dispatchHit('NATIVE')end,emu.callbackType.exec,0x5D57B)
emu.addMemoryCallback(function()dispatchHit('COMPACT')end,emu.callbackType.exec,0x5D583)
local inputs=os.getenv('QA_INPUT')and dofile(os.getenv('QA_INPUT'))or{
 {'b',180,184,999999,4},{'b',480,484,999999,4},
 {'a',720,5200,41,4},{'right',960,5200,347,4},
 {'down',1320,5200,503,4},{'left',1680,5200,719,4},
 {'up',2040,5200,887,4},{'b',2700,5200,613,4},
}
emu.addEventCallback(function()
 local t={a=false,b=false,start=false,up=false,down=false,left=false,right=false,up2=false,down2=false,left2=false,right2=false,sound=false}
 if not hold then for _,p in ipairs(inputs)do if f>=p[2]and f<p[3]and(f-p[2])%p[4]<p[5]then t[p[1]]=true end end end
 if hold_start and f>=hold_start+90 and f<hold_start+94 then t.a=true end
 emu.setInput(t,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function()
 if loaded and lid then local id=lid;lid=nil;emu.removeMemoryCallback(id)end
 f=f+1
 if pending[f]then local p=pending[f];captured[p]=true;wf(string.format('%s/stream_%06X_frame_%05d.png',out,p,f),emu.takeScreenshot())end
 if f==1 or f%120==0 or f==maxf then wf(string.format('%s/frame_%05d.png',out,f),emu.takeScreenshot())end
 if f==maxf then wf(out..'/END.mss',emu.createSavestate())end
 if f==maxf+2 then
  wf(out..'/reads.tsv','frame\trom\tvalue\n'..table.concat(reads,'\n')..'\n')
  wf(out..'/dispatch.tsv','frame\tpath\tes\tdi\trom\n'..table.concat(dispatch,'\n')..'\n')
  wf(out..'/result.json',string.format('{"result":"PASS_EXECUTION","frames":%d,"loaded":%s,"access_method":"SAVESTATE_REPLAY_WITH_SCRIPTED_INPUT","rom_writes":0,"affected_reads":%d,"dispatch_hits":%d}\n',f,tostring(loaded),#reads,#dispatch))
  emu.stop(loaded and 0 or 1)
 end
end,emu.eventType.endFrame)
