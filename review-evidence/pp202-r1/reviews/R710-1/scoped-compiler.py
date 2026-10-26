#!/usr/bin/env python3
import os, sys
args = sys.argv[1:]
for i, arg in enumerate(args[:-1]):
    if arg == '-j':
        args[i+1] = '2'
os.execv('$VALIDATION_TOOLS/pinned-verilator-5.050/verilator', ['verilator', *args])
