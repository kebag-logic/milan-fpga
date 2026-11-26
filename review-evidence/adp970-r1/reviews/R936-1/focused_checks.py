#!/usr/bin/env python3
"""Run focused source-head checks. All generated trees stay in packet/scratch.

Usage: python3 -B focused_checks.py SOURCE_ROOT --jobs 16
"""
import argparse
import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path


def worker(root, packet, task, jobs):
    sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
    import ctrl_build as cb
    import ctrl_arms as ca
    import ctrl_mutants as cm
    import adp_first_mutants as am
    import plat_arms as pa
    import fw_gtest as fw
    from ctrl_reuse import cut_reuse
    work = packet / 'scratch' / task
    work.mkdir(parents=True, exist_ok=True)
    build = fw.Build(jobs=jobs)
    tree = cb.Tree(cb.CTRL, work / 'build', work / 'reuse', build)
    if task.startswith('mutations-') or task == 'walk':
        cut_reuse(tree.reuse)
    arms = {'adp': ca.arm_adp, 'walk': ca.arm_walk,
            'platboot1': lambda t: pa.arm_platboot(t, 1),
            'platboot2': lambda t: pa.arm_platboot(t, 2)}
    if task in arms:
        result = arms[task](tree)
        (packet / (task + '.log')).write_text(result.log)
        (packet / (task + '.rc')).write_text(str(result.rc) + '\n')
        return task, result.rc
    if task == 'fresh-sample':
        original = cb.test_source
        probe = work / 'test_adp_probe.cpp'
        probe.write_text(original('test_adp.cpp').read_text() + (packet / 'fresh_sample_probe.cpp').read_text())
        cb.test_source = lambda n: probe if n == 'test_adp.cpp' else original(n)
        result = ca.arm_adp(tree)
        (packet / 'fresh-sample.log').write_text(result.log)
        (packet / 'fresh-sample.rc').write_text(str(result.rc) + '\n')
        return task, result.rc
    index = int(task.split('-')[-1])
    table = (*am.MUTANTS, next(m for m in cm.MUTANTS if m.name == 'latency-extra-read'))
    records = []
    for m in table[index::4]:
        ctrl, stack = cm.plant(m, work)
        planted = cb.Tree(ctrl, work / 'work/build', work / 'reuse', build, stack)
        kills = []
        for number, (arm, test, words) in enumerate(m.kills()):
            result = arms[arm](planted)
            (packet / f'mutation-{m.name}-{number}.log').write_text(result.log)
            (packet / f'mutation-{m.name}-{number}.rc').write_text(str(result.rc) + '\n')
            kills.append({'arm': arm, 'test': test, 'words': words,
                          'caught': cm.caught(test, words, result)})
        records.append({'name': m.name, 'kills': kills})
    (packet / (task + '.json')).write_text(json.dumps(records, indent=2) + '\n')
    return task, int(any(not k['caught'] for m in records for k in m['kills']))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source', type=Path)
    ap.add_argument('--jobs', type=int, required=True)
    ap.add_argument('--worker')
    ap.add_argument('--retry-mutations', action='store_true')
    args = ap.parse_args()
    packet = Path(__file__).resolve().parent
    if args.worker:
        task, rc = worker(args.source.resolve(), packet, args.worker, args.jobs)
        print(task, rc, flush=True)
        return rc
    assert 4 <= args.jobs <= 16
    summary = []
    groups = [('mutations-0', 'mutations-1')] if args.retry_mutations else [
        ('adp', 'platboot1', 'platboot2', 'fresh-sample'), tuple(f'mutations-{n}' for n in range(4))]
    for tasks in groups:
        def launch(task):
            with (packet / (task + '-driver.log')).open('w') as log:
                r = subprocess.run([sys.executable, '-B', __file__, str(args.source),
                                    '--jobs', str(args.jobs // 4), '--worker', task],
                                   stdout=log, stderr=subprocess.STDOUT, timeout=540)
            print(task, r.returncode, flush=True)
            return {'task': task, 'rc': r.returncode}
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            summary.extend(pool.map(launch, tasks))
    (packet / ('focused-retry-summary.json' if args.retry_mutations else 'focused-summary.json')).write_text(json.dumps(summary, indent=2) + '\n')
    return int(any(r['rc'] != (1 if r['task'] == 'fresh-sample' else 0) for r in summary))


if __name__ == '__main__':
    raise SystemExit(main())
