#!/usr/bin/env python3
"""For each #193 arm of the srp_top campaign, the first failing line naming its check.

usage: fail_words.py <campaign output dir> <processor tree>
"""
import ast, re, sys
from pathlib import Path

out, tree = Path(sys.argv[1]), Path(sys.argv[2])
src = (tree / "tb/srp_top/mutants.py").read_text()
body = src[src.index("MUTANTS = ["):]
arms = ast.literal_eval(body[body.index("["):body.index("\n]\n") + 2])
start = [i for i, a in enumerate(arms) if a[0] == "listener-settle-compare-dropped"][0]
for label, suite, group, want in arms[start:]:
    log = out / f"{label}.log"
    lines = [l for l in log.read_text(errors="replace").splitlines() if l.startswith("FAIL:")] if log.exists() else []
    hit = next((l for l in lines if want in l), None)
    print(f"{label} | {suite} {group} | {want} | {len(lines)} FAIL lines in its receipt")
    print(f"    {hit if hit else 'NO MATCH IN THE RECEIPT (the receipt is the last suite run of the label)'}")
