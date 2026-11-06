#!/usr/bin/env python3
"""R784-3: the README's mutant table against MUTANTS, the delta's added source lines against the comment rule, and
the mutant and check counts in the README and PR body. usage: doc_scan.py TREE PR_BODY DIFF_FILE"""
import re, sys
from pathlib import Path
tree, body, diff = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).read_text(), Path(sys.argv[3]).read_text()
h = tree / 'tb/verilator/ctrl_service_hooks'
sys.path.insert(0, str(h))
import hooks_selftest as t  # noqa: E402
readme = (h / 'README.md').read_text()
rows = re.findall(r'^\| ([^|]+?) \| ([^|]+?) \|$', readme, re.M)
table = {a.replace('\\|', '|'): b for a, b in rows}
names = {m[0]: m[2] for m in t.MUTANTS}
print('mutants', len(names), 'checks', len(t.CHECKS))
print('in MUTANTS, not in README:', [n for n in names if n not in table])
print('wrong check in README:', [n for n in names if n in table and table[n] != names[n]])
order = [a for a, _ in rows if a in names]
print('README order equals MUTANTS order:', order == list(names))
added = [l[1:] for l in diff.splitlines() if l.startswith('+') and not l.startswith('+++')]
bad = re.compile(r'\b(R78[34]|A702|B\d{1,2}\b|round \d|issuecomment|lane\b|F-\d|reviewer)', re.I)
print('comment-rule hits in added hooks_selftest.py lines:', [l.strip()[:100] for l in added if bad.search(l)])
print('over 120 columns:', [l[:60] for l in added if len(l) > 120])
for text, label in ((readme, 'README'), (body, 'PR body')):
    print(label, 'mutant counts:', sorted(set(re.findall(r'\b(\d+) (?:of \d+ )?mutants', text))), 'checks:', sorted(set(re.findall(r'\b(\d+) of \d+ checks', text))))
    for pat in ('change none', 'changes no verdict', 'change no verdict', 'every rule of the held'):
        print('   stale', repr(pat), text.count(pat))
