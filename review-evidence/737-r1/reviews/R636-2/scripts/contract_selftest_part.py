#!/usr/bin/env python3
"""Run one disjoint part of `ci_events.py --selftest` at a checkout and time it.

Usage: contract_selftest_part.py <checkout> rest|gen:<workflow,...>
  rest            the complete selftest with the generated-graph stage stubbed out
  gen:a,b         only the generated-graph stage, restricted to templates a,b
Running `rest` plus gen over all four templates covers every arm exactly once.
The checkout's own code is used unchanged; only the stage selection differs.
"""
import sys, time, pathlib
root = pathlib.Path(sys.argv[1]); part = sys.argv[2]
sys.path.insert(0, str(root / "scripts"))
import ci_events
start = time.perf_counter()
if part == "rest":
    ci_events._selftest_generated_gates = lambda pristine: ([], 0)
    rc = ci_events.selftest(root)
    print(f"PART rest rc={rc} seconds={time.perf_counter() - start:.1f}")
else:
    names = part.split(":", 1)[1].split(",")
    full = dict(ci_events.TEMPLATES)
    ci_events.TEMPLATES = {n: full[n] for n in names}
    # selftest() passes this stage the unprojected pristine world.
    world = ci_events.parse_world(ci_events.read_tree(root))
    found, arms = ci_events._selftest_generated_gates(world)
    rc = 1 if found else 0
    for p in found:
        print("FAIL", p)
    print(f"PART {part} arms={arms} problems={len(found)} rc={rc} seconds={time.perf_counter() - start:.1f}")
sys.exit(rc)
