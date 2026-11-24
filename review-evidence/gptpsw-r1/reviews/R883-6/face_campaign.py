#!/usr/bin/env python3
"""Run only the AECP face-mutant rows (aecp_face_mutants.ROWS) through the repository's own
aecp_mutants.campaign() grader, plus a control row that re-plants the AS_CAPABLE leak under the
PREVIOUS needle wording, which must now be reported ESCAPED (needle no longer present in the assertion).

Usage: python3 face_campaign.py <checkout> <output-dir> [--jobs N] [--only NAME]
"""
import argparse
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("checkout", type=Path)
ap.add_argument("output", type=Path)
ap.add_argument("--jobs", type=int, default=16)
ap.add_argument("--only", default=None)
ap.add_argument("--old-needle-control", action="store_true")
ap.add_argument("--interfaces", type=int, default=2)
ap.add_argument("--clean", action="store_true", help="run the selected face tests unplanted; all must pass")
args = ap.parse_args()

sys.path.insert(0, str((args.checkout / "sw/firmware/ctrl/test").resolve()))
import aecp_mutants as m  # noqa: E402
import aecp_face_mutants as face  # noqa: E402

rows = [m.defect(*row) for row in face.ROWS]
if args.only:
    rows = [d for d in rows if d.name == args.only]
if args.clean:
    # unplanted baseline: the same arm, same selection, no mutation; every selected test must pass
    import shutil
    src = args.output / "work/ctrl"
    shutil.copytree(m.CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copytree(m.CTRL.parent / "ctrl_nvm", src.parent / "ctrl_nvm", dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("test", "__pycache__", "*.pyc"))
    tree = m.Tree(src, args.output / "work/build", args.output / "work/reuse", m.fw_gtest.Build(jobs=args.jobs),
                  m.STACK.resolve())
    selected = ":".join(sorted({t for d in rows for t, _ in d.checks}))
    result = m.aecp_arms.core_arm(tree, m.ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", args.interfaces, "app", selected)
    (args.output / f"clean-if{args.interfaces}.log").write_text(result.log)
    print(f"clean arm rc={result.rc} selected={selected}", flush=True)
    sys.exit(result.rc)
if args.old_needle_control:
    leak = [d for d in rows if d.name == "face-software-gptp-keeps-datapath-capable"][0]
    rows = [m.Defect("control-old-needle-" + leak.name, leak.path, leak.old, leak.new,
                     ((leak.checks[0][0], "AS_CAPABLE is the software gPTP owner's"),))]

# controls() checks the WHOLE table owns every TEST; run it on the full table first, then narrow.
m.controls()
m.controls = lambda: None
m.DEFECTS = tuple(rows)
print(f"tsn-c-stack at {m.stack_pin(m.STACK.resolve())}", flush=True)
escaped = m.campaign(args.output, jobs=args.jobs, stack=m.STACK.resolve())
print("ESCAPES" if escaped else "ALL CAUGHT", flush=True)
sys.exit(int(escaped))
