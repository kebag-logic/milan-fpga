# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Synthetic trace and response constructors for the service grader controls."""
from __future__ import annotations

import grade
import scenario

def synthetic(lines: list[str]) -> str:
    """A minimal log in the testbench's line format, completed."""
    return '\n'.join([*lines, 'SUMMARY passes=1', 'RESULT: PASS']) + '\n'


def tx_record(ch: int, interface: int, frame: bytes, at: int, cycle: int) -> list[str]:
    """The ring writes of one TX record at word index at, then its TX_HEAD commit."""
    base, words = grade.TX_RING[ch]
    data = [len(frame) | interface << 16 | 2 << 28, 0]
    padded = frame + bytes(-len(frame) % 4)
    data += [int.from_bytes(padded[k:k + 4], 'little') for k in range(0, len(padded), 4)]
    writes = ' '.join(f'{cycle - len(data) - 1 + n}:{base + (at + n) % words:x}:{v:x}' for n, v in enumerate(data))
    head = at + len(data)
    return [f'PASS 1 {cycle - 100} {(cycle - 100) // 2} 50 instr=10 load_mbx=3 store_mbx={len(data) + 1} '
            f'W {writes} {cycle}:{scenario.ch_word(ch, "TX_HEAD"):x}:{head:x}', f'TXC {cycle} {ch} {head}']


def tx_sequence(ch: int, records: list[tuple[int, bytes, int]]) -> list[str]:
    """Consecutive TX records of one channel: (interface, frame, commit cycle) each."""
    lines, at = [], 0
    for interface, frame, cycle in records:
        lines += tx_record(ch, interface, frame, at, cycle)
        at += 2 + (len(frame) + 3) // 4
    return lines


def acmp_response(sequence: int, message: str = 'GET_RX_STATE_RESPONSE', status: int = 0) -> bytes:
    """An ACMP response frame with that sequence_id."""
    return scenario.f.acmp(scenario.f.ACMP[message], 0x020000000001,
                           scenario.f.Acmp(sequence=sequence, status=status))


def aem_response(controller: int, sequence: int, command: int = 0x0010, unsolicited: bool = False,
                 descriptor: tuple[int, int] = (0, 0)) -> bytes:
    """An AEM_RESPONSE (9.2.1.2) to controller; unsolicited sets the u bit (7.5.2)."""
    payload = scenario.f.be(descriptor[0], 2) + scenario.f.be(descriptor[1], 2) + bytes(4)
    frame = bytearray(scenario.f.aem_command(scenario.f.Aem(1, controller, 2, 3, sequence), command, payload))
    frame[15] = 1
    if unsolicited:
        frame[36] |= 0x80
    return bytes(frame)


def received(ch: int, tag: str, at: int = 1100) -> list[str]:
    """A 70-byte frame tagged tag whose receive commit lands 4 cycles after its last byte."""
    return [f'RXS {at} 0 70 {tag}', f'RXE {at + 69}', f'RXC {at + 73} {ch}']
