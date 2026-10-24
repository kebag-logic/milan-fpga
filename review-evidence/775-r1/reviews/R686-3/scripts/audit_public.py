#!/usr/bin/env python3
"""Verify and extract only published receipts and the assigned probe scripts."""
import hashlib, json, subprocess, sys
from pathlib import Path
repo, packet = map(Path, sys.argv[1:3])
rev = '36b5ada0cf094f322f16ea15fe4b87835bae5edd'
prefix = 'review-evidence/775-r1/'
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
manifest = json.loads(git('show', rev + ':' + prefix + 'MANIFEST.json'))
records = []
for entry in manifest:
    f = entry['file']
    selected = (f.startswith('author-r3/receipts/round3/') and '/superseded-' not in f
                or f in ['reviews/R685-2/scripts/probe_sq_claims.py',
                         'reviews/R685-2/scripts/strip_sv_comments.py'])
    if not selected:
        continue
    data = git('show', rev + ':' + prefix + f)
    digest = hashlib.sha256(data).hexdigest()
    assert digest == entry['published_sha256'], f
    target = packet / 'scratch/public' / f
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    records.append({'file': f, 'sha256': digest, 'path_redacted': entry['path_redacted']})
result = {'archive_commit': rev, 'signature_status': git('show', '--no-patch', '--format=%G?', rev).decode().strip(),
          'verified_files': len(records), 'mismatches': 0, 'files': records}
(packet / 'public-hash-audit.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k:v for k,v in result.items() if k != 'files'}, indent=2))
