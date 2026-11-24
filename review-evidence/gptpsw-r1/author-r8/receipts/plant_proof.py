#!/usr/bin/env python3
"""plant_proof.py <checkout> <work> <old|new>: the AS_CAPABLE leak (aecp_face.c's mask dropped) planted in a copy.
old: the checkout's own tests (the parent) with any named failure counting as caught; the leak must escape (exit 0).
new: the face table's three software-gPTP rows on their declared words, plus the unplanted AVB test at one and two
interfaces; every plant caught and the baseline green (exit 0). The checkout is copied, never written."""
import shutil
import sys
from pathlib import Path

repo, work, mode = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest")]
import aecp_arms, aecp_mutants, aecp_face_mutants, fw_gtest  # noqa: E401,E402
from ctrl_build import CTRL, ROOT, STACK, Tree, stack_pin  # noqa: E402

AVB = "Face.SoftwareGptpAvbKeepsTheDatapathsLinkAndClass"
OLD = "out->flags = (uint8_t)((out->flags & ~1u) | (as_capable ? 1u : 0u));"
LEAK = "out->flags = (uint8_t)(out->flags | (as_capable ? 1u : 0u));"
print(f"checkout {repo} mode {mode}; tsn-c-stack at {stack_pin(STACK.resolve())}", flush=True)
aecp_mutants.controls = lambda: None   # the full-table drift control belongs to the full campaign, not a sub-table
if mode == "old":
    aecp_mutants.DEFECTS = (aecp_mutants.defect("leak-against-old-tests", "aecp_face.c", OLD, LEAK, (AVB, "")),)
    escaped = aecp_mutants.campaign(work / "campaign", stack=STACK.resolve())
    print(f"old tests: leak {'ESCAPED (as F1 reports)' if escaped else 'caught (unexpected)'}", flush=True)
    raise SystemExit(0 if escaped else 1)
rows = [r for r in aecp_face_mutants.ROWS if r[0].startswith("face-software-gptp-")]
print("rows:", [r[0] for r in rows], flush=True)
assert any(r[3] == LEAK for r in rows), "the leak row is in the table"
aecp_mutants.DEFECTS = tuple(aecp_mutants.defect(*r) for r in rows)
escaped = aecp_mutants.campaign(work / "campaign", stack=STACK.resolve())
src = work / "base/ctrl"
shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__"))
shutil.copytree(CTRL.parent / "ctrl_nvm", work / "base/ctrl_nvm", ignore=shutil.ignore_patterns("test", "__pycache__"))
tree = Tree(src, work / "base/build", work / "base/reuse", fw_gtest.Build(jobs=4), STACK.resolve())
bad = 0
for n in (1, 2):
    out = aecp_arms.core_arm(tree, ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", n, "app", "Face.SoftwareGptp*")
    (work / f"baseline-if{n}.log").write_text(out.log)
    ran = f"[ RUN      ] {AVB}" in out.log
    ok = f"[       OK ] {AVB}" in out.log
    print(f"baseline if{n}: rc={out.rc} {AVB} ran={ran} ok={ok}", flush=True)
    bad += int(out.rc != 0 or not ran or not ok)
raise SystemExit(int(bool(escaped) or bad))
