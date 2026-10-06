#!/usr/bin/env python3
import os,sys
args=sys.argv[1:]
for i,arg in enumerate(args[:-1]):
    if arg in ("-j", "--build-jobs"):
        args[i+1]="2"
os.execv(os.environ["REVIEW_HDL_COMPILER"], [os.environ["REVIEW_HDL_COMPILER"], *args])
