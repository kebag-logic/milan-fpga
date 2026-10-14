#!/usr/bin/env python3
"""Read-only exact-tree and capture audit. Run from the candidate checkout."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

HEAD = 'd5cd863561ba1ee7bc6342fb1b00f57dd786bd97'
OLD = '9b32002cc0c3aafae9e864af7b4f08c1089a188a'
DEV = 'fa8209889411e8ca95757174c981f720dbcd95a2'
MERGE = 'f3bb2014d065141930ae1a473c966b419d1040aa'
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(*args, cwd=None):
    return subprocess.check_output(['git', *args], cwd=cwd, env=ENV)

def tree(rev, cwd=None):
    result = {}
    for row in git('ls-tree', '-rz', rev, cwd=cwd).split(b'\0'):
        if row:
            meta, path = row.split(b'\t', 1)
            result[os.fsdecode(path)] = tuple(meta.decode().split())
    return result

def changed(a, b):
    return {p: (a.get(p), b.get(p)) for p in a.keys() | b.keys() if a.get(p) != b.get(p)}

def verify_checkout(cwd, rev, recurse=False):
    entries = tree(rev, cwd)
    index = {}
    for row in git('ls-files', '-s', '-z', cwd=cwd).split(b'\0'):
        if row:
            meta, path = row.split(b'\t', 1)
            mode, oid, stage = meta.decode().split()
            assert stage == '0', (cwd, path, stage)
            index[os.fsdecode(path)] = (mode, oid)
    assert index == {p: (v[0], v[2]) for p, v in entries.items()}, 'index differs'
    blobs = 0
    for name, (mode, kind, oid) in entries.items():
        p = Path(cwd) / name
        if kind == 'commit':
            if recurse and name in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack'):
                assert git('rev-parse', 'HEAD', cwd=p).decode().strip() == oid
                assert (p / '.git').is_file(), (name, 'not an initialized submodule')
                verify_checkout(p, oid)
            continue
        st = p.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode)
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode)
            assert bool(st.st_mode & 0o111) == (mode == '100755'), name
            data = p.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, (name, oid, actual)
        blobs += 1
    print(f'PASS tracked blobs, modes, index: {Path(cwd).name}: {blobs} blobs')

assert git('rev-parse', 'HEAD').decode().strip() == HEAD
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == '029737bc62cb0fc1bbf45e3aed82a39160ee41da'
assert git('show', '-s', '--format=%P', MERGE).decode().strip() == OLD + ' ' + DEV
merged_tree = git('merge-tree', '--write-tree', OLD, DEV).decode().strip()
assert merged_tree == git('rev-parse', MERGE + '^{tree}').decode().strip()
print('PASS automatic two-parent merge tree:', merged_tree)
old, dev, merge, head = [tree(r) for r in (OLD, DEV, MERGE, HEAD)]
previous_dev = git('merge-base', OLD, DEV).decode().strip()
assert previous_dev == 'c6bd08c6f52632c6d33d834ce842ac3cf63f29cc'
prior = tree(previous_dev)
lane = changed(prior, old)
assert len(lane) == 15
assert set(lane) == set(changed(dev, merge))
for p in lane:
    assert merge.get(p) == old.get(p), p
assert changed(old, merge) == changed(prior, dev)
print('PASS all 15 lane paths byte/mode identical at merge; 160-path delta exactly dev:', len(changed(old, merge)))
for p in sorted(lane):
    print('LANE', p, old[p][2], merge[p][2])
gitlinks = {p: v for p, v in changed(old, merge).items() if any(e and e[1] == 'commit' for e in v)}
assert set(gitlinks) == {'third_party/tsn-c-stack'}
print('PASS only gitlink delta:', gitlinks)
final = changed(merge, head)
assert set(final) == {'tb/verilator/nvm_capture_cpu/measurements.json', 'docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md'}
page = 'docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md'
a = git('show', MERGE + ':' + page).decode()
b = git('show', HEAD + ':' + page).decode()
assert a.split('## 18. Cost')[0] == b.split('## 18. Cost')[0]
assert a.split('## 19.')[1:] == b.split('## 19.')[1:]
receipt_path = 'tb/verilator/nvm_capture_cpu/measurements.json'
r = json.loads(git('show', HEAD + ':' + receipt_path))
before = json.loads(git('show', OLD + ':' + receipt_path))
keys = {k for k in r.keys() | before.keys() if r.get(k) != before.get(k)}
assert keys == {'date', 'base', 'tree', 'remeasurement_assignment', 'provenance'}, keys
assert r['base'] == MERGE and r['tree'] == merged_tree
assert r['measurements'] == before['measurements']
assert sum(len(x['rows']) for x in r['measurements']) == 96
print('PASS final delta: section 18 only; receipt provenance only:', sorted(keys))
print('PASS all 96 complete measurement rows and every arm input hash equal round 7')
for x in r['measurements']:
    print('ARM', x['shape'], x['cpu_hz'], x['traffic'], min(v['sys_cycles'] for v in x['rows']), max(v['sys_cycles'] for v in x['rows']))
worst = max(v['sys_cycles']/x['sys_hz']*1000 for x in r['measurements'] if x['cpu_hz']==50000000 and '8x8' in x['shape'] for v in x['rows'])
assert worst == 13.86328
print('PASS 8x8 contract maximum ms:', worst, 'margin ms:', 24.5-worst, 'floor ratio:', 49/worst)
verify_checkout(Path.cwd(), HEAD, recurse=True)
print('PASS exact head integrity')
