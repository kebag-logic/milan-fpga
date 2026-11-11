#!/usr/bin/env python3
"""Reviewer probe of the REBOOT simulation's graders (tb/verilator/ctrl_reboot/run.py) on the logs of a
completed `run.py --self-test` build directory.

    python3 -B grader_probe.py CHECKOUT BUILD_DIR

1. The cut grade's "never a mix" clause, which no shipped control plants: the clean replay log is edited so
   one name reads the cut write's value and the other the saved one, and grade_cut must refuse it.
2. The plant `reset-before-the-response`: the cycles of the REBOOT's SUCCESS, its notification and the reset
   port in the planted run's own log, to see whether the port fired before the response left.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

CHECKOUT = Path(sys.argv[1]).resolve()
BUILD = Path(sys.argv[2]).resolve()
spec = importlib.util.spec_from_file_location('reboot_run', CHECKOUT / 'tb/verilator/ctrl_reboot/run.py')
run = importlib.util.module_from_spec(spec)
sys.modules['reboot_run'] = run
spec.loader.exec_module(run)

runs = BUILD / 'clean/runs'
reboot = run.parse(runs / 'reboot.log')
replay_path = runs / 'replay.log'
replay = run.parse(replay_path)
print('clean grade_cut:', run.grade_cut(reboot, replay))
saved_obj = 'reboot input'.encode().hex()
cut_obj = 'cut input'.encode().hex().ljust(len(saved_obj), '0')
text = replay_path.read_text()
assert text.count(saved_obj) >= 1, 'the saved object name is not in the replay log'
mixed = run.parse(replay_path, replay.tags, text.replace(saved_obj, cut_obj))
findings, report = run.grade_cut(reboot, mixed)
print('mixed grade_cut findings:', findings)
print('CONTROL cut-mix:', 'caught' if findings and findings[0].startswith('JOURNAL:') else 'ESCAPED')

plant = BUILD / 'plant-reset-before-the-response/runs/reboot.log'
log = run.parse(plant)
got = run.answers(log)
req = log.first('REQ')
note = [f.cycle for f in run.notifications(log, run.REBOOT) if f.cycle > log.rx_end.get('reboot', 0)]
success = got['reboot'].cycle if 'reboot' in got else None
print(f'PLANT reset-before-the-response: REBOOT in at {log.rx_end.get("reboot")}, SUCCESS left at {success}, '
      f'notification at {note[:1]}, reset port at {req[0] if req else None}; '
      f'port before the SUCCESS left: {bool(req and success and int(req[0]) < success)}')
