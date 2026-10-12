#!/usr/bin/env python3
"""Run a bounded foreground review batch and retain each result separately."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root', type=Path)
    ap.add_argument('packet', type=Path)
    ap.add_argument('jobs_file', type=Path)
    ap.add_argument('--jobs', type=int, default=2)
    a = ap.parse_args()
    root, packet = a.root.resolve(), a.packet.resolve()
    scratch = packet / 'scratch'
    scratch.mkdir(parents=True, exist_ok=True)
    (packet / 'receipts').mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch),
               RUNNER_TEMP=str(scratch), VERILATOR=os.environ['VERILATOR'],
               CPATH=os.environ.get('CPATH',''), LIBRARY_PATH=os.environ.get('LIBRARY_PATH',''))
    def run(job):
        name = job['name']
        argv = [s.replace('{root}',str(root)).replace('{packet}',str(packet)) for s in job['argv']]
        cwd_text = job.get('cwd','.').replace('{root}',str(root)).replace('{packet}',str(packet))
        cwd = root / cwd_text
        start = time.monotonic()
        with (packet/'receipts'/f'{name}.log').open('w') as out:
            result = subprocess.run(argv, cwd=cwd, env=env, stdout=out, stderr=subprocess.STDOUT, check=False)
        record = dict(name=name, argv=argv, cwd=str(cwd), rc=result.returncode,
                      elapsed_s=round(time.monotonic()-start,3))
        (packet/'receipts'/f'{name}.rc').write_text(str(result.returncode)+'\n')
        (packet/'receipts'/f'{name}.json').write_text(json.dumps(record,indent=2)+'\n')
        work = scratch/name
        for f in ('run.log','escape.log','build.log'):
            if (work/f).is_file(): shutil.copyfile(work/f,packet/'receipts'/f'{name}.{f}')
        print(f'{name}: rc={result.returncode}, {record["elapsed_s"]} s',flush=True)
        return record
    jobs=json.loads(a.jobs_file.read_text())
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        results=list(pool.map(run,jobs))
    (packet/'receipts'/f'{a.jobs_file.stem}-results.json').write_text(json.dumps(results,indent=2)+'\n')
    return int(any(x['rc'] for x in results))

if __name__ == '__main__':
    raise SystemExit(main())
