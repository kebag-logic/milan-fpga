#!/usr/bin/env python3
"""Static plant check: does every mutation arm of the drivers that build tb/pp_top
still find its planted text in a given source tree?

Exact-edit drivers (tb/pp_top notify_mutants, d3_mutants, acmp_mutants): every
(file, old, new) edit's old text must occur exactly once (their own plant() rule).
Patch drivers (tb/pp_top mutations/, aecp_dispatch_mutations/, ctr_mutations/,
tb/adp_engine mutations/, tb/maap mutations/): `git apply --check` from a copy of
the tree must accept the patch. Nothing is built; nothing is written in TREE.

Usage: plant_check.py TREE   (prints one line per arm and a summary; rc 0 iff all plant)
"""
import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem + "_probe", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    bad = 0
    total = 0
    for drv in ("notify_mutants.py", "d3_mutants.py", "acmp_mutants.py"):
        mod = load(tree / "tb/pp_top" / drv)
        for m in mod.MUTANTS:
            total += 1
            why = ""
            for rel, old, _new in m.edits:
                n = (tree / rel).read_text().count(old)
                if n != 1:
                    why = f"{rel}: {n} occurrences"
                    break
            bad += bool(why)
            print(f"{'PLANTS ' if not why else 'REFUSED'} {drv} {m.name} {why}")
    with tempfile.TemporaryDirectory(prefix="plant-check-") as tmp:
        copy = Path(tmp) / "t"
        shutil.copytree(tree, copy, ignore=shutil.ignore_patterns("obj*", "scratch"))
        for d in ("tb/pp_top/mutations", "tb/pp_top/aecp_dispatch_mutations",
                  "tb/pp_top/ctr_mutations", "tb/adp_engine/mutations", "tb/maap/mutations"):
            for p in sorted((tree / d).glob("*.patch")):
                total += 1
                r = subprocess.run(["git", "apply", "--check", str(p)], cwd=copy,
                                   capture_output=True, text=True)
                bad += r.returncode != 0
                print(f"{'PLANTS ' if r.returncode == 0 else 'REFUSED'} {d}/{p.name} "
                      f"{r.stderr.strip()}")
    print(f"SUMMARY {total - bad} of {total} arms plant; {bad} refused")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
