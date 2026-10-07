#!/usr/bin/env python3
"""Read-only exact-source, licence, anchor and branch-history audit."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

source, fresh, official = map(lambda x: Path(x).resolve(), sys.argv[1:4])
HEAD = '4eba61b7b1c49fc9b7260a487240ca86f9d38168'
BASE = '1401654530ce7d9275de9b901e67df47e5bbc536'

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])

def tree(repo, rev):
    result = {}
    for entry in git(repo, 'ls-tree', '-rz', rev).split(b'\0'):
        if entry:
            meta, name = entry.split(b'\t', 1)
            mode, kind, oid = meta.decode().split()
            result[name.decode()] = (mode, kind, oid)
    return result

def blob(repo, oid):
    return git(repo, 'cat-file', 'blob', oid)

assert git(source, 'rev-parse', 'HEAD').decode().strip() == HEAD
assert git(source, 'rev-parse', 'HEAD^{tree}').decode().strip() == 'bf90243127da3e4d22eaeef1402542f1095ee263'
current, base = tree(source, HEAD), tree(source, BASE)
assert not git(source, 'status', '--porcelain=v1')
assert not git(source, 'diff', '--raw', HEAD)
index = git(source, 'ls-files', '--stage', '-z')
expected = b''.join(f'{mode} {oid} 0\t{name}\0'.encode() for name, (mode, kind, oid) in sorted(current.items()))
assert index == expected
for name, (mode, kind, oid) in current.items():
    if kind == 'blob':
        path = source / name
        assert path.read_bytes() == blob(source, oid), name
        assert bool(path.stat().st_mode & 0o111) == (mode == '100755'), name
print('Exact head:', HEAD)
print('Tracked bytes, modes, index and clean status: PASS')
print('Tracked files:', len(current))
print('Required gitlinks:', sum(v[1] == 'commit' for v in current.values()))
assert (source/'LICENSE').read_bytes() == official.read_bytes()
print('LICENSE official bytes: PASS; SHA256', hashlib.sha256(official.read_bytes()).hexdigest())
assert (source/'NOTICE').read_text() == 'lwSRP\nCopyright 2026 kebag-logic\n\nLicensed under the Apache License, Version 2.0.\n'
print('NOTICE: PASS')
headers = 0
for name, (mode, kind, oid) in current.items():
    if name in ('LICENSE', 'NOTICE'):
        continue
    data = blob(source, oid)
    lines = data.splitlines()
    suffix = Path(name).suffix
    expected_header = (b'/* SPDX-License-Identifier: Apache-2.0 */' if suffix in ('.c', '.h') else
                       b'<!-- SPDX-License-Identifier: Apache-2.0 -->' if suffix == '.md' else
                       b'# SPDX-License-Identifier: Apache-2.0')
    first = 1 if lines[0].startswith(b'#!') else 0
    assert lines[first] == expected_header, name
    assert data.count(b'SPDX-License-Identifier:') == 1, name
    headers += 1
    print('Header PASS', name)
print('Header total:', headers, '; canonical licence and notice exempt')
changed, executable, anchors, shifted = [], [], 0, 0
line_link = re.compile(rb'#L([0-9]+)(?:-L([0-9]+))?')
for name in sorted(set(base) | set(current)):
    if base.get(name) == current.get(name):
        continue
    changed.append(name)
    if name in ('LICENSE', 'NOTICE'):
        assert name not in base
        continue
    assert name in base and name in current
    assert base[name][:2] == current[name][:2]
    before, after = blob(source, base[name][2]), blob(source, current[name][2])
    if name.endswith('.md'):
        def normalized(data):
            return line_link.sub(b'#LINE', data)
        assert normalized(before) == normalized(after), name
        links = re.compile(rb'\]\(([^)]+)#L([0-9]+)(?:-L([0-9]+))?\)')
        oldlinks, newlinks = list(links.finditer(before)), list(links.finditer(after))
        assert len(oldlinks) == len(newlinks)
        for old, new in zip(oldlinks, newlinks):
            assert old[1] == new[1]
            target = (source / Path(name).parent / old[1].decode()).resolve().relative_to(source).as_posix()
            a, z = int(old[2]), int(old[3] or old[2])
            b, y = int(new[2]), int(new[3] or new[2])
            assert blob(source, base[target][2]).splitlines()[a-1:z] == blob(source, current[target][2]).splitlines()[b-1:y], (name, target, a, b)
            anchors += 1
            shifted += (a, z) != (b, y)
        print('Documentation prose/graphs preserved; anchor contents identical:', name, len(oldlinks))
    else:
        stripped = b''.join(line for line in after.splitlines(keepends=True) if b'SPDX-License-Identifier:' not in line)
        assert stripped == before, name
        executable.append(name)
print('Changed files:', len(changed), '; header-only executable/config/test files:', len(executable))
print('Source anchors with identical target content:', anchors)
print('Shifted ranges:', shifted, '; already-correct ranges:', anchors - shifted)
assert (source/'src/include/shish_lan/mrp.h').read_text().splitlines()[118].startswith('#define MRP_LEAVE_TIME_CS     60u')
assert b'MRP_APPL_STATE_LO' in (source/'src/core/mrp_mad.c').read_bytes().splitlines()[162]
assert b'.group_addr' in (source/'src/modules/msrp.c').read_bytes().splitlines()[353]
print('Focused Leave interval 119, LA 162-163, stream address 353-354: PASS')
print('HDL files:', sum(Path(n).suffix in ('.v', '.sv', '.vhd', '.vhdl') for n in current))
print('RTL-impact boundary: source, interfaces and build behavior preserved after header removal')

# Hex literals keep excluded identifiers out of the published script text.
terms = [bytes.fromhex(x) for x in (
    '636c61756465', '636f646578', '63686174677074', '677074', '6f70656e6169',
    '616e7468726f706963', '636f70696c6f74', '67656d696e69', '637572736f72',
    '646565707365656b', '6c6c616d61', '6d69737472616c', '6169646572',
    '636c696e65', '77696e6473757266', '7177656e', '67726f6b', '6f707573',
    '736f6e6e6574', '6861696b75')]
pattern = re.compile(rb'(?i)(?<![a-z0-9])(?:' + b'|'.join(terms) + rb')(?![a-z])')
removed = bytes.fromhex('434c415544452e6d64')
commits = git(fresh, 'rev-list', '--all').decode().splitlines()
blobs, path_hits, message_hits, content_hits = set(), [], [], []
author_ids = set()
for commit in commits:
    raw = git(fresh, 'cat-file', 'commit', commit)
    if pattern.search(raw):
        message_hits.append(commit)
    author_ids.add(next(x for x in raw.splitlines() if x.startswith(b'author ')).rsplit(b'>', 1)[0])
    for name, (mode, kind, oid) in tree(fresh, commit).items():
        if pattern.search(name.encode()) or Path(name).name.encode().lower() == removed.lower():
            path_hits.append((commit, hashlib.sha256(name.encode()).hexdigest()))
        if kind == 'blob':
            blobs.add(oid)
for oid in sorted(blobs):
    data = blob(fresh, oid)
    if pattern.search(data):
        content_hits.append(oid)
print('Fresh branch refs:')
print(git(fresh, 'for-each-ref', '--format=%(refname) %(objectname)', 'refs/remotes/origin').decode(), end='')
print('All-reachable commits:', len(commits), '; unique blobs:', len(blobs), '; author identities:', len(author_ids))
print('Excluded-identifier matches: paths', len(path_hits), 'commits', len(message_hits), 'blobs', len(content_hits))
print('Match object IDs:', json.dumps({'paths': path_hits, 'commits': message_hits, 'blobs': content_hits}))
assert not path_hits and not message_hits and not content_hits
print('History audit: PASS')
