#!/usr/bin/env python3
"""Probe P1 (review R711-4): stage backlog-adp's composed window in a save's blank phase, opened after a
grandmaster-change flood of F ms (sim_main.cpp's `flood gm`, the same input save-starved uses), so that the
store's step age is not zero when the window opens. The flood stops just before the window opens
(scenario.OPEN_WINDOW waits for the event ring to drain), so the window's own population is unchanged.

usage: plant_aged_window.py <tree> F1,F2,...   (edits <tree>/tb/verilator/ctrl_service_budget/save_window.py)
"""
import sys
from pathlib import Path

tree, floods = Path(sys.argv[1]), [int(x) for x in sys.argv[2].split(',')]
path = tree / 'tb/verilator/ctrl_service_budget/save_window.py'
src = path.read_text()

old_sig = 'def window(p: scenario.Point, phase: str, k: int) -> scenario.Group:'
new_sig = 'def window(p: scenario.Point, phase: str, k: int, flood_ms: int = 0) -> scenario.Group:'
old_name = "    g = scenario.Group(row_names()[list(PHASES).index(phase) * TICK_PHASES + k], sim_ms=8000)"
new_name = ("    g = scenario.Group(row_names()[list(PHASES).index(phase) * TICK_PHASES + k] if not flood_ms else\n"
            "                       f'backlog-adp@{phase}-F{flood_ms}', sim_ms=8000)")
old_open = ("          f'wait flash {event} within {6000 * ms}', f'wait cycles {(delay + k * period / TICK_PHASES) * ms:.0f}',\n"
            "          *scenario.OPEN_WINDOW)")
new_open = ("          f'wait flash {event} within {6000 * ms}', f'wait cycles {(delay + k * period / TICK_PHASES) * ms:.0f}',\n"
            "          *((['flood gm 1', f'wait cycles {flood_ms * ms}', 'flood gm 0']) if flood_ms else []),\n"
            "          *scenario.OPEN_WINDOW)")
old_groups = "    return [*windows(p), alone(p, image), loaded(p, 'save-held', False, image), loaded(p, 'save-starved', True, image)]"
new_groups = ("    return [*windows(p), alone(p, image), loaded(p, 'save-held', False, image), loaded(p, 'save-starved', True, image),\n"
              f"            *(window(p, 'blank', 0, F) for F in {floods!r})]")
for old, new in ((old_sig, new_sig), (old_name, new_name), (old_open, new_open), (old_groups, new_groups)):
    if src.count(old) != 1:
        sys.exit(f'anchor not found once: {old[:60]!r}')
    src = src.replace(old, new)
path.write_text(src)
print('planted', path, floods)
