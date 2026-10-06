#!/usr/bin/env python3
"""Use the selected simulator with a bounded native build."""
import os, sys
real = os.environ.get("REVIEW_VERILATOR", "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator")
a = sys.argv[1:]
for i in range(len(a)-1):
    if a[i] == "-j": a[i+1] = "3"
os.execv(real, [real] + a)
