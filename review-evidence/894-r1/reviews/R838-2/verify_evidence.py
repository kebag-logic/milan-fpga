#!/usr/bin/env python3
"""Verify the published evidence manifest and the reviewed checkout's tracked bytes."""
from pathlib import Path
import hashlib
import json
import os
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
evidence = Path(sys.argv[2]).resolve()
def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])

rows = [r for r in json.loads((evidence/'MANIFEST.json').read_text())
        if r['file'].startswith('author-r7/')]
assert rows
bad = []
for r in rows:
    path = evidence/r['file']
    actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else 'MISSING'
    if actual != r['published_sha256']:
        bad.append([r['file'], actual, r['published_sha256']])
print(json.dumps({'published_author_r7_files':len(rows), 'mismatches':bad,
                  'redacted_entries':sum(r['path_redacted'] for r in rows)}, indent=2))
assert not bad
print('Evidence commit:',git(root,'show','-s','--format=%H %T signature=%G?',
      '6f321a998afb177721373be74100a0d84b199ab5').decode().strip())

def inspect(repo, label, expected=None):
    head = git(repo,'rev-parse','HEAD').decode().strip()
    if expected:
        assert head == expected, (label,head,expected)
    tree = git(repo,'rev-parse','HEAD^{tree}').decode().strip()
    assert git(repo,'write-tree').decode().strip() == tree, label+' index differs'
    bad, count, links = [], 0, []
    for entry in git(repo,'ls-files','--stage','-z').split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t',1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0'
        rel = os.fsdecode(name)
        path = repo/rel
        if mode == '160000':
            links.append((rel,oid))
            continue
        count += 1
        if path.is_symlink():
            content = os.fsencode(os.readlink(path))
            actual_mode = '120000'
        else:
            content = path.read_bytes()
            actual_mode = '100755' if path.stat().st_mode & stat.S_IXUSR else '100644'
        actual = hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
        if actual != oid or actual_mode != mode:
            bad.append(rel)
    print(json.dumps({'repository':label,'head':head,'tree':tree,'tracked_blobs_checked':count,
                      'byte_or_mode_mismatches':bad,'gitlinks':links}))
    assert not bad
    return links

links = inspect(root,'candidate','8a3791e44533d6b1cc26d486d0b18e7d83470dc1')
assert git(root,'rev-parse','HEAD^{tree}').decode().strip() == '3387d98b5f115d86cbb60ac303d5271d697e4584'
for rel, oid in links:
    if rel == 'external':
        print('external: optional uninitialized submodule; gitlink checked in index/tree')
        continue
    inspect(root/rel,rel,oid)
print('PASS: exact head, tree, index, tracked blob bytes/modes, and required submodule heads/bytes agree.')
