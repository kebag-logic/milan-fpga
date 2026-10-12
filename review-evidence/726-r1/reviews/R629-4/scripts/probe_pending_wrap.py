#!/usr/bin/env python3
"""Exercise the 32-bit pending receive accumulator through real MAC input."""
import importlib.util
import os
import pathlib
import sys

root, packet = map(pathlib.Path, sys.argv[1:])
here = root / "tb/verilator/milan_dp"
spec = importlib.util.spec_from_file_location("counter_driver", here / "stream_counters.py")
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)

def source(variant, work):
    header = (here / "stream_counters.hpp").read_text()
    header = driver.replace_once(header, "frx_acc_r[s]=65534;", "frx_acc_r[s]=UINT32_MAX-1u;")
    header = driver.replace_once(header, "batch crosses 65535 without loss", "pending total wraps modulo 2^32")
    header = driver.replace_once(header, "-batch_base[s]),65537);", "-batch_base[s]),1);")
    (work / "stream_counters.hpp").write_text(header)
    main = (here / "sim_nxn.cpp").read_text().replace(
        '#include "../../common/verilator_harness.hpp"',
        '#include "' + str(root / "tb/common/verilator_harness.hpp") + '"')
    destination = work / "sim_nxn.cpp"
    destination.write_text(main)
    return destination

driver.fixture_source = source
driver.run(1, "clean", packet / "scratch/pending-wrap", os.environ["VERILATOR"], "uncertain")
