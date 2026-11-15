#!/usr/bin/env python3
"""Check tracked bytes, file modes, index entries, and required submodule pins."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1])
head = '234bc149ff888eb96659ecaaa5ce6e4fb27319d4'
tree = '9b54edcc9bd235b734ad559291cdf1ec6da4716c'
env = os.environ | {'GIT_NO_REPLACE_OBJECTS': '1'}
def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)
def verify(repo, rev):
    records = git(repo, 'ls-tree', '-rz', rev).split(b'\0')
    expected = []
    files = 0
    links = {}
    for record in filter(None, records):
        meta, path = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected.append(mode + b' ' + oid + b' 0\t' + path)
        if mode == b'160000':
            links[os.fsdecode(path)] = oid.decode()
            continue
        p = repo / os.fsdecode(path)
        st = p.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), path
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode), path
            assert bool(st.st_mode & 0o111) == (mode == b'100755'), path
            data = p.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid.decode(), path
        files += 1
    actual_index = list(filter(None, git(repo, 'ls-files', '--stage', '-z').split(b'\0')))
    assert sorted(actual_index) == sorted(expected), 'index differs from commit tree'
    return files, links
assert git(root, 'rev-parse', 'HEAD').decode().strip() == head
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == tree
files, links = verify(root, head)
print('HEAD', head)
print('TREE', tree)
print('Root tracked blob bytes/modes/index: PASS;', files, 'files')
for name in ['protocol-processor', 'gptp-processor', 'third_party/lwSRP', 'third_party/tsn-c-stack', 'third_party/verilog-axis']:
    pin = links[name]
    sub = root / name
    assert (sub / '.git').is_file(), name
    assert git(sub, 'rev-parse', 'HEAD').decode().strip() == pin, name
    count, nested = verify(sub, pin)
    print(name, pin, 'PASS;', count, 'blob files; nested gitlinks', len(nested))
print('Other superproject gitlinks are index-verified; external is uninitialized and not required by this review.')
print('Tracked status:', git(root, 'status', '--porcelain=v1', '--untracked-files=no').decode().strip() or 'clean')
