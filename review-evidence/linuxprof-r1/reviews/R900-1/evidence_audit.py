#!/usr/bin/env python3
"""Audit the immutable published author packet without executing its scripts.

Usage: python3 evidence_audit.py REPO PACKET
Requires evidence commit adeb1331026950e5c13c31debb44a225caa62ad1 locally.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys

repo,packet=map(lambda s:Path(s).resolve(),sys.argv[1:3])
revision='adeb1331026950e5c13c31debb44a225caa62ad1'
prefix='review-evidence/linuxprof-r1/'
def read(path):
    return subprocess.check_output(['git','show',revision+':'+prefix+path],cwd=repo)
manifest=json.loads(read('MANIFEST.json'))
for row in manifest:
    assert hashlib.sha256(read(row['file'])).hexdigest()==row['published_sha256'],row['file']
receipts=[json.loads(read(f'author/receipts/sub-{n}.json')) for n in range(4)]
inventory=receipts[0]['inventory']
assert all(r['inventory']==inventory for r in receipts)
counts=Counter(g['gate'] for r in receipts for g in r['gates'])
assert all(n==1 for n in counts.values())
assert all(g['verdict']=='pass' for r in receipts for g in r['gates'])
not_run=[{'gate':g['gate'],'rows':g['not_run']} for r in receipts for g in r['gates'] if g['not_run']]
identities=[json.loads(read('author/receipts/'+name)) for name in
            ('identity-base-854bd723.json','identity-head-677d605f.json')]
assert identities[0]['artifacts']==identities[1]['artifacts']
assert all(not r['tracked_status'] for r in identities)
result=dict(public_commit=revision,published_files_hash_verified=len(manifest),
    inventory=len(inventory),function_pass_verdicts=len(counts),
    missing_functions=sorted(set(inventory)-counts.keys()),not_run=not_run,
    author_identity_artifacts=len(identities[0]['artifacts']),author_identity_equal=True,
    binding='Public packet and REVIEW READY attribute these receipts to the source head. Subset JSON itself has no head/tree binding.',
    limits=['Not a ci_builder_legs.py union proof.','No manager source bank.',
            'Calibration NOT RUN is not a hardware pass.','Focused firmware arm logs are not four completed firmware shards.'])
(packet/'evidence-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
