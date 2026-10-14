#!/usr/bin/env python3
"""Run focused review checks concurrently, retaining foreground ownership."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
prefix = os.environ.get('REVIEW_RECEIPT_PREFIX', '')
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch),
           CI_IMAGE_SHFMT=str(scratch / 'shfmt'), GIT_CONFIG_NOSYSTEM='1',
           GIT_CONFIG_GLOBAL='/dev/null')
checks = {
    'inventory-check': ['scripts/ci_tool_inventory.py', '--check'],
    'inventory-selftest': ['scripts/ci_tool_inventory_selftest.py'],
    'build-selftest': ['ci/image/build_selftest.py'],
    'integrity-selftest': ['ci/image/integrity_selftest.py'],
    'privacy-selftest': ['ci/image/privacy_selftest.py'],
    'patch-selftest': ['ci/image/privacy_patch_selftest.py'],
    'lock-check': ['ci/image/build.py', '--work', str(scratch / 'lock'), '--check-lock'],
    'baremetal-check': ['scripts/check_baremetal_only.py', '--check'],
}
def run(item):
    name, args = item
    started = time.monotonic()
    result = subprocess.run([sys.executable, *args], cwd=root, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=480)
    log = result.stdout.decode(errors='replace').replace(str(root), '<checkout>').replace(str(scratch), '<scratch>')
    (packet / (prefix + name + '.log')).write_text(log)
    (packet / (prefix + name + '.rc')).write_text(str(result.returncode) + '\n')
    return {'check': name, 'argv': [sys.executable, *args], 'rc': result.returncode,
            'seconds': round(time.monotonic()-started, 3)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records = list(pool.map(run, checks.items()))
(packet / (prefix + 'checks.json')).write_text(json.dumps({'python':sys.version,'checks':records}, indent=2).replace(str(scratch), '<scratch>') + '\n')
print(json.dumps(records, indent=2).replace(str(scratch), '<scratch>'))
