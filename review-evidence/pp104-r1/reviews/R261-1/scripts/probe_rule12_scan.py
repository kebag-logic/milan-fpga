#!/usr/bin/env python3
"""Run the parent's Rule 12 scanner over this repository's tracked Python.

Usage: probe_rule12_scan.py <parent-scripts-dir> <pp-repo> <rev> [<rev> ...]

Imports scan() from the parent's scripts/check_py_idiom.py (fetched at parent
live dev) and applies it, file by file, to every `git ls-tree` *.py blob of the
protocol-processor repository at each revision -- the same per-file function
the parent gate sums over the pinned submodule. Prints per-revision totals for
every counter and the sites for the two Rule 12 signature/docstring counters.
This is a focused reproduction of the submodule's contribution only; it is not
the parent gate's whole-population verdict.
"""

import subprocess
import sys


def blobs(repo: str, rev: str) -> list[str]:
    out = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev],
                         check=True, capture_output=True, text=True).stdout
    return sorted(p for p in out.splitlines() if p.endswith(".py"))


def main() -> int:
    scripts, repo, *revs = sys.argv[1:]
    sys.path.insert(0, scripts)
    import check_py_idiom as gate  # noqa: E402  (parent gate, unmodified)

    for rev in revs:
        totals: dict[str, int] = {}
        sites: list[str] = []
        paths = blobs(repo, rev)
        for path in paths:
            text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                                  check=True, capture_output=True, text=True).stdout
            counts, where = gate.scan(text, "protocol-processor/" + path)
            for key, n in counts.items():
                totals[key] = totals.get(key, 0) + n
            for key in ("unannotated public function", "undocumented public function"):
                for lineno, detail in where.get(key, []):
                    sites.append(f"    {key}: {path}:{lineno} {detail}")
        print(f"== rev {rev}: {len(paths)} tracked *.py")
        for key in sorted(totals):
            print(f"  {key}: {totals[key]}")
        print("  rule-12 signature/docstring sites:")
        print("\n".join(sites) if sites else "    (none)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
