#!/usr/bin/env python3
"""README mutant table against MUTANTS, and a scan of the added source lines of the delta.

usage: doc_parity.py TREE CLONE
"""
import re, subprocess, sys
from pathlib import Path
tree, clone = Path(sys.argv[1]).resolve(), sys.argv[2]
H = tree / 'tb/verilator/ctrl_service_hooks'
sys.path.insert(0, str(H)); sys.dont_write_bytecode = True
import hooks_selftest as st
text = (H / 'README.md').read_text()
rows = re.findall(r'^\| ([^|]+?) \| ([^|]+?) \|$', text, re.M)
names = {m[0]: m[2] for m in st.MUTANTS}
doc = {a.replace('\\|', '|'): b for a, b in rows if a in names}
print('MUTANTS', len(names), 'README rows matched', len(doc), 'absent', [n for n in names if n not in doc][:5],
      'wrong check', [n for n in doc if doc[n] != names[n]][:5])
print('amended mutants', sum(n.startswith('amended:') for n in names))
d = subprocess.run(['git', '-C', clone, 'diff', '--no-color', '-U0', '26ba56e1', '3f8caae5eca7e681c3452eacdd818d1033a89f8d'], capture_output=True, text=True).stdout
added = [l[1:] for l in d.split('\n') if l.startswith('+') and not l.startswith('+++')]
print('added lines', len(added))
pat = re.compile(r'\b(R7\d\d|R\d+-\d|A\d{2,3}[a-z]?|B\d{2}|F-\d|issuecomment|S\d\b|round \d)|—')
print('lane, reviewer, round or comment id hits:', [l[:90] for l in added if pat.search(l)])
print('control, the pattern on a planted line:', bool(pat.search('# per R783-2 F1, B17')))
lines = text.split('\n')
for n in (206, 459, 469):
    print(n, lines[n - 1][:110])
