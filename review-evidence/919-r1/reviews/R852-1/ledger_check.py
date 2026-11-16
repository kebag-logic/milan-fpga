#!/usr/bin/env python3
"""Dependency-free boundary checks of the exact-head memory ledger, using synthetic ELF maps."""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path.cwd() / 'sw/litex'))
import ctrl_memory as m

def image(rom, ram, size=18240, stage=13594):
    return m.Image(0, (m.Section('.text', 0, 0, rom, True, False),
                       m.Section('.bss', m.RAM.origin, m.RAM.origin, ram, False, True)),
                   {m.STAGE_SYMBOL: (m.RAM.origin, stage), 'ctrl_plat': (m.RAM.origin + stage, size)},
                   ((0, bytes(rom)),))

def refused(label, fn):
    try:
        fn()
    except m.Refusal as e:
        assert e.rule == 'budget', e
        print('PASS', label, str(e))
        return
    raise AssertionError(label + ': accepted')

one = image(132148, 97392)
key = m.product_point(one)
assert key == 'platform-8x8-one-interface'
assert m.plan(one, ledgered=key).tiles == 56.5
print('PASS one-interface product selection and 56.5-tile plan')
refused('same image without product allowance', lambda: m.plan(one))
refused('one-interface half-tile excess', lambda: m.plan(image(133121, 97392), ledgered=key))
for label, bad in [('wrong ctrl_plat size', image(132148, 97392, size=18241)),
                   ('wrong staging size', image(132148, 97392, stage=13595))]:
    assert m.product_point(bad) is None
    refused(label, lambda bad=bad: m.plan(bad, ledgered=key))
two = image(133716, 114352, size=20416)
assert m.product_point(two) is None
assert m.plan(two, ledgered='platform-8x8-two-interfaces').tiles == 61
print('PASS two-interface explicit allowance and 61-tile plan')
refused('two-interface no product allowance', lambda: m.plan(two))
refused('two-interface half-tile excess',
        lambda: m.plan(image(135169, 114352, size=20416), ledgered='platform-8x8-two-interfaces'))
print('PASS: eight ledger checks; synthetic maps, not a new linked-image measurement')
