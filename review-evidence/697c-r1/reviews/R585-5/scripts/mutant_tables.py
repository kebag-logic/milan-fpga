"""Compare two trees' firmware mutation tables: every Mutant's name and its
expected verdicts (arm, test, words, and any extra expectations) must match;
the file and the anchor text may differ (the cores moved and their comments
were trimmed). Usage: python3 -I mutant_tables.py TREE_A TREE_B"""
import dataclasses
import importlib
import sys
from pathlib import Path


def table(tree: str) -> dict:
    test = Path(tree) / "sw/firmware/ctrl/test"
    sys.path[:0] = [str(test), str(Path(tree) / "sw/firmware/gtest")]
    for m in list(sys.modules):
        if m.endswith("_mutants") or m in ("ctrl_mutant", "ctrl_build"):
            del sys.modules[m]
    rows = {}
    for name in ("ctrl_mutants", "srp_mutants", "aecp_mutants", "maap_mutants"):
        try:
            mod = importlib.import_module(name)
        except Exception as exc:  # report, do not hide
            rows[f"IMPORT {name}"] = repr(exc)
            continue
        for attr in dir(mod):
            val = getattr(mod, attr)
            if attr.isupper() and isinstance(val, (tuple, list)):
                for m in val:
                    if dataclasses.is_dataclass(m):
                        d = dataclasses.asdict(m)
                        key = f"{name}.{attr}:{d.get('name')}"
                        rows[key] = {k: v for k, v in d.items() if k not in ("file", "old", "new", "path")}
                        rows[key]["_file"] = str(d.get("file", d.get("path", "")))
    sys.path[:2] = []
    return rows


a, b = table(sys.argv[1]), table(sys.argv[2])
print(f"rows: A {len(a)}  B {len(b)}")
only_a = sorted(set(a) - set(b))
only_b = sorted(set(b) - set(a))
print(f"only in A: {len(only_a)}", *only_a[:20], sep="\n  ")
print(f"only in B: {len(only_b)}", *only_b[:20], sep="\n  ")
diff = 0
moved = 0
for k in sorted(set(a) & set(b)):
    ea = {x: y for x, y in a[k].items() if x != "_file"} if isinstance(a[k], dict) else a[k]
    eb = {x: y for x, y in b[k].items() if x != "_file"} if isinstance(b[k], dict) else b[k]
    if ea != eb:
        diff += 1
        print("EXPECTATION DIFFERS", k, ea, eb, sep="\n  ")
    elif isinstance(a[k], dict) and a[k]["_file"] != b[k]["_file"]:
        moved += 1
print(f"common rows {len(set(a) & set(b))}, expectations differing {diff}, file moved {moved}")
sys.exit(1 if diff or only_a or only_b else 0)
