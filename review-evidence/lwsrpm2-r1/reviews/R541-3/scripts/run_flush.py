# SPDX-License-Identifier: Apache-2.0
"""Reproduce the outstanding Flush loss; expected healthy result is zero."""
import argparse
import concurrent.futures
import os
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
p.add_argument('--jobs', type=int, default=2)
a = p.parse_args()
source, packet = a.source.resolve(), a.packet.resolve()

def profile(mode):
    binary = packet / 'scratch' / ('probe-flush-' + mode)
    cmd = ['cc', '-std=c11', '-g', '-O1', '-fsanitize=address,undefined', '-no-pie',
           '-DLWSRP_MILAN=' + ('1' if mode == 'ON' else '0'), '-Isrc/include', '-Isrc', '-Itests/unit',
           packet / 'scripts/probe_flush.c', 'src/core/mrp_mad.c', 'src/core/mrp_pdu.c',
           'src/modules/msrp.c', 'src/ports/timer.c', 'tests/unit/fault_alloc.c', '-o', binary]
    for label, command in [('build', cmd), ('run', [binary])]:
        r = subprocess.run(list(map(str, command)), cwd=source,
                           env=os.environ | {'ASAN_OPTIONS': 'detect_leaks=1:abort_on_error=1'},
                           capture_output=True, text=True, timeout=180)
        out = r.stdout + r.stderr
        (packet / 'receipts' / f'flush-{label}-{mode}.log').write_text(out.replace(str(source), '$SOURCE').replace(str(packet), '$PACKET'))
        (packet / 'receipts' / f'flush-{label}-{mode}.rc').write_text(str(r.returncode) + '\n')
        print(mode, label, r.returncode, out, flush=True)
        if r.returncode:
            return r.returncode
    return 0

with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs, 2)) as pool:
    results = list(pool.map(profile, ['OFF', 'ON']))
raise SystemExit(any(results))
