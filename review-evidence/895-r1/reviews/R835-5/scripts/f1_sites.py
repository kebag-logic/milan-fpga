#!/usr/bin/env python3
"""f1_sites.py TREE

Reviewer evidence for R835-5-F1: print each tracked statement that gives an earlier image's figure as the reviewed
head's, beside the head's own value from TREE (its constants and the platform ledger record). Read-only."""
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
SITES = [  # path, line, phrase, the head's figure
    ('sw/firmware/ctrl/plat/README.md', 110, '392 B of `rom` past 60.0',
     'head: 131,752 B in a 131,072 B 60.0 granule, 680 B past (ledger-final summary, section 5 table)'),
    ('docs/reference/FR_NFR.md', 383, 'which the built slice now is',
     'head: CTRL_LOOP_SLICE_US 900 at one interface (ctrl_loop.h), AECP_PACE_MS 9 (aecp_mbx.h)'),
    ('docs/reference/FR_NFR.md', 383, 'there 8 ms holds txL, 48.43 ms',
     'head: 9 ms pace, txL 48.58 ms, last queued 136.65 ms, ACMP 29.63 ms (flip-1x1-1if.log)'),
    ('docs/design/SPLIT_CONTROL_MEMORY.md', 2603, 'at this head a paced edit is at most 245 us',
     'head: dearest edit 23,877 cycles = 255 us, ordinary 225 us (author-r10 classes/plants/summary.md)'),
    ('docs/design/SPLIT_CONTROL_MEMORY.md', 2605, '33.69 at this head',
     'head: tx row 34.00 ms at 1x1/1if (flip-1x1-1if.log)'),
    ('docs/design/SPLIT_CONTROL_MEMORY.md', 2605, '94.99 at this head',
     'head: tx row 104.25 ms at 8x8/2if (flip-8x8-2if.log)'),
    ('docs/design/SPLIT_CONTROL_MEMORY.md', 2606, '1,656 at this head',
     'head: 1,368 B left at 60.5 (section 5 table, ledger-final summary)'),
]
bad = 0
for path, line, phrase, head in SITES:
    text = (tree / path).read_text().splitlines()[line - 1]
    i = text.find(phrase)
    found = i >= 0
    bad += found
    ctx = re.sub(r'\s+', ' ', text[max(0, i - 160):i + len(phrase) + 60]) if found else '(phrase not found)'
    print(f'{path}:{line}: {"PRESENT" if found else "absent"}\n  ...{ctx}...\n  {head}\n')
print(f'{bad} of {len(SITES)} superseded statements present')
