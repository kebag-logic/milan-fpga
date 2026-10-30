#!/usr/bin/env python3
"""Run bounded independent checks in the foreground and audit source integrity."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

PACKET = Path(__file__).resolve().parent
SOURCE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
PINNED = Path('$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
env = dict(os.environ, TMPDIR=str(PACKET/'scratch'), PYTHONDONTWRITEBYTECODE='1')
identity = subprocess.check_output([str(PINNED), '--version'], text=True)
assert '5.050' in identity and 'rev v5.050' in identity
env['PATH'] = str(PINNED.parent) + os.pathsep + env['PATH']
(PACKET/'lint-identity.txt').write_text(identity)

def command(name, argv):
    p = subprocess.run(argv, cwd=SOURCE, env=env, capture_output=True, text=True)
    (PACKET/(name+'.log')).write_text(p.stdout+p.stderr)
    (PACKET/(name+'.rc')).write_text(str(p.returncode)+'\n')
    return {'name':name, 'command':argv, 'rc':p.returncode}

jobs = [('contract', ['make','-j16','contract']),
        ('lint', ['make','-j16','lint']),
        ('whitespace', ['git','diff','--check','135afd04..HEAD'])]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(lambda args:command(*args),jobs))
(PACKET/'checks.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(x['rc']==0 for x in results)

def git(*args):
    return subprocess.check_output(['git','-C',str(SOURCE),*args])

head=git('rev-parse','HEAD').decode().strip()
tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert head=='411b35fcc56d11c2361d861e7205307587a04a1d'
assert tree=='131a1ffff543977e1881e3ba5b70a2871f7a6d89'
tracked=[]; gitlinks=[]
for entry in git('ls-tree','-rz','HEAD').split(b'\0'):
    if not entry: continue
    meta,rawpath=entry.split(b'\t',1)
    mode,kind,oid=meta.decode().split(); path=rawpath.decode()
    if mode=='160000':
        gitlinks.append({'path':path,'oid':oid});continue
    f=SOURCE/path
    data=os.readlink(f).encode() if mode=='120000' else f.read_bytes()
    digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    actualmode='120000' if f.is_symlink() else ('100755' if f.stat().st_mode & 0o111 else '100644')
    tracked.append({'path':path,'oid':oid,'bytes_match':digest==oid,'mode_match':mode==actualmode})
assert all(x['bytes_match'] and x['mode_match'] for x in tracked)
index_tree=git('write-tree').decode().strip()
status=git('status','--porcelain=v1').decode()
assert index_tree==tree and not status and not gitlinks
out={'head':head,'tree':tree,'index_tree':index_tree,'status':status,'gitlinks':gitlinks,'tracked':tracked}
(PACKET/'integrity.json').write_text(json.dumps(out,indent=2)+'\n')
(PACKET/'delta.diff').write_bytes(git('diff','806957b3..HEAD'))
(PACKET/'history.txt').write_bytes(git('log','--format=%h %s','135afd04..HEAD'))
(PACKET/'scope.txt').write_bytes(git('diff','--stat','135afd04..HEAD')+b'\nRound-three delta:\n'+git('diff','--stat','806957b3..HEAD')+b'\nImplementation delta (expected empty):\n'+git('diff','--name-only','135afd04..HEAD','--','hdl','bench','syn','Makefile'))
print('Checks:',[(x['name'],x['rc']) for x in results])
print('Exact tracked blobs and modes:',len(tracked),'; matching index; gitlinks:',gitlinks,'; status clean')
