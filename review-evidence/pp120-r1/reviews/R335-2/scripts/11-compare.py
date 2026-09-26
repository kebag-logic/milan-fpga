#!/usr/bin/env python3
"""Compare two 10-pp_top-builds.sh receipt directories.

Reports (1) the Verilator %Warning sets with source line numbers removed,
(2) C++ compiler warnings, and (3) byte equality of each simulation's own
output (default run, fixture run, name-write-only run).
Usage: 11-compare.py <old-receipt-dir> <new-receipt-dir>
"""
import re
import sys
from pathlib import Path


def warnings(text):
    """Return the sorted Verilator warning heads, line/column numbers removed."""
    out = []
    for line in text.splitlines():
        if line.startswith("%Warning"):
            out.append(re.sub(r":\d+:\d+:", ":L:C:", line))
    return sorted(out)


def cxx_warnings(text):
    """Return every C++ compiler warning line."""
    return [line for line in text.splitlines() if "warning:" in line]


def sim_sections(text):
    """Return the stdout of each simulation binary run in one log."""
    sections, cur, name = {}, None, None
    for line in text.splitlines():
        if line.startswith("./obj_dir/Vpp_top_sim") or line.startswith("./obj_vid/Vpp_top_vid"):
            name, cur = line.strip(), []
            sections[name] = cur
            continue
        if cur is not None and (line.startswith("<packet>/") or line.startswith("make") or "verilator" in line.split(" ")[0]):
            cur = None
            continue
        if cur is not None:
            cur.append(line)
    return sections


def main():
    old, new = Path(sys.argv[1]), Path(sys.argv[2])
    rc = 0
    for log in ("run.log", "name-writes.log"):
        a, b = (old / log).read_text(), (new / log).read_text()
        wa, wb = warnings(a), warnings(b)
        print(f"{log}: verilator warnings old={len(wa)} new={len(wb)} "
              f"set-equal(line-numbers-stripped)={wa == wb}")
        for w in sorted(set(wa) ^ set(wb)):
            print("  differs:", w)
        print(f"{log}: c++ warnings old={len(cxx_warnings(a))} new={len(cxx_warnings(b))}")
        for w in cxx_warnings(a):
            print("  old:", w)
        for w in cxx_warnings(b):
            print("  new:", w)
        sa, sb = sim_sections(a), sim_sections(b)
        for key in sorted(set(sa) | set(sb)):
            la, lb = sa.get(key), sb.get(key)
            same = la == lb
            n = "-" if lb is None else len(lb)
            print(f"{log}: sim '{key}' lines={n} identical={same}")
            if not same:
                rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
