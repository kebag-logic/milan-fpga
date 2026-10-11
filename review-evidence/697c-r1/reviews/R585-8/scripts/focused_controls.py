#!/usr/bin/env python3
"""Run the changed pin, census and README controls without launching builder banks."""
import argparse, os, sys
from pathlib import Path
p = argparse.ArgumentParser(); p.add_argument("checkout", type=Path); p.add_argument("work", type=Path)
a = p.parse_args(); root=a.checkout.resolve(); work=a.work.resolve(); work.mkdir(parents=True, exist_ok=True)
os.chdir(root); sys.dont_write_bytecode=True
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_pin, ctrl_boundary, ctrl_configs, ctrl_build
print("head", ctrl_build.git(root, "rev-parse", "HEAD").stdout.strip(), flush=True)
print("clean pin", ctrl_build.stack_pin(), flush=True)
found=ctrl_pin.proof_census(); print("proof census", found, flush=True); assert not found
bad, n = ctrl_pin.pin_controls(work, ctrl_configs.makefiles())
print("pin_controls", bad, n, flush=True); assert bad == 0
counts=ctrl_boundary.population(n); page=ctrl_boundary.README.read_text()
print("population", counts, flush=True)
found=ctrl_boundary.figures(page, counts); print("README findings", found, flush=True); assert not found
bad, n=ctrl_boundary.figure_controls(page, counts); assert bad == 0
print("figure_controls", bad, n, flush=True)
print("PASS", flush=True)
