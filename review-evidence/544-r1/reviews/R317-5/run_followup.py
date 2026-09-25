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
public = a.packet / 'public-inputs/reviews'
for mode, disable in (('sdk','assert_preprocessed_identity_sample'),('absent','assert_identity_macro_free')):
    tag='probe2-'+mode+'-disconnect-identity'
    cmd=py+[str(public/'R316-2/scripts/r316-2/probe2.py'),mode,'--disable',disable,
        '--out',str(raw/(tag+'.json')),'--scratch',str(scratch)]
    if mode=='sdk':cmd+=['--sdk',str(sdk)]
    jobs.append((tag,cmd))
for mode in ('sdk','absent'):
    tag='retained-S3-'+mode
    cmd=py+[str(public/'R317-2/probe_gate1b.py'),'--mode',mode,'--rev','head','--only','S3 verifier',
        '--tag',tag,'--outdir',str(raw)]
    if mode=='sdk':cmd+=['--sdk',str(sdk)]
    jobs.append((tag,cmd))
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
(raw / 'followup-execution.json').write_text(json.dumps(rows,indent=2)+'\n')
raise SystemExit(0 if all(r['rc']==0 for r in rows) else 1)
