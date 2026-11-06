#!/usr/bin/env python3
"""Probe the target harness's clock provenance through the checkout's own run.py and self-test helpers:
(a) the self-test's synthetic commit rendered at CPU 62.5 MHz / bus 125 MHz; (b) round 2's published
results, which carry no clocks, refused; (c) this round's 8x8 record relabelled to a 100 MHz CPU, refused;
(d) the same record as written, rendered. Prints each outcome; exit 0 when all four are as expected.

Usage: python3 -I clock_probe.py CHECKOUT ROUND2_RESULTS_JSON ROUND3_RESULTS_JSON
"""
import json
import sys
from pathlib import Path

checkout, round2, round3 = (Path(a) for a in sys.argv[1:4])
here = checkout / 'tb/verilator/nvm_split_target'
sys.path.insert(0, str(here))
import target_selftest as selftest  # noqa: E402
run = selftest.RUN
ok = True

print('== (a) the synthetic commit at CPU 62.5 MHz, bus 125 MHz')
text = run.table(selftest.graded_record(62_500_000, 125_000_000))
print(text)
ok &= 'CPU 62.5 MHz (62,500,000 Hz), bus 125 MHz (125,000,000 Hz)' in text and '50 MHz' not in text

print('== (b) round 2 results.json (a bare list, no clocks), as a record without clocks')
results = json.loads(round2.read_text())
words = selftest.refusal(dict(point='8x8', shape=run.POINTS['8x8'][0], results=results))
print(words)
ok &= 'no cpu_hz recorded' in words and 'no sys_hz recorded' in words

print('== (c) round 3 8x8 results.json with cpu_hz relabelled to 100,000,000')
rec = json.loads(round3.read_text())
words = selftest.refusal(dict(rec, cpu_hz=100_000_000))
print(words[:1200])
ok &= 'CPU cycles at 100,000,000 Hz' in words

print('== (d) round 3 8x8 results.json as written')
text = run.table(rec)
print(text.splitlines()[2])
ok &= text.splitlines()[2] == ("Clocks, as this run's builds recorded them: CPU 50 MHz (50,000,000 Hz), "
                               "bus 100 MHz (100,000,000 Hz).")
print('PROBES PASS' if ok else 'PROBES FAIL')
raise SystemExit(0 if ok else 1)
