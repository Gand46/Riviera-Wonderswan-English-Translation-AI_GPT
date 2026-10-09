from .util import crc32
MAGIC=b'BPS1'

def encnum(v):
    if v<0: raise ValueError('negative BPS varint')
    out=bytearray()
    while True:
        x=v&0x7f; v >>= 7
        if v==0: out.append(x|0x80); break
        out.append(x); v-=1
    return bytes(out)

def decnum(data,pos):
    result=0; shift=1
    while True:
        if pos>=len(data): raise ValueError('truncated BPS varint')
        x=data[pos]; pos+=1; result += (x&0x7f)*shift
        if x&0x80: return result,pos
        shift <<=7; result += shift

def encsigned(v): return encnum((abs(v)<<1)|(1 if v<0 else 0))
def decsigned(data,pos):
    v,pos=decnum(data,pos); x=v>>1
    return (-x if v&1 else x),pos

def create(source,target,metadata=b''):
    if isinstance(metadata,str): metadata=metadata.encode('utf-8')
    out=bytearray(MAGIC); out+=encnum(len(source))+encnum(len(target))+encnum(len(metadata))+metadata
    i=0
    # Emit SourceRead for unchanged same-offset runs, TargetRead for all changed bytes.
    while i<len(target):
        same=i<len(source) and source[i]==target[i]
        j=i+1
        if same:
            while j<len(target) and j<len(source) and source[j]==target[j]: j+=1
            mode=0; payload=b''
        else:
            while j<len(target) and not (j<len(source) and source[j]==target[j]): j+=1
            mode=1; payload=target[i:j]
        out += encnum(((j-i-1)<<2)|mode)
        if mode==1: out += payload
        i=j
    out += crc32(source).to_bytes(4,'little')
    out += crc32(target).to_bytes(4,'little')
    out += crc32(out).to_bytes(4,'little')
    return bytes(out)

def parse_header(p):
    if not p.startswith(MAGIC): raise ValueError('not a BPS patch')
    pos=4; ss,pos=decnum(p,pos); ts,pos=decnum(p,pos); ms,pos=decnum(p,pos)
    if pos+ms>len(p)-12: raise ValueError('truncated BPS metadata')
    md=p[pos:pos+ms]; pos+=ms
    return ss,ts,md,pos

def apply(source,p,verify_crc=True):
    ss,ts,md,pos=parse_header(p)
    if len(source)!=ss: raise ValueError(f'BPS source size mismatch: expected {ss}, got {len(source)}')
    if len(p)<pos+12: raise ValueError('truncated BPS patch')
    src_crc=int.from_bytes(p[-12:-8],'little'); tgt_crc=int.from_bytes(p[-8:-4],'little'); patch_crc=int.from_bytes(p[-4:],'little')
    if verify_crc and crc32(p[:-4])!=patch_crc: raise ValueError('BPS patch CRC mismatch')
    if verify_crc and crc32(source)!=src_crc: raise ValueError('BPS source CRC mismatch')
    end=len(p)-12; out=bytearray(); source_rel=0; target_rel=0
    while len(out)<ts:
        if pos>=end: raise ValueError('BPS action stream ended early')
        act,pos=decnum(p,pos); mode=act&3; length=(act>>2)+1
        if mode==0:
            s=len(out); out += source[s:s+length]
            if len(out)!=s+length: raise ValueError('BPS SourceRead out of range')
        elif mode==1:
            if pos+length>end: raise ValueError('BPS TargetRead out of range')
            out += p[pos:pos+length]; pos+=length
        elif mode==2:
            delta,pos=decsigned(p,pos); source_rel += delta
            if source_rel<0 or source_rel+length>len(source): raise ValueError('BPS SourceCopy out of range')
            out += source[source_rel:source_rel+length]; source_rel += length
        else:
            delta,pos=decsigned(p,pos); target_rel += delta
            if target_rel<0 or target_rel>=len(out): raise ValueError('BPS TargetCopy out of range')
            for _ in range(length):
                if target_rel>=len(out): raise ValueError('BPS TargetCopy out of range')
                out.append(out[target_rel]); target_rel+=1
        if len(out)>ts: raise ValueError('BPS produced too much output')
    out=bytes(out)
    if verify_crc and crc32(out)!=tgt_crc: raise ValueError('BPS target CRC mismatch')
    return out

def info(p):
    ss,ts,md,pos=parse_header(p)
    return {'format':'bps','source_size':ss,'target_size':ts,'metadata':md.decode('utf-8','replace'),'size':len(p),'source_crc32':f'{int.from_bytes(p[-12:-8],"little"):08x}','target_crc32':f'{int.from_bytes(p[-8:-4],"little"):08x}','patch_crc32':f'{int.from_bytes(p[-4:],"little"):08x}'}
