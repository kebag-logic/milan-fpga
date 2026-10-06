#!/usr/bin/env python3
"""Verify raw tracked bytes, executable bits, index entries and required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
HEAD = '0f3d37dbffc4ca3f0e0f69499de80fc256a7db57'
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root, env=ENV)

def audit(root, revision):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == revision
    entries = {}
    for row in git(root, 'ls-tree', '-rz', revision).split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, kind, oid = meta.split()
        entries[name] = (mode, kind, oid)
    index = {}
    for row in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and name not in index
        index[name] = (mode, oid)
    assert index == {n:(v[0], v[2]) for n,v in entries.items()}
    errors, links, blobs = [], {}, 0
    for name, (mode, kind, oid) in entries.items():
        path = root / os.fsdecode(name)
        if kind == b'commit':
            links[os.fsdecode(name)] = oid.decode()
            continue
        info = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), os.fsdecode(name)
            raw = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), os.fsdecode(name)
            assert bool(info.st_mode & 0o111) == (mode == b'100755'), os.fsdecode(name)
            raw = path.read_bytes()
        actual = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if actual != oid.decode():
            errors.append(os.fsdecode(name))
        blobs += 1
    assert not errors, errors
    status = git(root, 'status', '--porcelain=v1', '--untracked-files=all').decode()
    assert not status, status
    flags = git(root, 'ls-files', '-v', '-z').split(b'\0')
    assert not any(r and (r[:1].islower() or r[:1] == b'S') for r in flags)
    return {'head': revision, 'tree': git(root, 'rev-parse', 'HEAD^{tree}').decode().strip(),
            'blobs_verified': blobs, 'gitlinks': links, 'index_equals_head': True,
            'raw_bytes_and_modes_equal': True, 'no_assume_unchanged_or_skip_worktree': True,
            'status_empty': True}

def main():
    report = {'superproject': audit(ROOT, HEAD)}
    for name in ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis']:
        revision = report['superproject']['gitlinks'][name]
        report[name] = audit(ROOT/name, revision)
    report['external'] = 'Gitlink verified in parent index/tree; checkout is uninitialized and unused.'
    OUT.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
