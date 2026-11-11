# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""What a row's response must be (#882): its command or message type and its status, each stated by the scenario.

A probe that ends at a response (resp:<ch>:<seq>) states the response it measures as one of
  aem:<command_type>:<status>   an AEM_RESPONSE (IEEE 1722.1-2021 9.2.1.2) to that command_type, in hex
  mvu:<command_type>:<status>   a Milan MVU response (Milan v1.2 5.4.3.1) to that command_type, in hex
  acmp:<message_type>:<status>  an ACMP response of that message_type (IEEE 1722.1-2021 Table 8-1)
its status a name of IEEE 1722.1-2021 Table 7-141 (AEM and MVU) or of Table 8-3 (ACMP). The grader reads the
probe's own response, the one that answers its sequence_id, and a type or a status other than the stated one is an
unexpected response, which fails the run. A row that states a status other than SUCCESS measures a refusal, and its
row names it ("<row>, refused <status>"), so a refusal is never reported as the path it refuses: the get_avb_info
row once timed GET_AS_PATH on a missing interface, a NO_SUCH_DESCRIPTOR, as GET_AVB_INFO (#882). A run refuses a
group with a probe that ends at a response and states no type and status, or states a refusal its row does not name.
"""
from __future__ import annotations

import frames as f

#: The expectation kinds that state a response's type and status.
KINDS = ('aem', 'mvu', 'acmp')


def aem(command_type: int, status: str = 'SUCCESS') -> str:
    """The expectation of an AEM_RESPONSE to that command_type with that status."""
    return f'aem:{command_type:04x}:{status}'


def mvu(command_type: int, status: str = 'SUCCESS') -> str:
    """The expectation of a Milan MVU response to that command_type with that status."""
    return f'mvu:{command_type:04x}:{status}'


def acmp(message: str, status: str = 'SUCCESS') -> str:
    """The expectation of an ACMP response of that message type (a name of frames.ACMP) with that status."""
    return f'acmp:{message}:{status}'


def refused(row: str, status: str) -> str:
    """A row's label: a row that measures a refusal names it."""
    return row if status == 'SUCCESS' else f'{row}, refused {status}'


def codes(kind: str) -> dict[str, int]:
    """The status codes of an expectation kind."""
    return f.ACMP_STATUS if kind == 'acmp' else f.AEM_STATUS


def unstated(probes: list) -> list[str]:
    """Each probe that ends at a response and states no type and status, each whose stated status is no code of its
    kind, and each that states a refusal its row does not name."""
    out = []
    for pr in probes:
        kind, *args = pr.expect.split(':')
        if kind in KINDS:
            if len(args) != 2 or args[1] not in codes(kind):
                out.append(f'{pr.name}: the expectation {pr.expect} names no status of {kind}')
            elif args[1] != 'SUCCESS' and f'refused {args[1]}' not in pr.row:
                out.append(f'{pr.name}: states {args[1]}, and its row "{pr.row}" does not name the refusal')
        elif any(e.startswith('resp:') for e in pr.ends):
            out.append(f'{pr.name}: ends at a response and states no type and status')
    return out


def answered(frame: bytes, kind: str) -> tuple[int, int] | None:
    """A response frame's command or message type and its status, if it is a response of that kind: AEM's
    command_type at byte 36 and MVU's at byte 42 (after its protocol_identifier), with the u bit cleared."""
    if kind == 'acmp':
        return (frame[15] & 0xF, frame[16] >> 3) if len(frame) > 16 and frame[14] == 0xFC else None
    message, at = (1, 36) if kind == 'aem' else (7, 42)
    if len(frame) < at + 2 or frame[14] != 0xFB or frame[15] & 0xF != message:
        return None
    return int.from_bytes(frame[at:at + 2], 'big') & 0x7FFF, frame[16] >> 3


def differs(kind: str, got: tuple[int, int], want: tuple[int, int]) -> str:
    """'' when the response's type and status are the stated ones; else what it answered."""
    if got[0] != want[0]:
        types = {v: n for n, v in f.ACMP.items()} if kind == 'acmp' else {}
        return f'answered as {types.get(got[0], f"{got[0]:04x}")}, not as {types.get(want[0], f"{want[0]:04x}")}'
    if got[1] != want[1]:
        names = {v: n for n, v in codes(kind).items()}
        return f'status {names.get(got[1], got[1])}, not the stated {names.get(want[1], want[1])}'
    return ''


def check(expect: str, own: bytes | None) -> str:
    """'' when the probe's own response is the one its expectation states; else what is wrong."""
    kind, of, status = expect.split(':')
    if status not in codes(kind):
        return f'the expectation {expect} names no status of {kind}'
    if own is None:
        return f'no response answers its sequence_id ({kind})'
    got = answered(own, kind)
    if got is None:
        return f'its response is no {kind} response'
    return differs(kind, got, (f.ACMP[of] if kind == 'acmp' else int(of, 16), codes(kind)[status]))


#: GET_AVB_INFO (IEEE 1722.1-2021 7.4.40; Milan v1.2 5.4.2.23) on AVB_INTERFACE 0: its command_type 0x0027 and its
#: command, descriptor_type and descriptor_index (7.4.40.1), four bytes (#882).
AVB_INFO = (0x0027, f.be(9, 2) + f.be(0, 2))
#: The aecp group's unknown command: a reserved command_type (IEEE 1722.1-2021 Table 7-126) under 0x4000, since
#: aecp.c keeps the field's low 14 bits and so answers a command at or above 0x4000 under another command_type
#: (#891, whose fix sends 0x7FF0 again).
UNKNOWN = 0x3FF0
#: The talker commands the acmp-cmd group sends a source, each with the status it is answered with: the source has
#: no stream destination yet, so PROBE_TX is refused TALKER_DEST_MAC_FAIL (Milan v1.2 Tables 5.42 and 5.43), and
#: GET_TX_CONNECTION is NOT_SUPPORTED (Milan v1.2 5.5.4.4, Table 5.48).
TALKER = (('PROBE_TX', 'TALKER_DEST_MAC_FAIL'), ('GET_TX_STATE', 'SUCCESS'), ('DISCONNECT_TX', 'SUCCESS'),
          ('GET_TX_CONNECTION', 'NOT_SUPPORTED'))


def aecp_statuses(build: dict) -> dict[str, str]:
    """The aecp group's rows that are not answered SUCCESS, by row: the unknown command NOT_IMPLEMENTED; GET_AVB_INFO
    and GET_COUNTERS, whose values the face reads through a window (aecp_face.c), SUCCESS only where the arm's
    observation ports answer (answering-ports); on the image as linked the harness's datapath leaves the window
    unanswered, so each is refused ENTITY_MISBEHAVING once the window read's bound has passed."""
    face = 'SUCCESS' if build.get('variant') == 'answering-ports' else 'ENTITY_MISBEHAVING'
    return dict(get_avb_info=face, get_counters=face, unknown_command='NOT_IMPLEMENTED')
