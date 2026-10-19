"""Run shard k of n of an engine mutation arm through its own main().

usage: python3 -I shard.py <engine_dir> <k> <n>
The control and the per-mutant code are the suite's own; only MUTATIONS is
narrowed to MUTATIONS[k::n], matching the published 18-way shard layout.
"""
import importlib.util, sys
from pathlib import Path
suite, k, n = Path(sys.argv[1]).resolve(), int(sys.argv[2]), int(sys.argv[3])
sys.path.insert(0, str(suite))
spec = importlib.util.spec_from_file_location("mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
full = list(m.MUTATIONS)
m.MUTATIONS = full[k::n]
print(f"shard {k}/{n}: {len(m.MUTATIONS)} of {len(full)} mutants: "
      + "; ".join(x[0] for x in m.MUTATIONS), flush=True)
sys.exit(m.main())
