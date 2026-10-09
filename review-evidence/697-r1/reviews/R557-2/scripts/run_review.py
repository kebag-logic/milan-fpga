#!/usr/bin/env python3
"""Foreground review supervisor. Run from an exact, clean repository checkout."""
import concurrent.futures as cf
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

repo, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
work = packet / 'scratch' / 'runs'
out = packet / 'receipts' / 'local'
work.mkdir(parents=True, exist_ok=True)
out.mkdir(parents=True, exist_ok=True)
(work / 'temp').mkdir(exist_ok=True)
env = {k:v for k,v in os.environ.items() if not k.startswith('GTEST_')}
env.update(PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(work/'temp'),
           ASAN_OPTIONS='detect_leaks=1:halt_on_error=1', UBSAN_OPTIONS='halt_on_error=1')
results = []

def sanitize(s):
    return s.replace(str(packet), '<PACKET>').replace(str(repo), '<REPO>').replace(str(Path.home()), '<HOME>')

def run(name, cmd, limit=570):
    start=time.monotonic()
    raw=work/(name+'.raw.log')
    with raw.open('w') as log:
        log.write('COMMAND: '+sanitize(' '.join(map(str,cmd)))+'\n');log.flush()
        try:
            p=subprocess.run(list(map(str,cmd)),cwd=repo,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=limit)
            rc=p.returncode
        except subprocess.TimeoutExpired:
            rc=124
    (out/(name+'.log')).write_text(sanitize(raw.read_text()))
    (out/(name+'.rc')).write_text(str(rc)+'\n')
    item={'gate':name,'rc':rc,'seconds':round(time.monotonic()-start,2)}
    results.append(item)
    (out/'gates.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(item),flush=True)
    return rc

py=sys.executable
def script(name,*args):
    return [py,'scripts/'+name+'.py',*args]

def hosted(kind,cc,cxx,option):
    b=work/kind
    if run(kind+'-configure',['cmake','-S','.', '-B',b,'-DCMAKE_BUILD_TYPE=Debug',
            '-DCMAKE_C_COMPILER='+cc,'-DCMAKE_CXX_COMPILER='+cxx,option]):return
    if run(kind+'-build',['cmake','--build',b,'-j4']):return
    for p in b.rglob('*.gcda'):p.unlink()
    if run(kind+'-test',['ctest','--test-dir',b,'--output-on-failure','-j4']):return
    if kind=='gcc':run('coverage',script('coverage',b))

# At most twelve analysis workers and two RV32 compiler jobs.
with cf.ThreadPoolExecutor(max_workers=2) as pool:
    futures=[pool.submit(run,'static-analysis',script('static_analysis')),
             pool.submit(run,'baremetal',script('baremetal','--work',work/'rv32','--jobs','1'))]
    for f in futures:f.result()

# Independent builds and the campaign share a twelve-job budget.
with cf.ThreadPoolExecutor(max_workers=3) as pool:
    futures=[pool.submit(hosted,'gcc','gcc','g++','-DTSN_COVERAGE=ON'),
             pool.submit(hosted,'clang-sanitizers','clang','clang++','-DTSN_SANITIZERS=ON'),
             pool.submit(run,'mutation',script('mutation','--work',work/'mutations','--jobs','4'))]
    for f in futures:f.result()

# Test registration reuses the completed GCC build. The two expensive control
# drivers run concurrently with a combined maximum of eight compiler jobs.
with cf.ThreadPoolExecutor(max_workers=2) as pool:
    futures=[pool.submit(run,'mutation-controls',script('mutation_selftest','--work',work/'mutation-controls','--jobs','4')),
             pool.submit(run,'boundary',script('check_boundary','--selftest','--work',work/'boundary','--jobs','4'))]
    for f in futures:f.result()
for name,args in [
    ('needle_audit',['--selftest']),('check_comments',['--selftest']),
    ('registration_selftest',['--work',work/'registration-controls']),
    ('check_license',['--selftest']),
    ('traceability',['--selftest','--build',work/'gcc','--jobs','16']),
    ('test_inventory',['--build',work/'gcc','--jobs','16']),
    ('coverage_selftest',[]),('check_privacy',[]),
    ('render_graphs',['--output',work/'graphs'])]:
    run(name,script(name,*args))
for src,dst in [(work/'mutations/results.json',out/'mutation-results.json'),
                (work/'rv32/results.json',out/'rv32-results.json')]:
    if src.exists():dst.write_text(sanitize(src.read_text()))
for p in (work/'graphs').glob('*.svg'):shutil.copy2(p,out/p.name)
raise SystemExit(any(x['rc'] for x in results))
