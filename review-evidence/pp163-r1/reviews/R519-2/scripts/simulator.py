#!/usr/bin/env python3
"""Bound each simulation build to two compiler jobs; use the verified pinned binary."""
import os, sys
# Prevent inherited make -j16 from reopening a nested compiler pool.
os.environ['MAKEFLAGS'] = '-j2'
os.environ.pop('MFLAGS', None)
args = sys.argv[1:]
for i in range(len(args)-1):
    if args[i] == '-j': args[i+1] = '2'
os.execv(os.environ.get('REVIEW_SIMULATOR', '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'), ['verilator'] + args)
