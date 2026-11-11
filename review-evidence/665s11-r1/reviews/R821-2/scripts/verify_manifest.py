#!/usr/bin/env python3
"""Check every author-r2 entry of the archive's MANIFEST.json against the blob bytes at that archive commit.
Usage: verify_manifest.py <git-dir> <commit> <prefix> [subdir]"""
import hashlib, json, subprocess, sys
gitdir, commit, prefix = sys.argv[1:4]
sub = sys.argv[4] if len(sys.argv) > 4 else 'author-r2/'
def blob(path):
    return subprocess.run(['git', '--git-dir', gitdir, 'show', f'{commit}:{prefix}{path}'], capture_output=True, check=True).stdout
man = json.loads(blob('MANIFEST.json'))
tree = set(subprocess.run(['git', '--git-dir', gitdir, 'ls-tree', '-r', '--name-only', commit, prefix + sub],
                          capture_output=True, text=True, check=True).stdout.split())
listed = {e['file'] for e in man if e['file'].startswith(sub)}
bad = 0
for e in man:
    if not e['file'].startswith(sub):
        continue
    h = hashlib.sha256(blob(e['file'])).hexdigest()
    if h != e['published_sha256']:
        bad += 1; print('MISMATCH', e['file'])
unlisted = sorted(t[len(prefix):] for t in tree if t[len(prefix):] not in listed)
print(f'entries={len(listed)} tree_files={len(tree)} mismatches={bad} unlisted={len(unlisted)}')
for u in unlisted: print('UNLISTED', u)
redacted = sum(1 for e in man if e['file'].startswith(sub) and e['path_redacted'])
print(f'path_redacted={redacted}')
sys.exit(1 if bad or unlisted else 0)
