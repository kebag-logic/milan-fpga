#!/usr/bin/env python3
"""Independent section accounting and disassembler whitelist, without ctrl_image imports.

Usage: python3 audit_images.py SCRATCH_IMAGES COMPILER RECEIPT_DIRECTORY
"""
from collections import Counter
import hashlib
from pathlib import Path
import re
import struct
import subprocess
import sys

images, cc, receipts = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
prefix = cc.removesuffix('gcc')
allowed = set('lui auipc jal jalr beq bne blt bge bltu bgeu lb lh lw lbu lhu sb sh sw addi slti sltiu xori ori andi slli srli srai add sub sll slt sltu xor srl sra or and fence ecall ebreak'.split())
expected = {
    ('head', 'endstation_ax7101_1x1_tdm8'): (27700, 736, 0, 11280),
    ('head', 'endstation_ax7101_8x8'): (27704, 736, 0, 21648),
    ('base', 'endstation_ax7101_1x1_tdm8'): (16848, 700, 0, 6432),
    ('base', 'endstation_ax7101_8x8'): (16852, 700, 0, 16784),
}
for (side, shape), sizes in expected.items():
    elf = images / side / shape / 'ctrl_app.elf'
    data = elf.read_bytes()
    assert data[:7] == b'\x7fELF\x01\x01\x01'
    assert struct.unpack_from('<HH', data, 16) == (2, 243)
    assert struct.unpack_from('<I', data, 36)[0] == 0
    offset = struct.unpack_from('<I', data, 32)[0]
    width, count, names_index = struct.unpack_from('<HHH', data, 46)
    headers = [struct.unpack_from('<10I', data, offset + width * i) for i in range(count)]
    strings = headers[names_index][4]
    sections = {}
    code_bytes = 0
    for name, kind, flags, addr, start, length, *_ in headers:
        label = data[strings + name:].split(b'\0', 1)[0].decode()
        if flags & 2:
            sections[label] = length
        if flags & 4:
            assert addr % 4 == 0 and length % 4 == 0 and kind != 8
            code_bytes += length
    assert set(sections) <= {'.text', '.rodata', '.data', '.bss'}
    actual = tuple(sections.get('.' + name, 0) for name in ('text', 'rodata', 'data', 'bss'))
    assert actual == sizes, (side, shape, actual, sizes)
    header = subprocess.check_output([prefix + 'readelf', '-h', '-A', '-S', '-W', str(elf)], text=True)
    assert re.findall(r'Tag_RISCV_arch: "([^"]+)"', header) == ['rv32i2p1']
    assert not subprocess.check_output([prefix + 'nm', '-u', str(elf)]).strip()
    dis = subprocess.check_output([prefix + 'objdump', '-d', '-z', '-M', 'no-aliases,numeric', str(elf)], text=True)
    words = re.findall(r'^\s*([0-9a-f]+):\s+([0-9a-f]+)\s+(\S+)', dis, re.M)
    assert sum(len(raw) // 2 for _, raw, _ in words) == code_bytes
    assert all(len(raw) == 8 and instruction in allowed for _, raw, instruction in words)
    nm = subprocess.check_output([prefix + 'nm', '-S', '--defined-only', str(elf)], text=True)
    helper_names = {'__lshrdi3', '__muldi3', '__mulsi3', '__udivdi3', '__umoddi3', 'image_udivmod64'}
    helpers = {fields[3]: int(fields[1], 16) for line in nm.splitlines()
               if len(fields := line.split()) == 4 and fields[3] in helper_names}
    assert set(helpers) == helper_names and sum(helpers.values()) == 412
    runtime = {fields[3]: int(fields[1], 16) for line in nm.splitlines()
               if len(fields := line.split()) == 4 and fields[3] in {'memset', 'memcpy'}}
    assert sum(runtime.values()) == 64
    print(f'PASS {side}/{shape}: sections {actual}, total {sum(actual)}, {len(words)} RV32I words')
    print(f'ELF sha256 {hashlib.sha256(data).hexdigest()}; e_flags=0; ELF32 LE RISC-V executable; rv32i2p1; undefined=0')
    print(f'helpers {helpers}; runtime {runtime}; instructions {dict(sorted(Counter(i for _, _, i in words).items()))}')
    (receipts / f'{side}-{shape}.readelf.txt').write_text(header + '\n' + nm)
print('PASS: 4/4 images independently checked; section totals and deltas reproduce the README')
