#!/usr/bin/env python3
"""Classify killer changes between source and exported mutation tables.

Usage: classify_killers.py SOURCE_MUTANTS.json EXPORT_MUTATIONS.json EXPORT_TESTS_DIR
For each changed mutant, says whether each source killer test still exists in
the exported tests (a retained killer that was replaced is a possible weakening).
"""
import json, re, sys
from pathlib import Path
src = {m['name']: m for m in json.load(open(sys.argv[1]))}
exp = json.load(open(sys.argv[2]))
names = set()
for p in Path(sys.argv[3]).glob('*.cpp'):
    for m in re.finditer(r'^(?:TEST|TEST_F|TEST_P)\((\w+),\s*(\w+)\)', p.read_text(), re.M):
        names.add(m[1] + '.' + m[2])
def canon(t):
    t = t.rstrip('/')
    return t.split('/')[1] if '/' in t else t
retained_changed = []
generic = []
for e in exp:
    s = src[e['name']]
    sk = sorted((canon(k[1]), k[2]) for k in s['kills'])
    ek = sorted((canon(k['test']), k['needle']) for k in e['kills'])
    for k in e['kills']:
        if len(k['needle']) < 16:
            generic.append((e['name'], k['test'], k['needle']))
    if sk == ek:
        continue
    for t, n in sk:
        if t in names and (t, n) not in ek:
            retained_changed.append((e['name'], t, n, ek))
print('killers whose source test is retained but the (test, needle) pair was dropped:')
for r in retained_changed:
    print(' ', r)
print('short needles (<16 chars):')
for g in generic:
    print(' ', g)
