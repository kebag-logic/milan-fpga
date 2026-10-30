#!/usr/bin/env python3
"""Verify exact tracked bytes, modes, index and gitlinks without changing source."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
head = git('rev-parse', 'HEAD').decode().strip()
tree = git('rev-parse', 'HEAD^{tree}').decode().strip()
assert head == '806957b35c3c23a36505744d205f9692720d19e2'
assert tree == 'a3920c96afb9a4917515d337514de26ced4857b3'
records, gitlinks = [], []
for entry in git('ls-tree', '-rz', 'HEAD').split(b'\0'):
    if not entry:
        continue
    meta, path = entry.split(b'\t', 1)
    mode, kind, oid = meta.decode().split()
    path = path.decode()
    if mode == '160000':
        gitlinks.append(dict(path=path, oid=oid))
        continue
    data = (repo / path).read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    actual_mode = '100755' if os.stat(repo / path).st_mode & stat.S_IXUSR else '100644'
    assert actual == oid and actual_mode == mode, path
    records.append(dict(path=path, blob=oid, mode=mode))
assert not gitlinks, 'This source repository is expected to have no nested gitlinks'
assert git('diff', '--cached', '--name-only') == b''
assert git('status', '--porcelain') == b''
delta = {}
for base in ['135afd04', '86073476']:
    delta[base] = git('diff', '--name-only', base, 'HEAD', '--',
                     'hdl', 'tb', 'bench', 'syn', 'Makefile').decode().splitlines()
assert delta['86073476'] == []
assert all(path.endswith('README.md') for path in delta['135afd04'])
result = dict(head=head, tree=tree, tracked_count=len(records), gitlinks=gitlinks,
              index_matches=True, status_clean=True, implementation_delta=delta, files=records)
(packet / 'integrity.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k:v for k,v in result.items() if k != 'files'}, indent=2))
