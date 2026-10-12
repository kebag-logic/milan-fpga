#!/usr/bin/env python3
"""Prove worktree bytes/modes and index agree with HEAD, including initialized gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)

def inspect(where):
    """Hash actual file bytes without relying on index freshness flags."""
    head = git(where, 'rev-parse', 'HEAD').decode().strip()
    entries = []
    children = []
    counts = {}
    for record in git(where, 'ls-tree', '-rz', 'HEAD').split(b'\0'):
        if not record:
            continue
        meta, rawpath = record.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        path = os.fsdecode(rawpath)
        target = where / path
        counts[mode] = counts.get(mode, 0) + 1
        entries.append((mode, oid, path))
        if mode == '160000':
            initialized = (target / '.git').exists()
            child = dict(path=path, expected=oid, initialized=initialized)
            if initialized:
                child['verification'] = inspect(target)
                assert child['verification']['head'] == oid
            children.append(child)
            continue
        st = target.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode), path
            data = os.fsencode(os.readlink(target))
        else:
            assert stat.S_ISREG(st.st_mode), path
            actual_mode = '100755' if st.st_mode & 0o111 else '100644'
            assert actual_mode == mode, (path, mode, actual_mode)
            data = target.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest == oid, path
    index = []
    for record in git(where, 'ls-files', '-sz').split(b'\0'):
        if not record:
            continue
        meta, rawpath = record.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0'
        index.append((mode, oid, os.fsdecode(rawpath)))
    assert sorted(index) == sorted(entries), 'index differs from tree'
    flags = git(where, 'ls-files', '-v').decode().splitlines()
    assert all(line[0] not in 'Sabcdefghijklmnopqrstuvwxyz' for line in flags), 'hidden-index flags'
    status = git(where, 'status', '--porcelain=v1', '--untracked-files=all').decode()
    assert not status, status
    return dict(head=head, tree=git(where, 'rev-parse', 'HEAD^{tree}').decode().strip(),
                entries=len(entries), modes=counts, byte_mode_index_match=True,
                clean=True, gitlinks=children)

result = inspect(root)
assert result['head'] == 'e7d604faa0472d505d6459883b382c2b237ad06d'
assert result['tree'] == '641f45e32b484bb1da1d34379d5e19f0588f52b3'
base_links = {os.fsdecode(r.split(b'\t')[1]):r.split()[2].decode()
              for r in git(root, 'ls-tree', '-rz', 'c6bd08c6').split(b'\0') if r.startswith(b'160000 ')}
assert all(base_links[entry['path']] == entry['expected'] for entry in result['gitlinks'])
result['base_gitlinks_unchanged'] = True
print(json.dumps(result, indent=2))
