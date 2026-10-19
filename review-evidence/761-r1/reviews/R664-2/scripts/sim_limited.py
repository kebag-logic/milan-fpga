#!/usr/bin/env python3
import os,sys
args=sys.argv[1:]
for i,arg in enumerate(args[:-1]):
    if arg=="-j": args[i+1]="4"
binary=os.environ.get("REVIEW_SIMULATOR", "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator")
os.execv(binary, [binary]+args)
