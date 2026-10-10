#!/usr/bin/env python3
"""Compare the boundary self-test's planted controls of two trees: every control of <base> must exist at <head>
with the same plant fields and the same needle. Usage: python3 -I compare_plants.py <base-tree> <head-tree>"""
import dataclasses, importlib, sys
from pathlib import Path

def plants(tree):
    d = str(Path(tree).resolve() / "sw/firmware/ctrl/test")
    sys.path.insert(0, d)
    for m in [m for m in sys.modules if m.startswith(("ctrl_", "fw_", "srp_", "endstation"))]:
        del sys.modules[m]
    try:
        mod = importlib.import_module("ctrl_plants")
    except ModuleNotFoundError:
        mod = importlib.import_module("ctrl_boundary")
    out = {p.name: dataclasses.asdict(p) for p in mod.PLANTS}
    for f in out.values():  # the field "mode" was renamed "words" at the head
        if "mode" in f:
            f["words"] = f.pop("mode")
    sys.path.remove(d)
    return out, getattr(mod, "BASE", None)

a, _ = plants(sys.argv[1])
b, base = plants(sys.argv[2])
print(f"base controls {len(a)}, head controls {len(b)}, head base control: {base.name if base else None}")
bad = 0
for name, fields in a.items():
    if name not in b:
        print("MISSING at head:", name); bad += 1; continue
    diff = {k: (v, b[name].get(k)) for k, v in fields.items() if b[name].get(k) != v}
    if diff:
        print("CHANGED:", name, diff); bad += 1
new = [n for n in b if n not in a]
print(f"kept unchanged: {len(a) - bad} of {len(a)}; new at head: {len(new)}")
for n in new:
    print("  new:", n, "| needle:", b[n]["needle"][:110])
sys.exit(1 if bad else 0)
