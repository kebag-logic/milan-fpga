#!/usr/bin/env python3
"""Round 3's full-pass launcher (round 2 phase B's launchB.py, with launchM.py's fallback): the sweep first, as
native-shards.py's four shard units on four 8-wide ranges of 0-95 that the shared picker's busy set shows free at that
moment (cpu_ranges.free_ranges, none while a release hold collects), checked again right before the launch, and only
while MemAvailable is above 30 GB. Then the queue (NAME COMMAND lines), each as its own unit (unit.sh, MemoryMax 10G):
on a free picked range once the sweep has started or PRIORITY_S has passed, or, having waited FALLBACK_S with none
free, on this session's own CPUs (SESSION) while fewer than SESSION_MAX of mine run there; at most MAX at once, while
MemAvailable is above FLOOR_GB. Polls every POLL_S seconds; logs each launch and each end with its rc.
usage: launchC.py LABEL SPEC SWEEP_OUT QUEUE LOG MAX FLOOR_GB FALLBACK_S SESSION_MAX"""
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, '$MANAGEMENT/2026-09-23')
import cpu_ranges  # noqa: E402

T = Path('/data-2/milan/tmp/894b-a781')
SHARDS = '$MANAGEMENT/2026-09-23/native-shards.py'
SESSION = '96-127'
label, spec, sweep_out, queue, log = sys.argv[1:6]
MAX, FLOOR, FALLBACK_S, SESSION_MAX = int(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8]), int(sys.argv[9])
POLL_S, PRIORITY_S = 5, 1800
lines = [l.split(' ', 1) for l in Path(queue).read_text().splitlines() if l.strip() and not l.startswith('#')]
running: dict[str, str] = {}
start = waited_since = time.time()
swept = False


def note(text: str) -> None:
    with open(log, 'a') as f:
        f.write(f"{time.strftime('%T')} {text}\n")


def free() -> list[str]:
    return [] if cpu_ranges.p0_acquiring() else cpu_ranges.free_ranges(8)


def avail_gb() -> float:
    return next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable')) / 1048576


def active(name: str) -> bool:
    return subprocess.run(['systemctl', '--user', 'is-active', '--quiet',
                           f'milan-894b-a781-{name}.service']).returncode == 0


def launch(cpus: str) -> None:
    global waited_since
    name, cmd = lines.pop(0)
    subprocess.run(['bash', str(T / 'scripts/unit.sh'), name, cpus, str(T), 'bash', '-c', cmd], check=True)
    running[name] = cpus
    note(f'{name} started on {cpus} (MemAvailable {avail_gb():.0f} GB)')
    waited_since = time.time()
    time.sleep(5)


note(f'start: sweep {label} first, then {len(lines)} queue lines, at most {MAX} at once, floor {FLOOR} GB, '
     f'fallback after {FALLBACK_S:.0f} s to {SESSION} (at most {SESSION_MAX} there)')
while not swept or lines or running:
    for name in list(running):
        if not active(name):
            running.pop(name)
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
    if lines and len(running) < MAX and avail_gb() > FLOOR:
        if (swept or time.time() - start > PRIORITY_S) and ranges and ranges[-1] in free():
            launch(ranges[-1])
            continue
        on_session = sum(1 for c in running.values() if c == SESSION)
        if time.time() - waited_since > FALLBACK_S and on_session < SESSION_MAX:
            launch(SESSION)
            continue
    time.sleep(POLL_S)
note('all launched and ended')
