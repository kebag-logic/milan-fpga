#!/usr/bin/env python3
"""Focused review checks. Usage: focused.py SOURCE PACKET [INTEGRATION_PYTHON]."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
integration_python = sys.argv[3] if len(sys.argv) > 3 else sys.executable
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
budget = 'tb/verilator/ctrl_service_budget/'
host = '''import sys
from pathlib import Path
root, out = map(Path, sys.argv[1:3])
sys.path.insert(0, str(root/'sw/firmware/ctrl/test'))
import ctrl_build as c, plat_arms
tree = c.Tree(c.CTRL, out/'build', out/'reuse', c.fw_gtest.Build(jobs=4))
results = [plat_arms.arm_plat(tree), plat_arms.arm_platboot(tree, 1, mii=True)]
for result in results:
 print(result.arm, result.rc, result.log, flush=True)
raise SystemExit(max(r.rc for r in results))
'''
pll = '''import sys
sys.path.insert(0, 'sw/builder')
import test_timing_grade
test_timing_grade.test_pll_grade(sys.argv[1])
print('PASS exact PLL and rejection controls')
'''
jobs = [
 ('owner-model', [sys.executable, '-B', budget+'arty_grade.py']),
 ('owner-controls', [sys.executable, '-B', budget+'arty_grade.py', '--selftest']),
 ('service-controls', [sys.executable, '-B', budget+'selftest.py']),
 ('egress-controls', [sys.executable, '-B', budget+'egress_ledger.py', '--selftest']),
 ('record-controls', [sys.executable, '-B', budget+'record_classes.py', '--selftest']),
 ('host-focused', [sys.executable, '-B', '-c', host, str(root), str(scratch/'host')]),
 ('pll-controls', [sys.executable, '-B', '-c', pll, integration_python]),
]
def execute(item):
 name, cmd = item
 start = time.monotonic()
 with (packet/(name+'.log')).open('w') as log:
  try:
   result = subprocess.run(cmd, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=480)
   rc = result.returncode
  except subprocess.TimeoutExpired:
   rc = 124
   log.write('\nTIMEOUT\n')
 (packet/(name+'.rc')).write_text(str(rc)+'\n')
 row = {'name':name, 'command':cmd, 'rc':rc, 'elapsed_s':round(time.monotonic()-start, 3)}
 print(name, 'rc', rc, flush=True)
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results = list(pool.map(execute, jobs))
(packet/'focused-results.json').write_text(json.dumps(results, indent=2)+'\n')
raise SystemExit(any(r['rc'] for r in results))
