#!/usr/bin/env python3
"""Probe (R506-1): the planted defects at base and at head, by name and by seam
(file, old text, new text), for both campaigns. A base defect missing at head,
by name or with a different plant, is printed.
Usage: mutant_sets.py <repo> <base> <head> [work dir]"""
import importlib.util, subprocess, sys, tempfile, types
from pathlib import Path
repo, base, head = sys.argv[1:4]
def load(rev, rel, extra_mods):
    tmp = Path(tempfile.mkdtemp(dir=sys.argv[4] if len(sys.argv) > 4 else None))
    subprocess.run(f"git -C {repo} archive {rev} sw scripts configs | tar -x -C {tmp}", shell=True, check=True)
    d = tmp / Path(rel).parent
    sys.path[:0] = [str(d), str(tmp / "sw/firmware/gtest"), str(tmp / "scripts")]
    for m in list(sys.modules):
        if m in extra_mods:
            del sys.modules[m]
    spec = importlib.util.spec_from_file_location(Path(rel).stem, tmp / rel)
    mod = importlib.util.module_from_spec(spec); sys.modules[spec.name] = mod; spec.loader.exec_module(mod)
    del sys.path[:3]
    return mod
def plants(mod):
    out = {}
    for m in mod.MUTANTS:
        seams = getattr(m, "seams", None)
        if seams is None:
            seams = ((m.path, m.old, m.new),) if hasattr(m, "path") else ((getattr(m, "file", "?"), m.old, m.new),)
        out[m.name] = tuple(seams)
    return out
for rel, mods in (("sw/firmware/ctrl/test/ctrl_mutants.py", {"ctrl_mutants", "ctrl_build", "ctrl_arms", "fw_gtest"}),
                  ("sw/firmware/ctrl_nvm/test/nvm_mutants.py", {"nvm_mutants", "nvm_bench", "fw_gtest", "nvm_checks", "nvm_checks_write"})):
    b, h = plants(load(base, rel, mods)), plants(load(head, rel, mods))
    gone = [n for n in b if n not in h]
    changed = [n for n in b if n in h and b[n] != h[n]]
    print(f"{rel}: base {len(b)}, head {len(h)}, added {len(set(h) - set(b))}, missing at head {len(gone)}, plant changed {len(changed)}")
    for n in gone: print(f"   MISSING {n}")
    for n in changed: print(f"   CHANGED {n}:\n      base {b[n]}\n      head {h[n]}")
