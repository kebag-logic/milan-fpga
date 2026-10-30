#!/usr/bin/env python3
"""Run the three new mutations concurrently; preserve complete simulation logs.

The separate dynmap-clean receipt is the unmodified positive control.
Uses the repository campaign's planting, build recipe, and named-check grader.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import os
from pathlib import Path
import sys
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('repo', type=Path)
parser.add_argument('--jobs', type=int, required=True)
parser.add_argument('--verilator', default=os.environ.get(
    'VERILATOR', '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'))
args = parser.parse_args()
packet = Path(__file__).resolve().parent
suite = args.repo.resolve() / 'tb/verilator/milan_dp'
sys.path.insert(0, str(suite))
spec = importlib.util.spec_from_file_location('dynmap_mutants', suite / 'dynmap_mutants.py')
campaign = importlib.util.module_from_spec(spec)
spec.loader.exec_module(campaign)
os.environ['VERILATOR'] = args.verilator
os.environ['VERILATOR_JOBS'] = '5'
os.environ['MAKEFLAGS'] = '-j16'
original_run_leg = campaign.run_leg

def retained_run(leg, exe):
    rc, raw = original_run_leg(leg, exe)
    stem = 'mutant-' + exe.parent.name.removeprefix('obj_')
    (packet / 'logs' / (stem + '.log')).write_text(raw)
    (packet / 'logs' / (stem + '.rc')).write_text(str(rc) + '\n')
    return rc, raw

campaign.run_leg = retained_run
with tempfile.TemporaryDirectory(prefix='volatile-mutants-', dir=packet / 'scratch') as tmp:
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda mutation: campaign.run_mutant(mutation, Path(tmp)),
                                campaign.MUTATIONS[63:66]))
for passed, messages in results:
    print('\n'.join(messages))
assert len(results) == 3 and all(passed for passed, _ in results)
print('PASS: all three new volatile mutants failed their named checks; see dynmap-clean for the positive control')
