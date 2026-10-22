#!/usr/bin/env python3
"""Run a focused wrapper suite and omit-appended-identity fault control."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
compiler = sys.argv[2]
packet = Path(__file__).resolve().parent
assert root.is_relative_to(packet / 'scratch'), 'use only a disposable clone'
suite = root / 'tb/verilator/gptp_shadow'
source = root / 'gptp-processor/hdl/top/KL_gptp_engine.sv'
original = source.read_bytes()
env = dict(os.environ, TMPDIR=str(packet / 'scratch'), PYTHONDONTWRITEBYTECODE='1')
results = {}
version = subprocess.check_output([compiler, '--version'], text=True).strip()
assert '5.050' in version, version

def run(name):
    command = ['make', '-j16', '-C', str(suite), 'run',
               'VERILATOR=' + compiler, 'VERILATOR_JOBS=8']
    with (packet / 'scratch' / (name + '-build.log')).open('wb') as log:
        build = subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT,
                               timeout=540)
    # Preserve the executable's complete raw output separately from compiler paths.
    with (packet / (name + '.log')).open('wb') as log:
        sim = subprocess.run(['./obj_dir/Vgptp_shadow_sim'], cwd=suite, env=env,
                             stdout=log, stderr=subprocess.STDOUT, timeout=120)
    results[name] = {'build_and_run_rc': build.returncode, 'simulation_rc': sim.returncode,
                     'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
    (packet / (name + '.rc')).write_text(str(sim.returncode) + '\n')

try:
    run('shadow-golden')
    old = b'(ann_pub_count_clamped_w != 4\'d0) &&'
    assert original.count(old) == 1
    source.write_bytes(original.replace(old, b"1'b0 &&"))
    run('shadow-no-append')
finally:
    source.write_bytes(original)
    assert source.read_bytes() == original
results['compiler_version'] = version
(packet / 'shadow-probe-results.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
assert results['shadow-golden']['build_and_run_rc'] == 0
assert results['shadow-golden']['simulation_rc'] == 0
assert results['shadow-no-append']['build_and_run_rc'] != 0
assert results['shadow-no-append']['simulation_rc'] != 0
assert 'published full path count' in (packet / 'shadow-no-append.log').read_text()
