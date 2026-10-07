#!/usr/bin/env python3
"""Hash public retained source-validation evidence at a fixed evidence commit."""
import concurrent.futures, hashlib, json, subprocess, sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve();p=Path(__file__).resolve().parent
ref='a07d7d051a7a92365be7768c06a260a71fa78934';prefix='review-evidence/665f4-r1/author-r9/'
def fetch(path):
    return subprocess.check_output(['gh','api','-H','Accept: application/vnd.github.raw+json','repos/kebag-logic/milan-fpga/contents/'+prefix+path+'?ref='+ref])
gates=json.loads(fetch('ROUND9-GATES.json'));source=json.loads(fetch('ROUND9-SOURCE.json'))
assert gates['head']==source['head']=='edeef61c5a0cc6c18caa61db4019a8e378baf366'
for item in source['files']:
    data=(repo/item['path']).read_bytes();assert len(data)==item['size'] and hashlib.sha256(data).hexdigest()==item['sha256']
assert subprocess.check_output(['git','-C',str(repo),'diff','--name-only','877c0b9d..HEAD']).decode().splitlines()==['sw/firmware/gtest/coverage.ratchet']
def check(rec):
    assert rec['rc']==0
    kept=rec.get('retained_log')
    if not kept:return {'label':rec['label'],'rc':0,'raw_hash_only':True}
    data=fetch(kept['path']);assert len(data)==kept['size'] and hashlib.sha256(data).hexdigest()==kept['sha256'],rec['label']
    target=p/'scratch/audited-public'/kept['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    return {'label':rec['label'],'rc':0,'verified_public_log':kept}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:records=list(ex.map(check,gates['receipts']))
(p/'public-audit.json').write_text(json.dumps({'evidence_commit':ref,'head':source['head'],'source_files_verified':len(source['files']),'builder_difference_only_coverage_ratchet':True,'receipts':records},indent=2)+'\n')
print('PASS:',len(records),'zero-exit source receipts;',sum('verified_public_log' in r for r in records),'public log byte/hash matches;',len(source['files']),'current source file matches')
