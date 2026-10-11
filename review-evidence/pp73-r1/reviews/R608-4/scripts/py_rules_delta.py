# R608-4: the parent's own per-file Python scan (check_py_idiom.scan, fetched
# from the public parent at ac2c5e77) over the changed processor Python files,
# at the previous head and at this head. Not the parent bank or its budget.
# Usage: python3 -I py_rules_delta.py CHECKER PREV_TREE HEAD_TREE FILE...
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve().parent))
spec = importlib.util.spec_from_file_location("idiom", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
prev, head = Path(sys.argv[2]), Path(sys.argv[3])
tot = {"prev": {}, "head": {}}
for rel in sys.argv[4:]:
    for tag, root in (("prev", prev), ("head", head)):
        p = root / rel
        if not p.is_file():
            continue
        counts, sites = mod.scan(p.read_text(encoding="utf-8"), rel)
        for k, v in counts.items():
            tot[tag][k] = tot[tag].get(k, 0) + v
        if tag == "head" and any(counts.values()):
            print(f"{rel}: {dict((k, v) for k, v in counts.items() if v)}")
keys = sorted(set(tot["prev"]) | set(tot["head"]))
for k in keys:
    a, b = tot["prev"].get(k, 0), tot["head"].get(k, 0)
    if a or b:
        print(f"{k}: prev {a} head {b}{'  ROSE' if b > a else ''}")
print("files", len(sys.argv) - 4)
