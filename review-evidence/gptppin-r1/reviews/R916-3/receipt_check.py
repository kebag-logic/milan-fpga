#!/usr/bin/env python3
"""Verify and retain selected public receipts. Usage: receipt_check.py SOURCE PACKET."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode = True

src, out = map(lambda p: Path(p).resolve(), sys.argv[1:])
rev = '1fe0516af44a9d94eb1f5667d32eb67919851eba'
prefix = 'review-evidence/gptppin-r1/'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', PYTHONDONTWRITEBYTECODE='1')
def get(path):
    return subprocess.check_output(['git', 'show', rev + ':' + prefix + path], cwd=src, env=env)
manifest = {x['file']: x for x in json.loads(get('MANIFEST.json'))}
paths = [
 'author-r3/receipts/rtl/gptp_shadow-run.log',
 'author-r3/receipts/rtl/gptp_shadow-lifecycle.log',
 'author-r3/receipts/ledger/images-unchanged.txt',
 'author-r3/receipts/ledger/plat-ledger.txt',
 'author-r3/receipts/rtl/shard-projection.txt',
 'author-r3/receipts/tools/probes_r3.py.txt',
 'author-r3/receipts/rtl/milan_dp-inputs.txt',
 'author-r2/receipts/rtl/milan_dp-gptp-f97e49fe.log',
 'author-r2/receipts/rtl/milan_dp-gptp-lat-f97e49fe.log',
 'author-r2/receipts/ledger/image-hashes-vs-round1.txt',
 'reviews/R916-2/order-probe.patch',
 'reviews/R915-2/receipts/published/probe-diffs/p106-nocredit.probe.diff',
]
paths += [f'author-r3/receipts/rtl/gptp_shadow-mutants-{s}.log' for s in ('0-2','1-2','2-4','4-6','6-8','7-8','8-10','10-12','12-13')]
paths += [f'author-r3/receipts/probes/probe-{case}.{ext}' for case in ('order-stall','r915-p106-nocredit','r915-p106-beat','r916-delayed-announce','r916-retained-rate') for ext in ('log','rc')]
paths += [f'author-r3/receipts/windows/win{x}-SUMMARY.txt' for x in ('A','B','C','D','E','F','G','I','L')]
log = []
for path in paths:
    data = get(path)
    assert hashlib.sha256(data).hexdigest() == manifest[path]['published_sha256'], path
    dest = out / 'receipts' / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    log.append(hashlib.sha256(data).hexdigest() + '  ' + path)

sys.path.insert(0, str(src / 'tb/verilator/gptp_shadow'))
import mutants
assert len(mutants.MUTATIONS) == 13
for name, path, old, new, expected in mutants.MUTATIONS:
    anchors = old if isinstance(old, tuple) else (old,)
    for anchor in anchors:
        assert path.read_text().count(anchor) == 1, name
log.append('13 mutation controls have unique current-head anchors: PASS')
replay = ast.parse(get('author-r3/receipts/tools/probes_r3.py.txt'))
constants = {n.targets[0].id: ast.literal_eval(n.value) for n in replay.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ('STALL_OLD', 'STALL_NEW')}
stall = next(x for x in mutants.MUTATIONS if x[0] == 'master_announce_reaches_the_lane_after_the_re_election')
text = stall[1].read_text()
assert text.replace(constants['STALL_OLD'], constants['STALL_NEW']) == mutants.planted(text, stall[2], stall[3])
old_patch = get('reviews/R916-2/order-probe.patch').decode()
first_hunk = old_patch.split('@@')[2]
assert '+        dut->tx_tready_i = 0;' in first_hunk and '+        dut->tx_tready_i = 1;' in first_hunk
log.append('Published replay and campaign stall produce identical current-head bytes; original first hunk matches: PASS')
credit = next(x for x in mutants.MUTATIONS if x[0] == 'announce_leg_ignores_the_credit')
text = credit[1].read_text()
mutated = mutants.planted(text, credit[2], credit[3])
import difflib
changed = [x for x in difflib.ndiff(text.splitlines(), mutated.splitlines()) if x.startswith(('- ', '+ '))]
assert changed == ['-     e_credit_gate(p, "skip")']
orig = get('reviews/R915-2/receipts/published/probe-diffs/p106-nocredit.probe.diff').decode()
assert '-    e_credit_gate(p, "skip")' in orig
log.append('Credit control removes exactly the original no-credit probe gate: PASS')
seen = set()
for path in paths:
    if '/gptp_shadow-mutants-' in path:
        seen.update(re.findall(r'^\[ ok \] ([^:]+):', get(path).decode(), re.M))
assert seen == {x[0] for x in mutants.MUTATIONS}
for case, count in [('order-stall', '424 checks: 423 PASS, 1 FAIL'), ('r915-p106-nocredit', '424 checks: 421 PASS, 3 FAIL'), ('r916-delayed-announce', '422 checks: 416 PASS, 6 FAIL'), ('r916-retained-rate', '424 checks: 420 PASS, 4 FAIL')]:
    data = get(f'author-r3/receipts/probes/probe-{case}.log').decode()
    assert count in data
    assert get(f'author-r3/receipts/probes/probe-{case}.rc').strip() == b'2'
log.append('13/13 published campaign detections and four complete fault tallies: PASS')
for row in mutants.MUTATIONS[-2:]:
    expected = row[4]
    matching = [p for p in paths if '/gptp_shadow-mutants-' in p and f'caught by "{expected}"' in get(p).decode()]
    assert matching
    log.append(row[0] + ': named failure confirmed in ' + ', '.join(matching))
(out / 'receipt-check.log').write_text('\n'.join(log) + '\n')
print('\n'.join(log[-7:]))
