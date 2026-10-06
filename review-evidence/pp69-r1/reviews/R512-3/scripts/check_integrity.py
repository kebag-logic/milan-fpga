#!/usr/bin/env python3
"""Verify physical tracked bytes, modes, index, detached head and gitlinks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--packet', type=Path, required=True)
a = ap.parse_args()
root = a.repo.resolve()
p = a.packet.resolve()


def git(*argv):
    return subprocess.check_output(['git', *argv], cwd=root)


head = git('rev-parse', 'HEAD').decode().strip()
tree = git('rev-parse', 'HEAD^{tree}').decode().strip()
expected = []
errors = []
gitlinks = []
for record in git('ls-tree', '-rz', 'HEAD').split(b'\0'):
    if not record:
        continue
    meta, raw_path = record.split(b'\t', 1)
    mode, kind, oid = meta.decode().split()
    rel = os.fsdecode(raw_path)
    f = root / rel
    if mode == '160000':
        gitlinks.append({'path': rel, 'oid': oid})
        continue
    s = f.lstat()
    actual_mode = '120000' if stat.S_ISLNK(s.st_mode) else ('100755' if s.st_mode & 0o111 else '100644')
    data = os.fsencode(os.readlink(f)) if stat.S_ISLNK(s.st_mode) else f.read_bytes()
    actual_oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    row = {'path': rel, 'mode': actual_mode, 'blob': actual_oid, 'sha256': hashlib.sha256(data).hexdigest()}
    expected.append(row)
    if actual_oid != oid or actual_mode != mode:
        errors.append(row)
index = git('ls-files', '--stage')
initial_index = (p / 'initial-index.txt').read_bytes()
(p / 'receipts/final-index.txt').write_bytes(index)
status = git('status', '--porcelain=v2').decode()
detached = subprocess.run(['git', 'symbolic-ref', '-q', 'HEAD'], cwd=root,
                          stdout=subprocess.DEVNULL).returncode == 1
submodules = git('submodule', 'status', '--recursive').decode()
result = {'head': head, 'tree': tree, 'detached': detached, 'tracked_blobs': len(expected),
          'index_entries': len(index.splitlines()), 'index_unchanged': index == initial_index,
          'status': status, 'gitlinks': gitlinks, 'submodule_status': submodules, 'mismatches': errors}
result['pass'] = (head == '669ded57b1fabc2bbf274b8ad05493c7593e0a0a' and
                  tree == '4bce83358cf24f551909ab46aeb19c5f93787106' and detached and
                  index == initial_index and not status and not errors and not gitlinks and not submodules)
(p / 'receipts/checkout-integrity.json').write_text(json.dumps(result, indent=2) + '\n')
(p / 'receipts/tracked-blob-inventory.json').write_text(json.dumps(expected, indent=2) + '\n')
print(json.dumps(result))
raise SystemExit(not result['pass'])
