#!/usr/bin/env python3
"""Reviewer probe R546-1: does the new reset-before-D self-test arm
discriminate the original topology from the fixed one?

usage: r546_iob_arm_probe.py REPO
Runs the real sw/litex/iob_pack_check.tcl through the self-test's own stubs:
  A  the new arm as committed                      -> must hold
  B  the new arm's expectation over the FIXED shape -> must NOT hold
  C  the new arm's netlist under a PASS expectation -> must NOT hold
  D  each check mutant in the self-test, run against the new arm alone,
     reported (which mutants this arm kills on its own)
exit 0 when A holds and B, C do not.
"""
import dataclasses
import shutil
import sys
import tempfile
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "sw" / "litex"))
import iob_pack_selftest as t  # noqa: E402

tclsh = shutil.which("tclsh")
arm = next(a for a in t.ARMS if "reset remapped" in a.name)
fixed = dataclasses.replace(arm, name="fixed shape, refusal expected",
                            netlist=t.rx_dv())
as_pass = dataclasses.replace(
    arm, name="planted shape, pass expected", status=0, failed="",
    rows=("PASS  eth0_rx_dv:",))
ok = True
with tempfile.TemporaryDirectory() as tmp:
    work = Path(tmp)
    for case, want_hold in ((arm, True), (fixed, False), (as_pass, False)):
        problems = t.run_arm(tclsh, t.CHECK_TCL, case, work)
        held = not problems
        print(f"{'OK ' if held == want_hold else 'BAD'} {case.name}: "
              f"{'holds' if held else 'does not hold'}"
              + ("" if held else f" ({problems[0][:100]})"))
        ok &= held == want_hold
    source = t.CHECK_TCL.read_text(encoding="utf-8")
    kills = []
    for name, old, new in t.MUTANTS:
        mutant = work / "mutant.tcl"
        mutant.write_text(source.replace(old, new), encoding="utf-8")
        if t.run_arm(tclsh, mutant, arm, work):
            kills.append(name)
    print(f"new arm alone kills {len(kills)}/{len(t.MUTANTS)} check mutants: "
          + "; ".join(kills))
print("RESULT: PASS" if ok else "RESULT: FAIL")
sys.exit(0 if ok else 1)
