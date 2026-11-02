#!/usr/bin/env python3
"""Run probe_effect.py on the head and on three surviving reviewer mutants (as receipts/probe_effect.log).

usage: python3 -I run_effect.py <clone> <packet>
"""
import subprocess, sys
from pathlib import Path
clone, packet = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(clone / "scripts"))
import process_test_support as pts
src = (packet / "probe_mutants.py").read_text()
ns = {}
exec(src[src.index("OWN = {"):src.index("\npts.MUTANTS.update")], ns)
pts.MUTANTS.update(ns["OWN"])
for name in ("none", "rv-vanishing-waits-30s-more", "rv-parent-spared-past-kill-all", "rv-signal-by-number"):
    tree = pts.mutant_tree(packet / "scratch/trees", name)
    run = subprocess.run([sys.executable, "-B", str(packet / "probe_effect.py"), str(tree / "scripts")],
                         capture_output=True, text=True, timeout=120)
    print(f"== {name} rc {run.returncode}\n{run.stdout}{run.stderr[-600:]}", flush=True)
