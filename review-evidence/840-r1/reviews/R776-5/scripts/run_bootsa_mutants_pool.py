#!/usr/bin/env python3
"""Run bootsa_mutants.py's own MUTATIONS, positive control and verdict logic in
a bounded pool. Usage: run_bootsa_mutants_pool.py <milan_dp dir> <work dir> <workers>
Nothing is reimplemented: run_mutant(), run_leg() and verdict() are the suite's."""
import importlib.util, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

here, work, workers = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
spec = importlib.util.spec_from_file_location("bootsa_mutants", here / "bootsa_mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
exe = here / "obj_bootsa" / m.EXE
clean = m.verdict(*m.run_leg(exe), [])
print(f"positive control: {clean}", flush=True)
def one(mut):
    d = work / str(m.MUTATIONS.index(mut))
    d.mkdir(parents=True, exist_ok=True)
    return mut[0], m.run_mutant(mut, d)
with ThreadPoolExecutor(workers) as pool:
    res = list(pool.map(one, m.MUTATIONS))
caught = sum(ok for _, ok in res)
print(f"mutants: {len(res)}, caught {caught}, survived or invalid {len(res) - caught}", flush=True)
for name, ok in res:
    print(("CAUGHT   " if ok else "NOT CAUGHT ") + name)
sys.exit(0 if clean == "pass" and caught == len(res) else 1)
