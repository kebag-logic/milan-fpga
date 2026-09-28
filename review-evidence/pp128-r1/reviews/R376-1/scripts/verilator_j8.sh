#!/usr/bin/env python3
# Run the pinned Verilator (PINNED_VERILATOR) with every "-j N" rewritten to
# "-j 8", so a suite Makefile's "--build -j 0" stays within 8 parallel jobs.
import os
import sys

tool = os.environ.get("PINNED_VERILATOR")
if not tool:
    sys.exit("set PINNED_VERILATOR to the pinned Verilator 5.050 wrapper")
argv, out, i = sys.argv[1:], [], 0
while i < len(argv):
    if argv[i] == "-j" and i + 1 < len(argv):
        out += ["-j", "8"]
        i += 2
        continue
    out.append(argv[i])
    i += 1
os.execv(tool, [tool] + out)
