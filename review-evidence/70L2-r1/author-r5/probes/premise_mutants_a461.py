#!/usr/bin/env python3
"""Move one of the round-5 interior-byte breaks off its byte, in a tree copy's gate 1b.

usage: premise_mutants_a461.py <tree> <mutant>

Each mutant rewrites only one break's C statement, so the gate's own check that
the break's references from nvm_boot() land on its byte and no other must refuse
it before any break is graded:

  Q2_on_neighbour  the +2 break moved to `+ 6`: the neighbour's third byte, no
                   reference on the verdict at all ("byte(s) []")
  Q3_on_byte1      the +3 break moved to `+ 1`: an interior byte, but the one
                   the +1 break already measures ("byte(s) [1]", not +3)
"""
import sys
from pathlib import Path

tree, kind = Path(sys.argv[1]), sys.argv[2]
path = tree / "sw/builder/test_builder.py"
text = path.read_text()
MUTANTS = {
    "Q2_on_neighbour": ('"(char *)(&milan_verdict_next - 1) + 2);\\n",\n',
                        '"(char *)(&milan_verdict_next - 1) + 6);\\n",\n'),
    "Q3_on_byte1": ('"(char *)(&milan_verdict_next - 1) + 3);\\n",\n',
                    '"(char *)(&milan_verdict_next - 1) + 1);\\n",\n'),
}
old, new = MUTANTS[kind]
assert text.count(old) == 1, (kind, text.count(old))
path.write_text(text.replace(old, new, 1))
print(f"mutated {kind} in {path}")
