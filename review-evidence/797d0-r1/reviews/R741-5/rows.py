"""Compare the Findings (ID, page, line) rows and per-page statuses between two audit pages."""
import re, sys
def parse(t):
    rows, st = [], {}
    f = False
    for l in t.splitlines():
        if l.startswith('## Findings'): f = True
        c = [x.strip() for x in l.split(' | ')]
        if f and l.startswith('| D0-'):
            rows.append((c[0].lstrip('| '), re.sub(r'\(.*', '', c[1]), c[2]))
        elif not f and l.startswith('| [') and len(c) >= 9:
            st[re.sub(r'\(.*', '', c[0].lstrip('| '))] = (c[5], c[6])
    return rows, st
a, sa = parse(open(sys.argv[1]).read()); b, sb = parse(open(sys.argv[2]).read())
ka = {(i, p) for i, p, _ in a}; kb = {(i, p) for i, p, _ in b}
print('rows old', len(a), 'new', len(b))
for k in sorted(ka - kb): print('DROPPED ROW', k)
for k in sorted(kb - ka): print('ADDED ROW', k)
for i, p, l in b:
    o = [x for x in a if x[0] == i and x[1] == p]
    if o and o[0][2] != l: print('LINE', i, p, o[0][2], '->', l)
for p in sorted(set(sa) | set(sb)):
    if sa.get(p, ('-',))[0] != sb.get(p, ('-',))[0]: print('STATUS', p, sa.get(p, ('absent',))[0], '->', sb.get(p, ('absent',))[0])
