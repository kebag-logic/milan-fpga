#!/usr/bin/env python3
"""Verify tracked bytes, executable modes, index, and every required initialized gitlink."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
HEAD = '25ff0632c4ed312d57cad78783474308c92dd21f'
TREE = 'a5fa7c04b11c14c919f821f0075888a0633532c9'
os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'
def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
assert git(root, 'rev-parse', 'HEAD').decode().strip() == HEAD
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
audits = []
def audit(repo, label, expected):
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == expected
    tree = {}
    for entry in git(repo, 'ls-tree', '-r', '-z', 'HEAD').split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        tree[name] = (mode, oid)
    index = {}
    for entry in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0' and name not in index
        index[name] = (mode, oid)
    assert index == tree, label + ': index differs'
    blobs, links = 0, []
    digest = hashlib.sha256()
    for raw_name, (mode, oid) in sorted(tree.items()):
        path = repo / os.fsdecode(raw_name)
        if mode == '160000':
            initialized = (path / '.git').exists()
            links.append({'path': os.fsdecode(raw_name), 'gitlink': oid, 'initialized': initialized})
            if initialized:
                audit(path, label + '/' + os.fsdecode(raw_name), oid)
            else:
                assert label == '.' and os.fsdecode(raw_name) == 'external'
            continue
        st = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode)
            actual_mode = '100755' if st.st_mode & 0o111 else '100644'
            assert actual_mode == mode, str(path) + ': mode'
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, str(path) + ': blob'
        digest.update(raw_name + b'\0' + mode.encode() + b'\0' + oid.encode() + b'\n')
        blobs += 1
    audits.append({'repository': label, 'head': expected, 'tracked_blobs_verified': blobs,
                   'blob_inventory_sha256': digest.hexdigest(), 'index_matches_tree': True,
                   'gitlinks': links, 'status_porcelain': git(repo, 'status', '--porcelain=v1').decode()})
audit(root, '.', HEAD)
print(json.dumps({'head': HEAD, 'tree': TREE, 'result': 'PASS', 'repositories': audits}, indent=2))
