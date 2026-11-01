#!/usr/bin/env python3
"""Waits up to N seconds for each named rc file; prints each file's state."""
import os, sys, time
limit = time.time() + float(sys.argv[1])
files = sys.argv[2:]
while time.time() < limit and not all(os.path.exists(f) and open(f).read().strip() for f in files):
    time.sleep(10)
for f in files:
    print(f, open(f).read().strip() if os.path.exists(f) else 'pending')
