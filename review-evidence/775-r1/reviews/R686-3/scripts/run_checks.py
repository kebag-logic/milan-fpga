#!/usr/bin/env python3
"""Foreground supervisor: independent campaigns run concurrently, bounded to 12 compiler jobs."""
import concurrent.futures, json, os, subprocess, sys, time
from pathlib import Path
repo, packet, simulator = map(lambda p: Path(p).resolve(), sys.argv[1:4])
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
bin_dir = scratch / 'bin'
bin_dir.mkdir(exist_ok=True)
version = subprocess.check_output([str(simulator), '--version'], text=True).strip()
assert '5.050' in version and 'rev v5.050' in version, version
(packet / 'simulator-identity.txt').write_text(version + '\n')
wrapper = bin_dir / 'verilator'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i] == "-j": a[i+1]="4"\nos.execv(' + repr(str(simulator)) + ', [' + repr(str(simulator)) + ']+a)\n')
wrapper.chmod(0o755)
env = os.environ.copy()
env.update(PATH=str(bin_dir)+os.pathsep+env['PATH'], VERILATOR=str(wrapper),
           TMPDIR=str(scratch), PYTHONPYCACHEPREFIX=str(scratch/'pycache'), MAKEFLAGS='-j16')
tasks = [
    ('format', [sys.executable, str(packet/'scripts/run_format.py'), str(repo), str(scratch/'format-details')], repo),
    ('sq-probe', [sys.executable, '-I', str(packet/'scripts/probe_sq_claims.py'), str(repo), str(scratch/'sq-probe'), '2'], repo),
]
def task(item):
    name, cmd, cwd = item
    start = time.monotonic()
    with (scratch/(name+'.log')).open('w') as log:
        p = subprocess.run(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
    result = {'task':name,'rc':p.returncode,'elapsed_seconds':round(time.monotonic()-start,2)}
    (scratch/(name+'.rc')).write_text(str(p.returncode)+'\n')
    print(json.dumps(result), flush=True)
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(task, tasks))
(packet/'execution-summary.json').write_text(json.dumps(results, indent=2)+'\n')
sys.exit(int(any(r['rc'] for r in results)))
