#!/usr/bin/env python3
"""Check downloaded hosted receipts against the exact source inventory."""
import ast
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
receipts = packet / 'receipts'
head = '4c5d70b50230fbd5da347852d39daf7f23b3df0b'
tree = '8156e281ac181efc76139470e3cf5c530ae17793'
snapshot = json.loads((receipts / 'hosted-observation.json').read_text())
merge = json.loads((receipts / 'hosted-merge-identity.json').read_text())
assert snapshot['run']['head_sha'] == head
assert merge['tree']['sha'] == tree
assert [p['sha'] for p in merge['parents']] == ['fa8209889411e8ca95757174c981f720dbcd95a2', head]
jobs = snapshot['jobs']['jobs']
workers = [j for j in jobs if j['name'].startswith('Verilator shard')]
assert sorted(j['name'] for j in workers) == [f'Verilator shard {i}/6' for i in range(6)]
assert all(j['status'] == 'completed' and j['conclusion'] == 'success' for j in workers)
aggregate = [j for j in jobs if j['name'] == 'verilator-suites']
assert len(aggregate) == 1 and aggregate[0]['status'] == 'completed' and aggregate[0]['conclusion'] == 'success'
print('PASS six executed workers and the executed aggregate succeeded for', head)
print('PASS hosted merge', merge['sha'], 'has source tree', tree)

seen = collections.Counter()
for index in range(6):
    names = (receipts / f'suite-logs-{index}-inventory.txt').read_text().splitlines()
    suites = sorted(n[:-4] for n in names if '/' not in n and n.endswith('.log'))
    expected = (receipts / f'shard-{index}.txt').read_text().splitlines()
    assert suites == expected, (index, suites, expected)
    assert (receipts / f'suite-logs-{index}-TARGET_SHA.txt').read_text().strip() == merge['sha']
    seen.update(suites)
    print(f'PASS artifact {index}/6: {len(suites)} expected suites, exact target SHA')
assert sorted(seen) == (receipts / 'serial-inventory.txt').read_text().splitlines()
assert set(seen.values()) == {1}
print(f'PASS all {len(seen)} default suites exactly once in the uploaded artifacts')

hosted = (receipts / 'hosted-gptp-tables.log').read_text()
local = (receipts / 'gptp-tables-runtime.log').read_text()
prefix = hosted[:hosted.index('RESULT: PASS') + len('RESULT: PASS\n')]
assert prefix == local
module = ast.parse((repo / 'tb/verilator/gptp_tables/mutants.py').read_text())
assignment = next(n for n in module.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'MUTATIONS' for t in n.targets))
expected = [row.elts[0].value for row in assignment.value.elts]
caught = re.findall(r'^\[ ok \] ([^:]+): caught by ', hosted, re.M)
assert caught == expected
assert 'checks: 36   failures: 0' in hosted and 'controls: 26   failures: 0' in hosted
print('PASS hosted gptp_tables: 36 checks, 26 controls; every current control exactly once')
print('PASS hosted/local runtime byte equality, SHA-256', hashlib.sha256(local.encode()).hexdigest())
physical = [j for j in jobs if j['name'] == 'Physical gPTP (nightly and manual)']
assert len(physical) == 1 and physical[0]['conclusion'] == 'skipped'
print('Physical gPTP: SKIPPED, no execution or hardware proof')
