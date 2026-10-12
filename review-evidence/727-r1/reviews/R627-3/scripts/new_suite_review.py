#!/usr/bin/env python3
"""Exercise the documented new-suite steps in a disposable clone.

First two stages run the selector and actual driver refusal. The successful
stage uses an otherwise byte-identical driver whose final dispatch stops after
its real preflight calls, so it launches no suite or full bank. Final replacement
uses a synthetic hosted-format log and is explicitly not a hosted measurement.
"""
import concurrent.futures
import difflib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

source=Path(sys.argv[1]).resolve();packet=Path(sys.argv[2]).resolve()
scratch=packet/'scratch'; root=scratch/'new-suite';out=packet/'receipts/new-suite';out.mkdir(exist_ok=True)
env={**os.environ,'TMPDIR':str(scratch),'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'}
if root.exists(): raise SystemExit('Use a fresh scratch/new-suite directory')
subprocess.run(['git','clone','--shared','--no-checkout',str(source),str(root)],check=True,capture_output=True)
subprocess.run(['git','checkout','--detach','2c2f336979e4fdb1da444f041f37551e2c9175df'],cwd=root,check=True,capture_output=True)
new=root/'tb/verilator/zz_review_suite';new.mkdir();(new/'Makefile').write_text('all:\n\t@echo planted\n')

def run(name,args,expected=0):
    r=subprocess.run(args,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=540)
    (out/(name+'.log')).write_bytes(r.stdout);(out/(name+'.rc')).write_text(str(r.returncode)+'\n')
    print(name,'rc',r.returncode,'expected',expected,flush=True)
    assert r.returncode==expected,r.stdout.decode(errors='replace')[-5000:]
    return r.stdout.decode()

def edit(path,pairs):
    p=root/path; text=p.read_text()
    for old,new in pairs:
        assert old in text,(path,old)
        text=text.replace(old,new,1) if old=='SUITE_SECONDS = {' else text.replace(old,new)
    p.write_text(text)

refusal=run('01-no-figure-selftest',['python3','scripts/suite_shards.py','--selftest'],1)
for word in ('provisional','suite_timeout','add a worker','hosted run'): assert word in refusal
run('01-no-figure-shard',['bash','scripts/run_all_suites.sh','--shard','0/5','--list'],2)
run('01-no-figure-serial',['bash','scripts/run_all_suites.sh',str(scratch/'new-suite-refused')],2)
# Step 1: read the actual shell function's return value, without a mirrored default.
driver=(root/'scripts/run_all_suites.sh').read_text()
function=driver[driver.index('suite_timeout() {'):driver.index('\n}',driver.index('suite_timeout() {'))+2]
value=subprocess.check_output(['bash','-c',function+'\nsuite_timeout zz_review_suite'],env={k:v for k,v in env.items() if k!='SUITE_TIMEOUT'}).decode().strip()
assert value=='1800'
edit('scripts/suite_shards.py', [('SUITE_SECONDS = {','SUITE_SECONDS = {\n    "zz_review_suite": '+value+','),
    ('PROVISIONAL_SUITES: frozenset[str] = frozenset()','PROVISIONAL_SUITES: frozenset[str] = frozenset({"zz_review_suite"})')])
run('02-provisional-over-bound',['python3','scripts/suite_shards.py','--selftest'],1)
# Step 2: make each count/ownership/fixture update the docstring names.
edit('.github/workflows/rtl.yml', [
    ('shard: [0, 1, 2, 3, 4]','shard: [0, 1, 2, 3, 4, 5]'),('total: [5]','total: [6]'),
    ('--expect 5','--expect 6'),('4) test "$(cat "$RUNNER_TEMP/owned-suites")" = milan_dp','5) test "$(cat "$RUNNER_TEMP/owned-suites")" = milan_dp')])
edit('scripts/ci_events.py', [
    ('"--expect 6"),','"--expect 7"),'),
    ('--expect 5','--expect 6'),
    ('_m_dedicated_worker_reverted, "--expect 4"','_m_dedicated_worker_reverted, "--expect 5"'),
    ('4) test "$(cat "$RUNNER_TEMP/owned-suites")" = milan_dp','5) test "$(cat "$RUNNER_TEMP/owned-suites")" = milan_dp'),
    ('[0, 1, 2, 3, 4]','[0, 1, 2, 3, 4, 5]'),
    ('_restate_shards(w, "verilator-shards", "5")','_restate_shards(w, "verilator-shards", "6")'),
    ('shard.append(5)','shard.append(6)'),
    ('assert shard[-1] == 4','assert shard[-1] == 5'),
    ('assert matrix["shard"][-1] == 4','assert matrix["shard"][-1] == 5'),
    ('matrix["total"] = [4]','matrix["total"] = [5]'),
    ('[{"shard": 4, "total": 5}]','[{"shard": 5, "total": 6}]')])
edit('scripts/suite_shards.py', [
    ('WORKER_OVERHEAD_SECONDS = (83, 115, 80, 93, 80)','WORKER_OVERHEAD_SECONDS = (83, 115, 80, 93, 115, 80)'),
    ('landmarks = {"tsn_fuzz": 1, "chmap_capture": 3, "milan_dp": 4}','landmarks = {"tsn_fuzz": 1, "chmap_capture": 3, "milan_dp": 5}')])
patch=subprocess.check_output(['git','diff','--no-ext-diff','--no-textconv'],cwd=root)
(out/'documented-steps.diff').write_bytes(patch)
# Stop after the first five calls of main; every preflight command remains real.
assert driver.endswith('main "$@"\n')
preflight=driver[:-len('main "$@"\n')]+'''parse_args "$@"
select_suites
acquire_lock
prepare_logs
run_preflight_gates
'''
(root/'scripts/review_preflight.sh').write_text(preflight)
commands=[('03-six-worker-selftest',['python3','scripts/suite_shards.py','--selftest']),
          ('03-ci-events-check',['python3','scripts/ci_events.py','--check']),
          ('03-ci-events-selftest',['python3','scripts/ci_events.py','--selftest']),
          ('03-serial-preflight',['bash','scripts/review_preflight.sh',str(scratch/'new-suite-preflight')])]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    futures=[pool.submit(run,*item) for item in commands]
    for f in futures: f.result()
lists=[run(f'03-worker-{i}',['bash','scripts/run_all_suites.sh','--shard',f'{i}/6','--list']).splitlines() for i in range(6)]
inventory=run('03-serial-list',['bash','scripts/run_all_suites.sh','--list']).splitlines()
assert sorted(sum(lists,[]))==inventory and len(set(sum(lists,[])))==63
assert lists[5]==['milan_dp'] and 'tsn_fuzz' in lists[1] and 'chmap_capture' in lists[3]
for path in (scratch/'new-suite-preflight/preflight').glob('*.log'):
    (out/('preflight-'+path.name)).write_bytes(path.read_bytes())
# Step 3 cannot obtain a real hosted run for a disposable unpublished suite.
# Verify --measure and replacement mechanically with labelled synthetic data.
synthetic=out/'synthetic-hosted-format.log'
synthetic.write_text(''.join('Verilator shard 4/6\tRun suites\t'+line+'\n' for line in [
    '2026-01-01T00:00:00.0000000Z Current runner version',
    '2026-01-01T00:01:55.0000000Z shard: 4/6   selected suites: 1',
    '2026-01-01T00:03:55.2000000Z PASS     zz_review_suite',
    '2026-01-01T00:03:55.2000001Z suites: 1   passed: 1   failed: 0',
    '2026-01-01T00:03:58.2000000Z Cleaning up orphan processes']))
measured=run('04-synthetic-measure',['python3','scripts/suite_shards.py','--measure',str(synthetic)])
assert '"zz_review_suite": 121' in measured
spec=importlib.util.spec_from_file_location('six_selector',root/'scripts/suite_shards.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
figures=module.measure_log(synthetic.read_text());assert figures.overhead==118
edit('scripts/suite_shards.py', [('"zz_review_suite": 1800','"zz_review_suite": 121'),
    ('frozenset({"zz_review_suite"})','frozenset()'),
    ('(83, 115, 80, 93, 115, 80)','(83, 115, 80, 93, 118, 80)')])
run('04-synthetic-replaced-selftest',['python3','scripts/suite_shards.py','--selftest'])
(out/'summary.json').write_text(json.dumps({'suite':'zz_review_suite','provisional_seconds':1800,
    'six_worker_preflight_pass':True,'union_count':63,'step_3_real_hosted':'NOT RUN',
    'step_3_synthetic_mechanics_pass':True},indent=2)+'\n')
