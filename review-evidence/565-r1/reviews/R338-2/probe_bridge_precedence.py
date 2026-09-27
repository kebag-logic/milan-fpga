#!/usr/bin/env python3
"""Run the unmodified precedence test with the tracked AX clock pair appended.

Probe only: the test module's SHAPES list is extended in memory with the
(sys 100 MHz, milan 50 MHz) pair that both AX7101 configurations declare at
the reviewed head; no file is modified. Usage: probe_bridge_precedence.py <repo>
"""
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "sw/litex"))
import test_pp_mem_bridge as t  # noqa: E402

t.SHAPES.append(("ax7101 declared sys 100 / milan 50 (probe)", 100e6, 50e6))
import milan_soc  # noqa: E402
print("derived watchdog at 100/50:", milan_soc.pp_mem_timeout_cycles(100e6, 50e6), "sys cycles")
print("derived watchdog at 100/100:", milan_soc.pp_mem_timeout_cycles(100e6, 100e6), "sys cycles")
t.test_precedence()
checks, fails = t.TALLY["checks"], t.TALLY["fails"]
print(f"probe precedence: {checks} checks, {fails} FAIL")
sys.exit(1 if fails else 0)
