"""Focused review checks; all subprocesses are joined before exit."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

source, packet, public = map(Path, sys.argv[1:4])
scratch = packet / 'scratch'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch), PYTHONHASHSEED='0')
service = 'tb/verilator/ctrl_service_budget/'
jobs = {
    'receipt-regrade': ['python3', service+'receipt_regrade.py', str(public / 'author-r7/receipts')],
    'rows-controls': ['python3', service+'rows_tiers.py', '--selftest'],
    'kept-controls': ['python3', service+'kept_grade.py', '--selftest'],
    'owner-model': ['python3', service+'arty_grade.py'],
    'owner-controls': ['python3', service+'arty_grade.py', '--selftest'],
    'docs-inventory': ['python3', 'scripts/docs_inventory.py', '--check'],
    'python-idiom': ['python3', 'scripts/check_py_idiom.py'],
    'ledger-controls': ['python3', service+'egress_ledger.py', '--selftest'],
    'record-controls': ['python3', service+'record_classes.py', '--selftest'],
}

def run(item):
    name, cmd = item
    with (packet / (name+'.log')).open('w') as f:
        try:
            rc = subprocess.run(cmd, cwd=source, env=env, stdout=f, stderr=subprocess.STDOUT, timeout=540).returncode
        except subprocess.TimeoutExpired:
            rc = 124
            f.write('\nREVIEW TIMEOUT\n')
    (packet / (name+'.rc')).write_text(str(rc)+'\n')
    print(name, rc, flush=True)
    return dict(name=name, command=cmd, rc=rc)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(run, jobs.items()))
(packet / 'checks.json').write_text(json.dumps(rows, indent=2)+'\n')
