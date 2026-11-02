# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""A save in a composed window (#665): the heaviest window staged during each flash phase of a save.

A persisted change starts a save of the saved-state store (sw/firmware/ctrl_nvm/nvm_store.c): after the
1,000 ms first-dirty window it captures and seals, erases the slot that is not authoritative, checks it
blank, programs it a page at a time and reads it back. The flash phases put a heavy step on the store's
ticks: a 128-byte read-back on every tick of the blank check and of the verify, and a page program's
issue on every other tick of the program phase. Each group opens backlog-adp's window
(scenario.bound_talker_groups, at the burst), the heaviest the budget stages, at one phase of that step's
period, so some pass of the window meets the step if any can: eight phases 1.25 ms apart across the
10 ms tick for the blank check and the verify, and eight 2.5 ms apart across the program phase's 20 ms.
A phase starts at a flash event of the save itself, which sim_main.cpp's `wait flash` observes: the
erase, the first page program, and the first 30 ms with no program after the last one. The SET_NAME that
starts the save comes SET_MS into the 2 s the window waits for MAAP (scenario.announced), so the save's
first-dirty window and seal run beside it and its erase still follows the window's set-up at both points;
grade.save_phase refuses a window that did not open inside its phase.

A group is named backlog-adp@<phase>-<k>: grade.defined_load holds its window to backlog-adp's defined
load, its probe is an instance of backlog-adp's path and its records of the composed rows' paths, and
grade.pass_share holds every pass of the group to the share. The group `save` is one save with no other
load, marked at its change (save.change), run past its last step: each step's cost and the save's time
from the change to durable are read off its passes.
"""
from __future__ import annotations

import frames as f
import scenario

#: Each flash phase: the flash event it starts after (sim_main.cpp's `wait flash`), then the delay into
#: the phase and the heavy step's period, in ms. The verify starts once IDLE_MS pass with no page program.
PHASES = {'blank': ('erase 1', 30, 10), 'program': ('program 1', 30, 20), 'verify': ('idle', 10, 10)}
IDLE_MS = 30
#: The SET_NAME's time after ready, inside the wait for MAAP.
SET_MS = 1100
#: The tick phases staged in each flash phase.
TICK_PHASES = 8


def set_name(p: scenario.Point) -> bytes:
    """A SET_NAME of the entity's name, which the store persists (IEEE 1722.1-2021 7.4.17)."""
    name = b'save'.ljust(64, b'\0')
    return f.aem_command(f.Aem(p.entity_id, scenario.CTL2, scenario.CTL_MAC, p.mac, 0x6f00), 0x0010,
                         bytes(8) + name)


def window(p: scenario.Point, phase: str, k: int) -> scenario.Group:
    """backlog-adp's window opened at tick phase k of a save's flash phase."""
    ms = scenario.MS
    acmp, adp, aecp = scenario.CH['acmp'], scenario.CH['adp'], scenario.CH['aecp']
    disc = f.adp(f.ADP_DISCOVER, 0, scenario.CTL_MAC, f.Adp(valid_time=0))
    caps = dict(talker_sources=1, talker_caps=0x4001)
    gone = f.adp(f.ADP_DEPARTING, scenario.TALKER_A, scenario.TALKER_A_MAC, f.Adp(valid_time=0, **caps))
    avail = f.adp(f.ADP_AVAILABLE, scenario.TALKER_A, scenario.TALKER_A_MAC, f.Adp(valid_time=10, **caps))
    last_gm = max(n for n in range(15) if n % p.interfaces == 0)
    current = f.adp(f.ADP_AVAILABLE, scenario.TALKER_A, scenario.TALKER_A_MAC,
                    f.Adp(valid_time=10, gm_id=0x0A0B0C0DFFFE0000 + last_gm, **caps))
    event, delay, period = PHASES[phase]
    event = f'idle {IDLE_MS * ms}' if event == 'idle' else event
    g = scenario.Group(row_names()[list(PHASES).index(phase) * TICK_PHASES + k], sim_ms=8000)
    scenario.ready(g, p)
    # scenario.announced's wait for MAAP, with the SET_NAME inside it; backlog-adp's bound talker's bind is
    # persisted too, and joins the same save
    g.add(f'wait cycles {SET_MS * ms}', f'frame 0 {set_name(p).hex()}', f'wait tx {aecp} 1 within {50 * ms}',
          f'wait cycles {(2000 - SET_MS) * ms}', 'wait quiet 3 within 2000000',
          f'frame 0 {scenario.acmp_cmd(p, "BIND_RX", 0, 0x7000).hex()}', f'wait tx {acmp} 2 within {20 * ms}',
          'wait quiet 3 within 2000000', f'frame 0 {avail.hex()}', 'wait quiet 3 within 2000000',
          f'frame 0 {gone.hex()}', f'wait cycles {50 * ms}', 'wait quiet 3 within 2000000',
          f'wait flash {event} within {6000 * ms}', f'wait cycles {(delay + k * period / TICK_PHASES) * ms:.0f}',
          *scenario.OPEN_WINDOW)
    scenario.gm_run(g, p)
    scenario.composed_load(g, p, own='adp')
    for n in range(scenario.admission('adp', disc)['at_once'] - 1):
        g.offer('adp', f'frame {n % p.interfaces} {disc.hex()}', disc)
    probe = scenario.Probe(f'{g.name}.adp_available.if0', 'an ENTITY_AVAILABLE behind a full adp ring', 'disc',
                           f'rxc:{adp}', [f'arm:{p.interfaces}'], until='composed_end', path='backlog.adp_available')
    g.probe(probe, f'frame 0 {current.hex()}', wait=f'tmr {p.interfaces} 1 within {400 * ms}',
            settle='quiet 3 within 50000000')
    g.load['adp'] += 1
    g.add('mark composed_end')
    return g


def alone(p: scenario.Point) -> scenario.Group:
    """One save with no other load, from the change to 5.2 s after it."""
    g = scenario.Group('save', sim_ms=6000)
    scenario.ready(g, p)
    ms = scenario.MS
    g.add('mark save.change', f'frame 0 {set_name(p).hex()}', f'wait tx {scenario.CH["aecp"]} 1 within {50 * ms}',
          f'wait cycles {5200 * ms}')
    return g


def groups(p: scenario.Point) -> list[scenario.Group]:
    """The window at every tick phase of every flash phase, and the save alone."""
    return [*(window(p, phase, k) for phase in PHASES for k in range(TICK_PHASES)), alone(p)]


def row_names() -> list[str]:
    """The groups' names, at any point: build.py's planted store step runs them."""
    return [f'backlog-adp@{phase}-{k}' for phase in PHASES for k in range(TICK_PHASES)]


def row(name: str) -> str:
    """The backlog row a group's window is: its name, but backlog-adp for a save's."""
    return name.partition('@')[0]
