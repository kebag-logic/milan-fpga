#!/usr/bin/env python3
"""Foreground focused review; each independent task gets a log and exit receipt."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

packet = Path(__file__).resolve().parents[1]
source = Path(sys.argv[1]).resolve()
scratch = packet / 'scratch'
golden = scratch / 'golden'
golden.mkdir(exist_ok=True)
archive = subprocess.check_output(['git', 'archive', '8947bafdd62b4bf991debf7bfd8cdb73994a3a81'], cwd=source)
subprocess.run(['tar', '-x', '-C', str(golden)], input=archive, check=True)
env = os.environ.copy()
env['TMPDIR'] = str(scratch)
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['MAKEFLAGS'] = '-j16'
compiler = packet / 'scripts/compiler_bound.py'
compiler.chmod(0o755)
receipts = packet / 'receipts/runs'
receipts.mkdir(exist_ok=True)

def run(name, argv, cwd=golden):
    start = time.monotonic()
    with (receipts / (name + '.log')).open('w') as stream:
        rc = subprocess.run(argv, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT).returncode
    (receipts / (name + '.rc')).write_text(str(rc) + '\n')
    rec = {'name': name, 'argv': argv, 'rc': rc, 'seconds': round(time.monotonic()-start, 2)}
    print(json.dumps(rec), flush=True)
    return rec

def fixtures():
    rows = []
    for name, argv in [
        ('default-build', ['make', '-j16', 'gsi-build', 'VERILATOR='+str(compiler)]),
        ('default-run', ['./obj_dir/Vpp_top_sim']),
        ('shipping-build', ['make', '-j16', 'timer-defaults-build', 'VERILATOR='+str(compiler)]),
        ('shipping-withdraw', ['./obj_tdf/Vpp_top_tdf', '--withdraw-only'])]:
        rows.append(run(name, argv, golden / 'tb/pp_top'))
        if rows[-1]['rc']:
            break
    return rows

probes = packet / 'receipts/public/reviews/R518-2/scripts/reviewer_probes.py'
with concurrent.futures.ThreadPoolExecutor(3) as pool:
    futures = [pool.submit(run, 'reviewer-probes', ['python3', str(probes), str(golden), str(receipts/'probes'), str(compiler), '2', 'ctl-withdraw', 'r-wd-mask-dropped', 'r-wd-two-clocks', 'r-full-mask-dropped', 'r-full-two-clocks']),
               pool.submit(run, 'shipped-withdraw', ['python3', 'tb/pp_top/notify_mutants.py', '--jobs', '1', '--output', str(receipts/'shipped'), '--verilator', str(compiler), '--only', 'withdraw_mask_dropped', 'withdraw_two_clocks']),
               pool.submit(fixtures)]
    rows = [f.result() for f in futures]
(receipts/'execution.json').write_text(json.dumps(rows, indent=2)+'\n')
