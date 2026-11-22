#!/usr/bin/env python3
"""Exercise only memory ledger facts and the product allocator, no builder bank."""
import dataclasses
import functools
import sys
from pathlib import Path

repo, out = (Path(x).resolve() for x in sys.argv[1:3])
out.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(repo / 'sw/litex'))
import test_ctrl_memory as t
import ctrl_memory as m
import ctrl_memory_ledger as l

write = functools.partial(t.ledger_elf, out)
facts = list(l.facts(write)) + list(l.product_facts(write, t.soc_plan))
for ok, what in facts:
    print('PASS' if ok else 'FAIL', what)
assert all(ok for ok, _ in facts)
original = m.LEDGERED
try:
    m.LEDGERED = dict(original)
    m.LEDGERED[l.PRODUCT] = dataclasses.replace(original[l.PRODUCT], tiles=59.0)
    broken = list(l.facts(write))
    assert any(not ok for ok, _ in broken)
    print('PASS widened 59.0 entry detected by independent ledger facts')
finally:
    m.LEDGERED = original
print('PASS focused ledger: 58.5 accepted, 59.0 refused; widened-entry control caught')
