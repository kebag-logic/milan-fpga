#!/usr/bin/env python3
"""Replay published new-suite edits on a disposable candidate archive only."""
import argparse
import concurrent.futures
import os
import subprocess
import tarfile
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
a=p.parse_args(); repo=a.repo.resolve(); packet=a.packet.resolve()
root=packet/'scratch/new-suite-candidate'
root.mkdir(parents=True,exist_ok=False)
archive=packet/'scratch/new-suite-candidate.tar'
subprocess.run(['git','-c','core.commitGraph=false','archive','--format=tar','-o',str(archive),
                'b89a1ded1596030c4e0baf45a8509a20cbe04933'],cwd=repo,check=True)
with tarfile.open(archive) as tar: tar.extractall(root,filter='data')
env={**os.environ,'TMPDIR':str(packet/'scratch/tmp'),'PYTHONDONTWRITEBYTECODE':'1'}
suite=root/'tb/verilator/zz_new_suite';suite.mkdir()
(suite/'Makefile').write_text('all:\n\t@false\n')
def run(name,cmd,expected=0,needle=None):
    r=subprocess.run(cmd,cwd=root,env=env,text=True,capture_output=True,timeout=540)
    (packet/'receipts'/f'new-suite-{name}.log').write_text(r.stdout+r.stderr)
    (packet/'receipts'/f'new-suite-{name}.rc').write_text(str(r.returncode)+'\n')
    assert r.returncode==expected,(name,r.returncode,r.stderr)
    if needle: assert needle in r.stdout+r.stderr,(name,needle)
    print(f'PASS {name}: rc {r.returncode}, expected {expected}',flush=True)
    return r.stdout
run('missing',['python3','scripts/suite_shards.py','--selftest'],1,'inventory suite with no recorded duration')
run('missing-list',['bash','scripts/run_all_suites.sh','--shard','0/5','--list'],2,'new-suite steps')
step=packet/'scripts/published_new_suite_steps.py'
run('step1',['python3',str(step),str(root),'step1'])
run('five-worker-bound',['python3','scripts/suite_shards.py','--selftest'],1,'FAIL head worker')
run('step2',['python3',str(step),str(root),'step2'])
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    tasks=[pool.submit(run,'six-worker-selftest',['python3','scripts/suite_shards.py','--selftest'],0,'selftest: PASS'),
           pool.submit(run,'ci-check',['python3','scripts/ci_events.py','--check'],0,'ci_events: OK'),
           pool.submit(run,'ci-selftest',['python3','scripts/ci_events.py','--selftest'],0,'selftest: PASS'),
           pool.submit(run,'firmware-census',['python3','scripts/ci_events.py','--firmware-census'],0,'"preserved": true')]
    for task in tasks: task.result()
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    lists=list(pool.map(lambda i:run(f'list-{i}',['bash','scripts/run_all_suites.sh','--shard',f'{i}/6','--list']).splitlines(),range(6)))
flat=sum(lists,[])
default=run('default-list',['bash','scripts/run_all_suites.sh','--list']).splitlines()
assert sorted(flat)==sorted(default) and len(flat)==len(set(flat))==63
assert lists[5]==['milan_dp'] and 'tsn_fuzz' in lists[1] and 'chmap_capture' in lists[3]
print('PASS six-worker lists cover 63 suites exactly once, specialized owners retained',flush=True)
print('PASS candidate new-suite procedure and predecessor firmware census coexist; no suite/build/full preflight executed',flush=True)
