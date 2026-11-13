#!/usr/bin/env python3
"""Scan the arm's Python files at two commits with the parent's own scan().

usage: scan_arm_files.py <parent-checkout> <gptp-checkout> <commit>...
Reads each file's blob with `git show`, so no checkout is changed.
"""
import subprocess
import sys
from pathlib import Path

FILES = ("tb/verilator/engine/mutants.py", "tb/verilator/engine/path_mutants.py",
         "tb/mutation_jobs_test.py", "tb/mutation_order_test.py")


def main() -> int:
    parent, repo, *commits = sys.argv[1:]
    sys.path.insert(0, str(Path(parent) / "scripts"))
    import check_py_idiom as gate
    for commit in commits:
        for rel in FILES:
            show = subprocess.run(["git", "-C", repo, "show", f"{commit}:{rel}"],
                                  capture_output=True, text=True)
            if show.returncode:
                print(f"{commit[:8]} {rel}: absent")
                continue
            counts, sites = gate.scan(show.stdout, rel)
            nonzero = {k: v for k, v in counts.items() if v}
            print(f"{commit[:8]} {rel}: {len(show.stdout.splitlines())} lines, {nonzero or 'clean'}")
            for site in (sites if isinstance(sites, list) else []):
                print(f"    {site}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
