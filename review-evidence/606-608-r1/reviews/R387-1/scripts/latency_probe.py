#!/usr/bin/env python3
"""Instrument a DISPOSABLE copy of tb/verilator/pp_shadow/sim_main.cpp so each
#608 withdrawal phase prints the clocks from just before the Leave injection to
the first cycle the CRF licence (crft_emit_en_w) reads 0. Read-only observation;
no check is added, removed or changed. Usage: latency_probe.py <copy/sim_main.cpp>
then `make run-crf SIM_ARGS=--crf-stop-only` in that copy."""
import sys
from pathlib import Path

path = Path(sys.argv[1])
src = path.read_text()
old = "        while (cycle_count < withdrawal_cycle + kCrfPeriodCycles) step();"
new = """        uint64_t off_cycle = 0;
        while (cycle_count < withdrawal_cycle + kCrfPeriodCycles) {
            step();
            if (!off_cycle && !dut->rootp->milan_datapath__DOT__crft_emit_en_w) off_cycle = cycle_count;
        }
        printf("LATENCY phase=%s licence_off_after=%llu clocks (from before injection)\\n", phase,
               static_cast<unsigned long long>(off_cycle ? off_cycle - withdrawal_cycle : 0));"""
if src.count(old) != 1:
    sys.exit("anchor not found exactly once")
path.write_text(src.replace(old, new))
