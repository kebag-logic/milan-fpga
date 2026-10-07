#!/usr/bin/env python3
"""Run focused review work concurrently, with every child waited in the foreground.
Usage: run_review.py SOURCE PACKET
No source-tree mutation. All disposable work is below PACKET/scratch.
"""
import concurrent.futures, json, os, pathlib, subprocess, sys, tarfile, time
src, packet = map(lambda s: pathlib.Path(s).resolve(), sys.argv[1:])
scratch = packet/'scratch'; receipts = packet/'receipts'
scratch.mkdir(exist_ok=True); receipts.mkdir(exist_ok=True)
archive = scratch/'source.tar'
with archive.open('wb') as f: subprocess.run(['git','-C',str(src),'archive','HEAD'],stdout=f,check=True)
trees = {}
for name in ['campaign','suites','docs']:
    t = scratch/name; t.mkdir(exist_ok=True)
    with tarfile.open(archive) as a: a.extractall(t,filter='data')
    trees[name] = t
scratch_tmp = scratch/'tmp'; scratch_tmp.mkdir(exist_ok=True)
env = os.environ.copy(); env.update(TMPDIR=str(scratch_tmp), MAKEFLAGS='-j16', PYTHONDONTWRITEBYTECODE='1')
sim = str(packet/'scripts/simulator.py')
env['VERILATOR'] = sim
version=subprocess.check_output([sim,'--version'],text=True,env=env).strip()
assert version.startswith('Verilator 5.050 '), version
(receipts/'replay-simulator-version.txt').write_text(version+'\n')

def command(name, cwd, argv):
    start=time.time()
    with (receipts/(name+'.log')).open('w') as log:
        log.write('COMMAND '+json.dumps(argv)+'\n');log.flush()
        child_env = env.copy()
        rc=subprocess.run(argv,cwd=cwd,env=child_env,stdout=log,stderr=subprocess.STDOUT).returncode
    (receipts/(name+'.rc')).write_text(str(rc)+'\n')
    print(json.dumps({'task':name,'rc':rc,'seconds':round(time.time()-start,2)}),flush=True)
    return rc

def focused():
    results=[]
    for suite in ['tx_arbiter','aecp_notify','adp_engine','pp_top']:
        results.append(command(suite,trees['suites']/'tb'/suite,['make','-j16','VERILATOR='+sim]))
    return max(results)

with concurrent.futures.ThreadPoolExecutor(3) as pool:
    futures=[pool.submit(command,'notify-campaign',trees['campaign'],['python3','tb/pp_top/notify_mutants.py','--jobs','4','--verilator',sim,'--output',str(receipts/'notify-campaign')]),pool.submit(focused),pool.submit(command,'docs',src,['make','-j16','check'])]
    results=[f.result() for f in futures]
raise SystemExit(max(results))
