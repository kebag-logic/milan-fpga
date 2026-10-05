#!/usr/bin/env python3
"""Read-only exact tracked-byte, mode, index and required-gitlink verification."""
import argparse
import hashlib
import os
from pathlib import Path
import stat
import subprocess

HEAD = 'd0e29f6dda6f04f3ace1dbb395f57379e58cacaf'
TREE = '289f09d8c7151617ffb019f49b5c972924e4fedd'
REQUIRED = ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis')


def git(repo, *args):
    env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', GIT_OPTIONAL_LOCKS='0')
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)


def verify(repo, revision, label):
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == revision
    entries = {}
    for row in git(repo, 'ls-tree', '-rz', revision).split(b'\0'):
        if row:
            fields, path = row.split(b'\t', 1)
            mode, kind, oid = fields.split()
            entries[path] = (mode, oid)
    index = {}
    for row in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if row:
            fields, path = row.split(b'\t', 1)
            mode, oid, stage = fields.split()
            assert stage == b'0' and path not in index, (label, path, 'index stage')
            index[path] = (mode, oid)
    assert index == entries, (label, 'index differs from commit tree')
    count = 0
    links = {}
    for path, (mode, oid) in entries.items():
        target = repo / os.fsdecode(path)
        if mode == b'160000':
            links[os.fsdecode(path)] = oid.decode()
            continue
        info = target.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), (label, path, 'symlink type')
            raw = os.fsencode(os.readlink(target))
        else:
            assert stat.S_ISREG(info.st_mode), (label, path, 'regular type')
            expected_mode = b'100755' if info.st_mode & stat.S_IXUSR else b'100644'
            assert mode == expected_mode, (label, path, 'mode')
            raw = target.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert actual == oid.decode(), (label, path, 'blob bytes')
        count += 1
    hidden = [row for row in git(repo, 'ls-files', '-v', '-z').split(b'\0')
              if row and (row[:1].islower() or row[:1] == b'S')]
    assert not hidden, (label, 'hidden index flags')
    untracked = git(repo, 'ls-files', '--others', '--exclude-standard', '-z')
    assert not untracked, (label, 'untracked files')
    print(f'{label}: {count} tracked blobs match exact bytes and executable/symlink modes; index matches tree; hidden flags 0; untracked 0')
    return links


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    assert git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    assert subprocess.run(['git', '-C', str(repo), 'symbolic-ref', '-q', 'HEAD'],
                          stdout=subprocess.DEVNULL).returncode == 1
    print('HEAD:', HEAD)
    print('Tree:', TREE)
    print('Detached: yes')
    links = verify(repo, HEAD, 'review clone')
    for name in REQUIRED:
        pin = links[name]
        sub = repo / name
        assert not sub.is_symlink() and (sub / '.git').is_file()
        superproject = git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip()
        assert Path(superproject).resolve() == repo
        print(f'Required gitlink {name}: {pin}')
        verify(sub, pin, name)
    for name, pin in links.items():
        if name not in REQUIRED:
            print(f'Other gitlink {name}: {pin}; checkout metadata present={(repo / name / ".git").exists()}')
    assert not git(repo, 'status', '--porcelain=v1', '--untracked-files=all')
    print('PASS: exact-head clone integrity; no restoration needed.')


if __name__ == '__main__':
    main()
