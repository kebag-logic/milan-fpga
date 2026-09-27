#!/usr/bin/env python3
"""Confirm every PR #586 mutant (base driver) survives at the head driver, verbatim or re-anchored.

Usage (from the review clone): check586_mutants.py <base-rev> <head-rev>
A re-anchored mutant keeps its name and named test, its head anchor is unique in the
head planner, and its edit (the differing opcodes between anchor and replacement) is
the same edit as the base mutant's.
"""
import difflib, subprocess, sys, types

def show(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout

def edit(old, new):
    ops = difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes()
    return [(tag, old[i1:i2], new[j1:j2]) for tag, i1, i2, j1, j2 in ops if tag != "equal"]

def load(rev):
    mod = types.ModuleType("m")
    exec(compile(show(rev, "tb/tools/torture_release_mutants.py"), rev, "exec"), mod.__dict__)
    return mod.MUTANTS

base, head = load(sys.argv[1]), load(sys.argv[2])
planner = show(sys.argv[2], "tb/tools/torture_campaign.py")
by_name = {m[0]: m for m in head}
bad = 0
for name, old, new, test in base:
    if (name, old, new, test) in head:
        print(f"VERBATIM {name}")
        continue
    h = by_name.get(name)
    ok = (h is not None and h[3] == test and planner.count(h[1]) == 1
          and edit(old, new) == edit(h[1], h[2]))
    print(f"{'REANCHORED' if ok else 'LOST'} {name} -> {h[3] if h else None}")
    bad += not ok
print(f"base={len(base)} head={len(head)} lost={bad}")
sys.exit(1 if bad else 0)
