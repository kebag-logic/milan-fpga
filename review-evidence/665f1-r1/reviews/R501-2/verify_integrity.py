#!/usr/bin/env python3
"""Compare tracked bytes, modes, index and required submodules with exact Git trees."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

HEAD = '7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11'
TREE = '86236b61ec36ed252d6f91d698f2784302ef3743'
BASE = 'fa450d301805881ad713b67521477bf042ddadfd'
DEV = '510fae60b26bef1db138de5cf2ac72b17b5011a5'
REQUIRED = ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis')


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def entries(repo, rev):
    out = {}
    for line in git(repo, 'ls-tree', '-rz', rev).split(b'\0'):
        if line:
            info, name = line.split(b'\t', 1)
            mode, kind, oid = info.split()
            out[os.fsdecode(name)] = (mode.decode(), kind.decode(), oid.decode())
    return out


def check(repo, rev, label):
    expected = entries(repo, rev)
    index = {}
    for line in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if line:
            info, name = line.split(b'\t', 1)
            mode, oid, stage = info.split()
            assert stage == b'0', (label, os.fsdecode(name), 'unmerged')
            index[os.fsdecode(name)] = (mode.decode(), oid.decode())
    assert index == {name: (v[0], v[2]) for name, v in expected.items()}, label + ' index differs'
    blobs = 0
    for name, (mode, kind, oid) in expected.items():
        if kind != 'blob':
            continue
        path = repo / name
        actual_mode = path.lstat().st_mode
        if mode == '120000':
            assert stat.S_ISLNK(actual_mode), (label, name, 'not symlink')
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(actual_mode), (label, name, 'not regular')
            assert bool(actual_mode & 0o111) == (mode == '100755'), (label, name, 'mode differs')
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest == oid, (label, name, 'bytes differ')
        blobs += 1
    print(label, 'blobs=' + str(blobs), 'index_entries=' + str(len(index)), 'bytes_modes_index=PASS')
    return expected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo', type=Path, nargs='?', default=Path.cwd())
    args = ap.parse_args()
    repo = args.repo.resolve()
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == HEAD
    assert git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    print('HEAD', HEAD, 'TREE', TREE)
    top = check(repo, HEAD, 'superproject')
    for name in REQUIRED:
        mode, kind, pin = top[name]
        assert mode == '160000' and kind == 'commit'
        sub = repo / name
        assert (sub / '.git').is_file(), name + ' not initialized submodule'
        assert git(sub, 'rev-parse', 'HEAD').decode().strip() == pin, name + ' wrong pin'
        check(sub, pin, name)
        print('PIN', name, pin)
    print('ALL_GITLINKS', json.dumps({n: v[2] for n, v in top.items() if v[1] == 'commit'}, sort_keys=True))
    parent = entries(repo, HEAD + '^1')
    lane = {n for n in top if n.startswith('sw/firmware/ctrl_nvm/') or n == 'docs/README.md'}
    assert all(top[n] == parent[n] for n in lane)
    imported = git(repo, 'diff', '--name-only', '-z', HEAD + '^1', HEAD).split(b'\0')
    devtree = entries(repo, DEV)
    assert all(top.get(os.fsdecode(n)) == devtree.get(os.fsdecode(n)) for n in imported if n)
    assert git(repo, 'rev-parse', HEAD + '^2').decode().strip() == DEV
    base = entries(repo, BASE)
    shipping = 'sw/firmware/milan_baremetal/milan_baremetal.c'
    assert top[shipping] == base[shipping]
    print('MERGE lane_entries_unchanged=' + str(len(lane)),
          'imported_paths_equal_dev=' + str(len([n for n in imported if n])), 'shipping_writer_unchanged=PASS')
    print('LANE_DELTA', git(repo, 'diff', '--stat', DEV, HEAD).decode())
    assert not git(repo, 'status', '--porcelain'), 'checkout status dirty'
    assert not git(repo, 'ls-files', '--others', '--ignored', '--exclude-standard'), 'ignored artifacts remain'
    print('STATUS clean; no ignored artifacts; no source restoration needed')


if __name__ == '__main__':
    main()
