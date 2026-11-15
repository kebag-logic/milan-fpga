# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's checks of each row's stated response (answers.py, #882).

Synthetic traces hold a probe's own response, found by its sequence_id, to the command or message type and the
status its row states, for AEM, MVU and ACMP; the real scenario's rows are each checked to state theirs, a refusal
row to name its refusal, and the get_avb_info row to send GET_AVB_INFO on AVB_INTERFACE 0 at its command's length.
The helpers are selftest.py's, passed as that module.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from types import ModuleType

import answers
import run
import scenario

Check = tuple[str, bool, str]
f = scenario.f
CTL = scenario.CTL1
#: The talker rows' statuses, restated here on purpose (Milan v1.2 Tables 5.42, 5.43 and 5.48): a changed row fails.
TALKER = {'PROBE_TX': 'TALKER_DEST_MAC_FAIL', 'GET_TX_STATE': 'SUCCESS', 'DISCONNECT_TX': 'SUCCESS',
          'GET_TX_CONNECTION': 'NOT_SUPPORTED'}


def aem_frame(sequence: int, command: int, status: int = 0, message: int = 1) -> bytes:
    """An AEM_RESPONSE (message 1) or another AECP message of that command_type, sequence_id and status."""
    frame = bytearray(f.aem_command(f.Aem(1, CTL, 2, 3, sequence), command, bytes(8)))
    frame[15], frame[16] = message, frame[16] | status << 3
    return bytes(frame)


def mvu_frame(sequence: int, command: int, status: int = 0) -> bytes:
    """A Milan MVU response (message 7) of that command_type, sequence_id and status."""
    frame = bytearray(f.mvu_command(f.Aem(1, CTL, 2, 3, sequence), command, bytes(4)))
    frame[15], frame[16] = 7, frame[16] | status << 3
    return bytes(frame)


def graded(h: ModuleType, expect: str, records: list[tuple[bytes, int]], ch: int, row: str = 'row') -> dict:
    """A probe of that expectation over its command and the given responses on interface 0 (frame, commit cycle)."""
    probe = scenario.Probe('s.cmd.if0', row, 'aecp', f'rxc:{ch}', [f'resp:{ch}:41'], expect=expect)
    lines = ['MARK 1000 s.cmd.if0', *h.received(ch, 's.cmd.if0'),
             *h.tx_sequence(ch, [(0, frame, cycle) for frame, cycle in records])]
    return h.one(h.synthetic(lines), probe)


def response_checks(h: ModuleType) -> list[Check]:
    """A probe's own response held to its stated type and status, for AEM, MVU and ACMP."""
    aecp, acmp = scenario.CH['aecp'], scenario.CH['acmp']
    status = lambda r: (r.get('status'), r.get('reason', ''))
    info = answers.aem(0x0027)
    cases = [
        ('a response with the type and status its row states is measured',
         graded(h, info, [(aem_frame(0x41, 0x0027), 5000)], aecp), 'measured', ''),
        ('a response with another status than its row states is refused',
         graded(h, info, [(aem_frame(0x41, 0x0027, 2), 5000)], aecp), 'unexpected response',
         'status NO_SUCH_DESCRIPTOR, not the stated SUCCESS'),
        ('a response to another command type than its row states is refused',
         graded(h, info, [(aem_frame(0x41, 0x0028), 5000)], aecp), 'unexpected response', 'answered as 0028'),
        ("a probe's response is the one answering its sequence_id, not an earlier one on its channel",
         graded(h, info, [(aem_frame(0x40, 0x0028, 2), 3000), (aem_frame(0x41, 0x0027), 5000)], aecp), 'measured', ''),
        ('a refusal its row states and names is measured',
         graded(h, answers.aem(0x3FF0, 'NOT_IMPLEMENTED'), [(aem_frame(0x41, 0x3FF0, 1), 5000)], aecp,
                'unknown_command, refused NOT_IMPLEMENTED'), 'measured', ''),
        ('an MVU response with its stated command type and status is measured',
         graded(h, answers.mvu(0), [(mvu_frame(0x41, 0), 5000)], aecp), 'measured', ''),
        ('an MVU response with another status is refused',
         graded(h, answers.mvu(0), [(mvu_frame(0x41, 0, 1), 5000)], aecp), 'unexpected response', 'status'),
        ('an AEM response where an MVU response is stated is refused',
         graded(h, answers.mvu(0), [(aem_frame(0x41, 0), 5000)], aecp), 'unexpected response', 'no mvu response'),
        ('an ACMP response of another message type is refused',
         graded(h, answers.acmp('GET_RX_STATE_RESPONSE'), [(h.acmp_response(0x41, 'BIND_RX_RESPONSE'), 5000)], acmp),
         'unexpected response', 'answered as BIND_RX_RESPONSE'),
        ('an ACMP response with another status is refused',
         graded(h, answers.acmp('GET_RX_STATE_RESPONSE'), [(h.acmp_response(0x41, status=1), 5000)], acmp),
         'unexpected response', 'status LISTENER_UNKNOWN_ID'),
        ('an ACMP refusal its row states and names is measured',
         graded(h, answers.acmp('GET_TX_CONNECTION_RESPONSE', 'NOT_SUPPORTED'),
                [(h.acmp_response(0x41, 'GET_TX_CONNECTION_RESPONSE', 31), 5000)], acmp,
                'GET_TX_CONNECTION, refused NOT_SUPPORTED'), 'measured', '')]
    return [(name, status(r)[0] == want and words in status(r)[1], str(status(r))) for name, r, want, words in cases]


def scenario_groups(h: ModuleType, elf: Path) -> list[tuple[str, list[scenario.Group]]]:
    """Every group with a response row, at one and two interfaces, in arm A and in the arm whose ports answer (the
    notice arms' groups end at no response)."""
    out = []
    for p in h.points(json.loads(h.ORACLE.read_text())):
        for variant in ('none', 'answering-ports'):
            build = dict(elf=str(elf), variant=variant)
            groups = [*scenario.acmp_groups(p), *scenario.aecp_groups(p, build), *scenario.aecp_fanout_groups(p, build),
                      *scenario.backlog_groups(p), *scenario.adp_groups(p), *scenario.maap_groups(p),
                      *scenario.srp_groups(p), *(scenario.fixture_groups(p) if p.interfaces == 1 else [])]
            out.append((f'{p.interfaces} interface(s), {variant}', groups))
    return out


def avb_info(groups: list[scenario.Group], variant: str) -> list[str]:
    """What is wrong with the aecp group's get_avb_info rows: each must send GET_AVB_INFO (0x0027) on AVB_INTERFACE
    0 with its four-byte command (IEEE 1722.1-2021 7.4.40.1), and state SUCCESS where the observation ports answer
    (answering-ports) and the face's refusal, named, where they do not."""
    want = 'SUCCESS' if variant == 'answering-ports' else 'ENTITY_MISBEHAVING'
    wrong, found = [], 0
    for g in groups:
        for pr in g.probes:
            if not pr.name.startswith('aecp.get_avb_info.'):
                continue
            found += 1
            frame = next(bytes.fromhex(s.split()[2]) for s in g.steps if s.startswith('frame ')
                         and s.endswith(' ' + pr.name))
            command, length = int.from_bytes(frame[36:38], 'big') & 0x7FFF, int.from_bytes(frame[16:18], 'big') & 0x7FF
            if (command, frame[38:42], length) != (0x0027, f.be(9, 2) + f.be(0, 2), 16):
                wrong.append(f'{pr.name}: command_type {command:04x}, {frame[38:42].hex()}, length {length}')
            if (pr.expect, pr.row) != (answers.aem(0x0027, want), answers.refused('get_avb_info', want)):
                wrong.append(f'{pr.name}: states {pr.expect} as "{pr.row}"')
    return wrong if found else ['no get_avb_info row']


def scenario_checks(h: ModuleType) -> list[Check]:
    """The real scenario's rows: each states its response, each refusal is named, the get_avb_info and talker rows."""
    unstated, rows, talker = [], [], {}
    with tempfile.TemporaryDirectory() as tmp:
        elf = h.image_header(Path(tmp))
        for label, groups in scenario_groups(h, elf):
            unstated += [f'{label}: {line}' for g in groups for line in run.unstated(g)]
            rows += [f'{label}: {line}' for line in avb_info(groups, label.split(', ')[1])]
            talker.update({pr.name.split('.')[1].upper(): pr.expect.split(':')[2] for g in groups for pr in g.probes
                           if g.name == 'acmp-cmd' and pr.name.split('.')[1].upper() in TALKER})
    bare = scenario.Probe('g.bare.if0', 'GET_RX_STATE', 'acmp', 'rxc:0', ['resp:0:41'])
    unnamed = scenario.Probe('g.unnamed.if0', 'unknown_command', 'aecp', 'rxc:0', ['resp:0:41'],
                             expect=answers.aem(0x3FF0, 'NOT_IMPLEMENTED'))
    nameless = scenario.Probe('g.nameless.if0', 'row', 'aecp', 'rxc:0', ['resp:0:41'], expect='aem:0027:DONE')
    named = answers.unstated([bare, unnamed, nameless])
    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / 'g.log'
        log.write_text(h.synthetic([]))
        spec = dict(sys_hz=h.SYS_HZ, cpu_hz=h.CPU_HZ, interfaces=1)
        refusals = run.graded([scenario.Group('g', probes=[bare])], [log], spec, Path(tmp))[1]
    return [
        ('every row of the scenario that ends at a response states its type and status, each refusal named',
         not unstated, '; '.join(unstated[:4])),
        ('the get_avb_info row sends GET_AVB_INFO on AVB_INTERFACE 0 at its length, SUCCESS where the ports answer',
         not rows, '; '.join(rows[:4])),
        ("the talker rows state the statuses Milan gives them, restated", talker == TALKER, str(talker)),
        ('a probe that ends at a response and states no type and status is named',
         any(line.startswith('g.bare.if0: ends at a response') for line in named), str(named)),
        ('a refusal its row does not name is named', any('g.unnamed.if0: states NOT_IMPLEMENTED' in line
                                                         for line in named), str(named)),
        ('a stated status that is no code of its kind is named', any('g.nameless.if0: the expectation' in line
                                                                    for line in named), str(named)),
        ('a run refuses a group whose row states no response, by name',
         any(r.startswith('g: g.bare.if0: ends at a response') for r in refusals), str(refusals))]


def answer_checks(h: ModuleType) -> list[Check]:
    """Every check of the rows' stated responses."""
    return [*response_checks(h), *scenario_checks(h)]
