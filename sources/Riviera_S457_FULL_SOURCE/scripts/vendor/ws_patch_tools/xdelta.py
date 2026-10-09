import os,shutil,subprocess,tempfile
from pathlib import Path

def resolve(explicit=None):
    c=[]
    if explicit: c.append(explicit)
    if os.environ.get('WS_XDELTA3_BIN'): c.append(os.environ['WS_XDELTA3_BIN'])
    c.append(str(Path(__file__).resolve().parents[2]/'vendor/bin/xdelta3'))
    s=shutil.which('xdelta3')
    if s: c.append(s)
    for x in c:
        if x and Path(x).is_file() and os.access(x,os.X_OK): return x
    return None

def info(explicit=None):
    p=resolve(explicit)
    if not p: return {'available':False,'path':None,'version':None}
    cp=subprocess.run([p,'-V'],capture_output=True,text=True)
    return {'available':True,'path':p,'version':(cp.stdout or cp.stderr).strip().splitlines()[0] if (cp.stdout or cp.stderr).strip() else None}

def create(source,target,patch,explicit=None):
    p=resolve(explicit)
    if not p: raise RuntimeError('xdelta3 not found; set WS_XDELTA3_BIN or vendor/bin/xdelta3')
    subprocess.run([p,'-e','-s',source,target,patch],check=True)

def apply(source,patch,out,explicit=None):
    p=resolve(explicit)
    if not p: raise RuntimeError('xdelta3 not found; set WS_XDELTA3_BIN or vendor/bin/xdelta3')
    subprocess.run([p,'-d','-s',source,patch,out],check=True)
