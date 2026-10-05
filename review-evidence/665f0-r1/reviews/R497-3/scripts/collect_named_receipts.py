#!/usr/bin/env python3
"""Retain full named firmware-mutant failures from already-built binaries."""
import argparse
from pathlib import Path
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument('--packet', type=Path, required=True)
a = ap.parse_args()
cases = [
    ('available-replaces-owed-departing', 'test_adp', 'A15 with room, the next poll sends the owed ENTITY_DEPARTING first'),
    ('available-passes-owed-departing', 'test_adp', 'A17 room back and TMR_DELAY expiring before a poll'),
    ('second-departing-dropped', 'test_adp', 'A16 a SHUTDOWN while one is owed queues its own'),
    ('departing-sends-zero', 'test_adp', 'A10 SHUTDOWN in WAITING'),
    ('carried-ticks-overwritten', 'test_port_loop', 'L8 a TICK record taken while centiseconds are carried'),
]
for name, binary, needle in cases:
    exe = a.packet / 'scratch/firmware/mutants' / name / 'build' / binary
    r = subprocess.run([str(exe)], capture_output=True, text=True)
    log = r.stdout + r.stderr
    (a.packet / 'receipts' / ('firmware-' + name + '.log')).write_text(log)
    (a.packet / 'receipts' / ('firmware-' + name + '.rc')).write_text(str(r.returncode) + '\n')
    assert r.returncode == 1 and any('[FAIL]' in line and needle in line for line in log.splitlines())
    print(f'PASS {name}: completed rc=1 with its named assertion failure')
