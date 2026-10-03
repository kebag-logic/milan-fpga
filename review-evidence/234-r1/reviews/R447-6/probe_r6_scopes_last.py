#!/usr/bin/env python3
"""Is the delta mutant "SCOPES any last key" equivalent? Run check-baseline in its scratch copy (and in an
unmutated copy) on baseline copies whose record identity, figures or tolerance object holds a bracketed key.
Usage: probe_r6_scopes_last.py <mutant copy dir> <control copy dir> <repo checkout> <scratch dir>
"""
import json, subprocess, sys
from pathlib import Path
mutant, control, repo, tmp = (Path(arg).resolve() for arg in sys.argv[1:5])
tmp.mkdir(parents=True, exist_ok=True)
base = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())
budget = repo / "docs/design/AREA_BUDGET.md"
def case(label, edit):
    data = json.loads(json.dumps(base))
    edit(data)
    path = tmp / ("".join(ch if ch.isalnum() else "_" for ch in label) + ".json")
    path.write_text(json.dumps(data, indent=2))
    for name, folder in (("mutant", mutant), ("control", control)):
        r = subprocess.run([sys.executable, "-B", "pp_resource_gate.py", "check-baseline", "--baseline", str(path),
                            "--budget", str(budget)], cwd=folder, capture_output=True, text=True)
        print(f"{label} [{name}]: rc {r.returncode} :: {(r.stdout + r.stderr).strip().splitlines()[-1][:200]}")
def rename(where, old, new):
    def edit(data):
        obj = data
        for key in where: obj = obj[key]
        obj[new] = obj.pop(old)
    return edit
def add(where, key, value):
    def edit(data):
        obj = data
        for k in where: obj = obj[k]
        obj[key] = value
    return edit
rec = ("endpoints", "route-1x1", "record")
case("figures key LUT renamed LUT[1]", rename(rec + ("figures",), "LUT", "LUT[1]"))
case("figures extra key x[1]", add(rec + ("figures",), "x[1]", 1))
case("identity key tool renamed tool[1]", rename(rec + ("identity",), "tool", "tool[1]"))
case("identity extra key x[1]", add(rec + ("identity",), "x[1]", "a"))
case("tolerance key renamed with brackets (endpoint level, not record)",
     lambda d: d["endpoints"]["route-1x1"]["tolerance"].update({"x[1]": 1}))
