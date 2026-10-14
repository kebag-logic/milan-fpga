#!/usr/bin/env python3
"""Run focused review checks in foreground, retaining logs and exit statuses."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(sys.argv[1]).resolve()
OUT = Path(__file__).resolve().parent
SCRATCH = OUT / 'scratch'
os.environ.update(TMPDIR=str(SCRATCH), PYTHONDONTWRITEBYTECODE='1',
                  GIT_AUTHOR_NAME='review fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                  GIT_COMMITTER_NAME='review fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
commands = {
 'inventory': ['python3', 'scripts/ci_tool_inventory.py', '--check'],
 'inventory-controls': ['python3', 'scripts/ci_tool_inventory_selftest.py'],
 'build-controls': ['python3', 'ci/image/build_selftest.py'],
 'integrity-controls': ['python3', 'ci/image/integrity_selftest.py'],
 'privacy-controls': ['python3', 'ci/image/privacy_selftest.py'],
 'patch-controls': ['python3', 'ci/image/privacy_patch_selftest.py'],
 'baremetal': ['python3', 'scripts/check_baremetal_only.py', '--check'],
 'baremetal-controls': ['python3', 'scripts/check_baremetal_only.py', '--selftest'],
 'lock-consistency': ['python3', 'ci/image/build.py', '--work', str(SCRATCH/'image'), '--check-lock'],
}
def run(item):
 name, command = item
 start = time.monotonic()
 with (OUT/(name+'.log')).open('w') as log:
  result = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
 (OUT/(name+'.rc')).write_text(str(result.returncode)+'\n')
 return {'name':name, 'argv':command, 'rc':result.returncode, 'seconds':round(time.monotonic()-start,3)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(run,commands.items()))
(OUT/'focused-checks.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
