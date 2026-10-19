#!/usr/bin/env python3
import os, subprocess, sys
real = os.environ.get("REVIEW_SIM", "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator")
a = sys.argv[1:]
for i in range(len(a)-1):
    if a[i] in ("-j", "--build-jobs"): a[i+1] = os.environ.get("REVIEW_BUILD_JOBS", "4")
os.execv(real, [real] + a)
