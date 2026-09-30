#!/usr/bin/env python3
"""Plant one round-4 reviewer mutant of gate 1b's address range into a tree.

usage: r413_census_mutants.py <tree> <mutant>

Each mutant narrows the byte range rv32_image_references() reads at the
exact head; the WHOLE gate 1b then runs on the unplanted shipping firmware.
A mutant is KILLED when gate 1b fails, SURVIVES when it passes.

  N1_first_two_bytes  only bytes [low, low+2) are references
  N2_first_three      only bytes [low, high-1) are references (drops +3)
  N3_skip_first_byte  only bytes (low, high) are references (drops +0)
  N4_second_byte_only only relocations whose target is low+1 are references
"""
import sys
from pathlib import Path

tree, kind = Path(sys.argv[1]), sys.argv[2]
path = tree / "sw/builder/test_builder.py"
text = path.read_text()
OLD = "        if target is not None and not low <= target < high:\n"
MUTANTS = {
    "N1_first_two_bytes":
        "        if target is not None and not low <= target < low + 2:\n",
    "N2_first_three":
        "        if target is not None and not low <= target < high - 1:\n",
    "N3_skip_first_byte":
        "        if target is not None and not low < target < high:\n",
    "N4_second_byte_only":
        "        if target is not None and target not in (low, low + 1):\n",
}
assert text.count(OLD) == 1, (kind, text.count(OLD))
path.write_text(text.replace(OLD, MUTANTS[kind], 1))
print(f"mutated {kind} in {path}")
