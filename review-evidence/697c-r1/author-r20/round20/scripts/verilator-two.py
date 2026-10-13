#!/usr/bin/env python3
import os,sys
args=sys.argv[1:]
for i,a in enumerate(args[:-1]):
 if a=="-j": args[i+1]="2"
os.execv(os.environ["PINNED_VERILATOR"],["verilator",*args])
