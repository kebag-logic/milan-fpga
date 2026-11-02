#!/usr/bin/env python3
"""Recompute SPLIT_CONTROL_MEMORY.md section 14's S, L and U columns and the gPTP additions from the
document's own tables at the head under review.

Usage: check_estimate.py <docs/design/SPLIT_CONTROL_MEMORY.md>
S is computed two ways: from the 1x1/1if column section 14 prints (worst of the arms), and from arm A's
1x1/1if figure (section 13's backlog table, first of each 'A / B' pair), the arm the 8x8/1if point ran in.
"""
import re
import sys

text = open(sys.argv[1], encoding='utf-8').read()
s13 = text[text.index('**The rows at this head.**'):text.index('The per-pass share, 2.0 ms: the passes over it')]
s14 = text[text.index('### The estimate'):text.index('The rows that would not fit')]


def cells(line):
    return [c.strip().replace('*', '') for c in line.strip().strip('|').split('|')]


arm_a_1x1 = {}
for line in s13.splitlines():
    c = cells(line) if line.startswith('| ') else []
    if len(c) == 6 and re.match(r'[\d.]+ /', c[2]):
        arm_a_1x1[c[0]] = float(c[2].split('/')[0])
k = 48 / 14  # from 16 streams to 64, per stream step between 2 and 16
print(f'{"row":44} {"U":>6} {"U doc":>6} {"L":>6} {"L doc":>6} {"S(col)":>7} {"S(armA)":>8} {"S doc":>6}')
for line in s14.splitlines():
    c = cells(line) if line.startswith('| ') else []
    if len(c) != 8 or not re.fullmatch(r'[\d.]+', c[2]):
        continue
    name, a, b1, b = c[0], float(c[2]), float(c[3]), float(c[4])
    doc = [float(re.match(r'[\d.]+', x).group()) for x in c[5:]]
    u, l = 4 * b, b + (b - a) * k
    s_col = b + (b1 - a) * k
    s_a = b + (b1 - arm_a_1x1.get(name, float('nan'))) * k
    flag = '' if abs(s_col - doc[2]) < 0.051 else '  <- S differs from the printed 1x1 column'
    print(f'{name:44} {u:6.2f} {doc[0]:6.1f} {l:6.2f} {doc[1]:6.1f} {s_col:7.2f} {s_a:8.2f} {doc[2]:6.1f}{flag}')

# gPTP additions (section 14, "gPTP's share, an assumption")
units_s, cyc, lo, hi, hz = 62, 40000, 20000, 100000, 100e6
row_units = units_s * 0.018
print(f'\nrow mean: {row_units:.3f} units = {row_units * cyc / hz * 1e3:.3f} ms '
      f'({row_units * lo / hz * 1e3:.3f} to {row_units * hi / hz * 1e3:.3f})')
srp_last = 17.29
for label, add in (('mean', row_units * cyc / hz * 1e3), ('mean, top of range', row_units * hi / hz * 1e3),
                   ('bound 20 units', 20 * cyc / hz * 1e3)):
    print(f'  {label}: {srp_last} + {add:.3f} = {srp_last + add:.3f} ms against 18 -> {18 - srp_last - add:+.3f}')
print(f'pass bound 4 units: {4 * cyc / hz * 1e3:.2f} ms; 1.98 + that = {1.98 + 4 * cyc / hz * 1e3:.2f} ms')
