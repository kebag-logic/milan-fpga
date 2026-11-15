#!/usr/bin/env python3
"""Read-only checks for PR 902's documentation delta. Run from the candidate root.

The packet's scratch/review-evidence is extracted from archive 1a095573.
No source files are written. Receipts print to stdout.
"""
import ast
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HEAD = '867faf1e7321e1260f86701f01d7de0c94e67490'
BASE = '234bc149ff888eb96659ecaaa5ce6e4fb27319d4'
PACKET = Path(__file__).resolve().parent
EVIDENCE = PACKET / 'scratch/review-evidence/894-r1'

def git(*args, cwd=None):
    return subprocess.check_output(['git', *args], cwd=cwd)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def audit(root, revision):
    tree = git('ls-tree', '-rz', revision, cwd=root).split(b'\0')
    index = git('ls-files', '--stage', '-z', cwd=root).split(b'\0')
    idx = {}
    for row in filter(None, index):
        meta, name = row.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0'
        idx[name] = (mode, oid)
    expected = {}
    count = 0
    subs = []
    for row in filter(None, tree):
        meta, name = row.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected[name] = (mode, oid)
        path = root / os.fsdecode(name)
        if kind == b'commit':
            subs.append((os.fsdecode(name), oid.decode()))
            continue
        data = os.fsencode(os.readlink(path)) if mode == b'120000' else path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid.decode(), str(path)
        actual_mode = b'120000' if path.is_symlink() else (b'100755' if path.stat().st_mode & 0o111 else b'100644')
        assert mode == actual_mode, str(path)
        count += 1
    assert idx == expected, 'index differs from reviewed tree'
    print(f'{root.name}: {count} tracked blob bytes/modes and {len(idx)} index entries match {revision}')
    return subs

def identity():
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    assert git('rev-parse', 'HEAD^{tree}').decode().strip() == '639655730d2a898d963e195cfb95d35fef5ca715'
    paths = git('diff', '--name-only', BASE, HEAD).decode().splitlines()
    assert len(paths) == 6
    for path in paths:
        if path.endswith('.md'):
            continue
        sources = [git('show', f'{rev}:{path}') for rev in (BASE, HEAD)]
        if path.endswith('.h'):
            out = [subprocess.run(['gcc', '-fpreprocessed', '-dD', '-E', '-P', '-x', 'c', '-'], input=s, capture_output=True, check=True).stdout for s in sources]
            assert out[0] == out[1]
            print(path, 'preprocessed bytes identical', sha(out[0]), 'lines', len(out[0].splitlines()))
        else:
            trees = [ast.parse(s) for s in sources]
            if path.endswith('/edit_rows.py'):
                for t in trees:
                    assert isinstance(t.body[0], ast.Expr) and isinstance(t.body[0].value, ast.Constant)
                    t.body[0].value.value = '<module docstring>'
            dumps = [ast.dump(t, include_attributes=True) for t in trees]
            assert dumps[0] == dumps[1]
            print(path, 'AST including positions identical', '(module docstring excluded)' if path.endswith('/edit_rows.py') else '')
    print('Six changed files; three Markdown files; no executable delta.')

def receipts():
    manifest = json.loads((EVIDENCE / 'MANIFEST.json').read_text())
    selected = [r for r in manifest if r['file'].startswith('author-r14/')]
    for row in selected:
        assert sha((EVIDENCE / row['file']).read_bytes()) == row['published_sha256'], row['file']
        assert not row['path_redacted']
        assert row['original_sha256'] == row['published_sha256']
    print('Outer manifest:', len(selected), 'round-14 files verified, none redacted')
    folder = EVIDENCE / 'author-r14'
    rows = re.findall(r'^\| `([^`]+)` \| ([\d,]+) \| `([a-f0-9]{64})` \|$', (folder / 'INDEX.md').read_text(), re.M)
    for name, size, digest in rows:
        raw = (folder / name).read_bytes()
        assert len(raw) == int(size.replace(',', '')) and sha(raw) == digest, name
    assert {r['file'].removeprefix('author-r14/') for r in selected} == {r[0] for r in rows} | {'INDEX.md'}
    print('Inner index:', len(rows), 'byte counts and hashes verified')
    def image_map(path):
        return {name: digest for digest, name in re.findall(r'^([a-f0-9]{64})\s+(.+)$', path.read_text(), re.M)}
    maps = [image_map(folder / f'receipts/identity/image-sha256-{rev}.txt') for rev in ('234bc149', 'b25530f6', '867faf1e')]
    assert len(maps[0]) == 332 and maps[0] == maps[1] == maps[2]
    old = image_map(EVIDENCE / 'author-r13/receipts/images/image-sha256-c274b9f5.txt')
    assert old == maps[0]
    print('Image receipts: 332/332 equal at all three heads and round-13 receipt; kinds', dict(collections.Counter(Path(p).suffix for p in maps[0])))
    legs = [s.split() for s in (folder / 'receipts/identity/harness-elf-sha256.txt').read_text().splitlines() if s and not s.startswith('#')]
    old_legs = (EVIDENCE / 'author-r13/receipts/images/harness-elf-sha256.txt').read_text()
    assert len(legs) == 14
    for leg in legs:
        prior_hash = old['./fixture-1x1-1if/image/ctrl_app.elf'] if leg[0] == 'A' else next(s.split()[1] for s in old_legs.splitlines() if s.startswith(leg[0] + ' '))
        assert leg[2:5] == ['yes'] * 3 and leg[1] == prior_hash, leg[0]
    print('Harness receipts: 14/14 equal flags and prior hashes matched (A in the round-13 fixture image list, 13 in the harness list); 10 distinct ELF hashes')
    gates = (folder / 'receipts/gates/SUMMARY.txt').read_text()
    gs = re.findall(r'^(\w+): rc (\d+) :: (.*)$', gates, re.M)
    assert len(gs) == 28 and all(rc == '0' for _, rc, _ in gs)
    for name, _, tail in gs:
        assert tail in (folder / f'receipts/gates/{name}.log').read_text(), name
    print('Gate receipts: 28/28 rc 0, each summary tail agrees with its archived raw log')
    for rel in ['receipts/images/image-sha256-c274b9f5.txt', 'receipts/images/harness-elf-sha256.txt', 'receipts/model/flip-1x1-ed0df35b.txt', 'receipts/model/flip-selftest-ed0df35b.txt']:
        name = 'author-r13/' + rel
        row = next(r for r in manifest if r['file'] == name)
        assert sha((EVIDENCE / name).read_bytes()) == row['published_sha256']
    print('Four carried round-13 receipts verified against outer manifest')

def integrity():
    root = Path.cwd()
    subs = audit(root, HEAD)
    required = {'protocol-processor', 'gptp-processor', 'third_party/tsn-c-stack', 'third_party/verilog-axis', 'third_party/lwSRP'}
    for name, oid in subs:
        print('gitlink', name, oid)
        if name in required:
            path = root / name
            assert (path / '.git').exists(), name
            assert git('rev-parse', 'HEAD', cwd=path).decode().strip() == oid
            audit(path, oid)
    print('Five initialized dependency submodules: exact heads, tracked bytes, modes and indexes verified')
    assert not git('status', '--porcelain', '--untracked-files=no').strip()

if __name__ == '__main__':
    for name in sys.argv[1:] or ['identity', 'receipts', 'integrity']:
        globals()[name]()
