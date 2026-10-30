#!/usr/bin/env python3
"""Compare the mutant tables of two syn/ooc trees: added names and names whose edit changed.
usage: mutant_delta.py <old syn/ooc> <new syn/ooc> <out.json>"""
import importlib.util, json, sys
from pathlib import Path
def table(d):
    spec = importlib.util.spec_from_file_location(f"m{abs(hash(d))}", Path(d) / "pp_resource_gate_mutants.py")
    m = importlib.util.module_from_spec(spec); sys.path.insert(0, d); spec.loader.exec_module(m); sys.path.pop(0)
    return {n: list(c) for g in ("POPULATION_MUTANTS", "MUTANTS", "SET_MUTANTS", "RANK_MUTANTS", "PLACEMENT_MUTANTS")
            for n, c in getattr(m, g, {}).items()}
old, new = table(sys.argv[1]), table(sys.argv[2])
out = {"old": len(old), "new": len(new), "added": sorted(set(new) - set(old)), "removed": sorted(set(old) - set(new)),
       "rewritten": sorted(n for n in set(new) & set(old) if new[n] != old[n])}
Path(sys.argv[3]).write_text(json.dumps(out, indent=1) + "\n")
print({k: (v if isinstance(v, int) else len(v)) for k, v in out.items()})
