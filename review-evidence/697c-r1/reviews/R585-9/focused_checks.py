#!/usr/bin/env python3
"""Focused pin, make prerequisites and README figure checks; no build bank."""
import argparse
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('root', type=Path)
ap.add_argument('scratch', type=Path)
args = ap.parse_args()
sys.dont_write_bytecode = True
sys.path.insert(0, str(args.root.resolve() / 'sw/firmware/ctrl/test'))
import ctrl_pin as p
import ctrl_boundary as b

args.scratch.mkdir(parents=True, exist_ok=True)
print('CLEAN PIN', p.stack_pin(), flush=True)
print('CLEAN CENSUS', p.proof_census(), flush=True)
assert not p.proof_census()
bad, count = p.pin_controls(args.scratch, [p.ROOT / 'tb/verilator/mbx/Makefile'])
print('PIN CONTROLS', count, 'misbehaved', bad, flush=True)
assert bad == 0 and count == 35
found = p.makefile_findings([p.ROOT / 'tb/verilator/mbx/Makefile'], args.scratch / 'make')
print('MAKE PREREQUISITES', found, flush=True)
assert not found
counts = b.population(count)
page = b.PAGE.read_text() if hasattr(b, 'PAGE') else (p.ROOT / 'sw/firmware/ctrl/README.md').read_text()
found = b.figures(page, counts)
print('README FIGURES', counts, found, flush=True)
assert not found
bad, count = b.figure_controls(page, counts)
print('FIGURE CONTROLS', count, 'misbehaved', bad, flush=True)
assert bad == 0 and count == 4
