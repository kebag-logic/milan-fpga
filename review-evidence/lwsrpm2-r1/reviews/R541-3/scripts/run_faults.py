# SPDX-License-Identifier: Apache-2.0
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
scratch = packet / 'scratch'
env = os.environ | {'TMPDIR': str(scratch), 'ASAN_OPTIONS': 'detect_leaks=1:abort_on_error=1'}

def run(label, cmd):
    r = subprocess.run(list(map(str, cmd)), cwd=source, env=env, capture_output=True, text=True, timeout=180)
    out = r.stdout + r.stderr
    (scratch / (label + '.raw.log')).write_text(out)
    (packet / 'receipts' / (label + '.log')).write_text(out.replace(str(source), '$SOURCE').replace(str(packet), '$PACKET'))
    (packet / 'receipts' / (label + '.rc')).write_text(str(r.returncode) + '\n')
    print(label, r.returncode, out[-1200:], flush=True)
    return r.returncode

def profile(mode):
    binary = scratch / ('probe-fault-' + mode)
    common = ['cc', '-std=c11', '-g', '-O1', '-fno-omit-frame-pointer', '-fsanitize=address,undefined', '-no-pie', '-DLWSRP_MILAN=' + ('1' if mode == 'ON' else '0'), '-Isrc/include', '-Isrc', '-Itests/unit']
    srcs = ['src/core/mrp_mad.c', 'src/core/mrp_pdu.c', 'src/ports/timer.c', 'src/modules/msrp.c', 'tests/unit/fault_alloc.c']
    if run('fault-build-' + mode, common + [packet / 'scripts/probe_fault.c', *srcs, '-o', binary]):
        return 1
    failures = run('fault-' + mode, [binary])
    unit = scratch / ('unit-sanitized-' + mode)
    prefix = scratch / 'cgreen'
    units = sorted(source.glob('tests/unit/*_test.c')) + [source / 'tests/unit/main.c']
    cmd = common + ['-I' + str(prefix / 'include'), *units, *srcs, 'src/core/switch.c', 'src/modules/mmrp.c', 'src/modules/mvrp.c', '-L' + str(prefix / 'lib'), '-Wl,-rpath,' + str(prefix / 'lib'), '-lcgreen', '-o', unit]
    if run('sanitized-build-' + mode, cmd):
        return 1
    failures += run('sanitized-unit-' + mode, [unit])
    return failures

with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs, 2)) as pool:
    result = list(pool.map(profile, ['OFF', 'ON']))
raise SystemExit(any(result))
