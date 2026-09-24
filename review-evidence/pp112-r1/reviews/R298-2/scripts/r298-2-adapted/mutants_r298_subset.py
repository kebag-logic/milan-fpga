#!/usr/bin/env python3
"""Run a named subset of the UNCHANGED round-1 mutants_r298.py (for parallel,
time-bounded execution). Usage: mutants_r298_subset.py <name> <head> <vl> <work> <out>"""
import sys
from pathlib import Path
script = Path(__file__).resolve().parent.parent / "r298-1" / "mutants_r298.py"
name = sys.argv[1]
sys.argv = [str(script)] + sys.argv[2:6]
ns = {"__name__": "r298_subset", "__file__": str(script)}
exec(compile(script.read_text(), str(script), "exec"), ns)
ns["MUTANTS"][:] = [m for m in ns["MUTANTS"] if m[0] == name]
assert len(ns["MUTANTS"]) == 1, name
ns["main"]()
