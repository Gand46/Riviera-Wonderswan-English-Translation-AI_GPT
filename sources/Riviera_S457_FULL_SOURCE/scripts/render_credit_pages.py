"""Diagnostic field composition from native RAM, not a natural-play framebuffer.
Nonzero role pixels are overlaid; blank padding must not erase name pixels.
"""
from pathlib import Path
from PIL import Image
import json,sys
c={'credits_13_pages':json.loads((Path(__file__).resolve().parents[1]/'source/CREDIT_LAYOUT.json').read_text())}
def tiles(b,width,height):
 im=Image.new('L',(width,height))
 for y in range(height):
  for x in range(width):
   v=b[(y//8*(width//8)+x//8)*32+(y%8)*4+x%8//2];v=(v>>4 if x%2==0 else v&15);im.putpixel((x,y),v*17)
 return im
for p in Path(sys.argv[1]).glob('page_*/runtime/page_*.bin'):
 i=int(p.stem[-2:]);b=p.read_bytes();im=tiles(b[0x56e0:],96,144)
 for k,rec in enumerate(c['credits_13_pages'][i]['records']):
  role=tiles(b[0x7200+k*0x300:],96,16)
  # Diagnostic RAM composition: zero is background, never erase another field's ink.
  im.paste(role,(0,rec['size']*8),role.point(lambda value:255 if value else 0))
 im.save(p.with_suffix('.png'));im.resize((384,576),Image.Resampling.NEAREST).save(p.with_name('zoom.png'))
