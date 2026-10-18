"""Run a suite's own mutation arm, control included, over the named
MUTATIONS only. Usage: pick_mutants.py <suite_dir> <name> [<name> ...]"""
import sys, importlib.util
from pathlib import Path
suite = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
want = sys.argv[2:]
full = list(m.MUTATIONS)
m.MUTATIONS = [x for x in full if x[0] in want]
assert len(m.MUTATIONS) == len(want), [w for w in want if w not in [x[0] for x in full]]
print(f"picked {len(m.MUTATIONS)} of {len(full)} mutants: "
      + "; ".join(x[0] for x in m.MUTATIONS), flush=True)
sys.exit(m.main())
