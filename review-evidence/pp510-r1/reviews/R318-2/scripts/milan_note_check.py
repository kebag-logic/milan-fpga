#!/usr/bin/env python3
"""Usage: milan_note_check.py <pdftotext -layout output of Milan v1.2> <tree>
For every 'Note: Support for this feature is a recommendation' occurrence,
print the preceding 5.4.4.x / 7.6 clause heading and the two-sentence note as
printed, then compare it (after the two documented spelling normalizations)
with the quotation in 00 GAP-03 and 06 section 6.9 of <tree>. Also prints
Table 5.19's status rows."""
import re, sys, pathlib
txt, tree = sys.argv[1], pathlib.Path(sys.argv[2])
L = open(txt).read().splitlines()
heads = [(i, l.strip()) for i, l in enumerate(L) if re.match(r'^\s*(5\.4\.4\.\d|7\.6)\.?\s+[A-Z]', l)]
notes = []
for i, l in enumerate(L):
    if l.startswith('Note: Support for this feature is a recommendation'):
        h = [x for x in heads if x[0] < i]
        note = ' '.join((l + ' ' + L[i + 1]).split())
        notes.append(note)
        print(f'{h[-1][1][:48]:48} | {note}')
printed = set(notes)
print(f'distinct printed notes: {len(printed)}')
norm = {n.replace('recomendation', 'recommendation').replace('specificaiton', 'specification') for n in printed}
assert len(norm) == 1
want = norm.pop()
print('normalized:', want)
for rel in ('docs/00_MILAN_COMPLIANCE_REVIEW.md', 'docs/architecture/06_aecp_engine.md'):
    flat = ' '.join((tree / rel).read_text().split())
    q = '“' + want + '”'
    print(f'{rel}: full normalized note quoted = {q in flat}; "(Spelling normalized.)" follows = {(q + " (Spelling normalized.)") in flat}')
i = next(k for k, l in enumerate(L) if 'Table 5.19: MVU status codes' in l)
print('--- Table 5.19 ---')
for l in L[i:i + 7]:
    if l.strip():
        print(' '.join(l.split()))
