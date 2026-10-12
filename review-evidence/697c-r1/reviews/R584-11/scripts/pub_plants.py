#!/usr/bin/env python3
"""Compare dev's and the head's pub-acmp plants field by field and count each fixture in the target file.
usage: pub_plants.py <dev tree> <head tree>"""
import importlib, sys
from pathlib import Path

def load(tree):
    t = Path(tree) / "sw/firmware/ctrl/test"
    for extra in (t, Path(tree) / "sw/firmware/gtest"):
        sys.path.insert(0, str(extra))
    for m in [m for m in list(sys.modules) if m.startswith(("ctrl_", "fw_", "acmp_", "srp_", "aecp_", "maap_"))]:
        del sys.modules[m]
    mod = importlib.import_module("ctrl_mutants")
    sys.path[:] = [p for p in sys.path if not p.startswith(str(tree))]
    return {m.name: m for m in mod.MUTANTS}

dev, head = load(sys.argv[1]), load(sys.argv[2])
pub = sorted(n for n in dev if n.startswith("pub-acmp-") and dev[n].path == "acmp/acmp.c")
print(f"dev pub-acmp core plants: {len(pub)}")
bad = 0
for n in pub:
    d, h = dev[n], head.get(n)
    if h is None:
        print(f"MISSING {n}"); bad += 1; continue
    fields = [f for f in d.__dataclass_fields__ if f != "path"] if hasattr(d, "__dataclass_fields__") else \
             [f for f in d._fields if f != "path"]
    same = all(getattr(d, f) == getattr(h, f) for f in fields)
    target = Path(sys.argv[2]) / "third_party/tsn-c-stack" / Path(h.path).relative_to("tsn-c-stack") \
        if str(h.path).startswith("tsn-c-stack") else None
    text = Path(target).read_text() if target and target.is_file() else ""
    count = text.count(h.old)
    print(f"{'SAME' if same else 'CHANGED'} {n}: path {d.path} -> {h.path}; fixture count in target {count}")
    bad += (not same) or count != 1
print(f"other fields changed or fixture not unique: {bad}")
print("head names equal dev names:", sorted(dev) == sorted(head), len(dev), len(head))
sys.exit(1 if bad else 0)
