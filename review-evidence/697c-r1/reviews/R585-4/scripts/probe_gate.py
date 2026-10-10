#!/usr/bin/env python3
"""Judge one tree's checkout with its own boundary gate (derive + judge; no self-test, no stack gate, no
Makefile pin check): print every finding, or the refusal. Usage: python3 -I probe_gate.py <tree> [jobs]
Exit 0 = no finding, 1 = findings, 2 = refused."""
import sys, tempfile
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
import ctrl_boundary as cb  # noqa: E402
cb.JOBS = int(sys.argv[2]) if len(sys.argv) > 2 else 8
try:
    universe, computed = cb.derive()
    print("modes:", " ".join(universe))
    print("values:", " ".join(computed))
    findings = cb.judge(cb.Trees(cb.CTRL, cb.STACK), cb.fw_rv32.compiler(), Path(tempfile.mkdtemp(prefix="probe-")))
except cb.Refusal as exc:
    print(f"REFUSED: {exc}")
    sys.exit(2)
for f in findings:
    print("  [FAIL]", f)
print(f"findings: {len(findings)}")
sys.exit(1 if findings else 0)
