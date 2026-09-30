#!/usr/bin/env python3
"""Reviewer driver: run chosen tb/pp_top/notify_mutants.py mutants (or goldens) through
the script's own judge(), in chunks that fit a foreground window.

Usage: mutants_chunk.py TREE OUTPUT VERILATOR JOBS [--goldens] NAME...
TREE is an exact-head extraction; the script's plant/copy/judge logic is used unchanged.
"""
import concurrent.futures, json, sys
from pathlib import Path
tree, out, verilator, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], int(sys.argv[4])
names = sys.argv[5:]
sys.path.insert(0, str(tree / "tb/pp_top"))
import notify_mutants as nm  # noqa: E402
out.mkdir(parents=True, exist_ok=True)
known = {m.name: m for m in nm.MUTANTS}
if names and names[0] == "--goldens":
    chosen = nm.goldens([known[n] for n in names[1:]] if names[1:] else list(nm.MUTANTS))
else:
    chosen = [known[n] for n in names]
work = (tree, out, verilator)
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    for rec in pool.map(lambda m: nm.judge(m, work), chosen):
        (out / f"{rec['mutant']}.json").write_text(json.dumps(rec, indent=1) + "\n")
        print(json.dumps({k: rec.get(k) for k in ("mutant", "verdict", "missing", "run_rc")}), flush=True)
