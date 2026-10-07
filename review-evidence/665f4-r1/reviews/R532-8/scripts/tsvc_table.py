#!/usr/bin/env python3
"""Recompute MAILBOX_SPLIT.md's four-module T_svc rows from the header values
(receipts/pass-bounds.txt): bound = (pass + 1) * PASS_MAX; access time = 10 ms
over the bound, rounded down to 0.01 us as the page states."""
import math
PASS = {1: 3128, 2: 3977}
ROWS = (("an event behind 15 others", 2, (9384, 11931), (1.06, 0.83)),
        ("an ACMP command behind a full acmp ring", 10, (34408, 43747), (0.29, 0.22)),
        ("an ENTITY_AVAILABLE behind a full adp ring", 21, (68816, 87494), (0.14, 0.11)),
        ("a response with 7 frames owed ahead of it", 8, (28152, 35793), (0.35, 0.27)))
bad = 0
for name, taken, bounds, times in ROWS:
    for k, n in enumerate((1, 2)):
        bound = (taken + 1) * PASS[n]
        t = math.floor(10000 / bound * 100) / 100
        ok = bound == bounds[k] and abs(t - times[k]) < 1e-9
        bad += not ok
        print(f"{'ok ' if ok else 'BAD'} IF={n} {name}: {bound} accesses ({bounds[k]} published), "
              f"{t:.2f} us ({times[k]:.2f} published), {bound/1000:.3f} ms at 1 us, "
              f"fits 10 ms: {bound <= 10000}, fits 20 ms: {bound <= 20000}")
print("open items: ACMP 0.29/0.22, ADP 0.14/0.11 match rows 2 and 3")
raise SystemExit(1 if bad else 0)
