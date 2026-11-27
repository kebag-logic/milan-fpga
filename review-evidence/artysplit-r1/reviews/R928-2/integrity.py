"""Verify tracked file bytes, executable modes, index entries and required gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

source = Path(sys.argv[1])
HEAD = '4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1'
TREE = 'ee1b81d4fcd318aeca7c37c8096d35e0e056ea8a'

def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)

def verify(root, expected):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == expected
    entries = {}
    for line in git(root, 'ls-tree', '-r', '-z', 'HEAD').split(b'\0'):
        if not line:
            continue
        meta, path = line.split(b'\t', 1)
        mode, kind, oid = meta.split()
        entries[path] = (mode, oid)
        if mode == b'160000':
            continue
        file = root / os.fsdecode(path)
        info = file.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode)
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(info.st_mode)
            actual_mode = b'100755' if info.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, (path, mode, actual_mode)
            data = file.read_bytes()
        got = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert got == oid, (path, oid, got)
    index = {}
    for line in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not line:
            continue
        meta, path = line.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0'
        index[path] = (mode, oid)
    assert index == entries
    return entries

entries = verify(source, HEAD)
assert git(source, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
print('PARENT', HEAD, TREE, len(entries), 'tracked entries: bytes/modes/index exact')
for name in ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
             'third_party/tsn-c-stack', 'third_party/lwSRP']:
    mode, oid = entries[name.encode()]
    assert mode == b'160000'
    sub = source/name
    assert (sub/'.git').exists() and not sub.is_symlink()
    checked = verify(sub, oid.decode())
    print('SUBMODULE', name, oid.decode(), len(checked), 'tracked entries exact')
status = git(source, 'status', '--porcelain', '--untracked-files=normal').decode()
print('PARENT STATUS', repr(status))
assert not status
print('PASS final source integrity')
