"""Prove raw tracked bytes, modes, index, HEAD and populated gitlinks.

Run from the review checkout; does not rely on status or skip-worktree flags.
"""
import hashlib
import os
import stat
import subprocess
from pathlib import Path

ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=ENV)

def verify(root, head):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == head
    entries = {}
    for entry in git(root, 'ls-tree', '-rz', head).split(b'\0'):
        if not entry:
            continue
        info, name = entry.split(b'\t', 1)
        mode, kind, oid = info.decode().split()
        entries[name] = (mode, oid)
    index = {}
    for entry in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not entry:
            continue
        info, name = entry.split(b'\t', 1)
        mode, oid, stage = info.decode().split()
        assert stage == '0'
        index[name] = (mode, oid)
    assert index == entries, 'Index differs from exact HEAD tree'
    count = 0
    for name, (mode, oid) in entries.items():
        path = root / os.fsdecode(name)
        if mode == '160000':
            if not (path / '.git').exists():
                assert name == b'external'
                print(f'PASS gitlink {os.fsdecode(name)} {oid}: unchanged, intentionally unpopulated')
                continue
            verify(path, oid)
            print(f'PASS gitlink {os.fsdecode(name)} {oid}: HEAD/index/raw contents verified')
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
        assert digest == oid, os.fsdecode(name)
        count += 1
    print(f'PASS {head}: {count} raw tracked blobs, modes and complete stage-0 index')

root = Path.cwd()
head = 'ac45db8f18a5fde87c84be2225cc1be7d709eae9'
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == '158ec1f4835ba66973eb381f98904aa675d0855c'
verify(root, head)
print('PASS exact reviewed head and tree; no tracked bytes required restoration')
