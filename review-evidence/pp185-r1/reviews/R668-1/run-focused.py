#!/usr/bin/env python3
import concurrent.futures, os, pathlib, subprocess, time
p = pathlib.Path(__file__).resolve().parent
source = p / 'scratch/source'
env = os.environ.copy()
env['TMPDIR'] = str(p/'scratch/tmp')
env['MAKEFLAGS'] = '-j16'
env['VERILATOR'] = str(p / 'bounded-sim.py')
env['REVIEW_BUILD_JOBS'] = '4'
jobs = {
 'notify-baseline': ['make', '-j16', '-C', 'tb/aecp_notify', 'check'],
 'ucpu-baseline': ['make', '-j16', '-C', 'tb/ucpu', 'run'],
 'router-baseline': ['make', '-j16', '-C', 'tb/event_router'],
 'descriptor-lock-baseline': ['make', '-j16', '-C', 'tb/pp_top', 'aecp-dispatch'],
}
def run(item):
 name, cmd = item
 start = time.monotonic()
 with (p/'receipts'/f'{name}.log').open('w') as f:
  f.write('Command: ' + ' '.join(cmd) + '\n'); f.flush()
  rc = subprocess.run(cmd, cwd=source, env=env, stdout=f, stderr=subprocess.STDOUT).returncode
 (p/'receipts'/f'{name}.rc').write_text(str(rc)+'\n')
 print(f'{name}: rc={rc} elapsed={time.monotonic()-start:.1f}s', flush=True)
 return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results = list(pool.map(run, jobs.items()))
raise SystemExit(any(results))
