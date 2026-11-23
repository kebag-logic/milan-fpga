#!/usr/bin/env python3
"""Focused pin-control and README-figure check; all probe output stays in scratch."""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
(scratch / 'pins').mkdir(exist_ok=True)
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_pin
import ctrl_boundary
from ctrl_configs import makefiles

bad, count = ctrl_pin.pin_controls(scratch / 'pins', makefiles())
print(f'PIN_RESULT bad={bad} count={count}', flush=True)
page = ctrl_boundary.README.read_text()
counts = ctrl_boundary.population(count)
print(f'FIGURE_POPULATION {counts}', flush=True)
findings = ctrl_boundary.figures(page, counts)
print(f'CURRENT_FIGURES {findings}', flush=True)
old = page.replace('192 pin controls', '185 pin controls')
negative = ctrl_boundary.figures(old, counts)
print(f'OLD_VALUE_CONTROL {negative}', flush=True)
controls_bad, controls = ctrl_boundary.figure_controls(page, counts)
print(f'FIGURE_CONTROLS bad={controls_bad} count={controls}', flush=True)
assert bad == 0 and count == 192
assert not findings
assert len(negative) == 1 and 'pin controls as 185' in negative[0]
assert controls_bad == 0 and controls == 4
