#!/usr/bin/env python3
"""Spot-check the published round-13 receipts and three round-10 figure sources.
Usage: python3 -B audit_receipts.py EXTRACTED_PACKET_ROOT
"""
import hashlib
import json
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
p = root / 'author-r13' / 'receipts'
manifest = {r['file']: r for r in json.loads((root / 'MANIFEST.json').read_text())}
count = 0
for f in root.rglob('*'):
    if not f.is_file() or f.name == 'MANIFEST.json':
        continue
    name = str(f.relative_to(root))
    assert hashlib.sha256(f.read_bytes()).hexdigest() == manifest[name]['published_sha256'], name
    count += 1
print('Extracted published files verified:', count)

def text(name):
    return (p / name).read_text()

def images(name):
    return {m[1]: (m[2], m[3]) for m in re.finditer(
        r'^(\S+): rc 0 .*?elf sha256 ([a-f0-9]{64}), loadable sha256 ([a-f0-9]{64})$', text(name), re.M)}

before = images('images/qimg-8883d499.txt')
after = images('images/qimg-d0a2a160.txt')
assert len(before) == len(after) == 8
assert before.keys() == after.keys()
for name in sorted(before):
    same = before[name] == after[name]
    assert same == ('8x8-1if' not in name)
    print('IMAGE', name, 'identical' if same else 'changed', 'ELF', after[name][0], 'loadable', after[name][1])
identity = text('images/img-identity-d0a2a160.txt')
assert identity.count('1 differing') == 2
assert identity.count('li\ta3,2026') == identity.count('li\ta3,2027') == 2
assert "RESULT: PASS" in identity
print('Published disassembly/content comparison: one instruction in each 8x8/1if image; other six identical')
control = text('images/img-identity-control-8883d499-against-itself.txt')
assert 'RESULT: FAIL' in control
print('Image comparison negative control: unchanged 8x8/1if input rejected')

rcs = list((p / 'gates/workflow').glob('*.rc'))
assert rcs and all(f.read_text().strip() == '0' for f in rcs)
print('Published workflow step exit files:', len(rcs), 'all zero; not hosted job evidence')
campaign = text('gates/srp-campaign-plants-d0a2a160.txt')
assert len(re.findall(r'^\[ok\]', campaign, re.M)) == 436
assert not re.search(r'^\[ESCAPED\]', campaign, re.M)
for name in ('asking-is-ready', 'readyfailed-ignored', 'listener-copy-departure-dropped'):
    assert f'[ok] {name}:' in campaign
print('SRP campaign: 436 caught result lines, zero escaped result lines; retargeted and Listener-copy plants present')
coverage = text('gates/workflow/rtl-fast__firmware-unit__ci_step_12.log')
line = next(l for l in coverage.splitlines() if l.startswith('sw/firmware/ctrl/srp/srp_mbx.c'))
assert '746/746' in line and 'lines 100.00 %' in line
print('COVERAGE', line)
docs = text('gates/verify-docs-yml-d0a2a160.txt')
assert '61 steps ran, 34 not run with a reason, 0 bad' in docs
print('Docs: 61 executed steps; 34 NOT RUN with reasons; 0 bad')
print('Firmware-unit post-run status:', text('gates/workflow/rtl-fast__firmware-unit__tree-after.txt').strip().replace('\n', '; '))
print('The untracked dispatch-build output is declared test output, not a changed tracked source')

legs = text('harness/legs-32a9242f/legs-against-46cf2a7d.txt')
assert len(re.findall(r'^- .*: log [a-f0-9]+ identical,', legs, re.M)) == 11
assert 'RESULT: PASS' in legs
print('Leg comparison: 11 group logs reported byte-identical; grade differences only stated reclaim 4000 vs 3500 cycles')
gate = text('harness/legs-32a9242f/gate-8x8-1if-valid-destinations.txt')
missing = [l for l in gate.splitlines() if l.startswith('- the ledger:')]
assert len(missing) == 7
print('Scoped three-leg aggregate: RESULT FAIL for seven missing held-egress rows; not a full acceptance pass')
for l in missing:
    print(l)
old = root / 'author-r10/receipts/harness/legs-46cf2a7d'
g = (old / 'gate-8x8-1if.txt').read_text()
for needle in ('the last at most 25.625 ms', '2,403,014', 'the longest 222,434'):
    assert needle in g
    print('Figure source:', next(l for l in g.splitlines() if needle in l))
cost = (old / 'M8-VDh/costs.txt').read_text()
assert '32,936 CPU cycles' in cost
print('Figure source:', next(l for l in cost.splitlines() if '32,936 CPU cycles' in l))
print('Harness author receipt is abbreviated at its marked cut; final zero-failure and rc=0 lines are present')
assert 'self-test: 0 failures' in text('gates/harness-selftest-d0a2a160.txt')
print('RESULT: PASS')
