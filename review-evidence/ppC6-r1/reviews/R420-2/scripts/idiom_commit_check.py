#!/usr/bin/env python3
"""R420-2: 88e0bf8 keeps every planted/replacement string and every check message. Usage: idiom_commit_check.py <clone> <workdir>"""
import importlib.util, re, subprocess, sys, pathlib
clone, work = sys.argv[1], pathlib.Path(sys.argv[2]); work.mkdir(parents=True, exist_ok=True)
def show(c, p):
    return subprocess.run(["git", "-C", clone, "show", f"{c}:{p}"], capture_output=True, text=True, check=True).stdout
def mutants(c):
    f = work / f"nm_{c}.py"; f.write_text(show(c, "tb/pp_top/notify_mutants.py"))
    s = importlib.util.spec_from_file_location(f.stem, f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    out = {}
    for n in dir(m):
        v = getattr(m, n)
        if isinstance(v, tuple):
            for x in v:
                if hasattr(x, "edits") and hasattr(x, "name"): out[x.name] = (x.edits, x.checks)
    return out
def lits(c):
    t = re.sub(r'"\s*\n\s*"', "", show(c, "tb/pp_top/notify_phases.hpp"))
    return sorted(re.findall(r'"((?:[^"\\]|\\.)*)"', t))
a, b = mutants("2e99ab0"), mutants("88e0bf8")
print(f"mutants {len(a)} -> {len(b)}; names, edits and named checks identical: {a == b}")
la, lb = lits("2e99ab0"), lits("88e0bf8")
print(f"notify_phases.hpp string literals {len(la)} -> {len(lb)}; identical multiset: {la == lb}")
