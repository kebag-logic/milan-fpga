#!/usr/bin/env python3
"""proc-shards.py <label> <src-repo> <head> <base> <out> <N>: the processor's full suite sweep as N shards in parallel,
one dedicated clone and one unit per shard, as 2026-09-23/native-shards.py runs a native bank's sweep.

native-shards.py cannot drive this repository: it reads the submodule list from the head's .gitmodules
(`git config --blob <head>:.gitmodules`, check=True), which the processor does not have, so it stops before the
first unit, and it re-issues `scripts/run_all_suites.sh ... --shard k/N`, which the processor does not have either
(its sweep is scripts/run_suites.sh, with no shard option). This runner keeps everything else of it: a --shared
clone per shard at $LANES/<label>-shard<k>, checked out detached at the head and cleaned; a unit
milan-<label>-shard<k> per shard (systemd-run --user, --collect, MemoryMax=10G, MAKEFLAGS=-j4, the base PATH,
pinned with taskset to one CPU range from cpu_ranges.py pick, picked after the previous shard's unit started so
that no two shards share a range); and 2026-09-21/run-recorded-gates.py running the shard's spec. Each shard
runs proc-shard.sh (beside this file): the repository's own scripts/run_suites.sh with its suite loop given that
shard's suites, under the pinned Verilator and the CI Python. Prints one JSON line: units, CPU ranges, out.
"""
import json
import subprocess
import sys
from pathlib import Path

label, src, head, base, out, n = sys.argv[1:7]
n = int(n)
src, out = Path(src), Path(out)
here = Path(__file__).resolve().parent
mgmt = here.parents[2]
runner = mgmt / '2026-09-21' / 'run-recorded-gates.py'
picker = mgmt / '2026-09-23' / 'cpu_ranges.py'
venv = '$VALIDATION_STORAGE/scratch/pp216-a754/venv-ci/bin'
vl = '$VALIDATION_TOOLS/verilator-v5.050/bin'
base_path = '$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin'
out.mkdir(parents=True, exist_ok=False)


def run(*a, cwd=None):
    return subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


units, cpus = [], []
for k in range(n):
    clone = Path(f'$LANES/{label}-shard{k}')
    if not clone.exists():
        run('git', 'clone', '-q', '--shared', '--no-checkout', str(src), str(clone))
    run('git', 'fetch', '-q', str(src), head, cwd=clone)
    run('git', '-c', 'advice.detachedHead=false', 'checkout', '-q', '-f', '--detach', head, cwd=clone)
    run('git', 'clean', '-q', '-fdx', cwd=clone)
    assert run('git', 'rev-parse', 'HEAD', cwd=clone) == head
    assert run('git', 'status', '--porcelain', '--ignored', cwd=clone) == ''
    shard = out / f'shard-{k}'
    (shard / 'tmp').mkdir(parents=True)
    cmd = ['env', f'PATH={venv}:{vl}:{base_path}', f'TMPDIR={shard / "tmp"}',
           'bash', str(here / 'proc-shard.sh'), str(k), str(n), str(shard / 'logs')]
    spec = shard / 'spec.json'
    spec.write_text(json.dumps(dict(cwd=str(clone), head=head, base=base, commands=[cmd]), indent=1) + '\n')
    picked = subprocess.run(['python3', str(picker), 'pick'], capture_output=True, text=True)
    cpu = picked.stdout.strip()
    assert picked.returncode == 0 and cpu, 'no free CPU range'
    unit = f'milan-{label}-shard{k}'
    subprocess.run(['systemd-run', '--user', f'--unit={unit}', '--collect', '--property=MemoryMax=10G',
                    '--setenv=HOME=$HOME', '--setenv=MAKEFLAGS=-j4', f'--setenv=PATH={base_path}',
                    '/usr/bin/taskset', '-c', cpu, '/usr/bin/python3', str(runner), str(spec)], check=True)
    for _ in range(50):   # the next pick must see this unit's affinity
        mp = run('systemctl', '--user', 'show', '-p', 'MainPID', '--value', unit)
        if mp and mp != '0':
            break
        subprocess.run(['sleep', '0.2'])
    units.append(unit)
    cpus.append(cpu)
print(json.dumps(dict(label=label, head=head, shards=n, out=str(out), units=units, cpus=cpus)))
