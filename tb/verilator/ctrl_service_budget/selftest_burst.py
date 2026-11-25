# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's checks of a burst's and a change in flight's grade (save_burst.py, #920): synthetic logs of one
save, each name timed from its SET_NAME's response to the save's verify, and the journal a cut leaves, read against
containers built here from KLJ3's and layout 3's layout, apart from save_burst's own reader."""
from __future__ import annotations

import struct
import tempfile
import zlib
from pathlib import Path
from types import ModuleType

import grade
import save_burst
import scenario

Check = tuple[str, bool, str]
#: The synthetic container: its length, the NAME block's base, and where its two names' frames sit.
IMAGE, BASE, SLOT = 512, 222, 0xE40000
NAMES = {0: b'burst 000'.ljust(64, b'\0'), 1: b'burst 001'.ljust(64, b'\0')}


def frame(rid: int, payload: bytes) -> bytes:
    """A layout 3 frame: magic, version 3, reserved, id, length, then the CCITT-FALSE crc16, then the payload."""
    head = struct.pack('>HBBHH', 0x1722, 3, 0, rid, len(payload))
    crc, data = 0xFFFF, head + payload
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return head + struct.pack('>H', crc) + payload


def container(names: dict[int, bytes], seq: int, crc_ok: bool = True, ver: int = 0x00030000,
              nrec: int | None = None) -> bytes:
    """A KLJ3 container of IMAGE bytes: its header, an erased record before the names, the names, its CRC-32."""
    count = len(names) + 1 if nrec is None else nrec
    body = struct.pack('<10I', 0x334A4C4B, ver, seq, count, IMAGE, 0, 0, 0, 0, 3)
    body += b'\xff' * 18 + b''.join(frame(BASE + k, v) for k, v in sorted(names.items()))
    body = body.ljust(IMAGE - 4, b'\0')
    crc = zlib.crc32(body) ^ (0 if crc_ok else 1)
    return body + struct.pack('<I', crc)


def delta(base: bytes, new: bytes) -> bytes:
    """A delta frame (#1009, nvm_shape.h's KLD3) that makes base, a minor 1 container, into new: the span where they
    differ past the header, new's sequence and trailer, the sequence it follows, its CRC-32."""
    diff = [i for i in range(40, IMAGE - 4) if base[i] != new[i]]
    off, n = diff[0], diff[-1] + 1 - diff[0]
    body = struct.pack('<7I', 0x33444C4B, 0x00010000, *struct.unpack_from('<I', new, 8),
                       *struct.unpack_from('<I', base, 8), off, n, *struct.unpack_from('<I', new, IMAGE - 4))
    body += new[off:off + n] + bytes(-n % 4)
    return body + struct.pack('<I', zlib.crc32(body))


def save_lines(blob: bytes, erase: int, verify_end: int, slot: int = SLOT) -> list[str]:
    """One save of blob into a slot: its erase, its pages and their bytes, then a verify that reads it all back."""
    lines = [f'FLASHOP {erase} {grade.FLASH_ERASE} {slot:06x} 0']
    for n, at in enumerate(range(0, len(blob), 256)):
        page = blob[at:at + 256]
        lines += [f'FLASHOP {erase + 10 + n} {grade.FLASH_PROGRAM} {slot + at:06x} {len(page)}',
                  f'FLASHDATA {erase + 10 + n} {slot + at:06x} {page.hex()}']
    return lines + [f'FLASHRD {verify_end - 100} {verify_end} {slot:06x} {len(blob)}']


def group(kind: str) -> scenario.Group:
    """The synthetic group's declared names (save_burst.burst and save_burst.flight declare theirs so)."""
    spec = dict(kind=kind, image=IMAGE, base=BASE, target_ms=save_burst.TARGET_MS, records=2,
                sets=[dict(ordinal=k, seq=0x9000 + 2 * k, value=v.hex()) for k, v in NAMES.items()])
    return scenario.Group(f'synthetic-{kind}', save=dict(named=spec))


def graded(m: ModuleType, kind: str, blob: bytes, durable_ms: float, journal: bytes | None = None,
           **opts: int | bool) -> dict:
    """The grade of a log, built with the self-test's own builders (m: its synthetic, tx_sequence and aem_response,
    and its clocks), whose SET_NAMEs are answered at cycle 1000 with opts' status (0) unless opts' answered is False,
    and whose one save is durable durable_ms later, with that journal at the cut (written to a scratch file) and opts'
    steps (0) passes stepping after the save."""
    ms = m.SYS_HZ // 1000
    steps = int(opts.get('steps', 0))
    lines = []
    if opts.get('answered', True):
        records = []
        for k in NAMES:
            frame_ = bytearray(m.aem_response(scenario.CTL2, 0x9000 + 2 * k))
            frame_[16] = (frame_[16] & 0x07) | int(opts.get('status', 0)) << 3
            records.append((0, bytes(frame_), 1000 + k))
        lines += m.tx_sequence(scenario.CH['aecp'], records)
    end = 1000 + int(durable_ms * ms)
    lines += save_lines(blob, 2000, end)
    if 'frame' in opts:
        # a delta frame after the whole save, into its slot's room, verified frame_ms after the responses
        # (opts' merged: its blank check and verify one read run across its page, as the testbench merges them)
        frame_, frame_ms = opts['frame']
        done, at = 1000 + int(frame_ms * ms), SLOT + save_burst.delta_room(IMAGE)[0]
        first = done - 300 if opts.get('merged') else done - 100
        lines += [f'FLASHOP {done - 200} {grade.FLASH_PROGRAM} {at:06x} {len(frame_)}',
                  f'FLASHDATA {done - 200} {at:06x} {frame_.hex()}', f'FLASHRD {first} {done} {at:06x} {len(frame_)}']
    lines += [f'STEPPASS {n} {end + 10 + n} 1 100 store=50' for n in range(steps)]
    if kind == 'flight':
        lines += save_lines(blob, end + 10 + steps, end + 10 + steps + 2 * ms, SLOT + 0x50000)
    with tempfile.TemporaryDirectory() as tmp:
        path = None
        if journal is not None:
            path = Path(tmp) / 'cut.journal'
            path.write_bytes(journal)
        return grade.grade(m.synthetic(lines), group(kind), m.SYS_HZ, m.CPU_HZ, journal=path)['burst']


def burst_checks(m: ModuleType) -> list[Check]:
    """A burst's names timed and found at the cut; a name missing, late, refused or unanswered, a container that does
    not close, and a change in flight's next save that waited, each failing by its own words (m: the self-test)."""
    good = container(NAMES, 6)
    half = 640 * 1024 // 2
    journal = lambda blob: blob.ljust(half, b'\xff') + container({}, 5).ljust(half, b'\xff')
    run = lambda *a, **k: graded(m, *a, **k)
    out = []
    g = run('burst', good, 1500, journal(good))
    words = save_burst.misses(g, 'synthetic-burst')
    out.append(('burst: names durable within the target and held at the cut pass',
                not words and g['worst_ms'] is not None and abs(g['worst_ms'] - 1500) < 1, f'{words} {g["worst_ms"]}'))
    g = run('burst', container({0: NAMES[0]}, 6), 1500, journal(good))
    words = save_burst.misses(g, 'synthetic-burst')
    out.append(('burst: a name no durable save holds fails by its name',
                words == ['synthetic-burst: name 1 not durable 5,000 ms after its response, when the run ended'],
                str(words)))
    g = run('burst', good, 5200, journal(good))
    words = save_burst.misses(g, 'synthetic-burst')
    out.append(('burst: a name durable past the target fails by its name',
                len(words) == 2 and all('over its target 5,000 ms' in w for w in words), str(words)))
    g = run('burst', good, 1500, journal(container({1: NAMES[1]}, 6)))
    words = save_burst.misses(g, 'synthetic-burst')
    out.append(('burst: a name the cut\'s container lacks fails by its name',
                words == ['synthetic-burst: name 0 not in the authoritative container at the cut'], str(words)))
    g = run('burst', good, 1500, journal(container(NAMES, 4)))
    words = save_burst.misses(g, 'synthetic-burst')
    out.append(('burst: the cut reads the newer accepted slot, not the older',
                len(words) == 2 and all('not in the authoritative container' in w for w in words), str(words)))
    g = run('burst', container(NAMES, 6, crc_ok=False), 1500, journal(good))
    words = save_burst.misses(g, 'synthetic-burst')
    out.append(('burst: a container whose CRC does not close is not durable',
                len(words) == 2 and all('not durable' in w for w in words), str(words)))
    g = run('burst', good, 1500)
    words = save_burst.misses(g, 'synthetic-burst')
    out.append(('burst: a run that left no journal fails', 'synthetic-burst: the run left no journal' in words,
                str(words)))
    base = container({0: NAMES[0]}, 6, ver=0x00030001, nrec=3)
    new = container(NAMES, 7, ver=0x00030001, nrec=3)
    frame_ = delta(base, new)
    g = run('burst', base, 1500, journal(base + frame_), frame=(frame_, 2500))
    words = save_burst.misses(g, 'synthetic-burst')
    ms = {r['ordinal']: r['ms'] for r in g['rows']}
    out.append(('burst: a delta frame after a whole save is a save, durable at its verify, its container the slot\'s '
                'with the frame applied, and the cut reads the slot through its frames',
                not words and [s['kind'] for s in g['saves']] == ['whole', 'frame'] and ms[0] is not None
                and abs(ms[0] - 1500) < 1 and ms[1] is not None and abs(ms[1] - 2500) < 1, f'{words} {g["saves"]} {ms}'))
    g = run('burst', base, 1500, journal(base + frame_), frame=(frame_, 2500), merged=True)
    words = save_burst.misses(g, 'synthetic-burst')
    ms = {r['ordinal']: r['ms'] for r in g['rows']}
    out.append(('burst: a delta frame whose blank check and verify are one read run across its page is durable at '
                'that run\'s end', not words and ms[1] is not None and abs(ms[1] - 2500) < 1, f'{words} {ms}'))
    torn = frame_[:-4] + bytes(4)
    g = run('burst', base, 1500, journal(base + torn), frame=(torn, 2500))
    words = save_burst.misses(g, 'synthetic-burst')
    out.append(('burst: a delta frame whose CRC does not close is not durable, nor applied at the cut',
                words == ['synthetic-burst: name 1 not durable 5,000 ms after its response, when the run ended',
                          'synthetic-burst: name 1 not in the authoritative container at the cut'], str(words)))
    for name, kw, want in (('refused', dict(status=1), 'answered status 1'),
                           ('unanswered', dict(answered=False), 'was never answered')):
        try:
            run('burst', good, 1500, journal(good), **kw)
            out.append((f'burst: a SET_NAME {name} is refused', False, 'graded'))
        except grade.Refusal as error:
            out.append((f'burst: a SET_NAME {name} is refused', want in str(error), str(error)))
    want = 3 + 2 + -(-(IMAGE - 4) // 256)
    g = run('flight', good, 1500, steps=want)
    out.append(('flight: a next save whose capture and seal take every step after the verify passes',
                not save_burst.misses(g, 'synthetic-flight') and g['next_steps']['steps'] == want,
                str(g['next_steps'])))
    g = run('flight', good, 1500, steps=want + 1)
    words = save_burst.misses(g, 'synthetic-flight')
    out.append(('flight: a next save that waited a step past its capture and seal fails',
                len(words) == 1 and 'did not start at the first idle step' in words[0], str(words)))
    return out
