#!/usr/bin/env python3
"""Collect explicit results from the already built, unmodified main suites."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import os
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
os.environ['TMPDIR'] = str(packet / 'scratch')
sys.path.insert(0, str(root / 'sw/firmware/ctrl_nvm/test'))
import nvm_bench

trees = sorted((packet / 'scratch').glob('ctrl-nvm.*/shapes'))
assert len(trees) == 1, 'retain exactly one run_checks store build for collection'
executables = sorted(trees[0].glob('*/suite/nvm_suite'))
assert len(executables) == 5, 'all five unmodified main suites must already be built'

def collect(exe):
    shape = exe.parents[1]
    passed, log = nvm_bench.run_suite(exe, shape / 'fixture')
    return (shape.name, hashlib.sha256(exe.read_bytes()).hexdigest(), passed, log)

ok = True
with ThreadPoolExecutor(max_workers=2) as pool:
    for shape, digest, passed, log in pool.map(collect, executables):
        print('UNMODIFIED_MAIN_SUITE', shape, 'sha256', digest, 'PASS' if passed else 'FAIL', flush=True)
        print(log, flush=True)
        ok &= passed
print('FIVE_MAIN_SUITES', 'PASS' if ok else 'FAIL', flush=True)
raise SystemExit(0 if ok else 1)
