#!/usr/bin/env python3
"""Focused review checks. Usage: focused_checks.py REPO PACKET LITEX_PYTHON."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

repo, packet = map(Path, sys.argv[1:3])
scratch = packet / 'scratch'
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1',
           PYTHONUNBUFFERED='1', PYTHONHASHSEED='0', MILAN_LITEX_PYTHON=sys.argv[3])
jobs = {
 'flip-1x1': ['python3', '-I', 'tb/verilator/ctrl_service_budget/flip_grade.py', '--check', '--point', '1x1/1if'],
 'flip-8x8': ['python3', '-I', 'tb/verilator/ctrl_service_budget/flip_grade.py', '--check', '--point', '8x8/1if'],
 'flip-plants': ['python3', '-I', 'tb/verilator/ctrl_service_budget/flip_grade.py', '--selftest'],
 'feature': ['python3', 'scripts/check_feature_status.py', '--self-test'],
 'uart': ['python3', 'scripts/baremetal_uart_smoke.py', '--self-test'],
 'entity': ['python3', 'scripts/check_entity_shape.py'],
 'regmap': [sys.argv[3], 'scripts/gen_register_reference.py', '--check'],
}
def run(item):
 name, argv = item
 with (packet / (name+'.log')).open('w') as log:
  log.write('COMMAND '+json.dumps(argv)+'\n'); log.flush()
  rc = subprocess.run(argv, cwd=repo, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
 (packet / (name+'.rc')).write_text(str(rc)+'\n')
 print(name, rc, flush=True)
 return name, rc
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results = list(pool.map(run, jobs.items()))
sys.exit(any(rc for _,rc in results))
