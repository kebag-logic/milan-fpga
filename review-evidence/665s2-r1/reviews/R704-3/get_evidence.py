#!/usr/bin/env python3
"""Export only public evidence, checking its publication digests."""
import hashlib, json, os, subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
root = Path(os.environ['REVIEW_ROOT'])
packet = Path(os.environ['REVIEW_PACKET'])
commit = '0b3e0e3ab108a6d66ed762da7c8766a15d250a97'
prefix = 'review-evidence/665s2-r1/'
def show(name):
    return subprocess.check_output(['git','show',commit+':'+prefix+name],cwd=root)
manifest=json.loads(show('MANIFEST.json'))
selected=[e for e in manifest if (e['file'].startswith('author-r3/receipts/') or e['file'].startswith('author-r2/receipts/') or e['file'].startswith('reviews/R704-2/') or e['file']=='reviews/R704-1/controls/fanout.txt') and not e['file'].endswith('REPORT.md')]
def export(e):
    data=show(e['file']); digest=hashlib.sha256(data).hexdigest()
    assert digest==e['published_sha256'],e['file']
    dest=packet/'scratch/public'/e['file'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    return dict(file=e['file'],sha256=digest,bytes=len(data))
with ThreadPoolExecutor(max_workers=8) as pool:
    checked=list(pool.map(export,selected))
report=dict(commit=commit,signature_status=subprocess.check_output(['git','log','-1','--format=%G?',commit],cwd=root,text=True).strip(),checked=checked)
(packet/'publication-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('Verified',len(checked),'public files; signature status',report['signature_status'])
