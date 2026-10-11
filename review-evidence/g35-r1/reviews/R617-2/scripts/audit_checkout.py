#!/usr/bin/env python3
"""Verify tracked bytes, executable modes, index entries and gitlinks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument('checkout', type=Path)
a = p.parse_args()
def git(*args):
    return subprocess.check_output(['git', '-C', str(a.checkout), *args])
head = 'a70e38804cb16435c089d024c58e8c3fb4d39ff6'
tree = 'e02031a9d589ad6dc0f9d005c762de610c737784'
assert git('rev-parse', 'HEAD').decode().strip() == head
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == tree
entries = {}
gitlinks = {}
for row in git('ls-tree', '-rz', head).split(b'\0'):
    if not row: continue
    info, name = row.split(b'\t', 1)
    mode, kind, sha = info.decode().split()
    name = os.fsdecode(name)
    entries[name] = (mode, sha)
    file = a.checkout / name
    if kind == 'commit':
        gitlinks[name] = sha
        actual = subprocess.check_output(['git', '-C', str(file), 'rev-parse', 'HEAD']).decode().strip()
        assert actual == sha, name
        continue
    if mode == '120000':
        assert file.is_symlink(), name
        data = os.fsencode(os.readlink(file))
    else:
        assert file.is_file() and not file.is_symlink(), name
        actual_mode = '100755' if file.stat().st_mode & stat.S_IXUSR else '100644'
        assert actual_mode == mode, (name, mode, actual_mode)
        data = file.read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert actual == sha, (name, sha, actual)
index = {}
for row in git('ls-files', '--stage', '-z').split(b'\0'):
    if not row: continue
    info, name = row.split(b'\t', 1)
    mode, sha, stage = info.decode().split()
    assert stage == '0'
    index[os.fsdecode(name)] = (mode, sha)
assert index == entries
assert not git('status', '--porcelain=v1', '--untracked-files=all').strip()
round1 = '5b4ce3974f7627d57b31167bde50cde8f4bdcdf3'
rtl = 'hdl/wire/KL_gptp_rx_parser.sv'
def code(revision):
    text = git('show', revision + ':' + rtl).decode()
    text = re.sub(r'/\*.*?\*/|//[^\n]*', '', text, flags=re.S)
    return re.sub(r'\s+', '', text).encode()
assert code(round1) == code(head)
roms = [n for n in entries if n.endswith('.hex')]
assert all(git('show', round1 + ':' + n) == git('show', head + ':' + n) for n in roms)
print(json.dumps({'result': 'PASS', 'head': head, 'tree': tree,
 'tracked_files_and_index_entries': len(entries), 'gitlinks': gitlinks,
 'status': 'clean; all tracked bytes, modes and index entries match HEAD',
 'round1_parser_code_equals_head_ignoring_comments_and_whitespace': True,
 'round1_parser_normalized_sha256': hashlib.sha256(code(head)).hexdigest(),
 'unchanged_tracked_hex_files': roms}, indent=2))
