#!/usr/bin/env python3
"""Run test_ctrl_memory.py's arms other than the SoC build, and the mutants those arms grade.

usage: ctrl_memory_arms.py <tree>

The SoC arm is left out because it elaborates the split CPU, which can write
a generated netlist into the interpreter's LiteX install. Everything else is
the test's own code, unmodified, driven in its own order.
"""
import sys
import tempfile
from functools import partial
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/litex"))
sys.argv = [str(tree / "sw/litex/test_ctrl_memory.py")]
import test_ctrl_memory as t  # noqa: E402

problems: list[str] = []
with tempfile.TemporaryDirectory(prefix="ctrl-memory-arms-") as name:
    tmp = Path(name)
    green, outcomes = set(), {}
    for key, label, arm in (("banks", "banks", t.bank_arms), ("checks", "rules", partial(t.check_arms, tmp=tmp)),
                            ("sim", "simulation", t.sim_arms), ("link", "link", partial(t.link_arms, tmp=tmp))):
        before = len(problems)
        outcomes[key] = t.run_arm(problems, label, arm)
        if len(problems) == before:
            green.add(key)
    t.run_arm(problems, "register", partial(t.registry_arms, tmp=tmp))
    keep = [m for m in t.MUTANTS if m.arm != "soc"]
    skipped = len(t.MUTANTS) - len(keep)
    t.MUTANTS = type(t.MUTANTS)(keep)
    t.run_arm(problems, "mutants (non-SoC)", partial(t.mutant_arms, tmp=tmp, green=green))
for problem in problems:
    print(f"FAIL: {problem}")
print(f"arms green: {sorted(green)}; link ran: {bool(outcomes.get('link'))}; "
      f"mutants graded: {len(keep)}; SoC-arm mutants not run: {skipped}")
print(f"RESULT: {'PASS' if not problems else 'FAIL'} ({len(problems)} failure(s))")
sys.exit(1 if problems else 0)
