#!/usr/bin/env python3
"""Run the page's four figure checks using the independently established pin population."""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_boundary

pins = int(sys.argv[2])
counts = ctrl_boundary.population(pins)
page = ctrl_boundary.README.read_text()
print(f'PIN_POPULATION supplied from hosted self-test and seven-target delta: {pins}')
print(f'FIGURE_POPULATION {counts}')
actual = ctrl_boundary.figures(page, counts)
print(f'CURRENT_FIGURES {actual}')
assert not actual
old = ctrl_boundary.figures(page.replace('192 pin controls', '185 pin controls'), counts)
print(f'OLD_VALUE_CONTROL {old}')
assert len(old) == 1 and 'pin controls as 185' in old[0]
bad, controls = ctrl_boundary.figure_controls(page, counts)
assert bad == 0 and controls == 4
print(f'FIGURE_CONTROLS bad={bad} count={controls}')
