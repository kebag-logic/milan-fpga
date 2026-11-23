#!/usr/bin/env python3
"""Verify exact tracked bytes, modes, index entries and initialized gitlinks.
Usage: python3 verify_tree.py CHECKOUT OUTPUT_DIR
"""
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

checkout, output = map(lambda s: Path(s).resolve(), sys.argv[1:])
head = 'c113018d3cd4e70a7d3b66940a3a88fb93f0421a'
tree = '2a032e207225763bb455c62ba77ec39ed5f8b008'
required = ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
            'third_party/tsn-c-stack', 'third_party/lwSRP')

def git(root, *args):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(root), *args])

def verify(root, revision):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == revision
    entries = {}
    for record in git(root, 'ls-tree', '-rz', revision).split(b'\0'):
        if record:
            info, name = record.split(b'\t', 1)
            mode, kind, oid = info.decode().split()
            entries[os.fsdecode(name)] = (mode, kind, oid)
    indexed = {}
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if record:
            info, name = record.split(b'\t', 1)
            mode, oid, stage = info.decode().split()
            assert stage == '0', os.fsdecode(name)
            indexed[os.fsdecode(name)] = (mode, oid)
    assert indexed == {name: (mode, oid) for name, (mode, kind, oid) in entries.items()}
    count = 0
    links = {}
    for name, (mode, kind, oid) in entries.items():
        path = root / name
        if kind == 'commit':
            links[name] = oid
            continue
        st = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert ('100755' if st.st_mode & 0o111 else '100644') == mode, name
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest == oid, name
        count += 1
    return dict(head=revision, blobs=count, gitlinks=links, bytes_modes_index='PASS')

result = {'root': verify(checkout, head), 'submodules': {}}
assert git(checkout, 'rev-parse', 'HEAD^{tree}').decode().strip() == tree
result['tree'] = tree
detached = subprocess.run(['git', '-C', str(checkout), 'symbolic-ref', '-q', 'HEAD'], capture_output=True)
assert detached.returncode == 1 and not detached.stdout, 'HEAD is not detached'
for name in required:
    sub = checkout / name
    assert not sub.is_symlink()
    assert (sub / '.git').is_file(), name
    parent = git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip()
    assert Path(parent).resolve() == checkout, name
    result['submodules'][name] = verify(sub, result['root']['gitlinks'][name])
result['external'] = 'Unused external gitlink verified in root index; checkout intentionally uninitialized'
(output / 'tree-integrity.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
