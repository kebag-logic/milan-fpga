#!/usr/bin/env python3
"""Compare the planted-defect catalog (name, path, old, new, kills) of two extracted trees.
Usage: catalog_compare.py OLD_ROOT NEW_ROOT"""
import importlib, sys
def load(root):
    for k in [m for m in sys.modules if m.startswith(("ctrl_", "maap_", "fw_", "suite_", "mbx", "gen_mailbox", "mailbox"))]:
        del sys.modules[k]
    sys.path[:0] = [f"{root}/sw/firmware/ctrl/test", f"{root}/sw/firmware/gtest"]
    mod = importlib.import_module("ctrl_mutants")
    cat = {m.name: (m.path, m.old, m.new, m.kills()) for m in mod.MUTANTS}
    del sys.path[:2]
    return cat, len(mod.MUTANTS)
old, nold = load(sys.argv[1]); new, nnew = load(sys.argv[2])
print(f"old controls: {nold} (distinct {len(old)}), new controls: {nnew} (distinct {len(new)})")
print(f"obligations old {sum(len(v[3]) for v in old.values())}, new {sum(len(v[3]) for v in new.values())}")
print("removed:", sorted(set(old) - set(new)))
print("added:", sorted(set(new) - set(old)))
print("changed:", sorted(n for n in set(old) & set(new) if old[n] != new[n]))
