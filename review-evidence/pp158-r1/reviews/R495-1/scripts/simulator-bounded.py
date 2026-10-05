#!/usr/bin/env python3
import os,sys
a=sys.argv[1:]
for i in range(len(a)-1):
 if a[i] == "-j": a[i+1]="2"
os.execv(os.environ["REVIEW_SIMULATOR"],[os.environ["REVIEW_SIMULATOR"]]+a)
