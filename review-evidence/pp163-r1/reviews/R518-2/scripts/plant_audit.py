#!/usr/bin/env python3
"""Reviewer plant audit of one source tree (no build, no run).

1. Every tb/**/*.patch must apply cleanly to the tree (git apply --check -p1 from
   the tree root, the form the patch headers a/hdl/... use).
2. Every exact-text arm of the exact-text drivers that edit the RTL this PR or
   its merges touch (notify_mutants, d3_mutants, acmp_mutants: edits applied in
   order, each old text exactly once; gsi_mutants: each edit's stated site count)
   must plant.

usage: plant_audit.py TREE OUT.json
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


def load(tree: Path, rel: str):
    sys.path.insert(0, str(tree / "tb/common"))
    spec = importlib.util.spec_from_file_location(Path(rel).stem + "_audit", tree / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sequential(tree: Path, edits) -> str:
    texts: dict[str, str] = {}
    for rel, old, new in edits:
        text = texts.get(rel)
        if text is None:
            text = (tree / rel).read_text()
        n = text.count(old)
        if n != 1:
            return f"{rel}: old text occurs {n} times"
        texts[rel] = text.replace(old, new, 1)
    return ""


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2])
    result: dict[str, object] = {"tree": str(tree.name)}
    patches = sorted(tree.glob("tb/**/*.patch"))
    bad = []
    for p in patches:
        r = subprocess.run(["git", "apply", "--check", "-p1", str(p)], cwd=tree,
                           capture_output=True, text=True)
        if r.returncode != 0:
            bad.append({"patch": str(p.relative_to(tree)), "stderr": r.stderr.strip()})
    result["patches"] = {"total": len(patches), "apply": len(patches) - len(bad), "refused": bad}
    drivers = {}
    edit_count_total = 0
    for rel in ("tb/pp_top/notify_mutants.py", "tb/pp_top/d3_mutants.py",
                "tb/pp_top/acmp_mutants.py"):
        mod = load(tree, rel)
        refused = []
        edits = 0
        for m in mod.MUTANTS:
            edits += len(m.edits)
            why = sequential(tree, m.edits)
            if why:
                refused.append({"mutant": m.name, "reason": why})
        edit_count_total += edits
        drivers[rel] = {"arms": len(mod.MUTANTS), "edits": edits, "refused": refused,
                        "names": [m.name for m in mod.MUTANTS]}
    gsi = load(tree, "tb/pp_top/gsi_mutants.py")
    refused = []
    rows = gsi.mutations()
    for name, rel, old, _new, count, _check in rows:
        n = (tree / rel).read_text().count(old)
        if n != count:
            refused.append({"mutant": name, "reason": f"{rel}: {n} sites, expected {count}"})
    drivers["tb/pp_top/gsi_mutants.py"] = {"arms": len(rows), "edits": len(rows),
                                            "refused": refused}
    result["exact_text"] = drivers
    ok = not bad and all(not d["refused"] for d in drivers.values())
    result["verdict"] = "PLANT" if ok else "REFUSED"
    out.write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps({"tree": tree.name, "patches": result["patches"]["total"],
                      "patch_refused": len(bad),
                      **{k: [v["arms"], v["edits"], len(v["refused"])] for k, v in drivers.items()},
                      "verdict": result["verdict"]}))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
