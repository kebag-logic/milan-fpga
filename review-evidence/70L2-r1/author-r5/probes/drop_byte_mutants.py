#!/usr/bin/env python3
"""Drop exactly one byte of the verdict from gate 1b's census, in a tree copy.

usage: drop_byte_mutants.py <tree> <mutant>

Each mutant rewrites the one range test of rv32_image_references() (the line
the round-3 and round-4 reviews' range mutants rewrite) so that a relocation
landing on byte +k of the verdict is no longer a reference; the other three
bytes are still read. Gate 1b then runs on the unplanted shipping firmware. A
mutant is KILLED when gate 1b fails. Each of the four bytes must be measured by
some control on its own, so each mutant must be killed, and by the control
that reaches only that byte:

  D0_drop_byte0  the shipping firmware itself (milan_init()'s store is on +0)
  D1_drop_byte1  the break folded onto byte +1
  D2_drop_byte2  the break folded onto byte +2 (a +3 break alone misses it)
  D3_drop_byte3  the break folded onto byte +3
"""
import sys
from pathlib import Path

tree, kind = Path(sys.argv[1]), sys.argv[2]
path = tree / "sw/builder/test_builder.py"
text = path.read_text()
OLD = "        if target is not None and not low <= target < high:\n"
BYTE = {"D0_drop_byte0": 0, "D1_drop_byte1": 1, "D2_drop_byte2": 2, "D3_drop_byte3": 3}
new = ("        if target is not None and (not low <= target < high or "
       f"target == low + {BYTE[kind]}):\n")
assert text.count(OLD) == 1, (kind, text.count(OLD))
path.write_text(text.replace(OLD, new, 1))
print(f"mutated {kind} in {path}")
