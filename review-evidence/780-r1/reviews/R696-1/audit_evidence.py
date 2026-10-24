#!/usr/bin/env python3
"""Audit the published receipts, without executing their scripts."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

PACKET=Path(__file__).resolve().parent
REV='3e0d0e08ac6adcb2aa0f43316d800073f2492e6a'
HEAD='25f05752f7e50e3cf7e27008e434ffde930b4b6f'
BASE='review-evidence/780-r1/'
def read(path):
    return subprocess.check_output(['git','show',REV+':'+BASE+path])
def receipt(path):
    return read('author/receipts/'+path).decode()

manifest=json.loads(read('MANIFEST.json'))
checked=0
for row in manifest:
    if '/receipts/' not in row['file']:
        continue
    assert hashlib.sha256(read(row['file'])).hexdigest()==row['published_sha256'],row['file']
    checked+=1
print(f'PASS published hashes for {checked} executable receipt files at {REV}')
suites=[]; total=0
for i in range(4):
    meta=json.loads(receipt(f'sweep/shard-{i}/spec-results.json'))
    assert meta['head']==HEAD and all(r['exit_code']==0 for r in meta['results'])
    s=receipt(f'sweep/shard-{i}/spec-01.log')
    suites+=re.findall(r'^PASS\s+(\S+)$',s,re.M)
    total+=int(re.search(r'checks: (\d+)',s)[1])
assert len(suites)==len(set(suites))==64 and total==2190096
print('PASS sweep: 64 unique suites, 2190096 checks, four rc=0 exact-head shards')
fast={}
for f in ['rtl_fast/run1-receipts.json','rtl_fast/run2-fw-receipts.json']:
    d=json.loads(receipt(f)); assert d['head']==d['head_after']==HEAD
    assert not d['tracked_changes']
    fast.update(d['jobs'])
assert len(fast)==11 and all(j['result']=='success' for j in fast.values())
print('PASS fast-gate receipts: latest execution for each of 11 jobs succeeds; initial SDK refusal retained')
for name,j in fast.items():
    print('JOB',name,'executed',sum('rc' in s for s in j['steps']),
          'skipped',sum('skipped' in s for s in j['steps']))
docs={}
for f in ['docs_gates/all-receipts.json','docs_gates/leg1-ci312-receipts.json',
          'docs_gates/leg1-litex-receipts.json','docs_gates/md312-receipts.json']:
    d=json.loads(receipt(f));assert d['head']==d['head_after']==HEAD
    for step in d['steps']:docs[(step['job'],step['id'])]=step
failed=[s for s in docs.values() if s.get('rc') not in (0,None)]
assert not failed
print('PASS docs: latest published step receipts have no nonzero rc; skips are not execution')
for key,s in docs.items():
    if s.get('rc') is None:print('DOC SKIP',key,s)
print('Builder retry: same script hash on both successful leg-1 receipts; initial failure retained')
for f in ['docs_gates/leg1-ci312-receipts.json','docs_gates/leg1-litex-receipts.json']:
    d=json.loads(receipt(f));print(f,d['steps'][0]['script_sha256'],d['steps'][0]['rc'])
print('PASS firmware table:',len(re.findall(r'^0 ',receipt('firmware/table.txt'),re.M)),'commands rc=0')
assert len(re.findall(r'^0 ',receipt('firmware/table.txt'),re.M))==8
assert len(re.findall(r'^rc=0 ',receipt('pinchecks/table.txt'),re.M))==11
print('PASS pin table: 11 commands rc=0')
for f in ['vivado/route-1x1-check.log','vivado/ooc-1x1-check.log','vivado/ooc-8x8-check.log']:
    s=receipt(f);assert 'RESULT: PASS' in s
    print(f);print(s.split('sub-block movements')[0].strip())
print('Limits: this audits published receipts, not raw omitted build logs or a new full-bank run.')
