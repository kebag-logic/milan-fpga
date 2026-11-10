"""memlog.py OUT: every 15 s, the time, this session unit's anon memory in GB and MemAvailable, appended to OUT."""
import sys
import time
from pathlib import Path

G = Path("/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/milan-665s7-a757c2.service")
while True:
    stat = dict(line.split() for line in (G / "memory.stat").read_text().splitlines())
    avail = next(int(l.split()[1]) for l in open("/proc/meminfo") if l.startswith("MemAvailable"))
    with open(sys.argv[1], "a") as fh:
        fh.write(f"{time.strftime('%T')} anon {int(stat['anon']) / 1e9:.2f} GB MemAvailable {avail / 1e6:.1f} GB\n")
    time.sleep(15)
