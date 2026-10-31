"""(#814, the #780 lane's replica, paths only) rtl_fast_steps.py <out-dir> <repo> <head> [job ...]: the rtl-fast workflow's step bodies, run literally.

A native replica of .github/workflows/rtl-fast.yml for a head that is not pushed (the act runner rechecks the
remote head, so it cannot run an unpushed candidate). Every job in the fast gate's `needs:` list runs, one job at
a time, in the clone <repo>, as a pull_request event against `dev` replayed the way the act runner replays it
(ACT=true, the base read from refs/remotes/origin/dev, which the clone takes from the lane's own dev at the live
remote tip). Each selected step's `run:` body is written out unchanged and executed with `bash -e` from the
step's working directory, with the workflow, job and step `env:`; lines a step appends to $GITHUB_ENV and
$GITHUB_PATH are carried into the job's later steps, as the runner does.

Each job starts from a fresh CPython 3.12.3 virtual environment holding PyYAML 6.0.2 (the constraint pin), as
the hosted image's python3 does; the job's own pip steps install into it.

Not run, by rule (each recorded): `uses:` steps (checkout, caches, artifact upload); the package resolve and
tool-build-from-source steps (the pinned tools are already built here: Verilator 5.050, Yosys 0.66, sv2v
v0.0.12, GoogleTest from the host); the `sudo` tool-install steps; and the runtime-evidence record step (it
reads the hosted runner's job context). Two textual substitutions, each recorded per step: `/opt/verilator/bin`,
where the hosted job installs its pinned Verilator build, names a directory holding the pinned 5.050 here; and
in "Install GoogleTest and GoogleMock and print the versions" the `sudo apt-get install` and `dpkg-query` lines
are dropped (the host's GoogleTest is used), so its pip install runs as written.
The aggregate `rtl-fast` job's verdict is computed from the job results with the workflow's own rule
(every needed job succeeded, or was skipped by the change classifier).
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import yaml

OUT, REPO, HEAD = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
ONLY = sys.argv[4:]
SCR = Path('$VALIDATION_STORAGE/scratch/814-a703d')
CI312 = Path('$VALIDATION_STORAGE/scratch/a662/ci312/bin')
CPY312 = '$VALIDATION_TOOLS/uvpy/cpython-3.12.3-linux-x86_64-gnu/bin/python3'
OPT_VERILATOR = Path('$VALIDATION_TOOLS/pinned-verilator-5.050')
TOOLS = ['$VALIDATION_STORAGE/scratch/a662/make43/bin', '$VALIDATION_TOOLS/sv2v-v0.0.12']
HOME = Path(os.environ.get('RTLFAST_HOME', SCR / 'sdk'))  # $HOME/br-milan-rv32/host: the pinned RV32 SDK installed there by scripts/ci_rv32_sdk.py --archive
SKIP_NAMES = {
    'Build Verilator from source on cache miss': 'tool build on cache miss; the pinned 5.050 is built here',
    'Build Yosys from source on cache miss': 'tool build on cache miss; Yosys 0.66 is installed here',
    'Install the pinned Yosys and prove the version': 'sudo ln into /usr/local/bin; Yosys 0.66 is on PATH here',
    'Install the pinned sv2v release': 'downloads into /usr/local/bin; sv2v v0.0.12 is on PATH here',
    'Record actual job execution': 'reads the hosted runner job context',
}
SKIP_PREFIX = ('Resolve exact package downloads',)

workflow = yaml.safe_load((REPO / '.github/workflows/rtl-fast.yml').read_text())
assert subprocess.run(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], capture_output=True, text=True,
                      check=True).stdout.strip() == HEAD, 'clone is not at the head'
NEEDED = workflow['jobs']['rtl-fast']['needs']
OUT.mkdir(parents=True, exist_ok=True)
for sub in ('steps', 'logs', 'runner-temp'):
    (OUT / sub).mkdir(exist_ok=True)


def expand(value, outputs):
    value = str(value)
    subs = {
        '${{ github.workspace }}': str(REPO),
        '${{ github.event_name }}': 'pull_request',
        '${{ github.event.pull_request.base.ref }}': 'dev',
        '${{ github.event.pull_request.head.sha }}': HEAD,
        '${{ github.event.before }}': '',
        '${{ github.sha }}': HEAD,
    }
    for key, val in subs.items():
        value = value.replace(key, val)
    if '${{' in value:
        raise SystemExit(f'unexpanded expression: {value!r}')
    return value


def run_job(job):
    spec = workflow['jobs'][job]
    temp = OUT / 'runner-temp' / job
    temp.mkdir(exist_ok=True)
    genv, gpath, gout = temp / 'github_env', temp / 'github_path', temp / 'github_output'
    for f in (genv, gpath, gout):
        f.write_text('')
    base = {k: v for k, v in os.environ.items() if k not in ('VIRTUAL_ENV', 'MAKEFLAGS', 'PYTHONPATH')}
    venv = temp / 'venv'
    subprocess.run([CPY312, '-m', 'venv', str(venv)], check=True)
    subprocess.run([str(venv / 'bin/python3'), '-m', 'pip', 'install', '--quiet', '--disable-pip-version-check',
                    'pyyaml'], check=True, env={**base, 'PIP_CONSTRAINT': str(REPO / 'ci/constraints-ci.txt')})
    base['PATH'] = os.pathsep.join([str(venv / 'bin'), *TOOLS, base['PATH']])
    base.update(HOME=str(HOME), CI='true', GITHUB_ACTIONS='true', ACT='true', GITHUB_WORKSPACE=str(REPO),
                GITHUB_SHA=HEAD, GITHUB_EVENT_NAME='pull_request', RUNNER_TEMP=str(temp),
                GITHUB_ENV=str(genv), GITHUB_PATH=str(gpath), GITHUB_OUTPUT=str(gout))
    for key, value in (workflow.get('env') or {}).items():
        base[key] = expand(value, None)
    for key, value in (spec.get('env') or {}).items():
        base[key] = expand(value, None)
    results = []
    job_rc = 0
    for index, step in enumerate(spec['steps']):
        name = step.get('name') or step.get('uses') or f'step {index}'
        if 'run' not in step:
            results.append(dict(step=index, name=name, skipped='uses: ' + str(step.get('uses'))))
            continue
        why = SKIP_NAMES.get(name) or ('package resolve for the skipped install' if name.startswith(SKIP_PREFIX) else None)
        if why:
            results.append(dict(step=index, name=name, skipped=why))
            continue
        if job_rc:
            results.append(dict(step=index, name=name, skipped='an earlier step failed'))
            continue
        env = dict(base)
        for line in genv.read_text().splitlines():
            if '=' in line:
                k, v = line.split('=', 1)
                env[k] = v
        extra_path = [p for p in gpath.read_text().splitlines() if p]
        body = step['run']
        substituted = '/opt/verilator/bin' in body or any('/opt/verilator/bin' in p for p in extra_path)
        body = body.replace('/opt/verilator/bin', str(OPT_VERILATOR))
        dropped = []
        if name == 'Install GoogleTest and GoogleMock and print the versions':
            dropped = [l for l in body.splitlines() if 'sudo apt-get' in l or l.startswith('dpkg-query')]
            body = '\n'.join(l for l in body.splitlines() if l not in dropped) + '\n'
        extra_path = [p.replace('/opt/verilator/bin', str(OPT_VERILATOR)) for p in extra_path]
        env['PATH'] = os.pathsep.join([*reversed(extra_path), env['PATH']])
        for key, value in (step.get('env') or {}).items():
            env[key] = expand(value, None)
        wd = REPO / (step.get('working-directory') or (spec.get('defaults') or {}).get('run', {}).get('working-directory') or '.')
        script = OUT / 'steps' / f'{job}.{index}.sh'
        script.write_text(body)
        log = OUT / 'logs' / f'{job}.{index}.log'
        start = time.time()
        with log.open('w') as handle:
            rc = subprocess.run(['bash', '-e', str(script)], cwd=wd, env=env, stdout=handle,
                                stderr=subprocess.STDOUT).returncode
        seconds = round(time.time() - start, 1)
        data = log.read_bytes()
        results.append(dict(step=index, name=name, rc=rc, seconds=seconds, cwd=str(wd.relative_to(REPO)),
                            opt_verilator_substituted=substituted, dropped_lines=dropped,
                            log=str(log.relative_to(OUT)),
                            log_bytes=len(data), log_sha256=hashlib.sha256(data).hexdigest(),
                            body_sha256=hashlib.sha256(step['run'].encode()).hexdigest()))
        print(f'rc={rc} {seconds:>7}s {job}[{index}] {name}', flush=True)
        job_rc = job_rc or rc
    outputs = dict(line.split('=', 1) for line in gout.read_text().splitlines() if '=' in line)
    return job_rc, results, outputs


receipts = {}
scope = None
for job in ['changes', *[j for j in NEEDED if j != 'changes']]:
    if ONLY and job not in ONLY:
        continue
    cond = str(workflow['jobs'][job].get('if', ''))
    if 'needs.changes.outputs.rtl' in cond and scope is not None and scope != 'true':
        receipts[job] = dict(result='skipped', reason=f'changes rtl={scope}')
        print(f'SKIP {job}: rtl={scope}', flush=True)
        continue
    rc, steps, outputs = run_job(job)
    receipts[job] = dict(result='success' if rc == 0 else 'failure', rc=rc, outputs=outputs, steps=steps)
    if job == 'changes':
        scope = outputs.get('rtl')
    print(f'JOB {job}: {receipts[job]["result"]}', flush=True)

complete = not ONLY
bad = [j for j, r in receipts.items() if r['result'] not in ('success', 'skipped')]
verdict = ('success' if not bad else 'failure') if complete else 'partial'
head_after = subprocess.run(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], capture_output=True, text=True,
                            check=True).stdout.strip()
dirty = subprocess.run(['git', '-C', str(REPO), 'status', '--porcelain', '--untracked-files=no'],
                       capture_output=True, text=True, check=True).stdout
(OUT / 'receipts.json').write_text(json.dumps(dict(head=HEAD, head_after=head_after, tracked_changes=dirty,
                                                   rtl_fast=verdict, failed=bad, jobs=receipts), indent=2) + '\n')
print(f'rtl-fast: {verdict}; failed jobs: {bad or "none"}; head {HEAD}')
sys.exit(1 if bad else 0)
