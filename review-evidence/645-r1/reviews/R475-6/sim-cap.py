#!/usr/bin/env python3
"""Forward to the selected simulator with four compiler workers per build."""
import os, sys
args=sys.argv[1:]
for i,x in enumerate(args[:-1]):
    if x == "-j": args[i+1]="4"
os.execv(os.environ["REVIEW_SIM"], [os.environ["REVIEW_SIM"], *args])
