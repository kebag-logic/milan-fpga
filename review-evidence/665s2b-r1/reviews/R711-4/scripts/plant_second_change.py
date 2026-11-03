#!/usr/bin/env python3
"""Probe P2 (review R711-4): a save under input that leaves no pass empty (sim_main.cpp's `flood gm`, as
save-starved), with a second persisted change, a SET_NAME of the entity to another value, SECOND_MS after the
first, once the first save's capture has passed its record. The second change can only be written by the next
save, which cannot start its capture until the first save is durable (nvm_store.c, nvm_step: the idle step alone
begins a capture). analyse_second_change.py times the second save from the second change against
save_window.bound_ms.

usage: plant_second_change.py <tree> SECOND_MS   (edits <tree>/tb/verilator/ctrl_service_budget/save_window.py)
"""
import sys
from pathlib import Path

tree, second_ms = Path(sys.argv[1]), int(sys.argv[2])
path = tree / 'tb/verilator/ctrl_service_budget/save_window.py'
src = path.read_text()
probe = f'''

def second_change(p: scenario.Point, image: int) -> scenario.Group:
    """Probe P2: save-starved's flood without the held channels, and a second SET_NAME {second_ms} ms after the
    first, to another value."""
    bound = bound_ms(image, CHANGED)
    run_ms = {second_ms} + 2 * bound + 1000
    g = scenario.Group('save-second', sim_ms=int(run_ms) + 3000, save=dict(image=image, records=CHANGED))
    scenario.ready(g, p)
    scenario.announced(g)
    ms = scenario.MS
    other = f.aem_command(f.Aem(p.entity_id, scenario.CTL2, scenario.CTL_MAC, p.mac, 0x6f01), 0x0010,
                          bytes(8) + b'sav2'.ljust(64, b'\\0'))
    g.add('mark save.change', f'frame 0 {{set_name(p).hex()}}', 'flood gm 1',
          f'wait cycles {{{second_ms} * ms}}', 'mark save2.change', f'frame 0 {{other.hex()}}',
          f'wait cycles {{round(run_ms - {second_ms}) * ms}}', 'flood gm 0', 'wait quiet 3 within 2000000')
    return g
'''
anchor = '\n\ndef windows(p: scenario.Point) -> list[scenario.Group]:'
old_groups = "loaded(p, 'save-starved', True, image)"
if src.count(anchor) != 1 or src.count(old_groups) != 1:
    sys.exit('anchor not found once')
src = src.replace(anchor, probe + anchor).replace(old_groups, old_groups + ', second_change(p, image)')
path.write_text(src)
print('planted', path, second_ms)
