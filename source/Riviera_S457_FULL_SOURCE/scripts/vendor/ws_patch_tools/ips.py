MAGIC=b'PATCH'; EOF=b'EOF'

def create(source,target):
    if len(target)>0xFFFFFF: raise ValueError('IPS target exceeds 24-bit address space')
    out=bytearray(MAGIC); i=0; n=len(target)
    while i<n:
        if i<len(source) and source[i]==target[i]: i+=1; continue
        start=i; chunk=bytearray()
        while i<n and (i>=len(source) or source[i]!=target[i]) and len(chunk)<0xFFFF:
            chunk.append(target[i]); i+=1
        # RLE if a changed run is long and constant.
        if len(chunk)>=4 and len(set(chunk))==1:
            out += start.to_bytes(3,'big') + b'\x00\x00' + len(chunk).to_bytes(2,'big') + bytes([chunk[0]])
        else:
            out += start.to_bytes(3,'big') + len(chunk).to_bytes(2,'big') + chunk
    out += EOF
    if len(target)!=len(source): out += len(target).to_bytes(3,'big')
    return bytes(out)

def apply(source,patch):
    if not patch.startswith(MAGIC): raise ValueError('not an IPS patch')
    out=bytearray(source); i=5
    while True:
        if patch[i:i+3]==EOF:
            i+=3; break
        if i+5>len(patch): raise ValueError('truncated IPS record')
        off=int.from_bytes(patch[i:i+3],'big'); size=int.from_bytes(patch[i+3:i+5],'big'); i+=5
        if size==0:
            if i+3>len(patch): raise ValueError('truncated IPS RLE record')
            r=int.from_bytes(patch[i:i+2],'big'); val=patch[i+2]; i+=3; data=bytes([val])*r
        else:
            if i+size>len(patch): raise ValueError('truncated IPS data')
            data=patch[i:i+size]
            i+=size
        if len(out)<off+len(data): out.extend(b'\x00'*(off+len(data)-len(out)))
        out[off:off+len(data)]=data
    if len(patch)-i>=3:
        final=int.from_bytes(patch[i:i+3],'big'); del out[final:]
        if len(out)<final: out.extend(b'\x00'*(final-len(out)))
    return bytes(out)

def info(p):
    if not p.startswith(MAGIC): raise ValueError('not IPS')
    i=5; records=0
    while p[i:i+3]!=EOF:
        off=int.from_bytes(p[i:i+3],'big'); sz=int.from_bytes(p[i+3:i+5],'big'); i+=5
        i += 3 if sz==0 else sz; records+=1
        if i>len(p): raise ValueError('truncated IPS')
    return {'format':'ips','records':records,'size':len(p)}
