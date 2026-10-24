#!/usr/bin/env python3
"""Verify public receipt bytes without loading private handoff material."""
import hashlib, json, subprocess, sys
from pathlib import Path
repo, packet = map(Path, sys.argv[1:3])
commit = '15b983dfebd59ad8b658d69bfb0bac237c1c27f2'
prefix = 'review-evidence/775-r1/'
def blob(path):
    return subprocess.check_output(['git','show',commit+':'+prefix+path], cwd=repo)
manifest = json.loads(blob('MANIFEST.json'))
checked, failures = [], []
for entry in manifest:
    name = entry['file']
    if not (name.startswith('author-r2/receipts/') or name == 'reviews/R685-1/scripts/probe_lock_settle.py'):
        continue
    data = blob(name)
    digest = hashlib.sha256(data).hexdigest()
    checked.append({'file': name, 'sha256': digest, 'matches': digest == entry['published_sha256']})
    if digest != entry['published_sha256']: failures.append(name)
    target = packet/'scratch'/'public'/name
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
probe = blob('reviews/R685-1/scripts/probe_lock_settle.py')
(packet/'probe_lock_settle.py').write_bytes(probe)
signature = subprocess.check_output(['git','log','-1','--format=%G?',commit],cwd=repo,text=True).strip()
result={'commit':commit,'signature_status':signature,'manifest_sha256':hashlib.sha256(blob('MANIFEST.json')).hexdigest(),'checked_count':len(checked),'failures':failures,'entries':checked}
(packet/'public_hash_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='entries'},indent=2))
sys.exit(bool(failures))
