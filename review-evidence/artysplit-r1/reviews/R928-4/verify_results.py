#!/usr/bin/env python3
"""Assert both replay outcomes and record the exact receipt hashes."""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1])
receipt = root / 'receipts'
normal = (receipt / 'regrade.log').read_text()
control = (receipt / 'missing-bound.log').read_text()
refusal = 'srp-kept and srp-bound are graded together on one image, this run graded srp-kept alone'
assert (receipt / 'regrade.rc').read_text().strip() == '0'
assert (receipt / 'missing-bound.rc').read_text().strip() == '1'
assert sum(x.startswith('PASS ') for x in normal.splitlines()) == 147
assert sum(x.startswith('PASS ') for x in control.splitlines()) == 146
assert 'RESULT: PASS cases=147 worst_pass_cycles=142775' in normal
assert 'RESULT: PASS cross-case costs, record classes, held-egress ledger and owner bounds' in normal
assert any(x.startswith('REFUSED ') and refusal in x for x in control.splitlines())
assert 'RESULT: PASS cross-case' not in control
assert 'part integrity failure' not in control and 'grade differs' not in control
assert 'PASS valid-destinations/srp-talker: complete grade reproduced' in normal
out = dict(normal_cases=147, control_cases=146, normal_exit=0, control_exit=1,
           worst_pass_cycles=142775, worst_pass_ms=142775/80000,
           required_refusal=refusal,
           control_refusals=[x for x in control.splitlines() if x.startswith('REFUSED ')],
           hashes={name: hashlib.sha256((receipt/name).read_bytes()).hexdigest()
                   for name in ('regrade.log','missing-bound.log','audit.log','publication-delta.diff')})
(root / 'receipts/replay-summary.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

reference = root / 'scratch/evidence/author-r8/receipts/proofs/extract-regrade.log'
if reference.exists():
    actual = (receipt / 'regrade.log').read_bytes()
    published = reference.read_bytes()
    assert actual == published
    comparison = dict(normal_replay_matches_published_author_proof_byte_for_byte=True,
                      reviewer_sha256=hashlib.sha256(actual).hexdigest(),
                      published_author_sha256=hashlib.sha256(published).hexdigest())
    (receipt / 'proof-comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
    print('PASS full normal replay equals published author proof byte for byte')
