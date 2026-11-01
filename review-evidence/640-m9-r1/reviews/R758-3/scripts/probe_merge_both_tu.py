#!/usr/bin/env python3
"""Reviewer probe: the published merge model with tu set on BOTH networks.

Loads the author's merge_model.py from the path given as the first argument
and runs its own run()/judge() on cases its CASES list does not contain:
both copies carry tu from packet 100, with tu onsets equal or offset, with
small skews well inside one packet interval. Each case is also run with
rule 2 removed ('no_rule2') as the reference: without rule 2 nothing is lost.
Usage: python3 -I probe_merge_both_tu.py /path/to/merge_model.py
"""
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("merge_model", sys.argv[1])
mm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mm)

CASES = [
    ("both tu from packet 100, no skew", {'tu': {0: (100, 4000, 0.0, 0.0), 1: (100, 4000, 0.0, 0.0)}}),
    ("both tu from packet 100, skew +-5 us", {'tu': {0: (100, 4000, 5.0, 1.0), 1: (100, 4000, -5.0, 1.0)}}),
    ("primary tu from 100, secondary tu from 108 (1 ms later)", {'tu': {0: (100, 4000, 0.0, 0.0), 1: (108, 4000, 0.0, 0.0)}}),
    ("primary tu from 100, secondary tu from 140 (5 ms later)", {'tu': {0: (100, 4000, 0.0, 0.0), 1: (140, 4000, 0.0, 0.0)}}),
    ("both tu 100..600 then clean again, no skew", {'tu': {0: (100, 600, 0.0, 0.0), 1: (100, 600, 0.0, 0.0)}}),
]

bad = 0
for name, case in CASES:
    r = mm.run(case)
    ref = mm.run(case, {'no_rule2'})
    ok = mm.judge(r, {})
    bad += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    print(f"      rules as written : missing={r['missing']} samples ({r['missing'] / mm.NS:.0f} packets, "
          f"{r['missing'] * mm.SP:.1f} us), bad={r['bad']}, tu_drop={r['tu_drop']}")
    print(f"      without rule 2   : missing={ref['missing']}, bad={ref['bad']}, tu_drop={ref['tu_drop']}")
print(f"{bad} of {len(CASES)} cases lose samples under the rules as written")
