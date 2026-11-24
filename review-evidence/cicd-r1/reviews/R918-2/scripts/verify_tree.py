#!/usr/bin/env python3
"""Check #998 exact-head bytes, modes, index and required submodule pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = 'fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f'
TREE = '6aa4a42135fc7615a344aba1935eac8133bdf54b'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)

def verify(repo, revision):
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == revision
    expected = {}
    entries = git(repo, 'ls-tree', '-rz', revision).split(b'\0')
    blobs = 0
    links = {}
    for entry in entries:
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected[name] = (mode, oid, b'0')
        path = repo / os.fsdecode(name)
        if kind == b'commit':
            links[os.fsdecode(name)] = oid.decode()
            continue
        info = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), os.fsdecode(name)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), os.fsdecode(name)
            actual_mode = b'100755' if info.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, os.fsdecode(name)
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert digest == oid, os.fsdecode(name)
        blobs += 1
    index = {}
    for entry in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if entry:
            meta, name = entry.split(b'\t', 1)
            index[name] = tuple(meta.split())
    assert index == expected, 'Index differs from committed tree'
    return {'head': revision, 'blobs_checked': blobs, 'index_matches': True,
            'bytes_and_modes_match': True, 'gitlinks': links}

repo = Path(sys.argv[1]).resolve()
assert git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
assert subprocess.run(['git', '-C', str(repo), 'symbolic-ref', '-q', 'HEAD'],
                      stdout=subprocess.DEVNULL, env=env).returncode == 1
root = verify(repo, HEAD)
submodules = {}
for name in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
             'third_party/tsn-c-stack', 'third_party/lwSRP'):
    submodules[name] = verify(repo / name, root['gitlinks'][name])
print(json.dumps({'result': 'PASS', 'tree': TREE, 'detached': True,
                  'root': root, 'submodules': submodules,
                  'excluded': ['external: uninitialized, not required for this review']}, indent=2))
