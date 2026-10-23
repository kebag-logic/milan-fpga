#!/usr/bin/env python3
"""Verify tracked bytes, modes, index and required gitlinks without modifying them."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]).resolve()
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', GIT_OPTIONAL_LOCKS='0')
required = {
    'protocol-processor': '93fb0b2d736b36588ea7321e25fba2f8819ea41f',
    'gptp-processor': '55680bff3b287b9a7b0c759f51471fa617c17335',
    'third_party/lwSRP': '08ee86e812a0eb5e1dc6cd61b494d8baf3491348',
    'third_party/tsn-c-stack': '70936b77dc41981e192438388cd0aced69954f18',
    'third_party/verilog-axis': '48ff7a7e2ef782cf778d47910cf85835c64b1bce',
}

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=ENV)

def check(repo, expected):
    actual = git(repo, 'rev-parse', 'HEAD').decode().strip()
    assert actual == expected, actual
    entries = {}
    for row in git(repo, 'ls-tree', '-rz', 'HEAD').split(b'\0'):
        if not row:
            continue
        header, path = row.split(b'\t', 1)
        mode, kind, oid = header.split()
        entries[path] = (mode, oid)
        if kind == b'commit':
            continue
        file = repo / os.fsdecode(path)
        st = file.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), path
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(st.st_mode), path
            actual_mode = b'100755' if st.st_mode & 0o111 else b'100644'
            assert mode == actual_mode, path
            data = file.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert digest == oid, path
    index = {}
    for row in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if row:
            header, path = row.split(b'\t', 1)
            mode, oid, stage = header.split()
            assert stage == b'0', path
            index[path] = (mode, oid)
    assert index == entries, 'index differs from HEAD tree'
    status = git(repo, 'status', '--porcelain=v1', '--untracked-files=normal').decode()
    assert not status, status
    return {'head': actual, 'tree': git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip(), 'tracked_entries': len(entries), 'bytes_modes_index_match': True, 'status': 'clean'}

out = {'root': check(REPO, '417ec52864efc09f1e3ecd0f755cb0daa7604426'), 'required_submodules': {}}
assert out['root']['tree'] == 'aea3f763c8a6eea72a5f9bb8dec0bfe5af13b268'
for name, oid in required.items():
    link = git(REPO, 'ls-tree', 'HEAD', name).decode().split()
    assert link[:3] == ['160000', 'commit', oid], name
    out['required_submodules'][name] = check(REPO / name, oid)
out['external_submodule'] = {'status': 'uninitialized, not required by the focused checks', 'gitlink': git(REPO, 'ls-tree', 'HEAD', 'external').decode().strip()}
(ROOT / 'checkout-verification.json').write_text(json.dumps(out, indent=2) + '\n')
print('PASS: exact root head/tree, all tracked blob bytes and modes, index, required submodule heads and contents; clean checkout.')
