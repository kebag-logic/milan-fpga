#!/usr/bin/env python3
"""Reviewer probe: compare the PHY_TIMING the service-budget oracle records
at a base and at a head, and estimate the head's PHY publication reserve on
the findings page's own arithmetic. An ESTIMATE, not a measurement: the
--enforce-service plans that grade the bound were not run.

Usage: python3 -I phy_charge_estimate.py <base-oracle.json> <head-oracle.json>
"""
import json
import re
import sys

PAT = re.compile(r"PHY_TIMING transactions=(\d+) publications=(\d+) "
                 r"max_transaction_cycles=(\d+) max_poll_cycles=(\d+)")


def timing(path):
    out = {}
    for row in json.load(open(path)):
        m = PAT.search(row["raw_log"])
        out[(row["shape"].replace("endstation_", ""), row["media"]["plan"])] = tuple(map(int, m.groups()))
    return out


base, head = timing(sys.argv[1]), timing(sys.argv[2])
for key in head:
    b, h = base[key], head[key]
    print(f"{key[0]:16} {key[1]:10} T base={b[2]:6} head={h[2]:6} ({h[2] / b[2]:.2f}x)  "
          f"P base={b[3]:7} head={h[3]:7} ({h[3] / b[3]:.2f}x)  "
          f"C9 base={(b[3] + 9 * b[2]) / 1e5:.5f} ms  C16 head={(h[3] + 16 * h[2]) / 1e5:.5f} ms")

# docs/findings/397_SERVICE_BUDGET.md, the 8x8 row: worst duty + UART + charge
# 120.53961 ms with charge 1.95488 ms (P 0.83375, T 0.12457), trigger 125 ms.
duty_uart = 120.53961 - 1.95488
limit = 250 - 125 - duty_uart
h = head[("ax7101_8x8", "all")]
c_all = (h[3] + 16 * h[2]) / 1e5
print(f"8x8 duty+UART from the page {duty_uart:.5f} ms; charge must stay <= {limit:.5f} ms")
print(f"  head charge from the 'all' plan P/T: {c_all:.5f} ms -> reserve {limit - c_all:.5f} ms")
b = base[("ax7101_8x8", "all")]
sp, st = 0.83375e5 / b[3], 0.12457e5 / b[2]
c_scaled = (h[3] * sp + 16 * h[2] * st) / 1e5
print(f"  scaled as the page's plans exceeded the base 'all' plan (P x{sp:.3f}, T x{st:.3f}): "
      f"{c_scaled:.5f} ms -> reserve {limit - c_scaled:.5f} ms")
