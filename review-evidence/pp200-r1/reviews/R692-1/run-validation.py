#!/usr/bin/env python3
"""Run focused review checks in disposable copies; no source checkout edits.
Usage: python3 run-validation.py SOURCE PINNED_SIMULATOR
Concurrent foreground children are joined before this program exits.
"""
import concurrent.futures, datetime, json, os, pathlib, subprocess, sys
P = pathlib.Path(__file__).resolve().parent
S = P / 'scratch'
S.mkdir(exist_ok=True)
source = pathlib.Path(sys.argv[1]).resolve()
sim = pathlib.Path(sys.argv[2]).resolve()
head = '33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33'
tree = S / 'validation'
def command(args, cwd=None, **kw):
    return subprocess.run(args, cwd=cwd, check=True, **kw)
if not tree.exists():
    command(['git', 'clone', '--no-hardlinks', '--no-checkout', str(source), str(tree)])
    command(['git', 'checkout', '--detach', head], tree)
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=tree, text=True).strip() == head
wrapper = S / 'bounded-simulator.py'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i,v in enumerate(a[:-1]):\n if v=="-j": a[i+1]="3"\nos.execv('+repr(str(sim))+', ['+repr(str(sim))+']+a)\n')
wrapper.chmod(0o755)
env = os.environ.copy()
env.update(TMPDIR=str(S), PYTHONDONTWRITEBYTECODE='1', MAKEFLAGS='-j16')
tasks = [
 ('make-check', ['make', '-j16', 'check']),
 ('decode-control', ['python3', '-B', 'tb/aecp_cmds/mutants.py', '--jobs', '1', '--only', 'gavb-other-type-not-implemented', '--verilator', str(wrapper), '--output', str(P/'decode-control')]),
 ('dispatch-controls', ['python3', '-B', 'tb/pp_top/aecp_dispatch_mutants.py', '--jobs', '2', '--only', 'm9-guard-get-avb-info,gavb-other-type-not-implemented,gavb-other-type-header-only,gavb-other-type-full-body,gavb-type-gate-dropped,gavb-type-low-byte,gavb-interface-not-supported,gavb-locate-miss-ignored,gavb-padded-refused,gavb-floor-14', '--verilator', str(wrapper), '--output', str(P/'dispatch-controls')]),
]
def run(task):
    name,args=task
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (P/(name+'.log')).open('w') as log:
        log.write(json.dumps({'command':args,'head':head,'start':start})+'\n');log.flush()
        rc=subprocess.run(args,cwd=tree,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
    (P/(name+'.rc')).write_text(str(rc)+'\n')
    print(name, 'rc='+str(rc), flush=True)
    return {'name':name,'rc':rc,'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(run,tasks))
(P/'validation-results.json').write_text(json.dumps(results,indent=2)+'\n')
sys.exit(int(any(r['rc'] for r in results)))
