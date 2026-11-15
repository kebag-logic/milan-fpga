#!/usr/bin/env python3
"""Round 20, item 4: every sentence of SPLIT_CONTROL_MEMORY.md section 13 from :2189 to its end (THE TIERS' queued
notices onward) that carries a figure with a unit and no history marker, one a line, for reading against the head's
graders (flip_grade.py --check at both points, load_grade.py --check, poll_grade.STATED_US, record_classes.py's
round-13 output and the headers' constants). Run from the tree's top."""
import re

L = open('docs/design/SPLIT_CONTROL_MEMORY.md', encoding='utf-8').read().split('\n')
end = next(i for i, s in enumerate(L, 1) if s.startswith('## 14'))
SENT = re.compile(r'(?<=[.;])\s+(?=[A-Z`(*\[])')
HIST = re.compile(r"\b(was|were|had|before|then|earlier|previously|at round|round \d+'s|since|by the 2026|record of|"
                  r"at that head|used to|no longer|would|stated before|from \d+ to)\b", re.I)
NUM = re.compile(r'(?<![\w.])\d[\d,]*(?:\.\d+)?\s?(?:ms|us|%|x|cycles|B|KiB)\b')
n = 0
for i in range(2189, end):
    s = L[i - 1]
    if s.startswith('|---'):
        continue
    for k, sent in enumerate(SENT.split(s)):
        if NUM.search(sent) and not HIST.search(sent):
            n += 1
            print(f'{i}.{k}\t{sent[:300]}')
print(f'# {n} sentences, :2189 to :{end - 1}')
