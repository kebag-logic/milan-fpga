#!/usr/bin/env python3
"""Complete unexecuted self-test mutants after the recorded timeout, without changing the suite."""
import argparse, concurrent.futures, os, subprocess, sys
from pathlib import Path
P=Path(__file__).resolve().parents[1]
R=P/'receipts/checks'
parser=argparse.ArgumentParser();parser.add_argument('--jobs',type=int,default=4);parser.add_argument('--worker',type=int)
args=parser.parse_args()
sys.path.insert(0,str(Path.cwd()/'tb/verilator/ctrl_service_budget'))
import selftest
all_names=list(selftest.selftest_mutants.MUTANTS)
old=(R/'run-controls.log').read_text().splitlines()
assert not any(x.startswith(('FAIL:','MUTANT ESCAPED:')) for x in old)
done=[name for name in all_names if any(x.startswith('MUTANT caught: '+name+': ') for x in old)]
remaining=[name for name in all_names if name not in done]
if args.worker is not None:
    selected=remaining[args.worker::args.jobs];failures=0
    for name in selected:
        with selftest.mutated(name):
            try: failed=[(n,detail) for n,ok,detail in selftest.checks() if not ok]
            except (selftest.grade.Refusal,KeyError,ValueError,IndexError,TypeError,RuntimeError) as error:
                failed=[(f'refused: {error}','')]
        if failed: print('MUTANT caught: '+name+': '+str(failed[0])[:250],flush=True)
        else:print('MUTANT ESCAPED: '+name,flush=True);failures+=1
    print('PARTITION',args.worker,'total',len(selected),'failures',failures,flush=True)
    sys.exit(bool(failures))
print('Total',len(all_names),'already caught',len(done),'remaining',len(remaining),flush=True)
failed=[(n,d) for n,ok,d in selftest.checks() if not ok]
assert not failed,failed
print('Unmutated self-test checks PASS',flush=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(P/'scratch'))
def run(i):
    with (R/f'run-resume-{i}.log').open('w') as f:
        rc=subprocess.run([sys.executable,'-u',__file__,'--jobs',str(args.jobs),'--worker',str(i)],env=env,stdout=f,stderr=subprocess.STDOUT).returncode
    (R/f'run-resume-{i}.rc').write_text(str(rc)+'\n')
    print('PARTITION',i,'rc',rc,flush=True);return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:results=list(pool.map(run,range(args.jobs)))
assert not any(results),results
joined='\n'.join((R/f'run-resume-{i}.log').read_text() for i in range(args.jobs))
assert not any(x.startswith('MUTANT ESCAPED:') for x in joined.splitlines())
assert all('MUTANT caught: '+name+': ' in joined for name in remaining)
print('PASS complete coverage:',len(done),'prior +',len(remaining),'resumed =',len(all_names),'caught; unmutated checks pass',flush=True)
