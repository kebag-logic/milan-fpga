#!/usr/bin/env python3
"""Compare published scenario model counts with the real adapter/model measurement.

Exit 1 demonstrates the stale numeric evidence at the reviewed head.
The in-memory corrected-value control must pass; no source is edited.
"""
import json
from pathlib import Path
import re
import sys
repo, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
sys.path.insert(0, str(repo / 'tb/verilator/ctrl_service_budget'))
import scenario
log = (packet / 'receipts/focused/adp-baseline.log').read_text()
match = re.search(r'C0 LINK_UP -> TMR_DELAY armed\s+(\d+) accesses \(bound (\d+)\)', log)
assert match, 'missing executed C0 measurement'
measured, bound = map(int, match.groups())
assert measured == bound == 12
records = []
for n in (1, 8):
    point = scenario.Point(f'{n}x{n}-1if', f'endstation_ax7101_{n}x{n}', 1,
                           0x024b4cfffe4b4c01, 0x024b4c4b4c01, n, n)
    group = scenario.Group('advertised')
    scenario.advertised(group, point)
    for g in [group, *scenario.fixture_groups(point)]:
        for probe in g.probes:
            if 'link_up' in probe.name:
                records.append({'point': point.label, 'group': g.name, 'probe': probe.name,
                                'scenario_model_accesses': probe.accesses,
                                'executed_adapter_model_accesses': measured,
                                'matches': probe.accesses == measured})
result = {'head': 'f4833e16a07d07494277aba8dc7a5de19320c20b', 'records': records,
          'corrected_value_control': all(measured == bound for _ in records),
          'cpu_time_budget_verdict_affected': False,
          'propagation': 'grade.py:639 -> model_accesses -> run.py:568-571 Mailbox accesses (model)'}
text = json.dumps(result, indent=2) + '\n'
(packet / 'receipts/model-accesses.json').write_text(text)
print(text)
sys.exit(0 if all(r['matches'] for r in records) else 1)
