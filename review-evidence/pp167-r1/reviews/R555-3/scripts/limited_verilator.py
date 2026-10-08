#!/usr/bin/env python3
"""Use the pinned compiler with a four-worker build limit."""
import os
import sys
args = sys.argv[1:]
for i in range(len(args) - 2, -1, -1):
    if args[i] in ("-j", "--build-jobs"):
        del args[i:i + 2]
if "--build" in args:
    args += ["-j", "4"]
compiler = os.environ.get("REVIEW_VERILATOR", "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator")
os.execv(compiler, [compiler, *args])
