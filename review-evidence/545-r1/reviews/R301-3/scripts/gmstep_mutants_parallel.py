#!/usr/bin/env python3
"""Parallel driver for tb/verilator/milan_dp/gmstep_mutants.py --all (or --slew).

Imports the campaign's own CONTROLS, LEGS, is_fresh, build, run_leg, verdict
and run_control unchanged. Positive controls run first, serially, exactly as
main() does; the selected controls then run concurrently (at most 8 jobs),
each in its own tag-numbered build directory. Usage: <repo-root> [--slew]
"""
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root = Path(sys.argv[1]).resolve()
slew = "--slew" in sys.argv[2:]
sys.path.insert(0, str(root / "tb/verilator/milan_dp"))
import gmstep_mutants as gm  # noqa: E402

selected = [c for c in gm.CONTROLS if (c.name.startswith("the policy level") if slew else True)]
passes = fails = 0
with tempfile.TemporaryDirectory(prefix="gmstep-mutants-par-") as td:
    work = Path(td)
    for key in dict.fromkeys(c.leg for c in selected):
        leg = gm.LEGS[key]
        exe = leg.clean_mdir / leg.exe_name
        if not gm.is_fresh(leg, exe):
            print(f"[INFO] {exe} is missing or stale: the positive control is rebuilt", flush=True)
            exe = gm.build(leg, {}, work / f"obj_clean_{leg.target}")
        answer = gm.verdict(*gm.run_leg(leg, exe), None) if exe else "did not compile"
        if answer == "pass":
            passes += 1
            print(f"[PASS] the unmutated gateware still passes the {key} leg", flush=True)
        else:
            fails += 1
            print(f"[FAIL] the unmutated gateware does NOT pass the {key} leg ({answer})", flush=True)
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(lambda tc: gm.run_control(tc[1], work, tc[0]), enumerate(selected)))
    passes += sum(results)
    fails += sum(not r for r in results)
print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL (parallel driver, {len(selected)} controls)")
sys.exit(1 if fails else 0)
