#!/usr/bin/env python3
"""attribution_census.py - list each accepted MRPDU the bench marks neither Join-gated nor requested.

Usage: python3 -I attribution_census.py CAPTURE.json [...]

For each capture (srptx.hpp's write()), every lib record with rc 0 is classed by the bench's own per-poll
record: after_join (sent at the first poll after a Join expiry), requested (idle_us >= 0), or neither.
Each 'neither' record is printed with its ms, protocol, the gap in ms from the previous accepted record
of the same protocol, and whether that gap is inside JoinTime's widened range (160 to 260 ms).
"""
from __future__ import annotations

import json
import sys


def main() -> int:
    for path in sys.argv[1:]:
        doc = json.load(open(path))
        lib = [r for r in doc["lib"] if r["rc"] == 0]
        prev: dict[str, float] = {}
        rows = []
        for r in lib:
            kind = "after_join" if r["after_join"] else "requested" if r["idle_us"] >= 0 else "neither"
            gap = (r["us"] - prev[r["proto"]]) / 1000 if r["proto"] in prev else None
            if kind == "neither":
                rows.append((r["ms"], r["proto"], gap))
            prev[r["proto"]] = r["us"]
        print(f"{path}: {len(lib)} accepted, {len(rows)} neither")
        for ms, proto, gap in rows:
            g = "first" if gap is None else f"{gap:.3f} ms after the previous {proto}"
            inside = "" if gap is None else (" (inside 160..260)" if 160 <= gap <= 260 else " (OUTSIDE 160..260)")
            print(f"   ms {ms} {proto}: {g}{inside}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
