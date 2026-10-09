#!/usr/bin/env python3
"""List killers graded without a specific assertion needle.

Usage: needle_audit.py SOURCE_MUTANTS.json EXPORT_MUTATIONS.json
A killer is unspecific when its needle is empty or the generic 'Expected: true'.
Each is marked inherited (same test and needle in the source table) or export-introduced.
"""
import json, sys
src = {m['name']: m for m in json.load(open(sys.argv[1]))}
exp = json.load(open(sys.argv[2]))
rows = []
for m in exp:
    for k in m['kills']:
        if k['needle'] in ('', 'Expected: true'):
            inherited = any(s[1] == k['test'] and s[2] == k['needle'] for s in src[m['name']]['kills'])
            rows.append((('inherited' if inherited else 'export-introduced'), m['name'], k['test'], repr(k['needle']),
                         [f"{s[1]} :: {s[2]}" for s in src[m['name']]['kills']]))
for r in sorted(rows):
    print(' | '.join(map(str, r)))
print('total', len(rows), 'export-introduced', sum(r[0] == 'export-introduced' for r in rows))
