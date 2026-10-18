"""Run one shard of a suite's own mutation arm: the same main(), control
included, over MUTATIONS[k::n]. Usage: shard_mutants.py <suite_dir> <k> <n>"""
import sys, importlib.util
from pathlib import Path
suite, k, n = Path(sys.argv[1]).resolve(), int(sys.argv[2]), int(sys.argv[3])
spec = importlib.util.spec_from_file_location("mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
full = list(m.MUTATIONS)
m.MUTATIONS = full[k::n]
print(f"shard {k}/{n}: {len(m.MUTATIONS)} of {len(full)} mutants: "
      + "; ".join(x[0] for x in m.MUTATIONS), flush=True)
sys.exit(m.main())
