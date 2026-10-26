#!/usr/bin/env python3
"""Build focused controls while temporarily pausing this packet's simulations.

This keeps the fixed 16-way compiler build within the 16-job allowance.
Only this packet's simulation processes are paused; finally always resumes them.
"""
import os
from pathlib import Path
import signal
import sys
import run_review as review

pids = []
for entry in Path('/proc').iterdir():
    if not entry.name.isdecimal():
        continue
    try:
        argv = (entry / 'cmdline').read_bytes().split(b'\0')
        exe = argv[0].decode()
    except (OSError, UnicodeError):
        continue
    if exe.startswith(str(review.SCRATCH) + '/') and exe.endswith('/native/Vsim'):
        pids.append(int(entry.name))
try:
    for pid in pids:
        os.kill(pid, signal.SIGSTOP)
    for name, mutation, regions in [('asbuilt', 'none', 'as-built'),
                                     ('slow', 'slow-adp-rx', 'cover'),
                                     ('own-slow', 'review-slow-acmp', 'cover')]:
        rc = review.run(name + '-build', [sys.executable, '-B', str(Path(review.__file__)),
                        'build-one', name, '1x1', regions, mutation])
        if rc:
            raise SystemExit(rc)
finally:
    for pid in pids:
        try:
            os.kill(pid, signal.SIGCONT)
        except ProcessLookupError:
            pass
