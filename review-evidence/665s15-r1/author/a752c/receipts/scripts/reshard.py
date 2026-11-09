"""Re-run ONE shard of a native-shards sweep as native-shards.py runs it: a fresh --shared clone of the spec's cwd at
its head, submodules from that clone, the spec's env prefix, `scripts/run_all_suites.sh <out>/shard-k/logs --wait
--shard k/N` through run-recorded-gates.py, in unit milan-<label>-shard<k> with MemoryMax=10G and MAKEFLAGS=-j4.
Used when a shard's suite was killed by the wall clock (exit 92: "Re-run it uncontended"), so only that shard re-runs.

usage: python3 -I reshard.py <label> <full-native.json> <out-dir> <k> <N> <cpus>
"""
from pathlib import Path
import json, subprocess, sys

label, spec_path, out, k, n, cpus = sys.argv[1:7]
k, n = int(k), int(n)
spec = json.loads(Path(spec_path).read_text())
src, head, out = Path(spec['cwd']), spec['head'], Path(out)
suite = [c for c in spec['commands'] if 'scripts/run_all_suites.sh' in c]
assert len(suite) == 1, 'the spec must hold exactly one suite sweep'
prefix = suite[0][:suite[0].index('bash')]
out.mkdir(parents=True, exist_ok=False)
run = lambda *a, cwd=None: subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()
RUNNER = Path('$HOME/milan-fpga-management/2026-09-21/run-recorded-gates.py')
clone = Path(f'$DATA/lanes/{label}-shard{k}')
assert not clone.exists(), f'{clone} exists: the re-run takes a fresh clone'
run('git', 'clone', '-q', '--shared', '--no-checkout', str(src), str(clone))
run('git', '-c', 'advice.detachedHead=false', 'checkout', '-q', '-f', '--detach', head, cwd=clone)
gm = run('git', 'config', '--blob', f'{head}:.gitmodules', '--get-regexp', r'^submodule\..*\.path$', cwd=clone)
DEPS = [line.split()[1] for line in gm.splitlines() if line.split()[1] != 'external']
assert run('git', 'status', '--porcelain', '--untracked-files=all', cwd=clone) == ''
for dep in DEPS:
    url = str(src / dep) if (src / dep / '.git').exists() else run('git', 'config', '--blob', f'{head}:.gitmodules', f'submodule.{dep}.url', cwd=clone)
    run('git', 'config', f'submodule.{dep}.url', url, cwd=clone)
run('git', '-c', 'protocol.file.allow=always', 'submodule', 'update', '-q', '--init', '--force', *DEPS, cwd=clone)
assert run('git', 'rev-parse', 'HEAD', cwd=clone) == head
shard_dir = out / f'shard-{k}'
shard_dir.mkdir()
cmd = prefix + ['bash', 'scripts/run_all_suites.sh', str(shard_dir / 'logs'), '--wait', '--shard', f'{k}/{n}']
shard_spec = shard_dir / 'spec.json'
shard_spec.write_text(json.dumps(dict(cwd=str(clone), head=head, base=spec.get('base'), commands=[cmd]), indent=1) + '\n')
unit = f'milan-{label}-shard{k}'
subprocess.run(['systemd-run', '--user', f'--unit={unit}', '--collect', '--property=MemoryMax=10G',
                '--setenv=HOME=$HOME', '--setenv=MAKEFLAGS=-j4',
                '--setenv=PATH=$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin',
                '/usr/bin/taskset', '-c', cpus, '/usr/bin/python3', str(RUNNER), str(shard_spec)], check=True)
print(json.dumps(dict(label=label, head=head, shard=f'{k}/{n}', cpus=cpus, out=str(out), unit=unit)))
