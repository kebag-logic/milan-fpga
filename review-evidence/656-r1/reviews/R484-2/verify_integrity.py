#!/usr/bin/env python3
"""Verify tree/index/bytes/modes independently of index trust flags.

Usage: python3 verify_integrity.py CHECKOUT
No tracked or index writes. Uninitialized optional external gitlink is reported.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = 'd0e29f6dda6f04f3ace1dbb395f57379e58cacaf'
TREE = '289f09d8c7151617ffb019f49b5c972924e4fedd'
PINS = {
    'gptp-processor': '5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d',
    'protocol-processor': '631eeb342ca1e3fa80e734077a56a943aee76ff1',
    'third_party/verilog-axis': '48ff7a7e2ef782cf778d47910cf85835c64b1bce',
}
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=ENV)


def verify(root, revision):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == revision
    tree = {}
    for record in git(root, 'ls-tree', '-rz', revision).split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        tree[path] = (mode, oid)
    index = {}
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0' and path not in index, 'Non-stage-0 or duplicate entry'
        index[path] = (mode, oid)
    assert tree == index, 'Index entries differ from the reviewed tree'
    blobs = 0
    links = {}
    for path, (mode, oid) in tree.items():
        name = os.fsdecode(path)
        if mode == '160000':
            links[name] = oid
            continue
        file = root / name
        info = file.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(info.st_mode), name
            actual_mode = '100755' if info.st_mode & 0o111 else '100644'
            assert actual_mode == mode, name
            data = file.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, name
        blobs += 1
    untracked = git(root, 'ls-files', '--others', '--exclude-standard', '-z')
    ignored = git(root, 'ls-files', '--others', '--ignored', '--exclude-standard', '-z')
    assert not untracked and not ignored, 'Unexpected untracked or ignored paths'
    return {'revision': revision, 'index_entries': len(index),
            'verified_blob_bytes_and_modes': blobs, 'gitlinks': links,
            'untracked_paths': 0, 'ignored_paths': 0, 'result': 'PASS'}


def main():
    root = Path(sys.argv[1]).resolve()
    assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    result = {'superproject': verify(root, HEAD), 'required_submodules': {}}
    for name, pin in PINS.items():
        assert result['superproject']['gitlinks'][name] == pin
        assert (root / name / '.git').is_file(), 'Required submodule is not registered'
        superproject = git(root / name, 'rev-parse', '--show-superproject-working-tree').decode().strip()
        assert Path(superproject).resolve() == root
        result['required_submodules'][name] = verify(root / name, pin)
    result['optional_external'] = 'Uninitialized on arrival; not needed or executed in this delta review'
    result['tree'] = TREE
    result['result'] = 'PASS'
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
