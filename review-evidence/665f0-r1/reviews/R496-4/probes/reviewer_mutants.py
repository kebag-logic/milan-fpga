#!/usr/bin/env python3
"""R496-4 reviewer mutants for the round-4 delta of PR #668 (disposable).

Each mutant is planted into a COPY of sw/firmware/ctrl by the lane's own
ctrl_mutants.plant() and graded by its own `adp` arm. `expect` is True when
the reviewer expects some [FAIL] whose text contains `needle` (arm rc 1);
False when the mutant is expected to survive (recorded as a limit, not a kill).

Usage: reviewer_mutants.py CLONE REUSE_DIR OUT_DIR [--jobs N]
"""
import argparse
import concurrent.futures as cf
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("clone", type=Path)
ap.add_argument("reuse", type=Path)
ap.add_argument("out", type=Path)
ap.add_argument("--jobs", type=int, default=8)
args = ap.parse_args()
sys.path.insert(0, str(args.clone / "sw/firmware/ctrl/test"))
import ctrl_arms  # noqa: E402
import ctrl_mutants  # noqa: E402
from ctrl_build import Tree, Refusal, Outcome  # noqa: E402

M = ctrl_mutants.Mutant
MUTS = [
    (M("rv-cap-three", "adp/adp.h", "#define ADP_DEPARTING_OWED_MAX 2u ", "#define ADP_DEPARTING_OWED_MAX 3u ",
       "adp", "A21"), True),
    (M("rv-cap-le", "adp/adp.c", "a->departing_owed < ADP_DEPARTING_OWED_MAX", "a->departing_owed <= ADP_DEPARTING_OWED_MAX",
       "adp", "A21"), True),
    (M("rv-depart-keeps-oldest-index", "adp/adp.c", "\ta->departing_owed--;\n\ta->departing_index = 0;\n",
       "\ta->departing_owed--;\n", "adp", "DEPARTING 0"), True),
    (M("rv-poll-two-frames", "adp/adp.c", "\tif (a->departing_owed != 0u) {\n\t\tdepart(a);\n\t} else if",
       "\tif (a->departing_owed != 0u) {\n\t\tdepart(a);\n\t\tif (a->departing_owed == 0u && a->available_owed && "
       "a->enabled && a->state == ADP_STATE_DELAY) {\n\t\t\tadvertise(a);\n\t\t}\n\t} else if",
       "adp", "poll"), True),
    (M("rv-queue-counts-as-coalesced", "adp/adp.c",
       "\t\ta->departing_owed++;                                    // queued behind the oldest, carrying 0\n",
       "\t\ta->departing_owed++;\n\t\ta->departing_coalesced++;\n", "adp", "A21"), True),
    (M("rv-coalesce-drops-both", "adp/adp.c", "\t\ta->departing_coalesced++;",
       "\t\ta->departing_coalesced++;\n\t\ta->departing_owed = 0u;", "adp", "A21"), True),
    (M("rv-coalesce-keeps-available-owed", "adp/adp.c",
       "\ta->available_owed = false;                                      // its run is over\n",
       "\tif (a->departing_owed < ADP_DEPARTING_OWED_MAX) a->available_owed = false;\n", "adp", "A21"), True),
    (M("rv-loop-polls-twice", "loop/ctrl_loop.c", "\t\towed = l->polls[i].fn(l->polls[i].ctx) || owed;\n",
       "\t\towed = l->polls[i].fn(l->polls[i].ctx) || owed;\n\t\towed = l->polls[i].fn(l->polls[i].ctx) || owed;\n",
       "adp", "E5"), True),
    (M("rv-owed-passes-inflated", "adp/adp_mbx.h",
       "(ADP_DEPARTING_OWED_MAX + 1u > CTRL_LOOP_EVT_PASSES ? ADP_DEPARTING_OWED_MAX + 1u : CTRL_LOOP_EVT_PASSES)",
       "(9u)", "adp", "E5"), False),
    (M("rv-link-loss-while-disabled-drops-departing", "adp/adp.c",
       "\tbool was = a->link_up;\n\ta->link_up = up;\n",
       "\tbool was = a->link_up;\n\ta->link_up = up;\n\tif (!a->enabled && !up) {\n\t\ta->departing_owed = 0u;\n\t}\n",
       "adp", "A8"), True),
]


def run(item):
    m, expect = item
    root = args.out
    try:
        copy = ctrl_mutants.plant(m, root)
    except Refusal as exc:
        return m.name, expect, "PLANT-REFUSED", str(exc), []
    tree = Tree(copy, root / m.name / "build", args.reuse)
    try:
        oc = ctrl_arms.arm_adp(tree)
    except Refusal as exc:
        oc = Outcome("adp", 2, f"refused: {exc}")
    fails = [ln.strip() for ln in oc.log.splitlines() if "[FAIL]" in ln]
    killed = oc.rc == 1 and any(m.needle in f for f in fails)
    return m.name, expect, ("KILLED" if killed else "SURVIVED") + f" rc={oc.rc}", "", fails


bad = 0
with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
    for name, expect, verdict, err, fails in ex.map(run, MUTS):
        good = verdict.startswith("KILLED") == expect
        bad += 0 if good else 1
        print(f"[{'as-expected' if good else 'UNEXPECTED'}] {name}: {verdict} (expected "
              f"{'kill' if expect else 'survive'}) {err} failed={len(fails)}")
        for f in fails[:3]:
            print(f"    {f}")
print(f"reviewer mutants: {len(MUTS) - bad} of {len(MUTS)} as expected")
sys.exit(1 if bad else 0)
