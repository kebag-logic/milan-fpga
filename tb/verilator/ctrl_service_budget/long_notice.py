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
#: count and reserved field 8 (IEEE 1722.1-2021 7.4.44.1).
FIXED_BYTES = 46
#: The mappings that make the largest legal notice, each 8 bytes: 63.
MAPPINGS = (LONG_NOTICE_BYTES - FIXED_BYTES) // 8
#: The first sequence_id the group uses.
SEQ = 0x5400


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
    return [scenario.paced(g, aecp)]


def missing(results: list[dict]) -> list[str]:
    """This group, where it ran, with no aecp_long item measured (poll_grade.held's long list)."""
    return [f'{g["group"]}: no AECP poll item committed a notice longer than AECP_FAN_BYTES, so the largest legal '
            'notice was not measured' for g in results
            if g.get('group') == NAME and not g.get('passes', {}).get('polls', {}).get('long')]
