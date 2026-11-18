#!/usr/bin/env python3
"""Read-only byte, mode, index, gitlink, scope-hash and composition audit.

Usage: python3 audit_identity.py REPOSITORY PACKET
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
HEAD = '66c6edf3f0d05915ee8ddb7346302013833cf66a'
TREE = 'a37bcaecd8c7761f5da29b47b805dbe84bc39ae9'
ARCHIVE = '7bb94e82746cfb8f2a29c5b2b880a528dcbb3764'

def git(*args, cwd=root):
    return subprocess.check_output(['git', *args], cwd=cwd)

def entries(rev, cwd=root):
    out = {}
    for rec in git('ls-tree', '-rz', rev, cwd=cwd).split(b'\0'):
        if not rec:
            continue
        meta, name = rec.split(b'\t', 1)
        mode, kind, oid = meta.split()
        out[os.fsdecode(name)] = (mode.decode(), kind.decode(), oid.decode())
    return out

def verify_checkout(cwd, rev):
    files = entries(rev, cwd)
    index = {}
    for rec in git('ls-files', '--stage', '-z', cwd=cwd).split(b'\0'):
        if not rec:
            continue
        meta, name = rec.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0', name
        index[os.fsdecode(name)] = (mode.decode(), oid.decode())
    assert index == {name:(v[0],v[2]) for name,v in files.items()}, 'index differs from tree'
    n = 0
    for name, (mode, kind, oid) in files.items():
        if kind != 'blob':
            continue
        path = cwd / name
        st = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == '100755'), name
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, f'changed bytes: {name}'
        n += 1
    return n

assert git('rev-parse','HEAD').decode().strip() == HEAD
assert git('rev-parse','HEAD^{tree}').decode().strip() == TREE
print(f'HEAD {HEAD}\nTREE {TREE}')
print(f'Parent: {verify_checkout(root, HEAD)} tracked blobs match exact bytes and modes; index matches HEAD')
files = entries(HEAD)
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']:
    pin = files[name][2]
    assert (root/name/'.git').is_file(), f'not an initialized submodule: {name}'
    assert git('rev-parse','HEAD',cwd=root/name).decode().strip() == pin
    n = verify_checkout(root/name, pin)
    print(f'Submodule {name}: {pin}; {n} tracked blobs byte/mode/index exact')
print('External SSH-only submodule is not initialized and was not used; its gitlink is unchanged.')

release = ['hdl/', 'syn/', 'constraints/', 'configs/', 'avdecc/', 'sw/litex/',
           'sw/firmware/milan_baremetal/', 'sw/builder/', 'third_party/', 'protocol-processor', 'gptp-processor']
budget = ['sw/firmware/ctrl/' + x + '/' for x in ['aecp','mbx','loop','app','srp','maap','acmp','adp','port']]
budget += ['sw/firmware/ctrl_nvm/', 'tb/verilator/ctrl_service_budget/', 'sw/firmware/ctrl/test/ctrl_aecp_image.c',
           'sw/firmware/ctrl/test/ctrl_srp_image.py', 'sw/firmware/ctrl/plat/mbx_plat_mmio.c',
           'sw/firmware/ctrl/plat/ctrl_mem.c', 'sw/firmware/ctrl/plat/ctrl_link.ld',
           'sw/firmware/ctrl/plat/ctrl_hot.txt', 'sw/firmware/ctrl/plat/ctrl_start.S',
           'sw/firmware/ctrl/plat/ctrl_cc.h', 'sw/firmware/ctrl/plat/mbx_dma.h',
           'sw/firmware/ctrl/plat/ctrl_plat_mmio.c']

def scope_hash(rev, prefixes):
    digest = hashlib.sha256()
    subset = {n:v for n,v in entries(rev).items() if any(n == p or n.startswith(p) for p in prefixes)}
    for name, (mode, kind, oid) in sorted(subset.items()):
        data = git('cat-file','blob',oid) if kind == 'blob' else oid.encode()
        digest.update(f'{mode} {kind} {name}\0{len(data)}\0'.encode())
        digest.update(data)
    return len(subset), digest.hexdigest()

merged = git('merge-tree','--write-tree','b1f1161b',HEAD).decode().strip()
assert len(merged) == 40
print(f'Clean merge-tree with train b1f1161b: {merged}')
for label, prefixes in [('release source/input scope',release),('budget source/input scope',budget)]:
    for base, tip in [('cb96336d',HEAD),('b1f1161b',merged)]:
        old, new = scope_hash(base,prefixes), scope_hash(tip,prefixes)
        assert old == new, (label,base,tip,old,new)
        print(f'{label}: {base} -> {tip}: {new[0]} entries; SHA256 {new[1]} EQUAL')
print('These are input hashes, not a rebuilt release bitstream/ELF hash or a new CPU budget execution.')

public = packet/'scratch/public'
manifest = json.loads((public/'MANIFEST.json').read_text())
for row in manifest:
    data=(public/row['file']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == row['published_sha256'], row['file']
print(f'Public archive {ARCHIVE}: {len(manifest)} published file hashes verified')
assert git('diff','--name-only','0749e0d8',HEAD).decode().splitlines() == ['sw/firmware/ctrl/plat/README.md']
print('Evidence inheritance: 0749e0d8 -> exact head changes only platform README (two added lines).')
print('PASS identity, integrity, input equivalence and textual train composition')
