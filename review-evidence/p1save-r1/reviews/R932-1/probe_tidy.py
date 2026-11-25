#!/usr/bin/env python3
"""Compile the unchanged store with a focused maintenance-capture fault probe."""
from pathlib import Path
import os
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch' / 'tidy'
scratch.mkdir(parents=True, exist_ok=True)
os.environ['TMPDIR'] = str(packet / 'scratch')
sys.path.insert(0, str(root / 'sw/firmware/ctrl_nvm/test'))
import nvm_bench as b
import nvm_fixture as f
for shape in ['endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8']:
    inputs = b.shape_inputs(root / 'configs' / (shape + '.yaml'), scratch / shape / 'inputs')
    fixture = f.write_fixture(b.make_bench(inputs), scratch / shape / 'fixture')
    binary = b.Binary('tidy_probe', (*b.RIG, str(packet / 'probe_tidy.cpp')))
    exe = b.build_suite(inputs, scratch / shape / 'build', b.fw_gtest.Build(jobs=3), binary)
    ok, log = b.run_suite(exe, fixture)
    print('SHAPE', shape, 'contract_pass', ok, flush=True)
    print(log, flush=True)
