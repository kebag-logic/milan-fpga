#!/usr/bin/env python3
"""Focused platform review. Run from the exact-head checkout; outputs stay beside this script."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

PACKET = Path(__file__).resolve().parent
ROOT = Path.cwd()
SCRATCH = PACKET / 'scratch'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['TMPDIR'] = str(SCRATCH)
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'sw/firmware/ctrl/test'))

def child(mode, jobs):
    import ctrl_build as cb
    import plat_arms
    import fw_gtest
    cb.stack_pin()
    out = SCRATCH / mode
    out.mkdir(parents=True, exist_ok=True)
    tree = cb.Tree(cb.CTRL, out / 'build', out / 'reuse', fw_gtest.Build(jobs=jobs, coverage=(mode == 'platform')))
    if mode == 'platform':
        results = plat_arms.coverage_arms(tree)
        for r in results:
            print(r.log, flush=True)
        return max(r.rc for r in results)
    if mode == 'rv32':
        r = plat_arms.arm_platrv32(tree, True)
        print(r.log)
        return r.rc
    if mode == 'trace':
        r = plat_arms.arm_plattrace(tree)
        print(r.log)
        return r.rc
    if mode == 'mutants':
        import ctrl_mutants as cm
        import plat_mutants
        selected = plat_mutants.mutants(cm.Mutant)
        assert len(selected) == 37
        # Retain the complete registry for unnamed_tests(); select only this campaign's plants.
        cm.sliced = lambda part: selected
        print('Selected 37 platform mutants; full named-test inventory retained.', flush=True)
        return int(cm.campaign(out / 'mutants', tree.reuse, jobs))
    raise ValueError(mode)

def launch(mode):
    log = PACKET / (mode + '.log')
    argv = [sys.executable, '-B', str(Path(__file__).resolve()), '--mode', mode, '--jobs', '4']
    with log.open('w') as sink:
        sink.write('COMMAND: python3 -B focused.py --mode ' + mode + ' --jobs 4\n')
        sink.flush()
        result = subprocess.run(argv, stdout=sink, stderr=subprocess.STDOUT)
    (PACKET / (mode + '.rc')).write_text(str(result.returncode) + '\n')
    print(mode, 'rc', result.returncode, flush=True)
    return result.returncode

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--mode', choices=['platform', 'mutants', 'trace', 'rv32'])
    p.add_argument('--jobs', type=int, default=4)
    a = p.parse_args()
    SCRATCH.mkdir(parents=True, exist_ok=True)
    if a.mode:
        raise SystemExit(child(a.mode, min(4, a.jobs)))
    with ThreadPoolExecutor(max_workers=4) as pool:
        raise SystemExit(max(pool.map(launch, ['platform', 'mutants', 'trace', 'rv32'])))
