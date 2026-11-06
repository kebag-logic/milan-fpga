#!/usr/bin/env python3
"""Bind the tracked service oracle at the reviewed head to the published receipts.
usage: oracle_bind.py <repo> <service-budget-receipts-dir> <base-commit>"""
import hashlib, json, subprocess, sys
from pathlib import Path
repo, rec, base = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
head = json.loads((repo/'tb/verilator/fw_service_budget/oracle.json').read_text())
basej = json.loads(subprocess.check_output(['git','-C',str(repo),'show',base+':tb/verilator/fw_service_budget/oracle.json']))
names = ['fw-1x1-all+uart-paced--service-all-1-0-0.json','fw-8x8-all--service-all-1-0-0.json','fw-1x1-all+uart-paced--service-uart-paced-1-0-0.json']
for row, name, b in zip(head, names, basej):
    r = json.loads((rec/'json'/name).read_text())
    same = {k: row[k] == r[k] for k in ('raw_log','log_sha256','rows','budget_findings','heartbeat','liveness')}
    calc = hashlib.sha256(row['raw_log'].encode()).hexdigest() == row['log_sha256']
    print(row['shape'], row['media']['plan'], 'receipt-equal', all(same.values()), 'log-digest', calc, 'findings', row['budget_findings'], 'base-findings', b['budget_findings'])
    for rr in row['rows']:
        if rr['duty'] == 'milan_nvm' :
            br=[x for x in b['rows'] if x['duty']==rr['duty']]
            print('  milan_nvm sys_cycles', rr['sys_cycles'], 'budget_ms', rr.get('budget_ms'), 'base', [x['sys_cycles'] for x in br][:3])
# build hash comparison with the file tree at head
for name in sorted((rec/'json').glob('*.json')):
    r = json.loads(name.read_text())
    bad = []; n = 0
    def walk(d):
        for k, v in d.items():
            if isinstance(v, dict): yield from walk(v)
            else: yield k, v
    for k, v in walk(r.get('build_hashes', {})):
        p = repo/k
        if p.is_file():
            n += 1
            if hashlib.sha256(p.read_bytes()).hexdigest() != v: bad.append(k)
    print(name.name, 'build_hash source files checked', n, 'differ at head', bad)
