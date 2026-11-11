#!/usr/bin/env python3
"""Run ONE of crflic_mutants.PP_MUTATIONS (0-based index) through the
campaign's own run_pp_mutant(), in its own temporary work directory, so the
processor-copy arms can run concurrently. usage: <repo> <index>"""
import sys, tempfile
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
idx = int(sys.argv[2])
sys.path.insert(0, str(repo / "tb/verilator/milan_dp"))
import crflic_mutants as cm  # noqa: E402
mut = cm.PP_MUTATIONS[idx]
print(f"arm {idx}: {mut[0]!r} must fail {mut[2]!r}", flush=True)
with tempfile.TemporaryDirectory(prefix=f"r831-crflic-pp{idx}-",
                                 dir=sys.argv[3] if len(sys.argv) > 3 else None) as td:
    caught = cm.run_pp_mutant(mut, Path(td))
print("RESULT:", "CAUGHT" if caught else "NOT CAUGHT", flush=True)
sys.exit(0 if caught else 1)
