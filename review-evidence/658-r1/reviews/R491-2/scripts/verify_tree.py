#!/usr/bin/env python3
"""Prove tracked bytes, modes, index and initialized required gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)
def verify(repo, revision):
    tree = git(repo, 'ls-tree', '-rz', revision)
    index = git(repo, 'ls-files', '--stage', '-z')
    expected = []
    count = 0
    for item in tree.split(b'\0'):
        if not item:
            continue
        meta, raw_path = item.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected.append(mode + b' ' + oid + b' 0\t' + raw_path)
        if kind == b'commit':
            continue
        path = repo / os.fsdecode(raw_path)
        s = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(s.st_mode), raw_path
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(s.st_mode), raw_path
            assert bool(s.st_mode & 0o111) == (mode == b'100755'), raw_path
            data = path.read_bytes()
        got = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert got == oid, raw_path
        count += 1
    assert sorted(index.rstrip(b'\0').split(b'\0')) == sorted(expected), 'index differs'
    assert git(repo, 'rev-parse', 'HEAD').strip().decode() == revision
    print(f'{repo.name}: {revision} bytes/modes/index PASS ({count} blobs)')
head = '5747a8cb99495cb0331658cdd499b9c44e3eda91'
verify(root, head)
assert git(root, 'rev-parse', 'HEAD^{tree}').strip() == b'd1d63caa2490c515624194cb5711ddb76c1601dd'
for sub in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
    pin = git(root, 'rev-parse', head + ':' + sub).strip().decode()
    assert (root / sub / '.git').is_file(), 'not a registered submodule'
    verify(root / sub, pin)
print('PASS: exact parent tree and all three required submodule gitlinks')
