#!/usr/bin/env python3
"""Summarise listener lockstep results dirs: one line per configuration."""
import re, sys
for d in sys.argv[1:]:
    rows = [dict(re.findall(r"(\w+)=(-?\d+)", l)) for l in open(f"{d}/results.txt") if l.startswith("LSN")]
    rcs = [l for l in open(f"{d}/results.txt") if l.startswith("rc=")]
    tot = lambda k: sum(int(r[k]) for r in rows)
    caught = sum(1 for r in rows if int(r["mismatch"]))
    sinks = sorted({int(r["nsinks"]) for r in rows})
    print(f"{d.rstrip('/').split('/')[-1]:26s} runs={len(rows)}/{len(rcs)} sinks={sinks} cycles={tot('cycles'):,} "
          f"mismatch={tot('mismatch'):,} runs_caught={caught}/{len(rows)} txns={tot('txns'):,} "
          f"x_latch={tot('x_latch'):,} x_strt_ap={tot('x_strt_ap'):,} rec_writes={tot('rec_writes'):,} "
          f"probe_rsps={tot('probe_rsps'):,} settles={tot('settles'):,} expiries={tot('expiries'):,} "
          f"reset_clocks={tot('reset_clocks'):,}")
