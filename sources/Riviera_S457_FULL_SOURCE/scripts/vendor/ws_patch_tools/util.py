import hashlib,zlib

def sha256(b): return hashlib.sha256(b).hexdigest()
def crc32(b): return zlib.crc32(b)&0xffffffff
