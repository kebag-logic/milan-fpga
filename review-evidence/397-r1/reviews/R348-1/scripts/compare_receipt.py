#!/usr/bin/env python3
"""Compare a reviewer re-run with the committed receipt.
usage: compare_receipt.py <repo> <SHAPE 1X1|8X8> <run.log> [run.json]"""
import hashlib, json, sys
from pathlib import Path
repo, shape, log = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
rec = json.loads((repo / f'docs/findings/397_SERVICE_BUDGET_{shape}.json').read_text())
raw = log.read_bytes().decode()
print('committed log sha256 ', rec['log_sha256'])
print('reviewer  log sha256 ', hashlib.sha256(raw.encode()).hexdigest())
print('raw log identical    ', raw == rec['raw_log'])
sys.path.insert(0, str(repo / 'tb/verilator/fw_service_budget'))
import run
got = run.grade(raw, rec['media'])
print('rows identical       ', got['rows'] == rec['rows'])
print('findings             ', got['budget_findings'])
if len(sys.argv) > 4:
    mine = json.loads(Path(sys.argv[4]).read_text())
    print('run.json rows == committed rows', mine['rows'] == rec['rows'], '| input_hashes equal', mine['input_hashes'] == rec['input_hashes'])
