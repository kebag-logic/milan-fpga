#!/usr/bin/env python3
"""sweep_shard.py SPEC OUT N: start the next unstarted shard k of N of a native bank's Verilator suite sweep (lane 895
round 9), on a range cpu_ranges.pick8() books now, as native-shards.py starts each of its shards: its own --shared
clone $LANES/895r9sweep-shard<k> of the spec's cwd at the spec's head (submodules from that clone, cleaned,
the tree checked clean), the spec's env prefix and suite command with `--shard k/N`, through
2026-09-21/run-recorded-gates.py, unit milan-895r9sweep-shard<k>, MemoryMax=10G, -j4. One shard a call, so each
shard has its own pick; prints what it started, or why it started nothing."""
import json
import subprocess
import sys
from pathlib import Path

M = Path('$MANAGEMENT/2026-09-23')
sys.path.insert(0, str(M))
import cpu_ranges  # noqa: E402

LABEL = '895r9sweep'
spec_path, out, n = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
spec = json.loads(spec_path.read_text())
src, head = Path(spec['cwd']), spec['head']
suite = [c for c in spec['commands'] if 'scripts/run_all_suites.sh' in c]
assert len(suite) == 1, 'the spec must hold exactly one suite sweep'
prefix = suite[0][:suite[0].index('bash')]
RUNNER = M.parent / '2026-09-21' / 'run-recorded-gates.py'
assert RUNNER.is_file(), RUNNER
run = lambda *a, cwd=None: subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()
out.mkdir(parents=True, exist_ok=True)
k = next((k for k in range(n) if not (out / f'shard-{k}').exists()), None)
if k is None:
    print('sweep: every shard started')
    sys.exit(0)
avail = next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable')) / 1048576
cpus = cpu_ranges.pick8() if avail > 20 else None
if not cpus:
    print(f'sweep: shard {k} waiting (no pick8 range, MemAvailable {avail:.0f} GB)')
    sys.exit(0)


def deps(repo, rev):
    o = run('git', 'config', '--blob', f'{rev}:.gitmodules', '--get-regexp', r'^submodule\..*\.path$', cwd=repo)
    return [line.split()[1] for line in o.splitlines() if line.split()[1] != 'external']


clone = Path(f'$LANES/{LABEL}-shard{k}')
if not clone.exists():
    run('git', 'clone', '-q', '--shared', '--no-checkout', str(src), str(clone))
run('git', 'fetch', '-q', str(src), head, cwd=clone)
run('git', '-c', 'advice.detachedHead=false', 'checkout', '-q', '-f', '--detach', head, cwd=clone)
DEPS = deps(clone, head)
run('git', 'clean', '-q', '-fdx', *[x for d in DEPS for x in ('-e', d)], cwd=clone)
assert run('git', 'status', '--porcelain', '--untracked-files=no', cwd=clone) == ''
for dep in DEPS:
    url = str(src / dep) if (src / dep / '.git').exists() else run(
        'git', 'config', '--blob', f'{head}:.gitmodules', f'submodule.{dep}.url', cwd=clone)
    run('git', 'config', f'submodule.{dep}.url', url, cwd=clone)
run('git', '-c', 'protocol.file.allow=always', 'submodule', 'update', '-q', '--init', '--force', *DEPS, cwd=clone)
shard_dir = out / f'shard-{k}'
shard_dir.mkdir()
cmd = prefix + ['bash', 'scripts/run_all_suites.sh', str(shard_dir / 'logs'), '--wait', '--shard', f'{k}/{n}']
shard_spec = shard_dir / 'spec.json'
shard_spec.write_text(json.dumps(dict(cwd=str(clone), head=head, base=spec.get('base'), commands=[cmd]), indent=1) + '\n')
unit = f'milan-{LABEL}-shard{k}'
subprocess.run(['systemd-run', '--user', f'--unit={unit}', '--collect', '--property=MemoryMax=10G',
                '--setenv=HOME=$WORKSPACE_HOME', '--setenv=MAKEFLAGS=-j4',
                '--setenv=PATH=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin',
                '/usr/bin/taskset', '-c', cpus, '/usr/bin/python3', str(RUNNER), str(shard_spec)], check=True,
               capture_output=True)
with (out / 'launched.txt').open('a') as f:
    f.write(json.dumps(dict(shard=k, cpus=cpus, unit=unit, avail_gb=round(avail))) + '\n')
print(f'sweep: started shard {k} of {n} on {cpus} ({unit})')
