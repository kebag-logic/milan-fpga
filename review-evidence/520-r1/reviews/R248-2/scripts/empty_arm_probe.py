#!/usr/bin/env python3
"""Run the shipping empty-image arm's run in a given checkout and report which
refusal text produced the match the arm asserts on.
usage (cwd = checkout root): empty_arm_probe.py <work-dir>"""
import sys
from pathlib import Path
sys.path.insert(0, "syn/yosys")
import rom_cache_selftest as r
work = Path(sys.argv[1])
p = r.Probe(work)
head = work / "head"
p.run("seed", ["--cache", str(head)])
for cached in (False, True):
    flags = ["--cache", str(head)] if cached else []
    res = p.run(f"empty-{cached}", flags, ("ltn_rom.hex", "empty"))
    lines = [l for l in res["output"].splitlines() if "empty" in l or "digest" in l]
    arm_passes = res["exit"] == 2 and "generated ROM is empty:" in res["output"]
    print(f"cached={cached} exit={res['exit']} arm_assertion_passes={arm_passes}")
    for l in lines: print("   ", l)
