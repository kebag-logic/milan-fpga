#!/usr/bin/env python3
"""Run ONE of crflic_mutants.MUTATIONS + TSPEC_MUTATIONS (0-based index)
through the campaign's own run_mutant(), in its own temporary work directory.
usage: <repo> <index> [work-dir]"""
import sys, tempfile
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
idx = int(sys.argv[2])
sys.path.insert(0, str(repo / "tb/verilator/milan_dp"))
import crflic_mutants as cm  # noqa: E402
arms = cm.MUTATIONS + cm.TSPEC_MUTATIONS
mut = arms[idx]
print(f"arm {idx}: {mut[0]!r} must fail {mut[3]!r}", flush=True)
with tempfile.TemporaryDirectory(prefix=f"r831-crflic-dp{idx}-",
                                 dir=sys.argv[3] if len(sys.argv) > 3 else None) as td:
    caught = cm.run_mutant(cm.DP_RTL.read_text(), mut, Path(td))
print("RESULT:", "CAUGHT" if caught else "NOT CAUGHT", flush=True)
sys.exit(0 if caught else 1)
