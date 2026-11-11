"""List mutants whose old text is not exactly once in its file (stack files from third_party/tsn-c-stack)."""
import sys, importlib, pathlib
root = pathlib.Path(sys.argv[1]); import os; stack = pathlib.Path(os.environ.get("STACK", str(root / "third_party"))); sys.path.insert(0, str(root / "sw/firmware/ctrl/test")); sys.path.insert(0, str(root / "sw/firmware/gtest"))
import ctrl_mutants
tables = {}
for modname in sys.argv[2:]:
    m = importlib.import_module(modname)
    tables[modname] = getattr(m, "MUTANTS", ())
bad = 0
for t, muts in tables.items():
    for mu in muts:
        p = mu.path
        f = stack / p if p.startswith("tsn-c-stack/") else root / "sw/firmware/ctrl" / p
        try:
            n = f.read_text().count(mu.old)
        except FileNotFoundError:
            n = -1
        if n != 1:
            bad += 1
            print(f"{t}: {mu.name}: {p}: count={n}")
print("bad", bad)
