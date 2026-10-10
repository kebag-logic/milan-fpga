#!/usr/bin/env python3
"""fw_focus_probe.py - the round-5 firmware tests and their plants, through the gate's own arms.

Runs one part per invocation, so parts can run side by side:

  positive-acmp   ctrl_arms.arm_acmp and arm_acmpif2 on the unmodified tree
                  (B13 among the AcmpMailbox tests), rc 0 required
  positive-srp    srp_arms.arm_srp, Srp.PubTalkerDecl* at two and one interfaces
  plant-acmp      ctrl_mutants' campaign over pub-acmp-adapter-sid-valid-always alone
  plant-srp-if2   srp_mutants' campaign over the five round-5 defects at two interfaces
  plant-srp-if1   the same at one interface

Usage: fw_focus_probe.py <checkout> <lwsrp-at-pin> <scratch-dir> <part>
The checkout is read only: every planted copy and build is under scratch-dir.
"""
import sys
from pathlib import Path


def main() -> int:
    repo, lwsrp, scratch, part = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]), sys.argv[4]
    sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest")]
    import fw_gtest
    from ctrl_build import CTRL, Tree
    scratch = scratch.resolve() / part
    scratch.mkdir(parents=True, exist_ok=True)
    if part == "positive-acmp":
        import ctrl_arms
        rc = 0
        for arm in (ctrl_arms.arm_acmp, ctrl_arms.arm_acmpif2):
            out = arm(Tree(CTRL, scratch / "build", scratch / "reuse", fw_gtest.Build(jobs=4)))
            b13 = [ln for ln in out.log.splitlines() if "B13" in ln]
            print(f"[{'ok' if out.rc == 0 else 'FAIL'}] {out.arm}: rc {out.rc}; B13 lines: {b13[:3]}")
            print("\n".join(out.log.splitlines()[-4:]))
            rc |= out.rc
        return rc
    if part == "positive-srp":
        from srp_arms import arm_srp
        rc = 0
        for n in (2, 1):
            out = arm_srp(Tree(CTRL, scratch / f"build{n}", scratch / f"reuse{n}", fw_gtest.Build(jobs=4)), lwsrp, n,
                          test=("srp_mbx.cpp", "Srp.PubTalkerDecl*"))
            ran = [ln for ln in out.log.splitlines() if "PubTalkerDecl" in ln]
            print(f"[{'ok' if out.rc == 0 else 'FAIL'}] {out.arm}: rc {out.rc}")
            print("\n".join(ran[:12]))
            print("\n".join(out.log.splitlines()[-4:]))
            rc |= out.rc
        return rc
    if part == "plant-acmp":
        import ctrl_mutants
        ctrl_mutants.MUTANTS = tuple(m for m in ctrl_mutants.MUTANTS if m.name == "pub-acmp-adapter-sid-valid-always")
        assert len(ctrl_mutants.MUTANTS) == 1
        ctrl_mutants.unnamed_tests = lambda *a, **k: []      # a one-plant table names few tests by design
        escaped = ctrl_mutants.campaign(scratch, scratch / "reuse", 4)
        return int(escaped)
    if part.startswith("plant-srp-if"):
        import srp_mutants
        import srp_pub_mutants
        srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name in srp_pub_mutants.ROUND5)
        assert len(srp_mutants.DEFECTS) == 5, [d.name for d in srp_mutants.DEFECTS]
        failed = srp_mutants.campaign(scratch, lwsrp, 4, int(part[-1]))
        print(f"round-5 SRP plants at {part[-1]} interface(s): {'an escape' if failed else 'all 5 caught'}")
        return int(failed)
    raise SystemExit(f"unknown part {part}")


if __name__ == "__main__":
    sys.exit(main())
