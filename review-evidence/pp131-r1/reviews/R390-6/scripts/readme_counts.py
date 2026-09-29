#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R390-6: compare each D3 mutant's README "Failing checks" count with the run.

Reads every results.json given, and the mutation tables in the three READMEs
that record D3 mutants (tb/pp_top, tb/acmp_nvm, tb/rx_validator). A README row
is a table row whose first cell is a backquoted mutant name and whose last cell
is an integer. Reports each mutant in the run with its README count, run count,
and any mismatch, missing row or duplicate row.

Usage: python3 readme_counts.py --tree CLONE RESULTS.json [RESULTS.json ...]
"""

import argparse
import json
import re
from pathlib import Path

ROW = re.compile(r"^\|\s*`([A-Za-z0-9_]+)`\s*\|.*\|\s*(\d+)\s*\|\s*$")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tree", type=Path, required=True)
    parser.add_argument("results", nargs="+", type=Path)
    args = parser.parse_args()
    rows = {}
    dup = []
    for readme in ("tb/pp_top/README.md", "tb/acmp_nvm/README.md", "tb/rx_validator/README.md"):
        for line in (args.tree / readme).read_text().splitlines():
            m = ROW.match(line)
            if m:
                if m.group(1) in rows:
                    dup.append(m.group(1))
                rows[m.group(1)] = (readme, int(m.group(2)))
    runs = {}
    for path in args.results:
        for r in json.loads(path.read_text()):
            if not r["mutant"].startswith("golden-"):
                runs[r["mutant"]] = r
    problems = 0
    for name in sorted(runs):
        r = runs[name]
        n = len(r.get("failing_checks", []))
        readme, want = rows.get(name, ("-", None))
        ok = want == n and r["verdict"] == "KILLED"
        problems += not ok
        print(f"{'OK ' if ok else 'BAD'} {name:45s} {r['verdict']:8s} run={n:3d} readme={want} ({readme})")
    print(f"mutants in run: {len(runs)}; problems: {problems}; duplicate README rows: {dup}")
    return 1 if problems or dup else 0


if __name__ == "__main__":
    raise SystemExit(main())
