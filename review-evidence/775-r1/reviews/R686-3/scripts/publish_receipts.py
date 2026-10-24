#!/usr/bin/env python3
"""Validate focused results and copy receipts with installation paths normalized."""
import hashlib, json, re, sys
from pathlib import Path
repo, packet, simulator = map(lambda p:Path(p).resolve(),sys.argv[1:4])
scratch = packet/'scratch'
sys.path.insert(0,str(repo/'scripts'))
import suite_tally
fmt = (scratch/'format.log').read_text()
assert suite_tally.scan(fmt)[:2] == (13,0)
assert not suite_tally.log_reports_failure(fmt)[1]
assert 'NxN RX stack: 218 checks, 0 failures' in (scratch/'format-details/obj_clean.log').read_text()
summary = (scratch/'sq-probe/SUMMARY.txt').read_text()
assert summary.count('nx rc=1 NxN RX stack: 218 checks,') == 6
assert summary.count('lockstep N=1 rc=0 RESULT: PASS') == 6
assert summary.count('lockstep N=8 rc=0 RESULT: PASS') == 6
for key, check in [('mr_seed_set','[SQ6e]'),('mr_seed_clear','[SQ7d]')]:
    data=(scratch/'sq-probe'/f'{key}.nx.run.log').read_text()
    assert any('[FAIL]' in l and check in l for l in data.splitlines())
records=json.loads((scratch/'format-details/build-inputs.json').read_text())
pairs=[r for r in records if r['leg'].startswith('lockstep')]
assert len(pairs)==4 and all(len(r['inputs'])==2 for r in pairs)
for r in pairs:
    assert all(x['reject_writes'] for x in r['inputs'])
sources = [scratch/'format.log',scratch/'format.rc',scratch/'sq-probe.log',scratch/'sq-probe.rc']
sources += list((scratch/'format-details').glob('*'))
sources += [p for p in (scratch/'sq-probe').iterdir() if p.is_file()]
redactions=[]
for p in sources:
    raw=p.read_bytes()
    text=raw.decode()
    for old,new in [(str(packet),'<review-packet>'),(str(repo),'<review-checkout>'),
                    (str(simulator.parent),'<pinned-simulator>')]:
        text=text.replace(old,new)
    published=text.encode()
    dest=packet/'receipts'/p.relative_to(scratch)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(published)
    redactions.append({'file':str(dest.relative_to(packet)),
                       'original_sha256':hashlib.sha256(raw).hexdigest(),
                       'published_sha256':hashlib.sha256(published).hexdigest(),
                       'path_normalized':raw!=published})
(packet/'receipt-redactions.json').write_text(json.dumps(redactions,indent=2)+'\n')
print(f'PASS: 13/13 committed campaign, clean NX 218/0, six probes caught, four real paired build inputs; {len(sources)} receipts')
