#!/usr/bin/env python3
"""Verify tracked bytes, executable modes, index stages and required gitlinks."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
head = '313616d1a18549d41907db389d378f0beb9bc543'
def git(*args, cwd=root):
    return subprocess.check_output(['git', *args], cwd=cwd)

def verify(repo, expected, label):
    assert git('rev-parse', 'HEAD', cwd=repo).decode().strip() == expected
    entries = git('ls-tree', '-rz', 'HEAD', cwd=repo).split(b'\0')
    index = git('ls-files', '--stage', '-z', cwd=repo).split(b'\0')
    wanted = []
    count = 0
    for entry in entries:
        if not entry:
            continue
        meta, path = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        wanted.append(mode + b' ' + oid + b' 0\t' + path)
        if kind == b'commit':
            continue
        f = repo / os.fsdecode(path)
        if mode == b'120000':
            assert f.is_symlink(), (label, path, 'not symlink')
            data = os.fsencode(os.readlink(f))
        else:
            assert f.is_file() and not f.is_symlink(), (label, path, 'not regular')
            actual_mode = b'100755' if f.stat().st_mode & 0o111 else b'100644'
            assert mode == actual_mode, (label, path, 'mode')
            data = f.read_bytes()
        actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert oid == actual, (label, path, 'bytes')
        count += 1
    assert sorted(wanted) == sorted(e for e in index if e), (label, 'index mismatch')
    print(f'PASS {label}: HEAD={expected}; {count} tracked blobs match bytes/modes/index')

verify(root, head, 'candidate')
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == '8eb5d868bfac1973ba1d82b0665aabae07d9494c'
for sub in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
    pin = git('rev-parse', 'HEAD:'+sub).decode().strip()
    directory = root / sub
    assert not directory.is_symlink() and (directory / '.git').is_file()
    verify(directory, pin, sub)
print('PASS exact requested tree and all three required submodule gitlinks')
