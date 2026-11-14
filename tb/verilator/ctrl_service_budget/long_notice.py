# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The largest legal notice's cost (#894): a group that sends a 550 B notice to 15 controllers at 1x1/1if, whose
measured cost plus 5 % is the cost the tier model charges an AECP poll's owed frames where every notice is the largest
legal one (rows_tiers.LONG_NOTICE_US, read from poll_grade.STATED_US's aecp_long).

AECP_REGISTRATIONS controllers register on each interface, others on each, so a notice goes to every registration but
its requester's (aecp.c, fan_out: no requester receives its own): 15 at one interface, 31 at two. The requester, the
first registered on interface 0, sends REMOVE_AUDIO_MAPPINGS and then ADD_AUDIO_MAPPINGS of MAPPINGS mappings, a
map's last default row repeated (scenario.map_edit): the input map's, or where it can never change (capacity 0, as at
8x8) the output map's with the answering-ports arm, as aecp_fanout_groups edits it. The map is a set, so the first
removes that row and the second adds it back, and each response echoes every mapping (aecp_maps.c). That is a
control_data_length of 524, the most IEEE 1722.1-2021 9.2.2.6 allows, so the response and every notice is a 550 B AECPDU
(tier1_rows.LONG_NOTICE_BYTES), longer than AECP_FAN_BYTES, which fan_out sends a recipient at a time. Each command is
a probe of the notification family, from its receive commit to its last recipient's commit, and every AECP poll item
that commits such a notice is held to its own stated cost (poll_grade.py, aecp_long). A run in which this group
measured no such item is refused (missing), since the cost it states would then rest on nothing.

Then the maximum-length edits the port refuses (refused_edits; #894's egress ruling of 2026-11-13, item 3: an edit's
work is bounded refused or not, aecp_maps.c): two collisions, REMOVEs of MAPPINGS mappings of the row's key, one
over distinct indices of the value's first field, which the port's geometry refuses at its first illegal index, and
one over the key's legal values in turn, the row's own among them; and a conflict, an ADD of the row MAPPINGS - 1
times and then its key with another legal value, refused at its last turn.
Each is answered BAD_ARGUMENTS with every mapping echoed, a 550 B response probe of its own, and the group's record
handler costs (aecp_mbx.c, frame) include theirs, which the largest legal command's stated record must hold
(rows_tiers.LONG_RECORD_US).
"""
from __future__ import annotations

import answers
import frames as f
import scenario
from tier1_rows import LONG_NOTICE_BYTES

#: The group's name.
NAME = 'aecp-largest-notice'
#: The bytes of an AEM_RESPONSE to ADD/REMOVE_AUDIO_MAPPINGS before its mappings: the Ethernet header's 14, the AVTP
#: control header's 4, target_entity_id 8, controller_entity_id, sequence_id and command_type 12, and the descriptor,
#: count and reserved field 8 (IEEE 1722.1-2021 7.4.45.1 and 7.4.46.1).
FIXED_BYTES = 46
#: The mappings that make the largest legal notice, each 8 bytes: 63.
MAPPINGS = (LONG_NOTICE_BYTES - FIXED_BYTES) // 8
#: The first sequence_id the group uses.
SEQ = 0x5400
#: The refused edits' names, each its command_type.
REFUSED = {'collision_indices': 0x002D, 'collision_values': 0x002D, 'conflict_last': 0x002C}


def legal_values(build: dict, port: int, row: tuple[int, ...]) -> list[tuple[int, int]]:
    """The values the image's geometry makes legal for the key of `row` (stream, channel, cluster, cluster channel) at
    the STREAM_PORT 0 of that type, the row's own first (aecp_maps.c, legal): at an input port, whose key is a cluster
    channel, each audio STREAM_INPUT's channels; at an output port, whose key is a stream channel, each of the port's
    clusters' channels."""
    def be(value: bytes, at: int) -> int:
        """The big-endian 16-bit field of a descriptor's value at that offset."""
        return int.from_bytes(value[at:at + 2], 'big')
    out = []
    if port == 14:
        for index in range(256):
            try:
                fmt = int.from_bytes(scenario.descriptor_value(build, 5, index)[74:82], 'big')
            except KeyError:
                break
            out += [(index, ch) for ch in range((fmt >> 22) & 1023 if fmt >> 56 == 2 else 0)]
    else:
        value = scenario.descriptor_value(build, port, 0)
        for k in range(be(value, 12)):
            out += [(k, ch) for ch in range(be(scenario.descriptor_value(build, 20, be(value, 14) + k), 84))]
    own = (row[0], row[1]) if port == 14 else (row[2], row[3])
    return [own] + [v for v in out if v != own]


def refused_edits(build: dict, port: int, edit: bytes) -> dict[str, bytes]:
    """The maximum-length edits the port refuses BAD_ARGUMENTS, by name (REFUSED), each a payload of MAPPINGS
    mappings of the map's last default row's key, as the module docstring says; the conflict only where the key has a
    second legal value."""
    row = tuple(int.from_bytes(edit[8 + 2 * k:10 + 2 * k], 'big') for k in range(4))
    values = legal_values(build, port, row)

    def payload(mappings: list[tuple[int, ...]]) -> bytes:
        """The edit's descriptor, count and reserved field, then those mappings."""
        return edit[:8] + b''.join(b''.join(f.be(v, 2) for v in m) for m in mappings)

    def keyed(value: tuple[int, int]) -> tuple[int, ...]:
        """The row's key with that value: its cluster channel at an input port, its stream channel at an output."""
        return (*value, *row[2:]) if port == 14 else (*row[:2], *value)
    out = {'collision_indices': payload([keyed((n, row[1] if port == 14 else row[3])) for n in range(MAPPINGS)]),
           'collision_values': payload([keyed(values[n % len(values)]) for n in range(MAPPINGS)])}
    if len(values) > 1:
        out['conflict_last'] = payload([row] * (MAPPINGS - 1) + [keyed(values[1])])
    return out


def groups(p: scenario.Point, build: dict) -> list[scenario.Group]:
    """The largest legal notice from a registered requester to every other registration, removed then added back."""
    answering = build.get('variant') == 'answering-ports'
    port, edit = next(((t, e) for t, e in ((14, scenario.map_edit(build, 14, MAPPINGS)),
                                           (15, scenario.map_edit(build, 15, MAPPINGS) if answering else None)) if e),
                      (0, None))
    if edit is None:
        return []
    aecp, ms = scenario.CH['aecp'], scenario.MS
    g = scenario.Group(NAME, sim_ms=1500)
    scenario.ready(g, p)
    controllers = {i: [scenario.FANOUT_CONTROLLER + scenario.registrations() * i + n
                       for n in range(scenario.registrations())] for i in range(p.interfaces)}
    seq = SEQ
    for i, ids in controllers.items():
        for ctl in ids:
            frame = f.aem_command(f.Aem(p.entity_id, ctl, scenario.CTL_MAC, p.mac, seq), 0x0024, bytes(4))
            g.add(f'frame {i} {frame.hex()}', f'wait tx {aecp} 1 within {50 * ms}', 'wait quiet 3 within 2000000')
            seq += 1
    requester = controllers[0][0]
    others = tuple((ctl, i) for i, ids in controllers.items() for ctl in ids if ctl != requester)
    for name, command_type in (('remove_audio_mappings', 0x002D), ('add_audio_mappings', 0x002C)):
        frame = f.aem_command(f.Aem(p.entity_id, requester, scenario.CTL_MAC, p.mac, seq), command_type, edit)
        assert len(frame) == LONG_NOTICE_BYTES, len(frame)
        ends = [f'resp:{aecp}:{seq:x}', f'notify:{aecp}:{command_type:04x}:{port}:0']
        row = f'{name.upper()} of {MAPPINGS} ({LONG_NOTICE_BYTES} B notice)'
        g.probe(scenario.Probe(f'aecp_long.{name}.if0', row, 'notify', f'rxc:{aecp}', ends,
                               expect=answers.aem(command_type), recipients=others),
                f'frame 0 {frame.hex()}', wait=f'tx {aecp} {1 + len(others)} within {200 * ms}')
        seq += 1
    for name, payload in refused_edits(build, port, edit).items():
        frame = f.aem_command(f.Aem(p.entity_id, requester, scenario.CTL_MAC, p.mac, seq), REFUSED[name], payload)
        assert len(frame) == LONG_NOTICE_BYTES, len(frame)
        g.probe(scenario.Probe(f'aecp_long.refused.{name}.if0', f'{name.upper()} of {MAPPINGS}, refused BAD_ARGUMENTS',
                               'aecp', f'rxc:{aecp}', [f'resp:{aecp}:{seq:x}'],
                               expect=answers.aem(REFUSED[name], 'BAD_ARGUMENTS')),
                f'frame 0 {frame.hex()}', wait=f'tx {aecp} 1 within {200 * ms}')
        seq += 1
    return [scenario.paced(g, aecp)]


def missing(results: list[dict]) -> list[str]:
    """This group, where it ran, with no aecp_long item measured (poll_grade.held's long list)."""
    return [f'{g["group"]}: no AECP poll item committed a notice longer than AECP_FAN_BYTES, so the largest legal '
            'notice was not measured' for g in results
            if g.get('group') == NAME and not g.get('passes', {}).get('polls', {}).get('long')]
