#!/usr/bin/env python3
"""Read-only delta, arithmetic and published-evidence verification; run in candidate clone."""
import ast
import hashlib
import json
import pathlib
import re
import subprocess

HEAD = '084cf7a8455e9fa8e24a0e5bcf57c9557816c819'
OLD = '325514224bcc356a6b43843f1003c2323f09de25'
ARCHIVE = '3cb4df23ab4d50650e4945b31063250af797edcb'
ROOT = 'review-evidence/665s2b-r1/'
OUT = pathlib.Path(__file__).resolve().parent

def git(*args):
    return subprocess.check_output(['git', '--no-replace-objects', *args])

assert git('rev-parse', 'HEAD').decode().strip() == HEAD
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == '1ca7a215f77761a09bbb7363d70b5926e899628a'
assert git('rev-parse', OLD+'^{tree}') == git('rev-parse', '5bea2597^{tree}')
changed = git('diff', '--name-only', OLD, HEAD).decode().splitlines()
assert changed == ['docs/design/SPLIT_CONTROL_MEMORY.md', 'sw/litex/ctrl_memory.py']
print('PASS exact head/tree; round-30 source and sync trees equal; only two allowed delta files')
path = 'sw/litex/ctrl_memory.py'
a = ast.parse(git('show', OLD+':'+path))
b = ast.parse(git('show', HEAD+':'+path))
def reasons(tree):
    stmt = next(n for n in tree.body if isinstance(n, ast.AnnAssign) and getattr(n.target, 'id', '') == 'LEDGERED')
    result = {}
    for key, call in zip(stmt.value.keys, stmt.value.values):
        result[key.value] = call.args[-1].value
        call.args[-1].value = '<reason>'
    return result
ra, rb = reasons(a), reasons(b)
assert ast.dump(a) == ast.dump(b)
assert len(ra) == 2 and all(ra[k] != rb[k] for k in ra)
assert all('owed to S14' not in r for r in rb.values())
assert all('owed to the hybrid XIP work' in r and '#665 decision D3' in r for r in rb.values())
print('PASS complete Python AST identical after replacing exactly two LEDGERED reason values')
doc = pathlib.Path('docs/design/SPLIT_CONTROL_MEMORY.md').read_text()
table = doc[doc.index('| 1x1, one interface (shipping) | 105,696'):]
table = table.split('\n\n', 1)[0]
rom, ram = [], []
for row in table.splitlines():
    cells = row.split('|')
    for col in [2, 4]:
        needs = [int(x.replace(',', '')) for x in re.findall(r'([\d,]+) \(', cells[col])]
        assert len(needs) == 2
        rom.append((-needs[0]) % 2048)
        ram.append((-needs[1]) % 2048)
assert min(rom) == 288 and min(ram) == 16
assert 112640 - 112352 == 288 and 56 * 2048 - 114672 == 16
assert 59.0 + 0.5 == 59.5
assert all(s in doc[doc.index('On dev-soft-core `0fb66211`'):][:600] for s in ['#874', '#880', '#889', '#888'])
print('PASS all eight historical image/shape rows: min ROM=288 B; min SRAM=16 B; next SRAM tile=59.5')
manifest = json.loads(git('show', ARCHIVE+':'+ROOT+'MANIFEST.json'))
selected = [e for e in manifest if e['file'].startswith('author-r31/') or
            (e['file'].startswith('author-r30/receipts/final-5bea2597/harness/') and
             re.search(r'X-G[ABN][18]-(regrade.log|compare.txt|tree-after.txt)$', e['file']))]
assert selected
receipts = OUT / 'published'
receipts.mkdir(exist_ok=True)
for e in selected:
    data = git('show', ARCHIVE+':'+ROOT+e['file'])
    assert hashlib.sha256(data).hexdigest() == e['published_sha256'], e['file']
    if '/receipts/gates/' in e['file'] or e['file'].endswith('-regrade.log') or e['file'].endswith('-compare.txt'):
        target = receipts / pathlib.Path(e['file']).name
        target.write_bytes(data)
    print('HASH PASS', e['published_sha256'], e['file'])
print('PASS', len(selected), 'published files match archive manifest')
commit = git('cat-file', 'commit', ARCHIVE)
print('Archive commit signature:', 'present' if b'\ngpgsig ' in commit else 'absent; hash verification is not signature authentication')
for point, expected in [('8', '8.162'), ('1', '9.992')]:
    data = (receipts / ('X-GA'+point+'-regrade.log')).read_text()
    aged = next(x for x in data.splitlines() if x.startswith('AGED '))
    assert 'least margin '+expected+' ms' in aged
    assert expected in doc
    print('RECEIPT', aged)
assert 'Round 30 did not re-derive' in doc
print('PASS aged-window margins and explicit non-rederivation wording')
for name in ['X-GN8-regrade.log', 'X-GN1-regrade.log']:
    for line in (receipts/name).read_text().splitlines():
        if line.startswith('STEPS ') or 'groups graded' in line:
            print(name, line)
memory = (receipts/'test_ctrl_memory.log').read_text()
assert 'RESULT: PASS' in memory and (receipts/'test_ctrl_memory.rc').read_text().strip() == '0'
for line in memory.splitlines():
    if 'RESULT:' in line or re.search(r'\d+ checks.*failures', line):
        print('PUBLISHED MEMORY TEST', line)
print('RESULT: PASS')
