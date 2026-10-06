#!/usr/bin/env python3
"""Cap the scoped simulator's build workers without changing source files."""
import os
import sys

binary = os.environ.get("REVIEW_VERILATOR", "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator")
args = sys.argv[1:]
for i in range(len(args)-1):
    if args[i] == "-j":
        args[i+1] = "2"
os.execv(binary, [binary, *args])
