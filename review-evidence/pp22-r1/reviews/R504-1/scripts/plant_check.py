#!/usr/bin/env python3
"""Planting check over one exported processor tree.

usage: plant_check.py <tree> <out.json>

1. every tracked tb/**/*.patch: `git apply --check` from the tree root, in a
   throwaway repository so the export itself is never written;
2. every exact-text arm of every tb/**/*_mutants.py table that defines both
   MUTANTS and plant(): each arm is planted by that table's own plant() into a
   fresh copy of the files it edits, and the refusal text (if any) is kept.
Also records, for the two files this PR edits, which patches and arms touch them.
"""
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

tree = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2])
EDITED = ("hdl/packet_engine/KL_pp_originator.sv", "hdl/packet_engine/KL_pp_rx_validator.sv")

res = {"tree": tree.name, "patches": [], "tables": {}}
with tempfile.TemporaryDirectory() as td:
    work = pathlib.Path(td) / "w"
    shutil.copytree(tree, work)
    subprocess.run(["git", "init", "-q"], cwd=work, check=True)
    for p in sorted(work.glob("tb/**/*.patch")):
        rel = str(p.relative_to(work))
        r = subprocess.run(["git", "apply", "--check", rel], cwd=work, capture_output=True, text=True)
        text = p.read_text(errors="replace")
        res["patches"].append({"patch": rel, "rc": r.returncode, "stderr": r.stderr.strip(),
                               "touches_edited": [e for e in EDITED if e in text]})

for py in sorted(tree.glob("tb/**/*.py")):
    src = py.read_text(errors="replace")
    if "def plant(" not in src or "MUTANTS" not in src:
        continue
    spec = importlib.util.spec_from_file_location(py.stem, py)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(py.parent))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.pop(0)
    arms = []
    for m in mod.MUTANTS:
        edits = getattr(m, "edits", None)
        if edits is None:
            arms.append({"name": getattr(m, "name", repr(m)[:60]), "shape": "no-edits-field"})
            continue
        with tempfile.TemporaryDirectory() as td:
            t = pathlib.Path(td)
            for rel in {e[0] for e in edits}:
                (t / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(tree / rel, t / rel)
            why = mod.plant(t, tuple(edits))
            changed = all((t / rel).read_text() != (tree / rel).read_text() for rel in {e[0] for e in edits})
        arms.append({"name": m.name, "planted": why == "", "refusal": why, "changed": changed,
                     "files": sorted({e[0] for e in edits}),
                     "touches_edited": sorted({e[0] for e in edits} & set(EDITED))})
    res["tables"][str(py.relative_to(tree))] = arms

pp = res["patches"]
res["summary"] = {
    "patches": len(pp), "patches_ok": sum(p["rc"] == 0 for p in pp),
    "patches_touching_edited": [p["patch"] for p in pp if p["touches_edited"]],
    "tables": {k: {"arms": len(v), "planted": sum(a.get("planted", False) for a in v),
                   "changed": sum(a.get("changed", False) for a in v),
                   "arms_touching_edited": sum(bool(a.get("touches_edited")) for a in v)}
               for k, v in res["tables"].items()},
}
out.write_text(json.dumps(res, indent=1) + "\n")
print(json.dumps(res["summary"], indent=1))
