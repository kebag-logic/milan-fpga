#!/usr/bin/env python3
"""Check, without simulating, that every planting mutation arm of a tree still plants.

TREE is a git-archive extraction (not a git work tree), the way the drivers'
scratch copies are. Two arm forms are checked:
  * every tb/**/*.patch: `git apply --check PATCH` with cwd=TREE, as every
    patch driver plants (adp_engine, maap, srp_top, pp_top aecp/dispatch/ctr);
  * every exact-text edit of tb/pp_top/notify_mutants.py and d3_mutants.py:
    each old text must occur exactly once, edits applied in order in memory,
    as their plant() does.
Prints one line per refused arm, a per-family tally, and the total; rc 0 only
when every arm plants.
Usage: plant_check.py TREE
"""
import importlib.util
from pathlib import Path
import subprocess
import sys


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(module)
    return module


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    if (tree / ".git").exists():
        print("refusing: TREE is a git work tree")
        return 2
    tally = {}
    refused = []
    for patch in sorted(tree.glob("tb/**/*.patch")):
        family = str(patch.parent.relative_to(tree))
        r = subprocess.run(["git", "apply", "--check", str(patch)], cwd=tree,
                           capture_output=True, text=True)
        ok, total = tally.get(family, (0, 0))
        tally[family] = (ok + (r.returncode == 0), total + 1)
        if r.returncode != 0:
            refused.append(f"REFUSED {patch.relative_to(tree)}: {r.stderr.strip()}")
    for driver in ("tb/pp_top/notify_mutants.py", "tb/pp_top/d3_mutants.py"):
        module = load(tree / driver)
        ok = total = 0
        for m in module.MUTANTS:
            files = {}
            reason = ""
            for rel, old, new in m.edits:
                text = files.get(rel)
                if text is None:
                    text = (tree / rel).read_text()
                if text.count(old) != 1:
                    reason = f"{rel}: the planted text occurs {text.count(old)} times"
                    break
                files[rel] = text.replace(old, new, 1)
            total += 1
            ok += not reason
            if reason:
                refused.append(f"REFUSED {driver}:{m.name}: {reason}")
        tally[driver] = (ok, total)
    for line in refused:
        print(line)
    for family, (ok, total) in sorted(tally.items()):
        print(f"{family}: {ok} of {total} plant")
    ok = sum(v[0] for v in tally.values())
    total = sum(v[1] for v in tally.values())
    print(f"TOTAL: {ok} of {total} arms plant")
    return int(ok != total)


if __name__ == "__main__":
    raise SystemExit(main())
