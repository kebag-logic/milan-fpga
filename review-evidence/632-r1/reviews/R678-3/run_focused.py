#!/usr/bin/env python3
"""Run bounded independent spot checks from an exact-head disposable tree."""
import concurrent.futures
import os
import pathlib
import subprocess
import sys
import tarfile
import time

packet = pathlib.Path(__file__).resolve().parent
repo = pathlib.Path(sys.argv[1]).resolve()
compiler = pathlib.Path(sys.argv[2]).resolve()
scratch = packet / 'scratch'
src = scratch / 'focused-src'
src.mkdir(parents=True, exist_ok=True)
archive = scratch / 'focused-src.tar'
with archive.open('wb') as f:
    subprocess.run(['git', '-C', str(repo), 'archive', 'ee5ece607816a1bfc834bd51734b703a8aab8e46', 'hdl', 'tb/common', 'tb/verilator/media_phase', 'tb/verilator/render_queue'], stdout=f, check=True)
with tarfile.open(archive) as tf:
    tf.extractall(src, filter='data')
env = os.environ.copy()
env.update(VERILATOR=str(compiler), VERILATOR_JOBS='4', TMPDIR=str(scratch))
tasks = {
    'phase-focused': ['python3', 'phase_mutants.py', '--jobs', '4', '--only', 'hold_keeps_ref,crf_carry_dropped,render_b_lead_dropped,render_read_untimed,render_frame_off_by_one,render_late_rule_removed,render_early_rule_removed'],
    'queue-clean': ['make', '-j16', 'run', 'VERILATOR_JOBS=4'],
}
def run(item):
    name, cmd = item
    cwd = src / 'tb/verilator' / ('media_phase' if name.startswith('phase') else 'render_queue')
    start = time.monotonic()
    with (packet / (name + '.log')).open('w') as log:
        r = subprocess.run(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
    (packet / (name + '.rc')).write_text(str(r.returncode) + '\n')
    return {'name': name, 'command': cmd, 'returncode': r.returncode, 'seconds': round(time.monotonic()-start, 2)}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, tasks.items()))
for r in results:
    print(r)
sys.exit(any(r['returncode'] for r in results))
