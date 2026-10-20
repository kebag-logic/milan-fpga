#!/usr/bin/env python3
"""plant.py SRC DST ANCHOR REPLACEMENT : copy SRC to DST with ANCHOR replaced once.
Refuses unless ANCHOR occurs exactly once in SRC (a mutant that mutates nothing proves nothing)."""
import sys
src, dst, anchor, repl = sys.argv[1:5]
anchor = anchor.encode().decode("unicode_escape")
repl = repl.encode().decode("unicode_escape")
text = open(src).read()
n = text.count(anchor)
if n != 1:
    sys.exit(f"anchor occurs {n} times in {src}, expected 1")
open(dst, "w").write(text.replace(anchor, repl))
print(f"planted into {dst}")
