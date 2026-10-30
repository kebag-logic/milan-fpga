"""(#818 round 2) mutant_delta.py <old mutants.py> <new mutants.py>: the mutants added, edited and removed, by name."""
import importlib.util
import json
import sys


def table(path: str, name: str) -> dict:
    """Every mutant of one copy of the campaign, by name: its group and its edit."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {mutant: (group, change) for group in ("POPULATION_MUTANTS", "MUTANTS", "SET_MUTANTS", "RANK_MUTANTS",
                                                  "PLACEMENT_MUTANTS")
            for mutant, change in getattr(module, group, {}).items()}


old, new = table(sys.argv[1], "old"), table(sys.argv[2], "new")
print(json.dumps({"added": [n for n in new if n not in old],
                  "edited": [n for n in new if n in old and new[n][1] != old[n][1]],
                  "removed": [n for n in old if n not in new],
                  "counts": {"old": len(old), "new": len(new)}}, indent=1))
