#!/usr/bin/env python3
"""R843-3-F1's verification at a head: every figure section 13 now states as 8x8/1if's gate, load and every-source rows
equals its receipt, and 0.671 and 154,850 stand only on a line that labels them round 3's.
The section: from "**The gate at 8x8/1if**" to the end of "**The passes over THE SHARE:**" in SPLIT_CONTROL_MEMORY.md,
and the load bullet before it. The receipts: round 6's gate regrade and rows (the head carries their image and
graders but for record_classes.py, which neither reads) and the head's load_grade.py --check log. Prints one line a
figure; exit 1 on any figure missing from the section or its receipt, or a round-3 figure stated unlabelled.
usage: python3 -I f1_check.py CHECKOUT GATE_RECEIPT ROWS_RECEIPT LOAD_CHECK_LOG"""
import re
import sys
from pathlib import Path

checkout, gate, rows, load = (Path(a) for a in sys.argv[1:5])
doc = (checkout / 'docs/design/SPLIT_CONTROL_MEMORY.md').read_text()
start = doc.index('- **The load** at 8x8/1if takes those polls')
end = doc.index('\n', doc.index('- **The passes over THE SHARE:**', start))
section = doc[start:end]
norm = lambda s: s.replace(',', '')  # noqa: E731
receipts = {'gate': norm(gate.read_text()), 'rows': norm(rows.read_text()), 'load': norm(load.read_text())}
FIGURES = {
    'gate': ['114 groups', '1717', '4.860', '7.231', '6.014', '4.629', '6.255', '10.474', '4.114', '2.168', '2.812',
             '26.636', '2.547', '187.397', '190.147', '352 in 113 groups', '142809', '138906', '92744', '2453084',
             '202546'],
    'rows': ['19.82', '126.36', '118.28', '17.83', '325.90', '192.81', '48.37', '48.33', '49.03', '67.24', '134.96',
             '0.969', '1510'],
    'load': ['0.711', '0.673'],
}
bad = 0
for source, figures in FIGURES.items():
    for f in figures:
        in_doc = f in norm(section)
        got = f in receipts[source]
        ok = in_doc and got
        bad += not ok
        print(f'{"ok  " if ok else "BAD "} {f:>18}  section 13: {"yes" if in_doc else "NO"}  {source} receipt: '
              f'{"yes" if got else "NO"}')
for stale in ('0.671', '154,850'):
    for line in (l for l in section.splitlines() if stale in l):
        labelled = re.search(r'round-3|Round-3|round 3', line[:max(0, line.index(stale))])
        bad += not labelled
        print(f'{"ok  " if labelled else "BAD "} {stale:>18}  only as round 3\'s: {"yes" if labelled else "NO"}')
print(f'RESULT: {"PASS" if not bad else "FAIL"}: {bad} bad')
sys.exit(int(bool(bad)))
