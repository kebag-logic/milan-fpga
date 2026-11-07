#!/usr/bin/env python3
"""oracle_vs_receipts.py <oracle.json> <service-budget receipts dir>
Each oracle entry must equal its published trace receipt (gen_oracle.convert's
fields) and its raw log must hash to log_sha256."""
import hashlib, json, sys, os
o = json.load(open(sys.argv[1])); d = sys.argv[2]
files = ['fw-1x1-service-all-1-0-0.json', 'fw-8x8-service-all-1-0-0.json',
         'fw-1x1-service-uart-paced-1-0-0.json']
rc = 0
for entry, f in zip(o, files):
    r = json.load(open(os.path.join(d, f)))
    for k in ('shape', 'raw_log', 'log_sha256', 'rows', 'budget_findings', 'heartbeat', 'liveness'):
        if entry[k] != r[k]:
            print('MISMATCH', f, k); rc = 1
    for k in ('populated', 'plan', 'slots_sha256'):
        if entry['media'][k] != r['media'][k]:
            print('MISMATCH', f, 'media', k); rc = 1
    if hashlib.sha256(entry['raw_log'].encode()).hexdigest() != entry['log_sha256']:
        print('BAD DIGEST', f); rc = 1
    print(f, entry['shape'], 'slots', entry['media']['slots_sha256'][:8], 'findings', entry['budget_findings'])
print('RESULT', 'PASS' if rc == 0 else 'FAIL'); sys.exit(rc)
