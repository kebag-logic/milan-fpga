#!/usr/bin/env python3
"""Run only issue 177 controls, with all disposable files under scratch."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import tarfile
import time

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--output', type=Path, default=Path(__file__).resolve().parent,
               help='Use a fresh directory to preserve earlier receipts.')
p.add_argument('--simulator', default='$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
a = p.parse_args()
out = a.output.resolve()
out.mkdir(parents=True, exist_ok=True)
scratch = out / 'scratch'
scratch.mkdir(exist_ok=True)
tree = scratch / 'focused-source'
tree.mkdir()
archive = scratch / 'head.tar'
with archive.open('wb') as f:
    subprocess.run(['git', '-C', str(a.source), 'archive', '6aaec5dfc45e84c8842f3f31f76910bfa91a96e1'], stdout=f, check=True)
with tarfile.open(archive) as f:
    f.extractall(tree, filter='data')
identity = subprocess.check_output([a.simulator, '--version'], text=True)
(out / 'simulator-identity.txt').write_text(identity)
assert '5.050' in identity
# Bench recipes request unlimited compile workers. Limit each invocation to two.
wrapper = scratch / 'bounded-simulator.py'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i]=="-j": a[i+1]="2"\nos.execv(' + repr(a.simulator) + ', [' + repr(a.simulator) + '] + a)\n')
wrapper.chmod(0o755)
env = dict(os.environ, TMPDIR=str(scratch), MAKEFLAGS='-j16', PYTHONDONTWRITEBYTECODE='1')
arms = ['m9-guard-get-avb-info', 'gavb-other-type-not-supported', 'gavb-other-type-header-only', 'gavb-type-gate-dropped', 'gavb-type-low-byte', 'gavb-interface-not-implemented', 'gavb-locate-miss-ignored', 'gavb-padded-refused', 'gavb-floor-14']
jobs = {
 'dispatch': ['python3', '-B', 'tb/pp_top/aecp_dispatch_mutants.py', '--jobs', '3', '--only', ','.join(arms), '--output', str(out/'dispatch'), '--verilator', str(wrapper)],
 'decode': ['python3', '-B', 'tb/aecp_cmds/mutants.py', '--jobs', '2', '--only', 'gavb-other-type-not-supported', '--output', str(out/'decode'), '--verilator', str(wrapper)],
 'docs': ['make', '-j16', 'aecpcmd', 'links', 'matrix', 'reqtags', 'modmatrix', 'params', 'ids', 'figures', 'stale'],
}
def run(item):
    name, cmd = item
    (out/(name+'.command.json')).write_text(json.dumps(cmd, indent=2)+'\n')
    start = time.monotonic()
    with (out/(name+'.log')).open('w') as f:
        # Documentation inventory gates need the original Git index.
        rc = subprocess.run(cmd, cwd=a.source if name == 'docs' else tree, env=env, stdout=f, stderr=subprocess.STDOUT).returncode
    (out/(name+'.rc')).write_text(str(rc)+'\n')
    result = {'campaign':name, 'rc':rc, 'seconds':round(time.monotonic()-start, 2)}
    print(json.dumps(result), flush=True)
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, jobs.items()))
(out/'focused-results.json').write_text(json.dumps(results, indent=2)+'\n')
raise SystemExit(any(r['rc'] for r in results))
