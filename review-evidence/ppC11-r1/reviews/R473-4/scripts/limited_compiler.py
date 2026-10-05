#!/usr/bin/env python3
"""Use the verified scoped compiler with at most four compilation workers."""
import os
import sys
args = sys.argv[1:]
for i, arg in enumerate(args):
    if arg in ['-j', '--build-jobs'] and i + 1 < len(args):
        args[i + 1] = '4'
    elif arg.startswith('-j') and arg[2:].isdigit():
        args[i] = '-j4'
exe = os.environ.get('REVIEW_COMPILER', '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
os.execv(exe, [exe, *args])
