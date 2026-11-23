#!/usr/bin/env python3
"""Audit published author receipts and live campaign inventory, without running banks.
Usage: python3 -B audit.py CHECKOUT PACKET
The public author directories and MANIFEST.json must be extracted below
PACKET/scratch/review-evidence/963-r1 from evidence commit 7bd1b854.
"""
import collections
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
root, out = map(lambda x: Path(x).resolve(), sys.argv[1:])
e = out / 'scratch/review-evidence/963-r1'
rows = json.loads((e / 'MANIFEST.json').read_text())
verified = []
for row in rows:
    if not row['file'].startswith(('author/', 'author-r2/')):
        continue
    p = e / row['file']
    assert hashlib.sha256(p.read_bytes()).hexdigest() == row['published_sha256'], str(p)
    verified.append(row['file'])
result = {'evidence_commit': '7bd1b85460690e53a860c53d92c44816667e8be2', 'published_author_hashes_verified': len(verified)}
raw_commit = subprocess.check_output(['git','-C',str(root),'cat-file','commit',result['evidence_commit']])
result['evidence_commit_has_signature_header'] = b'\ngpgsig ' in raw_commit.split(b'\n\n',1)[0]
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import aecp_mutants
import test_ctrl_firmware as gate
import test_ctrl_firmware_shards as shards
work = out / 'scratch/audit'
work.mkdir(exist_ok=True)
os.chdir(work)
inventory = shards.run_cases(gate)
result['live_shard_invocations'] = [len(x) for x in inventory]
result['live_invocation_kinds'] = [dict(collections.Counter(s.split(':')[0] for s in x)) for x in inventory]
r2 = e / 'author-r2/receipts'
expected = [d.name for d in aecp_mutants.DEFECTS]
all_names = []
partitions = []
for k in range(20):
    p = r2 / f'firmware/aecp-campaign/p{k}'
    assert (p/'head.txt').read_text().strip() == 'a18f0996f4b1b654a232dfe56fa64ee7ecaf697e'
    assert (p/'rc').read_text().strip() == '0'
    log = (p/'log.txt').read_text()
    names = re.findall(r'^\[ok\] ([^:]+):', log, re.M)
    assert names == expected[k::20], (k, names)
    assert '[ESCAPED]' not in log
    all_names += names
    partitions.append({'partition': k, 'caught':len(names), 'rc':0})
assert collections.Counter(all_names) == collections.Counter(expected)
result['campaign'] = {'caught':len(all_names), 'unique':len(set(all_names)), 'partitions':partitions}
arms = (r2/'firmware/shard0-aecp-arms/log.txt').read_text()
assert (r2/'firmware/shard0-aecp-arms/rc').read_text().strip() == '0'
result['aecp_normal_arms'] = len(re.findall(r'^\[ok\] arm ',arms,re.M))
assert result['aecp_normal_arms'] == 18
focused = (r2/'tests/focused-head/run.log').read_text()
result['focused_caught'] = re.findall(r'^\[ok\] ([^:]+):', focused, re.M)
assert len(result['focused_caught']) == 17
docs = []
for p in sorted(r2.glob('docs/group-*/steps/summary.txt')):
    docs.extend(p.read_text().splitlines())
result['docs_steps'] = docs
coverage = (r2/'coverage/coverage-check/log.txt').read_text()
result['coverage_selected'] = [l for l in coverage.splitlines() if 'aecp_maps.c' in l or 'PASS' in l]
for name in ['coverage/coverage-check-cut-by-cap','docs/gate_24-cut-by-cap-1','docs/gate_24-cut-by-cap-2']:
    assert (r2/name/'rc').read_text().strip() == '124'
result['cut_units_rc124'] = 3
result['old_tally_recomputed'] = {'control':len(inventory[1])-1,'aecp':len(expected)-1,'srp':len(inventory[3])-1,
                                'plants':(len(inventory[1])-1)+(len(expected)-1)+(len(inventory[3])-1),
                                'normal_suite_arms':len(inventory[0]),'pin_controls':2}
assert result['old_tally_recomputed']['plants'] == 1756
result['round1_excerpt_headers'] = {}
for k in (1,2,3):
    p = e / f'author/receipts/gates-final2/firmware-shard{k}-50d3f10e/gate.log'
    lines = p.read_text().splitlines()
    result['round1_excerpt_headers'][str(k)] = [lines[0],*lines[-2:]]
    h = re.search(r'sha256 ([0-9a-f]{64})',lines[0]).group(1)
    assert h in (r2/'firmware/plant-tally.txt').read_text()
result['limit'] = 'Round-1 large logs are published excerpts. Their embedded raw hashes bind the new tally to the old log identities; hashes do not recover omitted lines. Live dispatch independently supplies category counts. Round-2 campaign logs are complete and recounted by name.'
p = e / 'author/receipts/harness-final'
a = json.loads((p/'strict-rows.json').read_text())
assert len(a) == 481 and len({(x['point'],x['arm'],x['group']) for x in a}) == 481
assert all(x['exact'] and x['rc'] == ['0','0'] for x in a)
b = json.loads((p/'measured-model.json').read_text())
spot = {'unique_exact_groups':len(a),'target_rows':[x for x in a if x['target']],
        'load':{k:v['total'] for k,v in b.items()}}
(out/'unchanged-evidence-spotcheck.json').write_text(json.dumps(spot,indent=2)+'\n')
(out/'audit-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('docs_steps','campaign','focused_caught')},indent=2))
