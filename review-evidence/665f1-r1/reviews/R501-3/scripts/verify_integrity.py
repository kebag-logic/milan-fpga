#!/usr/bin/env python3
"""Prove tracked bytes, file kinds, executable modes, indexes and gitlinks.

Usage: python3 scripts/verify_integrity.py /path/to/exact-checkout
Git replacements and optional index locking are disabled for every read.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = '9412006bd58c002835bb06d46045c53098cc59a5'
TREE = 'ba76ab7618f8d97c681d0e33f7b2d2128c6169aa'
BASE = 'fa450d301805881ad713b67521477bf042ddadfd'
DEV = '28f9666feab2b2ba287643c63ed3a16b1e0bb863'
REQUIRED = ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis']
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', GIT_OPTIONAL_LOCKS='0')


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=ENV)


def entries(repo, revision):
    out = {}
    for item in git(repo, 'ls-tree', '-rz', revision).split(b'\0'):
        if item:
            meta, path = item.split(b'\t', 1)
            mode, kind, oid = meta.split()
            out[os.fsdecode(path)] = (mode.decode(), kind.decode(), oid.decode())
    return out


def check(repo, revision, label):
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == revision
    want = entries(repo, revision)
    index = {}
    for item in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if item:
            meta, path = item.split(b'\t', 1)
            mode, oid, stage = meta.split()
            assert stage == b'0', (label, 'unmerged index')
            key = os.fsdecode(path)
            assert key not in index
            index[key] = (mode.decode(), oid.decode())
    assert index == {k: (v[0], v[2]) for k, v in want.items()}, (label, 'index differs')
    blobs = 0
    for name, (mode, kind, oid) in want.items():
        if kind == 'commit':
            assert mode == '160000'
            continue
        path = repo / name
        st = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), (label, name, 'kind')
            assert ('100755' if st.st_mode & 0o111 else '100644') == mode, (label, name, 'mode')
            data = path.read_bytes()
        got = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert got == oid, (label, name, 'bytes')
        blobs += 1
    print(json.dumps({'checkout': label, 'head': revision, 'blobs': blobs,
                      'index': 'MATCH', 'bytes_modes_kinds': 'MATCH',
                      'gitlinks': {k: v[2] for k, v in want.items() if v[1] == 'commit'}}))
    return want


def main():
    repo = Path(sys.argv[1]).resolve()
    assert git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    top = check(repo, HEAD, 'superproject')
    for name in REQUIRED:
        path = repo / name
        assert not path.is_symlink() and (path / '.git').is_file(), (name, 'not an initialized gitlink')
        superproject = git(path, 'rev-parse', '--show-superproject-working-tree').decode().strip()
        assert Path(superproject).resolve() == repo
        check(path, top[name][2], name)
    live = entries(repo, DEV)
    before = entries(repo, BASE)
    imported = [p for p in set(live) | set(before) if live.get(p) != before.get(p)]
    lane = [p for p in set(live) | set(top) if live.get(p) != top.get(p)]
    overlap = sorted(set(imported) & set(lane))
    assert overlap == ['docs/design/SAVED_STATE_FASTCONNECT.md']
    assert all(top.get(p) == live.get(p) for p in imported if p not in overlap)
    assert all(p.startswith('sw/firmware/ctrl_nvm/') or p in
               ['docs/README.md', 'docs/design/SAVED_STATE_FASTCONNECT.md'] for p in lane)
    assert top['sw/firmware/milan_baremetal/milan_baremetal.c'] == before['sw/firmware/milan_baremetal/milan_baremetal.c']
    print(json.dumps({'source_base': BASE, 'integrated_dev': DEV, 'lane_paths': len(lane),
                      'inherited_paths': len(imported), 'authority_page_overlap': overlap,
                      'other_imported_entries': 'EXACT dev entries', 'shipping_writer': 'UNCHANGED'}))
    for label, path in [('superproject', repo)] + [(name, repo / name) for name in REQUIRED]:
        status = git(path, 'status', '--porcelain=v1', '--untracked-files=all').decode()
        ignored = git(path, 'ls-files', '--others', '--ignored', '--exclude-standard').decode()
        print(json.dumps({'checkout': label, 'status': status, 'ignored_files': ignored.splitlines()}))
        assert not status and not ignored, (label, 'residue')
    print('PASS: exact tracked bytes, modes, index, required gitlinks, scope and clean checkout')
    return 0


if __name__ == '__main__':
    sys.exit(main())
