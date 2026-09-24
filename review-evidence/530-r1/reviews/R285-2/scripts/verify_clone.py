#!/usr/bin/env python3
"""Verify a review clone is exactly at its head: HEAD, tree, index, tracked
file bytes and modes, hide flags, untracked/ignored leftovers and gitlinks.

Usage: verify_clone.py <clone> <expected-head> <expected-tree>
Exit 0 only if every check is clean.
"""
import hashlib
import os
import stat
import subprocess
import sys


def git(repo, *args, env=None):
    e = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
    if env:
        e.update(env)
    return subprocess.run(['git', '-C', repo, *args], check=True,
                          capture_output=True, env=e).stdout


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def main():
    repo, head, tree = sys.argv[1:4]
    bad = []
    h = git(repo, 'rev-parse', 'HEAD').decode().strip()
    t = git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip()
    print(f'HEAD {h} {"OK" if h == head else "MISMATCH"}')
    print(f'tree {t} {"OK" if t == tree else "MISMATCH"}')
    if h != head or t != tree:
        bad.append('head/tree')
    idx_tree = git(repo, 'write-tree').decode().strip()
    print(f'index write-tree {idx_tree} {"OK" if idx_tree == tree else "MISMATCH"}')
    if idx_tree != tree:
        bad.append('index')
    hidden = [l for l in git(repo, 'ls-files', '-v').decode().splitlines()
              if l[:1] != 'H']
    print(f'hide/skip flags set: {len(hidden)}')
    if hidden:
        bad.append('flags')
    n = 0
    for rec in git(repo, 'ls-tree', '-r', '-z', 'HEAD').split(b'\0'):
        if not rec:
            continue
        meta, path = rec.split(b'\t', 1)
        mode, typ, oid = meta.decode().split()
        p = os.path.join(repo, path.decode())
        if typ == 'commit':
            sub = git(p, 'rev-parse', 'HEAD').decode().strip() if os.path.exists(os.path.join(p, '.git')) else None
            state = 'uninitialised' if sub is None else ('OK' if sub == oid else f'MISMATCH {sub}')
            if sub is not None:
                dirty = git(p, 'status', '--porcelain', '--ignored').decode().strip()
                state += ' clean' if not dirty else ' DIRTY'
                if dirty or sub != oid:
                    bad.append(path.decode())
            print(f'gitlink {path.decode()} {oid} {state}')
            continue
        n += 1
        st = os.lstat(p)
        if mode == '120000':
            data = os.readlink(p).encode()
            ok_mode = stat.S_ISLNK(st.st_mode)
        else:
            data = open(p, 'rb').read()
            exe = bool(st.st_mode & 0o100)
            ok_mode = stat.S_ISREG(st.st_mode) and (exe == (mode == '100755'))
        if blob_id(data) != oid or not ok_mode:
            bad.append(path.decode())
            print(f'MISMATCH {path.decode()}')
    print(f'tracked files checked: {n}')
    leftovers = git(repo, 'status', '--porcelain', '--ignored', '--untracked-files=all').decode().strip()
    print(f'untracked/ignored leftovers: {len(leftovers.splitlines()) if leftovers else 0}')
    if leftovers:
        print(leftovers)
        bad.append('leftovers')
    print('RESULT:', 'CLEAN' if not bad else f'NOT CLEAN {bad[:10]}')
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
