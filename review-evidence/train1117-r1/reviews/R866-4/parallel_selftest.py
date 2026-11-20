#!/usr/bin/env python3
"""Run the unchanged budget self-test checks and all mutations in isolated processes."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

P = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--jobs', type=int, default=12)
parser.add_argument('--worker', type=int)
args = parser.parse_args()
assert 1 <= args.jobs <= 16
sys.path.insert(0, str(Path.cwd() / 'tb/verilator/ctrl_service_budget'))
import selftest as st

names = list(st.selftest_mutants.MUTANTS)
if args.worker is not None:
    tmp = P / 'scratch/selftest' / str(args.worker)
    tmp.mkdir(parents=True, exist_ok=True)
    os.environ['TMPDIR'] = str(tmp)
    tempfile.tempdir = str(tmp)
    selected = names[args.worker::args.jobs]
    print('Assigned mutations:', json.dumps(selected), flush=True)
    st.selftest_mutants.MUTANTS = {name: st.selftest_mutants.MUTANTS[name] for name in selected}
    raise SystemExit(st.main([]))

out = P / 'selftest-workers'
out.mkdir(exist_ok=True)
def worker(i):
    with (out / f'{i:02}.log').open('w') as log:
        result = subprocess.run([sys.executable, '-B', str(Path(__file__).resolve()),
                                 '--jobs', str(args.jobs), '--worker', str(i)],
                                stdout=log, stderr=subprocess.STDOUT)
    (out / f'{i:02}.rc').write_text(str(result.returncode) + '\n')
    text = (out / f'{i:02}.log').read_text()
    caught = sum(line.startswith('MUTANT caught:') for line in text.splitlines())
    expected = len(names[i::args.jobs])
    assert result.returncode == 0 and caught == expected, (i, result.returncode, caught, expected)
    print(f'Worker {i}: baseline checks PASS; {caught}/{expected} mutations caught', flush=True)
    return caught
with ThreadPoolExecutor(max_workers=args.jobs) as pool:
    counts = list(pool.map(worker, range(args.jobs)))
assert sum(counts) == len(names) == 295
print('Full unchanged self-test: baseline checks passed in every worker; 295/295 mutations caught; 0 failures')
