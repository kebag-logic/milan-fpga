#!/usr/bin/env python3
"""Run the existing budget checks and every existing mutation with bounded local concurrency."""
import argparse
import concurrent.futures
import contextlib
import io
import json
import os
import sys
from pathlib import Path

def worker(task):
    repo, packet, name = task
    sys.path.insert(0, str(Path(repo) / 'tb/verilator/ctrl_service_budget'))
    import selftest
    import grade
    text = io.StringIO()
    with contextlib.redirect_stdout(text), contextlib.redirect_stderr(text):
        if name is None:
            checks = selftest.checks()
            failed = [(n, detail) for n, ok, detail in checks if not ok]
            for n, ok, detail in checks:
                print(('PASS: ' if ok else 'FAIL: ') + n + (': ' + detail if not ok else ''))
            ok = not failed
            number = 'baseline'
        else:
            with selftest.mutated(name):
                try:
                    failed = [(n, detail) for n, ok, detail in selftest.checks() if not ok]
                except (grade.Refusal, KeyError, ValueError, IndexError, TypeError, RuntimeError) as error:
                    failed = [(f'refused: {error}', '')]
            ok = bool(failed)
            number = str(list(selftest.selftest_mutants.MUTANTS).index(name)).zfill(3)
        print('BASELINE' if name is None else 'MUTANT', name, 'PASS' if ok else 'FAIL')
        for row in failed:
            print(repr(row))
    log = Path(packet) / 'scratch/budget-raw' / (number + '.log')
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(text.getvalue())
    return dict(name=name or 'baseline', passed=ok, failed_checks=failed,
                raw_receipt=str(Path('scratch/budget-raw') / log.name))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo', type=Path)
    ap.add_argument('packet', type=Path)
    ap.add_argument('--jobs', type=int, default=16)
    args = ap.parse_args()
    assert 1 <= args.jobs <= 16
    repo, packet = args.repo.resolve(), args.packet.resolve()
    os.environ['TMPDIR'] = str(packet / 'scratch')
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    sys.path.insert(0, str(repo / 'tb/verilator/ctrl_service_budget'))
    import model_counts
    import selftest_mutants
    assert model_counts.main() == 0
    names = [None, *selftest_mutants.MUTANTS]
    print(f'Running baseline and {len(names)-1} existing mutations with {args.jobs} local workers', flush=True)
    results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(worker, (str(repo), str(packet), name)) for name in names]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            print(('PASS ' if result['passed'] else 'FAIL ') + result['name'], flush=True)
    results.sort(key=lambda r: r['name'])
    (packet / 'budget-campaign.json').write_text(json.dumps(results, indent=2) + '\n')
    failed = sum(not r['passed'] for r in results)
    print(f'budget campaign: {len(results)} completed, {failed} failures', flush=True)
    return int(bool(failed))

if __name__ == '__main__':
    raise SystemExit(main())
