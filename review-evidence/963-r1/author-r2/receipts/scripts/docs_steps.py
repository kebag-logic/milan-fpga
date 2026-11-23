#!/usr/bin/env python3
"""docs_steps.py CLONE OUT JOB/ID...: the named gate steps of the docs workflow, each read from the clone's own
.github/workflows/docs.yml and run with bash -e in the clean clone, one log and rc a step, never piped, in the
environment the round-1 runner (docs_wf.py) gave every step: a push event from the source base dd163e41. The
docs-check-no-git step deletes .git, so it runs in a copy of the clone. Writes summary.txt and tree-after.txt."""
import os
import subprocess
import sys
from pathlib import Path

import yaml

clone, out, wanted = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3:]
out.mkdir(parents=True, exist_ok=True)
wf = yaml.safe_load((clone / '.github/workflows/docs.yml').read_text())
env = dict(os.environ, CI='true', GITHUB_WORKSPACE=str(clone), RUNNER_TEMP=str(out / 'runner_temp'),
           GITHUB_SHA=subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=clone, capture_output=True,
                                     text=True).stdout.strip(),
           GITHUB_BASE_REF='dev-soft-core', GITHUB_EVENT_NAME='push', EVENT_NAME='push',
           PUSH_BEFORE_SHA='dd163e41438acb86e0c4d4e76df90f3f91ace1c0', CI_CAMPAIGN_JOBS='4', CI_JOBS='4',
           GITHUB_ENV=str(out / 'github_env'), GITHUB_OUTPUT=str(out / 'github_output'),
           GITHUB_PATH=str(out / 'github_path'))
(out / 'runner_temp').mkdir(exist_ok=True)
for f in ('github_env', 'github_output', 'github_path'):
    (out / f).touch()
steps = {f"{job}/{s.get('id', '-')}": s for job in wf['jobs'] for s in wf['jobs'][job].get('steps', []) if 'run' in s}
missing = [w for w in wanted if w not in steps]
if missing:
    sys.exit(f'no such step: {missing}')
summary = []
for name in wanted:
    step = steps[name]
    job, sid = name.split('/')
    if job == 'docs-check-no-git':
        work = out / 'nogit'
        subprocess.run(['rm', '-rf', str(work)], check=True)
        subprocess.run(['cp', '-a', str(clone), str(work)], check=True)
    else:
        work = clone
    e = dict(env)
    for k, v in (step.get('env') or {}).items():
        if isinstance(v, str) and '${{' not in v:
            e[k] = v
    script = out / f'{job}__{sid}.sh'
    script.write_text(step['run'])
    with open(out / f'{job}__{sid}.log', 'w') as log:
        rc = subprocess.run(['bash', '-e', str(script)], cwd=work, env=e, stdout=log, stderr=subprocess.STDOUT,
                            stdin=subprocess.DEVNULL).returncode
    summary.append(f'{name}\trc={rc}\t{step.get("name")}')
    print(summary[-1], flush=True)
(out / 'summary.txt').write_text('\n'.join(summary) + '\n')
(out / 'tree-after.txt').write_text(subprocess.run(['git', 'status', '--porcelain'], cwd=clone, capture_output=True,
                                                   text=True).stdout)
print(f'{sum("rc=0" not in s for s in summary)} of {len(summary)} steps failed', flush=True)
