#!/usr/bin/env python3
"""Independently recompute cadence from raw notifications and measured service.

Usage: python3 audit_gaps.py RUN_LOG [RUN_LOG ...]
Checks the corrected consecutive-gap rule and packet/reset fixture tallies.
"""
import collections
import json
from pathlib import Path
import sys

results = []
for name in sys.argv[1:]:
    lines = Path(name).read_text().splitlines()
    times = collections.defaultdict(list)
    services = {}
    shape = None
    tx = []
    for line in lines:
        fields = line.split(',')
        if fields[0] == 'NOTE':
            times[tuple(map(int, fields[1:4]))].append(int(fields[4]))
        elif fields[0] == 'GAPS':
            shape = int(fields[1])
            services[tuple(map(int, fields[2:5]))] = round(float(fields[10]) * 1000)
        elif fields[0] == 'TX_COUNT':
            tx.append(list(map(int, fields[1:])))
    assert shape in (1, 8)
    assert len(times) == 4 * (shape + 1)
    gaps = []
    for key, events in times.items():
        assert len(events) >= 2
        row_gaps = [right-left for left,right in zip(events,events[1:])]
        assert min(row_gaps) >= 1000000, key
        assert max(row_gaps) <= 1000000 + services[key], key
        assert 5000000-events[-1] <= 1000000 + services[key], key
        gaps.extend(row_gaps)
    assert all(row[1] == row[2] for row in tx)
    results.append(dict(log=Path(name).name, shape=shape, rows=len(times), gaps=len(gaps),
                        min_ms=min(gaps)/1000, max_ms=max(gaps)/1000,
                        max_service_ms=max(services.values())/1000, tx_counts=tx))
print(json.dumps(results, indent=2))
