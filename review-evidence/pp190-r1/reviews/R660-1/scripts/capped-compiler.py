#!/usr/bin/env python3
import os, sys
args = sys.argv[1:]
for i in range(len(args)-1):
    if args[i] == "-j": args[i+1] = "4"
os.execv(os.environ["REVIEW_COMPILER"], [os.environ["REVIEW_COMPILER"], *args])
