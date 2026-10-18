"""Run a suite's own mutation arm main() over the mutants whose property
starts with a prefix. Usage: run_named_mutants.py <suite_dir> <prefix>"""
import sys, importlib.util
from pathlib import Path
suite, prefix = Path(sys.argv[1]).resolve(), sys.argv[2]
spec = importlib.util.spec_from_file_location("mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.MUTATIONS = [x for x in m.MUTATIONS if x[4].startswith(prefix)]
print(f"{len(m.MUTATIONS)} mutants: " + "; ".join(x[0] for x in m.MUTATIONS), flush=True)
sys.exit(m.main())
