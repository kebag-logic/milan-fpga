#!/usr/bin/env python3
"""For every figure the R421-4 receipt lists as dropped from a round, find it in
that round's validation section of the linked archived body.

The round-4 receipt line format is
  "  OLD figures with no occurrence in NEW Round N: ['41', ...]"
Round sections of the linked body: text before '## Round 2' is round 1, then each
'## Round N' block; the validation section is the round's '#+ Validation...'
heading up to the next heading of the same or higher level.

usage: dropped_in_linked.py R421-4_RECEIPT.txt LINKED_BODY.md
"""
import ast
import re
import sys

NUM = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?")
receipt, linked = open(sys.argv[1]).read(), open(sys.argv[2]).read()

parts = re.split(r"(?m)^## (Round [0-9a-z]+)\s*$", linked)
rounds = {"Round 1": parts[0]}
for i in range(1, len(parts), 2):
    rounds[parts[i]] = parts[i + 1]


def validation(text):
    m = re.search(r"(?m)^(#+) Validation[^\n]*$", text)
    lvl = len(m.group(1))
    rest = text[m.end():]
    n = re.search(r"(?m)^#{1,%d} " % lvl, rest)
    return m.group(0), rest[: n.start()] if n else rest


total = missing = 0
for rnd, lst in re.findall(r"OLD figures with no occurrence in NEW (Round \w+): (\[.*?\])", receipt):
    figs = ast.literal_eval(lst)
    head, sec = validation(rounds[rnd])
    secnums = set(NUM.findall(sec))
    roundnums = set(NUM.findall(rounds[rnd]))
    in_sec = [f for f in figs if f in secnums]
    elsewhere = [f for f in figs if f not in secnums and f in roundnums]
    absent = [f for f in figs if f not in roundnums]
    total += len(figs)
    missing += len(absent)
    print(f"{rnd}: {len(figs)} dropped figures; in '{head.strip()}' of the linked body: {len(in_sec)}; "
          f"only elsewhere in the round (prose, not a table figure): {elsewhere}; absent from the round: {absent}")
print(f"\nTOTAL dropped figures {total}; absent from the linked body's same round: {missing}")
sys.exit(1 if missing else 0)
