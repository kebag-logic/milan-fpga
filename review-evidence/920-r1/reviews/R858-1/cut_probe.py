#!/usr/bin/env python3
"""Compile and run cut_probe.cpp against the exact checkout, at both shapes."""
import argparse
import os
import sys
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument('repository', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('--jobs', type=int, default=4)
a = p.parse_args()
root, packet = a.repository.resolve(), a.packet.resolve()
(packet / 'scratch').mkdir(parents=True, exist_ok=True)
os.environ['TMPDIR'] = str(packet / 'scratch')
sys.path.insert(0, str(root / 'sw/firmware/ctrl_nvm/test'))
import test_ctrl_nvm as gate
import nvm_bench as bench
import fw_gtest
failed = False
for name in ('endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8'):
    work = packet / 'scratch/cut-probe' / name
    shape = gate.prepare(root / 'configs' / (name + '.yaml'), work)
    binary = bench.Binary('cut_probe', (*bench.RIG, str(packet / 'cut_probe.cpp')))
    exe = bench.build_suite(shape.inputs, work / 'build', fw_gtest.Build(jobs=a.jobs), binary)
    ok, log = bench.run_suite(exe, shape.fixture)
    print(name, log, flush=True)
    (packet / 'receipts' / (name + '-cuts.log')).write_text(log)
    failed |= not ok
raise SystemExit(int(failed))
