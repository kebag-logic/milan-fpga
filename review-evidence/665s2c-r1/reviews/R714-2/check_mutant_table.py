"""Compare the README's mutant table with the self-test's caught-mutant lines.

Usage: python3 -I check_mutant_table.py <README.md> <self-test log>
Every README row's mutant must be caught, by a line naming the README's check
(or the refusal the README says it names), and the counts must match.
"""
import re
import sys

readme, log = (open(p).read() for p in sys.argv[1:3])
start = readme.index('Then [`selftest_mutants.py`]')
body = readme[start:readme.index('A mutant whose name ends', start)]
rows = [(m.strip(), c.strip()) for m, c in re.findall(r'^\| (.+?) \| (.+?) \|$', body, re.M)
        if not set(m) <= set('-: ') and m.strip().lower() != 'mutant']
lines = re.findall(r'^MUTANT caught: (.+)$', log, re.M)
print('README rows', len(rows), 'caught lines', len(lines))
bad = []
for name, check in rows:
    hit = [l[len(name) + 2:] for l in lines if l.startswith(name + ': ')]
    if len(hit) != 1:
        bad.append((name, 'caught lines', len(hit)))
    elif check not in hit[0] and 'refus' not in check.lower():
        bad.append((name, check, hit[0][:160]))
print('mismatches', len(bad))
for b in bad:
    print(' ', b)
