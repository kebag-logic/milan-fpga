#!/usr/bin/env python3
"""Run focused review checks in disposable copies; never modify the checkout.

Usage: python3 scripts/run_review.py --source CHECKOUT --jobs 3
The foreground coordinator waits for every task. Three mutation builds plus
one focused suite use at most sixteen compiler jobs (four per build).
"""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--jobs', type=int, default=3, choices=range(1, 4))
p.add_argument('--compiler', type=Path, default=Path('$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'))
a = p.parse_args()
packet = Path(__file__).resolve().parents[1]
scratch = packet / 'scratch'
logs = packet / 'receipts' / 'local'
logs.mkdir(parents=True, exist_ok=True)
head = 'a70e38804cb16435c089d024c58e8c3fb4d39ff6'
assert subprocess.check_output(['git', '-C', str(a.source), 'rev-parse', 'HEAD'], text=True).strip() == head
version = subprocess.check_output([str(a.compiler), '--version'], text=True)
assert 'Verilator 5.050 ' in version, version
(logs / 'compiler-identity.txt').write_text(version + 'wrapper_sha256=' + hashlib.sha256(a.compiler.read_bytes()).hexdigest() + '\n')
src = scratch / 'head'
src.mkdir(parents=True, exist_ok=True)
archive = subprocess.check_output(['git', '-C', str(a.source), 'archive', head])
with tarfile.open(fileobj=io.BytesIO(archive)) as t:
    t.extractall(src, filter='data')
binpath = scratch / 'bin'
binpath.mkdir(exist_ok=True)
wrapper = binpath / 'verilator'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i]=="-j" and a[i+1]=="0": a[i+1]="4"\nos.execv(' + repr(str(a.compiler)) + ',[' + repr(str(a.compiler)) + ']+a)\n')
wrapper.chmod(0o755)
env = dict(os.environ, PATH=str(binpath) + ':' + os.environ['PATH'], TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')

def run(tag, cmd, cwd=src):
    (logs / (tag + '.command.json')).write_text(json.dumps(cmd) + '\n')
    with (logs / (tag + '.log')).open('w') as out:
        rc = subprocess.run(cmd, cwd=cwd, env=env, stdout=out, stderr=subprocess.STDOUT).returncode
    (logs / (tag + '.rc')).write_text(str(rc) + '\n')
    return rc

sys.path.insert(0, str(src / 'tb'))
spec = importlib.util.spec_from_file_location('mutants', src / 'tb/verilator/parser/mutants.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def mutant(task):
    index, name, edits, breaks = task
    tag = f'mutant-{index:02d}'
    original = (m.HDL / m.PARSER).read_text()
    assert all(original.count(old) == 1 for old, _ in edits), name
    rtl = m.stage(scratch / 'mutation', tag, edits)
    obj = scratch / 'mutation' / ('obj_' + tag)
    cmd = ['verilator', *m.VFLAGS, '--Mdir', str(obj), '-CFLAGS', f'-std=c++17 -O2 -I{m.HERE} -Wall -Wextra', *[str(rtl / s) for s in m.RTL_SOURCES], str(m.HERE / 'sim_main.cpp'), '-o', 'Vreview']
    rc = run(tag + '-build', cmd)
    if rc: return {'name': name, 'result': 'build failed', 'rc': rc}
    rc = run(tag, [str(obj / 'Vreview')])
    output = (logs / (tag + '.log')).read_text()
    failed = [l for l in output.splitlines() if l.startswith('FAIL ')]
    missed = [s for s in breaks if not any(s in l for l in failed)]
    verdict = m.verdict(rc, output)
    ok = (verdict == ('caught' if edits else 'pass')) and not missed
    return {'name': name, 'result': 'PASS' if ok else 'FAIL', 'harness_rc': rc, 'verdict': verdict, 'named_checks': len(breaks), 'missed': missed}

def campaign():
    tasks = [(0, 'unmutated positive control', [], ())] + [(i, *row) for i, row in enumerate(m.MUTATIONS, 1)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
        results = list(pool.map(mutant, tasks))
    (logs / 'mutations.json').write_text(json.dumps(results, indent=2) + '\n')
    return int(any(r['result'] != 'PASS' for r in results))

def focused():
    return run('parser', ['make', '-j16', '-C', str(src / 'tb/verilator/parser'), 'run'])

def static_gates():
    return run('docs-contract-lint', ['make', '-j16', 'docs', 'contract', 'lint'])

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futures = {n: pool.submit(f) for n, f in [('parser', focused), ('mutations', campaign), ('docs-contract-lint', static_gates)]}
    results = {n: f.result() for n, f in futures.items()}
(logs / 'summary.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results))
sys.exit(int(any(results.values())))
