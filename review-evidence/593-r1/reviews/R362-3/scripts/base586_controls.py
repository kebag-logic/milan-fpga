#!/usr/bin/env python3
"""Replay PR #586's release controls against a planner copy; report re-anchored ones.

usage: base586_controls.py <base_mutants.py> <head_mutants.py> <planner.py>
Each base control whose anchor is still unique is applied to a temporary planner copy
and must fail its named test. A control whose anchor moved is matched by name in the
head driver and reported with both anchors for manual equivalence review.
"""
import importlib.util, subprocess, sys, tempfile
from pathlib import Path

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

base = load(sys.argv[1], "base_m").MUTANTS
head = {m[0]: m for m in load(sys.argv[2], "head_m").MUTANTS}
text = Path(sys.argv[3]).read_text(encoding="utf-8")
bad = 0
with tempfile.TemporaryDirectory() as d:
    cand = Path(d) / "torture_campaign.py"
    for name, old, new, test in base:
        if text.count(old) != 1:
            h = head.get(name)
            same = h is not None and h[2] == new or (h is not None and h[3] == test)
            print(f"REANCHORED: {name}: base_test={test} head_entry={'present' if h else 'MISSING'}"
                  + (f" head_test={h[3]}\n  base_old={old!r}\n  head_old={h[1]!r}\n  base_new={new!r}\n  head_new={h[2]!r}" if h else ""))
            if h is None: bad += 1
            continue
        cand.write_text(text.replace(old, new), encoding="utf-8")
        r = subprocess.run([sys.executable, "-B", str(cand), "--self-test"], capture_output=True, text=True, timeout=600)
        ok = r.returncode == 1 and f"FAIL: {test} " in r.stderr
        print(f"{'KILLED' if ok else 'SURVIVED'}: {name}: {test}")
        bad += not ok
print(f"base controls: {len(base)}; problems: {bad}")
sys.exit(1 if bad else 0)
