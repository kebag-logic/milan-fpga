#!/usr/bin/env python3
"""doc11.py TREE N ADDED GONE: section 11's account of the hot list relearned on the composed flip train, after its
(c) paragraph's last line. Scratch."""
import sys
from pathlib import Path
tree, n, added, gone = Path(sys.argv[1]), *sys.argv[2:5]
p = tree / 'docs/design/SPLIT_CONTROL_MEMORY.md'
t = p.read_text()
a = "  In run order, a function a pass runs after another takes the next cache sets instead of evicting it.\n"
assert t.count(a) == 1
b = a + (f"  On the composed flip train the list is learned again at its head, on the largest legal record's cut "
         f"([section 13](#the-largest-legal-record-on-the-composed-flip-train-665)), by the procedure "
         f"`plat/ctrl_split_hot.txt` records: the backlog windows and, by [#665's ruling of 2026-11-17]"
         f"(https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6959600243), item 1, a third, the "
         f"largest legal AECP command's group, `aecp-largest-notice`, its functions appended after theirs in the order "
         f"it first ran them. That gives {n} entries, {added} added and {gone} gone, none placed by hand; the list's "
         f"header names the three traces by sha256.\n")
p.write_text(t.replace(a, b))
