#!/usr/bin/env python3
"""Focused review checks; all children are joined, outputs stay in this packet."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import os, subprocess, sys, json
P = Path(__file__).resolve().parent
R = Path(sys.argv[1]).resolve()
S = P / 'scratch'
S.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(S),
           VERILATOR=os.environ.get('VERILATOR', 'verilator'),
           VBUILD_JOBS='1')
def run(name, cmd):
    with (P / (name + '.log')).open('w') as f:
        f.write('COMMAND: '+repr(cmd)+'\n'); f.flush()
        rc = subprocess.run(cmd, cwd=R, env=env, stdout=f, stderr=subprocess.STDOUT).returncode
    (P / (name+'.rc')).write_text(str(rc)+'\n')
    print(name, rc, flush=True)
    return name, rc
checks = [
 ('protocol-driver', ['python3','-B',str(P/'run_protocol.py'),str(R)]),
 ('publication-driver',['python3','-B',str(P/'run_publication.py'),str(R)]),
 ('core-mutants',['python3','-B','sw/firmware/ctrl/test/gptp_mutants.py','--jobs','6','--build-dir',str(S/'mutants')]),
 ('core-arms',['python3','-B',str(P/'run_arms.py'),str(R)]),
]
with ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(lambda c:run(*c),checks))
(P/'execution.json').write_text(json.dumps(dict(results),indent=2)+'\n')
sys.exit(any(rc for _,rc in results))
