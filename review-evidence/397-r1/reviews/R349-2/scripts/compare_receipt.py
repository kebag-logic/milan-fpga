#!/usr/bin/env python3
"""Compare a reviewer rerun receipt with the committed receipt.

Usage: compare_receipt.py <rerun.json> <committed.json>
Reports raw-log digest equality, event-list equality and row equality.
"""
import json, sys
a, b = (json.load(open(p)) for p in sys.argv[1:3])
print('log_sha256 rerun    ', a['log_sha256'])
print('log_sha256 committed', b['log_sha256'])
print('raw log identical   ', a['log_sha256'] == b['log_sha256'])
print('events identical    ', a['events'] == b['events'])
print('rows identical      ', a['rows'] == b['rows'])
print('findings            ', a['budget_findings'])
print('input_hashes equal  ', a['input_hashes'] == b['input_hashes'])
diff = sorted(k for k in a['build_hashes'] if a['build_hashes'][k] != b['build_hashes'].get(k))
print('build_hashes differing:', diff)
for r in a['rows']:
    if r['duty'] in ('boot_to_entity_enabled', 'milan_nvm', 'maximum_heartbeat_gap'):
        print(f"   {r['duty']:28} cpu={r['cpu_cycles']} ms={r['ms']} margin={r['margin_ms']}")
