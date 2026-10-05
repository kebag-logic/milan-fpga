#!/usr/bin/env python3
"""Check that every mutation arm still plants at a revision, without simulating.

Usage: plant_check.py <clone> <scratch> <rev> [<rev> ...]

For each revision, extracts the tree with git archive into <scratch>/<rev>, then:
- runs `git apply --check` for every *.patch under tb/ (the drivers ctr_mutants.py,
  aecp_mutants.py and aecp_dispatch_mutants.py plant with git apply, refusing drift);
- for notify_mutants.py and d3_mutants.py (exact-text edits), requires every edit's
  old text to occur exactly once in its file, as the drivers' own plant() does.
Prints one line per arm that does not plant, then a per-revision tally.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path


def extract(clone: Path, rev: str, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    archive = subprocess.run(["git", "-C", str(clone), "archive", rev],
                             check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(dest)], input=archive, check=True)


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem + "_probe", path)
    module = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(module)
    return module


def check(tree: Path) -> tuple[int, int, list[str]]:
    total, bad, lines = 0, 0, []
    for patch in sorted(tree.glob("tb/**/*.patch")):
        total += 1
        res = subprocess.run(["git", "apply", "--check", str(patch)], cwd=tree,
                             capture_output=True, text=True)
        if res.returncode != 0:
            bad += 1
            lines.append(f"REFUSED patch {patch.relative_to(tree)}: "
                         + " ".join(res.stderr.split()))
    for driver in ("tb/pp_top/notify_mutants.py", "tb/pp_top/d3_mutants.py"):
        module = load(tree / driver)
        for mutant in module.MUTANTS:
            total += 1
            for rel, old, _new in mutant.edits:
                count = (tree / rel).read_text().count(old)
                if count != 1:
                    bad += 1
                    lines.append(f"REFUSED {driver} {mutant.name}: {rel} text occurs {count} times")
                    break
    return total, bad, lines


def main() -> int:
    clone, scratch, revs = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
    worst = 0
    for rev in revs:
        tree = scratch / rev
        extract(clone, rev, tree)
        total, bad, lines = check(tree)
        print(f"== {rev}")
        for line in lines:
            print(line)
        print(f"{rev}: {total} arms checked, {total - bad} plant, {bad} refused")
        worst = max(worst, bad)
    return 1 if worst else 0


if __name__ == "__main__":
    raise SystemExit(main())
