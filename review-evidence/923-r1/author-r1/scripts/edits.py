#!/usr/bin/env python3
"""edits.py HARNESS_DIR RESULTS...: every ADD/REMOVE_AUDIO_MAPPINGS record (and the dearest of each group) of each
results directory, by record_classes.read_leg: group, command, status, CPU cycles, cost by the rule."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import record_classes as rc
for results in sys.argv[2:]:
    leg, _ = rc.read_leg(Path(results))
    for group, records in sorted(leg.groups.items()):
        for r in records:
            if r.command in rc.EDITS:
                print(f"{leg.point} {leg.variant} {group}: {rc.EDITS[r.command]} status {r.status} "
                      f"{r.cycles:,} cycles, {rc.rule(r.cycles, leg.cpu_hz)} us by the rule")
