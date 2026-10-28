#!/usr/bin/env python3
"""Probe: run the CPU budget harness's own image step (build.firmware) and the SoC
memory plan that split_soc.py's milan_soc.add_ctrl_memory applies, at one point.
usage: probe_harness_8x8.py <checkout> <out> <shape> <n_if>
Prints the firmware step's outcome and, if an ELF exists, ctrl_memory.plan()'s."""
import sys, json, traceback
from pathlib import Path
root, out, shape, n_if = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], int(sys.argv[4])
sys.path[:0] = [str(root / 'tb/verilator/ctrl_service_budget'), str(root / 'sw/litex')]
out.mkdir(parents=True, exist_ok=True)
import build, ctrl_memory
elf = None
try:
    elf = build.firmware(out, shape, n_if)
    print('FIRMWARE-STEP OK', elf)
except Exception as e:
    print('FIRMWARE-STEP FAILED', type(e).__name__, e)
    log = out / 'image.log'
    if log.exists():
        print('--- image.log tail ---'); print('\n'.join(log.read_text().splitlines()[-6:]))
    cand = out / 'image' / 'ctrl_app.elf'
    elf = cand if cand.exists() else None
if elf is not None:
    try:
        print('SOC-PLAN (add_ctrl_memory, no override) OK', json.dumps(ctrl_memory.plan(ctrl_memory.read_elf(elf)).summary()))
    except Exception as e:
        print('SOC-PLAN (add_ctrl_memory, no override) REFUSED', type(e).__name__, e)
