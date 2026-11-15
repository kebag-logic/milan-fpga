#!/usr/bin/env python3
"""One shard of the Verilator suite sweep as its own unit, on its own range, as native-shards.py starts each of its
shards (2026-09-23/native-shards.py: a --shared clone of the spec's cwd at its head under <data>/lanes, the
submodules from that tree, the spec's env prefix, run-recorded-gates.py, MemoryMax=10G, -j4), so each shard can start
as soon as a range is free rather than all four at once.

usage: sweep_shard.py LABEL SPEC.json OUT K N CPUS
"""
import json
import subprocess
import sys
from pathlib import Path

label, spec_path, out, k, n, cpus = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4]), \
    int(sys.argv[5]), sys.argv[6]
spec = json.loads(spec_path.read_text())
src, head = Path(spec['cwd']), spec['head']
suite = [c for c in spec['commands'] if 'scripts/run_all_suites.sh' in c]
assert len(suite) == 1, 'the spec must hold exactly one suite sweep'
prefix = suite[0][:suite[0].index('bash')]
RUNNER = Path('<management>/2026-09-21/run-recorded-gates.py')


def run(*a: str, cwd: Path | None = None) -> str:
    """One command, its output."""
    return subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def deps(repo: Path, rev: str) -> list[str]:
    """The tree's own submodules but 'external', the private dependency no bank builds."""
    text = run('git', 'config', '--blob', f'{rev}:.gitmodules', '--get-regexp', r'^submodule\..*\.path$', cwd=repo)
    return [line.split()[1] for line in text.splitlines() if line.split()[1] != 'external']


clone = Path(f'<data>/lanes/{label}-shard{k}')
if not clone.exists():
    run('git', 'clone', '-q', '--shared', '--no-checkout', str(src), str(clone))
run('git', 'fetch', '-q', str(src), head, cwd=clone)
run('git', '-c', 'advice.detachedHead=false', 'checkout', '-q', '-f', '--detach', head, cwd=clone)
DEPS = deps(clone, head)
run('git', 'clean', '-q', '-fdx', *[x for d in DEPS for x in ('-e', d)], cwd=clone)
assert run('git', 'status', '--porcelain', '--untracked-files=no', cwd=clone) == ''
for dep in DEPS:
    url = str(src / dep) if (src / dep / '.git').exists() else \
        run('git', 'config', '--blob', f'{head}:.gitmodules', f'submodule.{dep}.url', cwd=clone)
    run('git', 'config', f'submodule.{dep}.url', url, cwd=clone)
run('git', '-c', 'protocol.file.allow=always', 'submodule', 'update', '-q', '--init', '--force', *DEPS, cwd=clone)
shard_dir = out / f'shard-{k}'
shard_dir.mkdir(parents=True)
cmd = prefix + ['bash', 'scripts/run_all_suites.sh', str(shard_dir / 'logs'), '--wait', '--shard', f'{k}/{n}']
shard_spec = shard_dir / 'spec.json'
shard_spec.write_text(json.dumps(dict(cwd=str(clone), head=head, base=spec.get('base'), commands=[cmd]), indent=1) + '\n')
unit = f'milan-{label}-shard{k}'
subprocess.run(['systemd-run', '--user', f'--unit={unit}', '--collect', '--property=MemoryMax=10G',
                '--setenv=HOME=<home>', '--setenv=MAKEFLAGS=-j4',
                '--setenv=PATH=<home-local>/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin',
                '/usr/bin/taskset', '-c', cpus, '/usr/bin/python3', str(RUNNER), str(shard_spec)], check=True)
print(json.dumps(dict(label=label, head=head, shard=k, of=n, cpus=cpus, unit=unit, out=str(shard_dir))))
