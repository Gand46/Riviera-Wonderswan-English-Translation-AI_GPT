"""S457: distinguish capital I from lowercase l in four credit names.

The global ROM font remains byte-identical. Only compiled credit graphics use a
three-pixel capital-I extension derived from the native one-pixel vertical stem.
"""
from pathlib import Path
import json,hashlib,struct,argparse
R=Path(__file__).resolve().parents[1]
BASE_SHA='b6ae03cda1be9d1742ca7aae3cfc32fe389c3fd51e9e3bc5b4929ff3653dcdc1'
STUB=0x7fdc40;DATA=0x7fde80;LIMIT=0x7fffd8
AFFECTED={'CREDIT-7A399A','CREDIT-7A3A3C','CREDIT-7A3AF1','CREDIT-7A3B4E'}
sha=lambda b:hashlib.sha256(b).hexdigest();word=lambda n:struct.pack('<H',n)
def rle(raw):
 out=bytearray();i=0
 while i<len(raw):
  zero=raw[i]==0;j=i+1
  while j<len(raw)and j-i<127 and(raw[j]==0)==zero:j+=1
  out.append((128 if zero else 0)+(j-i))
  if not zero:out+=raw[i:j]
  i=j
 return bytes(out)+b'\0'
def unrle(data):
 out=bytearray();i=0
 while data[i]:
  n=data[i];i+=1
  if n&128:out+=b'\0'*(n&127)
  else:out+=data[i:i+n];i+=n
 assert i==len(data)-1;return bytes(out)
def packbits(raw):
 assert len(raw)%4==0 and set(raw)<={0,6,0x60,0x66}
 return bytes(sum(((raw[i+j]&15!=0)+2*(raw[i+j]>>4!=0))<<(2*j)for j in range(4))for i in range(0,len(raw),4))
def unpackbits(raw):return bytes((6 if v&(1<<(2*j))else 0)+(0x60 if v&(2<<(2*j))else 0)for v in raw for j in range(4))
def pack2(raw):
 p={0:0,2:1,6:2};assert len(raw)%2==0
 return bytes(p[raw[i]&15]|p[raw[i]>>4]<<2|p[raw[i+1]&15]<<4|p[raw[i+1]>>4]<<6 for i in range(0,len(raw),2))
def unpack2(raw):
 p=[0,2,6,0];return bytes(p[(v>>j)&3]|p[(v>>(j+2))&3]<<4 for v in raw for j in [0,4])
def decode(data,m):
 raw=unrle(data)
 return unpackbits(raw)if m['codec']=='RLE_PACKED_1BPP_V1'else unpack2(raw)if m['codec']=='RLE_PACKED_2BPP_V1'else raw
def native_glyph(src,c):
 i=ord(c)-65 if c.isupper()else ord(c)-97+26;a=0x5534bc+i*50;raw=src[a:a+50]
 px=[[(raw[(y*10+x)//2]>>(4 if x%2==0 else 0))&15==6 for x in range(10)]for y in range(10)]
 xs=[x for row in px for x,v in enumerate(row)if v];return [row[min(xs):max(xs)+1]for row in px],dict(character=c,address=a,raw_sha256=sha(raw),width=max(xs)-min(xs)+1,height=10)
def glyph(src,c):
 px,ref=native_glyph(src,c)
 if c!='I':return px,ref
 assert len(px[0])==1 and px==[[False]]+[[True]]*7+[[False]]*2
 ext=[[False,False,False],[True,True,True]]+[[False,True,False]for _ in range(5)]+[[True,True,True]]+[[False,False,False]]*2
 return ext,dict(ref,extension='CAPITAL_I_SERIFS_NATIVE_STEM_V1',width=3,source_width=1,source_glyph_sha256=ref['raw_sha256'],font_data_changed=False)
def pxat(x,y):return(y//8*12+x//8)*32+y%8*4+x%8//2
def render(src,e):
 raw=bytearray(e['height']*48);metrics=[];refs={}
 for old in e['metrics']:
  line=old['text'];y=old['y'];gs={c:glyph(src,c)for c in set(line)if c!=' '}
  w=sum(3 if c==' 'else len(gs[c][0][0])+1 for c in line)-1;x=(96-w)//2
  assert 0<=x and w<=94 and y+10<=e['height'],(line,w,x,y,e['height'])
  metrics.append(dict(old,text=line,width=w,x=x,y=y,capital_i_extended='I'in line))
  for c in line:
   if c==' ':x+=3;continue
   pixels,ref=gs[c];refs[c]=ref
   for yy,row in enumerate(pixels):
    for xx,v in enumerate(row):
     if v:raw[pxat(x+xx,y+yy)]|=6<<(4 if(x+xx)%2==0 else 0)
   x+=len(pixels[0])+1
 return bytes(raw),dict(e,metrics=metrics,glyphs=[refs[c]for c in sorted(refs)],capital_i_extension='CAPITAL_I_SERIFS_NATIVE_STEM_V1')
def build(src):
 assert len(src)==8388608 and sha(src)==BASE_SHA
 s455=json.loads((R/'source/S455_RELEASE.json').read_text());s450=json.loads((R/'source/S450_RELEASE.json').read_text())
 assert sha(src[0x55364c:0x55364c+50])==sha(src[0x553bf6:0x553bf6+50])=='8ca1ac8443a83b2c6c6a9c8c2416ea3c5be51546b82379bf6739f70fc9e1e102'
 out=bytearray(src);blocks=[];payload=bytearray();changed_blocks=[]
 # Repack the current S455 handler from its exact decoded data, replacing page 0/5 graphics.
 for m in s455['blocks']:
  packed=src[m['source']:m['source']+m['compressed_length']];assert sha(packed)==m['compressed_sha256'];raw=decode(packed,m);assert sha(raw)==m['sha256']
  if m['id']in AFFECTED:raw,m=render(src,m);changed_blocks.append(m['id'])
  graphic=m['kind']=='native_glyph_graphic';codec=('RLE_PACKED_1BPP_V1'if set(raw)<={0,6,0x60,0x66}else'RLE_PACKED_2BPP_V1')if graphic else'RLE_ZERO_LITERAL_V1'
  enc=packbits(raw)if codec=='RLE_PACKED_1BPP_V1'else pack2(raw)if graphic else raw;packed=rle(enc);assert decode(packed,{'codec':codec})==raw
  m=dict(m,source=DATA+len(payload),length=len(raw),sha256=sha(raw),compressed_length=len(packed),compressed_sha256=sha(packed),codec=codec)
  blocks.append(m);payload+=packed
 # Rebuild the S455 dispatch/decoder byte-for-byte in architecture, with relocated block sources.
 code=bytearray.fromhex('9c5051535256571e0633c08ed8');calls=[]
 for page in sorted(set(b['page']for b in blocks)):
  code+=bytes.fromhex('33c08ed8')+b'\x80\x3e\x12\x16'+bytes([page+1]);j=len(code);code+=b'\x75\x00'+bytes.fromhex('b800f08ed833c08ec0fc')
  for b in blocks:
   if b['page']==page:code+=b'\xbe'+word(b['source']&65535)+b'\xbf'+word(b['destination']);calls.append((len(code),b['codec']));code+=b'\xe8\x00\x00'
  code[j+1]=len(code)-j-2;assert code[j+1]<128
 code+=bytes.fromhex('071f5f5e5a5b59589dea00c000f0');decoder=len(code);code+=bytes.fromhex('ac84c0741588c130eda8807504f3a4ebef80e17f30c0f3aaebe6c3')
 pdec=len(code);dec=bytearray.fromhex((R/'source/PACKED_DECODER.hex').read_text().strip());lut=STUB+len(code)+len(dec)
 for at in[27,44]:dec[at:at+2]=word(lut&65535)
 code+=dec
 for n in range(16):code+=word(sum((6 if n&(1<<k)else 0)<<(4*k)for k in range(4)))
 p2dec=len(code);dec=bytearray.fromhex((R/'source/PACKED2_DECODER.hex').read_text().strip());lut=STUB+len(code)+len(dec);pos=[i for i in range(len(dec)-1)if dec[i:i+2]==b'\x34\x12'];assert len(pos)==2
 for at in pos:dec[at:at+2]=word(lut&65535)
 code+=dec;code+=bytes([0,2,6,0][n&3]|[0,2,6,0][n>>2]<<4 for n in range(16))
 for at,codec in calls:
  target=pdec if codec=='RLE_PACKED_1BPP_V1'else p2dec if codec=='RLE_PACKED_2BPP_V1'else decoder;code[at+1:at+3]=word((target-at-3)&65535)
 end=DATA+len(payload);assert STUB+len(code)<=DATA and end<=LIMIT
 out[STUB:LIMIT]=b'\xff'*(LIMIT-STUB);out[STUB:STUB+len(code)]=code;out[DATA:end]=payload
 # Earlier S450 blocks are fixed-address uncompressed graphics below S455 ownership.
 older=[]
 for m in s450['blocks']:
  if m['id']not in AFFECTED:continue
  assert sha(src[m['source']:m['source']+m['length']])==m['sha256'];raw,nm=render(src,m);assert len(raw)==m['length'];out[m['source']:m['source']+len(raw)]=raw;older.append(dict(nm,source=m['source'],length=len(raw),sha256=sha(raw)));changed_blocks.append(m['id'])
 # Font ROM remains exact; animation tables and hooks are untouched.
 assert out[0x5534bc:0x5534bc+52*50]==src[0x5534bc:0x5534bc+52*50]
 out[-2:]=word(sum(out[:-2])&65535);result=bytes(out);changes=[i for i,(a,b)in enumerate(zip(src,result))if a!=b]
 allowed=set(range(STUB,LIMIT))|set(range(len(src)-2,len(src)))
 for m in older:allowed.update(range(m['source'],m['source']+m['length']))
 assert set(changes)<=allowed
 return result,dict(stage='S457',version='0.110',base_sha256=BASE_SHA,target_sha256=sha(result),checksum=f'{int.from_bytes(result[-2:],"little"):04X}',changed_bytes=len(changes),unexpected_changed_offsets=0,stub_address=STUB,stub_length=len(code),allocation_end=end,owned_region_end=LIMIT,blocks=blocks,older_blocks=older,changed_graphic_blocks=sorted(changed_blocks),affected_names=['Takeo Isogai','Tomofumi Ishida','Yoshinori Iwanaga','Fumie Ishinaka'],capital_i_extension='CAPITAL_I_SERIFS_NATIVE_STEM_V1',native_font_sha256=sha(src[0x5534bc:0x5534bc+52*50]),font_data_changed=False,animation_tables_changed=False,global_final_approved=False,stub_hex=code.hex())
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('base');p.add_argument('out');a=p.parse_args();b,r=build(Path(a.base).read_bytes());Path(a.out).write_bytes(b);Path(a.out).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items()if k not in ['blocks','older_blocks','stub_hex']})
