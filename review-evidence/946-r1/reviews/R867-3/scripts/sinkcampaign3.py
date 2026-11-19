#!/usr/bin/env python3
"""Reviewer probe for #946 round 3: plant the sink table (sink_mutants.py) or reviewer-written defects through the
control campaign's own planter and kill check (ctrl_mutants.campaign), on copies under OUT.

usage: sinkcampaign3.py REPO OUT {table|rv} [--jobs N]
rv: the reviewer's own two plants of round 2 in their original spelling (the type test dropped, the kind test
dropped), each required to fail S11 on its own words, plus round 2's seven wrap plants unchanged."""
import argparse, sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("repo", type=Path)
ap.add_argument("out", type=Path)
ap.add_argument("which", choices=("table", "rv"))
ap.add_argument("--jobs", type=int, default=4)
a = ap.parse_args()
sys.path.insert(0, str(a.repo / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(a.repo / "sw/firmware/gtest"))
import ctrl_mutants, sink_mutants  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402

S = sink_mutants
if a.which == "table":
    table = tuple(sink_mutants.mutants(Mutant))
else:
    P = S.PLAT
    ONE = "\tbool one = kind == AECP_CHANGE_FORMAT && type == STREAM_INPUT;\n"
    table = (
        Mutant("rv-one-type-dropped", P, ONE, "\tbool one = kind == AECP_CHANGE_FORMAT;\n",
               "platsinks8", S.S11, "is taken while input"),
        Mutant("rv-one-kind-dropped", P, ONE, "\tbool one = type == STREAM_INPUT;\n",
               "platsinks8", S.S11, "writes no context"),
        Mutant("rv-redo-outside-wait", P, "\tsinks.redo = applied && core->waiting;\n", "\tsinks.redo = applied;\n",
               "platsinks8", S.S2, "S2"),
        Mutant("rv-redo-never-cleared", P, "\tsinks.redo = false;\n\tsinks.changed", "\tsinks.changed",
               "platsinks8", S.S4, "S4"),
        Mutant("rv-immediate-unwritten", P, S.KEPT, "\tif (redo) {", "platsinks8", S.S2, "S2"),
        Mutant("rv-held-published", P, "\t\t\t\tbound |= v.bound;\n",
               "\t\t\t\tbound |= ctrl_plat.app.acmp.acmp.sinks[d->index].published_bound;\n",
               "platsinks8", S.S7, "S7"),
        Mutant("rv-held-stream", P, "\t\t\t\tbound |= v.bound;\n", "\t\t\t\tbound |= v.stream.stream_id != 0u;\n",
               "platsinks8", S.S7, "S7"),
        Mutant("rv-refuse-every-wait", P, S.REFUSE, "!core->waiting", "platsinks8", S.S4, "S4"),
        Mutant("rv-held-any-kind", P, ONE, "\tbool one = true;\n", "platsinks8", S.S5, "S5"),
    )
ctrl_mutants.MUTANTS = table
ctrl_mutants.unnamed_tests = lambda: []
a.out.mkdir(parents=True, exist_ok=True)
failed = ctrl_mutants.campaign(a.out, a.out / "reuse", a.jobs, (1, 1))
sys.exit(1 if failed else 0)
