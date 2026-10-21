#!/usr/bin/env python3
"""Keep each compilation within two workers; delegate to the supplied installation."""
import os
import sys
args = sys.argv[1:]
for i in range(len(args) - 1):
    if args[i] in ('-j', '--build-jobs'):
        args[i + 1] = '2'
os.execv(os.environ.get('REVIEW_SIMULATOR', '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'),
         ['verilator'] + args)
