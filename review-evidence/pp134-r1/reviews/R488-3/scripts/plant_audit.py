#!/usr/bin/env python3
"""Planting audit: every checked-in mutation arm still plants in a given tree.

Usage: plant_audit.py TREE   (an exported tree; its own tb/ drivers and patches are audited)
- every *.patch under tb/ is `git apply --check`ed at the tree root (the drivers' cwd);
- every exact-text arm (Mutant.edits) of the pp_top drivers with that shape is applied
  sequentially to in-memory copies; each `old` text must occur exactly once.
Prints one line per arm and a summary; exit 0 when every arm plants.
"""
import importlib.util, subprocess, sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
bad = total = 0
for patch in sorted(tree.glob("tb/**/*.patch")):
    total += 1
    r = subprocess.run(["git", "apply", "--check", str(patch)], cwd=tree,
                       capture_output=True, text=True)
    ok = r.returncode == 0
    bad += not ok
    print(f"{'PLANTS ' if ok else 'REFUSED'} patch {patch.relative_to(tree)}"
          + ("" if ok else f" :: {r.stderr.strip().splitlines()[0] if r.stderr.strip() else ''}"))
sys.path.insert(0, str(tree / "tb" / "common"))
for drv in sorted((tree / "tb").glob("*/*mutant*.py")):
    spec = importlib.util.spec_from_file_location(drv.stem + "_audit", drv)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        continue
    arms = getattr(mod, "MUTANTS", ())
    for m in arms:
        edits = getattr(m, "edits", None)
        if edits is None:
            continue
        total += 1
        files = {}
        why = ""
        for rel, old, new in edits:
            text = files.get(rel)
            if text is None:
                text = (tree / rel).read_text()
            if text.count(old) != 1:
                why = f"{rel}: planted text occurs {text.count(old)} times"
                break
            files[rel] = text.replace(old, new, 1)
        bad += bool(why)
        print(f"{'PLANTS ' if not why else 'REFUSED'} {drv.relative_to(tree)} {m.name} {why}")
print(f"plant audit {tree.name}: {total} arms, {total - bad} plant, {bad} refused")
sys.exit(1 if bad else 0)
