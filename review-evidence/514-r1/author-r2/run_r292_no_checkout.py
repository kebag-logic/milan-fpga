"""Run R292's unmodified mutation definitions using script copies, no checkout.

The original runner creates a shared clone. This adapter imports the exact
MUTANTS table and uses byte copies of HEAD's scripts instead. The checker runs
from the assigned repository, as in R293's runner, for its graft preflight.
"""
import json
import runpy
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SCRIPT, SRC, SCRATCH, REPO, OUT = (Path(arg).resolve() for arg in sys.argv[1:6])
MUTANTS = runpy.run_path(str(SCRIPT))['MUTANTS']
SCRATCH.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

def run(item):
    name, (filename, before, after) = item
    work = SCRATCH / name
    shutil.copytree(SRC, work)
    path = work / Path(filename).name
    data = path.read_text(encoding='utf-8')
    assert data.count(before) == 1, name
    path.write_text(data.replace(before, after), encoding='utf-8')
    log = OUT / (name + '.log')
    with log.open('w') as stream:
        result = subprocess.run([sys.executable, '-B', str(work / 'check_merge_containment.py'), '--selftest'],
                                cwd=REPO, stdout=stream, stderr=subprocess.STDOUT, timeout=1800)
    lines = log.read_text().splitlines()
    fails = [line.strip() for line in lines if line.lstrip().startswith('FAIL')]
    status = 'KILLED' if result.returncode or fails else 'SURVIVED'
    row = dict(mutant=name, status=status, rc=result.returncode, failing_count=len(fails), failing_cases=fails)
    print(name, status, 'rc=' + str(result.returncode), 'fails=' + str(len(fails)), flush=True)
    return row

with ThreadPoolExecutor(4) as pool:
    rows = list(pool.map(run, MUTANTS.items()))
(OUT / 'mutants.json').write_text(json.dumps(rows, indent=2) + '\n')
