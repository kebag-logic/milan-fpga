"""rerun_shard.py <spec.json> <out-dir> <k> <N> <cpus>: one shard of native-shards.py again, in its own unit.

The shard's clone ($LANES/799-a692b-shard<k>) is reset the way native-shards.py resets it (checkout -f at
the spec's head, git clean -fdx keeping the submodules, submodules updated from the lane), and the spec's sweep
command is re-issued as `--shard k/N` with VERILATOR_JOBS=2 added to its env prefix, under MemoryMax=10G, pinned to
<cpus>: capture_coherence's mutation bank sizes its build jobs from the CPU affinity, and sixteen concurrent
datapath builds overran the first run's 10 GB unit (OOM kill).
"""
import json
import subprocess
import sys
from pathlib import Path

spec_path, out, k, n, cpus = sys.argv[1:6]
spec = json.loads(Path(spec_path).read_text())
src, head = Path(spec['cwd']), spec['head']
clone = Path(f'$LANES/799-a692b-shard{k}')
run = lambda *a, cwd=None: subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()
deps = [l.split()[1] for l in run('git', 'config', '--blob', f'{head}:.gitmodules', '--get-regexp',
                                  r'^submodule\..*\.path$', cwd=clone).splitlines() if l.split()[1] != 'external']
run('git', '-c', 'advice.detachedHead=false', 'checkout', '-q', '-f', '--detach', head, cwd=clone)
run('git', 'clean', '-q', '-fdx', *[x for d in deps for x in ('-e', d)], cwd=clone)
assert run('git', 'status', '--porcelain', '--untracked-files=no', cwd=clone) == ''
run('git', '-c', 'protocol.file.allow=always', 'submodule', 'update', '-q', '--init', '--force', *deps, cwd=clone)
suite = [c for c in spec['commands'] if 'scripts/run_all_suites.sh' in c][0]
prefix = suite[:suite.index('bash')] + ['VERILATOR_JOBS=2']
shard_dir = Path(out)
shard_dir.mkdir(parents=True, exist_ok=False)
cmd = prefix + ['bash', 'scripts/run_all_suites.sh', str(shard_dir / 'logs'), '--wait', '--shard', f'{k}/{n}']
shard_spec = shard_dir / 'spec.json'
shard_spec.write_text(json.dumps(dict(cwd=str(clone), head=head, base=spec.get('base'), commands=[cmd]), indent=1) + '\n')
unit = f'milan-799-a692b-shard{k}-rerun'
subprocess.run(['systemd-run', '--user', f'--unit={unit}', '--collect', '--property=MemoryMax=10G',
                '--setenv=HOME=$WORKSPACE_HOME', '--setenv=MAKEFLAGS=-j4',
                '--setenv=PATH=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin',
                '/usr/bin/taskset', '-c', cpus, '/usr/bin/python3',
                '$MANAGEMENT/2026-09-21/run-recorded-gates.py', str(shard_spec)], check=True)
print(json.dumps(dict(unit=unit, clone=str(clone), out=str(shard_dir))))
