"""Prove raw tracked bytes, types/modes, index and required submodule pins. Usage: integrity.py CHECKOUT."""
import hashlib
import os
import stat
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
head = '98c0b62be911f5cff7a03ebfee7f837c23847d14'
tree = '42431e547e28fcdaa50feec57700fef4887d92e0'
required = {'protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
            'third_party/tsn-c-stack', 'third_party/lwSRP'}

def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)

def audit(where, revision, label):
    expected = {}
    for entry in git(where, 'ls-tree', '-rz', revision).split(b'\0'):
        if not entry:
            continue
        meta, path = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected[path] = (mode, oid)
        if kind == b'commit':
            continue
        p = where / os.fsdecode(path)
        st = p.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), (label, path, 'type')
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode), (label, path, 'type')
            actual_mode = b'100755' if st.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, (label, path, 'mode')
            data = p.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert digest == oid, (label, path, 'bytes')
    index = {}
    for entry in git(where, 'ls-files', '--stage', '-z').split(b'\0'):
        if not entry:
            continue
        meta, path = entry.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and path not in index, (label, path, 'index stage')
        index[path] = (mode, oid)
    assert index == expected, (label, 'index differs from tree')
    flags = git(where, 'ls-files', '-v', '-z').split(b'\0')
    assert all(not e or e[:1] == b'H' for e in flags), (label, 'hidden/sparse index flag')
    print(f'PASS {label}: {len(expected)} entries; raw blobs, types/modes and index agree')
    return expected

assert git(root, 'rev-parse', 'HEAD').decode().strip() == head
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == tree
entries = audit(root, head, 'superproject')
for name in sorted(required):
    mode, oid = entries[name.encode()]
    assert mode == b'160000'
    sub = root / name
    assert (sub / '.git').is_file(), (name, 'not initialized as a submodule')
    assert git(sub, 'rev-parse', 'HEAD').strip() == oid, (name, 'pin')
    assert git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip() == str(root)
    audit(sub, oid.decode(), name)
    print(f'PIN {name} {oid.decode()}')
assert entries[b'external'][0] == b'160000'
assert not (root / 'external/.git').exists()
print('external gitlink unchanged and intentionally uninitialized:', entries[b'external'][1].decode())
status = git(root, 'status', '--porcelain=v1', '--untracked-files=all')
assert not status, status.decode()
print(f'PASS clean status; exact head {head}; tree {tree}')
