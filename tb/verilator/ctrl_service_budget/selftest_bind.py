# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's checks of the binding class's grade (bind_save.py, #1009) and of a save's verify (save_grade.py):
synthetic logs of whole saves, each command timed from its response to the save whose container holds its value, the
kind of save each group times, the part's times the run modelled, and a verify that must read back every programmed byte
after its last page, each byte once, read against containers built here from KLJ3's and layout 3's layout."""
from __future__ import annotations

import os
import struct
import tempfile
import zlib
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

import bind_save
import grade
import save_grade
import scenario
from selftest_burst import IMAGE, NAMES, SLOT, frame
from selftest_burst import container as name_container
from selftest_burst import group as name_group

Check = tuple[str, bool, str]
BASE = 26                      # the BINDING block (nvm_layout3.h)
BOUND, STOPPED, UNBOUND = bind_save.record(True), bind_save.record(False), bytes(bind_save.BIND_LEN)
HALF = 640 * 1024 // 2
SEALS, READS, PAGES = -(-(IMAGE - 4) // 256), IMAGE // 128, IMAGE // 256


def container(binds: dict[int, bytes], seq: int) -> bytes:
    """A KLJ3 container of IMAGE bytes holding each sink's binding record, its CRC-32 closing."""
    body = struct.pack('<10I', 0x334A4C4B, 0x00030000, seq, len(binds) + 1, IMAGE, 0, 0, 0, 0, 3)
    body += b'\xff' * 18 + b''.join(frame(BASE + k, v) for k, v in sorted(binds.items()))
    body = body.ljust(IMAGE - 4, b'\0')
    return body + struct.pack('<I', zlib.crc32(body))


def journal(blob: bytes) -> bytes:
    """A journal whose slot A holds blob and slot B an older container."""
    return blob.ljust(HALF, b'\xff') + container({}, 1).ljust(HALF, b'\xff')


def acmp_response(message: int, seq: int, status: int = 0) -> bytes:
    """A BIND_RX_RESPONSE (7) or an UNBIND_RX_RESPONSE (9) with its sequence_id and status (bind_save reads them)."""
    pdu = bytearray(68)
    pdu[14], pdu[15] = 0xFC, 0x80 | message
    pdu[16] = status << 3
    struct.pack_into('>H', pdu, 62, seq)
    return bytes(pdu)


def save(ms: int, blob: bytes, at: float, slot: int = SLOT, verify: list[tuple[int, int]] | None = None,
         blank: tuple[int, int] | None = None) -> list[str]:
    """A whole save at `at` ms: its seal's CRC calls, its erase 1 ms later, an erase of 120 ms, the blank check's read
    calls, its pages 2 ms apart, then the verify's read calls and its runs of reads (verify: (offset, bytes) each, the
    whole container by default), the last one durable; blank adds a run of reads from the blank check to that one."""
    c = lambda t: int(t * ms)
    erase = at + 1
    lines = [f'CALL {c(at + 0.1 * k)} 1 {bind_save.SEAL_CALL}' for k in range(SEALS)]
    lines += [f'FLASHOP {c(erase)} {grade.FLASH_ERASE} {slot:06x} 0']
    lines += [f'CALL {c(erase + 121 + k)} 1 {bind_save.READ_CALL}' for k in range(READS)]
    lines += [f'FLASHRD {c(erase + 121)} {c(erase + 121 + READS - 0.5)} {slot:06x} {IMAGE}'] if blank is None else []
    pages = erase + 121 + READS
    for n in range(PAGES):
        lines += [f'FLASHOP {c(pages + 2 * n)} {grade.FLASH_PROGRAM} {slot + 256 * n:06x} 256',
                  f'FLASHDATA {c(pages + 2 * n)} {slot + 256 * n:06x} {blob[256 * n:256 * n + 256].hex()}']
    start = pages + 2 * PAGES
    lines += [f'CALL {c(start + k)} 1 {bind_save.READ_CALL}' for k in range(READS)]
    for k, (offset, n) in enumerate(verify if verify is not None else [(0, IMAGE)]):
        lines.append(f'FLASHRD {c(start + k)} {c(start + k + 0.5)} {slot + offset:06x} {n}')
    if blank is not None:
        lines.append(f'FLASHRD {c(erase + 121)} {c(start + 0.5)} {slot + blank[0]:06x} {blank[1]}')
    return lines


def save_end(at: float, reads: int = 1) -> float:
    """The ms a save at `at` is durable at, its verify read in `reads` runs."""
    return at + 1 + 121 + READS + 2 * PAGES + reads - 1 + 0.5


def graded(m: ModuleType, kind: str, ops: list[dict], answers: dict[int, float], lines: list[str],
           **spec: object) -> dict:
    """The bind grade of a log: each answered op's response, and those of the commands before them that it does not
    grade (spec's before), at its ms (answers), with spec's status (0), then the lines, the part's times (spec's flash,
    the group's by default), the journal at the cut (spec's cut; None: none written); the rest of spec is the
    group's."""
    cut = spec.pop('cut')
    flash = spec.pop('flash', bind_save.FLASH_US)
    before, status = spec.pop('before', ()), spec.pop('status', 0)
    ms, us = m.SYS_HZ // 1000, m.SYS_HZ // 1_000_000
    sent = [o for o in (*before, *ops) if o['seq'] in answers]
    acmp = [(0, acmp_response(7 if o['kind'] == 'BIND_RX' else 9, o['seq'], status), int(answers[o['seq']] * ms))
            for o in sent if o['kind'] in ('BIND_RX', 'UNBIND_RX')]
    aecp = [(0, m.aem_response(scenario.CTL1, o['seq'], command=bind_save.STOP_STREAMING), int(answers[o['seq']] * ms))
            for o in sent if o['kind'] not in ('BIND_RX', 'UNBIND_RX')]
    out = m.tx_sequence(scenario.CH['acmp'], acmp) + (m.tx_sequence(scenario.CH['aecp'], aecp) if aecp else [])
    sums = f'SUMMARY passes=1 flash_erase={flash[0] * us} flash_program={flash[1] * us}'
    text = '\n'.join([*out, *lines, sums, 'RESULT: PASS']) + '\n'
    bind = dict(dict(kind=kind, image=IMAGE, base=BASE, target_ms=800, ops=ops), **spec)
    group = scenario.Group(f'synthetic-{kind}', save=dict(journal=True, flash_us=bind_save.FLASH_US, bind=bind))
    with tempfile.TemporaryDirectory() as tmp:
        path = None
        if cut is not None:
            path = Path(tmp) / 'cut.journal'
            path.write_bytes(cut)
        return grade.grade(text, group, m.SYS_HZ, m.CPU_HZ, journal=path)['bind']


def refused(call: object) -> str:
    """The refusal a grade raised, or '' when it graded."""
    try:
        call()
    except grade.Refusal as error:
        return str(error)
    return ''


def idle_checks(m: ModuleType) -> list[Check]:
    """An idle store's commands: each its own save, within the gate, held at the cut; a save in flight, a second save,
    a save before the window, a late or missing value, a refused or unanswered command, other flash times, each fail."""
    ms = m.SYS_HZ // 1000
    ops = [bind_save.op('BIND_RX', 0, 0x9500), bind_save.op('STOP_STREAMING', 0, 0x9501)]
    answers = {0x9500: 10.0, 0x9501: 1000.0}
    one, two = container({0: BOUND}, 2), container({0: STOPPED}, 3)
    lines = save(ms, one, 110) + save(ms, two, 1100, SLOT + 0x50000)
    run = lambda lines_, cut=journal(two), **k: graded(m, 'idle', ops, answers, lines_, cut=cut, **k)
    words = lambda g: bind_save.misses(g, 'synthetic-idle')
    out = []
    g = run(lines)
    out.append(('bind: an idle store\'s commands, each durable by a whole save of its own within the gate, pass',
                not words(g) and [r['ms'] for r in g['rows']] == [round(save_end(110) - 10, 3),
                                                                 round(save_end(1100) - 1000, 3)]
                and g['saves'] == g['erases'] == 2, f"{words(g)} {g['rows']}"))
    g = run(save(ms, one, 110) + save(ms, two, 1700, SLOT + 0x50000))
    out.append(('bind: a command durable past the gate fails by its name',
                any('STOP_STREAMING of sink 0 durable' in w and 'over its target' in w for w in words(g)),
                str(words(g))))
    g = run(save(ms, one, 110) + save(ms, container({0: BOUND}, 3), 1100, SLOT + 0x50000), journal(one))
    out.append(('bind: a command no save holds fails by its name', any('not durable' in w for w in words(g)),
                str(words(g))))
    g = run(save(ms, one, 950) + save(ms, two, 1300, SLOT + 0x50000))
    out.append(('bind: a command that came with a save in flight is not an idle store\'s',
                any('save in flight, not to an idle store' in w for w in words(g)), str(words(g))))
    g = run(save(ms, one, 110) + save(ms, one, 400, SLOT + 0x50000) + save(ms, two, 1100))
    out.append(('bind: a command that took two saves fails', any('took 2 saves, not one' in w for w in words(g)),
                str(words(g))))
    g = run(save(ms, one, 40) + save(ms, two, 1100, SLOT + 0x50000))
    out.append(('bind: a save that erased its slot before the command\'s window is another change\'s',
                any('before its window' in w for w in words(g)), str(words(g))))
    g = run(lines, journal(one))
    out.append(('bind: a sink whose last value the cut lacks fails', any('at the cut' in w for w in words(g)),
                str(words(g))))
    g = run(lines, None)
    out.append(('bind: a run that left no journal fails', 'synthetic-idle: the run left no journal' in words(g),
                str(words(g))))
    why = refused(lambda: run(lines, flash=(0, 0)))
    out.append(('bind: a run under other flash times than the group\'s is refused', 'modelled an erase of 0 us' in why,
                why))
    why = refused(lambda: graded(m, 'idle', ops, {0x9500: 10.0}, lines, cut=journal(two)))
    out.append(('bind: an unanswered command is refused', 'was never answered' in why, why))
    why = refused(lambda: graded(m, 'idle', ops, answers, lines, cut=journal(two), status=1))
    out.append(('bind: a command answered with an error status is refused', 'answered status 1' in why, why))
    newer = container({}, 1).ljust(HALF, b'\xff') + two.ljust(HALF, b'\xff')
    g = run(lines, newer)
    out.append(('bind: the cut reads the newer accepted slot, slot B here', not words(g), str(words(g))))
    again = [bind_save.op('BIND_RX', 0, 0x9500)]
    g = graded(m, 'idle', again, {0x9500: 500.0}, save(ms, one, 110) + save(ms, container({0: BOUND}, 3), 600,
                                                                          SLOT + 0x50000), cut=journal(one))
    out.append(('bind: a save erased before the response is not its command\'s, though it holds the value',
                g['rows'][0]['ms'] == round(save_end(600) - 500, 3), str(g['rows'])))
    return out


def flight_checks(m: ModuleType) -> list[Check]:
    """A bind in another save: the save in flight without it, then its own, within the bound, its response in its
    arrival's phase; a bind the save in flight took, one in another phase, a third save, each fail."""
    ms = m.SYS_HZ // 1000
    ops = [bind_save.op('BIND_RX', 0, 0x9A00)]
    first, own = name_container(NAMES, 2), container({0: BOUND}, 3)
    # the boot's container check runs the CRC too: the seal is the save's own stretches before its erase
    lines = [f'CALL {5 * ms} 1 {bind_save.SEAL_CALL}', *save(ms, first, 100), *save(ms, own, 400, SLOT + 0x50000)]
    run = lambda lines_, at=180.0, phase='erase', part=(0.4, 1.0): graded(
        m, 'flight', ops, {0x9A00: at}, lines_, cut=journal(own), phase=phase, part=part, target_ms=950)
    words = lambda g: bind_save.misses(g, 'synthetic-flight')
    out = []
    g = run(lines)
    out.append(('flight: a bind in the save in flight\'s erase, durable by the next save within the bound, passes',
                not words(g) and g['rows'][0]['ms'] == round(save_end(400) - 180, 3), f"{words(g)} {g['rows']}"))
    g = run(lines, phase='seal', part=(0.0, 0.5))
    out.append(('flight: a bind whose response came in another phase than its arrival\'s fails',
                any("of the save's erase phase, not in" in w for w in words(g)), str(words(g))))
    g = run(lines, at=100.05, phase='seal', part=(0.0, 0.5))
    out.append(('flight: a bind just after the capture is in the seal\'s first part', not words(g), str(words(g))))
    g = run(lines, at=save_end(100) - 0.1, phase='verify', part=(0.5, 1.0))
    out.append(('flight: a bind late in the verify is graded there', not words(g), str(words(g))))
    g = run(save(ms, container({0: BOUND}, 2), 100) + save(ms, own, 400, SLOT + 0x50000))
    out.append(('flight: a save in flight that holds the bind took it in its capture, and fails',
                any('came before that save\'s capture ended' in w for w in words(g)), str(words(g))))
    g = run(lines + save(ms, own, 800))
    out.append(('flight: a run of three saves is not the one in flight and the bind\'s own',
                any('took 3 saves' in w for w in words(g)), str(words(g))))
    return out


def burst_checks(m: ModuleType) -> list[Check]:
    """A burst: its last commands timed, its saves at most its cap; one save, or more than the cap, fails."""
    ms = m.SYS_HZ // 1000
    ops = [bind_save.op('BIND_RX', 0, 0x9800), bind_save.op('UNBIND_RX', 0, 0x9801)]
    answers = {0x9800: 10.0, 0x9801: 150.0}
    last = container({0: UNBOUND}, 3)
    lines = save(ms, container({0: BOUND}, 2), 110) + save(ms, last, 400, SLOT + 0x50000)
    run = lambda lines_, cap=2: graded(m, 'burst', ops[1:], answers, lines_, cut=journal(last), before=tuple(ops[:1]),
                                       first=0x9800, saves_max=cap, all=2, target_ms=950)
    words = lambda g: bind_save.misses(g, 'synthetic-burst')
    out = []
    g = run(lines)
    out.append(('burst: the last command durable within the bound by the second save passes',
                not words(g) and g['commands'] == 2 and g['erases'] == 2, f"{words(g)} {g['rows']}"))
    g = run(lines, cap=1)
    out.append(('burst: more erases than the burst may take fail', any('more than 1' in w for w in words(g)),
                str(words(g))))
    g = run(save(ms, last, 200))
    out.append(('burst: a burst of one save had no command during another save, and fails',
                any('no command arrived during another save' in w for w in words(g)), str(words(g))))
    return out


def verify_checks(m: ModuleType) -> list[Check]:
    """A save is durable once its verify has read back every programmed byte after its last page, each byte once, and
    through the bind and burst grades: none, part, the same bytes twice, or the blank check's reads make no save
    durable, a run of reads across a write is refused, and runs are not merged across a write."""
    ms = m.SYS_HZ // 1000
    ops = [bind_save.op('BIND_RX', 0, 0x9500)]
    one = container({0: BOUND}, 2)
    rows = lambda verify=None, blank=None: graded(m, 'idle', ops, {0x9500: 10.0}, save(ms, one, 110, verify=verify,
                                                                                     blank=blank), cut=journal(one))
    durable = lambda g: g['rows'][0]['ms'] is not None and not g['faults']
    halves = [(0, IMAGE // 2), (IMAGE // 2, IMAGE // 2)]
    out = [('verify: a verify that reads back every byte, in two runs, makes the save durable at the second',
            durable(g := rows(halves)) and g['rows'][0]['ms'] == round(save_end(110, 2) - 10, 3), str(g['rows'])),
           ('verify: a save with no read-back after its last page is not durable', not durable(rows([])), ''),
           ('verify: a read-back of part of the container is not durable',
            not durable(g := rows([(0, IMAGE - 128)])) and any('not a whole container' in f for f in g['faults']),
            str(g['faults'])),
           ('verify: the same half read back twice is not the whole container', not durable(rows(halves[:1] * 2)), ''),
           ('verify: the blank check\'s reads before the pages do not count, so a partial verify stays not durable',
            not durable(rows([(0, IMAGE // 2)])), '')]
    why = refused(lambda: rows([(0, IMAGE // 2)], blank=(IMAGE // 2, IMAGE // 2)))
    out.append(('verify: a run of reads across a page program is refused, so its bytes never count as read back',
                'spans a write of the device' in why, why))
    log = grade.Log(m.SYS_HZ, m.CPU_HZ, flash_ops=[(150, grade.FLASH_PROGRAM, SLOT, 256)],
                    reads=[(100, 120, SLOT, 128), (200, 220, SLOT + 128, 128)])
    out.append(('verify: two runs of reads with a write between them are not merged into one read-back',
                len(save_grade.merged_reads(log)) == 2, str(save_grade.merged_reads(log))))
    names = name_container(NAMES, 6)
    text = lambda verify: m.synthetic([*m.tx_sequence(scenario.CH['aecp'], [
        (0, m.aem_response(scenario.CTL2, 0x9000 + 2 * k), 1000 + k) for k in NAMES]),
        *save(ms, names, 110, verify=verify)])
    with tempfile.TemporaryDirectory() as tmp:
        cut = Path(tmp) / 'cut.journal'
        cut.write_bytes(journal(names))
        never = lambda verify: grade.grade(text(verify), name_group('burst'), m.SYS_HZ, m.CPU_HZ,
                                           journal=cut)['burst']['never']
        out.append(('verify: the burst grade times a name only to a save read back whole',
                    never(None) == [] and never(halves[:1] * 2) == sorted(NAMES), f'{never(None)} {never(halves[:1])}'))
    return out


def arrival_checks() -> list[Check]:
    """The binds in flight cover at least eight arrivals, one just after the capture, in every phase of a save."""
    rows = bind_save.arrivals(3444)
    phases = {phase for _, phase, *_ in rows}
    with patch.dict(os.environ, BUDGET_FLASH_US='1:1', BUDGET_JOURNAL_OUT='elsewhere'):
        env = bind_save.environment(dict(flash_us=(120000, 500)), Path('j'))
        plain = bind_save.environment(dict(), Path('j'))
    return [('arrivals: at least eight, the first just after the capture, every phase of a save',
             len(rows) >= 8 and rows[0][:2] == ('capture', 'seal') and rows[0][4][0].startswith(
                 f'call {bind_save.SEAL_CALL} 1 ')
             and phases == {'seal', 'erase', 'blank', 'program', 'verify'}, str(rows)),
            ('environment: a group that models the part has its times, and no other group has any',
             env.get('BUDGET_FLASH_US') == '120000:500' and 'BUDGET_FLASH_US' not in plain
             and 'BUDGET_JOURNAL_OUT' not in plain, f"{env.get('BUDGET_FLASH_US')} {plain.get('BUDGET_FLASH_US')}")]


def bind_checks(m: ModuleType) -> list[Check]:
    """Every check of this module (m: the self-test)."""
    return [*idle_checks(m), *flight_checks(m), *burst_checks(m), *verify_checks(m), *arrival_checks(),
            ('bind: the targets are the scope ruling\'s (#1009, items 3 and 4; the Arty points by PR #1004\'s rule)',
             bind_save.IDLE_MS == 800 and bind_save.FLIGHT_MS == {'1x1': 450, '8x8-1if': 950, 'arty-1x1': 400,
                                                                 'arty-4x4': 550}
             and bind_save.BURST_SAVES == {'1x1': 4, '8x8-1if': 3, 'arty-1x1': 4, 'arty-4x4': 4}
             and bind_save.FLASH_US == (120000, 500), '')]
