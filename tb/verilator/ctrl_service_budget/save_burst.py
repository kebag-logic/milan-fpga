# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""A burst of name changes, and a change marked while a save is in flight, under the contract's held load (#920).

THE TARGET (#665's ruling of 2026-11-15, item 1): at 1x1/1if and 8x8/1if, under the contract's held
load, every acknowledged change is durable within TARGET_MS of its response, a burst marking every name and a change
marked during a save in flight included. Milan v1.2 5.3.13 requires the names saved in non-volatile memory and
restored after a power cycle; the 5 s is the ruling's, and the cut CUT_MS after the last response the in-house
persistence scenario's.

`save-burst`: a SET_NAME (IEEE 1722.1-2021 7.4.17) of every name the image's table holds (AECP_ENTITY_NAMES_INIT), each
followed by a GET_NAME (7.4.18) of it, as a controller sets each name and reads it back. The entity's two names come
first, then every other name from the last ordinal down, so each later mark is of a record before the earlier ones and
a capture that starts during the burst has passed it (nvm_store.c, nvm_mark). The frames go out FRAME_MS apart, the
controller's pace in #665's capture of the finding (1.1 to 1.4 ms from a response to its next command), while the AECP
channel's token bucket holds a token (KL_mbx_rx.sv, the contract's burst and refill); a frame the bucket would refuse
the controller sends RETRY_MS later instead, its command timeout, as the capture shows it doing three times. Every
other receive channel is held at its contract refill rate with its bursts (save_window.arrivals) from the first
SET_NAME to the cut, CUT_MS after the last frame, when the script ends and the testbench writes the journal
(sim_main.cpp, BUDGET_JOURNAL_OUT): the journal a power cut then leaves.

`save-flight`: under the same held load, AECP's bursts one record short so the two SET_NAMEs keep inside its bucket, a
SET_NAME of the entity, which marks both its names, and at the first save's erase, once its capture is over, a SET_NAME
of the entity to another value. Its records are in flight in the first save, so they are the next save's, which starts
at the first idle step after the first (nvm_store.c, nvm_mark and nvm_idle).

THE GRADE. Each save is read off the testbench's flash lines: its erase (FLASHOP), the bytes each page program left
(FLASHDATA), and the read-backs after its last page, the verify, which make it durable (save_grade.first_save). Its
container is the programmed pages over an erased slot, accepted when its magic, length and CRC-32 close (KLJ3,
nvm_klj2.c), and a name is in it when its layout 3 frame (nvm_layout3.h: the NAME block's base and the ordinal) carries
the value with a closing crc16. A change is durable at the first durable save whose container holds its value, timed
from its SET_NAME's response (the AECP TX commit with its sequence_id), which must be SUCCESS. At the cut the journal's
authoritative container (section 7: the newer accepted slot) must hold every name. `save-flight` must also take no step
between the first save's verify and the next save's erase but the next save's capture and seal: its capture starts at
the first idle step, with no window.
"""
from __future__ import annotations

import math
import re
import struct
import sys
import zlib
from pathlib import Path
from typing import TYPE_CHECKING

import frames as f
import save_window
import scenario

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
import nvm_layout3  # noqa: E402

if TYPE_CHECKING:
    import grade as grader  # grade.py imports this module

#: The ruling's target, the persistence scenario's cut, and the store's first-dirty window (DR2a), in ms.
TARGET_MS, CUT_MS = 5000, 10000
#: The controller's pace, from a frame to its next one, and its command timeout, in ms (#665's capture of the finding).
FRAME_MS, RETRY_MS = 1.3, 250.0
#: The bucket refills one token a period up to its burst on the fabric's ms tick (KL_mbx_rx.sv, buckets), whose phase
#: the script does not know: the schedule counts a refill this long after its period ends and sends only while it holds
#: TOKEN_MARGIN tokens more than the frame takes, so it never sends a frame the fabric refuses.
TOKEN_SLACK_MS, TOKEN_MARGIN = 1.0, 1
#: The commands (IEEE 1722.1-2021 Table 7-125) and the sequence_ids the burst gives them.
SET_NAME, GET_NAME = 0x0010, 0x0011
SEQ = 0x9000
#: KLJ3 (nvm_shape.h, nvm_klj2.c): the magic, the header and trailer, and the layout 3 frame's magic and version.
KLJ3_MAGIC, KLJ_HDR, TRAILER = 0x334A4C4B, 40, 4
REC_MAGIC, LAYOUT, NAME_BYTES = 0x1722, 3, 64


def names(build: dict) -> list[tuple[int, int, int]]:
    """The image's writable names in their table order (aecp_shape.py, AECP_ENTITY_NAMES_INIT): (descriptor type,
    index, name_index) at each ordinal, whose record is the layout 3 NAME block's base plus the ordinal."""
    header = Path(build['elf']).with_name('aecp_entity_gen.h').read_text()
    body = header.split('#define AECP_ENTITY_NAMES_INIT', 1)[1].split('}\n', 1)[0] + '}'
    rows = re.findall(r'\{AECP_CHANGE_NAME,(\d+),(\d+),(\d+)\}', body)
    if not rows:
        raise RuntimeError('the image declares no writable name (AECP_ENTITY_NAMES_INIT)')
    return [(int(t), int(i), int(n)) for t, i, n in rows]


def name_base() -> int:
    """The layout 3 NAME block's first record id (nvm_layout3.h)."""
    return nvm_layout3.read().block('NAME').base


def value(ordinal: int, tag: bytes = b'burst') -> bytes:
    """A 64-byte name no default carries, one per ordinal."""
    return (tag + b' %03d' % ordinal).ljust(NAME_BYTES, b'\0')


def name_command(p: scenario.Point, command: int, seq: int, name: tuple[int, int, int], text: bytes = b'') -> bytes:
    """SET_NAME of `name` to `text`, or GET_NAME of it, from a controller, in configuration 0."""
    kind, index, name_index = name
    payload = f.be(kind, 2) + f.be(index, 2) + f.be(name_index, 2) + f.be(0, 2) + text
    return f.aem_command(f.Aem(p.entity_id, scenario.CTL2, scenario.CTL_MAC, p.mac, seq), command, payload)


def order(table: list[tuple[int, int, int]]) -> list[int]:
    """The burst's ordinals: the entity's names first, then every other one from the last down."""
    entity = [k for k, (kind, _, _) in enumerate(table) if kind == 0]
    return entity + [k for k in reversed(range(len(table))) if k not in entity]


def schedule(count: int) -> list[float]:
    """The ms, from the first, of each of `count` AECP frames sent FRAME_MS apart while the channel's bucket holds a
    token and RETRY_MS later where it would not: the bucket full at the first, one token a frame, and one a refill
    period up to the burst (KL_mbx_rx.sv), each refill TOKEN_SLACK_MS late and TOKEN_MARGIN tokens kept."""
    ch = scenario.CONTRACT.channels[scenario.CH['aecp']]
    times, at, tokens, refilled = [], 0.0, ch.burst, 0
    for _ in range(count):
        while True:
            while (refilled + 1) * ch.refill_ms + TOKEN_SLACK_MS <= at:
                refilled += 1
                tokens = min(ch.burst, tokens + 1)
            if tokens > TOKEN_MARGIN:
                break
            at += RETRY_MS
        tokens -= 1
        times.append(at)
        at += FRAME_MS
    return times


def held(p: scenario.Point, run_ms: float, aecp: bool) -> list[tuple[float, str, str]]:
    """Every receive channel but AECP at its contract refill rate with its bursts for run_ms (save_window.arrivals),
    and AECP with its bursts one record short where `aecp`, so two commands of the group keep inside its bucket."""
    load = [a for a in save_window.arrivals(p, run_ms) if a[1] != 'aecp']
    if aecp:
        ch = scenario.CONTRACT.channels[scenario.CH['aecp']]
        read = f.read_descriptor(f.Aem(p.entity_id, scenario.CTL1, scenario.CTL_MAC, p.mac, 0), 0, 0)
        at_once = scenario.admission('aecp', read)['at_once'] - 1
        start, n = save_window.held_start() + save_window.OFFSET_MS * scenario.CH['aecp'], 0
        while start < run_ms:
            for _ in range(at_once):
                frame = f.read_descriptor(f.Aem(p.entity_id, scenario.CTL1, scenario.CTL_MAC, p.mac,
                                                0x8000 + n % 0x8000), 0, 0)
                load.append((start, 'aecp', f'frame {n % p.interfaces} {frame.hex()}'))
                n += 1
            start += at_once * ch.refill_ms
    return sorted(load, key=lambda a: a[0])


def timed(g: scenario.Group, events: list[tuple[float, str, str]], until_ms: float) -> None:
    """The events in time order, each at its ms from now, then the script waits to until_ms."""
    ms, at = scenario.MS, 0
    for when, _, step in events:
        cycles = round(when * ms)
        if cycles > at:
            g.add(f'wait cycles {cycles - at}')
            at = cycles
        g.add(step)
    g.add(f'wait cycles {max(round(until_ms * ms) - at, 0)}')


def burst(p: scenario.Point, build: dict) -> scenario.Group:
    """`save-burst`: every name set and read back as a controller does, under the held load, cut CUT_MS after."""
    table = names(build)
    image = save_window.container(build)
    ordinals = order(table)
    times = schedule(2 * len(ordinals))
    run_ms = times[-1] + CUT_MS
    aecp, sets = [], []
    for n, k in enumerate(ordinals):
        seq = SEQ + 2 * n
        aecp.append((times[2 * n], 'aecp', f'frame 0 {name_command(p, SET_NAME, seq, table[k], value(k)).hex()}'))
        aecp.append((times[2 * n + 1], 'aecp', f'frame 0 {name_command(p, GET_NAME, seq + 1, table[k]).hex()}'))
        sets.append(dict(ordinal=k, seq=seq, value=value(k).hex()))
    load = held(p, run_ms, aecp=False)
    offered = {c: sum(1 for _, ch, _ in load if ch == c) + (2 * len(ordinals) if c == 'aecp' else 0)
               for c in scenario.CH}
    g = scenario.Group('save-burst', sim_ms=int(run_ms) + 3200,
                       save=dict(loaded=True, offered=offered, journal=True,
                                 named=dict(kind='burst', image=image, base=name_base(), sets=sets,
                                            target_ms=TARGET_MS, cut_ms=CUT_MS)))
    scenario.ready(g, p)
    scenario.announced(g)
    g.add('mark save.change')
    timed(g, sorted(load + aecp, key=lambda a: a[0]), run_ms)
    return g


def flight(p: scenario.Point, build: dict) -> scenario.Group:
    """`save-flight`: a SET_NAME of the entity, and another at the first save's erase, under the held load."""
    table = names(build)
    image = save_window.container(build)
    entity = next(k for k, (kind, _, n) in enumerate(table) if kind == 0 and n == 0)
    run_ms = 2 * TARGET_MS + 1000
    first = name_command(p, SET_NAME, SEQ, table[entity], value(entity, b'first'))
    second = name_command(p, SET_NAME, SEQ + 2, table[entity], value(entity, b'again'))
    load = held(p, run_ms, aecp=True)
    offered = {c: sum(1 for _, ch, _ in load if ch == c) + (2 if c == 'aecp' else 0) for c in scenario.CH}
    # the SET_NAME changes the entity_name and marks both its names (aecp_nvm.c), so the next save captures two
    marks = [k for k, (kind, _, _) in enumerate(table) if kind == 0]
    g = scenario.Group('save-flight', sim_ms=int(run_ms) + 3200,
                       save=dict(loaded=True, offered=offered,
                                 named=dict(kind='flight', image=image, base=name_base(), target_ms=TARGET_MS,
                                            records=len(marks),
                                            sets=[dict(ordinal=entity, seq=SEQ + 2,
                                                       value=value(entity, b'again').hex())])))
    scenario.ready(g, p)
    scenario.announced(g)
    ms = scenario.MS
    # the load and the first SET_NAME are timed from the change; the second waits for the first save's erase, which
    # comes after its first-dirty window, and the load after it keeps its times from there
    early = [a for a in load if a[0] < save_window.DIRTY_MS]
    late = [(when - save_window.DIRTY_MS, ch, step) for when, ch, step in load if when >= save_window.DIRTY_MS]
    g.add('mark save.change', f'frame 0 {first.hex()}')
    timed(g, early, save_window.DIRTY_MS)
    g.add(f'wait flash erase 1 within {3000 * ms}', 'mark save.second', f'frame 0 {second.hex()}')
    timed(g, late, run_ms - save_window.DIRTY_MS)
    return g


def groups(p: scenario.Point, build: dict) -> list[scenario.Group]:
    """The burst and the change in flight."""
    return [burst(p, build), flight(p, build)]


def names_of_groups() -> list[str]:
    """The groups' names, at any point: build.py's planted defects run them."""
    return ['save-burst', 'save-flight']


# ---- the grade ---------------------------------------------------------------------------------------------------

def crc16(data: bytes) -> int:
    """The layout 3 frame's CCITT-FALSE crc16 (nvm_klj2.c, nvm_crc16_update from 0xffff)."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def accepted(blob: bytes, image: int) -> int | None:
    """The sequence of a KLJ3 container of `image` bytes whose magic, length and CRC-32 close, else None."""
    if len(blob) < image or image < KLJ_HDR + TRAILER:
        return None
    magic, _, seq, _, length = struct.unpack_from('<5I', blob, 0)
    if magic != KLJ3_MAGIC or length != image:
        return None
    if zlib.crc32(blob[:image - TRAILER]) != struct.unpack_from('<I', blob, image - TRAILER)[0]:
        return None
    return seq


def held_names(blob: bytes, image: int, base: int) -> dict[int, bytes]:
    """Every name frame in a container, by ordinal: each layout 3 frame of the NAME block, 64 payload bytes, whose
    crc16 closes, wherever its offset (the frames before it may be erased, of any length)."""
    out, at = {}, KLJ_HDR
    head = struct.pack('>HBB', REC_MAGIC, LAYOUT, 0)
    while True:
        at = blob.find(head, at, image - TRAILER)
        if at < 0:
            return out
        rid, plen, crc = struct.unpack_from('>HHH', blob, at + 4)
        payload = blob[at + 10:at + 10 + plen]
        if (plen == NAME_BYTES and rid >= base and len(payload) == plen
                and crc16(blob[at:at + 8] + payload) == crc):
            out[rid - base] = payload
        at += 1


def saves(log: grader.Log, image: int) -> list[dict]:
    """Every save the log shows: its erase, the container its pages left over an erased slot, its sequence when the
    container is accepted, and when it is durable (save_grade.first_save), or None."""
    import grade
    import save_grade
    out = []
    # one save an erase the log shows, its blocks erased in one step (NVM_ERASE_BLOCKS is 1 at every shape)
    erases = sorted(c for c, op, _, _ in log.flash_ops if op == grade.FLASH_ERASE)
    for n in range(len(erases)):
        save = save_grade.first_save(log, n)
        if save is None:
            break
        stop = next((c for c in erases if c > save.erase), 1 << 62)
        blob = bytearray(b'\xff' * image)
        for cycle, addr, data in log.programmed:
            if save.erase < cycle < stop and save.base <= addr < save.base + image:
                blob[addr - save.base:addr - save.base + len(data)] = data[:image - (addr - save.base)]
        seq = accepted(bytes(blob), image)
        out.append(dict(erase=save.erase, base=save.base, durable=save.durable if seq is not None else None,
                        seq=seq, blob=bytes(blob)))
    return out


def responses(log: grader.Log) -> dict[int, tuple[int, int]]:
    """Each AEM_RESPONSE the AECP channel committed (IEEE 1722.1-2021 9.2.1.2): sequence_id -> (cycle, status)."""
    out = {}
    for cycle, ch, _, frame in log.tx:
        if ch != scenario.CH['aecp'] or len(frame) < 38 or frame[14] != 0xFB or frame[15] & 0x0F != 1:
            continue
        seq = struct.unpack_from('>H', frame, 34)[0]
        out.setdefault(seq, (cycle, frame[16] >> 3))
    return out


def newer(path: Path, image: int) -> tuple[int | None, bytes]:
    """The journal a cut leaves: its authoritative container (section 7: the newer accepted slot, wrap-safe, slot A
    on a tie), its sequence and bytes, or (None, b'') with no slot accepted."""
    data = path.read_bytes()
    half = len(data) // 2
    slots = [(accepted(data[o:o + image], image), data[o:o + image]) for o in (0, half)]
    good = [(s, b) for s, b in slots if s is not None]
    if not good:
        return None, b''
    return good[0] if len(good) == 1 or ((good[0][0] - good[1][0]) & 0xFFFFFFFF) < 1 << 31 else good[1]


def journal(path: Path, image: int, base: int) -> tuple[int | None, dict[int, bytes]]:
    """The authoritative container's names at the cut (newer), or (None, {}) with no slot accepted."""
    seq, blob = newer(path, image)
    return seq, held_names(blob, image, base)


def grade(log: grader.Log, group: scenario.Group, journal_path: Path | None) -> dict | None:
    """A burst's or a change in flight's names, each from its response to durable against TARGET_MS, the
    authoritative container at the cut, and the change in flight's next save from the first idle step."""
    import grade as grader
    spec = group.save.get('named')
    if spec is None:
        return None
    image, base = spec['image'], spec['base']
    answered = responses(log)
    done = saves(log, image)
    rows = []
    for s in spec['sets']:
        if s['seq'] not in answered:
            raise grader.Refusal(f"{group.name}: the SET_NAME of name {s['ordinal']} was never answered")
        cycle, status = answered[s['seq']]
        if status != 0:
            raise grader.Refusal(f"{group.name}: the SET_NAME of name {s['ordinal']} answered status {status}")
        want = bytes.fromhex(s['value'])
        holds = [d for d in done if d['durable'] is not None and d['erase'] > cycle
                 and held_names(d['blob'], image, base).get(s['ordinal']) == want]
        durable = min((d['durable'] for d in holds), default=None)
        ms = round(log.ms_of(durable - cycle), 3) if durable is not None else None
        rows.append(dict(ordinal=s['ordinal'], response_sys=cycle, durable_sys=durable, ms=ms,
                         within=ms is not None and ms <= spec['target_ms']))
    out = dict(kind=spec['kind'], names=len(rows), target_ms=spec['target_ms'],
               saves=[dict(erase=d['erase'], durable=d['durable'], seq=d['seq']) for d in done], rows=rows)
    timed_rows = [r for r in rows if r['ms'] is not None]
    worst = max(rows, key=lambda r: (r['ms'] is None, r['ms'] or 0))
    out.update(worst_ms=worst['ms'], worst_ordinal=worst['ordinal'],
               never=[r['ordinal'] for r in rows if r['ms'] is None],
               over=[r['ordinal'] for r in timed_rows if not r['within']])
    if spec['kind'] == 'burst':
        left = journal_path is not None and journal_path.exists()
        seq, held = journal(journal_path, image, base) if left else (None, {})
        missing = [s['ordinal'] for s in spec['sets'] if held.get(s['ordinal']) != bytes.fromhex(s['value'])]
        out.update(cut_seq=seq, cut_missing=missing, journal=left)
    else:
        out.update(next_steps=next_steps(log, done, spec, image))
    return out


def next_steps(log: grader.Log, done: list[dict], spec: dict, image: int) -> dict:
    """The steps between the first save's verify and the next save's erase, and those its capture and seal take: the
    step that starts the capture, one for each of its records and one that finds none left, and the seal's stretches
    (save_window.steps), and the erase's own."""
    want = 3 + spec['records'] + math.ceil((image - TRAILER) / save_window.PAGE)
    if len(done) < 2 or done[0]['durable'] is None:
        return dict(steps=None, want=want, gap_ms=None)
    lo, hi = done[0]['durable'], done[1]['erase']
    taken = sum(1 for _, start, *_ in log.stepped if lo < start <= hi)
    return dict(steps=taken, want=want, gap_ms=round(log.ms_of(hi - lo), 3))


def misses(result: dict, group: str) -> list[str]:
    """What fails the run, named by its group: a name not durable within the target, or never, one the
    authoritative container lacks at the cut, and a next save that waited past the first idle step."""
    g = result
    out = [f"{group}: name {k} not durable {g['target_ms']:,} ms after its response, when the run ended"
           for k in g['never']]
    out += [f"{group}: name {r['ordinal']} durable {r['ms']:.3f} ms after its response, over its target "
            f"{g['target_ms']:,} ms" for r in g['rows'] if r['ordinal'] in g['over']]
    if g['kind'] == 'burst':
        if not g['journal']:
            out.append(f'{group}: the run left no journal')
        out += [f'{group}: name {k} not in the authoritative container at the cut' for k in g['cut_missing']]
    elif g['next_steps']['steps'] != g['next_steps']['want']:
        n = g['next_steps']
        out.append(f"{group}: {n['steps']} steps between the save in flight's verify and the next save's erase, "
                   f"{n['gap_ms']} ms, want {n['want']}: its capture did not start at the first idle step")
    return out


def late(results: list[dict]) -> list[str]:
    """Every burst's and change in flight's misses."""
    return [m for g in results if g.get('burst') for m in misses(g['burst'], g['group'])]
