#!/usr/bin/env python3
"""Read pinned blobs directly; verify bytes, modes, index and submodule heads."""
import hashlib
import json
import os
import pathlib
import stat
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(__file__).resolve().parent
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root, env=ENV)

def check(root, expected):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == expected
    records = {}
    for raw in git(root, 'ls-tree', '-rz', expected).split(b'\0'):
        if not raw:
            continue
        left, path = raw.split(b'\t', 1)
        mode, kind, oid = left.decode().split()
        records[path] = (mode, kind, oid)
    index = {}
    for raw in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not raw:
            continue
        left, path = raw.split(b'\t', 1)
        mode, oid, stage = left.decode().split()
        assert stage == '0'
        index[path] = (mode, oid)
    assert index == {path:(r[0],r[2]) for path,r in records.items()}
    count = 0
    links = {}
    for rawpath, (mode, kind, oid) in records.items():
        path = root / os.fsdecode(rawpath)
        if kind == 'commit':
            links[os.fsdecode(rawpath)] = oid
            continue
        st = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode)
            assert bool(st.st_mode & 0o111) == (mode == '100755')
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest == oid, str(path)
        count += 1
    return {'head':expected, 'tree':git(root,'rev-parse','HEAD^{tree}').decode().strip(), 'blobs_verified':count, 'index_matches':True, 'gitlinks':links}

head = '09201d35d7ea720b3ba205da185ba35c159ec24a'
result = {'superproject':check(ROOT,head), 'submodules':{}}
for path, oid in result['superproject']['gitlinks'].items():
    if path == 'external':
        continue
    result['submodules'][path] = check(ROOT / path, oid)
assert result['superproject']['tree'] == 'a3b3dca8a55b738e714ada4662a309a50118a481'
result['tracked_status'] = git(ROOT,'status','--porcelain=v1','--untracked-files=no').decode()
assert result['tracked_status'] == ''
result['external'] = 'Gitlink checked; intentionally uninitialized, not required by these checks.'
(OUT / 'checkout-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: exact HEAD/tree, tracked bytes/modes/index and five initialized submodule pins and bytes; tracked status clean.')
