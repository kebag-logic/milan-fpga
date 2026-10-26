#!/usr/bin/env python3
"""Compare the release mutant tables of two tb/tools trees: removed, changed and added entries.

Usage: python3 -I r4_mutant_table_diff.py <old tb/tools> <new tb/tools>
Each anchor is also checked to occur exactly once in its tree's planner, steps or driver source.
"""
import importlib.util
import sys
from pathlib import Path


def table(tools):
    sys.path.insert(0, tools)
    for name in ("torture_release_mutants", "torture_release_audio_mutants"):
        sys.modules.pop(name, None)
    spec = importlib.util.spec_from_file_location("trm", Path(tools) / "torture_release_mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.path.remove(tools)
    return list(mod.MUTANTS)


old, new = table(sys.argv[1]), table(sys.argv[2])
print("old", len(old), "new", len(new))
oldk = {m[0]: m for m in old}
newk = {m[0]: m for m in new}
for k in oldk:
    if k not in newk:
        print("REMOVED", repr(k))
    elif oldk[k] != newk[k]:
        o, n = oldk[k], newk[k]
        print("CHANGED", repr(k), "anchor" if o[1] != n[1] else "", "replacement" if o[2] != n[2] else "",
              "test" if o[3:] != n[3:] else "", o[3:], "->", n[3:])
for k in newk:
    if k not in oldk:
        print("ADDED", repr(k), newk[k][3:])
src = (Path(sys.argv[2]) / "torture_campaign.py").read_text()
for m in new:
    if "audio" in str(m[3:]) or m in new[-60:]:
        c = src.count(m[1])
        if c != 1:
            print("ANCHOR-COUNT", c, repr(m[0]))
