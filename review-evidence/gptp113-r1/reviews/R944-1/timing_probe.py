#!/usr/bin/env python3
"""Issue #113: isolate inherited host-timing checks at both layouts."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('packet', type=Path)
    ap.add_argument('--jobs', type=int, default=2, choices=(1, 2))
    args = ap.parse_args()
    packet = args.packet.resolve()
    program = '''import importlib.util, pathlib, sys
testfile, root = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("passes", testfile)
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
total = 0
for repeat in range(3):
    trial = root / str(repeat); trial.mkdir(parents=True)
    trees = t.tree(trial)
    bad = t.budget(trees, trial) + t.fail_fast(trees, trial)
    total += bad
    print("repeat", repeat, "failures", bad, flush=True)
print("observed timing failures", total)
'''
    def one(label):
        rel = 'tb/engine_passes_test.py' if label == 'head' else 'tb/verilator/engine/passes_test.py'
        argv = [sys.executable, '-u', '-c', program, str(packet / 'scratch' / label / rel), str(packet / 'scratch' / ('timing-' + label))]
        with (packet / 'receipts' / ('timing-' + label + '.log')).open('w') as log:
            done = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT, timeout=240,
                                  env={**os.environ, 'MAKEFLAGS': '', 'PYTHONDONTWRITEBYTECODE': '1'})
        assert done.returncode == 0, (label, done.returncode)
        return label
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        print('Completed:', ', '.join(pool.map(one, ('base', 'head'))))


if __name__ == '__main__':
    main()
