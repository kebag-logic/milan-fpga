#!/usr/bin/env python3
"""Keep each compiler build to four workers while independent checks overlap."""
import os
import sys
args = sys.argv[1:]
for i, arg in enumerate(args[:-1]):
    if arg in ('-j', '--build-jobs', '--verilate-jobs'):
        args[i + 1] = '4'
compiler = os.environ.get('PP_REVIEW_COMPILER', '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
os.execv(compiler, ['verilator', *args])
