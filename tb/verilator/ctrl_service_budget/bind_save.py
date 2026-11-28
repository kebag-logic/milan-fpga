# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""A binding change's time from its response to durable (#1009), for the binding class's 100 ms first-dirty window, each
save the whole container in an erased slot.

Milan v1.2 5.5.3.5.3 saves the binding parameters before the BIND_RX_RESPONSE is sent; 5.3.8.3 counts the started and
stopped state with them, and the store holds both in one binding record a sink (nvm_layout3.h's BINDING block). These
groups time a command from its response (the TX commit with its sequence_id) to the first durable save whose container
holds the sink's record as the command left it (save_burst.saves). A save is durable at the read that completes its
verify, so a figure holds for a cut at any later instant; the journal at the script's end must hold every sink's last
value.

`save-bind`, an idle store: BIND_RX, STOP_STREAMING, START_STREAMING and UNBIND_RX of sink 0, each left to finish before
the next. Each must be durable within IDLE_MS of its response, by one save of its own that starts after the binding
class's window, no earlier save in flight.

`save-bind-burst`: BURST binds and unbinds, one every PACE_MS over every sink in turn. Each sink's last command must be
durable within FLIGHT_MS of its response, and the burst takes at most BURST_SAVES saves, an erase each.

`save-bind-in-<arrival>`: a BIND_RX that arrives during a SET_NAME's save, one group an arrival (arrivals: just after
the capture, in the seal, the erase, the blank check, the program phase and the verify, early and late in each). The
save in flight took its capture before the bind, so its container holds no binding, and the bind's own save follows it:
durable within FLIGHT_MS of its response, the rest of one save and one save.

Every group runs with the part's erase and page-program times modelled (FLASH_US; sim_main.cpp); the log records them
and a run under other times is refused, so a figure counts the busy time of the part it names. A group fails by name
unless its saves are the ones it times (faults): whole saves, each an erase, every byte of the container programmed and
read back after it, and a container whose CRC closes; on an idle store one of the command's own; in a burst at least one
that another followed; in flight the two, the bind's response in its arrival's phase.
"""
from __future__ import annotations

import os
import struct
from pathlib import Path
from typing import TYPE_CHECKING

import frames as f
import save_burst
import save_window
import scenario
import nvm_layout3

if TYPE_CHECKING:
    import grade as grader  # grade.py imports this module

#: The part's times the groups model: an erase's and a page program's, microseconds. With them the harness times the
#: 8x8/1if base image's whole save at 1,451.5 ms from its change, a board between its 1,440 ms and 1,502 ms readings.
FLASH_US = (120000, 500)
#: From a response to durable, ms: an idle store's gate, and the bound on a bind that arrives during another save or a
#: burst, by point (#1009's scope ruling, items 3 and 4): the rest of that save plus one save, each the point's whole
#: save from its window to durable as these groups model it (1x1 204.5 ms, 8x8-1if 451.5 ms), twice that rounded up to
#: 50 ms. At arty-1x1 (PR #1004's ruling of 2026-11-27) the save-bind group's 288.8 ms less its 100 ms window gives
#: 188.8 ms: 377.6, stated 400.
IDLE_MS = 800
FLIGHT_MS = {'1x1': 450, '8x8-1if': 950, 'arty-1x1': 400}
#: The burst: its commands, their pace, ms, and the most saves it takes, by point, each one erase of 64 KiB. By the same
#: rule, saves start back to back from the first window's end while commands arrive, and the last command takes one
#: more: floor((630 - 100) / save) + 2, 4 at 1x1 and arty-1x1, 3 at 8x8-1if.
BURST, PACE_MS, BURST_SAVES = 64, 10, {'1x1': 4, '8x8-1if': 3, 'arty-1x1': 4}
#: The time after each command of the idle group, and after the burst and a bind in flight, ms: past the gate.
SETTLE_MS, END_MS = 1200, 2000
#: The binding record's payload: VALID and STARTED, the talker's unique id, its entity id, the controller's.
BIND_LEN, BIND_VALID, BIND_STARTED = 20, 1, 2
#: The commands' AECP command types (IEEE 1722.1-2021 Table 7-125) and the descriptor a sink is.
START_STREAMING, STOP_STREAMING, STREAM_INPUT = 0x0022, 0x0023, 0x0005
#: The BINDING block's records, one a sink.
SINKS = nvm_layout3.read().block('BINDING').cap
#: The sequence_ids of the idle group, the burst and the bind in flight.
SEQ_IDLE, SEQ_BURST, SEQ_FLIGHT = 0x9500, 0x9800, 0x9A00
#: The CALL lines' functions (build.CALL_SYMBOLS) whose entries mark a save's seal and its read-backs.
SEAL_CALL, READ_CALL = 'nvm_crc32_update', 'nvm_flash_litespi:ls_read'


def record(started: bool) -> bytes:
    """The binding record a BIND_RX of scenario.acmp_cmd leaves, started or stopped."""
    flags = BIND_VALID | (BIND_STARTED if started else 0)
    return bytes([flags, 0]) + struct.pack('>H', 1) + struct.pack('>QQ', scenario.TALKER_A, scenario.CTL1)


#: What a sink's record holds after each command.
LEAVES = dict(BIND_RX=record(True), START_STREAMING=record(True), STOP_STREAMING=record(False),
              UNBIND_RX=bytes(BIND_LEN))


def command(p: scenario.Point, kind: str, sink: int, seq: int) -> str:
    """One command to a sink, as a stimulus step."""
    if kind in ('BIND_RX', 'UNBIND_RX'):
        return f'frame 0 {scenario.acmp_cmd(p, kind, sink, seq).hex()}'
    start = START_STREAMING if kind == 'START_STREAMING' else STOP_STREAMING
    to = f.Aem(p.entity_id, scenario.CTL1, scenario.CTL_MAC, p.mac, seq)
    return f'frame 0 {f.aem_command(to, start, f.be(STREAM_INPUT, 2) + f.be(sink, 2)).hex()}'


def op(kind: str, sink: int, seq: int) -> dict:
    """One graded command: its sequence_id and what its sink's record then holds."""
    return dict(kind=kind, sink=sink, seq=seq, value=LEAVES[kind].hex())


def save_base() -> int:
    """The BINDING block's first record id."""
    return nvm_layout3.read().block('BINDING').base


def group(name: str, sim_ms: int, image: int, kind: str, target_ms: int, **more: object) -> scenario.Group:
    """A bind group: its part's times, its journal at the cut, and what it grades."""
    bind = dict(kind=kind, image=image, base=save_base(), target_ms=target_ms, **more)
    return scenario.Group(name, sim_ms=sim_ms, save=dict(journal=True, flash_us=FLASH_US, bind=bind))


def idle(p: scenario.Point, image: int) -> scenario.Group:
    """Each kind of binding change on an idle store."""
    ops = [op(kind, 0, SEQ_IDLE + n)
           for n, kind in enumerate(('BIND_RX', 'STOP_STREAMING', 'START_STREAMING', 'UNBIND_RX'))]
    g = group('save-bind', 1500 + SETTLE_MS * len(ops), image, 'idle', IDLE_MS, ops=ops)
    scenario.ready(g, p)
    for o in ops:
        g.add(command(p, o['kind'], o['sink'], o['seq']), f'wait cycles {SETTLE_MS * scenario.MS}')
    return g


def burst(p: scenario.Point, image: int) -> scenario.Group:
    """BURST binds and unbinds, one every PACE_MS over every sink in turn."""
    ms, ops = scenario.MS, []
    for k in range(BURST):
        sink, turn = k % p.sinks, k // p.sinks
        ops.append(op('BIND_RX' if turn % 2 == 0 else 'UNBIND_RX', sink, SEQ_BURST + k))
    last = {o['sink']: o for o in ops}
    g = group('save-bind-burst', 1500 + BURST * PACE_MS + END_MS, image, 'burst', FLIGHT_MS[p.label],
              ops=[o for o in ops if last[o['sink']] is o], all=len(ops), first=ops[0]['seq'],
              saves_max=BURST_SAVES[p.label])
    scenario.ready(g, p)
    for o in ops:
        g.add(command(p, o['kind'], o['sink'], o['seq']), f'wait cycles {PACE_MS * ms}')
    g.add(f'wait cycles {END_MS * ms}')
    return g


def arrivals(image: int) -> list[tuple[str, str, float, float, list[str]]]:
    """The bind's arrivals in the save in flight: each one's name, the save's phase its response comes in and the part
    of the phase (from, to), and the waits after the SET_NAME's response that place it. A container of image bytes has
    its seal's stretches and pages (save_window.PAGE) and its read-backs (save_window.READ)."""
    ms = scenario.MS
    seals = -(-(image - save_window.TRAILER) // save_window.PAGE)
    pages, reads = -(-image // save_window.PAGE), -(-image // save_window.READ)
    erase, last = f'flash erase 1 within {3000 * ms}', f'flash program {pages} within {3000 * ms}'
    call = lambda function, n: f'call {function} {n} within {3000 * ms}'
    return [('capture', 'seal', 0.0, 0.5, [call(SEAL_CALL, 1)]),
            ('seal', 'seal', 0.4, 1.0, [call(SEAL_CALL, seals // 2 + 1)]),
            ('erase', 'erase', 0.0, 0.2, [erase]),
            ('erase-late', 'erase', 0.4, 1.0, [erase, f'cycles {FLASH_US[0] * ms // 2000}']),
            ('blank', 'blank', 0.0, 0.5, [erase, call(READ_CALL, 1)]),
            ('blank-late', 'blank', 0.5, 1.0, [erase, call(READ_CALL, reads - 2)]),
            ('program', 'program', 0.0, 0.5, [f'flash program 1 within {3000 * ms}']),
            ('program-late', 'program', 0.5, 1.0, [f'flash program {pages - 2} within {3000 * ms}']),
            ('verify', 'verify', 0.0, 0.5, [last, call(READ_CALL, 1)]),
            ('verify-late', 'verify', 0.5, 1.0, [last, call(READ_CALL, reads - 2)])]


def in_flight(p: scenario.Point, image: int) -> list[scenario.Group]:
    """A BIND_RX of sink 0 at each arrival in a SET_NAME's save."""
    ms, out = scenario.MS, []
    for name, phase, start, stop, waits in arrivals(image):
        g = group(f'save-bind-in-{name}', 2500 + END_MS, image, 'flight', FLIGHT_MS[p.label],
                  ops=[op('BIND_RX', 0, SEQ_FLIGHT)], phase=phase, part=(start, stop))
        scenario.ready(g, p)
        g.add(f'frame 0 {save_window.set_name(p).hex()}', f'wait tx {scenario.CH["aecp"]} 1 within {50 * ms}',
              *(f'wait {w}' for w in waits), command(p, 'BIND_RX', 0, SEQ_FLIGHT), f'wait cycles {END_MS * ms}')
        out.append(g)
    return out


def groups(p: scenario.Point, build: dict) -> list[scenario.Group]:
    """The idle store's commands, the burst and the binds in flight, at one interface."""
    image = save_window.container(build)
    return [idle(p, image), burst(p, image), *in_flight(p, image)]


def environment(save: dict, journal: Path) -> dict[str, str]:
    """The testbench's environment for a group's run (sim_main.cpp): the journal the cut leaves, written at the
    script's end for a group that grades it, and the part's times for a group that models them, and for no other."""
    env = {k: v for k, v in os.environ.items() if k not in ('BUDGET_JOURNAL_OUT', 'BUDGET_FLASH_US')}
    if save.get('journal'):
        env['BUDGET_JOURNAL_OUT'] = str(journal)
    if save.get('flash_us'):
        env['BUDGET_FLASH_US'] = ':'.join(map(str, save['flash_us']))
    return env


# ---- the grade ---------------------------------------------------------------------------------------------------

def responses(log: grader.Log) -> dict[int, tuple[int, int]]:
    """Each response to a graded command: a BIND_RX_RESPONSE's or an UNBIND_RX_RESPONSE's that ACMP committed, and an
    AEM_RESPONSE's (save_burst.responses): sequence_id -> (cycle, status)."""
    out = dict(save_burst.responses(log))
    for cycle, ch, _, pdu in log.tx:
        if ch != scenario.CH['acmp'] or len(pdu) < 66 or pdu[14] != 0xFC or pdu[15] & 0x0F not in (7, 9):
            continue
        out.setdefault(struct.unpack_from('>H', pdu, 62)[0], (cycle, pdu[16] >> 3))
    return out


def held(blob: bytes, image: int, base: int) -> dict[int, bytes]:
    """Every binding frame in a container, by sink: each layout 3 frame of the BINDING block, 20 payload bytes."""
    out, at = {}, save_burst.KLJ_HDR
    head = struct.pack('>HBB', save_burst.REC_MAGIC, save_burst.LAYOUT, 0)
    while True:
        at = blob.find(head, at, image - save_burst.TRAILER)
        if at < 0:
            return out
        rid, plen, crc = struct.unpack_from('>HHH', blob, at + 4)
        payload = blob[at + 10:at + 10 + plen]
        if (plen == BIND_LEN and base <= rid < base + SINKS and len(payload) == plen
                and save_burst.crc16(blob[at:at + 8] + payload) == crc):
            out[rid - base] = payload
        at += 1


def flash_times(log: grader.Log, group_: scenario.Group) -> tuple[int, int]:
    """The part's times the run modelled, microseconds, from the log's own record; refused unless the group's."""
    import grade as grader
    cycles = [int(log.summary.get(k, -1)) for k in ('flash_erase', 'flash_program')]
    got = tuple(c * 1_000_000 // log.sys_hz if c >= 0 else -1 for c in cycles)
    want = tuple(group_.save['flash_us'])
    if got != want:
        raise grader.Refusal(f'{group_.name}: the run modelled an erase of {got[0]} us and a page program of '
                             f'{got[1]} us, the group times {want[0]} us and {want[1]} us')
    return got


def grade(log: grader.Log, group_: scenario.Group, journal_path: Path | None) -> dict | None:
    """A bind group's rows, each graded command from its response to the first durable save that holds its value, and
    what its saves were (faults: whole_faults, and the group's kind's idle_faults, burst_faults or flight_faults)."""
    import grade as grader
    spec = group_.save.get('bind')
    if spec is None:
        return None
    image, base = spec['image'], spec['base']
    flash = flash_times(log, group_)
    answered = responses(log)
    every = save_burst.saves(log, image)
    done = [s for s in every if s['durable'] is not None]
    rows = []
    for o in spec['ops']:
        if o['seq'] not in answered:
            raise grader.Refusal(f"{group_.name}: the {o['kind']} of sink {o['sink']} was never answered")
        cycle, status = answered[o['seq']]
        if status != 0:
            raise grader.Refusal(f"{group_.name}: the {o['kind']} of sink {o['sink']} answered status {status}")
        durable = first_durable(done, cycle, o['sink'], bytes.fromhex(o['value']), image, base)
        ms = round(log.ms_of(durable - cycle), 3) if durable is not None else None
        rows.append(dict(sink=o['sink'], kind=o['kind'], response_sys=cycle, ms=ms,
                         within=ms is not None and ms <= spec['target_ms']))
    left = journal_path is not None and journal_path.exists()
    bound = bind_of(journal_path, image, base) if left else {}
    final = {o['sink']: bytes.fromhex(o['value']) for o in spec['ops']}
    worst = max(rows, key=lambda r: (r['ms'] is None, r['ms'] or 0))
    found = dict(kind=spec['kind'], target_ms=spec['target_ms'], flash_us=list(flash), rows=rows, journal=left,
                 missing=sorted(s for s, v in final.items() if left and bound.get(s) != v), saves=len(done),
                 erases=sum(1 for _, o, _, _ in log.flash_ops if o == grader.FLASH_ERASE), worst_ms=worst['ms'],
                 worst_sink=worst['sink'], worst_kind=worst['kind'], commands=spec.get('all', len(rows)))
    kind = dict(idle=idle_faults, burst=burst_faults, flight=flight_faults)[spec['kind']]
    return dict(found, faults=[*whole_faults(every), *kind(log, spec, every, answered)])


def whole_faults(every: list[dict]) -> list[str]:
    """Each erase of the log must be a whole save that became durable."""
    return [f"its save {n + 1}, erased at {s['erase']}, is not a whole container read back after it was programmed"
            for n, s in enumerate(every) if s['durable'] is None]


def idle_faults(log: grader.Log, spec: dict, every: list[dict], answered: dict) -> list[str]:
    """Each command on an idle store: the saves before it durable before its response, and one save between it and the
    next command, begun once its own window has passed."""
    out = []
    window = (save_window.BIND_DIRTY_MS - 2 * save_window.TICK_MS) * log.sys_hz // 1000
    ops = spec['ops']
    for n, o in enumerate(ops):
        start = answered[o['seq']][0]
        stop = answered[ops[n + 1]['seq']][0] if n + 1 < len(ops) else 1 << 62
        mine = [s for s in every if start < s['erase'] <= stop]
        if any(s['durable'] is None or s['durable'] >= start for s in every if s['erase'] <= start):
            out.append(f"the {o['kind']} came with a save in flight, not to an idle store")
        if len(mine) != 1:
            out.append(f"the {o['kind']} took {len(mine)} saves, not one")
        elif mine[0]['erase'] - start < window:
            out.append(f"the {o['kind']}'s save erased its slot {log.ms_of(mine[0]['erase'] - start):.3f} ms after its "
                       "response, before its window: another change's save")
    return out


def burst_faults(log: grader.Log, spec: dict, every: list[dict], answered: dict) -> list[str]:
    """The burst's saves all come after its first command, at most saves_max of them, an erase each."""
    first = answered.get(spec['first'], (1 << 62, 0))[0]
    out = [] if all(s['erase'] > first for s in every) else ['a save came before the first command']
    if len(every) < 2:
        out.append(f'the burst took {len(every)} save(s): no command arrived during another save')
    if len(every) > spec['saves_max']:
        out.append(f"the burst took {len(every)} erases, more than {spec['saves_max']}")
    return out


def flight_faults(log: grader.Log, spec: dict, every: list[dict], answered: dict) -> list[str]:
    """The SET_NAME's save, in whose phase the bind's response came, and then the bind's own, and no other: the first
    container holds no binding, so the bind came after its capture."""
    cycle = answered[spec['ops'][0]['seq']][0]
    if len(every) != 2 or every[0]['durable'] is None:
        return [f"the run took {len(every)} saves, not the one in flight and the bind's own"]
    sink = spec['ops'][0]['sink']
    out = []
    if sink in held(every[0]['blob'], spec['image'], spec['base']):
        out.append("the save in flight holds the bind: it came before that save's capture ended")
    phase, part = phase_of(log, every[0], cycle)
    low, high = spec['part']
    if phase != spec['phase'] or not low <= part <= high:
        out.append(f"the bind's response came at {part:.2f} of the save's {phase} phase, not in "
                   f"[{low:.2f}, {high:.2f}] of its {spec['phase']} phase")
    return out


def phase_of(log: grader.Log, save: dict, cycle: int) -> tuple[str | None, float]:
    """The phase of a whole save a cycle is in, and how far through it: the seal from its first stretch to the erase,
    the erase to the blank check's first read-back, the blank check to the first page, the program phase to the verify's
    first read-back, and the verify to durable (nvm_store.c's phases, by the CALL and FLASHOP lines)."""
    import grade as grader
    calls = lambda function, a, b: sorted(int(t[1]) for t in log.traced
                                          if t[0] == 'CALL' and t[3] == function and a < int(t[1]) < b)
    erase, durable = save['erase'], save['durable']
    pages = [c for c, o, _, _ in log.flash_ops if o == grader.FLASH_PROGRAM and erase < c < durable]
    stretches = -(-(len(save['blob']) - save_window.TRAILER) // save_window.PAGE)
    seals = calls(SEAL_CALL, 0, erase)[-stretches:]
    checks = calls(READ_CALL, erase, durable)
    if not pages or not any(c > pages[-1] for c in checks):
        return None, 0.0
    edges = [('seal', min(seals, default=erase)), ('erase', erase), ('blank', checks[0]), ('program', pages[0]),
             ('verify', next(c for c in checks if c > pages[-1])), ('', durable)]
    for (name, start), (_, end) in zip(edges, edges[1:]):
        if start <= cycle < end:
            return name, (cycle - start) / (end - start)
    return None, 0.0


def first_durable(done: list[dict], cycle: int, sink: int, want: bytes, image: int, base: int) -> int | None:
    """The first durable save erased after a response at that cycle whose container holds the sink's record as want."""
    return min((d['durable'] for d in done if d['erase'] > cycle
                and held(d['blob'], image, base).get(sink) == want), default=None)


def bind_of(path: Path, image: int, base: int) -> dict[int, bytes]:
    """The authoritative container's bindings at the cut (save_burst.newer), none with no slot accepted."""
    return held(save_burst.newer(path, image)[1], image, base)


def misses(g: dict, name: str) -> list[str]:
    """What fails the run, named by its group: a command not durable within the target, or never; a save that is not the
    one the group times; a sink whose last value the authoritative container lacks at the cut."""
    out = [f"{name}: the {r['kind']} of sink {r['sink']} not durable when the run ended, target {g['target_ms']:,} ms"
           for r in g['rows'] if r['ms'] is None]
    out += [f"{name}: the {r['kind']} of sink {r['sink']} durable {r['ms']:.3f} ms after its response, over its target "
            f"{g['target_ms']:,} ms" for r in g['rows'] if r['ms'] is not None and not r['within']]
    out += [f'{name}: {fault}' for fault in g['faults']]
    if not g['journal']:
        out.append(f'{name}: the run left no journal')
    out += [f'{name}: sink {s} not bound as its last command left it in the authoritative container at the cut'
            for s in g['missing']]
    return out


def late(results: list[dict]) -> list[str]:
    """Every bind group's misses."""
    return [m for g in results if g.get('bind') for m in misses(g['bind'], g['group'])]


def worst_of(b: dict) -> str:
    """A group's latest command, in ms and its sink, or that it was never durable."""
    return f"{b['worst_ms']:.3f} ms" if b['worst_ms'] is not None else 'never'


def lines(results: list[dict]) -> list[str]:
    """One BIND line for each bind group: its latest command, its target, its saves and erases, the part's times."""
    return [f"BIND {g['group']}: {b['commands']} command(s), the latest durable {worst_of(b)} after its response "
            f"({b['worst_kind']} of sink {b['worst_sink']}; target {b['target_ms']:,} ms), {b['saves']} whole save(s), "
            f"{b['erases']} erase(s), erase {b['flash_us'][0] / 1000:g} ms and page {b['flash_us'][1] / 1000:g} ms "
            f"modelled, {len(b['missing'])} sink(s) not as last commanded at the cut "
            f"{'FAILED' if misses(b, g['group']) else 'within'}"
            for g in results for b in [g.get('bind')] if b]


def table(results: list[dict]) -> list[str]:
    """The bind groups' section of the table: each command's time to durable, its target, and the group's saves."""
    rows = [(g['group'], g['bind']) for g in results if g.get('bind')]
    if not rows:
        return []
    flash = rows[0][1]['flash_us']
    out = ['', 'Binding changes from their response to durable (bind_save.py; the binding class\'s 100 ms window, '
           f'Milan v1.2 5.5.3.5.3 and 5.3.8.3), with the part\'s erase of {flash[0] / 1000:g} ms and page program of '
           f'{flash[1] / 1000:g} ms modelled:', '',
           '| Group | Command | Sink | Durable, ms | Target ms | Saves | Erases | Verdict |',
           '|---|---|---:|---:|---:|---:|---:|---|']
    for name, b in rows:
        verdict = 'FAILED' if misses(b, name) else 'within'
        out += [f"| {name} | {r['kind']} | {r['sink']} | {r['ms'] if r['ms'] is not None else 'never'} | "
                f"{b['target_ms']:,} | {b['saves']} | {b['erases']} | {verdict} |" for r in b['rows']]
    return out
