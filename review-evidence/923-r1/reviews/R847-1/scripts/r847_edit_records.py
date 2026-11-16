#!/usr/bin/env python3
"""Reviewer probe (R847-1, PR #931): list a CPU budget harness leg's map-edit and SET_CONFIGURATION AECP records
with record_classes.read_leg (the harness's own reader) and record_classes.rule (cost by the rule).

Usage: python3 -B r847_edit_records.py <checkout> <results-dir>
"""
import sys
from pathlib import Path

checkout, results = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(checkout / 'tb/verilator/ctrl_service_budget'))
import record_classes  # noqa: E402

NAMES = {0x002C: 'ADD_AUDIO_MAPPINGS', 0x002D: 'REMOVE_AUDIO_MAPPINGS', 0x0006: 'SET_CONFIGURATION'}
leg, spec = record_classes.read_leg(results)
print(f'point {leg.point} variant {leg.variant} cpu_hz {leg.cpu_hz}')
for group, records in sorted(leg.groups.items()):
    for r in records:
        if r.command in NAMES:
            print(f'{group}: {NAMES[r.command]} status {r.status} {r.cycles:,} cycles, '
                  f'{record_classes.rule(r.cycles, leg.cpu_hz)} us by the rule')
    dearest = max((r for r in records if r.command in (0x002C, 0x002D)), key=lambda r: r.cycles, default=None)
    if dearest is not None:
        print(f'{group}: dearest map edit {dearest.cycles:,} cycles, '
              f'{record_classes.rule(dearest.cycles, leg.cpu_hz)} us by the rule')
