#!/usr/bin/env python3
"""Verify tracked bytes, executable modes, index records and required submodule pins."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)

required = {'protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
            'third_party/tsn-c-stack', 'third_party/lwSRP'}
lines = []
def verify(where, rev, label, top=False):
    assert git(where, 'rev-parse', 'HEAD').decode().strip() == rev
    expected = {}
    links = []
    files = 0
    for raw in git(where, 'ls-tree', '-rz', rev).split(b'\0'):
        if not raw: continue
        meta, name = raw.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = os.fsdecode(name)
        expected[name] = (mode, oid, '0')
        path = where / name
        if kind == 'commit':
            links.append((name, oid))
            continue
        st = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode), (label, name, 'symlink type')
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), (label, name, 'regular type')
            assert bool(st.st_mode & 0o111) == (mode == '100755'), (label, name, 'mode')
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, (label, name, 'blob')
        files += 1
    index = {}
    for raw in git(where, 'ls-files', '-sz').split(b'\0'):
        if not raw: continue
        meta, name = raw.split(b'\t', 1)
        key = os.fsdecode(name)
        assert key not in index, (label, key, 'duplicate index')
        index[key] = tuple(meta.decode().split())
    assert index == expected, (label, 'index differs from tree')
    lines.append(f'{label}: {rev}, {files} tracked blobs/modes and {len(index)} stage-0 index entries PASS')
    for name, oid in links:
        initialized = (where / name / '.git').exists()
        if top and name in required:
            assert initialized, ('required submodule absent', name)
        lines.append(f'{label}/{name}: gitlink {oid}, initialized={initialized}')
        if initialized:
            verify(where / name, oid, label + '/' + name)

head = '2b295a44d136275ccbf060fe4f36c42e573b6460'
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == 'd18031d79799e3e765e05b82528cbcc40b0af332'
verify(root, head, 'review-root', True)
lines.append('External legacy submodule is uninitialized; its gitlink/index are verified, its worktree is not claimed.')
text = '\n'.join(lines) + '\n'
(out / 'tree-integrity.txt').write_text(text)
print(text)
