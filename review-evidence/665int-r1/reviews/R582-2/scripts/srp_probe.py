#!/usr/bin/env python3
"""Reviewer probe: plant one defect in a scratch copy of the SRP adapter and run
the whole Srp suite at two interfaces; report which tests fail.
Usage: srp_probe.py <checkout> <scratch-root>. Reads the checkout only."""
import shutil, sys
from pathlib import Path

repo, root = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest")]
from ctrl_build import CTRL, Tree  # noqa: E402
import fw_gtest  # noqa: E402
from srp_arms import arm_srp  # noqa: E402

OWED = ("                i->stop_owed[s] = false;\n                i->active[s] = false;\n"
        "                ++m->stops;\n                publish_licence(i);\n")
PROBES = [
    ("control-unmodified", None, None),
    ("owed-stop-licence-publish-skipped", OWED, OWED.replace("                publish_licence(i);\n", "")),
    ("owed-stop-licence-publish-after-report", OWED + "                m->config.licence(m->config.ctx,n,s,false);\n",
     OWED.replace("                publish_licence(i);\n", "")
     + "                m->config.licence(m->config.ctx,n,s,false);\n                publish_licence(i);\n"),
]
build = fw_gtest.Build(jobs=4)
for name, old, new in PROBES:
    work = root / name
    shutil.rmtree(work, ignore_errors=True)
    src = work / "ctrl"
    shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    target = src / "srp/srp_mbx.c"
    text = target.read_text()
    if old is not None:
        assert text.count(old) == 1, (name, text.count(old))
        target.write_text(text.replace(old, new))
    out = arm_srp(Tree(src, work / "build", work / "reuse", build), repo / "third_party/lwSRP", 2,
                  debug=False, test=("srp_mbx.cpp", "Srp.*"))
    (root / f"{name}.log").write_text(out.log)
    fails = sorted({l.split(":")[0] for l in out.log.splitlines() if l.strip().startswith("[FAIL] ")})
    print(f"{name}: rc={out.rc} failing={fails if fails else 'none'}", flush=True)
