#!/usr/bin/env python3
"""count_defects.py TESTDIR: import the AECP campaign table from TESTDIR and print its size, its distinct names,
the rows graded by the map-edit definition test and whether map-read-before-legal is among them."""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
import aecp_mutants, aecp_map_mutants
D = aecp_mutants.DEFECTS
edit = [d.name for d in D if any(t == aecp_map_mutants.EDIT for t, _ in d.checks)]
print(f"DEFECTS {len(D)} distinct {len({d.name for d in D})}")
print(f"graded by {aecp_map_mutants.EDIT}: {len(edit)}; map-read-before-legal among them: {'map-read-before-legal' in edit}")
print("rows:", " ".join(edit))
