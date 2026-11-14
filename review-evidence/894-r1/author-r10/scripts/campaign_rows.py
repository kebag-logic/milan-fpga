#!/usr/bin/env python3
"""Run named rows of a tree's AECP campaign (aecp_mutants.campaign, the controls() check first) and nothing else.

usage: campaign_rows.py TREE OUT NAME...
Imports the campaign from TREE/sw/firmware/ctrl/test, keeps only the DEFECTS rows NAME..., and runs them with the
campaign's own planting, arms and graders into OUT (which it creates). Prints the campaign's [ok]/[ESCAPED] lines;
exit 1 when any row escaped, as the campaign's own exit."""
import sys
from pathlib import Path

tree, out, names = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3:]
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
import aecp_mutants  # noqa: E402

aecp_mutants.controls()
rows = tuple(d for d in aecp_mutants.DEFECTS if d.name in names)
assert len(rows) == len(names), ("unknown rows", set(names) - {d.name for d in rows})
aecp_mutants.controls = lambda: None  # run once above, against the whole table
aecp_mutants.DEFECTS = rows
raise SystemExit(int(aecp_mutants.campaign(out, jobs=8)))
