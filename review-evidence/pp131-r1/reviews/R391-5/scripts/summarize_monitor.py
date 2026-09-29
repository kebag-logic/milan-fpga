#!/usr/bin/env python3
"""R391-5: tally the R391MON lines (r391_5_mutants.py mon_unreachable_inputs)
in each named run log. Usage: summarize_monitor.py LABEL=LOG [LABEL=LOG ...]"""
import collections, re, sys
print("R391-5 arbiter input monitor (prints the first 20 clocks of each kind per simulation)")
for arg in sys.argv[1:]:
    label, path = arg.split("=", 1)
    t = open(path).read()
    c = collections.Counter(re.findall(r"R391MON (\w+)", t))
    print(f"== {label}: {dict(c) if c else 'no monitored input occurred'}")
    for line in t.splitlines():
        if re.search(r"checks|rc=|AGG 2800", line):
            print("   ", line.strip()[:220])
