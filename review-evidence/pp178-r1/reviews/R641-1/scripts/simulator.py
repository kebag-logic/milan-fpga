#!/usr/bin/env python3
import os,sys
args=sys.argv[1:]
for i,a in enumerate(args[:-1]):
 if a == '-j': args[i+1]='4'
os.execv('$VALIDATION_TOOLS/pinned-verilator-5.050/verilator', ['verilator']+args)
