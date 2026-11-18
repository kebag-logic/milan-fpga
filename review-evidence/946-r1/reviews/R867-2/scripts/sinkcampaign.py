#!/usr/bin/env python3
"""Reviewer probe for #946 round 2: plant the sink table (sink_mutants.py) and reviewer-written extra defects through
the control campaign's own planter and kill check (ctrl_mutants.plant / caught), on copies under OUT.

usage: sinkcampaign.py REPO OUT {table|extra} [--jobs N] [--slice K/N]"""
import argparse, sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("repo", type=Path)
ap.add_argument("out", type=Path)
ap.add_argument("which", choices=("table", "extra"))
ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--slice", default="1/1")
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
    table = (
        # the applied wrap reports a redo outside a wait: a stale redo reaches the next change
        Mutant("rv-redo-outside-wait", P, "\tsinks.redo = applied && core->waiting;\n", "\tsinks.redo = applied;\n",
               "platsinks8", S.S2, "S2"),
        # the change port never clears the redo it consumed
        Mutant("rv-redo-never-cleared", P, "\tsinks.redo = false;\n\tsinks.changed", "\tsinks.changed",
               "platsinks8", S.S4, "S4"),
        # the change port writes only a redo, never a change the face applied at once
        Mutant("rv-immediate-unwritten", P, S.KEPT, "\tif (redo) {", "platsinks8", S.S2, "S2"),
        # the bound check reads the ACMP's published binding instead of its bound state
        Mutant("rv-held-published", P, "\t\t\t\tbound |= v.bound;\n",
               "\t\t\t\tbound |= ctrl_plat.app.acmp.acmp.sinks[d->index].published_bound;\n",
               "platsinks8", S.S7, "S7"),
        # the bound check reads the input's settled stream only
        Mutant("rv-held-stream", P, "\t\t\t\tbound |= v.bound;\n", "\t\t\t\tbound |= v.stream.stream_id != 0u;\n",
               "platsinks8", S.S7, "S7"),
        # the wrap refuses every waiting change, bound or not (over-refusal)
        Mutant("rv-refuse-every-wait", P, S.REFUSE, "!core->waiting", "platsinks8", S.S4, "S4"),
        # refusal also blocks a change of another kind on a bound input (over-refusal of SET_NAME etc.)
        Mutant("rv-held-any-kind", P, "\tbool one = kind == AECP_CHANGE_FORMAT && type == STREAM_INPUT;\n",
               "\tbool one = true;\n", "platsinks8", S.S5, "S5"),
    )
ctrl_mutants.MUTANTS = table
ctrl_mutants.unnamed_tests = lambda: []
k, n = (int(x) for x in a.slice.split("/"))
a.out.mkdir(parents=True, exist_ok=True)
failed = ctrl_mutants.campaign(a.out, a.out / "reuse", a.jobs, (k, n))
sys.exit(1 if failed else 0)
