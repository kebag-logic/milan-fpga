#!/usr/bin/env python3
"""compare_equiv.py <dir> <cycles> <period>...: staged and undelayed DFI commands against
LiteDRAM's own (plain) shifted one cycle, inside the run's window; spacing of REFRESH and ZQCS."""
import json, sys
d, cycles = sys.argv[1], int(sys.argv[2])
bad = 0
for p in sys.argv[3:]:
    plain = [tuple(c) for c in json.load(open(f"{d}/{p}_plain.json"))]
    shifted = [(c + 1, i, n, a) for c, i, n, a in plain if c + 1 < cycles]
    zq = [c for c, _, n, _ in plain if n == "ZQCS"]
    ref = [c for c, _, n, _ in plain if n == "REFRESH"]
    gaps = sorted({b - a for a, b in zip(ref, ref[1:])})
    print(f"period {p}: plain {len(plain)} commands, REFRESH {len(ref)} spacing {gaps}, ZQCS {len(zq)} at {zq}")
    for s in ("staged", "undelayed"):
        got = [tuple(c) for c in json.load(open(f"{d}/{p}_{s}.json"))]
        szq = [c for c, _, n, _ in got if n == "ZQCS"]
        same = got == shifted
        first = next((k for k, (a, b) in enumerate(zip(got, shifted)) if a != b), min(len(got), len(shifted)))
        print(f"  {s:9s}: {len(got)} commands, ZQCS {len(szq)} at {szq}; equals plain+1: {same}"
              + ("" if same else f" (first difference at command {first})"))
        if s == "staged" and not same:
            bad += 1
        if s == "undelayed" and same and zq:
            bad += 1
print("RESULT:", "PASS" if not bad else "FAIL")
sys.exit(1 if bad else 0)
