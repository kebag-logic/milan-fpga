#!/usr/bin/env python3
"""Collect focused.py's platform coverage with the repository's declared exclusions."""
import contextlib
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
packet = Path(__file__).resolve().parent
os.environ['TMPDIR'] = str(packet / 'scratch')
sys.path.insert(0, str(Path.cwd() / 'sw/firmware/gtest'))
import fw_coverage as c

raw = c.collect([packet / 'scratch/platform/build'])
selected = {p:v for p,v in raw.items() if p.startswith('sw/firmware/ctrl/plat/')}
assert len(selected) == 4
before = c.tally(selected)
rows = [r for r in c.exclusions(c.README.read_text()) if r.file in selected]
kept, found = c.apply_exclusions(selected, rows)
after = c.tally(kept)
ratchet = {p:v for p,v in c.read_ratchet(c.RATCHET.read_text()).items() if p in selected}
with (packet / 'coverage.log').open('w') as f, contextlib.redirect_stdout(f):
    print('Focused exact-head coverage of four newly instrumented platform C files.')
    print('Main is not in the host coverage population; it executes in the published boot simulation.')
    print('The existing mailbox MMIO file is in the published 35-file full coverage receipt.')
    c.report(before, after)
    print('Exclusion findings:', found)
    print('Ratchet findings:', c.compare(after, ratchet))
raise SystemExit(bool(found or c.compare(after, ratchet)))
