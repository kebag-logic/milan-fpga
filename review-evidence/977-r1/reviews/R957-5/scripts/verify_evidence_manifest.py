"""Verify every entry of a published evidence MANIFEST.json against the bytes at an evidence commit.
Usage: python3 -I verify_evidence_manifest.py <repo> <commit> <dir>   Exit 0 iff all published_sha256 match."""
import hashlib, json, subprocess, sys
repo, c, d = sys.argv[1:]
show = lambda p: subprocess.run(['git', '-C', repo, 'show', f'{c}:{d}/{p}'], capture_output=True, check=True).stdout
m = json.loads(show('MANIFEST.json'))
bad = [e['file'] for e in m if hashlib.sha256(show(e['file'])).hexdigest() != e['published_sha256']]
r14 = [e['file'] for e in m if e['file'].startswith('author-r14/')]
print(f'evidence {c} {d}: {len(m)} entries, {len(m) - len(bad)} match, {len(bad)} mismatch; author-r14 entries {len(r14)}')
for f in bad: print('MISMATCH', f)
sys.exit(1 if bad else 0)
