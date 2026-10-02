#!/usr/bin/env python3
"""For each driver, derive every per-unit log path the full campaign writes and report collisions."""
import collections
import importlib.util
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])


def load(rel: str):
    spec = importlib.util.spec_from_file_location(rel.replace("/", "_")[:-3], ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def report(driver: str, names: list[str]) -> None:
    dup = {n: c for n, c in collections.Counter(names).items() if c > 1}
    print(f"{driver}: {len(names)} log paths, collisions={dup}")


m = load("tb/acmp_talker/retry_mutants.py")
report("retry", ["baseline.txt"] + [f"{n}.txt" for n in m.MUTATIONS] + ["restored.txt"])
m = load("tb/adp_engine/mutants.py")
report("adp", [f"control-{s}-{t}.log" for s, t in sorted({(x[2], x[3]) for x in m.MUTANTS})]
       + [f"{x[0]}.log" for x in m.MUTANTS])
m = load("tb/maap/mutants.py")
report("maap", [f"control-{s}-{t}.log" for s, t in sorted({(x[1], x[2]) for x in m.MUTANTS})]
       + [f"{x[0]}-{x[1]}.log" for x in m.MUTANTS])
m = load("tb/pp_top/aecp_dispatch_mutants.py")
report("dispatch", [f"control-{t}.log" for t in sorted({x[2] for x in m.MUTANTS})]
       + [f"{x[0]}.log" for x in m.MUTANTS])
m = load("tb/pp_top/aecp_mutants.py")
report("aecp", [f"control-{s}-{t}.log" for s, t in sorted({(x[2], x[3]) for x in m.MUTANTS})]
       + [f"{x[0]}.log" for x in m.MUTANTS])
m = load("tb/pp_top/gsi_mutants.py")
names = ["golden"] + [v[0] for v in m.mutations()] + ["restored"]
report("gsi", [f"{n}-build.log" for n in names] + [f"{n}-run.log" for n in names])
m = load("tb/srp_admission/mutants.py")
report("srp_admission", [f"{lab}-{n}.log" for lab in ["control"] + [x[0] for x in m.MUTANTS]
                         for n, _, _ in m.SUITES])
m = load("tb/srp_top/mutants.py")
report("srp_top (written by the consumer, in order)",
       [f"control-{s}-{g}.log" for s, g in sorted({(x[1], x[2]) for x in m.MUTANTS})]
       + [f"{x[0]}.log" for x in m.MUTANTS])
