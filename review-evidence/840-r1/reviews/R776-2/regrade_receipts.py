#!/usr/bin/env python3
"""Grade every published full service receipt with the reviewed head's grader.
usage: regrade_receipts.py <repo> <service-budget-receipts-dir>"""
import json, sys
from pathlib import Path
repo, rec = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo/'tb/verilator/fw_service_budget'))
import run
print('| receipt | plan | transactions | T cycles | P cycles | charge ms | largest bound ms | duty | service findings |')
for name in sorted((rec/'json').glob('*.json')):
    r = json.loads(name.read_text())
    raw = r['raw_log']
    res = run.grade(raw, r['media'])
    f = run.service_findings(res, raw)
    best = max((x for x in res['rows'] if 'phy_publication_bound_ms' in x), key=lambda x: x['phy_publication_bound_ms'])
    p = res['phy']
    print(f"| {name.name[:28]} | {r['media']['plan']} | {p['transactions']} | {p['max_transaction_sys_cycles']} | {p['max_poll_sys_cycles']} | {p['scheduling_charge_sys_cycles']/1e5:.5f} | {best['phy_publication_bound_ms']:.5f} | {best['duty']} | {f or 'none'} |")
