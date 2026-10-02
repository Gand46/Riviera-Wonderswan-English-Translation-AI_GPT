import argparse,json,sys,tempfile
from pathlib import Path
from . import __version__
from . import ips,bps,xdelta
from .util import sha256

def detect(data,path=''):
    if data.startswith(b'PATCH'): return 'ips'
    if data.startswith(b'BPS1'): return 'bps'
    if str(path).lower().endswith(('.xdelta','.vcdiff','.xdelta3')): return 'xdelta'
    return 'xdelta' if data[:3]==b'\xd6\xc3\xc4' else 'unknown'

def emit(v,j): print(json.dumps(v,indent=2,ensure_ascii=False) if j or isinstance(v,(dict,list)) else v)
def main(argv=None):
    p=argparse.ArgumentParser(prog='ws-patch-tools'); p.add_argument('--version',action='version',version=__version__); p.add_argument('--xdelta-bin'); sp=p.add_subparsers(dest='cmd',required=True)
    q=sp.add_parser('backend'); q.add_argument('--json',action='store_true')
    q=sp.add_parser('info'); q.add_argument('patch'); q.add_argument('--json',action='store_true')
    q=sp.add_parser('create'); q.add_argument('--format',choices=['ips','bps','xdelta'],required=True); q.add_argument('source'); q.add_argument('target'); q.add_argument('patch'); q.add_argument('--metadata',default=''); q.add_argument('--json',action='store_true')
    q=sp.add_parser('apply'); q.add_argument('patch'); q.add_argument('source'); q.add_argument('output'); q.add_argument('--format',default='auto',choices=['auto','ips','bps','xdelta']); q.add_argument('--json',action='store_true')
    q=sp.add_parser('verify'); q.add_argument('patch'); q.add_argument('source'); q.add_argument('target'); q.add_argument('--format',default='auto',choices=['auto','ips','bps','xdelta']); q.add_argument('--json',action='store_true')
    a=p.parse_args(argv)
    try:
        if a.cmd=='backend': emit({'ips':'native','bps':'native','xdelta3':xdelta.info(a.xdelta_bin)},a.json); return 0
        pb=Path(a.patch).read_bytes() if a.cmd!='create' else None
        fmt=(detect(pb,a.patch) if getattr(a,'format','auto')=='auto' else getattr(a,'format',None))
        if a.cmd=='info':
            fmt=detect(pb,a.patch)
            if fmt=='ips': v=ips.info(pb)
            elif fmt=='bps': v=bps.info(pb)
            else: v={'format':fmt,'size':len(pb),'sha256':sha256(pb)}
            emit(v,a.json); return 0
        if a.cmd=='create':
            s=Path(a.source).read_bytes(); t=Path(a.target).read_bytes()
            if a.format=='ips': data=ips.create(s,t); Path(a.patch).write_bytes(data)
            elif a.format=='bps': data=bps.create(s,t,a.metadata); Path(a.patch).write_bytes(data)
            else: xdelta.create(a.source,a.target,a.patch,a.xdelta_bin); data=Path(a.patch).read_bytes()
            emit({'format':a.format,'patch':a.patch,'patch_size':len(data),'patch_sha256':sha256(data),'source_sha256':sha256(s),'target_sha256':sha256(t)},a.json); return 0
        if a.cmd=='apply':
            s=Path(a.source).read_bytes()
            if fmt=='ips': o=ips.apply(s,pb); Path(a.output).write_bytes(o)
            elif fmt=='bps': o=bps.apply(s,pb); Path(a.output).write_bytes(o)
            elif fmt=='xdelta': xdelta.apply(a.source,a.patch,a.output,a.xdelta_bin); o=Path(a.output).read_bytes()
            else: raise ValueError('unknown patch format')
            emit({'format':fmt,'output':a.output,'output_size':len(o),'output_sha256':sha256(o)},a.json); return 0
        if a.cmd=='verify':
            s=Path(a.source).read_bytes(); target=Path(a.target).read_bytes()
            if fmt=='ips': got=ips.apply(s,pb)
            elif fmt=='bps': got=bps.apply(s,pb)
            elif fmt=='xdelta':
                with tempfile.TemporaryDirectory() as d:
                    q=str(Path(d)/'out'); xdelta.apply(a.source,a.patch,q,a.xdelta_bin); got=Path(q).read_bytes()
            else: raise ValueError('unknown patch format')
            ok=got==target
            emit({'format':fmt,'verified':ok,'expected_sha256':sha256(target),'actual_sha256':sha256(got)},a.json); return 0 if ok else 4
    except Exception as e:
        print(f'error: {e}',file=sys.stderr); return 2
if __name__=='__main__': raise SystemExit(main())
