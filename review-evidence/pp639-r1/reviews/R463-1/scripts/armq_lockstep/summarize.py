#!/usr/bin/env python3
"""Summarise arm-port lockstep results dirs: one line per configuration."""
import re, sys
for d in sys.argv[1:]:
    rows = [dict(re.findall(r"(\w+)=(-?\d+)", l)) for l in open(f"{d}/results.txt") if l.startswith("ARMQ")]
    tot = lambda k: sum(int(r[k]) for r in rows)
    caught = sum(1 for r in rows if int(r["lockstep_mismatch"]) or int(r["negedge_mismatch"]))
    print(f"{d.rstrip('/').split('/')[-1]:20s} runs={len(rows)} cycles={tot('cycles'):,} "
          f"lockstep_mismatch={tot('lockstep_mismatch'):,} model_mismatch={tot('model_mismatch'):,} "
          f"runs_caught={caught}/{len(rows)} arms={tot('arms'):,} offers_to_full={tot('offers_to_full'):,} "
          f"full_pop_push={tot('full_pop_push'):,} drop_rises={tot('drop_rises'):,} "
          f"sat_clocks={tot('sat_clocks'):,} reset_clocks={tot('reset_clocks'):,}")
