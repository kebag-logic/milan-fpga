#!/usr/bin/env python3
"""Verify worktree bytes, modes, indexes and required submodules against exact commits."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

OUT = Path(__file__).resolve().parent
HEAD = '4461d77ca34ec1203321821a3313071ff1923984'
os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def verify(root, commit):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == commit
    records = git(root, 'ls-tree', '-rz', commit).split(b'\0')
    expected_index, blobs, links = [], 0, {}
    for record in filter(None, records):
        info, name = record.split(b'\t', 1)
        mode, kind, oid = info.split()
        expected_index.append(mode + b' ' + oid + b' 0\t' + name + b'\0')
        path = root / os.fsdecode(name)
        if kind == b'commit':
            links[os.fsdecode(name)] = oid.decode()
            continue
        meta = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(meta.st_mode), str(path)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(meta.st_mode), str(path)
            assert bool(meta.st_mode & 0o111) == (mode == b'100755'), str(path)
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid.decode(), os.fsdecode(name)
        blobs += 1
    assert b''.join(sorted(expected_index)) == b''.join(sorted(
        x + b'\0' for x in git(root, 'ls-files', '--stage', '-z').split(b'\0') if x))
    return {'commit': commit, 'blobs': blobs, 'gitlinks': links, 'bytes_modes_index': 'PASS'}

root = Path.cwd()
parent = verify(root, HEAD)
submodules = {}
for name in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
             'third_party/tsn-c-stack', 'third_party/lwSRP'):
    path = root / name
    assert not path.is_symlink() and (path / '.git').is_file()
    submodules[name] = verify(path, parent['gitlinks'][name])
result = {'parent': parent, 'submodules': submodules,
          'tree': git(root, 'rev-parse', 'HEAD^{tree}').decode().strip(),
          'status': git(root, 'status', '--porcelain=v1').decode(),
          'external': 'Optional checkout not initialized; parent gitlink and index verified.'}
assert result['tree'] == '13f3c4bb69da311a9d3a30849348c4358e9bb28d'
assert not result['status']
(OUT / 'checkout-integrity.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS:', parent['blobs'], 'parent blobs;', sum(s['blobs'] for s in submodules.values()),
      'submodule blobs; bytes, modes, exact indexes, HEADs and gitlinks unchanged')
