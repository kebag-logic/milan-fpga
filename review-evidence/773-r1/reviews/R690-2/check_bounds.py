#!/usr/bin/env python3
"""Independent rational check of #773 round-2 bounds and receipt claims.

Usage: python3 check_bounds.py REPO PUBLISHED_CAPTURE_EXCERPT
No source changes or builds. Exit 1 means a stated measurement is false.
"""
from collections import Counter
from fractions import Fraction as F
from math import ceil, floor
from pathlib import Path
import json
import re
import sys

repo = Path(sys.argv[1])
log = Path(sys.argv[2]).read_text()
doc = (repo / 'docs/design/MEDIA_CLOCK_FOLLOWING.md').read_text()
matrix = (repo / 'docs/reference/MILAN_COMPLIANCE_MATRIX.md').read_text()
ps = F(10**9, 48000)
lead = ceil(8 * ps)
five = ceil(5 * ps)
startup = (floor(5 * F(50_000_000, 48000)) + 26 * 3 + 57) * 20
hold = 2_000_000 + lead - startup
def rnd(x):
    return (x.numerator * 2 + x.denominator) // (2 * x.denominator)

assert startup == 106860 and hold == 2059807
assert lead < startup + 125000
assert '231.8 us' in doc  # conservative truncation of strict 231860 ns ceiling
assert f'{hold:,}' in doc and f'{hold:,}' in matrix
for n, slots, loop, audio, k in [(1, 8, 4, 24576000, 2), (8, 32, 1, 98304000, 1)]:
    marker = rnd(F(256 * 10**9, slots * 32 * 48000)) + rnd(F(10**9, audio)) + 90
    age = ceil(F(50_000_000, 48000)) + 1
    walk = 4 + loop + 26 * (4 * n - 1)
    pipe = 4 + (3 if n > 1 else 0) + 24 + 30 - 1
    late = marker - floor(ps) + (age + walk + pipe) * 20
    delay = ceil(F(late) / ps)
    tc_late = marker + 20 + 9 * 20
    tc = ceil(F(tc_late) / ps)
    earliest = 5 * ps + marker + (4 + loop + 26 * 3 + 57) * 20
    grid_hold = floor(2_000_000 + lead - earliest)
    queue = rnd((k + 128 - F(3, 2)) * ps - marker)
    low = rnd((k + F(1, 2)) * ps - marker)
    aaf_spare = ceil(delay * ps) - late
    crf_spare = ceil(tc * ps) - tc_late
    max_frame = (1522 + 8 + 12) * 8
    # Store-and-forward: frame fill, preceding wire frames, own fill overlap.
    aaf_extra = 189 * 20 + max_frame + (60 + 4 + 20) * 8 - 29 * 20
    crf_extra = 189 * 20 + max_frame + (234 + 4 + 20) * 8 - 7 * 20
    row = dict(shape=f'{n}x{n}', marker=marker, age=age, walk=walk, pipe=pipe,
               after_estimate=late, delay_periods=delay, lead=lead, tc_periods=tc,
               tc_ns=ceil(tc * ps), grid_hold=grid_hold, startup_hold=hold,
               grid_last=grid_hold + five, startup_last=hold + five,
               queue=queue, grid_margin=queue-grid_hold-five,
               startup_margin=queue-hold-five, transit_bound=2_000_000+lead-low,
               first_offset_bound=queue-lead, whole_offset_bound=queue-lead-five,
               max_frame=max_frame, aaf_spare=aaf_spare, crf_spare=crf_spare,
               aaf_one_frame=aaf_spare-max_frame, crf_one_frame=crf_spare-max_frame,
               aaf_extra=aaf_extra, crf_extra=crf_extra,
               aaf_store_forward=aaf_spare-aaf_extra, crf_store_forward=crf_spare-crf_extra)
    print(json.dumps(row, sort_keys=True))
    assert delay == 2 and tc == (2 if n == 1 else 1)
    assert hold + five < queue and hold < 2126000
    for key in ['grid_hold', 'startup_hold', 'grid_last', 'startup_last', 'queue',
                'transit_bound', 'first_offset_bound', 'whole_offset_bound',
                'max_frame', 'aaf_one_frame', 'crf_one_frame', 'aaf_extra',
                'crf_extra', 'aaf_store_forward', 'crf_store_forward']:
        assert f'{abs(row[key]):,}' in doc, (key, row[key])
    assert f'{grid_hold:,}' in matrix
    assert f'{row["startup_margin"]/1000:.1f} us' in doc

rows = re.findall(r'\[([^\]]+)\] \[WIRE\] offset (\d+) ns:.*?\[HOLD\].*?max (\d+) ns', log)
assert len(rows) == 31
counts = Counter(int(v) for _, offset, v in rows if offset == '2000000')
assert sum(counts.values()) == 23
assert max(counts) <= hold
assert all(int(v) <= int(offset) + lead - startup for _, offset, v in rows)
print('PASS: both bound derivations, queue margins, supported ranges, MAC figures, and all 31 observed maxima')
print('2 ms HOLD maximum distribution:', dict(sorted(counts.items())))
print('Strict Equation (1) lead ceiling:', startup + 125000, 'ns; documented conservative ceiling 231800 ns')
claim = 'measures that `[HOLD]` maximum in every 2 ms run.'
if claim in doc and any(v != hold for v in counts):
    print('FAIL: doc claims every 2 ms run attains 2059807; only', counts[hold], 'of', sum(counts.values()), 'do')
    sys.exit(1)
