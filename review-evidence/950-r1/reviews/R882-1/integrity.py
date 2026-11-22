#!/usr/bin/env python3
"""Compare raw bytes, modes, index tree and initialized gitlinks with HEAD."""
import os
import stat
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
expected = '287ca1ee96e69f71a5036061d2bf33c564965755'
def git(path, *args, **kwargs):
    return subprocess.check_output(['git', '-C', str(path), *args], **kwargs)

def verify(path, head, label):
    assert git(path, 'rev-parse', 'HEAD').decode().strip() == head
    tree = git(path, 'rev-parse', 'HEAD^{tree}').strip()
    assert git(path, 'write-tree').strip() == tree
    count = 0
    links = []
    for entry in git(path, 'ls-tree', '-rz', 'HEAD').split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        f = path / os.fsdecode(name)
        if kind == b'commit':
            links.append((name, oid))
            continue
        st = f.lstat()
        actual_mode = b'120000' if stat.S_ISLNK(st.st_mode) else b'100755' if st.st_mode & 0o111 else b'100644'
        assert actual_mode == mode, (label, name, 'mode')
        data = os.fsencode(os.readlink(f)) if stat.S_ISLNK(st.st_mode) else f.read_bytes()
        actual = subprocess.check_output(['git', 'hash-object', '--stdin', '--no-filters'], input=data).strip()
        assert actual == oid, (label, name, 'bytes')
        count += 1
    print(label, head, 'tree', tree.decode(), 'index and raw blobs/modes PASS', count)
    return links

links = verify(root, expected, 'candidate')
required = {'protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
            'third_party/tsn-c-stack', 'third_party/lwSRP'}
for name, oid in links:
    label = os.fsdecode(name)
    if label in required:
        assert (root / label / '.git').exists(), label
        verify(root / label, oid.decode(), label)
        required.remove(label)
    else:
        print(label, 'gitlink', oid.decode(), 'uninitialized, not a test dependency')
assert not required
print('PASS exact-head integrity')
