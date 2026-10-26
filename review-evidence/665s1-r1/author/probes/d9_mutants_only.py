#!/usr/bin/env python3
"""Probe: run only the two D9 undefined-event mutants of sw/firmware/ctrl/test/ctrl_mutants.py
through its own campaign() (test_ctrl_firmware.py --self-test runs every defect).

Usage: python3 d9_mutants_only.py <repo> <output-dir>
"""
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(repo / "sw/firmware/gtest"))
import ctrl_mutants as m  # noqa: E402
from ctrl_build import stack_pin  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

out = Path(sys.argv[2]).resolve()
stack_pin()
cut_reuse(out / "reuse")
m.MUTANTS = tuple(x for x in m.MUTANTS if x.name.startswith("unknown-event-decoded"))
m.unnamed_tests = lambda: []
escaped = m.campaign(out / "mutants", out / "reuse", 4)
print(f"D9 undefined-event mutants: {len(m.MUTANTS)}, escaped: {escaped}")
sys.exit(int(escaped))
