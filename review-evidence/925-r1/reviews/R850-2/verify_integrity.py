#!/usr/bin/env python3
"""Check actual tracked bytes, modes, index and submodule gitlinks without index shortcuts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
a = p.parse_args()
errors = []
required = {'protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/lwSRP', 'third_party/tsn-c-stack'}
def git(root, *args):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(root), *args])
def verify(root, revision):
    entries = git(root, 'ls-tree', '-rz', revision).split(b'\0')
    expected_index = []
    count = 0
    submodules = []
    for entry in entries:
        if not entry:
            continue
        meta, raw_path = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        path = os.fsdecode(raw_path)
        expected_index.append(mode + b' ' + oid + b' 0\t' + raw_path)
        target = root / path
        if kind == b'commit':
            if path in required:
                actual = git(target, 'rev-parse', 'HEAD').strip()
                if actual != oid:
                    errors.append(path + ': gitlink mismatch')
                if not (target / '.git').is_file():
                    errors.append(path + ': not an initialized submodule')
                submodules.append(verify(target, oid.decode()))
            continue
        count += 1
        st = target.lstat()
        if mode == b'120000':
            valid_mode = stat.S_ISLNK(st.st_mode)
            data = os.fsencode(os.readlink(target))
        else:
            valid_mode = stat.S_ISREG(st.st_mode) and bool(st.st_mode & 0o111) == (mode == b'100755')
            data = target.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if not valid_mode or blob != oid.decode():
            errors.append(path + ': tracked bytes or mode differ')
    actual_index = git(root, 'ls-files', '--stage', '-z').split(b'\0')
    if sorted(x for x in actual_index if x) != sorted(expected_index):
        errors.append(root.name + ': index differs')
    return {'repository': root.name, 'revision': revision, 'tracked_blobs_checked': count, 'submodules': submodules}

head = git(a.repo, 'rev-parse', 'HEAD').decode().strip()
tree = git(a.repo, 'rev-parse', 'HEAD^{tree}').decode().strip()
assert head == '5f625090bbd09a67f01080aeaa1f05e9d9a79cdd'
assert tree == '84cd6032a8efac1563ae09d11a40ba206674373c'
report = verify(a.repo, head)
report.update(tree=tree, errors=errors, passed=not errors)
print(json.dumps(report, indent=2))
raise SystemExit(bool(errors))
