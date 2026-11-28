"""Run this repository's workflow jobs locally at one head, step for step as the workflow files state them.

Each job runs in its own copy of a clean clone at the head (submodules at their pins), with bash -eo pipefail as
Actions runs a `run:` step, its matrix values substituted, and GITHUB_ENV/GITHUB_OUTPUT/RUNNER_TEMP its own.
Steps that install tools, fetch submodules, restore caches, record CI evidence or cancel runs are not run: the
pinned tools (Verilator v5.050, sv2v v0.0.12, Yosys 0.66, the RV32 SDK, the pinned LiteX stack) are put on PATH
instead, and every submodule is already at its pin. Jobs that only read other jobs' uploaded artifacts are not run.
nproc reports CPUS (a hosted runner's 4), so each job sizes its own parallelism as hosted does.

usage: python3 run_ci.py OUT [JOB-GLOB...]   one line per job and step in OUT/results.json and OUT/<job>/*.log
"""
import concurrent.futures, fnmatch, json, os, re, shutil, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / 'src'
CPUS = 4
SKIP_STEP = re.compile(r'^(Install|Build Verilator|Build Yosys|Restore the pinned|Package the pinned|Fetch|Resolve exact package'
                       r'|Record|Collect actual runtime|Cancel|Observe the first|Retain checkout identity|Print the event'
                       r'|Put Verilator on PATH|Put a job-private Python|Place the VexiiRiscv|Apply the toolchain patch'
                       r'|Keep the generated CPU netlist|Assert the repository default branch|Decide whether|Classify the change'
                       r'|Require |Judge the complete publication census)')
#: Jobs whose every gate reads other jobs' uploads or the hosted API.
SKIP_JOB = {'docs-check', 'ci-manifest', 'ci-fail-fast', 'ci-cancel-tail', 'elaborate', 'rtl-fast', 'changes',
            'publication-census', 'firmware-boundary', 'full-ci-gate', 'verilator-suites', 'yosys-portability',
            'yosys-tool'}
#: The hosted runner's tool prefixes, and this host's pinned builds standing in for them.
OPT = {'/opt/verilator': '$PINNED_TOOLS/verilator-v5.050', '/opt/yosys': str(HERE / 'opt-yosys'),
       '/opt/sbt': str(HERE / 'opt-sbt')}
TOOLS = ['$PINNED_TOOLS/verilator-v5.050/bin', '$PINNED_TOOLS/sv2v-v0.0.12', '$HOME/br-milan-rv32/host/bin']


def jobs(selected):
    """Every (workflow, job, matrix) to run."""
    import yaml
    out = []
    for w in ('docs', 'elaborate', 'rtl-fast', 'rtl'):
        data = yaml.safe_load((SRC / f'.github/workflows/{w}.yml').read_text())
        for name, job in data['jobs'].items():
            if name.startswith('union-') or name in SKIP_JOB:
                continue
            matrix = (job.get('strategy') or {}).get('matrix') or {}
            combos = [{}]
            for key, values in matrix.items():
                if key in ('include', 'exclude'):
                    continue
                combos = [dict(c, **{key: v}) for c in combos for v in values]
            for extra in matrix.get('include', []) or []:
                combos = [dict(c, **extra) for c in combos] if combos != [{}] else [extra]
            for combo in combos:
                label = f'{w}/{name}' + ''.join(f'-{k}{v}' for k, v in sorted(combo.items()))
                if not selected or any(fnmatch.fnmatch(label, g) for g in selected):
                    out.append((w, name, combo, label, {**(data.get('env') or {}), **(job.get('env') or {})},
                                job.get('steps', [])))
    return out


#: A pull request into dev-soft-core, ready for review, at the head under test.
EVENT = {'github.event_name': 'pull_request', 'github.event.pull_request.base.ref': 'dev-soft-core',
         'github.event.before': '', 'github.event.pull_request.draft': 'false'}


def expression(text, combo, head):
    """A step env value with the event's fields, its matrix and the head substituted; anything else left as is."""
    values = dict(EVENT, **{'github.event.pull_request.head.sha': head, 'needs.full-ci-gate.outputs.target_sha': head},
                  **{f'matrix.{k}': str(v) for k, v in combo.items()})
    return re.sub(r'\$\{\{\s*([\w.-]+)\s*\}\}', lambda m: values.get(m.group(1), m.group(0)), text)


def condition(text, combo):
    """A step's `if:` as a pull-request run on an RTL-relevant head evaluates it: its matrix comparisons, always()
    and the scope true, failure() false, and every cache a miss."""
    expr = text.strip()
    expr = re.sub(r'^\$\{\{|\}\}$', '', expr).strip()
    for key, value in combo.items():
        expr = re.sub(r'matrix\.' + key + r'\b', repr(value), expr)
    expr = re.sub(r"steps\.scope\.outputs\.rtl == 'true'", 'True', expr)
    expr = re.sub(r"steps\.[\w-]+\.outputs\.cache-hit != 'true'", 'True', expr)
    expr = expr.replace('always()', 'True').replace('failure()', 'False').replace('!cancelled()', 'True')
    expr = expr.replace('&&', ' and ').replace('||', ' or ')
    if re.search(r'[a-z_]+\.', expr):
        raise ValueError(f'an unhandled condition: {text}')
    return bool(eval(expr, {'__builtins__': {}}, {'True': True, 'False': False}))


def run_job(spec, out):
    """One job in its own copy: each run step in order, stopping at the first failure as Actions does."""
    w, name, combo, label, env0, steps = spec
    slug = label.replace('/', '__')
    work = out / 'work' / slug
    log_dir = out / slug
    log_dir.mkdir(parents=True, exist_ok=True)
    if work.exists():
        return dict(job=label, status='refused', reason='work directory exists')
    while shutil.disk_usage(out).free < 6 * 10**9 or shutil.disk_usage('/data').free < 18 * 10**9:
        time.sleep(60)  # a job starts only with room for it, and /data keeps its 18 GB
    shutil.copytree(SRC, work, symlinks=True)
    temp = out / 'temp' / slug
    temp.mkdir(parents=True, exist_ok=True)
    shim = temp / 'shim'
    shim.mkdir(exist_ok=True)
    (shim / 'nproc').write_text(f'#!/bin/sh\necho {CPUS}\n')
    (shim / 'nproc').chmod(0o755)
    genv = temp / 'github_env'
    genv.write_text('')
    gpath = temp / 'github_path'
    gpath.write_text('')
    env = dict(os.environ)
    env.update({k: str(v).replace('${{ github.workspace }}', str(work)) for k, v in env0.items()})
    env.update(GITHUB_WORKSPACE=str(work), RUNNER_TEMP=str(temp), GITHUB_ENV=str(genv), GITHUB_EVENT_NAME='pull_request',
               GITHUB_OUTPUT=str(temp / 'github_output'), GITHUB_PATH=str(gpath), GITHUB_STEP_SUMMARY=str(temp / 'summary'), CI='true',
               GITHUB_ACTIONS='true', GITHUB_SHA=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=SRC,
                                                                          text=True).strip(),
               HOME=os.environ['HOME'], TMPDIR=str(temp))
    env['PATH'] = os.pathsep.join([str(shim), str(HERE / 'venv312/bin'), *TOOLS, env['PATH']])
    rows, status = [], 'success'
    for i, step in enumerate(steps):
        if 'run' not in step:
            continue
        sname = step.get('name', f'step {i}')
        if SKIP_STEP.match(sname):
            rows.append(dict(step=i, name=sname, status='not run (setup or evidence)'))
            continue
        if 'if' in step and not condition(str(step['if']), combo):
            rows.append(dict(step=i, name=sname, status='not run (its condition is false)'))
            continue
        script = step['run']
        for key, value in combo.items():
            script = re.sub(r'\$\{\{\s*matrix\.' + key + r'\s*\}\}', str(value), script)
        for opt, local in OPT.items():
            script = script.replace(opt, local)
        if '${{' in script:
            rows.append(dict(step=i, name=sname, status='refused', reason='unresolved expression'))
            status = 'failure'
            break
        for line in reversed(gpath.read_text().splitlines()):
            for opt, local in OPT.items():
                line = line.replace(opt, local)
            if line and line not in env['PATH'].split(os.pathsep):
                env['PATH'] = line + os.pathsep + env['PATH']
        for line in genv.read_text().splitlines():
            if '=' in line:
                k, _, v = line.partition('=')
                env[k] = v
        senv = dict(env, **{k: expression(str(v), combo, env['GITHUB_SHA']) for k, v in (step.get('env') or {}).items()})
        senv = {k: v for k, v in senv.items() if '${{' not in v}
        cwd = work / step.get('working-directory', '.')
        began = time.time()
        with (log_dir / f'{i:02d}.log').open('w') as sink:
            rc = subprocess.run(['bash', '--noprofile', '--norc', '-eo', 'pipefail', '-c', script], cwd=cwd,
                                env=senv, stdout=sink, stderr=subprocess.STDOUT).returncode
        rows.append(dict(step=i, name=sname, rc=rc, seconds=round(time.time() - began)))
        if rc:
            status = 'failure'
            break
    result = dict(job=label, status=status, steps=rows)
    (log_dir / 'result.json').write_text(json.dumps(result, indent=1) + '\n')
    if status == 'success':
        with open('$LANE_TOOLS/disk-cleanup.log', 'a') as log:
            log.write(f'{time.strftime("%Y-%m-%dT%H:%M:%S")} [A829] round 11 local CI: rm -rf {work} and {temp} '
                      f'(the passed job {label}\'s own copy of the clean clone and its temp; logs kept in {log_dir})\n')
        shutil.rmtree(work)
        shutil.rmtree(temp)
    print(f'{status.upper()} {label}', flush=True)
    return result


def main():
    out = Path(sys.argv[1]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    selected = jobs(sys.argv[2:])
    print('JOBS', len(selected), *[s[3] for s in selected], flush=True)
    parallel = int(os.environ.get('CI_LOCAL_PARALLEL', '6'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as pool:
        results = list(pool.map(lambda s: run_job(s, out), selected))
    prior = json.loads((out / 'results.json').read_text()) if (out / 'results.json').exists() else []
    keep = {r['job']: r for r in prior}
    keep.update({r['job']: r for r in results})
    (out / 'results.json').write_text(json.dumps(sorted(keep.values(), key=lambda r: r['job']), indent=1) + '\n')
    print('RESULT', sum(r['status'] == 'success' for r in results), 'of', len(results), 'passed', flush=True)


if __name__ == '__main__':
    main()
