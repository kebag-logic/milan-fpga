#!/usr/bin/env python3
"""cap_probe.py TREE OUT [VARIANT ...]: link the CPU budget harness's 8x8/2if image (the size fixture, ledgered point
8x8-two-interfaces) of TREE through its own build.firmware, once unmodified ('none') and once per named variant arm,
on the RV32 stand-ins (no flash map), and print each image's rc, rom, sram and tiles from its size.json. A link the
planner refuses past the ledger's tiles is rc 1 with its log's last lines."""
import json
import subprocess
import sys
from pathlib import Path

tree, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
variants = sys.argv[3:] or ['none', 'answering-every-port']
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import build  # noqa: E402

for v in variants:
    o = out / v
    try:
        elf = build.firmware(o, 'endstation_ax7101_8x8', 2, variant=v)
        s = json.loads((elf.parent / 'size.json').read_text())['split']
        print(f"{v}: rc 0 rom {s['rom']['bytes']} sram {s['sram']['bytes']} tiles {s['tiles']} "
              f"rom banks {sum(s['rom']['banks'])} sram banks {sum(s['sram']['banks'])}")
    except (subprocess.CalledProcessError, RuntimeError, FileNotFoundError) as e:
        log = o / 'image.log'
        tail = log.read_text().strip().splitlines()[-6:] if log.is_file() else [repr(e)]
        print(f"{v}: rc 1 ({type(e).__name__})")
        for line in tail:
            print(f"    {line[:300]}")
