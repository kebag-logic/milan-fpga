#!/usr/bin/env python3
"""Run only srp_arms.own_leaveall_arms of a parent tree against a given lwSRP checkout.

Usage: run_own_la.py <parent-root> <lwsrp-checkout> <out-dir>
Prints each arm's rc and log, then a summary of the OWN-LA lines per arm:
withdrawals, never sent, worst Lv delay, any over 240 ms, and the no-withdrawal line.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
lwsrp = Path(sys.argv[2]).resolve()
out = Path(sys.argv[3]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_build  # noqa: E402,F401
import fw_gtest  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402

out.mkdir(parents=True, exist_ok=True)
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
rc = 0
line = re.compile(r"OWN-LA input=(\d+) offset_ms=(\d+) leaveall_ms=(\d+) withdrawn_ms=(\d+) lv_ms=(none>)?(\d+)")
for o in srp_arms.own_leaveall_arms(tree, lwsrp):
    print(f"=== ARM {o.arm} rc={o.rc}")
    print(o.log)
    n = unsent = worst = over = 0
    for m in line.finditer(o.log):
        n += 1
        if m.group(5):
            unsent += 1
            continue
        d = int(m.group(6)) - int(m.group(4))
        worst = max(worst, d)
        over += d > 240
    held = re.search(r"OWN-LA held .*", o.log)
    summary = (f"SUMMARY {o.arm} rc={o.rc} withdrawals={n} never_sent={unsent} worst_ms={worst} over_240={over} | "
               f"{held.group(0) if held else 'no held line'}")
    print(summary)
    rc |= 1 if o.rc else 0
print(f"run_own_la: rc={rc}")
sys.exit(rc)
