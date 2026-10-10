#!/usr/bin/env python3
"""Reviewer driver (R582-4): the round-4b/5 firmware tests and their plants, focused.

Runs, from the checkout's own harness and tables, only the tests and plants
this delta adds; each build goes under <scratch>/<mode>, never into the
checkout. Modes:
  baseline  the unplanted new tests: acmp and acmpif2 arms (B13), srp_mbx.cpp at
            one and two interfaces (both TALKER_DECL tests), F5's app arm with
            App.StartAndStopPublishTheStartedLevelBeforeTheirResponse at one and two
  ctrl      ctrl_mutants' pub-acmp-adapter-sid-valid-always (B13's plant)
  srp2      srp_pub_mutants.ROUND5 at two interfaces
  srp1      srp_pub_mutants.ROUND5 at one interface
  aecp      aecp_mutants' app-start-skips-publication and app-start-response-before-publication
Usage: python3 -I -B focused_plants.py <checkout> <scratch> <mode> [jobs]
"""
import sys
from pathlib import Path

tree_root, scratch, mode = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 4
sys.path.insert(0, str(tree_root / "sw/firmware/ctrl/test"))
import aecp_arms  # noqa: E402
import aecp_mutants  # noqa: E402
import ctrl_arms  # noqa: E402
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
import srp_arms  # noqa: E402
import srp_mutants  # noqa: E402
import srp_pub_mutants  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

LWSRP = tree_root / "third_party/lwSRP"
out = scratch / mode
out.mkdir(parents=True, exist_ok=True)
failed = False
if mode == "baseline":
    tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=jobs))
    cut_reuse(tree.reuse)
    cfg = tree_root / "configs/endstation_ax7101_1x1_tdm8.yaml"
    outs = [ctrl_arms.arm_acmp(tree), ctrl_arms.arm_acmpif2(tree)]
    outs += [srp_arms.arm_srp(tree, LWSRP, i) for i in (1, 2)]
    outs += [aecp_arms.core_arm(tree, cfg, i, "app", "App.StartAndStopPublishTheStartedLevelBeforeTheirResponse")
             for i in (1, 2)]
    for o in outs:
        (out / f"{o.arm}.log").write_text(o.log)
        names = [n for n in ("B13AMoveWithNoStream", "PubTalkerDeclHoldsAcrossADomainAdoption",
                             "PubTalkerDeclIsNotPublishedByACreationThatFails",
                             "StartAndStopPublishTheStartedLevelBeforeTheirResponse") if n in o.log]
        tail = [ln for ln in o.log.splitlines() if "PASSED" in ln or "FAILED" in ln or "tests" in ln.lower()][-2:]
        print(f"[{'ok' if o.rc == 0 else 'FAIL'}] {o.arm} rc {o.rc}; names seen {names}; {' | '.join(tail)}")
        failed |= o.rc != 0
elif mode == "ctrl":
    tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=jobs))
    cut_reuse(tree.reuse)
    ctrl_mutants.MUTANTS = tuple(m for m in ctrl_mutants.MUTANTS if m.name == "pub-acmp-adapter-sid-valid-always")
    ctrl_mutants.unnamed_tests = lambda: []
    assert len(ctrl_mutants.MUTANTS) == 1
    failed = ctrl_mutants.campaign(out / "mutants", tree.reuse, jobs)
elif mode in ("srp1", "srp2"):
    srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name in srp_pub_mutants.ROUND5)
    assert len(srp_mutants.DEFECTS) == 5, [d.name for d in srp_mutants.DEFECTS]
    failed = srp_mutants.campaign(out / "mutants", LWSRP, jobs, 1 if mode == "srp1" else 2)
elif mode == "aecp":
    aecp_mutants.DEFECTS = tuple(d for d in aecp_mutants.DEFECTS if d.name in ("app-start-skips-publication", "app-start-response-before-publication"))
    assert len(aecp_mutants.DEFECTS) == 2
    aecp_mutants.controls = lambda: None   # its table-drift control refuses any subset by design
    failed = aecp_mutants.campaign(out / "mutants", jobs)
else:
    sys.exit(f"unknown mode {mode}")
print(f"focused {mode}: {'FAIL' if failed else 'PASS'}")
sys.exit(1 if failed else 0)
