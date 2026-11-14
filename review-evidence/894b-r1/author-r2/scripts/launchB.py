#!/usr/bin/env python3
"""Phase B's full-pass launcher: the sweep first, then the queue (dispatch.py's lines), every unit on an 8-wide range
of 0-95 that the shared picker's busy set shows free at that moment (cpu_ranges.busy through free8's rule: aligned,
none while a release hold collects), checked again right before each launch. The sweep runs as native-shards.py's four
shard units on four such ranges at once. Until the sweep has started, or for PRIORITY_S after the start, no queue line
takes a range; after that, a queue line starts on each free range while fewer than MAX run and MemAvailable is above
FLOOR_GB. Polls every POLL_S seconds; logs each launch and each end with its rc.
usage: launchB.py LABEL SPEC SWEEP_OUT QUEUE LOG MAX FLOOR_GB"""
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, '$MANAGEMENT/2026-09-23')
import cpu_ranges  # noqa: E402

T = Path('/data-2/milan/tmp/894b-a781')
SHARDS = '$MANAGEMENT/2026-09-23/native-shards.py'
label, spec, sweep_out, queue, log = sys.argv[1:6]
MAX, FLOOR = int(sys.argv[6]), float(sys.argv[7])
POLL_S, PRIORITY_S = 3, 1800
lines = [l.split(' ', 1) for l in Path(queue).read_text().splitlines() if l.strip() and not l.startswith('#')]
running: list[str] = []
start = time.time()
swept = False


def note(text: str) -> None:
    with open(log, 'a') as f:
        f.write(f"{time.strftime('%T')} {text}\n")


def free() -> list[str]:
    """The free 8-wide aligned ranges now (cpu_ranges.free_ranges over its busy set), none while a hold collects."""
    return [] if cpu_ranges.p0_acquiring() else cpu_ranges.free_ranges(8)


def avail_gb() -> float:
    return next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable')) / 1048576


def active(name: str) -> bool:
    return subprocess.run(['systemctl', '--user', 'is-active', '--quiet', f'milan-894b-a781-{name}.service']).returncode == 0


note(f'start: sweep {label} first, then {len(lines)} queue lines, at most {MAX} at once, floor {FLOOR} GB')
while not swept or lines or running:
    for name in list(running):
        if not active(name):
            running.remove(name)
            rc = T / 'units' / f'{name}.rc'
            note(f"{name} ended rc={rc.read_text().strip() if rc.exists() else '?'}")
    ranges = free()
    if not swept and len(ranges) >= 4 and avail_gb() > 30:
        cpus = ranges[:4]
        if all(c in free() for c in cpus):
            note(f'sweep {label} launching on {" ".join(cpus)} (MemAvailable {avail_gb():.0f} GB)')
            r = subprocess.run(['python3', SHARDS, label, spec, sweep_out, '4', *cpus], capture_output=True, text=True)
            note(f'sweep launch rc={r.returncode} {r.stdout.strip()[-300:]} {r.stderr.strip()[-300:]}')
            swept = True
            time.sleep(10)
            continue
    if (swept or time.time() - start > PRIORITY_S) and lines and len(running) < MAX and avail_gb() > FLOOR and ranges:
        cpus = ranges[-1]
        if cpus in free():
            name, cmd = lines.pop(0)
            subprocess.run(['bash', str(T / 'scripts/unit.sh'), name, cpus, str(T), 'bash', '-c', cmd], check=True)
            running.append(name)
            note(f'{name} started on {cpus} (MemAvailable {avail_gb():.0f} GB)')
            time.sleep(5)
            continue
    time.sleep(POLL_S)
note('all launched and ended')
