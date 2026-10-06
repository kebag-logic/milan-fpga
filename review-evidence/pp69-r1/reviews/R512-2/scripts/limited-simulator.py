#!/usr/bin/env python3
"""Bound generated compilation concurrency without changing repository files."""
import os,sys
args=sys.argv[1:]
for i,a in enumerate(args[:-1]):
    if a in ('-j','--build-jobs'): args[i+1]='2'
os.execv(os.environ.get('SCOPED_SIMULATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'), ['verilator',*args])
