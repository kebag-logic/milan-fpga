# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's checks of the binding class's timing grade (bind_save.py, #1009): synthetic logs of a bind's save,
each command timed from its response to the save whose container holds its value, the burst's last command per sink,
and the cut's container, read against containers built here from KLJ3's and layout 3's layout."""
from __future__ import annotations

import struct
import tempfile
import zlib
from pathlib import Path
from types import ModuleType

import bind_save
import grade
import scenario
import selftest_burst
from selftest_burst import IMAGE, SLOT, frame, save_lines

Check = tuple[str, bool, str]
BASE = 26                      # the BINDING block (nvm_layout3.h)
BOUND, UNBOUND = bind_save.bound_payload(), bytes(bind_save.BIND_LEN)


def container(binds: dict[int, bytes], seq: int) -> bytes:
    """A KLJ3 container of IMAGE bytes holding each sink's binding record, its CRC-32 closing."""
    body = struct.pack('<10I', 0x334A4C4B, 0x00030000, seq, len(binds) + 1, IMAGE, 0, 0, 0, 0, 3)
    body += b'\xff' * 18 + b''.join(frame(BASE + k, v) for k, v in sorted(binds.items()))
    body = body.ljust(IMAGE - 4, b'\0')
    return body + struct.pack('<I', zlib.crc32(body))


def response(message: int, seq: int, status: int = 0) -> bytes:
    """A BIND_RX_RESPONSE (7) or an UNBIND_RX_RESPONSE (9) with its sequence_id and status (the fields bind_save reads)."""
    pdu = bytearray(68)
    pdu[14], pdu[15] = 0xFC, 0x80 | message
    pdu[16] = status << 3
    struct.pack_into('>H', pdu, 62, seq)
    return bytes(pdu)


def graded(m: ModuleType, ops: list[dict], saves: list[tuple[bytes, float]], journal: bytes | None = None,
           kind: str = 'frame', target: int = 250, **answered: int) -> dict:
    """The grade of a log: each op answered at cycle 1000 + its place (unless answered's 'skip' names its seq, or 'status' is
    nonzero), then one save of a container for each (container, durable ms)."""
    ms = m.SYS_HZ // 1000
    records = [(0, response(7 if o['kind'] == 'BIND_RX' else 9, o['seq'], answered.get('status', 0)),
                o.get('at', 1000 + n)) for n, o in enumerate(ops) if answered.get('skip') != o['seq']]
    lines = m.tx_sequence(scenario.CH['acmp'], records)
    erase = 2000
    for n, (blob, at) in enumerate(saves):
        end = 1000 + int(at * ms)
        lines += save_lines(blob, erase, end, SLOT + 0x50000 * (n % 2))
        erase = end + 1000
    spec = dict(kind=kind, image=IMAGE, base=BASE, target_ms=target, ops=ops)
    group = scenario.Group('synthetic-bind', save=dict(bind=spec))
    with tempfile.TemporaryDirectory() as tmp:
        path = None
        if journal is not None:
            path = Path(tmp) / 'cut.journal'
            path.write_bytes(journal)
        return grade.grade(m.synthetic(lines), group, m.SYS_HZ, m.CPU_HZ, journal=path)['bind']


def bind_checks(m: ModuleType) -> list[Check]:
    """A binding's time from its response, its target, its missing response, its missing value at the cut."""
    bind = bind_save.op('BIND_RX', 0, 0x9500)
    half = 640 * 1024 // 2
    good = container({0: BOUND}, 6)
    journal = lambda blob: blob.ljust(half, b'\xff') + container({}, 5).ljust(half, b'\xff')
    out = []
    g = graded(m, [bind], [(good, 200.0)], journal(good))
    out.append(('bind: a bind durable within its target and held at the cut passes',
                not bind_save.misses(g, 'synthetic-bind') and g['rows'][0]['ms'] is not None
                and abs(g['rows'][0]['ms'] - 199) < 2, f"{g['rows']}"))
    g = graded(m, [bind], [(good, 300.0)], journal(good))
    out.append(('bind: a bind durable past its target fails by its name',
                len(bind_save.misses(g, 'synthetic-bind')) == 1 and 'over its target' in bind_save.misses(g, 'synthetic-bind')[0],
                str(bind_save.misses(g, 'synthetic-bind'))))
    g = graded(m, [bind], [(container({}, 6), 200.0)], journal(good))
    out.append(('bind: a bind no save holds fails by its name',
                any('not durable' in w for w in bind_save.misses(g, 'synthetic-bind')), str(bind_save.misses(g, 'synthetic-bind'))))
    g = graded(m, [bind], [(good, 200.0)], journal(container({}, 6)))
    out.append(('bind: a sink whose value the cut lacks fails by its name',
                any('at the cut' in w for w in bind_save.misses(g, 'synthetic-bind')), str(bind_save.misses(g, 'synthetic-bind'))))
    g = graded(m, [bind], [(good, 200.0)])
    out.append(('bind: a run that left no journal fails', 'synthetic-bind: the run left no journal' in bind_save.misses(g, 'synthetic-bind'),
                str(bind_save.misses(g, 'synthetic-bind'))))
    for name, kw, want in (('refused', dict(status=1), 'answered status 1'), ('unanswered', dict(skip=0x9500), 'never answered')):
        try:
            graded(m, [bind], [(good, 200.0)], journal(good), **kw)
            out.append((f'bind: a {name} bind is refused', False, 'graded'))
        except grade.Refusal as error:
            out.append((f'bind: a {name} bind is refused', want in str(error), str(error)))
    # a value's save before its response is not its save: the first command's save began before the second's response
    ops = [bind_save.op('BIND_RX', 0, 0x9600), bind_save.op('UNBIND_RX', 1, 0x9601)]
    g = graded(m, ops, [(container({0: BOUND}, 6), 120.0), (container({0: BOUND, 1: UNBOUND}, 7), 260.0)],
               journal(container({0: BOUND, 1: UNBOUND}, 7)), kind='burst', target=250)
    out.append(('bind: each command is timed to the first save that holds its value after its response, and a burst '
                'counts its saves and erases', g['saves'] == 2 and g['erases'] == 2 and g['rows'][0]['ms'] < 125
                and g['rows'][1]['ms'] > 250, f"{g['rows']} {g['saves']}"))
    # a command that came after a save that already held its value is timed to a save after it, and one no later save
    # holds is never durable
    late = [dict(bind_save.op('BIND_RX', 0, 0x9700), at=2500)]
    g = graded(m, late, [(good, 120.0), (container({0: BOUND}, 7), 220.0)], journal(good))
    out.append(('bind: a save begun before the response is not its command\'s', g['rows'][0]['ms'] is not None
                and g['rows'][0]['ms'] > 190, f"{g['rows']}"))
    return out
