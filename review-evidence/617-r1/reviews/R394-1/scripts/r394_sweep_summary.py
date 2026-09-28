#!/usr/bin/env python3
"""Summarise an r394_crf_phase_probe.py log: one row per CRF start delay.

  python3 r394_sweep_summary.py <log>

Prints delay, the tick-to-close lock phase, torn columns, repeats/skips, the
committed harness's [FAIL] names for the scenario, and the per-pair tail
slips; then counts scenarios with any tail slip on any pair, with torn
columns, and with a committed-check failure.
"""

import re
import sys


def main() -> int:
    rows, cur = [], None
    for line in open(sys.argv[1], encoding="utf-8"):
        m = re.match(r"\[P\w+-d(\d+)\]", line)
        if m:
            cur = {"d": int(m.group(1)), "fails": [], "phase": "", "torn": 0, "rep": 0, "skp": 0, "pp": [0] * 4}
            rows.append(cur)
            continue
        if cur is None:
            continue
        if "[FAIL]" in line:
            cur["fails"].append(line.split("] ", 2)[-1].split(" got=")[0].strip())
        m = re.search(r"CRF tail: tick (\d+) cycles", line)
        if m:
            cur["phase"] = m.group(1)
        m = re.search(r"(\d+) torn \([\d.]+%\), (\d+) repeats, (\d+) skips", line)
        if m:
            cur["torn"], cur["rep"], cur["skp"] = (int(x) for x in m.groups())
        m = re.search(r"tail per-pair slips: (\d+) (\d+) (\d+) (\d+)", line)
        if m:
            cur["pp"] = [int(x) for x in m.groups()]
    slip_rows = [r for r in rows if any(r["pp"])]
    torn_rows = [r for r in rows if r["torn"]]
    fail_rows = [r for r in rows if r["fails"]]
    print("delay phase torn rep skp tail-per-pair-slips fails")
    for r in rows:
        if any(r["pp"]) or r["fails"] or r["rep"] or r["skp"]:
            print(r["d"], r["phase"], r["torn"], r["rep"], r["skp"], r["pp"], "; ".join(sorted(set(r["fails"]))))
    print(f"scenarios {len(rows)}; with tail slips on any pair {len(slip_rows)}; "
          f"with torn columns {len(torn_rows)}; with a committed-check FAIL {len(fail_rows)}")
    print("tail-slip scenarios per pair:", [sum(1 for r in rows if r["pp"][p]) for p in range(4)])
    return 0


if __name__ == "__main__":
    sys.exit(main())
