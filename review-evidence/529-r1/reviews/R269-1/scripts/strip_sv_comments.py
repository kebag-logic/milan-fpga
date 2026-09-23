#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Print a SystemVerilog file with // and /* */ comments and blank runs removed,
so two revisions can be compared for non-comment changes."""
import re, sys
t = sys.stdin.read()
t = re.sub(r"/\*.*?\*/", " ", t, flags=re.S)
t = re.sub(r"//[^\n]*", "", t)
for line in t.splitlines():
    s = " ".join(line.split())
    if s:
        print(s)
