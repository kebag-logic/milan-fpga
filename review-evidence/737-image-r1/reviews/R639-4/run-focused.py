#!/usr/bin/env python3
"""Run review-only focused controls, synchronously, in an unchanged checkout."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
prefix = os.environ.get('REVIEW_RECEIPT_PREFIX', '')
env = dict(os.environ, TMPDIR=str(packet / 'scratch'), PYTHONDONTWRITEBYTECODE='1',
           CI_IMAGE_SHFMT=str(packet / 'scratch/shfmt'), GIT_CONFIG_GLOBAL='/dev/null',
           GIT_CONFIG_NOSYSTEM='1')
commands = [
    ['scripts/ci_tool_inventory.py', '--check'],
    ['scripts/ci_tool_inventory_selftest.py'],
    ['scripts/ci_inventory_patterns_selftest.py'],
    ['ci/image/build_selftest.py'],
    ['ci/image/integrity_selftest.py'],
    ['ci/image/privacy_selftest.py'],
    ['ci/image/privacy_patch_selftest.py'],
    ['ci/image/build.py', '--work', str(packet / 'scratch/lock-check'), '--check-lock'],
    ['scripts/check_baremetal_only.py', '--check'],
    ['scripts/check_baremetal_only.py', '--selftest'],
    ['scripts/docs_check.py'],
    ['scripts/check_doc_style.py'],
    ['scripts/check_doc_paths.py'],
]

def run(args):
    name = prefix + Path(args[0]).stem + ('-controls' if '--selftest' in args else '')
    start = time.monotonic()
    with (packet / (name + '.log')).open('w') as log:
        completed = subprocess.run([sys.executable, *args], cwd=root, env=env,
                                   stdout=log, stderr=subprocess.STDOUT, timeout=600)
    row = dict(command=['python3', *args], rc=completed.returncode,
               seconds=round(time.monotonic() - start, 3))
    (packet / (name + '.rc')).write_text(str(completed.returncode) + '\n')
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, commands))
(packet / (prefix + 'focused-results.json')).write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
