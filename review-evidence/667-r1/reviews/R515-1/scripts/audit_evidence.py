#!/usr/bin/env python3
"""Check published receipt hashes, merge preservation and measured summaries.

Usage: python3 scripts/audit_evidence.py CHECKOUT
Requires the public evidence tree already extracted into scratch/.
"""
import ast
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
repo = Path(sys.argv[1]).resolve()
public = root / 'scratch/review-evidence/667-r1'
head = '41bc9dac031526c1fd637ff1e801d3c6dc1260b4'
author = '5d6164a2da2d4f7374558bf33b464bcd8a9b4fc2'
dev = 'bd884631684ccf5060339efa92263d5c3e5c262c'


def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def table(data):
    for item in ast.parse(data).body:
        if isinstance(item, ast.Assign) and any(isinstance(t, ast.Name) and
                t.id == 'DUT_READER_DISPOSITIONS' for t in item.targets):
            return ast.literal_eval(item.value)
    raise AssertionError('missing reader table')


manifest = json.loads((public / 'MANIFEST.json').read_text())
for row in manifest:
    actual = hashlib.sha256((public / row['file']).read_bytes()).hexdigest()
    assert actual == row['published_sha256'], row['file']
old = table(git('show', author + ':scripts/measure_test_evidence.py'))
live = table(git('show', dev + ':scripts/measure_test_evidence_readers.py'))
merged = table(git('show', head + ':scripts/measure_test_evidence_readers.py'))
key = 'tb/verilator/aaf/start_mutants.py'
assert merged == dict(live, **{key: old[key]})
paths = git('diff', '--name-only', dev + '..' + head).decode().splitlines()
for path in paths:
    if path != 'scripts/measure_test_evidence_readers.py':
        assert git('show', head + ':' + path) == git('show', author + ':' + path), path
assert git('show', head + ':scripts/measure_test_evidence.py') == git('show', dev + ':scripts/measure_test_evidence.py')

render = json.loads((public / 'author/render-comparison.json').read_text())
assert len(render['runs']) == 32 and render['same_campaign_verdicts']
assert all(r['byte_equal'] and r['base_rc'] == r['head_rc'] and
           r['base_sha256'] == r['head_sha256'] and r['base_bytes'] == r['head_bytes']
           for r in render['runs'])
b = (public / 'author/render-base-epoch.log').read_bytes()
h = (public / 'author/render-candidate-epoch.log').read_bytes()
assert b == h and len(b) == 3745
assert hashlib.sha256(b).hexdigest() == '7876a3a277df5e06a9381e502249b9638b7a4e04ec676fefba207150b41d4007'

areas = list(csv.DictReader((public / 'author/area.csv').open()))
own = [r for r in areas if r['instance'] == 'aaf_packetizer']
area_delta = {k:int(own[1][k])-int(own[0][k]) for k in ['lut','ff','ramb36','ramb18','dsp']}
assert area_delta == {'lut':-4,'ff':0,'ramb36':0,'ramb18':0,'dsp':0}

new_log = (root / 'receipts/startup-head.log').read_text()
assert 'checks: 34020   failures: 0' in new_log and 'startup mutants: 8/8 caught' in new_log
steps = re.findall(r'^START-SWEEP .*first_step=(-?\d+) steady=(-?\d+) tolerance_ns=(\d+)$',new_log,re.M)
assert len(steps) == 486 and all(r == ('125000','125000','0') for r in steps)
assert len(re.findall(r'^START-PDU ',new_log,re.M)) == 4860
base_log = (root / 'receipts/startup-base.log').read_text()
assert 'first_step=-494821316 steady=125000' in base_log
assert 'checks: 33804   failures: 864' in base_log
multi = (root / 'receipts/multi-run.log').read_text()
rows = re.findall(r'^multi phase=.*checks=(\d+) failures=(\d+) counts=([\d,]+)$',multi,re.M)
assert len(rows) == 48 and all(r[1]=='0' for r in rows)

result = {
  'published_receipts_verified': len(manifest),
  'public_evidence_commit': '90d0bcbfb83ee4f5d47edadd734acd1e1056759b',
  'public_gate_summary_head': author,
  'merge_head': head, 'dev_parent': dev,
  'merge_reader_table': 'exact dev table plus unchanged author startup entry',
  'new_paths_against_dev': paths,
  'other_new_path_bytes': 'equal to author head',
  'public_render_comparison': '32 identical stdout/rc/hash/size records; author head versus assigned base',
  'public_epoch_logs': {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'equal':True},
  'public_own_area_delta': area_delta,
  'reviewer_startup': {'starts':len(steps),'pdus':4860,'checks':34020,'failures':0,'mutants_caught':8},
  'reviewer_base': {'checks':33804,'failures':864,'backward_step_ns':-494821316},
  'reviewer_multistream': {'cases':len(rows),'stream_starts':8*len(rows),
       'checks':sum(int(r[0]) for r in rows),'failures':0,
       'pdus':sum(sum(int(v) for v in r[2].split(',') if v) for r in rows)},
  'limits': 'Public gate summaries and artifact indexes are not raw logs or a fresh full-bank execution.'
}
print(json.dumps(result,indent=2))
