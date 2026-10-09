local out=assert(os.getenv('ASTRA_OUT'));local resume=assert(os.getenv('ASTRA_RESUME'));local f=0;local loaded=false
local function w(p,d)local h=assert(io.open(out..'/'..p,'wb'));h:write(d);h:close()end
local cb;cb=emu.addMemoryCallback(function()local h=assert(io.open(resume,'rb'));local d=h:read('*a');h:close();emu.loadSavestate(d);loaded=true;emu.removeMemoryCallback(cb,emu.callbackType.exec,0,0xfffff)end,emu.callbackType.exec,0,0xfffff)
emu.addEventCallback(function()local i={};if f>=5 and f%8==0 then i.a=true end;emu.setInput(i,0)end,emu.eventType.inputPolled)
emu.addEventCallback(function()f=f+1;if loaded and f%60==0 then w(string.format('credit_%02d_f%04d.png',emu.read(0x1612,emu.memType.wsWorkRam),f),emu.takeScreenshot())end;if f>=4500 then w('done.txt','S459 savestate replay; screenshots only; input A every 8 frames');emu.stop(0)end end,emu.eventType.endFrame)
