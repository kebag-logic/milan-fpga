#!/usr/bin/env python3
"""Hash tracked bytes directly, independently of git stat-cache shortcuts."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
head = 'e355f789b4f59b86083809299134557ca47bbcfb'
base = 'fa7347fc59173f90e4feec2df207692e6e6e72ec'
def git(path,*args):
    return subprocess.check_output(['git','--no-replace-objects',*args],cwd=path)
def verify(path, revision):
    assert git(path,'rev-parse','HEAD').decode().strip() == revision
    tree = git(path,'ls-tree','-rz',revision)
    wanted_index = []
    count = 0
    links = {}
    for entry in tree.split(b'\0'):
        if not entry: continue
        metadata,name = entry.split(b'\t',1)
        mode,kind,oid = metadata.split()
        wanted_index.append(mode+b' '+oid+b' 0\t'+name+b'\0')
        f = path / os.fsdecode(name)
        if kind == b'commit':
            links[os.fsdecode(name)] = oid.decode()
            continue
        info = f.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode)
            data = os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(info.st_mode)
            assert bool(info.st_mode & 0o111) == (mode == b'100755')
            data = f.read_bytes()
        actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual == oid.decode(), os.fsdecode(name)
        count += 1
    assert b''.join(wanted_index) == git(path,'ls-files','--stage','-z')
    return dict(head=revision, checked_blobs=count, index_equal=True, gitlinks=links)
result = verify(root,head)
result['tree'] = git(root,'rev-parse','HEAD^{tree}').decode().strip()
assert result['tree'] == '42f0ade89e45e059ac27a477376ec3f289996e54'
result['submodules'] = {}
for name,oid in result['gitlinks'].items():
    assert git(root,'rev-parse',base+':'+name).decode().strip()==oid
    if (root/name/'.git').exists():
        result['submodules'][name]=verify(root/name,oid)
    else:
        result['submodules'][name]={'gitlink':oid,'initialized':False}
result['status'] = git(root,'status','--porcelain').decode()
assert not result['status']
diff = git(root,'diff','--no-ext-diff','--no-textconv',base+'..'+head)
result['diff_sha256'] = hashlib.sha256(diff).hexdigest()
result['changed_paths'] = git(root,'diff','--name-only',base+'..'+head).decode().splitlines()
assert not any(p.startswith(('.github/','hdl/','sw/','tb/')) for p in result['changed_paths'])
result['workflow_tree_unchanged'] = git(root,'rev-parse',base+':.github/workflows') == git(root,'rev-parse',head+':.github/workflows')
(packet/'final-tree.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: exact head/tree,',result['checked_blobs'],'blob bytes/modes, index, six gitlinks, initialized submodule bytes/index and clean status')
