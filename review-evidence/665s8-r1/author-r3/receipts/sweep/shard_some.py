"""(scratch copy: the listed shards only, the same clone, unit and command per shard) Run a native bank's Verilator suite sweep as N shards in parallel: one dedicated clone and one unit per shard.

usage: native-shards.py <label> <full-native.json> <out-dir> <N> <cpus-0> ... <cpus-N-1>
The spec's suite command (`... scripts/run_all_suites.sh <logs> --wait`) is re-issued per shard k as
`... scripts/run_all_suites.sh <out>/shard-k/logs --wait --shard k/N`, with the spec's own env prefix (pinned tools,
VERILATOR_ROOT), through 2026-09-21/run-recorded-gates.py, in <data>/lanes/<label>-shard<k> (a --shared clone of
the spec's cwd at the spec's head, submodules from that clone). Units milan-<label>-shard<k>, MemoryMax=10G, -j4.
2026-10-02: the serial sweep was 1h45m of a 2h32m native bank at 1.8 of 8 cores busy (owner asked why runs are
slow); hosted CI already runs these shards on separate runners, so separate clones keep generated files apart.
"""
from pathlib import Path
import json, subprocess, sys

label, spec_path, out, n = sys.argv[1:5]
wanted = dict(a.split(':') for a in sys.argv[5:])
n = int(n)
spec = json.loads(Path(spec_path).read_text())
src, head, out = Path(spec['cwd']), spec['head'], Path(out)
suite = [c for c in spec['commands'] if 'scripts/run_all_suites.sh' in c]
assert len(suite) == 1, 'the spec must hold exactly one suite sweep'
prefix = suite[0][:suite[0].index('bash')]
out.mkdir(parents=True, exist_ok=True)
run = lambda *a, cwd=None: subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()
RUNNER = Path('<home>/milan-fpga-management/2026-09-21/run-recorded-gates.py')
def _deps(repo, rev=None):
    """2026-10-13 21:5x: the submodule list comes from the tree's own .gitmodules (697c added third_party/tsn-c-stack and the
    hardcoded three-entry list left it uninitialised, failing the candidate banks at mbx and milan_dp). 'external' stays out:
    it is the private SSH dependency no bank builds."""
    src = ['git', 'config', '--blob', f'{rev}:.gitmodules'] if rev else ['git', 'config', '-f', '.gitmodules']
    out = subprocess.run(src + ['--get-regexp', r'^submodule\..*\.path$'], cwd=repo, capture_output=True, text=True, check=True).stdout
    return [line.split()[1] for line in out.splitlines() if line.split()[1] != 'external']


units = []
for k in sorted(int(x) for x in wanted):
    clone = Path(f'<data>/lanes/{label}-shard{k}')
    if not clone.exists():
        run('git', 'clone', '-q', '--shared', '--no-checkout', str(src), str(clone))
    for active in run('systemctl', '--user', 'list-units', '--plain', '--no-legend', 'milan-*').splitlines():
        assert str(clone) not in run('systemctl', '--user', 'show', active.split()[0], '-p', 'ExecStart'), active
    run('git', 'fetch', '-q', str(src), head, cwd=clone)
    run('git', '-c', 'advice.detachedHead=false', 'checkout', '-q', '-f', '--detach', head, cwd=clone)
    DEPS = _deps(clone, head)
    run('git', 'clean', '-q', '-fdx', *[x for d in DEPS for x in ('-e', d)], cwd=clone)
    assert run('git', 'status', '--porcelain', '--untracked-files=no', cwd=clone) == ''
    for dep in DEPS:
        url = str(src / dep) if (src / dep / '.git').exists() else run('git', 'config', '--blob', f'{head}:.gitmodules', f'submodule.{dep}.url', cwd=clone)
        run('git', 'config', f'submodule.{dep}.url', url, cwd=clone)
    run('git', '-c', 'protocol.file.allow=always', 'submodule', 'update', '-q', '--init', '--force', *DEPS, cwd=clone)
    shard_dir = out / f'shard-{k}'
    shard_dir.mkdir()
    cmd = prefix + ['bash', 'scripts/run_all_suites.sh', str(shard_dir / 'logs'), '--wait', '--shard', f'{k}/{n}']
    shard_spec = shard_dir / 'spec.json'
    shard_spec.write_text(json.dumps(dict(cwd=str(clone), head=head, base=spec.get('base'), commands=[cmd]), indent=1) + '\n')
    unit = f'milan-{label}-shard{k}'
    subprocess.run(['systemd-run', '--user', f'--unit={unit}', '--collect', '--property=MemoryMax=10G',
                    '--setenv=HOME=<home>', '--setenv=MAKEFLAGS=-j4',
                    '--setenv=PATH=<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin',
                    '/usr/bin/taskset', '-c', wanted[str(k)], '/usr/bin/python3', str(RUNNER), str(shard_spec)], check=True)
    units.append(unit)
print(json.dumps(dict(label=label, head=head, shards=n, out=str(out), units=units)))
