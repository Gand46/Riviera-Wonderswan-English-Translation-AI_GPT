local out=assert(os.getenv('PROBE_OUT'));local f=0;local started=false;local stage=0;local readhits={};local execs={}
local function w(p,d)local h=assert(io.open(out..'/'..p,'wb'));h:write(d);h:close()end
local function wb(a,v)emu.write(a,v,emu.memType.wsWorkRam)end
local function ww(a,v)wb(a,v%256);wb(a+1,math.floor(v/256))end
local function dump(a,n)local t={};for x=a,a+n-1 do t[#t+1]=string.char(emu.read(x,emu.memType.wsWorkRam))end;return table.concat(t)end
local function jump(cs,ip)local s=emu.getState();s['cpu.cs']=cs;s['cpu.ip']=ip;s['cpu.prefetch.size']=0;s['cpu.prefetch.readPos']=0;s['cpu.prefetch.writePos']=0;s['cpu.prefetch.fetchIp']=ip;s['cpu.prefetch.fetchCs']=cs;emu.setState(s)end
emu.addMemoryCallback(function(a,v)if started then readhits[a]=(readhits[a] or 0)+1 end end,emu.callbackType.read,0x6cacbe,0x6caebd,emu.cpuType.ws,emu.memType.wsPrgRom)
emu.addMemoryCallback(function()if started then local t={};for k,v in pairs(emu.getState())do if k:lower():find('dma') or k:lower():find('bank')then t[#t+1]=k..'='..tostring(v)end end;table.sort(t);w('dma_state.txt',table.concat(t,'\n'));local a=emu.convertAddress(0x3acbe,emu.memType.wsMemory,emu.cpuType.ws);local b=emu.convertAddress(0x3aebd,emu.memType.wsMemory,emu.cpuType.ws);w('source_mapping.json',string.format('{"cpu_start":%d,"cpu_end_inclusive":%d,"rom_start":%d,"rom_end_inclusive":%d}',0x3acbe,0x3aebd,a.address,b.address))end end,emu.callbackType.exec,0x23878)
for _,a in ipairs({0x54a54,0x2377f,0x237af,0x2384a,0x23878})do emu.addMemoryCallback(function()if started then execs[#execs+1]=string.format('%05X',a)end end,emu.callbackType.exec,a)end
emu.addMemoryCallback(function()if started and stage==1 then stage=2;w('native_descriptor.bin',dump(0xcb62,14));jump(0x2000,0x37af)end end,emu.callbackType.exec,0x54a74)
emu.addMemoryCallback(function()if started and stage==2 then stage=3;w('native_pixels.bin',dump(0x4000,512));w('executed_pcs.txt',table.concat(execs,'\n'));local h={'rom_offset,read_events'};for a=0x6cacbe,0x6caebd do h[#h+1]=string.format('%06X,%d',a,readhits[a] or 0)end;w('resource_reads.csv',table.concat(h,'\n'))
for a=0,2047,2 do ww(a,16)end
for y=0,3 do for x=0,3 do ww(((7+y)*32+12+x)*2,y*4+x)end end
for a=0x4200,0x421f do wb(a,0)end
for a=0,31 do wb(0xfe00+a,emu.read(0x6caebe+a,emu.memType.wsPrgRom))end
jump(0,0x2100)
end end,emu.callbackType.exec,0x237d4)
emu.addEventCallback(function()f=f+1
if f==100 then local cb;cb=emu.addMemoryCallback(function()emu.removeMemoryCallback(cb,emu.callbackType.exec,0,0xfffff);started=true;stage=1
for a=0xcb62,0xcc41 do wb(a,0)end
for i,v in ipairs({250,176,15,230,192,176,114,230,194,176,108,230,195,234,84,74,0,80})do wb(0x2000+i-1,v)end
for i,v in ipairs({250,176,224,230,96,176,0,230,7,230,16,230,17,176,1,230,20,184,1,0,231,0,235,254})do wb(0x2100+i-1,v)end
ww(0x1024,0x4000);ww(0x16f2,0);local s=emu.getState();s['cpu.ds']=0;s['cpu.es']=0;s['cpu.ss']=0;s['cpu.sp']=0x3000;s['cpu.si']=0x1000;s['cpu.bx']=0;s['cpu.bp']=0xacbe;emu.setState(s);jump(0,0x2000)
end,emu.callbackType.exec,0,0xfffff)end
if f==104 then w('screen.png',emu.takeScreenshot());w('RESULT.json',string.format('{"frames":%d,"stage":%d,"access_method":"SYNTHETIC_NATIVE_DESCRIPTOR_DMA_PPU","natural_reachability":false,"rom_writes":0}',f,stage));emu.stop(stage==3 and 0 or 1)end
end,emu.eventType.endFrame)
