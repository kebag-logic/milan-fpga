#!/usr/bin/python3
import os,sys
args=sys.argv[1:]
for i in range(len(args)-1):
    if args[i] in ("-j", "--build-jobs") and args[i+1] == "0": args[i+1]="8"
os.execv("$VALIDATION_TOOLS/verilator-v5.050/bin/verilator",["verilator",*args])
