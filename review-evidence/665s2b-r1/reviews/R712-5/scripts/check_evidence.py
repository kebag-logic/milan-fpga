#!/usr/bin/env python3
"""Check the published round 16 packet against its MANIFEST.json, and sum every leg's grading line.
usage: python3 -I check_evidence.py <review-evidence/665s2b-r1 directory>"""
import hashlib, json, os, re, sys
root = sys.argv[1]
man = json.load(open(os.path.join(root, 'MANIFEST.json')))
r16 = [e for e in man if e['file'].startswith('author-r16/')]
bad = [e['file'] for e in r16 if not os.path.exists(os.path.join(root, e['file'])) or
       hashlib.sha256(open(os.path.join(root, e['file']), 'rb').read()).hexdigest() != e['published_sha256']]
print(f"manifest author-r16 entries {len(r16)}, bad or missing {len(bad)}, path-redacted {sum(e['path_redacted'] for e in r16)}")
m = os.path.join(root, 'author-r16/receipts/measure')
tot_g = tot_p = 0
for d in sorted(os.listdir(m)):
    line = None
    for f in ('regrade.log', 'run.log'):
        q = os.path.join(m, d, f)
        if os.path.exists(q):
            for l in open(q, errors='replace'):
                if 'groups graded' in l:
                    line = l.strip()
            if line:
                break
    if not line:
        continue
    g = int(re.match(r'(\d+) groups', line).group(1)); r = int(re.search(r'(\d+) refusals', line).group(1))
    over, passes = map(int, re.search(r'(\d+) of (\d+) work passes over', line).groups())
    print(f"{d}: groups {g} refusals {r} over-share {over} of {passes}")
    if d[:2] in ('N-', 'D-', 'NT', 'X4', 'P8'):
        tot_g += g; tot_p += passes
print(f"head legs with struct-ends and 8x8/1if: groups {tot_g}, work passes {tot_p}")
