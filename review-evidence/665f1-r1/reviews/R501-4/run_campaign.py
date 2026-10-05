#!/usr/bin/env python3
"""Run the saved-state checks and mutations concurrently, with joined workers.

Usage: python3 run_campaign.py CHECKOUT [--jobs 8]
All disposable files are beneath this packet's scratch directory.
"""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import sys
import traceback

PACKET = Path(__file__).resolve().parent

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('checkout', type=Path)
    ap.add_argument('--jobs', type=int, default=8)
    args = ap.parse_args()
    root = args.checkout.resolve()
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(root / 'sw/firmware/ctrl_nvm/test'))
    import test_ctrl_nvm as gate
    import nvm_rv32
    import nvm_mutants
    scratch = PACKET / 'scratch/campaign'
    receipts = PACKET / 'receipts/campaign'
    receipts.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    inputs = {}
    configs = sorted((root / 'configs').glob('endstation_*.yaml'))
    # Shape generation is inexpensive; read immutable inputs before workers start.
    for cfg in configs:
        inputs[cfg.stem] = gate.shape_inputs(cfg, scratch / 'inputs' / cfg.stem)
    cc = nvm_rv32.compiler()
    if cc is None:
        raise RuntimeError('RV32 compiler required')
    def run_task(name, mutant=None):
        out = []
        rc = 1
        try:
            stem = name if mutant is None else mutant.shape or gate.SELF_TEST_SHAPE
            work = scratch / name
            tree = gate.TREE
            if mutant:
                tree = work / 'tree'
                nvm_mutants.plant(mutant, tree)
            b = gate.bench_for(inputs[stem], work, tree)
            names = list(mutant.kills) if mutant else list(gate.CHECKS)
            result = gate.grade(b, names)
            out.append('SHAPE ' + stem + ' CLOCK ' + str(b.clock_hz))
            for check, findings in result.items():
                out.append(json.dumps({'check': check, 'findings': findings}))
            if mutant:
                survivors = nvm_mutants.survivors(mutant, result)
                rc = int(bool(survivors))
                out.append('MUTANT ' + name + ' ' + ('SURVIVED' if rc else 'CAUGHT'))
            else:
                findings, sizes = nvm_rv32.build(tree, work / 'rv32', work / 'store/gen', cc)
                out.append('RV32 ' + json.dumps({'clock_hz': b.clock_hz, 'sizes': sizes,
                                                'findings': findings}, sort_keys=True))
                out.append('CALL_MAX ' + json.dumps(b.call_max, sort_keys=True))
                out.append('RUNS ' + str(b.runs + (b.vector.runs if b.vector else 0)))
                rc = int(bool(findings or any(result.values())))
        except Exception:
            out.append(traceback.format_exc())
            rc = 2
        (receipts / (name + '.log')).write_text('\n'.join(out) + '\n')
        (receipts / (name + '.rc')).write_text(str(rc) + '\n')
        print(name, rc, flush=True)
        return rc
    tasks = [(c.stem, None) for c in configs] + [(m.name, m) for m in nvm_mutants.MUTANTS]
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(16, max(1,args.jobs))) as pool:
        results = list(pool.map(lambda t: run_task(*t), tasks))
    unnamed = nvm_mutants.unnamed_checks(list(gate.CHECKS))
    summary = {'head': 'd763fce6f3e48fa9c468aaa835653befb8382d06', 'shapes': len(configs),
               'checks': len(gate.CHECKS), 'mutants': len(nvm_mutants.MUTANTS),
               'unnamed_checks': unnamed, 'nonzero_tasks': sum(bool(x) for x in results)}
    (receipts / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary), flush=True)
    return int(bool(unnamed or any(results)))

if __name__ == '__main__':
    sys.exit(main())
