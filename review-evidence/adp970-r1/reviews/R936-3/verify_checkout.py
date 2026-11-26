#!/usr/bin/env python3
"""Compare raw tracked bytes, kinds, modes, indexes and initialized gitlinks with pinned trees."""
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

repo, packet = (Path(p).resolve() for p in sys.argv[1:3])
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env)

HEAD = '701a980b32bf31636811ef831739c9bfd3d6f978'
TREE = '03e2a77c669704aa8b42207ff0e99163d925e304'
assert git(repo, 'rev-parse', 'HEAD').decode().strip() == HEAD
assert git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
records = []
def verify(root, commit, label):
    entries = {}
    for entry in git(root, 'ls-tree', '-rz', commit).split(b'\0'):
        if not entry:
            continue
        fields, name = entry.split(b'\t', 1)
        mode, kind, oid = fields.decode().split()
        entries[os.fsdecode(name)] = (mode, kind, oid)
    index = {}
    for entry in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not entry:
            continue
        fields, name = entry.split(b'\t', 1)
        mode, oid, stage = fields.decode().split()
        assert stage == '0', (label, name, stage)
        index[os.fsdecode(name)] = (mode, oid)
    assert index == {name: (mode, oid) for name, (mode, _, oid) in entries.items()}, label
    blobs = 0
    links = []
    for name, (mode, kind, oid) in entries.items():
        path = root / name
        if kind == 'commit':
            links.append(dict(path=name, commit=oid))
            if label == '.' and name == 'external':
                links[-1]['state'] = 'optional, uninitialized'
                continue
            assert path.is_dir() and not path.is_symlink(), name
            assert (path / '.git').exists(), name
            assert git(path, 'rev-parse', 'HEAD').decode().strip() == oid, name
            verify(path, oid, name)
            links[-1]['state'] = 'verified'
            continue
        s = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(s.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(s.st_mode), name
            assert bool(s.st_mode & 0o111) == (mode == '100755'), name
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest == oid, (label, name)
        blobs += 1
    records.append(dict(repository=label, commit=commit, tracked_entries=len(entries), blobs=blobs,
                        index='exact', bytes_and_modes='exact', gitlinks=links))
verify(repo, HEAD, '.')
report = dict(head=HEAD, tree=TREE, repositories=records,
              total_entries=sum(r['tracked_entries'] for r in records))
(packet / 'checkout-integrity.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
