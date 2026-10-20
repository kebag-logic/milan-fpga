#!/usr/bin/env python3
"""Bound each compilation to four workers; preserve all other arguments."""
import os, sys
a=sys.argv[1:]
for i in range(len(a)-1):
    if a[i] == '-j': a[i+1]='4'
v=os.environ.get('PINNED_FRONTEND','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
os.execv(v,[v]+a)
