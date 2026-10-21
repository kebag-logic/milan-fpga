#!/usr/bin/env python3
"""Verify the published author receipts without consulting review reports."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
revision = '6576850939843f0356182fb63f8ba50008027d88'
prefix = 'review-evidence/632-r1/'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=repo)

manifest = json.loads(git('show', revision + ':' + prefix + 'MANIFEST.json'))
rows = []
for entry in manifest:
    if not entry['file'].startswith('author-r2/receipts/'):
        continue
    data = git('show', revision + ':' + prefix + entry['file'])
    digest = hashlib.sha256(data).hexdigest()
    rows.append({'path': entry['file'], 'sha256': digest, 'match': digest == entry['published_sha256']})
    if '/round2/' in entry['file']:
        target = packet / 'scratch/evidence' / entry['file']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
signatures = []
for sha in [revision, '2ff30f0dc5e89be46f8103272883885e8553f4b8']:
    raw = git('cat-file', 'commit', sha)
    header = raw.split(b'\n\n', 1)[0]
    verification = subprocess.run(['git', 'verify-commit', sha], cwd=repo, capture_output=True, text=True)
    signatures.append({'commit': sha, 'embedded_signature': b'\ngpgsig ' in header,
                       'verify_commit_rc': verification.returncode,
                       'diagnostic': verification.stdout + verification.stderr})
result = {'commit': revision, 'checked': len(rows), 'failures': sum(not row['match'] for row in rows),
          'signatures': signatures, 'files': rows}
(packet / 'receipts/published-hash-verification.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'files'}, indent=2))
sys.exit(bool(result['failures']))
