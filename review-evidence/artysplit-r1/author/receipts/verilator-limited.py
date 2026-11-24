#!/usr/bin/env python3
"""Limit compiler parallelism while retaining the suite's native stimulus and checks."""
import os,sys
args=sys.argv[1:]
for i in range(len(args)-1):
 if args[i]=='-j' and args[i+1]=='0':args[i+1]='8'
os.execv('/usr/bin/verilator',['verilator',*args])
