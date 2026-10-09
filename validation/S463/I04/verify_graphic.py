#!/usr/bin/env python3
"""Verify exact resource, native DMA output and full PPU reconstruction; no ROM edits."""
import argparse,csv,hashlib,json
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--evidence',type=Path,default=Path(__file__).resolve().parent);a=p.parse_args();r=a.rom.read_bytes();out=a.evidence
start,end=0x6cacbe,0x6caebe;raw=r[start:end];copied=(out/'native_pixels.bin').read_bytes();screen=Image.open(out/'screen.png').convert('RGB');pal=[int.from_bytes(r[end+i*2:end+i*2+2],'little') for i in range(16)];expected=Image.new('RGB',(32,32));rows=[];pxbad=[]
for i,v in enumerate(raw):
 tile=i//32;y=(tile//4)*8+(i%32)//4;x=(tile%4)*8+(i%4)*2
 for xx,n in ((x,v>>4),(x+1,v&15)):
  c=pal[n];rgb=((c>>8&15)*16,(c>>4&15)*16,(c&15)*16);expected.putpixel((xx,y),rgb)
  if screen.getpixel((96+xx,56+y))!=rgb:pxbad.append([xx,y])
 rows.append({'rom_offset':f'0x{start+i:06X}','dma_wram_offset':f'0x{0x4000+i:04X}','tile':tile,'pixel_x':x,'pixel_y':y,'source':f'{v:02X}','destination':f'{copied[i]:02X}','equal':v==copied[i]})
with (out/'byte_pixel_mapping.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
expected.save(out/'complete_resource_32x32.png');screen.crop((96,56,128,88)).resize((256,256),Image.Resampling.NEAREST).save(out/'runtime_crop8x.png')
cases=[]
for ident,lo,hi in [('CP932-15939',0x6cae90,0x6cae99),('CP932-15968',0x6cad76,0x6cad81)]:
 rr=rows[lo-start:hi-start];cases.append({'id':ident,'start':hex(lo),'end_exclusive':hex(hi),'bytes':hi-lo,'pixels':2*(hi-lo),'raw_cp932':r[lo:hi].decode('cp932'),'dma_exact_bytes':sum(x['equal'] for x in rr),'pixel_mapping':rr,'classification':'CONFIRMED_GRAPHIC_NON_TEXT','structural':'PASS','native_consumer_synthetic':'PASS','runtime_ppu':'PASS','natural_reachability':'NOT_VALIDATED','unused_proven':False})
rep={'gate':'I04-6C-TECH','result':'PASS','scope':'Classification of the two CP932 candidates as non-text pixel data, using documented synthetic native consumer execution','rom_sha256':hashlib.sha256(r).hexdigest(),'resource':{'start':hex(start),'end_exclusive':hex(end),'length':512,'sha256':hashlib.sha256(raw).hexdigest(),'format':'16 tiles arranged 4x4; 8x8 pixels per tile; packed 4bpp, high nibble first','size_pixels':[32,32],'palette_range':[hex(end),hex(end+32)],'native_destination':'0x4000..0x4200','native_descriptor_hex':(out/'native_descriptor.bin').read_bytes().hex()},'validation':{'dma_bytes_equal':sum(x['equal'] for x in rows),'dma_bytes_total':512,'ppu_pixels_equal':1024-len(pxbad),'ppu_pixels_total':1024,'runtime_stage':json.loads((out/'RESULT.json').read_text())['stage'],'source_mapping':json.loads((out/'source_mapping.json').read_text()),'callback_reads':0,'callback_limitation':'Mesen GDMA did not emit wsPrgRom read callbacks; consumption is proven by pre-DMA hardware registers, active source mapping and exact destination equality, not callback counts'},'cases':cases,'visual_observation':'Complete pixel-art building/tower with roof, openings and side structures; neither candidate is a string or lettering.','access_method':'SYNTHETIC_NATIVE_DESCRIPTOR_DMA_PPU','synthetic_controls':['BP=0xACBE, SI=0x1000, destination field=0x4000','Selected banks C0=0x0F, C2=0x72, C3=0x6C','Native descriptor construction at 5000:4A54..4A74 and native dispatcher 2000:37AF through GDMA 2000:3878','Synthetic BG1 tile map, packed4bpp mode and palette loaded from adjacent ROM palette; transferred pixel bytes never rewritten'],'natural_reachability':False,'natural_scene_identified':False,'unused_proven':False,'rom_modified':False,'translation_required':'N/A: graphic pixels, not Japanese text','historical_status':'UNRESOLVED_TECHNICAL_NOT_CONFIRMED_TEXT / S461 NOT_VALIDATED','new_status':'CONFIRMED_GRAPHIC_NON_TEXT / synthetic classification PASS','unchanged_scope':'No renewed validation of the eight already closed sibling icons; no release-wide approval inferred'}
assert copied==raw and not pxbad
(out/'I04_GRAPHIC_CLOSEOUT.json').write_text(json.dumps(rep,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'dma':f"{rep['validation']['dma_bytes_equal']}/512",'ppu':f"{rep['validation']['ppu_pixels_equal']}/1024",'classification':rep['result']}))
