#!/usr/bin/env python3
"""Verify published receipt bytes at an immutable evidence commit; inspect no review report."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
a = p.parse_args()
archive = '22239840693f38be230410d189dc9f4d16303feb'
prefix = 'review-evidence/925-r1/'
def git(*args):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(a.repo), *args])
manifest = json.loads(git('show', archive + ':' + prefix + 'MANIFEST.json'))
records = []
for item in manifest:
    if not item['file'].startswith('author-r3/'):
        continue
    data = git('show', archive + ':' + prefix + item['file'])
    actual = hashlib.sha256(data).hexdigest()
    records.append({'file': item['file'], 'sha256': actual,
                    'matches': actual == item['published_sha256'],
                    'published_path_redaction': item['path_redacted']})
raw_commit = git('cat-file', 'commit', archive)
tree_files = git('ls-tree', '-r', '--name-only', archive, prefix + 'author-r3').decode().splitlines()
assert set(prefix + x['file'] for x in records) == set(tree_files)
report = {'archive': archive, 'manifest_sha256': hashlib.sha256(git('show', archive + ':' + prefix + 'MANIFEST.json')).hexdigest(),
          'archive_has_commit_signature': b'\ngpgsig ' in raw_commit,
          'files_checked': len(records), 'all_match': all(x['matches'] for x in records), 'records': records}
print(json.dumps(report, indent=2))
raise SystemExit(0 if report['all_match'] else 1)
