#!/usr/bin/env python3
"""Verify tracked bytes, modes, index entries and the required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

HEAD = '97e713168470bfae2685521fa557dc462b782b32'
TREE = 'e4c0561c897f787ce72c0258fb5caab1c79cf8a1'
root = Path.cwd()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)

def verify(where, revision):
    entries = {}
    for row in git(where, 'ls-tree', '-rz', revision).split(b'\0'):
        if not row:
            continue
        prefix, name = row.split(b'\t', 1)
        mode, kind, oid = prefix.decode().split()
        entries[os.fsdecode(name)] = (mode, kind, oid)
    index = {}
    for row in git(where, 'ls-files', '--stage', '-z').split(b'\0'):
        if not row:
            continue
        prefix, name = row.split(b'\t', 1)
        mode, oid, stage = prefix.decode().split()
        assert stage == '0', name
        index[os.fsdecode(name)] = (mode, oid)
    assert index == {n: (v[0], v[2]) for n, v in entries.items()}
    blobs = 0
    for name, (mode, kind, oid) in entries.items():
        if kind == 'commit':
            continue
        path = where / name
        st = path.lstat()
        actual_mode = '120000' if stat.S_ISLNK(st.st_mode) else ('100755' if st.st_mode & 0o111 else '100644')
        assert actual_mode == mode, (name, mode, actual_mode)
        if mode != '120000':
            assert stat.S_ISREG(st.st_mode), name
        data = os.fsencode(os.readlink(path)) if mode == '120000' else path.read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == oid, name
        blobs += 1
    assert not git(where, 'diff', '--no-ext-diff', '--no-textconv', revision, '--')
    return entries, blobs

assert git(root, 'rev-parse', 'HEAD').decode().strip() == HEAD
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
entries, blobs = verify(root, HEAD)
print('superproject:', HEAD, TREE, 'verified tracked blobs', blobs, 'index entries', len(entries))
for name in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
             'third_party/lwSRP', 'third_party/tsn-c-stack'):
    mode, kind, pin = entries[name]
    assert (mode, kind) == ('160000', 'commit')
    sub = root / name
    assert (sub / '.git').is_file()
    assert git(sub, 'rev-parse', 'HEAD').decode().strip() == pin
    _, n = verify(sub, pin)
    print(name, pin, 'verified tracked blobs', n)
print('untracked nonignored:', git(root, 'ls-files', '--others', '--exclude-standard').decode().strip() or 'none')
group = Path('/proc/self/cgroup')
if group.exists():
    path = Path('/sys/fs/cgroup') / group.read_text().strip().split(':')[-1].lstrip('/')
    if (path / 'memory.max').exists():
        print('unit memory:', json.dumps({n: (path / n).read_text().strip()
                                          for n in ('memory.peak', 'memory.max', 'memory.events')}))
print('exact tracked bytes, modes, index and required submodules: PASS')
