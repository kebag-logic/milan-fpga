#!/usr/bin/env python3
"""Bound compilation fanout; use the explicitly selected simulator."""
import os, sys
args=sys.argv[1:]; out=[]; i=0
while i < len(args):
    if args[i] in ('-j','--build-jobs'):
        out += [args[i], '2']; i += 2
    else:
        out.append(args[i]); i += 1
compiler=os.environ.get('REVIEW_VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
os.execv(compiler,[compiler]+out)
