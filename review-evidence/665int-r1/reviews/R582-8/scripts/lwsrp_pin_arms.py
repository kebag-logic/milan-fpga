#!/usr/bin/env python3
"""Run ctrl_mutants.lwsrp_pin_arms (the lwSRP pin-refusal plants of test_ctrl_firmware.py
--self-test) alone against a candidate checkout. Exit 1 when any escapes.

Usage: python3 lwsrp_pin_arms.py <candidate checkout> <lwSRP checkout> <scratch out>
"""
import sys
from pathlib import Path

clone, lwsrp, out = (Path(a).resolve() for a in sys.argv[1:4])
sys.path[:0] = [str(clone / "sw/firmware/ctrl/test"), str(clone / "sw/firmware/gtest")]
import ctrl_mutants  # noqa: E402

escaped = ctrl_mutants.lwsrp_pin_arms(out, lwsrp)
print(f"lwsrp pin arms: {'FAIL' if escaped else 'PASS'} ({escaped} escaped)", flush=True)
sys.exit(1 if escaped else 0)
