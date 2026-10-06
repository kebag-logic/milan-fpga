#!/usr/bin/env python3
"""Read raw tracked bytes/modes and compare index records with immutable trees."""
import argparse
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path

HEAD = '6c94e9f5f496ac25f8c4e31f9e3685c725de29f3'
TREE = '25b32c793bd4bb6d959640094a44fb2b5c9d7a45'
REQUIRED = {
    'protocol-processor': 'ead8036035affd53ef4b29979190f2f4f67084c0',
    'gptp-processor': '5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d',
    'third_party/verilog-axis': '48ff7a7e2ef782cf778d47910cf85835c64b1bce',
}


def git(root, *args):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(root), *args],
                                   env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'})


def verify(root, revision):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == revision
    tree_records = {}
    for raw in git(root, 'ls-tree', '-r', '-z', revision).split(b'\0'):
        if raw:
            meta, name = raw.split(b'\t', 1)
            mode, kind, oid = meta.decode().split()
            tree_records[os.fsdecode(name)] = (mode, kind, oid)
    index_records = {}
    for raw in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if raw:
            meta, name = raw.split(b'\t', 1)
            mode, oid, stage = meta.decode().split()
            name = os.fsdecode(name)
            assert stage == '0' and name not in index_records
            index_records[name] = (mode, oid)
    assert index_records == {name: (mode, oid) for name, (mode, kind, oid) in tree_records.items()}
    raw_proof = []
    gitlinks = {}
    for name, (mode, kind, oid) in tree_records.items():
        if kind == 'commit':
            gitlinks[name] = oid
            continue
        path = root / name
        for parent in path.parents:
            if parent == root:
                break
            assert not parent.is_symlink(), name
        st = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode), name
            content = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert mode == ('100755' if st.st_mode & 0o111 else '100644'), name
            content = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
        assert actual == oid, name
        raw_proof.append([name, mode, actual])
    return {'revision': revision, 'tree': git(root, 'rev-parse', revision + '^{tree}').decode().strip(),
            'tracked_blobs_verified': len(raw_proof), 'index': 'all stage-0 records equal tree',
            'byte_mode_inventory_sha256': hashlib.sha256(json.dumps(raw_proof, separators=(',', ':')).encode()).hexdigest(),
            'gitlinks': gitlinks, 'result': 'PASS'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repository', type=Path)
    args = ap.parse_args()
    root = args.repository.resolve()
    result = {'superproject': verify(root, HEAD), 'required_submodules': {}}
    assert result['superproject']['tree'] == TREE
    assert subprocess.run(['git', '-C', str(root), 'symbolic-ref', '-q', 'HEAD'], capture_output=True).returncode == 1
    for name, revision in REQUIRED.items():
        assert result['superproject']['gitlinks'][name] == revision
        sub = root / name
        assert not sub.is_symlink() and (sub / '.git').is_file()
        assert Path(git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip()).resolve() == root
        result['required_submodules'][name] = verify(sub, revision)
    result['status_porcelain'] = git(root, 'status', '--porcelain=v1', '--untracked-files=all').decode()
    assert result['status_porcelain'] == ''
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
