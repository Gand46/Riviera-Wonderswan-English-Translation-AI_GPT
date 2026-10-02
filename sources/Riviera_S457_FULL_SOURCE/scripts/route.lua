local out=assert(os.getenv('QA_OUT'))
local source=assert(os.getenv('QA_STATE'))
local maxf=tonumber(os.getenv('QA_FRAMES') or '300')
local inputs=dofile(assert(os.getenv('QA_INPUT')))
local ranges=dofile(assert(os.getenv('QA_RANGES')))
local f=0;local loaded=false;local saved=false;local lid
local function wf(p,d) local h=assert(io.open(p,'wb'));h:write(d);h:close() end
local h=assert(io.open(source,'rb'));local state=h:read('*a');h:close()
lid=emu.addMemoryCallback(function()
 if not loaded then loaded=true;emu.loadSavestate(state) end
end,emu.callbackType.exec,0,0xfffff)
if os.getenv('QA_EXT') then dofile(os.getenv('QA_EXT'))({out=out,write=wf,frame=function()return f end,isLoaded=function()return loaded end}) end
local hits={};local resources={};local control=false;local cid
cid=emu.addMemoryCallback(function(a,v)
 if loaded then control=true;emu.removeMemoryCallback(cid) end
end,emu.callbackType.read,0,0x7fffff,emu.cpuType.ws,emu.memType.wsPrgRom)
for _,r in ipairs(ranges) do
 hits[r[1]]={count=0,first=-1,pc=''}
 emu.addMemoryCallback(function(a,v)
  if not loaded then return end
  local k=hits[r[1]];k.count=k.count+1
  if k.first<0 then local s=emu.getState();k.first=f;k.pc=string.format('%04X:%04X',s['cpu.cs'],s['cpu.ip']) end
 end,emu.callbackType.read,r[2],r[3]-1,emu.cpuType.ws,emu.memType.wsPrgRom)
end
emu.addMemoryCallback(function()
 if loaded then
  local s=emu.getState();resources[#resources+1]=string.format('%d,%04X',f,s['cpu.bx'])
  if s['cpu.bx']==0x15 or s['cpu.bx']==0x14 then
   local q={};for k,v in pairs(s) do if k:find('cpu') or k:find('Bank') then q[#q+1]=k..'='..tostring(v) end end
   local sp=s['cpu.sp'];for a=sp,sp+16 do q[#q+1]=string.format('stack_%04X=%02X',a,emu.read(a,emu.memType.wsWorkRam)) end
   wf(out..'/loader_state.txt',table.concat(q,'\n'));wf(out..'/PRE_HEADER.mss',emu.createSavestate())
  end
 end
end,emu.callbackType.exec,0x21b03)
emu.addEventCallback(function()
 local t={a=false,b=false,start=false,up=false,down=false,left=false,right=false,up2=false,down2=false,left2=false,right2=false,sound=false}
 for _,p in ipairs(inputs) do if f>=p[2] and f<p[3] and (f-p[2])%(p[4] or 999999)<(p[5] or 6) then t[p[1]]=true end end
 if QA_HOLD then for k,v in pairs(t)do t[k]=false end end
 emu.setInput(t,0)
end,emu.eventType.inputPolled)
local function flush()
 local lines={'candidate_id,read_count,first_frame,first_pc'}
 for _,r in ipairs(ranges)do local k=hits[r[1]];lines[#lines+1]=string.format('%s,%d,%d,%s',r[1],k.count,k.first,k.pc) end
 wf(out..'/residual_hits.csv',table.concat(lines,'\n')..'\n')
 wf(out..'/resources.csv','frame,resource_id\n'..table.concat(resources,'\n')..'\n')
end
emu.addEventCallback(function()
 if loaded and lid then local old=lid;lid=nil;emu.removeMemoryCallback(old) end
 f=f+1
 if f==1 or f%120==0 or f==maxf then wf(string.format('%s/frame_%05d.png',out,f),emu.takeScreenshot()) end
 if f%600==0 then flush() end
 if f==maxf then
  local saver;saver=emu.addMemoryCallback(function()
   if not saved then saved=true;wf(out..'/END.mss',emu.createSavestate());emu.removeMemoryCallback(saver) end
  end,emu.callbackType.exec,0,0xfffff)
 end
 if f==maxf+2 then
  flush();wf(out..'/report.json',string.format('{"frames":%d,"saved":%s,"positive_read_control":%s,"rom_mutated":false,"access":"%s"}\n',f,tostring(saved),tostring(control),os.getenv('QA_ACCESS') or 'checkpoint_and_scripted_input'))
  emu.stop(saved and 0 or 1)
 end
end,emu.eventType.endFrame)
