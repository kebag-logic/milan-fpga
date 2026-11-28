"""Run an unchanged Python gate, logging every removal before it executes."""
import datetime
import os
from pathlib import Path
import runpy
import sys

cleanup_log = Path('$MANAGEMENT/2026-09-23/disk-cleanup.log')

def audit(event, args):
    if event not in ('os.remove', 'os.rmdir', 'shutil.rmtree'):
        return
    path = Path(os.fsdecode(args[0]))
    if not path.is_absolute():
        fd = args[1] if len(args) > 1 else None
        base = Path(os.readlink(f'/proc/self/fd/{fd}')) if isinstance(fd, int) and fd >= 0 else Path.cwd()
        path = base / path
    with cleanup_log.open('a') as stream:
        stream.write(f'{datetime.datetime.now(datetime.timezone.utc).isoformat()} BEFORE {event} {path.absolute()}\n')
        stream.flush()
        os.fsync(stream.fileno())

sys.addaudithook(audit)
sys.argv = sys.argv[1:]
sys.path.insert(0, str(Path(sys.argv[0]).resolve().parent))
runpy.run_path(sys.argv[0], run_name='__main__')
