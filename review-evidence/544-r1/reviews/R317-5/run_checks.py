#!/usr/bin/env python3
"""Run only gate 1b and unchanged public round-2 probes, with two workers.
Raw local paths remain in scratch; export.py writes public-safe receipts.
"""
import argparse, concurrent.futures, json, os, subprocess, sys, time
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument('--root', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
p.add_argument('--verilator-bin', type=Path, required=True)
a = p.parse_args()
a.root = a.root.resolve(); a.packet = a.packet.resolve()
scratch = a.packet / 'scratch'; raw = scratch / 'raw'
raw.mkdir(exist_ok=True)
sdk = scratch / 'sdk'
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1',
           PATH=str(a.verilator_bin) + os.pathsep + os.environ['PATH'], MAKEFLAGS='-j2')
py = [sys.executable, '-B']
jobs = []
for mode in ('sdk', 'absent'):
    args = ['--sdk-destination', str(sdk), '--require-rv32'] if mode == 'sdk' else ['--absent']
    jobs.append(('gate1b-' + mode, py + ['sw/builder/test_firmware_compiler.py', *args,
                 '--audit', str(raw / ('gate1b-' + mode + '-argv.jsonl'))]))
public = a.packet / 'public-inputs/reviews'
for case in ('cases_544_r2', 'cases_544_r2b', 'cases_544_r2c', 'cases_544_r2d', 'cases_544_r2e'):
    for mode, disconnect in (('sdk',False),('absent',False),('sdk',True),('absent',True)):
        tag = case + '-' + mode + ('-disconnect' if disconnect else '')
        cmd = py + [str(public / 'R317-2/probe_gate1b_r2.py'), '--mode', mode,
                     '--rev', 'head', '--cases', case, '--tag', tag, '--outdir', str(raw)]
        if mode == 'sdk': cmd += ['--sdk', str(sdk)]
        if disconnect: cmd += ['--disconnect']
        jobs.append((tag, cmd))
for mode, disable in (('sdk',None),('absent',None),('sdk','assert_preprocessed_asm_allowlist')):
    tag = 'probe2-' + mode + ('-disconnect-asm' if disable else '')
    cmd = py + [str(public / 'R316-2/scripts/r316-2/probe2.py'), mode,
        '--out', str(raw / (tag + '.json')), '--scratch', str(scratch)]
    if mode == 'sdk': cmd += ['--sdk', str(sdk)]
    if disable: cmd += ['--disable', disable]
    jobs.append((tag, cmd))
def run(job):
    tag, cmd = job; started = time.monotonic()
    with (raw / (tag + '.log')).open('w') as out:
        r = subprocess.run(cmd, cwd=a.root, env=env, stdout=out, stderr=subprocess.STDOUT, timeout=2400)
    row = dict(tag=tag, argv=cmd, rc=r.returncode, seconds=round(time.monotonic()-started, 3))
    (raw / (tag + '-execution.json')).write_text(json.dumps(row,indent=2)+'\n')
    print(tag, 'rc='+str(r.returncode), flush=True)
    return row
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    rows = list(pool.map(run, jobs))
(raw / 'execution.json').write_text(json.dumps(rows,indent=2)+'\n')
raise SystemExit(0 if all(r['rc']==0 for r in rows) else 1)
