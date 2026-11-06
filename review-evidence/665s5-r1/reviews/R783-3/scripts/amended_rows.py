#!/usr/bin/env python3
"""Rows whose verdict would move under the amended column, read from the published run tables.

usage: amended_rows.py DIR/1x1-ans/table.md ...
"""
import re, sys
for f in sys.argv[1:]:
    rows = moved = over = srp_band = 0; first = []; t5 = []
    hook_miss = {}; hook_miss_am = {}
    for l in open(f):
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) != 13 or c[0] in ('Hook',) or c[0].startswith('-'): continue
        hook, probe, group, iface, ms, cyc, w, bound, am, within, slack, load, margin = c
        rows += 1
        never = ms == 'never'
        v = within == 'yes'
        a = (not never) and float(ms) <= float(am)
        hook_miss[hook] = hook_miss.get(hook, 0) + (not v)
        hook_miss_am[hook] = hook_miss_am.get(hook, 0) + (not a)
        if v != a:
            moved += 1; t5.append((probe.strip('`'), ms, bound, am))
        if hook == 'H-SRP' and not never and 18.0 + float(w) < float(ms) <= 20.0 + float(w): srp_band += 1
        if probe.strip('`').startswith('counters.first'): first.append((probe, ms, am, within))
    print(f, 'rows', rows, 'moved', moved, t5, 'srp in 18-20 band', srp_band, 'first', first)
    print('   misses', hook_miss); print('   amended', hook_miss_am)
