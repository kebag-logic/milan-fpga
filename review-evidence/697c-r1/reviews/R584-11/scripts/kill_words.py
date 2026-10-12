#!/usr/bin/env python3
"""Every (arm, test, words) a plant of the control campaign names must be findable: the test's name and its words
in the test sources the arms compile (the stack's tests/ and the firmware's test/ and gtest/). A kill whose words
appear nowhere can never be caught. usage: kill_words.py <tree>"""
import sys, re
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(tree / "sw/firmware/ctrl/test"), str(tree / "sw/firmware/gtest")]
import ctrl_mutants
srcs = list((tree / "third_party/tsn-c-stack/tests").glob("*.[ch]pp")) + \
       list((tree / "sw/firmware/ctrl/test").glob("*.[ch]pp")) + list((tree / "sw/firmware/gtest").glob("*.[ch]pp"))
text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in srcs)
flat = re.sub(r'"\s*\n\s*"', "", text)  # join adjacent string literals split over lines
missing = []
for m in ctrl_mutants.MUTANTS:
    for arm, test, words in m.kills():
        name = test.split(".")[-1] if test else ""
        ok_name = (not name) or name in text
        ok_words = words in flat or words in text
        if not (ok_name and ok_words):
            missing.append((m.name, arm, test, words, ok_name, ok_words))
print(f"plants {len(ctrl_mutants.MUTANTS)}, kills {sum(len(m.kills()) for m in ctrl_mutants.MUTANTS)}, "
      f"kills whose test or words are in no test source: {len(missing)}")
for row in missing[:40]:
    print("  ", row)
