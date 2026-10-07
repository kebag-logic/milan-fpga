# SPDX-License-Identifier: Apache-2.0
"""Run bounded, foreground review campaigns; all products stay in packet scratch."""
import argparse
import concurrent.futures
import os
from pathlib import Path
import subprocess
import threading

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--packet', type=Path, required=True)
parser.add_argument('--jobs', type=int, default=4)
args = parser.parse_args()
source, packet = args.source.resolve(), args.packet.resolve()
scratch = packet / 'scratch'
prefix = scratch / 'cgreen'
build_lock = threading.Lock()
env = os.environ.copy()
env.update(PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch), LD_LIBRARY_PATH=str(prefix / 'lib'))

def run(label, cmd, extra=None):
    e = env | (extra or {})
    r = subprocess.run(list(map(str, cmd)), cwd=source, env=e, capture_output=True, text=True, timeout=540)
    raw = r.stdout + r.stderr
    (scratch / (label + '.raw.log')).write_text(raw)
    out = raw.replace(str(source), '$SOURCE').replace(str(packet), '$PACKET')
    (packet / 'receipts' / (label + '.log')).write_text(out)
    (packet / 'receipts' / (label + '.rc')).write_text(str(r.returncode) + '\n')
    print(label, 'rc', r.returncode, flush=True)
    if r.returncode:
        print(out[-2000:], flush=True)
    return r.returncode

def profile(mode):
    b = scratch / ('build-' + mode)
    with build_lock:
        if run('configure-' + mode, ['cmake', '-S', source, '-B', b, '-DCMAKE_BUILD_TYPE=Debug', '-DCMAKE_PREFIX_PATH=' + str(prefix), '-DLWSRP_MILAN=' + mode]):
            return 1
        if run('build-' + mode, ['make', '-C', b, '-j16']):
            return 1
    failures = run('ctest-' + mode, ['ctest', '--test-dir', b, '--output-on-failure'])
    failures += run('unit-' + mode, [b / 'unit_tests'])
    failures += run('scenarios-' + mode, ['behave'], {'SHLAN_LIBRARY': str(b / 'libshlan.so')})
    binary = scratch / ('probe-rx-' + mode)
    cmd = ['cc', '-std=c11', '-g', '-I' + str(source / 'src/include'), '-I' + str(source / 'src'), packet / 'scripts/probe_rx.c', '-L' + str(b), '-lshlan', '-Wl,-rpath,' + str(b), '-o', binary]
    failures += run('probe-rx-build-' + mode, cmd)
    failures += run('probe-rx-' + mode, [binary])
    return failures

def docs():
    result = 0
    for name, extra in [('sentences', []), ('references', []), ('references-selftest', ['--self-test']), ('links', ['--github-auth'])]:
        tool = 'references' if name == 'references-selftest' else name
        result += run('docs-' + name, ['python3', source / ('doc/tools/check_' + tool + '.py'), *extra])
    return result

def ports():
    with build_lock:
        result = run('embedded', ['python3', source / 'tests/check_embedded.py', '--work-dir', scratch / 'embedded'])
    for mode in ['OFF', 'ON']:
        result += run('freestanding-' + mode, ['python3', source / 'tests/check_freestanding.py'], {'CC': 'cc -DLWSRP_MILAN=' + ('1' if mode == 'ON' else '0')})
    result += run('scenario-dry-run', ['behave', '--dry-run'])
    return result

with concurrent.futures.ThreadPoolExecutor(max_workers=min(args.jobs, 4)) as pool:
    jobs = [pool.submit(profile, mode) for mode in ['OFF', 'ON']]
    jobs += [pool.submit(docs), pool.submit(ports)]
    results = [j.result() for j in jobs]
raise SystemExit(any(results))
