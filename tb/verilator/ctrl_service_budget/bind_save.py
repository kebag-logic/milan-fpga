# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""A binding change's time from its response to durable (#1009), for the binding class's 100 ms first-dirty window.

Milan v1.2 5.5.3.5.3 saves the binding parameters before the BIND_RX_RESPONSE is sent; 5.3.8.3 counts the started and
stopped state with them, and the store holds both in one binding record (nvm_layout3.h's BINDING block). These groups
time a BIND_RX or an UNBIND_RX from its response (the ACMP TX commit with its sequence_id) to the first durable save
whose container holds the sink's binding record with the value the command asked for (save_burst.saves, which reads a
whole commit or a delta frame off the log). A save's verify is the read that completes it, so a figure holds for a cut
at any later instant: the testbench's journal at the script's end must hold every sink's last value.

`save-bind` binds one sink of a device with blank flash: its save is the whole container (WHOLE_MS, the commit path).
`save-bind-frame` writes both slots, a bind and its unbind each left to finish, then binds again: that save is a
delta frame (FRAME_MS). `save-bind-burst` writes both slots, then binds and unbinds every sink in turn, one command
every PACE_MS, BURST commands: each sink's last command is timed, and the saves and erases of the burst counted.
The targets are the acceptance's, on the board: with the part's busy times modelled (BUDGET_FLASH_US, sim_main.cpp)
they hold for it; without them they bound the store's and the loop's own time alone.
"""
from __future__ import annotations

import struct
from pathlib import Path
from typing import TYPE_CHECKING

import save_burst
import save_window
import scenario
import nvm_layout3

if TYPE_CHECKING:
    import grade as grader  # grade.py imports this module

#: The acceptance's targets, ms from the response to durable: a save that goes as a frame, and one written whole.
FRAME_MS, WHOLE_MS = 250, 800
#: The burst: its commands, their pace, and the settle after a warm-up command and at the end, ms.
BURST, PACE_MS, WARM_MS, END_MS = 64, 10, 1200, 2500
#: The binding record's payload: VALID and STARTED, the talker's unique id, its entity id, the controller's.
BIND_LEN, BIND_VALID, BIND_STARTED = 20, 1, 2


def bound_payload() -> bytes:
    """The binding record a BIND_RX of scenario.acmp_cmd leaves: valid and started, then the talker's and its controller."""
    return (bytes([BIND_VALID | BIND_STARTED, 0]) + struct.pack('>H', 1) + struct.pack('>QQ', scenario.TALKER_A, scenario.CTL1))


def command(p: scenario.Point, kind: str, sink: int, seq: int) -> str:
    """A BIND_RX or an UNBIND_RX of sink, as a stimulus step."""
    return f'frame 0 {scenario.acmp_cmd(p, kind, sink, seq).hex()}'


def op(kind: str, sink: int, seq: int) -> dict:
    """One graded command: its sequence_id and what its sink's record then holds."""
    return dict(kind=kind, sink=sink, seq=seq, value=(bound_payload() if kind == 'BIND_RX' else bytes(BIND_LEN)).hex())


def whole(p: scenario.Point, image: int) -> scenario.Group:
    """A BIND_RX of sink 0 on blank flash, its save the whole container."""
    ops = [op('BIND_RX', 0, 0x9500)]
    g = scenario.Group('save-bind', sim_ms=2500, save=dict(journal=True, bind=dict(
        kind='whole', image=image, base=save_base(), ops=ops, target_ms=WHOLE_MS)))
    scenario.ready(g, p)
    g.add(command(p, 'BIND_RX', 0, 0x9500), f'wait cycles {1500 * scenario.MS}')
    return g


def frame(p: scenario.Point, image: int) -> scenario.Group:
    """Both slots written by a bind and its unbind of sink 0, then a BIND_RX of it, whose save is a delta frame."""
    ops = [op('BIND_RX', 0, 0x9600), op('UNBIND_RX', 0, 0x9601), op('BIND_RX', 0, 0x9602)]
    g = scenario.Group('save-bind-frame', sim_ms=6500, save=dict(journal=True, bind=dict(
        kind='frame', image=image, base=save_base(), ops=ops[2:], target_ms=FRAME_MS)))
    scenario.ready(g, p)
    ms = scenario.MS
    g.add(command(p, 'BIND_RX', 0, 0x9600), f'wait cycles {WARM_MS * ms}',
          command(p, 'UNBIND_RX', 0, 0x9601), f'wait cycles {WARM_MS * ms}',
          command(p, 'BIND_RX', 0, 0x9602), f'wait cycles {1000 * ms}')
    return g


def burst(p: scenario.Point, image: int) -> scenario.Group:
    """Both slots written, then BURST binds and unbinds, one every PACE_MS over every sink in turn."""
    sinks = max(1, min(p.sinks, 32))
    ms = scenario.MS
    g = scenario.Group('save-bind-burst', sim_ms=9000, save=dict(journal=True, bind=dict(
        kind='burst', image=image, base=save_base(), ops=[], target_ms=FRAME_MS)))
    scenario.ready(g, p)
    g.add(command(p, 'BIND_RX', 0, 0x9700), f'wait cycles {WARM_MS * ms}',
          command(p, 'UNBIND_RX', 0, 0x9701), f'wait cycles {WARM_MS * ms}')
    ops = []
    for k in range(BURST):
        sink, turn = k % sinks, k // sinks
        kind = 'BIND_RX' if turn % 2 == 0 else 'UNBIND_RX'
        g.add(command(p, kind, sink, 0x9800 + k), f'wait cycles {PACE_MS * ms}')
        ops.append(op(kind, sink, 0x9800 + k))
    last = {o['sink']: o for o in ops}
    g.save['bind']['ops'] = [o for o in ops if last[o['sink']] is o]
    g.save['bind'].update(all=len(ops), first=ops[0]['seq'])
    g.add(f'wait cycles {END_MS * ms}')
    return g


def save_base() -> int:
    """The BINDING block's first record id."""
    return nvm_layout3.read().block('BINDING').base


def groups(p: scenario.Point, build: dict) -> list[scenario.Group]:
    """The three groups, at one interface."""
    image = save_window.container(build)
    return [whole(p, image), frame(p, image), burst(p, image)]


def names_of_groups() -> list[str]:
    """The groups' names."""
    return ['save-bind', 'save-bind-frame', 'save-bind-burst']


# ---- the grade ---------------------------------------------------------------------------------------------------

def responses(log: grader.Log) -> dict[int, tuple[int, int]]:
    """Each BIND_RX_RESPONSE and UNBIND_RX_RESPONSE the ACMP channel committed: sequence_id -> (cycle, status)."""
    out = {}
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
        if (plen == BIND_LEN and rid >= base and len(payload) == plen
                and save_burst.crc16(blob[at:at + 8] + payload) == crc):
            out[rid - base] = payload
        at += 1


def grade(log: grader.Log, group: scenario.Group, journal_path: Path | None) -> dict | None:
    """A bind group's rows: each graded command from its response to the first durable save that holds its value."""
    import grade as grader
    spec = group.save.get('bind')
    if spec is None:
        return None
    image, base = spec['image'], spec['base']
    answered = responses(log)
    done = [s for s in save_burst.saves(log, image) if s['durable'] is not None]
    rows = []
    for o in spec['ops']:
        if o['seq'] not in answered:
            raise grader.Refusal(f"{group.name}: the {o['kind']} of sink {o['sink']} was never answered")
        cycle, status = answered[o['seq']]
        if status != 0:
            raise grader.Refusal(f"{group.name}: the {o['kind']} of sink {o['sink']} answered status {status}")
        want = bytes.fromhex(o['value'])
        durable = first_durable(done, cycle, o['sink'], want, image, base)
        ms = round(log.ms_of(durable - cycle), 3) if durable is not None else None
        rows.append(dict(sink=o['sink'], kind=o['kind'], ms=ms, within=ms is not None and ms <= spec['target_ms']))
    first = answered.get(spec.get('first', spec['ops'][0]['seq']), (0, 0))[0]
    late = [s for s in save_burst.saves(log, image) if s['start'] >= first]
    left = journal_path is not None and journal_path.exists()
    bound = bind_of(journal_path, image, base) if left else {}
    final = {o['sink']: bytes.fromhex(o['value']) for o in spec['ops']}
    missing = sorted(s for s, v in final.items() if left and bound.get(s) != v)
    worst = max(rows, key=lambda r: (r['ms'] is None, r['ms'] or 0)) if rows else None
    return dict(kind=spec['kind'], target_ms=spec['target_ms'], rows=rows, journal=left,
                missing=missing, saves=len(late), frames=sum(s['kind'] == 'frame' for s in late),
                erases=sum(s['kind'] == 'whole' for s in late), worst_ms=worst['ms'] if worst else None,
                worst_sink=worst['sink'] if worst else None, commands=spec.get('all', len(rows)))


def first_durable(done: list[dict], cycle: int, sink: int, want: bytes, image: int, base: int) -> int | None:
    """The first durable save begun after a response at that cycle whose container holds the sink's record as want."""
    return min((d['durable'] for d in done if d['start'] > cycle
                and held(d['blob'], image, base).get(sink) == want), default=None)


def bind_of(path: Path, image: int, base: int) -> dict[int, bytes]:
    """The authoritative container's bindings at the cut (save_burst.journal's choice of slot)."""
    data = path.read_bytes()
    half = len(data) // 2
    slots = [save_burst.slot_state(data[o:o + half], image) for o in (0, half)]
    good = [(s, b) for s, b in slots if s is not None]
    if not good:
        return {}
    seq, blob = good[0] if len(good) == 1 or ((good[0][0] - good[1][0]) & 0xFFFFFFFF) < 1 << 31 else good[1]
    return held(blob, image, base)


def misses(g: dict, group: str) -> list[str]:
    """What fails the run, named by its group: a command not durable within the target, or never; a sink whose last value the
    authoritative container lacks at the cut; a burst that left a save with an erase."""
    out = [f"{group}: the {r['kind']} of sink {r['sink']} not durable {g['target_ms']:,} ms after its response"
           for r in g['rows'] if r['ms'] is None]
    out += [f"{group}: the {r['kind']} of sink {r['sink']} durable {r['ms']:.3f} ms after its response, over its target "
            f"{g['target_ms']:,} ms" for r in g['rows'] if r['ms'] is not None and not r['within']]
    if not g['journal']:
        out.append(f'{group}: the run left no journal')
    out += [f'{group}: sink {s} not bound as its last command left it in the authoritative container at the cut'
            for s in g['missing']]
    return out
