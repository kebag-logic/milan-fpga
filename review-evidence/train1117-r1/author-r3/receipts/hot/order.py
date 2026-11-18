#!/usr/bin/env python3
"""order.py MAP TRACE... : the hot list ctrl_split_hot.txt's recorded procedure learns, from committed-PC traces.

Each traced PC (the testbench's `PC <cpu cycle> <pc>` lines, BUDGET_TRACE_AFTER / BUDGET_TRACE_PCS) is mapped through
the image's link map to the input section that holds it, `.text.<function>` of `<n>-<stem>.o` (or an archive's member),
named as ctrl_hot.py names an entry, `<stem> <function>`. The list is every such section the traces ran, in the order
they first ran it, the traces taken in the order given. Prints the list, then a `#`-prefixed summary on stderr."""
import bisect
import re
import sys

SECTION = re.compile(r"^ \.text\.(\S+)\s+(0x[0-9a-f]+)\s+(0x[0-9a-f]+)\s+\S*/"
                     r"(?:\d+-([A-Za-z0-9_]+)\.o|([A-Za-z0-9_.]+\.a)\(([A-Za-z0-9_]+)\.o\))$", re.M)
text = open(sys.argv[1]).read()
body = text[text.index('Linker script and memory map'):]
spans = []
for name, addr, size, stem, archive, member in SECTION.findall(body):
    a, n = int(addr, 16), int(size, 16)
    if n:
        spans.append((a, a + n, stem or f'{archive}:{member}', name))
spans.sort()
starts = [s[0] for s in spans]
order, seen, unmapped, pcs = [], set(), 0, 0
for trace in sys.argv[2:]:
    for line in open(trace):
        f = line.split()
        if len(f) != 3 or f[0] != 'PC':
            continue
        pcs += 1
        pc = int(f[2], 16)
        k = bisect.bisect_right(starts, pc) - 1
        if k < 0 or not spans[k][0] <= pc < spans[k][1]:
            unmapped += 1
            continue
        e = (spans[k][2], spans[k][3])
        if e not in seen:
            seen.add(e)
            order.append(e)
for stem, name in order:
    print(f'{stem} {name}')
print(f'# {len(order)} sections from {pcs} committed PCs ({unmapped} outside any .text.<function> section)',
      file=sys.stderr)
