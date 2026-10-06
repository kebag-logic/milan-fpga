#!/usr/bin/env python3
"""Bound nested make parallelism to two jobs; use VERIFIED_SIMULATOR."""
import os,sys
args=sys.argv[1:]
for i,a in enumerate(args[:-1]):
 if a=='-j': args[i+1]='2'
exe=os.environ['VERIFIED_SIMULATOR']
os.execv(exe,[exe,*args])
