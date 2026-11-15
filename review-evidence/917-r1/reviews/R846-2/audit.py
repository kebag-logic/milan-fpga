"""Audit exact source bytes/indexes and public archive receipts; no writes.
Usage: python3 -B audit.py CHECKOUT EXTRACTED_EVIDENCE_ROOT
"""
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1]).resolve()
archive = Path(sys.argv[2]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(*args, at=root):
    return subprocess.check_output(['git', '-C', str(at), *args], env=env)

def prove(at, revision):
    records = git('ls-tree', '-rz', '--full-tree', revision, at=at).split(b'\0')
    expected_index = []
    pins = []
    count = 0
    for record in filter(None, records):
        meta, path = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected_index.append(mode + b' ' + oid + b' 0\t' + path)
        file = at / os.fsdecode(path)
        if kind == b'commit':
            pins.append((os.fsdecode(path), oid.decode()))
            continue
        info = file.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), path
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(info.st_mode), path
            assert bool(info.st_mode & 0o111) == (mode == b'100755'), path
            data = file.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid.decode(), path
        count += 1
    actual_index = sorted(filter(None, git('ls-files', '--stage', '-z', at=at).split(b'\0')))
    assert actual_index == sorted(expected_index), 'index differs'
    assert git('rev-parse', 'HEAD', at=at).decode().strip() == revision
    print(f'{at.relative_to(root) if at != root else "superproject"}: {count} blobs bytes/modes and index match {revision}')
    return pins

head = '8f73ade54366cc832bad3386c8b6f3bbb12ca5e4'
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == 'ae584aff6a5a4e2dc9dde81b170c893cde65a2da'
pins = prove(root, head)
for path, pin in pins:
    if path == 'external':
        print(f'external: gitlink {pin}; intentionally uninitialized, no gate reads it')
        continue
    prove(root / path, pin)

manifest = json.loads((archive / 'MANIFEST.json').read_text())
counts = Counter()
for entry in manifest:
    if not entry['file'].startswith(('author-r1/', 'author-r2/')):
        continue
    path = archive / entry['file']
    assert path.is_file(), entry['file']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['published_sha256'], entry['file']
    counts[entry['file'].split('/')[0]] += 1
print('Published manifest hashes verified: ' + json.dumps(counts, sort_keys=True))
commit = git('cat-file', 'commit', '24755cf4fb9ea20dbede7ad298e7782957a619d8')
print('Archive commit gpgsig present: ' + str(b'\ngpgsig ' in commit))
r2 = archive / 'author-r2/receipts'
a = (r2 / 'images/fixture-images-base.sha256').read_bytes()
b = (r2 / 'images/fixture-images-8f73ade5.sha256').read_bytes()
assert a == b
print(f'Fixture-image receipts: {len(a.splitlines())} hash entries byte-identical')
rtl = 'hdl/milan/mailbox/KL_mbx_rx.sv'
strip = lambda b: re.sub(rb'\s+', b'', re.sub(rb'//[^\n]*|/\*.*?\*/', b'', b, flags=re.S))
assert strip(git('show', '3926c271:' + rtl)) == strip(git('show', head + ':' + rtl))
print('Receive RTL comment-stripped tokens equal to prior head')
changed = git('diff', '--name-only', '3926c271', head).decode().splitlines()
assert not any(p.startswith('sw/firmware/') for p in changed)
print('No firmware source changed in round-2 delta')
import yaml
assert yaml.safe_load(git('show', 'cec88385:sw/mailbox/mailbox.yaml')) == yaml.safe_load((root / 'sw/mailbox/mailbox.yaml').read_text())
print('Parsed mailbox contract equals source base, including every rate and ABI field')
