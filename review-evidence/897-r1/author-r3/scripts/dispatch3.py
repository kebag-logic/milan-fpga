#!/usr/bin/env python3
"""Run a queue of gate commands (each line: NAME MEMORY_MAX CMD...), every one as its own transient unit of lane 897,
as round 2's dispatch2.py did, the pool only while its measured load leaves 16 CPUs idle. A line starts only while MemAvailable is above FLOOR_GB: on a range
cpu_ranges.py picks while this lane holds fewer than MAX booked units, else on the session pool while fewer than POOL
of this lane's units run there. A line is taken once; a log line per start and end; a unit's rc is the file its
command writes. usage: dispatch.py MAX POOL FLOOR_GB QUEUE LOG"""
import fcntl, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, '$MANAGEMENT/2026-09-23')
import cpu_ranges  # noqa: E402

T = Path('/data-2/milan/tmp/897-a776')
RCS = T / 'r3/gates-out/rc'
LOCK = T / 'r3/pick.lock'
MAX, POOL, FLOOR, Q, LOG = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5])
RCS.mkdir(parents=True, exist_ok=True)
mine = {}


def note(text):
    with LOG.open('a') as f:
        f.write(f"{time.strftime('%T')} {text}\n")


def active(name):
    return subprocess.run(['systemctl', '--user', 'is-active', '--quiet', f'milan-897-a776-{name}.service']).returncode == 0


def avail_gb():
    return next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable')) / 1048576


def my_pool_units():
    """Every active unit of this lane on the session pool, this dispatcher's or another's."""
    out = subprocess.run(['systemctl', '--user', 'list-units', '--plain', '--no-legend', '--state=active',
                          'milan-897-a776-*'], capture_output=True, text=True).stdout.split()
    n = 0
    for u in (w for w in out if w.endswith('.service') and w != 'milan-897-a776c.service'):
        pid = subprocess.run(['systemctl', '--user', 'show', '-p', 'MainPID', '--value', u], capture_output=True,
                             text=True).stdout.strip()
        aff = subprocess.run(['taskset', '-cp', pid], capture_output=True, text=True).stdout
        n += aff.strip().endswith(cpu_ranges.SESSION_POOL)
    return n


def pool_busy():
    """The session pool's CPUs in use now, from two /proc/stat samples a second apart."""
    def sample():
        out = {}
        for line in open('/proc/stat'):
            p = line.split()
            if p[0].startswith('cpu') and p[0][3:].isdigit() and 96 <= int(p[0][3:]) <= 127:
                v = list(map(int, p[1:]))
                out[p[0]] = (sum(v), v[3] + v[4])
        return out
    a = sample(); time.sleep(1); b = sample()
    return sum(1 - (b[k][1] - a[k][1]) / max(1, b[k][0] - a[k][0]) for k in a)


def start(name, rng, mem, cmd, where):
    rc = RCS / f'{name}.rc'
    rc.unlink(missing_ok=True)
    subprocess.run(['bash', str(T / 'scripts/unit.sh'), name, rng, mem, str(T), '--', '/bin/bash', '-c',
                    repr(f'{cmd}; echo $? > {rc}')], check=True)
    mine[name] = where
    note(f'{name} unit on {rng} ({where}, MemAvailable {avail_gb():.0f} GB)')


while True:
    for name in list(mine):
        if not active(name):
            rc = RCS / f'{name}.rc'
            note(f'{name} ended rc={rc.read_text().strip() if rc.exists() else "none"}')
            del mine[name]
    lines = [line for line in Q.read_text().splitlines() if line.strip()]
    if not lines:
        if not mine:
            note(f'queue {Q.name} empty')
            break
        time.sleep(30)
        continue
    name, mem, cmd = lines[0].split(None, 2)
    started = False
    if avail_gb() > FLOOR:
        if sum(1 for w in mine.values() if w == 'booked') < MAX:
            # one pick at a time across this lane's launchers (the sweep's too), held until the unit is visible
            with open(LOCK, 'a') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX)
                r = subprocess.run([sys.executable, '$MANAGEMENT/2026-09-23/cpu_ranges.py', 'pick'],
                                   capture_output=True, text=True)
                if r.returncode == 0 and r.stdout.strip():
                    start(name, r.stdout.strip(), mem, cmd, 'booked')
                    started = True
                    time.sleep(5)
        if not started and my_pool_units() < POOL and pool_busy() < 16:
            start(name, cpu_ranges.SESSION_POOL, mem, cmd, 'pool')
            started = True
    if started:
        Q.write_text(''.join(line + '\n' for line in lines[1:]))
        time.sleep(20)
    else:
        time.sleep(30)
