#!/usr/bin/env python3
"""Recount public receipts and check source/campaign carry to the reviewed head."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

tree, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
author = packet / 'scratch/review-evidence/665s11-r1/author-r5'
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import build
import run
import scenario

def git(*args):
    return subprocess.check_output(['git', *args], cwd=tree)

# The image receipt hashes the whole firmware tree, including campaign sources.
# Replace only later changed blobs with their measured revision to audit that hash.
measured = '7653571f'
changed = set(git('diff','--name-only',measured+'..HEAD').decode().splitlines())
h = hashlib.sha256()
for root in [tree / p for p in build.FIRMWARE_TREES]:
    paths = [root] if root.is_file() else sorted(p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts)
    for p in paths:
        name = str(p.relative_to(tree))
        data = git('show',measured+':'+name) if name in changed else p.read_bytes()
        h.update(name.encode()+b'\0'+hashlib.sha256(data).digest())
for leg in ['A','E1','B1F','B8R']:
    spec = json.loads((author / f'receipts/legs2/{leg}/build.json').read_text())
    assert h.hexdigest() == spec['inputs']['tree:firmware'], (leg,h.hexdigest())
    checked = 0
    for key, expected in spec['inputs'].items():
        if key.startswith('checkout:'):
            name = key.split(':',1)[1]
            data = git('show',measured+':'+name) if name in changed else (tree/name).read_bytes()
            assert hashlib.sha256(data).hexdigest() == expected, (leg,name)
            checked += 1
    print('PASS measured build inputs',leg,': firmware tree and',checked,'checkout hashes')
scripts=list((author/'receipts/legs2/A').glob('results-*/*.txt'))
indexed=[r.split('\t')[0] for r in (author/'receipts/legs2/A/RAW.tsv').read_text().splitlines() if r.split('\t')[0].endswith('.txt')]
assert len(indexed)==96 and len(set(indexed))==96
later=git('diff','--name-only',measured+'..HEAD','--','tb/verilator/ctrl_service_budget').decode().splitlines()
assert all(p.endswith('.md') or p.endswith('/notice_window.py') or p.endswith('/selftest_notice.py') for p in later), later
print('PASS arm A: 96 distinct indexed scripts,',len(scripts),'included; arm A generators unchanged since measured revision')
print('Later notice-window changes apply to answering-every-port stimuli; those legs are represented separately.')
print('LIMIT: raw multi-megabyte execution traces and generated symbols are indexed but not included; no full regrade claimed')
totals=[0,0,0,0,0,0]
for n in range(4):
    path=author/f'receipts/pass/sweep/shard-{n}/spec'
    receipt=json.loads((path/'results.json').read_text())
    assert receipt['head'].startswith('57daf4ff') and receipt['results'][0]['exit_code']==0
    text=(path/'01.log').read_text()
    suite=re.search(r'suites:\s*(\d+)\s+passed:\s*(\d+)\s+failed:\s*(\d+)\s+timed out:\s*(\d+)',text)
    checks=re.search(r'checks:\s*(\d+)\s+in-suite failures:\s*(\d+)',text)
    assert suite and checks
    counts=list(map(int,suite.groups()+checks.groups()))
    totals=[a+b for a,b in zip(totals,counts)]
print('Sweep totals (suites,passed,failed,timed-out,checks,failures):',totals)
assert totals==[65,65,0,0,2713040,0]
control=(author/'receipts/pass/wf/logs/rtl-fast.firmware-control-mutants__ci_step_9.log').read_text()
assert 'mutants: 738 of 738 caught' in control
print('PASS control receipt: 738/738')
aecp=(author/'receipts/pass4/wf/logs/rtl-fast.firmware-aecp-mutants__ci_step_9.log').read_text()
count=len(re.findall(r'^\[ok\]',aecp,re.M))
assert count==314 and 'test_ctrl_firmware: PASS' in aecp
print('PASS AECP receipt: 314/314')
for name in ['reboot-retries-after-its-success','owed-round-beside-the-queue']:
    assert '[ok] '+name+':' in aecp
print('PASS both focused mutations also present in full receipt')
print('PASS receipt consistency')
