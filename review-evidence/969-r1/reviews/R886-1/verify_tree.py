#!/usr/bin/env python3
"""Read-only byte/mode/index/gitlink verification: CHECKOUT [EXPECTED_HEAD]."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
expected = sys.argv[2] if len(sys.argv) > 2 else 'f863258d2a455697d85a5ab48813be8f0783e2d4'
pins = {
    'gptp-processor': '1616fc8f062fbf58c35ad31674b5b233207bbdb8',
    'protocol-processor': '801ef2283ec793e35a2590fc6593c90313a64041',
    'third_party/lwSRP': '08ee86e812a0eb5e1dc6cd61b494d8baf3491348',
    'third_party/tsn-c-stack': '715589c1db7cf67e2f3259fd7083ebc7f0923376',
    'third_party/verilog-axis': '48ff7a7e2ef782cf778d47910cf85835c64b1bce',
}
errors = []
def git(path, *args):
    return subprocess.check_output(['git', '-C', str(path), *args])

def check(path, want):
    head = git(path, 'rev-parse', 'HEAD').decode().strip()
    tree = git(path, 'rev-parse', 'HEAD^{tree}').decode().strip()
    if head != want:
        errors.append(f'{path}: wrong HEAD {head}')
    entries = {}
    checked = 0
    links = {}
    for record in git(path, 'ls-tree', '-rz', 'HEAD').split(b'\0'):
        if not record:
            continue
        info, name = record.split(b'\t', 1)
        mode, kind, oid = info.decode().split()
        name = os.fsdecode(name)
        entries[name] = (mode, oid)
        if kind == 'commit':
            links[name] = oid
            continue
        p = path / name
        try:
            st = p.lstat()
            if stat.S_ISLNK(st.st_mode):
                actual_mode = '120000'
                data = os.fsencode(os.readlink(p))
            else:
                actual_mode = '100755' if st.st_mode & 0o111 else '100644'
                data = p.read_bytes()
            actual_oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            if (actual_mode, actual_oid) != (mode, oid):
                errors.append(f'{path.name}/{name}: bytes or mode differ')
            checked += 1
        except OSError as exc:
            errors.append(f'{path.name}/{name}: {exc}')
    index = {}
    for record in git(path, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        info, name = record.split(b'\t', 1)
        mode, oid, stage = info.decode().split()
        if stage != '0':
            errors.append(f'{path.name}: nonzero index stage')
        index[os.fsdecode(name)] = (mode, oid)
    if index != entries:
        errors.append(f'{path.name}: index differs from HEAD tree')
    return {'head': head, 'tree': tree, 'checked_blobs': checked, 'index_matches': index == entries, 'gitlinks': links}

result = {'root': check(root, expected), 'required_submodules': {}}
for name, oid in pins.items():
    if result['root']['gitlinks'].get(name) != oid:
        errors.append(f'{name}: wrong parent gitlink')
    result['required_submodules'][name] = check(root / name, oid)
result['uninitialized_external'] = 'Parent gitlink checked; contents not required or initialized.'
result['errors'] = errors
result['result'] = 'FAIL' if errors else 'PASS'
print(json.dumps(result, indent=2))
sys.exit(bool(errors))
