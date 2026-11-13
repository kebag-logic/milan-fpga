"""Hold this round's own simulations (Vsim under this round's scratch) with SIGSTOP while /data-2 has under 2,000 MB
free, and resume them with SIGCONT over 4,000 MB; a line per change. usage: a683zo_diskguard.py LOG"""
import os, shutil, signal, sys, time
from pathlib import Path
MINE = '/data-2/milan/tmp/665s2b-a683zo/'
log = Path(sys.argv[1])
held = False


def mine():
    """PIDs of this round's Vsim processes."""
    out = []
    for d in Path('/proc').iterdir():
        if d.name.isdigit():
            try:
                args = (d / 'cmdline').read_bytes().split(b'\0')
            except OSError:
                continue
            if args and args[0].decode(errors='replace').startswith(MINE) and args[0].endswith(b'/Vsim'):
                out.append(int(d.name))
    return out


while True:
    free = shutil.disk_usage('/data-2').free // 2**20
    if not held and free < 2000:
        pids = mine()
        for p in pids:
            os.kill(p, signal.SIGSTOP)
        held = True
        log.open('a').write(f"{time.strftime('%T')} held {len(pids)} at {free} MB free\n")
    elif held and free > 4000:
        pids = mine()
        for p in pids:
            os.kill(p, signal.SIGCONT)
        held = False
        log.open('a').write(f"{time.strftime('%T')} resumed {len(pids)} at {free} MB free\n")
    time.sleep(10)
