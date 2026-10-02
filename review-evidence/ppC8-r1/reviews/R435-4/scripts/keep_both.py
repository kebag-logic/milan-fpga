#!/usr/bin/env python3
"""keep_both.py <repo>

For the two rows the merge 3bfc7c6 resolved by hand (07 §3.1 L6 and
REQ-MDL-005), splits main's (631eeb34) row and the lane's (97f6eace) row
into table cells and sentences, and reports each piece that does not occur
verbatim in the merged row at bd86f646. Also prints the merged row's text
that neither side carries."""
import re
import subprocess
import sys

repo = sys.argv[1]
MAIN, LANE, HEAD = "631eeb342ca1e3fa80e734077a56a943aee76ff1", \
    "97f6eace064901f223e13abed7026f96bc4df805", "bd86f6466baa77113eea2266c00044c3a29678f2"
ROWS = (("docs/architecture/07_memory_maps.md", "| L6 |"),
        ("docs/00_MILAN_COMPLIANCE_REVIEW.md", "| REQ-MDL-005 |"))


def row(rev, path, key):
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout
    hits = [ln for ln in text.splitlines() if ln.startswith(key)]
    assert len(hits) == 1, (rev, path, len(hits))
    return hits[0]


def pieces(line):
    out = []
    for cell in [c.strip() for c in line.strip("|").split(" | ")]:
        out += [p.strip() for p in re.split(r"(?<=[.;:])\s+(?=[A-Z(`≥e])", cell) if p.strip()]
    return out


for path, key in ROWS:
    m, l, h = (row(r, path, key) for r in (MAIN, LANE, HEAD))
    print(f"== {path} {key}")
    for side, line in (("main", m), ("lane", l)):
        missing = [p for p in pieces(line) if p not in h]
        print(f"  {side}: {len(pieces(line))} pieces, {len(missing)} not verbatim in the merged row")
        for p in missing:
            print(f"    - {p}")
    new = [p for p in pieces(h) if p not in m and p not in l]
    print(f"  merged row: {len(new)} pieces in neither side verbatim")
    for p in new:
        print(f"    + {p}")
