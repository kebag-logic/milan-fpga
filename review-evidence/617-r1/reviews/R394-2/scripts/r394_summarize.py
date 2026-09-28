#!/usr/bin/env python3
"""Summarize r394_probe.py / capture_coherence logs: one row per CRF engagement.

  python3 r394_summarize.py <log> [<log> ...]

Row: name, landed offset, close movement range, repeats, skips, and any
[FAIL] lines of that scenario. Then totals: engagements, with any slip, with a
[FAIL], and the shard tallies.
"""

import re
import sys

ROW = re.compile(r"\[i\]\s+(\S+): engaged ([+-]\d+) cycles from the crossing, the close then moved "
                 r"([+-]\d+)\.\.([+-]\d+) \(furthest at column (\d+)\); tail: tick (\d+) cycles after the frame "
                 r"close, ([+-]\d+)\.\.([+-]\d+) \(spread (\d+)\); (\d+) repeats, (\d+) skips")


def main() -> int:
    for path in sys.argv[1:]:
        rows, fails, tallies = [], [], []
        for line in open(path, encoding="utf-8", errors="replace"):
            m = ROW.search(line)
            if m:
                rows.append(m.groups())
            elif "[FAIL]" in line:
                fails.append(line.strip())
            elif "checks:" in line and "failures:" in line:
                tallies.append(line.strip())
        print(f"== {path}")
        print(f"{'name':28s} {'landed':>6s} {'moved':>12s} {'far_col':>7s} {'rep':>4s} {'skip':>4s}")
        for g in rows:
            name, landed, mlo, mhi, far, _tick, _tlo, _thi, _spread, rep, skip = g
            print(f"{name:28s} {landed:>6s} {mlo + '..' + mhi:>12s} {far:>7s} {rep:>4s} {skip:>4s}")
        slipping = [g[0] for g in rows if g[9] != "0" or g[10] != "0"]
        print(f"engagements: {len(rows)}; with any repeat/skip: {len(slipping)} {slipping}")
        print(f"[FAIL] lines: {len(fails)}")
        for f in fails:
            print("  ", f)
        for t in tallies:
            print("  tally:", t)
    return 0


if __name__ == "__main__":
    sys.exit(main())
