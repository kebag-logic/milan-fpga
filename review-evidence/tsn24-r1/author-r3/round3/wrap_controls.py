#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Run the unchanged wrap harness and require each planted failure."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--work', type=Path, required=True)
work = parser.parse_args().work.resolve()
out = work / 'wrap-controls'
out.mkdir(exist_ok=True)
rows = []
env = dict(os.environ, ASAN_OPTIONS='detect_leaks=1:halt_on_error=1', UBSAN_OPTIONS='halt_on_error=1')
for name, expected in [('baseline', (0, 0)), ('g-expiry-skipped-with-listener', (1, 0)),
                       ('g-expiry-skipped-invalid-da', (0, 1))]:
    source = work / 'tree' if name == 'baseline' else work / 'gap' / name / 'tree'
    binary = out / name
    argv = ['clang', '-std=c11', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer',
            '-I' + str(source / 'include'), str(source / 'src/acmp.c'),
            str(work / 'review-scripts/wrap_alias_demo.c'), '-o', str(binary)]
    with (out / (name + '-build.log')).open('w') as log:
        built = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT, env=env).returncode
    (out / (name + '-build.rc')).write_text(str(built) + '\n')
    assert built == 0
    result = subprocess.run([str(binary)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    (out / (name + '.log')).write_bytes(result.stdout)
    (out / (name + '.rc')).write_text(str(result.returncode) + '\n')
    wanted = (f'listener-held 2^32+100 ms then withdrawn: declaring={expected[0]} (claim: 0)\n'
              f'destination invalid 2^32+100 ms then valid: declaring={expected[1]} (claim: 0)\n').encode()
    assert result.returncode == int(any(expected)) and result.stdout == wanted
    rows.append(dict(case=name, build_rc=built, run_rc=result.returncode,
                     expected_failure=bool(any(expected)), listener_declaring=expected[0],
                     destination_declaring=expected[1], bytes=binary.stat().st_size,
                     sha256=hashlib.sha256(binary.read_bytes()).hexdigest()))
(out / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
print('Wrap harness: baseline closed; both planted stale-probe revivals reproduced')
