#!/usr/bin/env python3
"""Drive the real split SoC export with reset bytes missing from PT_LOAD."""
import json
from pathlib import Path
import struct
import sys

tree, out = map(Path, sys.argv[1:])
out.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(tree / 'sw/litex'))
import test_ctrl_memory as test
import ctrl_memory as cm

cc = test.fw_rv32.compiler()
assert cc is not None, 'RV32 compiler required'
linked = out / 'linked'
linked.mkdir(exist_ok=True)
firmware = test.link(cc, linked, (tree / 'sw/firmware/ctrl/plat/ctrl_split.ld').read_text())
data = bytearray(firmware.read_bytes())
original = cm.read_elf(firmware)
cm.plan(original)
cm.check_stage(original, 3344, '1x1')
original_words = cm.rom_words(original)
phoff = struct.unpack_from('<I', data, 28)[0]
phentsize, phnum = struct.unpack_from('<HH', data, 42)
targets = []
for n in range(phnum):
    at = phoff + n * phentsize
    kind, offset, vaddr, paddr, filesz, memsz, flags, align = struct.unpack_from('<8I', data, at)
    if kind == 1 and vaddr <= original.entry < vaddr + memsz and filesz:
        targets.append(at)
assert len(targets) == 1
struct.pack_into('<I', data, targets[0] + 16, 0)
bad = out / 'missing-reset-load.elf'
bad.write_bytes(data)
result = test.soc_case(out, 'missing reset load', ['--ctrl-mailbox', '--ctrl-firmware', str(bad)], None)
first = sorted(result['out'].glob('gateware/*_rom_bank0.init'))
words = first[0].read_text().split() if first else []
print(json.dumps({'build_rc': result['rc'], 'refusal': result.get('refusal'),
                  'error': result.get('error'), 'verilog_count': len(result['verilog']),
                  'first_eight_programmed_words': words[:8],
                  'original_first_eight_words': [f'{w:08x}' for w in original_words[:8]],
                  'changed_field': 'p_filesz of the PT_LOAD containing _start',
                  'fixture': 'linked with the exact-head reset assembly and linker script'}, indent=2))
assert result['rc'] == 0 and len(result['verilog']) == 1
assert words and all(int(w, 16) == 0 for w in words[:8])
print('REPRODUCED: named reset-bytes refusal bypassed; split export programs zeros at reset')
