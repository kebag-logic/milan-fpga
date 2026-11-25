#!/usr/bin/env python3
"""Run independent source checks concurrently; keep disposable output in scratch."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
scratch = out / 'scratch'
env = dict(os.environ)
pin = env.get('REVIEW_TEST_PREFIX', '$VALIDATION_TOOLS/gtest-1.14.0')
env.update(PKG_CONFIG_PATH=pin + '/lib/pkgconfig', CMAKE_PREFIX_PATH=pin,
           LD_LIBRARY_PATH=pin + '/lib', TSN_CLANG=env.get('TSN_CLANG', '$VALIDATION_TOOLS/clang-18/bin/clang-18'))
env = {k: v for k, v in env.items() if not k.startswith('GTEST_')}

def campaign(name, commands):
    with (out / (name + '.log')).open('w') as log:
        for cmd in commands:
            log.write('COMMAND ' + ' '.join(cmd) + '\n')
            log.flush()
            rc = subprocess.run(cmd, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540).returncode
            log.write('RETURN ' + str(rc) + '\n')
            if rc:
                break
    (out / (name + '.rc')).write_text(str(rc) + '\n')
    print(name, rc, flush=True)
    return name, rc

gcc = str(scratch / 'host')
san = str(scratch / 'san')
campaigns = [
    ('host', [['cmake', '-S', str(root), '-B', gcc, '-DTSN_COVERAGE=ON', '-DCMAKE_BUILD_TYPE=Debug'],
              ['cmake', '--build', gcc, '-j5'], ['ctest', '--test-dir', gcc, '--output-on-failure', '-j5'],
              ['python3', 'scripts/coverage.py', gcc],
              ['python3', 'scripts/traceability.py', '--build', gcc, '--jobs', '5'],
              ['python3', 'scripts/test_inventory.py', '--build', gcc, '--jobs', '5']]),
    ('sanitizers', [['cmake', '-S', str(root), '-B', san, '-DCMAKE_BUILD_TYPE=Debug', '-DCMAKE_C_COMPILER=clang', '-DCMAKE_CXX_COMPILER=clang++', '-DTSN_SANITIZERS=ON'],
                    ['cmake', '--build', san, '-j5'], ['ctest', '--test-dir', san, '--output-on-failure', '-j5']]),
    ('six-plants', [['python3', 'scripts/mutation.py', '--work', str(scratch / 'plants'), '--jobs', '5', '--select', 'control-length']])
]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(lambda row: campaign(*row), campaigns))
(out / 'check-results.json').write_text(json.dumps(dict(results), indent=2) + '\n')
raise SystemExit(any(rc for _, rc in results))
