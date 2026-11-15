#!/usr/bin/env python3
"""Check published rounding, per-image growth, and attribution arithmetic.
Usage: python3 audit_timing.py EVIDENCE_ROOT REPOSITORY
"""
import pathlib
import re
import sys
base, root = map(pathlib.Path, sys.argv[1:])
sys.path.insert(0, str(root/'tb/verilator/ctrl_service_budget'))
import record_classes as rc
def rule(cycles):
    return ((cycles*21+9999)//10000)*5
row = re.compile(r'^(.*?)\s+([\d,]+)\s+(\d+\.\d+)\s+(\d+)\s+(\d+)\s+(within|OVER-raw|OVER)\s+(.*)$')
errors = []
for name in ('compare-1x1.txt', 'compare-1x1-E1-B1F.txt', 'compare-8x8.txt'):
    text = (base/'author-r13/receipts/compare'/name).read_text().split('\n# ')[0]
    n = 0
    over = []
    for line in text.splitlines():
        match = row.match(line)
        if not match:
            continue
        key, cyc, us, rounded, stated, verdict, where = match.groups()
        cyc, rounded, stated = int(cyc.replace(',', '')), int(rounded), int(stated)
        n += 1
        expected = 'OVER-raw' if cyc > stated*100 else 'OVER' if rule(cyc) > stated else 'within'
        if rounded != rule(cyc) or abs(float(us)-cyc/100) > .005 or verdict != expected:
            errors.append((name, line, rule(cyc), expected))
        if verdict != 'within':
            over.append((key, cyc, rounded, stated, where))
    print(name, 'rows checked', n, 'exceptions', len(over))
    for item in over:
        print('  EXCEPTION', item)
for tag in ('b1','b8'):
    p = base/f'author-r12/receipts/attribution/budget-{tag}-frame.txt'
    vals = list(map(int, re.search(r'^span\s+([\d ]+)$', p.read_text(), re.M)[1].split()))
    assert sum(vals[:-1]) == vals[-1]
    print('Attribution', tag, vals, 'sum verified')
p = base/'author-r12/receipts/images/rom-per-image.txt'
for line in p.read_text().splitlines():
    if line.startswith('#'):
        continue
    name, a,b,c,d1,d2,cap,*_ = line.split()
    a,b,c,d1,d2,cap = map(int, (a,b,c,d1,d2,cap))
    assert b-a == d1 and c-b == d2 and c <= cap
    print('ROM', name, a,b,c, 'growth', d1,d2, 'cap spare', cap-c)
for cycles in (33724,28509,78332,55377,28376,56474,69635,6206,14715,4784,4692):
    print('RULE', cycles, 'cycles ->', rule(cycles), 'us')
# A remaining optional limit of response-based attribution: a gap response
# can name a completed unanswered span, even though a later span cannot.
records = rc.named([(0,23000),(1000000,22500)], [(40000,6,0),(1010000,45,0)])
leg = rc.Leg('1x1/1if', 'answering-ports', 100000000, 100000000, {'aecp-fanout': records})
classified = rc.classes(leg, 'aecp-fanout', {'long':975, 'paced':300, 'other':235, 'pace_ms':8})
print('Attribution gap probe:', records[0], 'actual span ends 23000, response 40000, class', classified[0][0])
assert records[0].command == 6 and classified[0][0] == 'paced'
print('This demonstrates an optional attribution limit, not an observed misclassification in published runs.')
for e in errors:
    print('ERROR', e)
print('Arithmetic audit:', 'FAIL' if errors else 'PASS')
sys.exit(bool(errors))
