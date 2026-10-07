#!/usr/bin/env python3
"""Re-run one lane SRP defect exactly as srp_mutants.campaign grades it.

Usage: lane_campaign.py REPO LWSRP OUT NAME   (prints one verdict line)
The plant goes into a disposable copy under OUT; the checkout is not written.
"""
import shutil
import sys
from pathlib import Path

REPO, LWSRP, OUT = (Path(a).resolve() for a in sys.argv[1:4])
sys.path[:0] = [str(REPO / "sw/firmware/ctrl/test"), str(REPO / "sw/firmware/gtest")]
from ctrl_build import CTRL, Tree, Refusal  # noqa: E402
import fw_gtest  # noqa: E402
from srp_arms import arm_srp  # noqa: E402
from srp_mutants import DEFECTS, caught  # noqa: E402

d = {x.name: x for x in DEFECTS}[sys.argv[4]]
out = OUT / f"lane-{d.name}"
shutil.rmtree(out, ignore_errors=True)
src = out / "ctrl"
shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
text = (src / d.path).read_text()
if text.count(d.old) != 1:
    print(f"[ESCAPED] {d.name}: {text.count(d.old)} planting sites")
    sys.exit(1)
(src / d.path).write_text(text.replace(d.old, d.new))
selected = d.test if "." in d.test else "Srp." + d.test
try:
    r = arm_srp(Tree(src, out / "build", out / "reuse", fw_gtest.Build(jobs=1)), LWSRP, 2,
                debug=d.debug, test=(d.suite, selected))
except Refusal as e:
    print(f"[ESCAPED] {d.name}: refused {e}")
    sys.exit(1)
ok = caught(selected, d.needle, r)
(OUT / f"{d.name}.log").write_text(r.log)
print(f"[{'ok' if ok else 'ESCAPED'}] {d.name}: {d.test} / {d.needle} ({d.suite}{' debug' if d.debug else ''})")
sys.exit(0 if ok else 1)
