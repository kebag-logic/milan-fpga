#!/usr/bin/env python3
"""Check actual blob bytes, executable modes, index, tree and recorded parent pins."""
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
def git(*args):
    return subprocess.check_output(['git',*args],cwd=root)
head = git('rev-parse','HEAD').decode().strip()
tree = git('rev-parse','HEAD^{tree}').decode().strip()
assert head == '8947bafdd62b4bf991debf7bfd8cdb73994a3a81'
assert tree == '9436b17406d7f6a1f9241331781bcc09a5d72633'
index = {}
for entry in git('ls-files','--stage','-z').split(b'\0'):
    if entry:
        meta,path = entry.split(b'\t',1)
        mode,oid,stage = meta.decode().split()
        assert stage=='0'
        index[path.decode()] = (mode,oid)
rows = []
gitlinks = []
for entry in git('ls-tree','-rz','HEAD').split(b'\0'):
    if not entry:
        continue
    meta,path = entry.split(b'\t',1)
    mode,kind,oid = meta.decode().split()
    rel = path.decode()
    assert index.pop(rel)==(mode,oid), rel
    file = root/rel
    if kind=='commit':
        actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=file).decode().strip()
        assert actual==oid
        gitlinks.append({'path':rel,'sha':oid})
        continue
    if mode=='120000':
        data = file.readlink().as_posix().encode()
        actual_mode='120000'
    else:
        data=file.read_bytes()
        actual_mode='100755' if file.stat().st_mode & stat.S_IXUSR else '100644'
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert actual==oid and actual_mode==mode, rel
    rows.append({'path':rel,'mode':mode,'git_blob':oid,'sha256':hashlib.sha256(data).hexdigest()})
assert not index
assert git('status','--porcelain=v1')==b''
parents=[]
for name in ('parent-recorded-tree','parent-live-tree'):
    public=json.loads((packet/'scratch'/f'{name}.json').read_text())
    links=[r for r in public['tree'] if r['mode']=='160000']
    d={r['path']:r['sha'] for r in links}
    assert d['gptp-processor']=='5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d'
    assert d['third_party/verilog-axis']=='48ff7a7e2ef782cf778d47910cf85835c64b1bce'
    assert d['protocol-processor']=='ead8036035affd53ef4b29979190f2f4f67084c0'
    parents.append({'record':name,'revision':public['sha'],'gitlinks':links})
out={'head':head,'tree':tree,'status':'clean','tracked_blob_count':len(rows),
     'all_bytes_modes_index_match':True,'checkout_gitlinks':gitlinks,'parent_metadata':parents,
     'measurement_substitution':'The historical measurement substitutes c4539ff1 for the recorded processor gitlink; its comment-only equivalence to this head is separately audited.',
     'files':rows}
(packet/'receipts/checkout-integrity.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='files'},indent=2))
