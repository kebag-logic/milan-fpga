#!/usr/bin/env python3
"""Read-only exact-tree, merge provenance and scanned-inventory verification."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

HEAD = '80588cdc43ca5605a1d3748d13dd8ed7f22f7000'
TREE = 'e20b82dacbc2a3299f47c8e8444537f979d17029'

def main():
    p = argparse.ArgumentParser()
    p.add_argument('repo', type=Path)
    p.add_argument('--final', action='store_true')
    a = p.parse_args()
    def git(*args):
        return subprocess.check_output(['git', '-C', str(a.repo), *args])
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    assert git('rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    records = git('ls-tree', '-rz', HEAD).split(b'\0')
    failures, count, gitlinks = [], 0, []
    for record in records:
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = path.decode()
        if kind == 'commit':
            gitlinks.append([name, oid])
            continue
        f = a.repo / name
        raw = os.readlink(f).encode() if mode == '120000' else f.read_bytes()
        computed = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        actual_mode = '120000' if f.is_symlink() else ('100755' if f.stat().st_mode & 0o111 else '100644')
        if computed != oid or actual_mode != mode:
            failures.append(name)
        count += 1
    assert not failures, failures
    assert git('write-tree').decode().strip() == TREE
    assert not git('diff', '--raw', HEAD)
    print(json.dumps({'head': HEAD, 'tree': TREE, 'tracked_blobs_bytes_and_modes_verified': count,
                      'index_tree_matches': True, 'gitlinks': gitlinks,
                      'status': git('status', '--porcelain=v1').decode()}, indent=2))
    if a.final:
        return
    for commit in ['07b1469d', 'b0a74196', 'ead80360', '5b2199b', 'e219709', HEAD]:
        row = git('rev-list', '--parents', '-n', '1', commit).decode().split()
        assert len(row) == 3, row
        sha, left, right = row
        merged = git('merge-tree', '--write-tree', left, right).decode().strip()
        expected = git('rev-parse', commit + '^{tree}').decode().strip()
        assert merged == expected, (commit, merged, expected)
        print('CLEAN_REMERGE', sha, left, right, expected)
    def files(rev):
        return set(git('ls-tree', '-r', '--name-only', rev, '--', 'docs', 'hdl', 'tb').decode().splitlines())
    old, new = files('91cef52'), files(HEAD)
    premerge = files('3d5a201')
    added, removed = sorted(new - old), sorted(old - new)
    assert len(old) == 488 and len(new) == 531 and not removed
    assert premerge == old
    main_added = files('ead80360') - files('c050d971')
    assert set(added) == main_added
    print('SCAN_INVENTORY', json.dumps({'round1': len(old), 'premerge': len(premerge),
          'head': len(new), 'added': added, 'removed': removed,
          'extra_files_exactly_main_lane_additions': True}, indent=2))
    for sha in ['07b1469d','b0a74196','ead80360']:
        print('LANE_ADDITIONS', sha, sorted(files(sha) - files(sha+'^1')))

if __name__ == '__main__':
    main()
