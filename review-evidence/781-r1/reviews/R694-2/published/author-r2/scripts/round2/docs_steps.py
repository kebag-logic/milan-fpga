"""docs_steps.py <out-dir> <repo>: run the docs workflow's gate step bodies literally.
Adapted for #781 (paths are this lane's) from the #774 lane's copy of the #632 lane's copy of the #771 lane's replica (same selection and skips); the
repository and the tool directories are this lane's own.

Each selected step's `run:` body is written out unchanged and executed with
`bash -e` (the runner's default shell) from the repository root, GNU Make 4.3
first on PATH, with the job's `env:` and the step's `env:`, and records rc,
seconds, the make version, the interpreter and the log digest.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import yaml

REPO = Path(sys.argv[2])
OUT = Path(sys.argv[1])
CI312 = '$VALIDATION_STORAGE/scratch/781-a671/ci312/bin'
MDVENV = '$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin'
TOOLS = ['$VALIDATION_STORAGE/scratch/781-a671/make43/bin', '$VALIDATION_TOOLS/sv2v-v0.0.12',
         '$VALIDATION_TOOLS/pinned-verilator-5.050']
MARKDOWN_GATES = {'gate_7', 'gate_8', 'gate_9', 'gate_43', 'gate_45'}
SKIP = {
    'gate_42': 'executes the candidate act_ci.py on the host; AGENTS.md section 5 allows the '
               'candidate copy only inside the disposable CI job',
    'docs-check-no-git/ci_step_3': 'its body runs rm -rf .git, which would delete this '
                                   'worktree\'s git link; its two gates run in place below',
}
SELECT = [('wire-accountability', 'ci_step_4'), *[('docs-gates-0', None)],
          ('docs-gates-1', 'gate_25_0'), ('docs-gates-2', 'gate_25_1'),
          ('docs-gates-2', 'gate_41'), ('docs-gates-2', 'gate_42'),
          ('docs-check-no-git', 'ci_step_3')]

workflow = yaml.safe_load((REPO / '.github/workflows/docs.yml').read_text())
base = subprocess.run(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], capture_output=True,
                      text=True, check=True).stdout.strip()
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'steps').mkdir(exist_ok=True)
(OUT / 'logs').mkdir(exist_ok=True)
runner_temp = OUT / 'runner-temp'
runner_temp.mkdir(exist_ok=True)
receipts = []


def steps_for(job, step_id):
    for step in workflow['jobs'][job]['steps']:
        if 'run' not in step:
            continue
        sid = str(step.get('id', ''))
        if step_id is None and sid.startswith('gate_'):
            yield step
        elif step_id is not None and sid == step_id:
            yield step


def environment(job, step, markdown):
    env = dict(os.environ)
    first = MDVENV if markdown else CI312
    env['PATH'] = os.pathsep.join([first, *TOOLS, env['PATH']])
    env.pop('VIRTUAL_ENV', None)
    if step.get('id') in ('gate_25_0', 'gate_25_1'):
        # the builder legs find the verified SDK at $HOME/br-milan-rv32/host
        env['HOME'] = '$VALIDATION_STORAGE/scratch/781-a671/home'
    env['GITHUB_WORKSPACE'] = str(REPO)
    env['RUNNER_TEMP'] = str(runner_temp)
    env['GITHUB_ENV'] = str(runner_temp / 'github_env')
    env['GITHUB_OUTPUT'] = str(runner_temp / 'github_output')
    # the CPU-derived budgets the job writes, capped at this lane's limits
    env.update(CI_BUILD_JOBS='8', CI_TOOL_BUILD_JOBS='8', CI_CAMPAIGN_JOBS='4',
               VERILATOR_JOBS='2', SIM_JOBS='4', MAKEFLAGS='-j1 --no-print-directory',
               PYTHON_CPU_COUNT='4')
    env['VERILATOR'] = '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'
    for key, value in (workflow['jobs'][job].get('env') or {}).items():
        env[key] = str(value).replace('${{ github.workspace }}', str(REPO))
    for key, value in (step.get('env') or {}).items():
        value = str(value)
        value = value.replace('${{ github.event_name }}', 'pull_request')
        value = value.replace('${{ github.event.pull_request.base.ref }}', 'dev')
        value = value.replace('${{ github.event.before }}', '')
        env[key] = value
    return env


ONLY = os.environ.get('DOCS_ONLY')
EXTRA = dict(item.split('=', 1) for item in os.environ.get('DOCS_EXTRA_ENV', '').split() if item)
if ONLY and '/' in ONLY:
    # #781: one named step, JOB/STEP_ID, for a rerun of a step inside an all-gates job
    SELECT = [tuple(ONLY.split('/', 1))]
elif ONLY:
    SELECT = [(job, sid) for job, sid in SELECT if sid == ONLY]
for job, step_id in SELECT:
    for step in steps_for(job, step_id):
        sid = str(step.get('id'))
        key = sid if sid in SKIP else f'{job}/{sid}'
        name = step.get('name', '')
        if key in SKIP or sid in SKIP:
            receipts.append(dict(job=job, id=sid, name=name, rc=None, skipped=SKIP.get(key) or SKIP[sid]))
            print(f'SKIP {job}/{sid} {name}', flush=True)
            continue
        markdown = sid in MARKDOWN_GATES
        script = OUT / 'steps' / f'{job}.{sid}.sh'
        script.write_text(step['run'])
        log = OUT / 'logs' / f'{job}.{sid}.log'
        env = environment(job, step, markdown)
        env.update(EXTRA)
        make = subprocess.run(['make', '--version'], capture_output=True, text=True, env=env).stdout.splitlines()[0]
        python = subprocess.run(['python3', '--version'], capture_output=True, text=True, env=env).stdout.strip()
        start = time.time()
        with log.open('w') as handle:
            rc = subprocess.run(['bash', '-e', str(script)], cwd=REPO, env=env,
                                stdout=handle, stderr=subprocess.STDOUT).returncode
        seconds = round(time.time() - start, 1)
        data = log.read_bytes()
        receipts.append(dict(job=job, id=sid, name=name, rc=rc, seconds=seconds, make=make, home=env['HOME'],
                             python=python, extra_env=EXTRA, interpreter=('md-venv' if markdown else 'ci312'),
                             log=str(log.relative_to(OUT)), log_bytes=len(data),
                             log_sha256=hashlib.sha256(data).hexdigest(),
                             script_sha256=hashlib.sha256(step['run'].encode()).hexdigest()))
        print(f'rc={rc} {seconds:>7}s {job}/{sid} {name} [{make}; {python}]', flush=True)

head_after = subprocess.run(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], capture_output=True,
                            text=True, check=True).stdout.strip()
(OUT / 'receipts.json').write_text(json.dumps(dict(head=base, head_after=head_after,
                                                   steps=receipts), indent=2) + '\n')
failed = [r for r in receipts if r.get('rc') not in (0, None)]
print(f'{len(receipts)} steps, {len(failed)} failed, head {base}')
sys.exit(1 if failed else 0)
