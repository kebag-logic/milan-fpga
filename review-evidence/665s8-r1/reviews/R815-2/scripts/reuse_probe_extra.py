#!/usr/bin/env python3
"""Reviewer probe of wire_build.reused at both points' recipe variables: a stand-in build directory recorded by
wire_build.inputs itself (with the shape and split_vars a real build records), then one real edit of each
source kind not named by the round-1 probes, each restored byte-for-byte.

usage: reuse_probe_extra.py <disposable checkout> <empty scratch dir>
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_wire_timing'))
import wire_build as wb  # noqa: E402

POINTS = {'1x1': ('endstation_ax7101_1x1_tdm8', 1), '8x8': ('endstation_ax7101_8x8', 2)}
EDITS = (('tb/verilator/milan_dp/Makefile', b'\n# probe\n'),
         ('hdl/milan/mailbox/KL_mbx_cdc.sv', b'\n// probe\n'),
         ('third_party/verilog-axis/rtl/axis_async_fifo.v', b'\n// probe\n'),
         ('third_party/lwSRP/README.md', b'\nprobe\n'),
         ('sw/mailbox/mailbox.yaml', b'\n# probe\n'),
         ('tb/verilator/ctrl_service_budget/build.py', b'\n# probe\n'),
         ('tb/verilator/ctrl_split_boot/run.py', b'\n# probe\n'))
rc = 0
for point, (shape, n_if) in POINTS.items():
    out = OUT / point
    for rel in ('image/ctrl_app.elf', 'soc/gateware/rom.init', 'wire_config.hpp', f'split/{wb.SPLIT_ARCHIVE}',
                'native/Vsim'):
        (out / rel).parent.mkdir(parents=True, exist_ok=True)
        (out / rel).write_bytes(b'stand-in ' + rel.encode())
    spec = dict(elf=str(out / 'image/ctrl_app.elf'), sources=[str(ROOT / 'hdl/milan/mailbox/KL_mbx_wb.sv')],
                shape=shape, split_vars=wb.split_vars(shape, n_if))
    spec['inputs'] = wb.inputs(out, spec)
    spec['executable_sha256'] = wb.digest(out / 'native/Vsim')
    (out / 'build.json').write_text(json.dumps(spec))
    keys = sorted(spec['inputs'])
    print(f'{point}: {len(keys)} keys recorded; split_vars {spec["split_vars"]}; '
          f'config key {"configs/" + shape + ".yaml" in keys}')
    edits = (*EDITS, (f'configs/{shape}.yaml', b'\n# probe\n'))
    for rel, extra in ((None, b''), *edits):
        path = ROOT / rel if rel else None
        before = path.read_bytes() if path else b''
        try:
            if path:
                path.write_bytes(before + extra)
            try:
                wb.reused(out)
                verdict = 'ACCEPTED'
            except RuntimeError as why:
                verdict = f'refused: {why}'
        finally:
            if path:
                path.write_bytes(before)
        ok = verdict == 'ACCEPTED' if rel is None else verdict.startswith('refused') and (
            'missing separator' not in verdict)
        rc |= not ok
        print(f'  {point} {rel or "unchanged"}: {verdict[:200]} -> {"as required" if ok else "UNEXPECTED"}')
status = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--ignore-submodules=none'],
                        capture_output=True, text=True).stdout
print('tree restored:', not status.strip(), status.strip()[:200])
sys.exit(rc or bool(status.strip()))
