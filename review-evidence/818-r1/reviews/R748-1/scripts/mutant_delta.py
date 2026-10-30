#!/usr/bin/env python3
"""List the mutants added or rewritten between two copies of pp_resource_gate_mutants.py (by name and edit)."""
import importlib.util, json, sys
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod); return mod
def table(mod):
    out = {}
    for group in ("POPULATION_MUTANTS", "MUTANTS", "SET_MUTANTS", "RANK_MUTANTS", "PLACEMENT_MUTANTS"):
        for name, change in getattr(mod, group, {}).items():
            out[name] = (group, change)
    return out
old, new = table(load(sys.argv[1], "old")), table(load(sys.argv[2], "new"))
added = [n for n in new if n not in old]
rewritten = [n for n in new if n in old and new[n][1] != old[n][1]]
removed = [n for n in old if n not in new]
print(json.dumps({"added": added, "rewritten": rewritten, "removed": removed,
                  "counts": {"old": len(old), "new": len(new), "added": len(added), "rewritten": len(rewritten)}}, indent=1))
