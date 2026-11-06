#!/usr/bin/env python3
"""capture_replay.py CHECKOUT WORK [PREFIX...]: the boundary gate's run of test_ctrl_firmware.py, under its capture, as
ctrl_runs.standalone makes it; prints its exit status and seconds. PREFIX wraps the command (a syscall trace)."""
import os, sys, time
from pathlib import Path
root, work, prefix = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_capture
from ctrl_configs import BUILDERS
b = next(b for b in BUILDERS if b.path.endswith('test_ctrl_firmware.py'))
words = b.runs[0]
argv = prefix + [w.format(python=sys.executable, work=work, verilator='') for w in words]
work.mkdir(parents=True, exist_ok=True)
print('argv', argv, flush=True)
t = time.monotonic()
with (work / 'run.log').open('w') as sink:
    res = ctrl_capture.run(work / 'capture', argv, cwd=root, stdout=sink, stderr=sink)
print(f'exit {res.returncode} after {time.monotonic() - t:.0f} s', flush=True)
