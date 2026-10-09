local captureHoldUntil=0
local out=assert(os.getenv('I23_OUT'));local route=tonumber(os.getenv('I23_ROUTE') or '0');local f=0;local n=0;local injected=false;local log=assert(io.open(out..'/trace.tsv','w'));local boundary=nil;local pages=0;local creditframe=nil;local done=false
local function w(p,d)local h=assert(io.open(out..'/'..p,'wb'));h:write(d);h:close()end
local function state(p)local cb;cb=emu.addMemoryCallback(function()w(p..'.mss',emu.createSavestate());emu.removeMemoryCallback(cb,emu.callbackType.exec,0,0xfffff)end,emu.callbackType.exec,0,0xfffff)end
local function note(k,x)local s=emu.getState();log:write(string.format('%d\t%s\t%s\t%04X:%04X\tSI=%04X\tDI=%04X\tES=%04X\n',f,k,x,s['cpu.cs'],s['cpu.ip'],s['cpu.si'],s['cpu.di'],s['cpu.es']));log:flush()end
local resume=os.getenv('I23_RESUME')
if resume then local cb;cb=emu.addMemoryCallback(function()local h=assert(io.open(resume,'rb'));local d=h:read('*a');h:close();emu.loadSavestate(d);injected=true;emu.removeMemoryCallback(cb,emu.callbackType.exec,0,0xfffff)end,emu.callbackType.exec,0,0xfffff)end
emu.addMemoryCallback(function()
 if injected then return end
 local s=emu.getState();if s['cpu.cs']~=0x6000 then return end
 injected=true;note('ENTER','native ending 013F route '..route)
 emu.write(0x6a0,route,emu.memType.wsWorkRam);for a=0x66e,0x673 do emu.write(a,60,emu.memType.wsWorkRam)end
 s['cpu.ip']=0x13f;s['cpu.prefetch.size']=0;s['cpu.prefetch.readPos']=0;s['cpu.prefetch.writePos']=0;s['cpu.prefetch.fetchIp']=0x13f;s['cpu.prefetch.fetchCs']=0x6000;emu.setState(s);state('injected_anchor')
end,emu.callbackType.exec,0x600b1)
emu.addMemoryCallback(function()
 if injected and os.getenv('I23_LATE')=='1' then emu.write(0xc020,0x40,emu.memType.wsWorkRam) end
end,emu.callbackType.exec,0x60174)

emu.addMemoryCallback(function()
 if not injected or n>3000 then return end;local s=emu.getState();if s['cpu.es']~=0x9300 then return end
 n=n+1;note('VM',string.format('%04X %02X route=%d step=%d',s['cpu.di'],emu.read(0x93000+s['cpu.di'],emu.memType.wsMemory),emu.read(0x6a0,emu.memType.wsWorkRam),emu.read(0x160c,emu.memType.wsWorkRam)))
end,emu.callbackType.exec,0x61300)
emu.addMemoryCallback(function(a,v)
 if not injected then return end;local p=emu.convertAddress(a,emu.memType.wsMemory,emu.cpuType.ws);if p and p.address>=0x660000 and p.address<0x670000 and ((v&255)==254 or (v&255)==255) then boundary={f=f,a=p.address,v=v&255};note('TEXT_BOUNDARY',string.format('%06X %02X',p.address,v&255))end
end,emu.callbackType.read,0x660000,0x66ffff,emu.cpuType.ws,emu.memType.wsPrgRom)
emu.addMemoryCallback(function()if injected then note('CREDITS','page='..emu.read(0x1612,emu.memType.wsWorkRam));creditframe=f+120;end end,emu.callbackType.exec,0x610c2)
emu.addMemoryCallback(function()if injected then note('SEQUENCE_RETURN','native return 0177');w('sequence_return.png',emu.takeScreenshot());w('complete.mss',emu.createSavestate());w('complete.txt','native ending event sequencer returned');done=true end end,emu.callbackType.exec,0x60177)
emu.addEventCallback(function()local i={};if f>=5 and f>=captureHoldUntil and f%8==0 then i.a=true end;if not injected and f%180==40 then i.start=true end;emu.setInput(i,0)end,emu.eventType.inputPolled)
emu.addEventCallback(function()
 f=f+1
 if done then log:close();emu.stop(0);return end
 if creditframe and f>=creditframe then w(string.format('credit_%02d.png',emu.read(0x1612,emu.memType.wsWorkRam)),emu.takeScreenshot());creditframe=nil end
 if boundary and f>=boundary.f+4 then pages=pages+1;w(string.format('text_%03d_%06X.png',pages,boundary.a),emu.takeScreenshot());boundary=nil end
 if injected and f%2000==0 then state(string.format('checkpoint_%05d',f)) end
 if injected and f%600==0 then w(string.format('frame_%05d.png',f),emu.takeScreenshot())end
 if f==7200 then w('final.png',emu.takeScreenshot());note('STOP','chunk');local cb;cb=emu.addMemoryCallback(function()emu.removeMemoryCallback(cb,emu.callbackType.exec,0,0xfffff);w('resume.mss',emu.createSavestate());done=true end,emu.callbackType.exec,0,0xfffff)end
end,emu.eventType.endFrame)

local currentOwner=nil;local captured={};local binding={};local pendingShot=nil
local bf=assert(io.open(out..'/owner_stream_binding.tsv','w'));bf:write('frame\towner_rom\tstream_rom\tconsumer_cs_ip\n')
local tf=assert(io.open(out..'/dialogue_reads.tsv','w'));tf:write('frame\towner_rom\trom\tvalue\n')
emu.addMemoryCallback(function()
 local st=emu.getState();if st['cpu.cs']~=0x6000 then return end
 local p=emu.convertAddress(st['cpu.es']*16+st['cpu.di'],emu.memType.wsMemory,emu.cpuType.ws)
 if p and p.memType==emu.memType.wsPrgRom then currentOwner=p.address end
end,emu.callbackType.exec,0x61A16)
emu.addMemoryCallback(function(a,v)
 local st=emu.getState();if not currentOwner or st['cpu.cs']~=0x5000 or st['cpu.ip']~=0x20D4 then return end
 local p=emu.convertAddress(a,emu.memType.wsMemory,emu.cpuType.ws)
 if not p or p.memType~=emu.memType.wsPrgRom then return end
 if not binding[currentOwner] then binding[currentOwner]=p.address;bf:write(string.format('%d\t%06X\t%06X\t5000:20D1(read)/20D4(callback)\n',f,currentOwner,p.address));bf:flush()end
 tf:write(string.format('%d\t%06X\t%06X\t%04X\n',f,currentOwner,p.address,v));tf:flush()
 if (v&255)==255 and not captured[currentOwner] then captureHoldUntil=f+8;pendingShot={frame=f+6,owner=currentOwner};captured[currentOwner]=true end
end,emu.callbackType.read,0x7C0000,0x7CFFFF,emu.cpuType.ws,emu.memType.wsPrgRom)
emu.addEventCallback(function()
 if pendingShot and f>=pendingShot.frame then w(string.format('owner_%06X.png',pendingShot.owner),emu.takeScreenshot());pendingShot=nil end
end,emu.eventType.endFrame)

local ds=assert(io.open(out..'/dispatch.tsv','w'));ds:write('frame\tpath\tes\tdi\n')
local function dpath(k)local s=emu.getState();if s['cpu.es']==0xC000 and s['cpu.di']>=0xED22 then ds:write(string.format('%d\t%s\t%04X\t%04X\n',f,k,s['cpu.es'],s['cpu.di']));ds:flush()end end
emu.addMemoryCallback(function()dpath('NATIVE')end,emu.callbackType.exec,0x5D57B)
emu.addMemoryCallback(function()dpath('COMPACT')end,emu.callbackType.exec,0x5D583)
