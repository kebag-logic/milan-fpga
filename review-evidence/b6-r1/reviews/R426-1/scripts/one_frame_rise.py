#!/usr/bin/env python3
"""Read-time rise of every one-frame event, per case and cause (F3).
Usage: one_frame_rise.py <evidence-root>/author/summary"""
import csv, os, statistics as S, sys
root = sys.argv[1]
print("One-frame events (listener and DUT beat) per case: count, with a measurable read-time rise, median, and every rise over 1.05 ms")
for c in ['a0', 'a1', 'a2', 'bint', 'bcrf']:
    ev = list(csv.DictReader(open(os.path.join(root, c, 'events.csv'))))
    for cause in ('listener', 'DUT beat'):
        one = [e for e in ev if e['cause'] == cause]
        r = [float(e['read_jump_ms']) for e in one if e['read_jump_ms'] not in ('', 'None')]
        big = [(e['capture_frame'], e['kind'], e['read_jump_ms']) for e in one
               if e['read_jump_ms'] not in ('', 'None') and abs(float(e['read_jump_ms'])) > 1.05]
        if one:
            print(c, cause, 'events', len(one), 'measured', len(r), 'median_ms', round(S.median(r), 3) if r else None,
                  'max_abs_ms', max(map(abs, r)) if r else None, 'over_1.05ms', big)
