#!/usr/bin/env python3
"""Instrument a tree copy's gate 1b to print each planted verdict break's refusal.

usage: print_break_refusals.py <tree> [<mutant-name>]

Inserts one print just after gate 1b records a planted break as refused, so the
log carries each break's name and the resolver's refusal text (the pins named),
and the premise bytes each interior break reached. With a second argument it is
a no-op mutant name for stop_run.sh, which calls it as `<script> <tree> <name>`.
Run it with the round-4 external review's r413_stop_after_breaks.py (R413_STOP=1)
so the gate stops right after its verdict controls.
"""
import sys
from pathlib import Path

path = Path(sys.argv[1]) / "sw/builder/test_builder.py"
text = path.read_text()
anchor = "                verdict_pin_refused.append(what)\n"
assert text.count(anchor) == 1
probe = anchor + ('                print("A461 BREAK REFUSED:", what, "::",\n'
                  '                      " ".join(str(exc).split()).split("because: ")[-1][:600],\n'
                  '                      flush=True)\n')
premise = "            verdict_interior_bytes.extend(reached)\n"
assert text.count(premise) == 1
premise_probe = premise + ('            print(f"A461 PREMISE +{offset}: nvm_boot() reaches byte(s) {reached}",\n'
                           '                  flush=True)\n')
path.write_text(text.replace(anchor, probe, 1).replace(premise, premise_probe, 1))
print("instrumented", path)
