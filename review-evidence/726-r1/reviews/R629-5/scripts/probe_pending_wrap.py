#!/usr/bin/env python3
"""Seed the widened pending total near 2**32 and add three real MAC packets."""
import importlib.util
import os
from pathlib import Path
import sys

root, packet = map(lambda arg: Path(arg).resolve(), sys.argv[1:3])
suite = root / 'tb/verilator/milan_dp'
spec = importlib.util.spec_from_file_location('counter_driver', suite / 'stream_counters.py')
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
work = packet / 'scratch/pending-wrap'
work.mkdir(parents=True, exist_ok=True)
header = (suite / 'stream_counters.hpp').read_text()
header = driver.replace_once(header, 'frx_acc_r[s]=65534;', 'frx_acc_r[s]=UINT32_MAX-1u;')
header = driver.replace_once(header, 'batch crosses 65535 without loss', 'pending 32-bit wrap retains all three packets')
header = driver.replace_once(header, 'batch_base[s]),65537);', 'batch_base[s]),1);')
(work / 'stream_counters.hpp').write_text(header)
source = (suite/'sim_nxn.cpp').read_text().replace('../../common/verilator_harness.hpp', str(root/'tb/common/verilator_harness.hpp'))
(work/'sim_nxn.cpp').write_text(source)
driver.fixture_source = lambda variant, directory: work/'sim_nxn.cpp'
driver.run(1, 'clean', work, os.environ['VERILATOR'], 'uncertain')
