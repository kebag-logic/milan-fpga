#!/usr/bin/env python3
"""Reviewer probe: is the admission swap's join-before-leave order observable on the wire?

usage: swap_order_probe.py --repo CLONE --root OUT --interfaces {1,2}
Runs AdmissionChangeSwapsTheTypeInPlace in scratch copies of sw/firmware/ctrl with one added assertion (no Leave of
the declared Talker Failed leaves while its swap's join is refused), twice: on the head's code (the control, which
must pass) and with the old type left before the new is joined (the mutant). Nothing is written to CLONE."""
import argparse, shutil, sys
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument("--repo", type=Path, required=True); ap.add_argument("--root", type=Path, required=True)
ap.add_argument("--interfaces", type=int, required=True); a = ap.parse_args()
sys.path.insert(0, str(a.repo / "sw/firmware/ctrl/test"))
from ctrl_build import CTRL, ROOT, Tree
from srp_arms import arm_srp
import fw_gtest
TEST_OLD = ('        EXPECT_EQ(pub_of(model,i).talker_decl,2u) << "a swap whose join is refused keeps the declared type";\n'
            '    }\n    advance(400);\n')
TEST_NEW = ('        EXPECT_EQ(pub_of(model,i).talker_decl,2u) << "a swap whose join is refused keeps the declared type";\n'
            '        EXPECT_EQ(leave(talker(i,1,first),2),nullptr) << "REVIEWER no Leave of the declared Failed while its swap join is refused";\n'
            '    }\n    advance(400);\n')
CODE_OLD = "        if (valid && !waits && (how != SRP_DECLARE_CHANGED || (i->talkers & bit) == 0u || admitted != was)) {\n"
CODE_NEW = ("        if ((i->talkers & bit) != 0u && valid && admitted != was) {\n"
            "            (void)mrp_mad_leave(i->msrp,0,was ? MSRP_ATTR_TYPE_TALKER_ADV : MSRP_ATTR_TYPE_TALKER_FAILED,&value);\n"
            "        }\n" + CODE_OLD)
build = fw_gtest.Build(jobs=2)
for name, code in (("control", False), ("mutant-leave-before-join", True)):
    out = a.root / name; src = out / "ctrl"
    shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    t = src / "test/srp_talker.cpp"; s = t.read_text(); assert s.count(TEST_OLD) == 1; t.write_text(s.replace(TEST_OLD, TEST_NEW))
    if code:
        c = src / "srp/srp_mbx.c"; s = c.read_text(); assert s.count(CODE_OLD) == 1; c.write_text(s.replace(CODE_OLD, CODE_NEW))
    cfg = {"config": ROOT / "configs/endstation_ax7101_8x8.yaml"} if a.interfaces == 2 else {}
    r = arm_srp(Tree(src, out / "build", out / "reuse", build), (a.repo / "third_party/lwSRP").resolve(), a.interfaces,
                test=("srp_talker.cpp", "Talker.AdmissionChangeSwapsTheTypeInPlace"), **cfg)
    (a.root / f"{name}.log").write_text(r.log)
    fails = sorted({ln.strip()[:200] for ln in r.log.splitlines() if ln.strip().startswith("[FAIL] ")})
    print(f"{name} if{a.interfaces}: rc {r.rc}; failing: {fails}", flush=True)
    shutil.rmtree(out)
