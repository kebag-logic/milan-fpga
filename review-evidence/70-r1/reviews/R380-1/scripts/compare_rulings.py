#!/usr/bin/env python3
"""Compare the manager's D3 ruling table (issue comment body, file arg 1)
with the 'Selected option' column of D3 section 15.1 (file arg 2).
Prints one line per DR id: MATCH / DIFF / MISSING. Exit 0 iff all match."""
import re, sys

def rows(text):
    out = {}
    for line in text.splitlines():
        m = re.match(r'^\|\s*(DR\d+[a-z]?)\b[^|]*\|(.*)\|\s*$', line)
        if m:
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            out[m.group(1)] = cells
    return out

ruling = rows(open(sys.argv[1], encoding='utf-8').read())
doc = rows(open(sys.argv[2], encoding='utf-8').read())
ok = True
for k in sorted(set(ruling) | set(doc)):
    if k not in ruling or k not in doc:
        print(f'{k}: MISSING ruling={k in ruling} doc={k in doc}'); ok = False; continue
    r = ruling[k][1]
    d = doc[k][2] if len(doc[k]) >= 4 else None
    status = 'RULED' in doc[k][0]
    if r == d and status:
        print(f'{k}: MATCH (status RULED)')
    else:
        ok = False
        print(f'{k}: DIFF status_ruled={status}\n  ruling: {r}\n  doc   : {d}')
print('ruling rows', len(ruling), 'doc rows', len(doc))
sys.exit(0 if ok else 1)
