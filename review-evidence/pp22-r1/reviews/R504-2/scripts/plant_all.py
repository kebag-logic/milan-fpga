#!/usr/bin/env python3
"""Planting census over one exported source tree.

Usage: plant_all.py <export_root> <out.json>

1. Every tracked tb/**/*.patch: `git apply --check` from the export root.
2. Every exact-text arm (tables whose plant() takes an edits tuple): each arm is
   planted with the table's own plant() into a fresh scratch copy of the files
   it edits.
3. Every patch-driven table: each MUTANTS label resolves to an existing patch.
This is a planting census, not a kill claim.
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
res = {"root": str(root), "patches": [], "exact": {}, "labels": {}}

patches = sorted(p.relative_to(root).as_posix() for p in root.glob("tb/**/*.patch"))
for p in patches:
    r = subprocess.run(["git", "apply", "--check", p], cwd=root, capture_output=True, text=True)
    res["patches"].append({"arm": p, "rc": r.returncode, "detail": r.stderr.strip()[:300]})


def load(rel):
    spec = importlib.util.spec_from_file_location(Path(rel).stem + "_r504", root / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str((root / rel).parent))
    spec.loader.exec_module(mod)
    sys.path.pop(0)
    return mod


for rel in ("tb/pp_top/acmp_mutants.py", "tb/pp_top/d3_mutants.py", "tb/pp_top/notify_mutants.py"):
    mod = load(rel)
    rows = []
    for m in mod.MUTANTS:
        name = getattr(m, "name", None) or getattr(m, "label", None) or repr(m)[:60]
        with tempfile.TemporaryDirectory(prefix="r504-plant-") as tmp:
            tree = Path(tmp)
            for f in {e[0] for e in m.edits}:
                (tree / f).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(root / f, tree / f)
            refusal = mod.plant(tree, m.edits)
            changed = all((tree / f).read_bytes() != (root / f).read_bytes() for f in {e[0] for e in m.edits})
        rows.append({"arm": name, "edits": len(m.edits), "refusal": refusal, "changed": changed})
    res["exact"][rel] = rows

# tuple index of the patch name each table hands to its own plant()
PATCH_IX = {"tb/adp_engine/mutants.py": 1, "tb/maap/mutants.py": 0,
            "tb/pp_top/aecp_dispatch_mutants.py": 1, "tb/pp_top/aecp_mutants.py": 1,
            "tb/pp_top/ctr_mutants.py": 0, "tb/srp_top/mutants.py": 0}
for rel, ix in PATCH_IX.items():
    mod = load(rel)
    pdir = Path(mod.PATCHES)
    labels = []
    for m in mod.MUTANTS:
        lab = m[ix]
        labels.append({"label": lab, "exists": (pdir / (str(lab) + ".patch")).is_file()})
    res["labels"][rel] = labels

pfail = [p for p in res["patches"] if p["rc"]]
efail = {k: [r for r in v if r["refusal"] or not r["changed"]] for k, v in res["exact"].items()}
lfail = {k: [r for r in v if not r["exists"]] for k, v in res["labels"].items()}
res["summary"] = {
    "patches": len(res["patches"]), "patch_fail": len(pfail),
    "exact": {k: len(v) for k, v in res["exact"].items()},
    "exact_fail": {k: len(v) for k, v in efail.items()},
    "labels": {k: len(v) for k, v in res["labels"].items()},
    "label_missing": {k: len(v) for k, v in lfail.items()},
}
out.write_text(json.dumps(res, indent=1) + "\n")
print(json.dumps(res["summary"], indent=1))
for p in pfail:
    print("PATCH FAIL", p)
for k, v in efail.items():
    for r in v:
        print("EXACT FAIL", k, r)
for k, v in lfail.items():
    for r in v:
        print("LABEL MISSING", k, r)
sys.exit(1 if pfail or any(efail.values()) or any(lfail.values()) else 0)
