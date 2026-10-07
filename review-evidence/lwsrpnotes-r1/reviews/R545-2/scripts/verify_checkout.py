#!/usr/bin/env python3
"""Verify every tracked byte, executable mode, index entry, and gitlink."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, default=Path.cwd())
args = parser.parse_args()
root = args.repo.resolve()
def git(*args):
    return subprocess.check_output(['git', *args], cwd=root)

head = 'f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152'
base = 'a4cbe41de1c80d43f26e0d348cbdb45075273a4f'
previous = 'ced667d8ee35929ab5f9e77a1c5396e173a693d8'
assert git('rev-parse', 'HEAD').decode().strip() == head
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == 'e7c4cf6a8fb382e5260f5fc9674c21c286289841'
assert subprocess.run(['git', 'symbolic-ref', '-q', 'HEAD'], cwd=root, stdout=subprocess.DEVNULL).returncode == 1
index = {}
for item in git('ls-files', '--stage', '-z').split(b'\0'):
    if not item:
        continue
    metadata, name = item.split(b'\t')
    mode, sha, stage = metadata.decode().split()
    assert stage == '0'
    index[name.decode()] = (mode, sha)
records = []
gitlinks = []
for item in git('ls-tree', '-rz', head).split(b'\0'):
    if not item:
        continue
    metadata, name = item.split(b'\t')
    mode, kind, sha = metadata.decode().split()
    name = name.decode()
    assert index.pop(name) == (mode, sha), ('index', name)
    path = root / name
    if mode == '160000':
        assert git('-C', str(path), 'rev-parse', 'HEAD').decode().strip() == sha
        gitlinks.append({'path': name, 'sha': sha})
        continue
    content = os.readlink(path).encode() if mode == '120000' else path.read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
    assert actual == sha, ('bytes', name)
    if mode != '120000':
        assert bool(path.stat().st_mode & 0o111) == (mode == '100755'), ('mode', name)
    records.append({'path': name, 'mode': mode, 'git_blob': sha,
                    'sha256': hashlib.sha256(content).hexdigest()})
assert not index
assert not git('status', '--porcelain=v1', '--untracked-files=all').strip()
assert not git('diff', base, head, '--', 'src').strip()
delta = git('diff', '--name-only', previous, head).decode().splitlines()
assert delta == ['doc/manager.md', 'doc/tester.md']
assert git('rev-parse', 'HEAD^').decode().strip() == previous
print(json.dumps({'head': head, 'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
                  'detached': True, 'clean_worktree_and_index': True,
                  'source_equal_to_base': True, 'round_2_changed_files': delta,
                  'tracked_blob_count': len(records), 'gitlinks': gitlinks,
                  'tracked_files': records}, indent=2))
