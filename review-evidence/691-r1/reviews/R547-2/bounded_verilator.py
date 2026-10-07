#!/usr/bin/env python3
"""Bound compilation even when the suite passes -j 0. REAL_VERILATOR required."""
import os,sys
args=sys.argv[1:]
for index,arg in enumerate(args[:-1]):
    if arg in ("-j","--build-jobs"):
        args[index+1] = str(min(16,int(args[index+1]))) if int(args[index+1]) else "16"
os.execv(os.environ["REAL_VERILATOR"], [os.environ["REAL_VERILATOR"], *args])
