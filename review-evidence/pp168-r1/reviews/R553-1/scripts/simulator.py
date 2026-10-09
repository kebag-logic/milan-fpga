#!/usr/bin/env python3
"""Bound compilation parallelism; use an explicitly selected 5.050 installation."""
import os,sys
args=sys.argv[1:]
for i,a in enumerate(args[:-1]):
    if a in ('-j','--build-jobs'): args[i+1]=os.environ.get('REVIEW_BUILD_JOBS','2')
os.execv(os.environ['REVIEW_VERILATOR'],[os.environ['REVIEW_VERILATOR']]+args)
