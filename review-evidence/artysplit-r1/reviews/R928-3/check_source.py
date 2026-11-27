"""Check tracked bytes, file modes, index entries and required submodule pins.

Usage: python3 -B check_source.py SOURCE
"""
import ast
import hashlib
import os
import stat
import subprocess
import sys
from pathlib import Path

source = Path(sys.argv[1]).resolve()
def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def check(root):
    tree = {}
    for entry in git(root, 'ls-tree', '-rz', 'HEAD').split(b'\0'):
        if entry:
            metadata, name = entry.split(b'\t', 1)
            mode, kind, digest = metadata.split()
            tree[name] = (mode, digest)
    index = {}
    for entry in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if entry:
            metadata, name = entry.split(b'\t', 1)
            mode, digest, stage = metadata.split()
            assert stage == b'0', name
            index[name] = (mode, digest)
    assert tree == index, 'index differs from HEAD'
    blobs = 0
    for name, (mode, digest) in tree.items():
        path = root / os.fsdecode(name)
        if mode == b'160000':
            continue
        info = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), name
            assert bool(info.st_mode & 0o111) == (mode == b'100755'), name
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert actual == digest, name
        blobs += 1
    return blobs, tree

count, entries = check(source)
print('HEAD', git(source, 'rev-parse', 'HEAD').decode().strip())
print('TREE', git(source, 'rev-parse', 'HEAD^{tree}').decode().strip())
print('PASS parent tracked blobs/modes/index', count)
for name, (mode, digest) in entries.items():
    if mode != b'160000':
        continue
    relative = os.fsdecode(name)
    if relative == 'external':
        print('PASS external gitlink in index/tree', digest.decode(), '(checkout not initialized; not required)')
        continue
    child = source / relative
    assert (child / '.git').exists(), relative
    assert git(child, 'rev-parse', 'HEAD').strip() == digest, relative
    n, _ = check(child)
    print('PASS required submodule', relative, digest.decode(), 'blobs', n)

base = '4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1'
changed = git(source, 'diff', '--name-only', base, 'HEAD').decode().splitlines()
print('Delta files', len(changed))
for name in changed:
    print('DELTA', name)
    if name.endswith('.py') and name not in (
        'tb/verilator/ctrl_service_budget/census_extract.py',
        'tb/verilator/ctrl_service_budget/receipt_regrade.py'):
        old = git(source, 'show', f'{base}:{name}').decode()
        new = (source / name).read_text()
        assert ast.dump(ast.parse(old)) == ast.dump(ast.parse(new)), name
        print('PASS Python AST unchanged', name)
import yaml
name = 'configs/endstation_arty_split.yaml'
assert yaml.safe_load(git(source, 'show', f'{base}:{name}')) == yaml.safe_load((source / name).read_text())
print('PASS configuration values unchanged')
assert not any(p.startswith('hdl/') for p in changed)
assert not any(p.startswith('sw/firmware/') and p != 'sw/firmware/ctrl/test/ctrl_mutant_fixtures.py'
               for p in changed)
assert not any(entries[os.fsencode(p)][0] == b'160000' for p in changed)
print('PASS no RTL, compiled firmware, row, image or gitlink delta')
subprocess.run(['git', '-C', str(source), 'diff', '--check', '854bd7236792ce1adbd10c43b13a6a5002ad3bb6',
                'HEAD'], check=True)
print('PASS original-base diff whitespace check')
