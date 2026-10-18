"""Run a suite's own mutation arm main(), control included, over the
mutants named on the command line. Usage: run_by_names.py <suite> <name>..."""
import sys, importlib.util
from pathlib import Path
suite, names = Path(sys.argv[1]).resolve(), sys.argv[2:]
spec = importlib.util.spec_from_file_location("mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.MUTATIONS = [x for x in m.MUTATIONS if x[0] in names]
assert len(m.MUTATIONS) == len(names), [x[0] for x in m.MUTATIONS]
print(f"{len(m.MUTATIONS)} named mutants: " + "; ".join(x[0] for x in m.MUTATIONS), flush=True)
sys.exit(m.main())
