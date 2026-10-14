#!/usr/bin/env python3
"""Reconstruct both merge trees and verify the narrowly authorized cleanup."""
import argparse
import ast
import copy
import hashlib
import json
import re
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
a = p.parse_args()
repo = a.repo.resolve()
out = a.packet.resolve() / 'receipts'
head = '412e3f6c8c402bce63e94c291d2782b5579aaa1d'
old = '354f781828d8b4d73037129f297b072320a10f9c'
dev = 'fa8209889411e8ca95757174c981f720dbcd95a2'
donor = repo / 'gptp-processor'
dh = 'e4869fd0c42889b2ac806587cc5c78afb1c33461'
dm = '6b5a4282586a3851117674891d1955253e3de452'

def git(root, *args):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(root), *args])

def entry(root, revision, path):
    return git(root, 'ls-tree', revision, '--', path).decode().strip()

def merge(root, revision, label):
    parents = git(root, 'show', '-s', '--format=%P', revision).decode().split()
    assert len(parents) == 2
    merged = subprocess.run(['git', '--no-replace-objects', '-C', str(root),
        'merge-tree', '--write-tree', *parents], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert merged.returncode in (0, 1)
    (out / (label + '-merge-tree.log')).write_bytes(merged.stdout)
    automatic = next(row.decode() for row in merged.stdout.splitlines()
                     if re.fullmatch(rb'[0-9a-f]{40}', row))
    difference = git(root, 'diff', '--name-only', automatic, revision).decode().splitlines()
    print(label, 'parents:', *parents)
    print(label, 'manual resolution / regenerated paths:', json.dumps(difference))
    (out / (label + '-resolution.diff')).write_bytes(git(root, 'diff', automatic, revision))
    return difference

assert git(repo, 'rev-parse', 'HEAD').decode().strip() == head
assert git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip() == '3a0b668761728b2e9fcc328f71f67f885ef3d11e'
assert git(repo, 'show', '-s', '--format=%P', head).decode().split() == [old, dev]
parent_paths = merge(repo, head, 'parent')
assert all(x.startswith('docs/') or x in ['gptp-processor', 'syn/yosys/rom_digests.tsv'] for x in parent_paths)
assert merge(donor, dm, 'donor') == ['docs/MANAGER.md']
assert git(donor, 'show', '-s', '--format=%P', dm).decode().split() == [
    git(donor, 'rev-parse', '18dd997b').decode().strip(),
    git(donor, 'rev-parse', '61d486e9').decode().strip()]
for ancestor in ['18dd997b', '7dda9c3b', '61d486e9']:
    git(donor, 'merge-base', '--is-ancestor', ancestor, dh)
    print('donor ancestry PASS:', ancestor, 'in', dh)

paths = ['hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv',
         'hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv',
         'tb/verilator/gptp_tables', 'scripts/gen_one_valued_table.py']
for path in paths:
    assert entry(repo, old, path) == entry(repo, head, path)
    print('unchanged since round 3:', entry(repo, head, path))
for path in ['scripts/check_py_idiom.py', 'scripts/check_cpp_idiom.py',
             'scripts/py_idiom.budget', 'scripts/cpp_idiom.budget']:
    assert entry(repo, dev, path) == entry(repo, head, path)
    print('unchanged from live dev:', entry(repo, head, path))
for path in ['scripts/py_idiom.budget', 'scripts/cpp_idiom.budget']:
    assert entry(repo, old, path) == entry(repo, head, path)
    print('unchanged budget since round 3:', path)

style_paths = git(donor, 'diff', '--name-only', dm, dh).decode().splitlines()
assert style_paths == ['docs/MANAGER.md', 'syn/ooc/check_ooc_clock.py', 'tb/verilator/parser/sim_main.cpp']
print('style commit paths:', style_paths)
cpp = 'tb/verilator/parser/sim_main.cpp'
before = git(donor, 'show', dm + ':' + cpp).decode()
after = git(donor, 'show', dh + ':' + cpp).decode()
replacements = [
 ('  int writes_before = bank_writes, writes_through = bank_writes;',
  '  int writes_before = bank_writes;\n  int writes_through = bank_writes;', 1),
 ('    size_t dropped = 0, silent = 0, unwritten = 0;',
  '    size_t dropped = 0;\n    size_t silent = 0;\n    size_t unwritten = 0;', 2),
 ('    size_t kept = 0, beyond = 0;',
  '    size_t kept = 0;\n    size_t beyond = 0;', 1)]
for source, target, count in replacements:
    assert before.count(source) == count
    before = before.replace(source, target)
assert before == after
print('C++ PASS: exactly four declaration splits; types, initializers and order preserved')

path = 'syn/ooc/check_ooc_clock.py'
before = git(donor, 'show', dm + ':' + path).decode()
after = git(donor, 'show', dh + ':' + path).decode()
assert before.split('def selftest()')[0] == after.split('def selftest_arms(')[0]
assert before.split('def main()')[1] == after.split('def main()')[1]
b = ast.parse(before)
c = ast.parse(after)
bs = next(x for x in b.body if isinstance(x, ast.FunctionDef) and x.name == 'selftest')
cs = next(x for x in c.body if isinstance(x, ast.FunctionDef) and x.name == 'selftest')
arms = next(x for x in c.body if isinstance(x, ast.FunctionDef) and x.name == 'selftest_arms')
dump = lambda node: ast.dump(node, include_attributes=False)
assert [dump(x) for x in bs.body[1:-3]] == [dump(x) for x in arms.body[1:-2]]
bwith = next(x for x in bs.body if isinstance(x, ast.With))
cwith = next(x for x in cs.body if isinstance(x, ast.With))
assert dump(bwith.body[5]) == dump(arms.body[-2])
assert dump(bwith.body[6].value) == dump(arms.body[-1].value)
assert [dump(x) for x in bwith.body[:5]] == [dump(x) for x in cwith.body[:5]]
bf = copy.deepcopy(bwith.body[7])
cf = copy.deepcopy(cwith.body[6])
assert isinstance(cf.body[0], ast.Expr) and isinstance(cf.body[0].value, ast.Constant)
cf.body = cf.body[1:]
assert dump(bf) == dump(cf)
assert [dump(x) for x in bwith.body[8:]] == [dump(x) for x in cwith.body[7:]]
assert [dump(x) for x in bs.body[-2:]] == [dump(x) for x in cs.body[-2:]]
print('Python PASS: production/CLI unchanged; all 29 defect fixtures, checks and runner preserved; added docstring')
for function in [arms, cs, cwith.body[6]]:
    print('function lines:', function.name, function.end_lineno - function.lineno + 1)

print('MERGE AND STYLE AUDIT PASS')
