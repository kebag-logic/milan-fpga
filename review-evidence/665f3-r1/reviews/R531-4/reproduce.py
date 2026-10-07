#!/usr/bin/env python3
"""Replay focused checks, all children joined, with disposable work under scratch.

Usage: python3 reproduce.py REPOSITORY NEW_OUTPUT_DIRECTORY
The repository must be the reviewed head with required submodules initialized.
The SDK is downloaded into the output directory, never installed globally.
"""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
scripts = Path(__file__).resolve().parent
scratch = out / 'scratch'
(scratch / 'tmp').mkdir(parents=True, exist_ok=True)
env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(scratch / 'tmp'),
       'MILAN_RV32_CC': str(scratch / 'sdk/bin/riscv32-linux-gcc')}

def run(name, argv):
    with (out / (name + '.log')).open('w') as log:
        result = subprocess.run([str(a) for a in argv], cwd=repo, env=env,
                                stdout=log, stderr=subprocess.STDOUT, timeout=580)
    (out / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(name, 'rc', result.returncode, flush=True)
    if result.returncode:
        raise RuntimeError(name)

py = sys.executable
run('tree-before', [py, scripts / 'verify_tree.py', repo])
run('sdk', [py, 'scripts/ci_rv32_sdk.py', '--destination', scratch / 'sdk'])
tasks = [
    ('image', [py, 'sw/firmware/ctrl/test/ctrl_image.py', '--base',
               'd51b373ad7e8e8381af2797be3ebb8ee45c62e3c', '--out', scratch / 'images']),
    ('selftest', [py, 'sw/firmware/ctrl/test/ctrl_image_selftest.py', '--require-rv32',
                  '--out', scratch / 'selftest']),
    ('helper-mutations', [py, scripts / 'helper_mutations.py', repo, scratch / 'mutations',
                         env['MILAN_RV32_CC']]),
    ('baremetal', [py, 'scripts/check_baremetal_only.py', '--check']),
    ('python-idiom', [py, 'scripts/check_py_idiom.py']),
]
# At most six mutation children plus three other foreground commands (<16 jobs).
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(run, name, argv) for name, argv in tasks]
    for future in futures:
        future.result()
run('independent-audit', [py, scripts / 'audit_images.py', scratch / 'images', env['MILAN_RV32_CC'], out])
run('tree-after', [py, scripts / 'verify_tree.py', repo])
