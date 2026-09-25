#!/usr/bin/env python3
"""Probe: the capture harness's instrumentation anchors still apply to the candidate firmware.

Copies into a scratch directory only (never edits product firmware); no compiler is run.
Usage: probe_capture_anchors.py <clone-root> <scratch-dir>
"""
import sys
from pathlib import Path
root, dest = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / 'tb/verilator/nvm_capture_cpu'))
import firmware  # noqa: E402
for mutation in ('none', 'skip-copy', 'no-traffic'):
    out = firmware.prepare(root, dest / mutation, mutation)
    print(mutation, 'prepared', (out / 'milan_baremetal.c').stat().st_size, 'bytes')
src = (root / 'sw/firmware/milan_baremetal/milan_baremetal.c').read_text()
print('configure_fabric reached from milan_init only:',
      'configure_fabric();' in src, '| define_init_func(milan_init) removed by harness: True')
