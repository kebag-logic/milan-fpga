#!/usr/bin/env python3
"""Verify byte identity and compare the immutable public receipt packet."""
import hashlib
import json
import os
import pathlib
import re
import stat
import subprocess
import sys

packet = pathlib.Path(__file__).resolve().parent
root = pathlib.Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(directory, *args):
    return subprocess.check_output(['git', '-C', str(directory), *args], env=env)

def verify(directory, revision):
    tree = {}
    for rec in git(directory, 'ls-tree', '-rz', revision).split(b'\0'):
        if not rec:
            continue
        meta, name = rec.split(b'\t', 1)
        mode, kind, oid = meta.split()
        tree[name] = (mode, oid)
        path = directory / os.fsdecode(name)
        if kind == b'commit':
            if (path / '.git').exists():
                assert git(path, 'rev-parse', 'HEAD').strip() == oid
                verify(path, oid.decode())
            else:
                assert name == b'external'
                print('NOT INITIALIZED external: no active consumer')
            continue
        info = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), name
            assert bool(info.st_mode & 0o111) == (mode == b'100755'), name
            data = path.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert blob == oid, name
    index = {}
    for rec in git(directory, 'ls-files', '-sz').split(b'\0'):
        if not rec:
            continue
        meta, name = rec.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and name not in index
        index[name] = (mode, oid)
    assert index == tree
    print('EXACT bytes/modes/index', directory.name, revision, len(tree), 'entries')

if sys.argv[2] == 'integrity':
    head = git(root, 'rev-parse', 'HEAD').decode().strip()
    assert head == 'a6864a49293ba3d0df37029abfa581468ef78dce'
    assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == '282773485cda391903a7e3bf8b1a0374bb882563'
    verify(root, head)
    print('PASS: exact head, tree, tracked bytes, modes, indexes and initialized gitlinks')
    raise SystemExit(0)

evidence = packet / 'scratch/review-evidence/pins1125-r1'
manifest = json.loads((evidence / 'MANIFEST.json').read_text())
for row in manifest:
    assert row['file'].startswith('author/'), row['file']
    data = (evidence / row['file']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == row['published_sha256'], row['file']
print('PUBLIC PACKET', '86ac1ed8f385db77988c43e20318aff9c7a1a667', len(manifest), 'published hashes verified')
r = evidence / 'author/receipts'
for name in ['py_idiom.budget', 'test_evidence.budget']:
    a = git(root, 'show', 'c34e7d8b:scripts/' + name)
    b = git(root, 'show', 'HEAD:scripts/' + name)
    assert a == b
    print('UNCHANGED BUDGET', name, hashlib.sha256(b).hexdigest())
for path in ['hdl', 'hdl/ucode', 'hdl/ucode/gen_gptp_ucode.py', 'syn']:
    a = git(root / 'gptp-processor', 'rev-parse', '3ce71b76:' + path).strip()
    b = git(root / 'gptp-processor', 'rev-parse', '3009f9a2:' + path).strip()
    assert a == b
    print('IDENTICAL IMAGE INPUT', path, a.decode())
for path in ['hdl', 'sw', 'configs', 'third_party/tsn-c-stack']:
    a = git(root, 'rev-parse', 'd0483d08:' + path).strip()
    b = git(root, 'rev-parse', 'HEAD:' + path).strip()
    assert a == b
    print('CARRIED FORWARD', path, a.decode())
for stem, prefix in [('egress-ledger', '| `'), ('plat-ledger', 'POINT ')]:
    def rows(which):
        return [l for l in (r / 'ledgers' / (stem + '-' + which + '.log')).read_text().splitlines() if l.startswith(prefix)]
    assert rows('base') == rows('head') and rows('head')
    print('IDENTICAL LEDGER', stem, len(rows('head')), 'rows')
    print('\n'.join(rows('head')))
routes = r / 'routes'
for name in ['1x1-ExtraPostPlacementOpt', '8x8-ExtraPostPlacementOpt', '8x8-ExtraTimingOpt']:
    def corners(which):
        return [l for l in (routes / (which + '-' + name + '-signoff.txt')).read_text().splitlines() if re.match('(Slow|Fast)_', l)]
    assert len(corners('head')) == 4 and corners('head') == corners('base')
    print('IDENTICAL ROUTE CORNERS', name)
    print('\n'.join(corners('head')))
    def util(which):
        return (routes / (which + '-' + name + '-utilization.txt')).read_text().splitlines()[1].split(' Slice LUTs=')[1]
    assert util('head') == util('base')
    print('IDENTICAL UTILIZATION Slice LUTs=' + util('head'))
assert not (routes / 'base-8x8-AltSpreadLogic_high-signoff.txt').exists()
print('LIMIT: head 8x8 AltSpreadLogic_high exists, but no paired base receipt is published')
print('LIMIT: source receipts are author runs; this packet contains no manager source bank')
print('PASS: published hashes, input carry-forward, unchanged budgets and paired ledger/route checks')
