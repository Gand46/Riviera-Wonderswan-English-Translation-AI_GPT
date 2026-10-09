local root=assert(os.getenv('I04_ROOT'));local out=root..'/runtime'
local spec=dofile(root..'/inputs/native_probe_cases.lua');local h=assert(io.open(root..'/inputs/native_probe.bin','rb'));local code=h:read('*a');h:close()
local ranges=dofile(root..'/inputs/hook_ranges.lua')
local f=0;local started=false;local rows={};local hits={};local widths={};local active=false;local stream=0
local function word(a)return emu.read(a,emu.memType.wsWorkRam)+256*emu.read(a+1,emu.memType.wsWorkRam)end
emu.addMemoryCallback(function()if started then active=true;stream=emu.getState()['cpu.di'] end end,emu.callbackType.exec,0x255f9)
emu.addMemoryCallback(function()if started and active then
 local s=emu.getState();local x=math.floor((word(0x1584)-word(0x2ae))/32)*8+(word(0x2aa)%256);local glyph=s['cpu.bx'];local step=(glyph>=0xaa and glyph<0xfe) and 8 or 10
 widths[#widths+1]=string.format('%04X,%04X,%d,%d,%d',stream,s['cpu.bx'],x,step,word(0x2b0)/4)
end end,emu.callbackType.exec,0x24cfa)
emu.addMemoryCallback(function()if started then active=false end end,emu.callbackType.exec,0x610c2)
local function wf(p,v)local h=assert(io.open(p,'wb'));h:write(v);h:close()end
local hookActive=false;local hookBefore=nil;local hookWrites={};local hookBad={};local hookPage=-1
emu.addMemoryCallback(function()
 if started then hookBefore=emu.getState();hookPage=emu.read(0x1612,emu.memType.wsWorkRam);hookActive=true end
end,emu.callbackType.exec,0x61124)
emu.addMemoryCallback(function(address,value)
 if hookActive then
  local allowed=address>=hookBefore['cpu.sp']-20 and address<hookBefore['cpu.sp']
  if hookPage==13 then
   for _,a in ipairs({0x7200,0x7500,0x7800,0x6160,0x68e0}) do if address>=a and address<a+768 then allowed=true end end
  end
  for _,r in ipairs(ranges)do if hookPage==r.page and address>=r.address and address<r.address+r.length then allowed=true end end
  hookWrites[address]=(hookWrites[address] or 0)+1
  if not allowed then hookBad[#hookBad+1]=string.format('%04X',address) end
 end
end,emu.callbackType.write,0,0xffff)
emu.addMemoryCallback(function()
 if started and hookActive then
  hookActive=false;local s=emu.getState();local bad={}
  for _,k in ipairs({'cx','si','bx','dx','bp','ss','sp','ds'})do if s['cpu.'..k]~=hookBefore['cpu.'..k]then bad[#bad+1]=k end end
  if s['cpu.ax']~=0 or s['cpu.es']~=0 or s['cpu.di']~=0xd6a3 then bad[#bad+1]='displaced_instructions' end
  local stack=0;local pixels=0;local unique=0
  for a,n in pairs(hookWrites)do unique=unique+1;if a>=hookBefore['cpu.sp']-20 and a<hookBefore['cpu.sp']then stack=stack+n else pixels=pixels+n end end
  wf(out..'/hook_guard.json',string.format('{"page_counter":%d,"register_errors":%d,"unexpected_writes":%d,"stack_write_events":%d,"pixel_write_events":%d,"unique_written_addresses":%d}\n',hookPage,#bad,#hookBad,stack,pixels,unique))
  if #bad>0 or #hookBad>0 then wf(out..'/hook_errors.txt',table.concat(bad,',')..'\n'..table.concat(hookBad,','));emu.stop(1)end
 end
end,emu.callbackType.exec,0x6112b)
for _,c in ipairs(spec.cases) do
 emu.addMemoryCallback(function()
  if started and not hits[c.name] then
   hits[c.name]=true;local bytes={};for a=c.address,c.address+c.length-1 do bytes[#bytes+1]=string.char(emu.read(a,emu.memType.wsWorkRam))end
   wf(out..'/'..c.name..'.bin',table.concat(bytes))
   local s=emu.getState();rows[#rows+1]=string.format('%s,%04X,%04X,%04X,%04X,%04X',c.name,s['cpu.cx'],s['cpu.si'],s['cpu.di'],s['cpu.ds'],s['cpu.es'])
  end
 end,emu.callbackType.exec,c.pc)
end
emu.addMemoryCallback(function()
 if started then
  wf(out..'/glyph_widths.csv','stream,glyph,x,advance,width\n'..table.concat(widths,'\n')..'\n')
  wf(out..'/native_probe_registers.csv','case,cx,si,di,ds,es\n'..table.concat(rows,'\n')..'\n')
  wf(out..'/native_probe_result.json',string.format('{"cases_executed":%d,"expected":%d,"access":"controlled WRAM harness calling ROM routines with S455 RLE scoped credit hooks","natural_progression":false}\n',#rows,#spec.cases))
  emu.stop(#rows==#spec.cases and 0 or 1)
 end
end,emu.callbackType.exec,spec.finish)
emu.addEventCallback(function()
 f=f+1
 if f==1000 then
  emu.addMemoryCallback(function()
   if not started then
    started=true
    for i=1,#code do emu.write(0x2000+i-1,string.byte(code,i),emu.memType.wsWorkRam)end
    local s=emu.getState();s['cpu.cs']=0;s['cpu.ip']=0x2000
    s['cpu.prefetch.size']=0;s['cpu.prefetch.readPos']=0;s['cpu.prefetch.writePos']=0;s['cpu.prefetch.fetchIp']=0x2000;s['cpu.prefetch.fetchCs']=0
    emu.setState(s)
   end
  end,emu.callbackType.exec,0,0xfffff)
 end
 if f==1100 then wf(out..'/native_probe_timeout.json','{"timeout":true}\n');emu.stop(1)end
end,emu.eventType.endFrame)
