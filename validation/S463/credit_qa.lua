local out=assert(os.getenv('QA_OUT'))
local resume=assert(os.getenv('QA_STATE'))
local f=0
local function w(p,d) local h=assert(io.open(out..'/'..p,'wb'));h:write(d);h:close() end
local loadcb
loadcb=emu.addMemoryCallback(function()
  local h=assert(io.open(resume,'rb')); local d=h:read('*a'); h:close()
  emu.loadSavestate(d)
  emu.removeMemoryCallback(loadcb,emu.callbackType.exec,0,0xfffff)
end,emu.callbackType.exec,0,0xfffff)
emu.addEventCallback(function()
  local i={}; if f>=5 and f%8==0 then i.a=true end
  emu.setInput(i,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function()
  f=f+1
  if f%60==0 then
    w(string.format('credit_%02d_f%04d.png',emu.read(0x1612,emu.memType.wsWorkRam),f),emu.takeScreenshot())
  end
  if f==3300 then
    local savecb
    savecb=emu.addMemoryCallback(function()
      w('page09_stable.mss',emu.createSavestate())
      local raw={}
      for a=0x5b60,0x6d5f do raw[#raw+1]=string.char(emu.read(a,emu.memType.wsWorkRam)) end
      w('page09_native_pixels.bin',table.concat(raw))
      emu.removeMemoryCallback(savecb,emu.callbackType.exec,0,0xfffff)
    end,emu.callbackType.exec,0,0xfffff)
  end
  if f==6000 then
    w('RESULT.json','{"frames":6000,"access_method":"SAVESTATE","checkpoint_origin":"S460 synthetic ending","rom_writes":0,"input":"A every 8 frames"}')
    emu.stop(0)
  end
end,emu.eventType.endFrame)
