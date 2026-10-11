#!/usr/bin/env python3
"""Compare the full gmstep leg's check lines with the --no-small-steps run.

usage: compare_short.py <suite log> <short log>. The full leg is the first
transcript in the suite log, ending at its first 'gmstep: checks' line.
"""
import re
import sys

def checks(lines):
    return [l.rstrip("\n") for l in lines if re.match(r"\s*\[( ok |FAIL)\]", l)]

full_all = open(sys.argv[1]).read().splitlines(True)
end = next(i for i, l in enumerate(full_all) if "gmstep: checks" in l)
full = checks(full_all[:end + 1])
short = checks(open(sys.argv[2]).read().splitlines(True))
idx = [i for i, l in enumerate(full) if "621:" in l]
block = full[idx[0]:idx[-1] + 1]
rest = full[:idx[0]] + full[idx[-1] + 1:]
print(f"full={len(full)} short={len(short)} block={len(block)} (from the first to the last 621: check; {len(idx)} carry the prefix, the rest are the licence grades inside it)")
print(f"short equals full minus the contiguous #621 block: {short == rest}")
sys.exit(0 if short == rest else 1)
