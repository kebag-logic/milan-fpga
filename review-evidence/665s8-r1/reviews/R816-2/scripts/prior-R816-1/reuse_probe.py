# Reviewer probe of wire_build.reused (#868): which source edits a reused build notices.
# Usage: python3 -I reuse_probe.py <checkout> <empty scratch dir>
# A synthetic build directory holds stand-ins for the built artifacts (the ELF, the .init files, the
# split archive, the native model); build.json is recorded by wire_build.inputs itself. Each probe
# appends one comment line to a tracked source the model is built from, asks reused(), and restores
# the file's exact bytes before the next probe.
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_wire_timing'))
import wire_build as wb  # noqa: E402

for rel in ('image/ctrl_app.elf', 'soc/gateware/rom.init', 'wire_config.hpp', 'split/Vtb_split_top__ALL.a',
            'native/Vsim'):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b'stand-in ' + rel.encode())
# the CPU half's tracked Verilog sources a real build records (spec['sources'], as the published CI
# step's verilate command lists them); its generated sim.v and the CPU netlist are outside the checkout
MAILBOX = ('KL_mbx_pkg.sv', 'KL_mbx_ring.sv', 'KL_mbx_rx.sv', 'KL_mbx_tx.sv', 'KL_mbx_evt.sv', 'KL_mbx.sv',
           'KL_mbx_wb.sv')
spec = dict(elf=str(OUT / 'image/ctrl_app.elf'), sources=[str(ROOT / 'hdl/milan/mailbox' / m) for m in MAILBOX])
spec['inputs'] = wb.inputs(OUT, spec)
spec['executable_sha256'] = wb.digest(OUT / 'native/Vsim')
(OUT / 'build.json').write_text(json.dumps(spec, indent=1))
print('recorded keys:', sorted(spec['inputs']))


def ask(label):
    try:
        wb.reused(OUT)
        print(f'{label}: reuse ACCEPTED')
    except RuntimeError as why:
        print(f'{label}: reuse refused: {why}')


ask('unchanged')
for rel, comment in (('tb/verilator/ctrl_wire_timing/wire_main.cpp', '// probe\n'),
                     ('tb/verilator/milan_dp/tb_split_top.sv', '// probe\n'),
                     ('hdl/milan/mailbox/KL_mbx.sv', '// probe\n'),
                     ('hdl/milan/milan_datapath.sv', '// probe\n'),
                     ('third_party/tsn-c-stack/src/maap.c', '/* probe */\n'),
                     ('sw/firmware/ctrl/maap/maap_mbx.c', '/* probe */\n')):
    path = ROOT / rel
    before = path.read_bytes()
    try:
        path.write_bytes(before + comment.encode())
        ask(f'{rel} edited')
    finally:
        path.write_bytes(before)
    assert path.read_bytes() == before
