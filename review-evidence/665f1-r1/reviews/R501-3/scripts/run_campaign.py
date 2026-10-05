#!/usr/bin/env python3
"""Run the F1 checks and planted controls concurrently in disposable trees.

Usage: python3 scripts/run_campaign.py --repo CHECKOUT --jobs 16
The calling process waits for all workers. No process is detached.
"""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import traceback


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--jobs', type=int, default=16)
    ap.add_argument('--worker', nargs=2)
    args = ap.parse_args()
    packet = Path(__file__).resolve().parents[1]
    scratch = packet / 'scratch' / 'campaign'
    scratch.mkdir(parents=True, exist_ok=True)
    receipts = packet / 'receipts' / 'campaign'
    receipts.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(args.repo / 'sw/firmware/ctrl_nvm/test'))
    import test_ctrl_nvm as gate
    import nvm_bench
    import nvm_mutants

    if args.worker:
        kind, name = args.worker
        work = scratch / name
        if work.exists():
            shutil.rmtree(work)
        work.mkdir(parents=True, exist_ok=True)
        log = receipts / (name + '.runs.jsonl')
        log.unlink(missing_ok=True)
        oldrun = nvm_bench.Bench.run
        def traced(self, *command):
            result = oldrun(self, *command)
            row = {'args': list(command), 'stdout': result.out}
            raw = json.dumps(row).replace(str(packet), '<packet>').replace(str(args.repo), '<repo>')
            with log.open('a') as stream:
                stream.write(raw + '\n')
            return result
        nvm_bench.Bench.run = traced
        if kind == 'shape':
            ns = argparse.Namespace(check=None, require_rv32=True)
            findings, _ = gate.run_shape(args.repo / 'configs' / (name + '.yaml'), work, ns)
        else:
            inputs = nvm_bench.shape_inputs(args.repo / 'configs/endstation_ax7101_1x1_tdm8.yaml', work)
            mutant = next(m for m in nvm_mutants.MUTANTS if m.name == name)
            tree = work / 'tree'
            nvm_mutants.plant(mutant, tree)
            bench = gate.bench_for(inputs, work, tree)
            result = gate.grade(bench, list(mutant.kills))
            findings = nvm_mutants.survivors(mutant, result)
            print(json.dumps({'mutant': name, 'named_checks': list(mutant.kills),
                              'findings_by_check': result, 'survivors': findings}, indent=2))
        print(json.dumps({'task': name, 'unexpected_findings': findings}))
        return int(bool(findings))

    assert 1 <= args.jobs <= 16
    assert not nvm_mutants.unnamed_checks(list(gate.CHECKS))
    tasks = [('shape', p.stem) for p in sorted((args.repo / 'configs').glob('endstation_*.yaml'))]
    tasks += [('mutant', m.name) for m in nvm_mutants.MUTANTS]
    env = dict(os.environ, TMPDIR=str(packet / 'scratch'), PYTHONDONTWRITEBYTECODE='1')
    def run(task):
        kind, name = task
        cmd = [sys.executable, str(Path(__file__).resolve()), '--repo', str(args.repo), '--worker', kind, name]
        with (receipts / (name + '.log')).open('w') as stream:
            result = subprocess.run(cmd, stdout=stream, stderr=subprocess.STDOUT, env=env, timeout=540)
        (receipts / (name + '.rc')).write_text(str(result.returncode) + '\n')
        print(kind, name, 'rc', result.returncode, flush=True)
        return result.returncode
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(run, tasks))
    print(json.dumps({'tasks': len(tasks), 'shapes': sum(k == 'shape' for k, n in tasks),
                      'controls': len(nvm_mutants.MUTANTS), 'failures': sum(rc != 0 for rc in results)}))
    return int(any(results))


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
