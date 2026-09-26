#!/usr/bin/env python3
"""Run the docs-check job's `run:` steps from .github/workflows/docs.yml.

Each step's script is taken verbatim from the workflow at the checked-out
head and executed with `bash -e -o pipefail` in the repository root, in step
order, one at a time. Steps that install software, use actions, or are
outside this review's authority are listed in SKIP with the reason and are
not executed. Step 8 (em-dash) is judged against an explicit base commit via
EVENT_NAME=push / PUSH_BEFORE_SHA, since there is no event payload locally.

Usage: run_docs_check.py <repo> <outdir> <em-dash-base-sha>
Environment: PYTHON_BIN_DIR (directory whose python3 carries the pinned doc
deps), SDK_BIN (pinned RV32 SDK bin, for the --require-rv32 builder step).
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import yaml

SKIP = {
    1: 'installs pyslang via pip; not available offline in this review',
    6: 'installs apt/pip packages; wavedrom supplied by the pinned doc venv',
    17: 'submodule fetch; required gitlinks already checked out and verified',
    20: 'downloads and installs sv2v; a local sv2v is used instead',
    23: 'downloads the RV32 SDK; the pinned SDK already installed is used',
    42: 'act_ci --selftest is outside this reviewer\'s authority',
}

repo, out, base = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
out.mkdir(parents=True, exist_ok=True)
steps = yaml.safe_load((repo / '.github/workflows/docs.yml').read_text())['jobs']['docs-check']['steps']
env = os.environ.copy()
env['PATH'] = os.environ['PYTHON_BIN_DIR'] + ':' + env['PATH']
env.update(EVENT_NAME='push', PUSH_BEFORE_SHA=base, RUNNER_TEMP=str(out / 'runner-temp'))
(out / 'runner-temp').mkdir(exist_ok=True)
results = []
for i, step in enumerate(steps):
    name = step.get('name') or step.get('uses')
    if 'run' not in step:
        results.append(dict(step=i, name=name, status='action-not-run'))
        continue
    if i in SKIP:
        results.append(dict(step=i, name=name, status='skipped', reason=SKIP[i]))
        continue
    script = step['run']
    step_env = dict(env)
    if i == 24:  # compiler-absent controls: no RV32 compiler on PATH
        step_env['PATH'] = ':'.join(p for p in env['PATH'].split(':') if p != os.environ['SDK_BIN'])
    if i == 25:
        step_env['PATH'] = os.environ['SDK_BIN'] + ':' + env['PATH']
        script = script.replace('python3 -m pip install --quiet pyyaml\n', '')
    if i == 3:
        results.append(dict(step=i, name=name, status='skipped', reason='pip install pyyaml; already present'))
        continue
    if i == 5:
        results.append(dict(step=i, name=name, status='skipped', reason='pip install of pinned renderer; pinned versions present in doc venv'))
        continue
    log = out / f'step-{i:02d}.log'
    t = time.time()
    with log.open('w') as f:
        f.write(f'# step {i}: {name}\n# script:\n{script}\n# output:\n')
        f.flush()
        rc = subprocess.run(['bash', '-e', '-o', 'pipefail', '-c', script], cwd=repo, env=step_env,
                            stdout=f, stderr=subprocess.STDOUT).returncode
    results.append(dict(step=i, name=name, status='rc', rc=rc, seconds=round(time.time() - t, 1), log=log.name))
    print(f'step {i:02d} rc={rc} {name}', flush=True)
(out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
bad = [r for r in results if r.get('status') == 'rc' and r['rc'] != 0]
print('FAILED STEPS:', [r['step'] for r in bad] or 'none')
sys.exit(1 if bad else 0)
