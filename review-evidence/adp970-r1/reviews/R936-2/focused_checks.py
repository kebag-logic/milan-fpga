#!/usr/bin/env python3
"""Run the ADP and boot suites and the draw fault controls in disposable trees.

Usage: python3 -B focused_checks.py REPOSITORY PACKET
Three independent workers, four compile jobs each; all are joined.
"""
import concurrent.futures
import json
from pathlib import Path
import sys

repo, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
sys.path.insert(0, str(repo / 'sw/firmware/ctrl/test'))
import ctrl_arms
import plat_arms
import ctrl_mutants
import adp_first_mutants
from ctrl_build import Tree, CTRL, STACK
import fw_gtest

logs = packet / 'receipts/focused'
logs.mkdir(parents=True, exist_ok=True)
scratch = packet / 'scratch/focused'
scratch.mkdir(parents=True, exist_ok=True)
arms = {'adp': ctrl_arms.arm_adp,
        'platboot1': lambda t: plat_arms.arm_platboot(t, 1),
        'platboot2': lambda t: plat_arms.arm_platboot(t, 2)}
# The earlier delay/GM controls are covered by the published campaign.
selected = [m for m in adp_first_mutants.MUTANTS if m.name.startswith(('seed-', 'later-', 'link-up-not-',
            'duplicate-', 'disabled-', 'link-up-sample-', 'plat-clock-'))]

def worker(arm):
    build = fw_gtest.Build(jobs=4)
    root = scratch / arm
    root.mkdir(exist_ok=True)
    tree = Tree(CTRL, root / 'baseline', root / 'reuse', build, STACK)
    outcome = arms[arm](tree)
    (logs / f'{arm}-baseline.log').write_text(outcome.log)
    results = [{'arm': arm, 'case': 'baseline', 'rc': outcome.rc, 'pass': outcome.rc == 0}]
    for mutant in selected:
        kills = [k for k in mutant.kills() if k[0] == arm]
        if not kills:
            continue
        src, stack = ctrl_mutants.plant(mutant, root / mutant.name)
        tree = Tree(src, root / 'mutant-build', root / 'reuse', build, stack)
        outcome = arms[arm](tree)
        (logs / f'{arm}-{mutant.name}.log').write_text(outcome.log)
        results.append({'arm': arm, 'case': mutant.name, 'rc': outcome.rc,
                        'pass': all(ctrl_mutants.caught(test, words, outcome) for _, test, words in kills),
                        'required_tests': [test for _, test, _ in kills]})
    return results

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = [item for group in pool.map(worker, arms) for item in group]
(logs / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
for result in results:
    print(json.dumps(result), flush=True)
sys.exit(0 if all(r['pass'] for r in results) else 1)
