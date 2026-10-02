#!/usr/bin/env python3
"""Cell-by-cell comparison of the two conflicted rows (07 §3.1 L6 and
REQ-MDL-005) at base, the lane's round-3 head, main and the merge.
Usage: conflict_cells.py <repo>   (read-only: git show)"""
import subprocess
import sys

REPO = sys.argv[1]
REVS = {"base": "2ebd4fe8d31e88c44559e934bd624e1c50515ad5",
        "lane": "97f6eace064901f223e13abed7026f96bc4df805",
        "main": "631eeb342ca1e3fa80e734077a56a943aee76ff1",
        "merge": "3bfc7c66ef25ed28165cecc8fd98212793dca9a6",
        "head": "bd86f6466baa77113eea2266c00044c3a29678f2"}
ROWS = {"L6": ("docs/architecture/07_memory_maps.md", "| L6 |"),
        "REQ-MDL-005": ("docs/00_MILAN_COMPLIANCE_REVIEW.md", "| REQ-MDL-005 |")}


def row(rev: str, path: str, key: str) -> list[str]:
    text = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout
    hits = [ln for ln in text.splitlines() if ln.startswith(key)]
    assert len(hits) == 1, (rev, path, len(hits))
    return [c.strip() for c in hits[0].strip("|").split(" | ")]


for name, (path, key) in ROWS.items():
    cells = {r: row(v, path, key) for r, v in REVS.items()}
    print(f"== {name} ({path}); cells per revision: " +
          ", ".join(f"{r} {len(c)}" for r, c in cells.items()))
    print(f"   merge == head: {cells['merge'] == cells['head']}")
    for i in range(max(len(c) for c in cells.values())):
        get = {r: (c[i] if i < len(c) else None) for r, c in cells.items()}
        src = [r for r in ("main", "lane", "base") if get[r] == get["merge"]]
        print(f"   cell {i}: merge equals {src or 'NEITHER'}")
        if not src:
            for r in ("lane", "main", "merge"):
                print(f"      {r}: {get[r]}")
