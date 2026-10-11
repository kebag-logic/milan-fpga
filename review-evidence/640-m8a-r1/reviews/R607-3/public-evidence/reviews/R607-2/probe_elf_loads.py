#!/usr/bin/env python3
"""Probe the correspondence between allocated sections and programmed ROM bytes."""
import argparse
from pathlib import Path
import struct
import sys

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('tree', type=Path)
ap.add_argument('out', type=Path)
a = ap.parse_args()
a.out.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(a.tree / 'sw/litex'))
import ctrl_memory as cm
import test_ctrl_memory as test

good = test.elf(a.out, test.GOOD)
raw = good.read_bytes()
image = cm.read_elf(good)
print('CONTROL:', cm.plan(image).rom_bytes, 'ROM bytes;', len(cm.rom_words(image)), 'initial words')

for name, edit in (
    ('no-load-segments', lambda b: struct.pack_into('<H', b, 44, 0)),
    ('reset-segment-empty', lambda b: struct.pack_into('<I', b, 52 + 16, 0)),
    ('reset-segment-short', lambda b: struct.pack_into('<I', b, 52 + 16, 4)),
):
    data = bytearray(raw)
    edit(data)
    path = a.out / (name + '.elf')
    path.write_bytes(data)
    try:
        img = cm.read_elf(path)
        plan = cm.plan(img)
        cm.check_stage(img, 3344, '1x1')
        words = cm.rom_words(img)
        print(name, 'ACCEPTED', 'planned_rom_bytes', plan.rom_bytes,
              'initial_words', len(words), 'first_two_words', words[:2])
    except cm.Refusal as exc:
        print(name, 'REFUSED', exc.check, exc.rule)

for n in (6, 7, 16, 20, 40, 51):
    path = a.out / ('cut-' + str(n) + '.elf')
    path.write_bytes(raw[:n])
    try:
        cm.read_elf(path)
        raise AssertionError('truncated header accepted')
    except cm.Refusal as exc:
        assert exc.rule == 'elf truncated'
        print('header-cut', n, 'REFUSED', exc.check, exc.rule)
