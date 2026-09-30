#!/usr/bin/env python3
"""Move the round-4 interior-byte break off an interior byte, in a tree copy's gate 1b.

usage: premise_mutants.py <tree> <mutant>

Each mutant rewrites only the break's C statement, so the gate's own check that
the break lands inside the verdict's bytes and none on the first must refuse it
before the break is graded:

  P1_on_neighbour   `(char *)&milan_verdict_next + 1`: the neighbour's second
                    byte, no reference on the verdict at all
  P2_on_first_byte  `(char *)(&milan_verdict_next - 1)`: the verdict's first
                    byte, the byte every other break already lands on
"""
import sys
from pathlib import Path

tree, kind = Path(sys.argv[1]), sys.argv[2]
path = tree / "sw/builder/test_builder.py"
text = path.read_text()
old = '"(char *)(&milan_verdict_next - 1) + 1);\\n",\n'
MUTANTS = {"P1_on_neighbour": '"(char *)&milan_verdict_next + 1);\\n",\n',
           "P2_on_first_byte": '"(char *)(&milan_verdict_next - 1));\\n",\n'}
assert text.count(old) == 1, text.count(old)
path.write_text(text.replace(old, MUTANTS[kind], 1))
print(f"mutated {kind} in {path}")
