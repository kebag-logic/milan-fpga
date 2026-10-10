#!/usr/bin/env python3
"""Check every author manifest line in the packet: the file's bytes either match
the manifest hash, or the redaction records name the manifest hash as the
original and the current bytes as the retained copy; and check the packet's
top-level MANIFEST.json against the bytes. usage: check_manifests.py <packet-root>"""
import hashlib, json, os, sys
R = sys.argv[1]; A = os.path.join(R, 'author')
def h(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
red = {}
for f in ['redaction.json'] + ['redaction-index/' + x for x in os.listdir(os.path.join(A, 'redaction-index'))]:
    d = json.load(open(os.path.join(A, f)))
    ents = d.get('entries', d)
    if isinstance(ents, dict):
        for k, v in ents.items():
            if isinstance(v, dict) and 'original_sha256' in v: red[k] = v
    elif isinstance(ents, list):
        for v in ents:
            if isinstance(v, dict) and 'original_sha256' in v: red[v.get('path') or v.get('file')] = v
pub = {}
for v in json.load(open(os.path.join(R, 'MANIFEST.json'))):
    pub[v['file']] = v
stats = {'match': 0, 'redacted-ok': 0, 'bad': []}
for m in ['MANIFEST.sha256', 'item3/cycles/MANIFEST.sha256', 'item4/MANIFEST.sha256', 'soak/MANIFEST.sha256']:
    base = os.path.dirname(os.path.join(A, m))
    for l in open(os.path.join(A, m)):
        hh, p = l.split(None, 1); p = p.strip()
        fp = os.path.join(base, p)
        if not os.path.exists(fp): stats['bad'].append((m, p, 'missing')); continue
        cur = h(fp)
        if cur == hh: stats['match'] += 1; continue
        rel = os.path.relpath(fp, A)
        r = red.get(rel) or red.get(p) or red.get(os.path.basename(rel))
        if r and r['original_sha256'] == hh and r['retained_sha256'] == cur: stats['redacted-ok'] += 1
        elif pub.get('author/' + rel, {}).get('original_sha256') == hh and pub['author/' + rel]['published_sha256'] == cur: stats['redacted-ok'] += 1
        else: stats['bad'].append((m, p))
print('author manifests:', stats['match'], 'match,', stats['redacted-ok'], 'redacted with matching original/retained records, bad:', stats['bad'][:20], len(stats['bad']))
ok = bad = 0; badl = []
for p, v in pub.items():
    fp = os.path.join(R, p)
    if os.path.exists(fp) and h(fp) == v['published_sha256']: ok += 1
    else: bad += 1; badl.append(p)
nfiles = sum(len(fs) for _, _, fs in os.walk(R)) - 1
print('top-level MANIFEST.json:', ok, 'published hashes match,', bad, 'bad', badl[:5], '; files in tree excluding MANIFEST.json:', nfiles, '; path-redacted entries:', sum(1 for v in pub.values() if v['path_redacted']))
