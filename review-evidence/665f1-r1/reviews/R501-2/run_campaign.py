#!/usr/bin/env python3
"""Reproduce focused source and mutation checks; disposable files stay in scratch."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys


def worker(repo, packet, label):
    sys.path.insert(0, str(repo / 'sw/firmware/ctrl_nvm/test'))
    import test_ctrl_nvm as suite
    import nvm_bench
    import nvm_mutants
    work = packet / 'scratch' / label
    work.mkdir(parents=True, exist_ok=True)
    original = nvm_bench.Bench.run

    def recorded(self, *args):
        print('RUN', json.dumps(list(args)).replace(str(packet), '<packet>'), flush=True)
        result = original(self, *args)
        print(result.out, end='', flush=True)
        return result

    nvm_bench.Bench.run = recorded
    if label.startswith('shape-'):
        cfg = repo / 'configs' / (label.removeprefix('shape-') + '.yaml')
        args = argparse.Namespace(check=None, require_rv32=True)
        found, _ = suite.run_shape(cfg, work, args)
        print('RESULT', json.dumps(found), flush=True)
        return bool(found)
    mutant = next(m for m in nvm_mutants.MUTANTS if m.name == label)
    cfg = repo / 'configs' / (suite.SELF_TEST_SHAPE + '.yaml')
    inputs = suite.shape_inputs(cfg, work)
    nvm_mutants.plant(mutant, work / 'tree')
    bench = suite.bench_for(inputs, work, work / 'tree')
    result = suite.grade(bench, list(mutant.kills))
    alive = nvm_mutants.survivors(mutant, result)
    print('MUTANT', label, 'GRADES', json.dumps(result), 'SURVIVORS', json.dumps(alive), flush=True)
    return bool(alive)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, default=Path.cwd())
    ap.add_argument('--packet', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--jobs', type=int, default=8)
    ap.add_argument('--worker')
    args = ap.parse_args()
    repo, packet = args.repo.resolve(), args.packet.resolve()
    os.environ['TMPDIR'] = str(packet / 'scratch')
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    sys.dont_write_bytecode = True
    if args.worker:
        return worker(repo, packet, args.worker)
    assert 1 <= args.jobs <= 16
    sys.path.insert(0, str(repo / 'sw/firmware/ctrl_nvm/test'))
    import nvm_mutants
    import test_ctrl_nvm as suite
    assert not nvm_mutants.unnamed_checks(list(suite.CHECKS))
    labels = ['shape-' + p.stem for p in sorted((repo / 'configs').glob('endstation_*.yaml'))]
    labels += [m.name for m in nvm_mutants.MUTANTS]
    receipt = packet / 'receipts' / 'campaign'
    receipt.mkdir(parents=True, exist_ok=True)

    def run(label):
        command = [sys.executable, str(Path(__file__).resolve()), '--repo', str(repo),
                   '--packet', str(packet), '--worker', label]
        with (receipt / (label + '.log')).open('w') as log:
            try:
                rc = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                                    timeout=540, check=False).returncode
            except subprocess.TimeoutExpired:
                rc = 124
        (receipt / (label + '.rc')).write_text(str(rc) + '\n')
        return label, rc

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for future in concurrent.futures.as_completed([pool.submit(run, label) for label in labels]):
            label, rc = future.result()
            results[label] = rc
            print(label, 'rc=' + str(rc), flush=True)
    (receipt / 'summary.json').write_text(json.dumps(results, indent=2, sort_keys=True) + '\n')
    return int(any(results.values()))


if __name__ == '__main__':
    sys.exit(main())
