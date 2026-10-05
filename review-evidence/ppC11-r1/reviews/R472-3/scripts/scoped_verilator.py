#!/usr/bin/env python3
"""Bound each of four concurrent small suite builds to two build workers."""
import os
import sys
exe=os.environ.get('REVIEW_VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
args=sys.argv[1:]
for i,arg in enumerate(args[:-1]):
 if arg=='-j': args[i+1]='2'
os.execv(exe,[exe,*args])
