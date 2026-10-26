#!/usr/bin/env python3
"""Verify archived receipt bytes against the public manifest at its pinned commit."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
out=Path(__file__).resolve().parent
record=json.loads((out/'public-evidence-checks.json').read_text())
rev=record['commit'];prefix='review-evidence/396g-r1/'
def get(name):
    return subprocess.check_output(['git','-C',str(root),'show',rev+':'+prefix+name])
manifest={r['file']:r for r in json.loads(get('MANIFEST.json'))}
for row in record['files']:
    data=get(row['file'])
    assert hashlib.sha256(data).hexdigest()==row['sha256']==manifest[row['file']]['published_sha256']
    assert (out/'public'/row['file']).read_bytes()==data
assert (out/'delta_probes.py').read_bytes()==get('reviews/R700-2/delta_probes.py')
print('PASS:',len(record['files']),'published hashes and retained bytes; delta probe unchanged')
