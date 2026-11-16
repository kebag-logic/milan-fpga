#!/usr/bin/env python3
"""Run a named subset of the AECP campaign's planted defects (aecp_mutants.campaign over them alone).
usage: some_plants.py OUTPUT NAME... (or @FILE of names); run from the tree's root."""
import sys
from pathlib import Path
sys.path[:0] = ['sw/firmware/ctrl/test', 'sw/firmware/gtest']
import aecp_mutants as am
out, names = Path(sys.argv[1]), sys.argv[2:]
if names and names[0].startswith('@'):
    names = Path(names[0][1:]).read_text().split()
picked = tuple(d for d in am.DEFECTS if d.name in names)
missing = set(names) - {d.name for d in picked}
assert not missing, missing
am.controls()  # the whole table: every test owned, the reader's controls
am.controls = lambda: None
am.DEFECTS = picked
from ctrl_build import STACK
escaped = am.campaign(out, jobs=4, stack=STACK.resolve())
print('ESCAPED' if escaped else f'all {len(picked)} caught')
sys.exit(int(escaped))
