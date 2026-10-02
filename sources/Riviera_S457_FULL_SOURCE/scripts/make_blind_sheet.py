#!/usr/bin/env python3
"""Create a randomized, unlabeled glyph sheet for a fresh blind review."""
from pathlib import Path
from PIL import Image, ImageDraw
import argparse, hashlib, importlib.util, json, random, secrets
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_s457', ROOT/'scripts/build_s457.py')
build_s457 = importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(build_s457)
def pxat(x,y): return (y//8*12+x//8)*32+y%8*4+x%8//2
def main():
 ap=argparse.ArgumentParser();ap.add_argument('rom',type=Path);ap.add_argument('--runtime',type=Path,default=ROOT/'evidence/credits/S457');ap.add_argument('--sheet',type=Path,default=ROOT/'analysis/B4/GLYPH_BLIND_SHEET_NEW.png');ap.add_argument('--key',type=Path,default=ROOT/'analysis/B4/GLYPH_BLIND_KEY_NEW.json');a=ap.parse_args()
 rom=a.rom.read_bytes();release=json.loads((ROOT/'source/RELEASE.json').read_text());items=[]
 for block in release['blocks']+release['older_blocks']:
  if block['id'] not in build_s457.AFFECTED: continue
  page=block['page'];ram=(a.runtime/f'page_{page:02d}/runtime/page_{page:02d}.bin').read_bytes();data=ram[block['destination']:block['destination']+block['length']]
  for metric in block['metrics']:
   x,y=metric['x'],metric['y']
   for char in metric['text']:
    if char==' ': x+=3;continue
    pixels,_=build_s457.glyph(rom,char);width=len(pixels[0])
    if char=='I':
     actual=[[int(((data[pxat(x+xx,y+yy)]>>(4 if (x+xx)%2==0 else 0))&15)==6) for xx in range(width)] for yy in range(10)]
     assert actual==pixels;items.append((f'runtime_I_{page}','I',actual))
    x+=width+1
 for char in ['l','i','j','L','T','f','r']:
  pixels,_=build_s457.native_glyph(rom,char);items.append((f'native_{char}',char,pixels))
 assert len(items)==11
 seed=secrets.randbits(64);random.Random(seed).shuffle(items);image=Image.new('RGB',(len(items)*64,76),'#181818');draw=ImageDraw.Draw(image)
 for index,(_,_,pixels) in enumerate(items):
  glyph=Image.new('L',(len(pixels[0]),10));glyph.putdata([102 if value else 0 for row in pixels for value in row]);x=index*64+12;image.paste(glyph.resize((glyph.width*5,50),Image.Resampling.NEAREST),(x,16));draw.text((index*64+2,2),str(index+1),fill='white')
 a.sheet.parent.mkdir(parents=True,exist_ok=True);image.save(a.sheet);key={'seed':seed,'key':{str(i+1):{'source':src,'character':char} for i,(src,char,_) in enumerate(items)},'sheet_sha256':hashlib.sha256(a.sheet.read_bytes()).hexdigest()};a.key.write_text(json.dumps(key,indent=2)+'\n');print('BLIND_SHEET_OK',len(items))
if __name__=='__main__': main()
