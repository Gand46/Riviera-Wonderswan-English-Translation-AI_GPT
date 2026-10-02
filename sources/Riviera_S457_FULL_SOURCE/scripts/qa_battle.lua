local out=assert(os.getenv('MESEN_MULTI_DIR'));local rep=assert(os.getenv('MESEN_LUA_REPORT'));local st=assert(os.getenv('MESEN_STATE_PATH'));local f=0;local loaded=false
local function wf(p,d,m)local h=assert(io.open(p,m or'w'));h:write(d);h:close()end
local h=assert(io.open(st,'rb'));local state=h:read('*a');h:close();local id;id=emu.addMemoryCallback(function()if not loaded then loaded=true;emu.loadSavestate(state)end end,emu.callbackType.exec,0,0xFFFFF)
local function pulse(t,k,period,width,offset)local m=(f-offset)%period;if f>=offset and m>=0 and m<width then t[k]=true end end
emu.addEventCallback(function()
 local t={a=false,b=false,start=false,up=false,down=false,left=false,right=false,up2=false,down2=false,left2=false,right2=false,sound=false}
 -- default action cadence; occasionally press right/down to escape cursor stalls
 if f>=20 then pulse(t,'a',22,5,20) end
 if f>=400 then pulse(t,'right',220,4,400) end
 if f>=700 then pulse(t,'down',310,4,700) end
 emu.setInput(t,0)
end,emu.eventType.inputPolled)
local traces={};local swaps={};local owners={}
local function word(a)return emu.read(a,emu.memType.wsWorkRam)+256*emu.read(a+1,emu.memType.wsWorkRam)end
emu.addMemoryCallback(function()
 if loaded then local s=emu.getState();local sp=s['cpu.sp'];traces[#traces+1]=string.format('%d,%d,%d,%d,%d,%d,%d',f,s['cpu.bx'],s['cpu.ax'],word(0x1584),word(0x1586),word(sp),word(sp+2)) end
end,emu.callbackType.exec,0x24CFA)
emu.addMemoryCallback(function()
 if loaded then local s=emu.getState();local sp=s['cpu.sp'];local old=s['cpu.di'];local d=word(0x1584)
 if d==0x57A0 and f>=0 then swaps[#swaps+1]=string.format('%d,%d,%d',f,old,d)end
 owners[#owners+1]=string.format('%d,%d,%d,%d,%d,%d,%d,%d',f,old,s['cpu.cx'],s['cpu.ax'],d,word(0x1586),word(sp),word(sp+2))end
end,emu.callbackType.exec,0x2D150)
local savedTarget=false;local savedAction=false
emu.addMemoryCallback(function()if f>8000 and not savedTarget then savedTarget=true;wf(out..'/TARGET_PRE_DRAW.mss',emu.createSavestate(),'wb')end end,emu.callbackType.exec,0x29427)
emu.addMemoryCallback(function()if not savedAction then savedAction=true;wf(out..'/ACTION_PRE_DRAW.mss',emu.createSavestate(),'wb')end end,emu.callbackType.exec,0x45aad)
local caps={};for x=30,2500,30 do caps[x]=true end
emu.addEventCallback(function()f=f+1;if f%250==0 then local h=assert(io.open(out..'/wram_'..f..'.bin','wb'));for a=0,65535 do h:write(string.char(emu.read(a,emu.memType.wsWorkRam)))end;h:close()end;if caps[f]then wf(string.format('%s/frame_%04d.png',out,f),emu.takeScreenshot(),'wb')end;if f==2500 then wf(out..'/swaps.csv','frame,original_di,dest1\n'..table.concat(swaps,'\n'));wf(out..'/owners.csv','frame,di,cx,ax,dest1,dest2,return_ip,return_cs\n'..table.concat(owners,'\n'));  wf(out..'/glyph_trace.csv','frame,glyph,ax,dest1,dest2,return_ip,return_cs\n'..table.concat(traces,'\n')); wf(rep,'{"capture_complete":true,"frames":2500}\n');emu.stop(0)end end,emu.eventType.endFrame)

local sharedCalls={}
local function sharedWord(a)return emu.read(a,emu.memType.wsWorkRam)+256*emu.read(a+1,emu.memType.wsWorkRam)end
emu.addMemoryCallback(function()
 local s=emu.getState();local sp=s['cpu.sp'];local key=string.format('%04X:%04X,%04X',sharedWord(sp+2),sharedWord(sp)-5,s['cpu.di']);sharedCalls[key]=(sharedCalls[key]or 0)+1
end,emu.callbackType.exec,0x255f9)
emu.addEventCallback(function()
 if f%60~=0 then return end
 local root=os.getenv('MESEN_MULTI_DIR');if root then local h=io.open(root..'/shared_consumers.csv','w');if h then h:write('caller,pointer,calls\n');for k,v in pairs(sharedCalls)do h:write(k..','..v..'\n')end;h:close()end end
end,emu.eventType.endFrame)

local writers={};local resources={}
emu.addMemoryCallback(function(a,v)
 local s=emu.getState();local pc=(s['cpu.cs']*16+s['cpu.ip'])%0x100000;local k=string.format('%04X,%05X',math.floor(a/32)*32,pc);writers[k]=(writers[k]or 0)+1
end,emu.callbackType.write,0x5a60,0x5a7f,emu.cpuType.ws,emu.memType.wsWorkRam)
for _,p in ipairs({0x21b01,0x2254e,0x21777,0x2277d})do emu.addMemoryCallback(function()
 local s=emu.getState();local sp=s['cpu.sp'];resources[#resources+1]=string.format('%d,%05X,%04X,%04X,%04X,%04X,%04X,%04X:%04X',f,p,s['cpu.di'],s['cpu.si'],s['cpu.cx'],s['cpu.bx'],s['cpu.ds'],word(sp+2),word(sp))
end,emu.callbackType.exec,p)end
emu.addEventCallback(function()
 if f%60==0 then local a={};for k,v in pairs(writers)do a[#a+1]=k..','..v end;wf(out..'/writers.csv','tile,pc,count\n'..table.concat(a,'\n'));wf(out..'/resources.csv','frame,call,di,si,cx,bx,ds,return\n'..table.concat(resources,'\n'))end
end,emu.eventType.endFrame)

local level=tonumber(os.getenv('RAGE_LEVEL')or'-1');if level>=0 then emu.addMemoryCallback(function()local s=emu.getState();s['cpu.ax']=math.floor(s['cpu.ax']/256)*256+level;emu.setState(s)end,emu.callbackType.exec,0x45994)end

emu.addEventCallback(function()if loaded and id then local old=id;id=nil;emu.removeMemoryCallback(old)end end,emu.eventType.endFrame)
