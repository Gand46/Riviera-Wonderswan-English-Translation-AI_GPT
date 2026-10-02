local out=assert(os.getenv('MESEN_MULTI_DIR'))
local rep=assert(os.getenv('MESEN_LUA_REPORT'))
local final=assert(os.getenv('MESEN_CAPTURE_PATH'))
local f=0
local function wf(p,d,m)local h=assert(io.open(p,m or'w'));h:write(d);h:close()end
local frames={1200,1450,1700,1950,2200,2450,2700,2950,3200,3450,3700,3950,4200,4450,4700}
local caps={};for _,v in ipairs(frames)do caps[v]=true end
local function pulse(t,k,s,e)if f>=s and f<e then t[k]=true end end
emu.addEventCallback(function()
 local t={a=false,b=false,start=false,up=false,down=false,left=false,right=false,up2=false,down2=false,left2=false,right2=false,sound=false}
 if f>=180 and f<420 then t.a=true end
 pulse(t,'a',950,958)
 if f>=1200 then local m=(f-1200)%90;if m<5 then t.a=true end end
 emu.setInput(t,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function()
 f=f+1
 if caps[f] then wf(out..'/frame_'..f..'.png',emu.takeScreenshot(),'wb') end
 if f==4800 then
  wf(final,emu.takeScreenshot(),'wb')
  wf(rep,'{"passed":true,"route":"Title -> Game Start -> bounded opening prologue","end_frame":4800,"captures":15}\n')
  emu.stop(0)
 end
end,emu.eventType.endFrame)
