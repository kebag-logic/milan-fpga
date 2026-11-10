#!/usr/bin/env python3
"""The full sweep as four native-shards units, launched only at a moment when four 8-CPU ranges are free together,
with no placeholder holding a range idle meanwhile (release lanes have CPU priority; this lane's holds of 13:02 were
stopped at 14:03). The four shard clones are prepared first, as native-shards.py prepares them, so its own preparation
at launch is a no-op and the units start within seconds of the ranges being read. Shard 2, which holds
capture_coherence, gets four CPUs of its range (its mutant driver builds one datapath a CPU). Waits while
MemAvailable is at or under 30 GB or a release hold is still collecting CPUs. usage: sweep_free.py COMMIT"""
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, '<management>/2026-09-23')
import cpu_ranges  # noqa: E402

H = sys.argv[1]
T = Path('<scratch>')
LABEL = '665s2b-a683ze-sweep'
SRC = T / f'src-{LABEL}'
OUT = T / 'sweep'
LOG = T / f'logs/{LABEL}.txt'
M = '<management>/2026-09-23'


def note(text: str) -> None:
    with LOG.open('a') as f:
        f.write(f"{time.strftime('%T')} {text}\n")


def run(*a, cwd=None) -> str:
    return subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


assert run('git', 'rev-parse', 'HEAD', cwd=SRC) == H and run('git', 'status', '--porcelain', cwd=SRC) == ''
deps = [line.split()[1] for line in run('git', 'config', '-f', '.gitmodules', '--get-regexp',
                                        r'^submodule\..*\.path$', cwd=SRC).splitlines() if line.split()[1] != 'external']
for k in range(4):
    clone = Path(f'<data>/lanes/{LABEL}-shard{k}')
    if not clone.exists():
        run('git', 'clone', '-q', '--shared', '--no-checkout', str(SRC), str(clone))
    run('git', 'fetch', '-q', str(SRC), H, cwd=clone)
    run('git', '-c', 'advice.detachedHead=false', 'checkout', '-q', '-f', '--detach', H, cwd=clone)
    for dep in deps:
        url = str(SRC / dep) if (SRC / dep / '.git').exists() else run(
            'git', 'config', '--blob', f'{H}:.gitmodules', f'submodule.{dep}.url', cwd=clone)
        run('git', 'config', f'submodule.{dep}.url', url, cwd=clone)
    run('git', '-c', 'protocol.file.allow=always', 'submodule', 'update', '-q', '--init', '--force', *deps, cwd=clone)
    note(f'shard {k} clone prepared at {run("git", "rev-parse", "HEAD", cwd=clone)}')
spec = T / f'{LABEL}-spec.json'
spec.write_text(json.dumps({
    'cwd': str(SRC), 'head': H, 'base': '1d6bf5556a',
    'commands': [['env', 'PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:'
                  '<data>/scratch/a662/make43/bin:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin',
                  'VERILATOR=<tools>/pinned-verilator-5.050/verilator',
                  'TSN_GEN_ROOT=<management>/tools/tsn-gen-deca300c',
                  f'TMPDIR={T}/tmp-{LABEL}', 'MAKEFLAGS=-j4 --no-print-directory',
                  'bash', 'scripts/run_all_suites.sh', f'{OUT}/logs', '--wait']]}) + '\n')
(T / f'tmp-{LABEL}').mkdir(exist_ok=True)
while True:
    avail = next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable'))
    if avail > 30 * 1024 * 1024 and not cpu_ranges.p0_acquiring():
        taken = cpu_ranges.busy()
        halves = cpu_ranges.packed8(taken)
        for block in cpu_ranges.free_ranges(16, taken):
            a = int(block.split('-')[0])
            halves += [f'{a}-{a + 7}', f'{a + 8}-{a + 15}']
        if len(halves) >= 4:
            ranges = halves[:4]
            first = int(ranges[2].split('-')[0])
            ranges[2] = f'{first}-{first + 3}'
            note(f'launching on {" ".join(ranges)} (MemAvailable {avail // 1024} MB)')
            rc = subprocess.run(['python3', f'{M}/native-shards.py', LABEL, str(spec), str(OUT), '4', *ranges],
                                stdout=LOG.open('a'), stderr=subprocess.STDOUT).returncode
            note(f'native-shards rc={rc}')
            break
    time.sleep(20)
