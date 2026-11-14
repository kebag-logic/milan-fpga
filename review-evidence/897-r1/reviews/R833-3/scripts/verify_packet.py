"""usage: python3 -I verify_packet.py <extracted review-evidence/897-r1 dir>
Checks author-r3 files against MANIFEST.json published_sha256, and INDEX.md rows against the published files."""
import hashlib, json, os, re, sys
root = sys.argv[1]
h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
man = [e for e in json.load(open(os.path.join(root, 'MANIFEST.json'))) if e['file'].startswith('author-r3/')]
ok = sum(1 for e in man if os.path.exists(os.path.join(root, e['file'])) and h(os.path.join(root, e['file'])) == e['published_sha256'])
print('manifest author-r3 entries', len(man), 'verified', ok)
rows = [m.groups() for m in (re.match(r'\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|', l) for l in open(os.path.join(root, 'author-r3/receipts/INDEX.md'))) if m]
miss = [r[0] for r in rows if not os.path.exists(os.path.join(root, 'author-r3', r[0]))]
print('INDEX rows', len(rows), 'not published', len(miss))
for r in miss: print('  NOT PUBLISHED', r)
