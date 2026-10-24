#!/usr/bin/env python3
"""Execute the seven new planted controls through the repository's own grader."""
import argparse
import concurrent.futures
import importlib.util
import os
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
parser.add_argument('repo', type=Path)
parser.add_argument('--jobs', type=int, required=True, choices=range(1,5))
args = parser.parse_args()
packet = Path(__file__).resolve().parent
repo = args.repo.resolve()
os.environ['TMPDIR'] = str(packet/'scratch')
os.environ['VERILATOR'] = os.environ.get('REVIEW_VERILATOR',os.environ.get('VERILATOR','verilator'))
os.environ['VERILATOR_JOBS'] = '1'
suite = repo/'tb/verilator/capture_coherence'
sys.path.insert(0,str(suite))
spec = importlib.util.spec_from_file_location('review_controls',suite/'mutants.py')
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
work = packet/'scratch/controls'
work.mkdir(exist_ok=True)
made, lines = module.rom_images_result(work)
assert made, lines
units = [u for u in module.arm_units(work) if u.name.startswith('mutant/') and '#773' in u.name]
assert len(units) == 7

def run(pair):
    index, unit = pair
    results, raw = module.observed_unit(unit,work)
    (packet/f'control-{index:02}.json').write_text(raw+'\n')
    passed = all(p for p,_ in results)
    for _, lines in results:
        for line in lines:
            print(line,flush=True)
    (packet/f'control-{index:02}.rc').write_text('0\n' if passed else '1\n')
    return passed

with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
    results = list(pool.map(run,enumerate(units,1)))
print(f'New controls: {sum(results)}/{len(results)} caught by named checks',flush=True)
sys.exit(not all(results))
