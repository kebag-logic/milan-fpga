#!/usr/bin/env python3
"""Each reviewer mutant, as published in its probe, has the same edit as its MUTANTS entry.

usage: python3 -I -B same_edits.py <tree> <probe.py> <published name>=<MUTANTS name> ...
The probe's MINE dict is read by running its source only up to its first use of its arguments' names.
"""
import sys
from pathlib import Path

tree, probe = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
pairs = [arg.split("=") for arg in sys.argv[3:]]
sys.path.insert(0, str(tree / "scripts"))
import process_test_support as pts  # noqa: E402

source = probe.read_text()
head = source[:source.index("names = sys.argv[3:]")]
scope = {"__file__": str(probe), "__name__": "probe"}
saved = sys.argv
sys.argv = [str(probe), str(tree), "1"]
exec(compile(head, str(probe), "exec"), scope)
sys.argv = saved
bad = 0
for published, ours in pairs:
    edit = tuple(scope["MINE"][published])
    same = tuple(pts.MUTANTS[ours][2:]) == (edit,)
    bad += not same
    print(f"{published} = {ours}: {'same edit' if same else 'DIFFERENT'}; {ours} names {pts.MUTANTS[ours][0]}")
sys.exit(1 if bad else 0)
