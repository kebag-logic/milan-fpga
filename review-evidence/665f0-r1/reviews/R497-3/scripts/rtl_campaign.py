#!/usr/bin/env python3
"""Run the existing scoped mailbox campaign and retain each complete receipt."""
import argparse
import importlib.util
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--packet', type=Path, required=True)
ap.add_argument('--jobs', type=int, required=True)
a = ap.parse_args()
spec = importlib.util.spec_from_file_location('mbx_mutants', a.repo / 'tb/verilator/mbx/mutants.py')
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
original = m.build_and_run

def retained(rtl, work, host):
    rc, log = original(rtl, work, host)
    raw = a.packet / 'scratch' / 'raw' / (work.name + '.log')
    raw.parent.mkdir(parents=True, exist_ok=True)
    raw.write_text(log)
    public = log.replace(str(a.packet.resolve()), '<packet>').replace(str(a.repo.resolve()), '<review-root>')
    (a.packet / 'receipts' / (work.name + '.log')).write_text(public)
    (a.packet / 'receipts' / (work.name + '.rc')).write_text(str(rc) + '\n')
    return rc, log

m.build_and_run = retained
raise SystemExit(m.main(['--jobs', str(a.jobs), '--keep', str(a.packet / 'scratch' / 'rtl-mutants')]))
