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

A save's worst case (bound_ms) follows from THE STEP's age limit (ctrl_loop.h): input that leaves no pass
empty holds a step off for at most CTRL_LOOP_STEP_AGE centiseconds, so the store steps at least once every
CTRL_LOOP_STEP_AGE + 1 ticks, and a save takes its first-dirty window and then its steps (steps) at that pace
at worst. `save-held` holds every receive channel at its contract refill rate with its bursts (loaded) through
a whole save; `save-starved` adds a grandmaster change as every pass starts (sim_main.cpp's flood), an event
source the contract coalesces but does not rate, so no pass takes nothing and the store steps only through its
age limit. save_grade.save_time times each save from its change to durable against bound_ms, save_grade.held
gives each channel's longest record, and build.py's store-step-ageless, the age limit removed, leaves
save-starved's save not durable within it.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

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
#: The store's first-dirty window (DR2a, MILAN_NVM_DEBOUNCE_MS) and its tick, in ms (nvm_store.c).
DIRTY_MS, TICK_MS = 1000, 10
#: A seal step's and a page program's stretch, a read-back's, and the container's trailer, in bytes (nvm_store.c,
#: NVM_STEP_BYTES and NVM_READ_BYTES; nvm_klj2.h).
PAGE, READ, TRAILER = 256, 128, 4
#: The records a SET_NAME of the entity's name marks: both of the entity's names, as aecp_nvm.c marks every name of
#: the descriptor a SET_NAME names.
CHANGED = 2
#: The change's own pass, which marks its record, and the passes between a tick's posting and the aged pass it
#: triggers (the event's pass bound and the aged pass, each within the 2.0 ms share, ctrl_loop.h), in ms.
SLACK_MS = 10
#: An aged window (aged_window) opens this many ms after the last centisecond of its age was posted: TICK_PHASES
#: delays spread evenly across the whole tick, so the aged step the next centisecond brings lands anywhere in the
#: window's first tick (at the age limit) or its second (one short of it).
AGED_DELAYS = tuple(TICK_MS * (n + 0.5) / TICK_PHASES for n in range(TICK_PHASES))
#: The store's steps an aged window lets pass under the flood after its phase's flash event, so the phase's heavy step
#: is next: the erase's issue and its one wait before the first blank-check read-back, a page's issue and its wait
#: before the next page's issue, two of the verify's read-backs before the next.
AGED_LEAD = 2
#: A change in flight's second change (second), after the first's mark: its first-dirty window, the step that starts
#: its capture 20 ms past it under the flood (the first change marks just after a step), and 15 ms, half a step period
#: short of the step that takes the entity's first name.
SECOND_MS = DIRTY_MS + 35
#: The receive channels' bursts start this far apart, in ms, so no burst queues behind another's at the
#: ingress and each channel's arrivals keep their period exactly (KL_mbx_rx.sv refills on the ms tick).
OFFSET_MS = 0.2


#: The record header of look-ahead the stage holds past the container (nvm_shape.h, NVM_STAGE_BYTES).
REC_HDR = 8


def container(build: dict) -> int:
    """An image's saved-state container length, NVM_IMG_LEN: its stage, nvm_stage, less that look-ahead."""
    symbols = Path(build['elf']).with_name('symbols.txt').read_text().splitlines()
    return next(int(line.split()[1], 16) for line in symbols if line.split()[-1] == 'nvm_stage') - REC_HDR


def step_age() -> int:
    """THE STEP's age limit, CTRL_LOOP_STEP_AGE, read from ctrl_loop.h, so a changed limit restates the bound."""
    header = (Path(__file__).resolve().parents[3] / 'sw/firmware/ctrl/loop/ctrl_loop.h').read_text()
    return int(re.search(r'#define CTRL_LOOP_STEP_AGE (\d+)u', header).group(1))


def steps(image: int, records: int) -> int:
    """A save's steps from the first after its first-dirty window to durable, with no flash busy time
    (nvm_store.c): the step that starts the capture, one for each changed record and one that finds none left,
    the seal's PAGE-byte stretches of the container less its trailer, the erase and its one wait, the blank
    check's READ-byte read-backs, each page's issue and its one wait, and the verify's read-backs."""
    pages, reads = math.ceil(image / PAGE), math.ceil(image / READ)
    return 1 + records + 1 + math.ceil((image - TRAILER) / PAGE) + 2 + reads + 2 * pages + reads


def bound_ms(image: int, records: int, age: int | None = None, flight: int | None = None) -> int:
    """A change's worst case from its mark to durable: its first-dirty window, then each step of its save at most
    age + 1 ticks after the one before (THE STEP's age limit), and SLACK_MS. A change marked while a save of flight
    records is in flight, after that save's capture took the first record the change names (nvm_store.c, nvm_mark),
    waits for the rest of that save, its steps less the two that started its capture and took that record, at the
    same pace, or its own first-dirty window if that is longer, before its own save's steps. A flash part's busy
    time adds its erase's polls, one a step."""
    age = step_age() if age is None else age
    per = (age + 1) * TICK_MS
    wait = DIRTY_MS if flight is None else max(DIRTY_MS, (steps(image, flight) - 2) * per)
    return wait + steps(image, records) * per + SLACK_MS


def set_name(p: scenario.Point, value: bytes = b'save') -> bytes:
    """A SET_NAME of the entity's name, which the store persists (IEEE 1722.1-2021 7.4.17)."""
    name = value.ljust(64, b'\0')
    return f.aem_command(f.Aem(p.entity_id, scenario.CTL2, scenario.CTL_MAC, p.mac, 0x6f00), 0x0010,
                         bytes(8) + name)


def window(p: scenario.Point, phase: str, k: int) -> scenario.Group:
    """backlog-adp's window opened at tick phase k of a save's flash phase."""
    event, delay, period = PHASES[phase]
    return staged(p, row_names()[list(PHASES).index(phase) * TICK_PHASES + k], phase,
                  [f'wait cycles {(delay + k * period / TICK_PHASES) * scenario.MS:.0f}'])


def aged_window(p: scenario.Point, phase: str, age: int, n: int) -> scenario.Group:
    """backlog-adp's window opened in a save's flash phase with THE STEP's age at `age` centiseconds, AGED_DELAYS[n]
    ms after the last of them was posted: a grandmaster change as every pass starts from the phase's flash event
    (sim_main.cpp's flood), so no pass takes nothing and the store steps only through its age limit, AGED_LEAD steps,
    which leave the phase's heavy step next, then `age` centiseconds, then the window."""
    ms = scenario.MS
    return staged(p, f'backlog-adp@{phase}-aged{age}-{n}', phase,
                  ['flood gm 1', f'wait steps {AGED_LEAD} within {200 * ms}', f'wait ticks {age} within {40 * ms}',
                   f'wait cycles {AGED_DELAYS[n] * ms:.0f}', 'flood gm 0'])


def staged(p: scenario.Point, name: str, phase: str, opening: list[str]) -> scenario.Group:
    """backlog-adp's window, its set-up's SET_NAME starting a save, opened by `opening` after the save's flash
    event that starts the phase."""
    ms = scenario.MS
    acmp, adp, aecp = scenario.CH['acmp'], scenario.CH['adp'], scenario.CH['aecp']
    disc = f.adp(f.ADP_DISCOVER, 0, scenario.CTL_MAC, f.Adp(valid_time=0))
    caps = dict(talker_sources=1, talker_caps=0x4001)
    gone = f.adp(f.ADP_DEPARTING, scenario.TALKER_A, scenario.TALKER_A_MAC, f.Adp(valid_time=0, **caps))
    avail = f.adp(f.ADP_AVAILABLE, scenario.TALKER_A, scenario.TALKER_A_MAC, f.Adp(valid_time=10, **caps))
    last_gm = max(n for n in range(15) if n % p.interfaces == 0)
    current = f.adp(f.ADP_AVAILABLE, scenario.TALKER_A, scenario.TALKER_A_MAC,
                    f.Adp(valid_time=10, gm_id=0x0A0B0C0DFFFE0000 + last_gm, **caps))
    event = PHASES[phase][0]
    event = f'idle {IDLE_MS * ms}' if event == 'idle' else event
    g = scenario.Group(name, sim_ms=8000)
    scenario.ready(g, p)
    # scenario.announced's wait for MAAP, with the SET_NAME inside it; backlog-adp's bound talker's bind is
    # persisted too, and joins the same save
    g.add(f'wait cycles {SET_MS * ms}', f'frame 0 {set_name(p).hex()}', f'wait tx {aecp} 1 within {50 * ms}',
          f'wait cycles {(2000 - SET_MS) * ms}', 'wait quiet 3 within 2000000',
          f'frame 0 {scenario.acmp_cmd(p, "BIND_RX", 0, 0x7000).hex()}', f'wait tx {acmp} 2 within {20 * ms}',
          'wait quiet 3 within 2000000', f'frame 0 {avail.hex()}', 'wait quiet 3 within 2000000',
          f'frame 0 {gone.hex()}', f'wait cycles {50 * ms}', 'wait quiet 3 within 2000000',
          f'wait flash {event} within {6000 * ms}', *opening, *scenario.OPEN_WINDOW)
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


def alone(p: scenario.Point, image: int) -> scenario.Group:
    """One save of an image of a container of that length, with no other load, from the change to 5.2 s after it."""
    g = scenario.Group('save', sim_ms=6000, save=dict(image=image, records=CHANGED))
    scenario.ready(g, p)
    ms = scenario.MS
    g.add('mark save.change', f'frame 0 {set_name(p).hex()}', f'wait tx {scenario.CH["aecp"]} 1 within {50 * ms}',
          f'wait cycles {5200 * ms}')
    return g


def maap_conflict(interface: int) -> str:
    """A bridge's PROBE of the range the interface's MAAP last sent, as scenario.maap_conflict, copied from its newest
    MAAPDU of any type, since a stream of them is answered with DEFENDs, which push its ANNOUNCE out of the frames the
    testbench keeps. A DEFEND keeps the requested range of the PROBE it answers and goes to that PROBE's source
    (IEEE 1722-2016 B.2, B.3.6.6), so the copy is sent to the MAAP group address with no conflict range."""
    return (f'reply {interface} {scenario.CH["maap"]} 14:fe on={interface} 0={f.MAAP_DA:012x} '
            f'6={scenario.BRIDGE_MAC:012x} 15={f.MAAP_PROBE:02x} 34=0000000000000000')


def arrivals(p: scenario.Point, run_ms: float) -> list[tuple[float, str, str]]:
    """Every receive channel at its contract refill rate with its bursts for run_ms: the composed load's records
    (scenario.composed_load), admission()'s at_once of them at once, again each at_once refill periods, which
    refill the bucket by as many, channel n's bursts OFFSET_MS * n after channel 0's. Each is (ms, channel, step),
    in time order."""
    disc = f.adp(f.ADP_DISCOVER, 0, scenario.CTL_MAC, f.Adp(valid_time=0))
    read = lambda seq: f.read_descriptor(f.Aem(p.entity_id, scenario.CTL1, scenario.CTL_MAC, p.mac, seq), 0, 0)
    get = lambda seq: scenario.acmp_cmd(p, 'GET_RX_STATE', 0, seq)
    srp = scenario.listener_ready(p)
    frames = {'adp': lambda n: (f'frame {n % p.interfaces} {disc.hex()}', disc),
              'acmp': lambda n: (f'frame 0 {get(0x8000 + n % 0x8000).hex()}', get(0)),
              'aecp': lambda n: (f'frame {n % p.interfaces} {read(0x8000 + n % 0x8000).hex()}', read(0)),
              'maap': lambda n: (maap_conflict(n % p.interfaces), scenario.MAAP_PDU),
              'srp': lambda n: (f'frame {n % p.interfaces} {srp.hex()}', srp)}
    out = []
    for name, make in frames.items():
        ch = scenario.CONTRACT.channels[scenario.CH[name]]
        at_once = scenario.admission(name, make(0)[1])['at_once']
        start, period, n = OFFSET_MS * scenario.CH[name], at_once * ch.refill_ms, 0
        while start < run_ms:
            for _ in range(at_once):
                out.append((start, name, make(n)[0]))
                n += 1
            start += period
    return sorted(out, key=lambda a: a[0])


def held_start() -> int:
    """The AECP channel's held load starts one refill period after the change, in ms: the SET_NAME takes one of its
    bucket's tokens, which is back by then (KL_mbx_rx.sv), so its first burst is admitted whole. The other channels
    burst at the change, so the SET_NAME's marks fall among their first bursts' records."""
    return scenario.CONTRACT.channels[scenario.CH['aecp']].refill_ms


def held_arrivals(p: scenario.Point, run_ms: float) -> list[tuple[float, str, str]]:
    """arrivals for run_ms from a save's change, AECP's held_start later."""
    late = [(when + held_start(), channel, step) for when, channel, step in arrivals(p, run_ms - held_start())]
    return sorted([a for a in arrivals(p, run_ms) if a[1] != 'aecp'] + [a for a in late if a[1] == 'aecp'],
                  key=lambda a: a[0])


def loaded(p: scenario.Point, name: str, flood: bool, image: int) -> scenario.Group:
    """A save of a container of image bytes from its change, every receive channel at its refill rate with its
    bursts (held_arrivals) until its stated worst case has passed, and with flood a grandmaster change as every
    pass starts, so no pass takes nothing."""
    run_ms = bound_ms(image, CHANGED) + 500
    load = held_arrivals(p, run_ms)
    # every record the group's receive channels must commit from its change on: the load and the SET_NAME
    offered = {name: sum(1 for _, channel, _ in load if channel == name) + (name == 'aecp') for name in scenario.CH}
    g = scenario.Group(name, sim_ms=int(run_ms) + 2700,
                       save=dict(image=image, records=CHANGED, loaded=True, offered=offered))
    scenario.ready(g, p)
    scenario.announced(g)
    ms = scenario.MS
    g.add('mark save.change', f'frame 0 {set_name(p).hex()}', *(['flood gm 1'] if flood else []))
    at = 0
    for when, _, step in load:
        cycles = round(when * ms)
        if cycles > at:
            g.add(f'wait cycles {cycles - at}')
            at = cycles
        g.add(step)
    g.add(f'wait cycles {round(run_ms * ms) - at}', *(['flood gm 0'] if flood else []), 'wait quiet 3 within 2000000')
    return g


def second(p: scenario.Point, image: int) -> scenario.Group:
    """A change marked while a save is in flight, just after that save's capture took the first record the change
    names, timed from its mark to durable against bound_ms with that save in flight: under a grandmaster change as
    every pass starts, so the store steps once every CTRL_LOOP_STEP_AGE + 1 ticks, a SET_NAME just after a step,
    then SECOND_MS later, past its first-dirty window and the step that starts its save's capture, the next step,
    which takes the entity's first name, and then a SET_NAME of the entity to another value. The capture in flight
    takes its second name; its first waits for a save of its own (nvm_store.c, nvm_mark)."""
    run_ms = bound_ms(image, CHANGED, flight=CHANGED) + 500
    g = scenario.Group('save-second', sim_ms=int(SECOND_MS + run_ms) + 2800,
                       save=dict(image=image, records=CHANGED, flight=CHANGED))
    scenario.ready(g, p)
    scenario.announced(g)
    ms = scenario.MS
    g.add('flood gm 1', f'wait steps 1 within {100 * ms}', 'mark save.change', f'frame 0 {set_name(p).hex()}',
          f'wait cycles {SECOND_MS * ms}', f'wait steps 1 within {100 * ms}', 'mark save.second',
          f'frame 0 {set_name(p, b"again").hex()}', f'wait cycles {round(run_ms * ms)}', 'flood gm 0',
          'wait quiet 3 within 2000000')
    return g


def windows(p: scenario.Point) -> list[scenario.Group]:
    """The window at every tick phase of every flash phase."""
    return [window(p, phase, k) for phase in PHASES for k in range(TICK_PHASES)]


def aged_windows(p: scenario.Point, ages: tuple[int, ...] | None = None) -> list[scenario.Group]:
    """The window in every flash phase opened at each of `ages` (the age limit and one short of it), at every delay
    across the tick."""
    ages = (step_age(), step_age() - 1) if ages is None else ages
    return [aged_window(p, phase, age, n) for phase in PHASES for age in ages for n in range(len(AGED_DELAYS))]


def groups(p: scenario.Point, build: dict) -> list[scenario.Group]:
    """The windows, opened from idle and aged, the save alone, a save under every channel at its refill rate,
    without and with no pass that takes nothing, and a change while a save is in flight, each of the build's
    image's container."""
    image = container(build)
    return [*windows(p), *aged_windows(p), alone(p, image), loaded(p, 'save-held', False, image),
            loaded(p, 'save-starved', True, image), second(p, image)]


def row_names() -> list[str]:
    """The groups' names, at any point: build.py's planted store step runs them."""
    return [f'backlog-adp@{phase}-{k}' for phase in PHASES for k in range(TICK_PHASES)]


def aged_names() -> list[str]:
    """The aged windows' names, at any point: build.py's heavier aged step runs some of them."""
    ages = (step_age(), step_age() - 1)
    return [f'backlog-adp@{phase}-aged{age}-{n}' for phase in PHASES for age in ages for n in range(len(AGED_DELAYS))]


def aged_age(name: str) -> int | None:
    """The opening age an aged window's name declares (aged_window), or None for any other group."""
    found = re.fullmatch(r'[^@]+@[a-z]+-aged(\d+)-\d+', name)
    return int(found.group(1)) if found else None


def row(name: str) -> str:
    """The backlog row a group's window is: its name, but backlog-adp for a save's."""
    return name.partition('@')[0]
