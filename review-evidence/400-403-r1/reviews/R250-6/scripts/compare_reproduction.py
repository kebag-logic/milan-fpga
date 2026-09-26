#!/usr/bin/env python3
"""Compare reproduced capture arms with the committed receipt, row by row.

Usage: compare_reproduction.py <repo> <label>=<build-dir> [...]
Each build dir holds run.py's graded measurement.json and the instrumented
firmware/BIOS it built; their hashes are compared with the receipt too.
"""
import hashlib
import json
from pathlib import Path
import sys

repo = Path(sys.argv[1])
receipt = json.loads((repo / 'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
arms = {(a['shape'], a['cpu_hz'], a['traffic']): a for a in receipt['measurements']}
fw = hashlib.sha256((repo / 'sw/firmware/milan_baremetal/milan_baremetal.c').read_bytes()).hexdigest()
print(f"receipt product_firmware_sha256 {receipt['product_firmware_sha256']} head {fw} "
      f"{'MATCH' if fw == receipt['product_firmware_sha256'] else 'DIFFER'}")
ok = True
for spec in sys.argv[2:]:
    label, build = spec.split('=', 1)
    build = Path(build)
    mine = json.loads((build / 'measurement.json').read_text())
    ref = arms[(mine['shape'], mine['cpu_hz'], mine['traffic'])]
    same_rows = mine['rows'] == ref['rows']
    diffs = [(i, a['sys_cycles'], b['sys_cycles']) for i, (a, b) in enumerate(zip(mine['rows'], ref['rows'])) if a != b]
    inst = hashlib.sha256((build / 'measurement_firmware/milan_baremetal.c').read_bytes()).hexdigest()
    bios = build / 'software/bios/bios.bin'
    bios_h = hashlib.sha256(bios.read_bytes()).hexdigest() if bios.exists() else 'absent'
    print(f"{label}: shape={mine['shape']} cpu_hz={mine['cpu_hz']} traffic={mine['traffic']} captures={mine['captures']} "
          f"phase={mine['phase']}")
    print(f"  mine min/max ms {mine['minimum_ms']:.5f}/{mine['maximum_ms']:.5f}; receipt {ref['minimum_ms']:.5f}/{ref['maximum_ms']:.5f}")
    print(f"  rows identical to receipt: {same_rows}; differing rows: {diffs}")
    print(f"  instrumented firmware {inst} receipt {ref['instrumented_firmware_sha256']} "
          f"{'MATCH' if inst == ref['instrumented_firmware_sha256'] else 'DIFFER'}")
    print(f"  bios {bios_h} receipt {ref['bios_sha256']} {'MATCH' if bios_h == ref['bios_sha256'] else 'DIFFER'}")
    ok &= same_rows
print('ALL REPRODUCED ROWS IDENTICAL' if ok else 'SOME ROWS DIFFER')
