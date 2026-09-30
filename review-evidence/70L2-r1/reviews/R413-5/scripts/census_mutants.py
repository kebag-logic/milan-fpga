#!/usr/bin/env python3
"""Plant one reviewer mutant into a tree COPY of sw/builder/test_builder.py.

usage: census_mutants.py <tree> <mutant>

Census-range narrowings (rv32_image_references()'s one range test):
  X0..X3   drop exactly byte +k of the verdict
  P1,P2,P3 read only the first 1, 2 or 3 bytes
  S1       skip the first byte, read +1..+3
  O1       read byte +1 only
  EV       read even bytes only (+0, +2)
Verdict extent narrowings (verdict_image_pins()'s low/high):
  H1,H2,H3 the verdict's extent taken as 1, 2 or 3 bytes
Premise (gate's own control data) mutants:
  B2TO4    the +2 break's offset moved onto the neighbour (+4)
  B3TO1    the +3 break's offset moved onto +1
  B3TO0    the +3 break's offset moved onto +0
Necessity pairs (a control removed AND a narrowing planted):
  NO2_X2   +2 break removed, byte +2 dropped
  NO3_X3   +3 break removed, byte +3 dropped
  NO3_P3   +3 break removed, only first three bytes read
"""
import sys
from pathlib import Path

tree, kind = Path(sys.argv[1]), sys.argv[2]
path = tree / "sw/builder/test_builder.py"
text = path.read_text()

RANGE = "        if target is not None and not low <= target < high:\n"
EXTENT = ('        low, high = verdict["value"], verdict["value"] + '
          'verdict["size"]\n')


def sub(old, new):
    global text
    assert text.count(old) == 1, (kind, old, text.count(old))
    text = text.replace(old, new, 1)


def rng(cond):
    sub(RANGE, f"        if target is not None and ({cond}):\n")


def drop_break(k):
    old = (f"        {k}: in_nvm_boot(\"static int milan_verdict_next;\\n\",\n")
    start = text.index(old)
    end = text.index(f"\"verdict address on interior byte +{k}\"),\n", start)
    end += len(f"\"verdict address on interior byte +{k}\"),\n")
    sub(text[start:end], "")


def move_break(k, to):
    sub(f"\"(char *)(&milan_verdict_next - 1) + {k});\\n\",",
        f"\"(char *)(&milan_verdict_next - 1) + {to});\\n\",")


table = {
    **{f"X{k}": (lambda k=k: rng(f"not low <= target < high or "
                                 f"target == low + {k}")) for k in range(4)},
    **{f"P{n}": (lambda n=n: rng(f"not low <= target < low + {n}"))
       for n in (1, 2, 3)},
    "S1": lambda: rng("not low + 1 <= target < high"),
    "O1": lambda: rng("not low + 1 <= target < low + 2"),
    "EV": lambda: rng("not low <= target < high or (target - low) % 2"),
    **{f"H{n}": (lambda n=n: sub(EXTENT, '        low, high = '
                                 'verdict["value"], verdict["value"] + '
                                 f'{n}\n')) for n in (1, 2, 3)},
    "B2TO4": lambda: move_break(2, 4),
    "B3TO1": lambda: move_break(3, 1),
    "B3TO0": lambda: move_break(3, 0),
    "NO2_X2": lambda: (drop_break(2),
                       rng("not low <= target < high or target == low + 2")),
    "NO3_X3": lambda: (drop_break(3),
                       rng("not low <= target < high or target == low + 3")),
    "NO3_P3": lambda: (drop_break(3), rng("not low <= target < low + 3")),
}
table[kind]()
path.write_text(text)
print(f"mutated {kind} in {path}")
