#!/usr/bin/env python3
"""Hold reviewer campaign verdicts and failure counts to the published receipts."""
import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]
out=[]
for local,public in [('notify','notify'),('d3-final','d3')]:
    actual=json.loads((p/'receipts'/local/'results.json').read_text())
    expected=json.loads((p/'receipts/public/receipts/round3/processor_51f88c7e/campaigns'/f'{public}.results.json').read_text())
    want={r['mutant']:r for r in expected}
    for r in actual:
        w=want[r['mutant']]
        assert r['verdict']==w['verdict'],r
        assert len(r['failing_checks'])==len(w['failing_checks']),r
        assert r['build_rc']==0 and r['completed'] and not r['missing'],r
        assert r['run_rc']==(0 if r['verdict']=='PASS' else 1),r
        out.append(f"{r['mutant']}: {r['verdict']}; {len(r['failing_checks'])} failing checks; published count agrees")
(p/'receipts/reconciliation.txt').write_text('\n'.join(out)+'\n')
print('\n'.join(out))
