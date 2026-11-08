# Verify every author-r5 entry of the evidence MANIFEST.json against the checked-out files,
# and list any author-r5 file that the manifest does not name.
import hashlib, json, os, sys
man, root, sub = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open(man))
def entries(d):
    if isinstance(d, dict):
        for k in ('files', 'entries', 'artifacts'):
            if k in d:
                return d[k]
    return d
ents = entries(d)
items = []
if isinstance(ents, dict):
    items = list(ents.items())
else:
    for e in ents:
        p = e.get('file') or e.get('path'); h = e.get('published_sha256') or e.get('sha256')
        items.append((p, h))
sel = [(p, h) for p, h in items if p and sub in p]
bad = 0
for p, h in sel:
    fp = os.path.join(root, p if p.startswith('review-evidence') else os.path.join('review-evidence/tsn26-r1', p))
    got = hashlib.sha256(open(fp, 'rb').read()).hexdigest() if os.path.exists(fp) else 'MISSING'
    if got != h:
        bad += 1
        print('MISMATCH', p, h, got)
listed = set(os.path.normpath(p if p.startswith('review-evidence') else os.path.join('review-evidence/tsn26-r1', p)) for p, _ in sel)
unl = []
for dp, _, fs in os.walk(os.path.join(root, 'review-evidence/tsn26-r1', sub.strip('/'))):
    for f in fs:
        rel = os.path.normpath(os.path.relpath(os.path.join(dp, f), root))
        if rel not in listed:
            unl.append(rel)
print(f'manifest entries under {sub}: {len(sel)}; mismatches: {bad}; unlisted files: {len(unl)}')
for u in unl: print('UNLISTED', u)
sys.exit(1 if bad or unl else 0)
