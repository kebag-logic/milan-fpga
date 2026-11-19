#!/usr/bin/env python3
"""Compare published image/grade receipts and summarize execution provenance."""
from pathlib import Path
import hashlib
import re
import sys

out = Path(sys.argv[1]).resolve()
root = out / 'scratch/review-evidence/train1117-r1/author-r5/receipts'
def read(p):
    return (root / p).read_text()
def emit(p, text):
    print('\nARTIFACT', p)
    print(text.strip())

hashfiles = ['step11/images/hashes-b1f1161b.txt', 'step12/images/hashes.txt',
             'step12b/images/hashes.txt', 'step12c/images/hashes.txt']
sets = [{tuple(line.split()[:2]): line.split()[2] for line in read(p).splitlines() if len(line.split()) == 3}
        for p in hashfiles]
assert all(s == sets[0] for s in sets)
assert len(sets[0]) == 12
print('CPU budget: all twelve hash rows equal at all four recorded heads')
for p in hashfiles:
    emit(p, read(p))

grades = list(root.glob('**/flip_check.log'))
final = read('step12c/gates/q-0839453f/flip_check.log')
def payload(s):
    return ''.join(line for line in s.splitlines(keepends=True) if not line.startswith(('CMD ', 'HEAD ', 'rc=')))
for p in grades:
    if any(x in str(p) for x in ['step11', 'step12']):
        print('flip output (command/head/rc wrapper excluded)', p.relative_to(root), 'equal final:', payload(p.read_text()) == payload(final),
              'sha256', hashlib.sha256(p.read_bytes()).hexdigest())
assert (out / 'flip-check.log').read_text() == payload(final)
print('Independent exact-head flip stdout is byte-identical to published final stdout, excluding execution metadata')

for p in ['step12c/images/images-14.txt', 'step12b/images/split-images-13.txt',
          'step12/images/split-gateware-12.txt', 'step12b/images/gateware13.txt']:
    emit(p, read(p))
for p in ['step12c/ledger/plat-ledger.log', 'step12b/ledger/plat-ledger.log']:
    emit(p, '\n'.join(x for x in read(p).splitlines() if x.startswith(('POINT ', 'plat_ledger', 'CONTROL '))))
for step, prefix in [('step12b','r5-g13'), ('step12c','r5-g14')]:
    for p in sorted((root / step / 'logs').glob(prefix+'*log*')):
        if p.name.endswith('.rc'):
            continue
        s = p.read_text()
        lines = [x for x in s.splitlines() if re.search(r'^(HEAD |START|END|== .*rc=|mutants:|test_ctrl_firmware:|CTXFMT|[0-9]+ checks:|.*twin.*findings|.*tests from.*ran|.*tests?\.)', x)]
        emit(str(p.relative_to(root)), '\n'.join(lines[-25:]))
        rc = p.with_name(p.name.replace('.stub.txt','')+'.rc')
        if rc.exists():
            assert rc.read_text().strip() == '0', rc
            print('exit receipt', rc.name, '0')
for point in ['1x1','8x8']:
    emit('step12/fit/fit-'+point+'.log', '\n'.join(x for x in read('step12/fit/fit-'+point+'.log').splitlines()
         if re.search(r'signoff|WNS|floors|rc=',x))[-5000:])
    base = 'step12b/gating/'+point+'/'
    for p in ['artifacts.sha256','identity.log','signoff.txt','image_manifest.json']:
        text = read(base+p)
        emit(base+p, text[:3000])
for p in ['step12c/logs/r5-q14.log','step12c/gates/q-0839453f/fw_coverage_check.log']:
    emit(p, read(p))
print('PASS published receipt comparisons; execution and carried results are distinguished above')
