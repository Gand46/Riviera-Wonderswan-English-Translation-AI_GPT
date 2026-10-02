#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json

ROOT=Path(__file__).resolve().parent;CHUNK=ROOT/'chunk0';ROM=ROOT.parent/'Riviera_EN_v0.113_S460_RC4.wsc'
diag=json.loads((ROOT/'DIAGNOSTIC_BUILD.json').read_text());raw=ROM.read_bytes();captures=[]
for change in diag['changes']:
    start=int(change['target_stream_rom'],16);end=start+change['target_bytes'];page=1;pos=start
    while pos<end:
        value=raw[pos]
        if value in (0xFE,0xFF):
            matches=sorted(CHUNK.glob(f'dialog_*_{pos:06X}_{value:02X}.png'));assert matches,(hex(pos),change)
            path=matches[0];captures.append({'old_stream_rom':change['target_old_stream_rom'],'page':page,'boundary_rom':hex(pos),'capture':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
            page+=1
        pos += 2 if value==0xFE or 0xA2<=value<=0xA8 else 1
assert len(captures)==sum(len(c['expected_pages']) for c in diag['changes'])==12
first=Image.open(ROOT/captures[0]['capture']).convert('RGB');w,h=first.size;label=18;cols,rows=4,3
canvas=Image.new('RGB',(cols*w,rows*(h+label)),(28,31,37));draw=ImageDraw.Draw(canvas)
for i,item in enumerate(captures):
    x=(i%cols)*w;y=(i//cols)*(h+label);im=Image.open(ROOT/item['capture']).convert('RGB');canvas.paste(im,(x,y+label))
    draw.text((x+2,y+2),f"{item['old_stream_rom']} p{item['page']}",fill='white')
out=ROOT/'CONDITIONAL_STREAMS_SYNTHETIC_CONTACT.png';canvas.resize((canvas.width*2,canvas.height*2),Image.Resampling.NEAREST).save(out)
(ROOT/'SYNTHETIC_CAPTURE_MANIFEST.json').write_text(json.dumps({'pages':captures,'page_count':len(captures),'contact_sheet':out.name,'contact_sheet_sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2)+'\n')
print('WROTE',out,len(captures),'pages')
