#!/usr/bin/env python3
"""Reviewer probe: as probe_merge_both_tu.py, with both networks at the
primary's latency (60-180 us after release). The author's run() is used
unchanged except for that one latency table line, patched in memory.
Usage: python3 -I probe_merge_both_tu_equal_latency.py /path/to/merge_model.py
"""
import sys
src = open(sys.argv[1]).read()
old = "lat = {0: (60, 180), 1: (1100, 1500)}"
assert src.count(old) == 1
src = src.replace(old, "lat = {0: (60, 180), 1: (60, 180)}").replace('if __name__ == "__main__":', 'if False:')
g = {'__name__': 'merge_model_eq'}
exec(compile(src, 'merge_model_eq', 'exec'), g)
for name, case in [
    ("both tu from packet 100, equal latency", {'tu': {0: (100, 4000, 0.0, 0.0), 1: (100, 4000, 0.0, 0.0)}}),
    ("primary tu from 100, secondary from 104 (0.5 ms later), equal latency", {'tu': {0: (100, 4000, 0.0, 0.0), 1: (104, 4000, 0.0, 0.0)}}),
    ("control: secondary only tu from 100, equal latency", {'tu': {1: (100, 4000, 0.0, 0.0)}}),
]:
    r = g['run'](case); ref = g['run'](case, {'no_rule2'})
    print(f"{'PASS' if g['judge'](r, {}) else 'FAIL'}  {name}: missing={r['missing']} samples = "
          f"{r['missing'] / g['NS']:.0f} packets = {r['missing'] * g['SP']:.1f} us; without rule 2 missing={ref['missing']}")
