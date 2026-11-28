#!/usr/bin/env python3
"""Prove tracked bytes, modes, index entries and required gitlinks against HEAD."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = Path.cwd()
EXPECTED = 'a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35'
REQUIRED = ['gptp-processor', 'protocol-processor', 'third_party/lwSRP',
    'third_party/tsn-c-stack', 'third_party/verilog-axis']

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def audit(root, expected):
    head = git(root, 'rev-parse', 'HEAD').decode().strip()
    assert head == expected, (str(root), head)
    entries = {}
    blobs = 0
    pins = {}
    for row in git(root, 'ls-tree', '-rz', 'HEAD').split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        entries[name] = (mode, oid)
        path = root / os.fsdecode(name)
        if kind == 'commit':
            pins[os.fsdecode(name)] = oid
            continue
        st = path.lstat()
        actual_mode = '120000' if stat.S_ISLNK(st.st_mode) else ('100755' if st.st_mode & 0o111 else '100644')
        assert actual_mode == mode, (str(path), actual_mode, mode)
        data = os.fsencode(os.readlink(path)) if stat.S_ISLNK(st.st_mode) else path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, str(path)
        blobs += 1
    index = {}
    for row in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0'
        index[name] = (mode, oid)
    assert index == entries, str(root)
    return {'head': head, 'tree': git(root, 'rev-parse', 'HEAD^{tree}').decode().strip(),
        'blobs_verified': blobs, 'index_matches': True, 'gitlinks': pins,
        'status': git(root, 'status', '--porcelain').decode()}

result = {'parent': audit(ROOT, EXPECTED), 'submodules': {}}
for name in REQUIRED:
    assert (ROOT / name / '.git').exists()
    result['submodules'][name] = audit(ROOT / name, result['parent']['gitlinks'][name])
assert result['parent']['tree'] == '222e3e20fa0f6313632775aabf4f74a26c4417fc'
assert all(not x['status'] for x in [result['parent'], *result['submodules'].values()])
(OUT / 'checkout-integrity.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS:', result['parent']['blobs_verified'], 'parent blobs;',
    sum(x['blobs_verified'] for x in result['submodules'].values()), 'submodule blobs; modes/index/gitlinks clean')
