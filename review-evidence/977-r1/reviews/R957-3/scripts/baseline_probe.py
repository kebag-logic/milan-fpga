#!/usr/bin/env python3
"""Usage: python3 -I baseline_probe.py <postswap-8x8-1if.txt (round 10d)> <deliveries-8x8-1if.txt (round 11)>.
Recomputes the 8x8/1if deliveries term for the answering-ports swap under each published baseline: round 10d's median of
the 500 ms before the record and round 11's median of the 50 ms before it. Rule: 5 us steps of (cycles/100) x 1.05 rounded
up; term = cost x 3 records x V (9) / (1.5 x 180 ms); the load without the term is the gate's 0.76614 (load_probe.py)."""
import math, re, sys
V, SINKS, BASE_LOAD = 9, 9, 0.76614
rule = lambda c: 5 * math.ceil(c / 100 * 1.05 / 5)
term = lambda us: us * 3 * V / (1.5 * 180) / 1000
old = open(sys.argv[1]).read()
m = re.search(r'answering-ports srp-register-swap: .*?median base before it \(([\d,]+)\): (\d+) passes, ([\d, ]+) cycles', old)
base10, n10, xs = int(m[1].replace(',', '')), int(m[2]), [int(x) for x in m[3].replace(',', '').split()]
ex10 = sum(xs)
new = open(sys.argv[2]).read()
m2 = re.search(r'answering-ports/s-srp-register-swap .*?median base before ([\d,]+) .*?excess ([\d,]+) cycles', new)
base11, ex11 = int(m2[1].replace(',', '')), int(m2[2].replace(',', ''))
print(f'round 10d (500 ms median {base10:,}): {n10} passes over it, excess {ex10:,} cycles; '
      f'{ex10 / SINKS:,.0f} a sink, {rule(ex10 / SINKS)} us by the rule; term {term(rule(ex10 / SINKS)):.5f}; '
      f'load {BASE_LOAD + term(rule(ex10 / SINKS)):.5f}; unruled term {ex10 / 100 * 3 / 270 / 1000:.5f}, '
      f'load {BASE_LOAD + ex10 / 100 * 3 / 270 / 1000:.5f}')
print(f'round 11 (50 ms median {base11:,}): excess {ex11:,} cycles; {ex11 / SINKS:,.0f} a sink, '
      f'{rule(ex11 / SINKS)} us by the rule; term {term(rule(ex11 / SINKS)):.5f}; load {BASE_LOAD + term(rule(ex11 / SINKS)):.5f}')
print(f'difference {ex10 - ex11:,} cycles = {n10} passes x {(ex10 - ex11) / n10:,.1f}; baseline step {base11 - base10:,}')
