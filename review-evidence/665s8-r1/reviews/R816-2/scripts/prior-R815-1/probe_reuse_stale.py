#!/usr/bin/env python3
"""Probe: does wire_build.reused() refuse a build after the split top's source, the datapath RTL or the firmware
source changes? A synthetic build directory is recorded with wire_build.inputs(), then one source of each kind is
changed in the (disposable) checkout and reused() is asked. Every change is restored before exit.

usage: probe_reuse_stale.py <disposable checkout> <scratch dir>
"""
import json, shutil, subprocess, sys
from pathlib import Path
root, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_wire_timing'))
import wire_build as wb
out = scratch / 'reuse-probe'
shutil.rmtree(out, ignore_errors=True)
(out / 'soc/gateware').mkdir(parents=True)
(out / 'split').mkdir()
(out / 'native').mkdir()
for p, text in ((out / 'image/ctrl_app.elf', 'elf'), (out / 'soc/gateware/mem.init', 'init'),
                (out / 'wire_config.hpp', 'cfg'), (out / 'split' / wb.SPLIT_ARCHIVE, 'archive'),
                (out / 'native/Vsim', 'exe')):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
spec = dict(elf=str(out / 'image/ctrl_app.elf'), sources=[str(root / 'hdl/milan/mailbox/KL_mbx_wb.sv')])
spec['inputs'] = wb.inputs(out, spec)
spec['executable_sha256'] = wb.digest(out / 'native/Vsim')
(out / 'build.json').write_text(json.dumps(spec))
print('recorded input keys:', sorted(spec['inputs']))
changes = ['tb/verilator/milan_dp/tb_split_top.sv', 'hdl/milan/mailbox/KL_mbx.sv', 'hdl/milan/KL_ctrl_split.sv',
           'sw/firmware/ctrl/maap/maap_mbx.c', 'tb/verilator/milan_dp/Makefile', 'hdl/milan/mailbox/KL_mbx_wb.sv']
rc = 0
for rel in changes:
    path = root / rel
    original = path.read_bytes()
    try:
        path.write_bytes(original + b'\n// probe\n')
        try:
            wb.reused(out)
            verdict = 'ACCEPTED (stale build reused)'
        except RuntimeError as why:
            verdict = f'refused: {why}'
    finally:
        path.write_bytes(original)
    print(f'{rel}: {verdict}')
status = subprocess.run(['git', '-C', str(root), 'status', '--porcelain', '--untracked-files=no'], capture_output=True,
                        text=True).stdout
print('tracked tree restored:', status.strip() == '')
