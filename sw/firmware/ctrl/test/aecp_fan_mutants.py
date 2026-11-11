# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_fan_mutants.py - the AECP campaign's planted defects in a notice's fan-out (#665, aecp.c's fan_out and address):
the notice built once, each recipient's frame addressed to it alone (its MAC, its interface's, its entity ID and its
own sequence_id), the used registrations walked by their mask from the recipient a stopped notice resumes at, the
one that asked left out, and a frame the fan port reports lost sent again to its recipient at the sequence_id it did
not have (IEEE 1722.1-2021 7.5.2; Milan v1.2 5.4.5.1). aecp_mutants.py appends this table to its own,
each row its defect()'s arguments: the name, the file in aecp/, the text, its replacement, and each test that must
refuse it with its words.
"""
from __future__ import annotations

CORE = 'Core.ANoticeIsAddressedToEachRecipientAlone'
FAN = 'Mailbox.ANoticeThroughTheFanPortIsAddressedToEachRecipientAlone'
ADDRESSED = "carries its recipient's MAC, its interface's, its entity ID and its own sequence"
COUNTED = 'the response, then one notice a recipient'
RESUMED = 'the notice stopped partway is sent whole once it resumes'
LOST = 'Core.ANoticeWhoseFrameWasLostSendsItToItsRecipientAgain'
ONCE = 'was lost is delivered once to each recipient, in order'
AGAIN = 'was lost carries its recipient\'s addresses and sequence'
#: The walk of an interface's used registrations.
SLOTS = 'for (unsigned slots = (unsigned)a->used[i] >> (k % AECP_REGISTRATIONS); slots != 0u;'

ROWS: tuple[tuple[str | tuple[str, str], ...], ...] = (
    ('notice-source-of-the-first-interface', 'aecp.c',
     'address(frame, r, a->cfg.mac[i]);',
     'address(frame, r, a->cfg.mac[0]);',
     (CORE, ADDRESSED),
     (FAN, "through the fan port carries its recipient's addresses and sequence")),
    ('notice-sequence-low-byte-unwritten', 'aecp.c',
     '\tf[35] = (uint8_t)r->sequence;\n',
     '',
     (CORE, ADDRESSED)),
    ('notice-controller-halves-swapped', 'aecp.c',
     'const uint32_t id_hi = (uint32_t)(r->controller >> 32), id_lo = (uint32_t)r->controller;',
     'const uint32_t id_lo = (uint32_t)(r->controller >> 32), id_hi = (uint32_t)r->controller;',
     (CORE, ADDRESSED)),
    ('notice-next-interface-skipped', 'aecp.c',
     '\t\t\tk = (i + 1u) * AECP_REGISTRATIONS;\n',
     '\t\t\tk = total;\n',
     (CORE, COUNTED),
     (FAN, COUNTED)),
    ('notice-resumed-walk-from-the-row-start', 'aecp.c',
     SLOTS,
     SLOTS.replace('>> (k % AECP_REGISTRATIONS)', '>> 0u'),
     (CORE, RESUMED)),
    ('notice-resumed-from-the-first-recipient', 'aecp.c',
     '\ta->recipient = k;\n',
     '\ta->recipient = owed ? 0u : k;\n',
     (CORE, RESUMED)),
    ('notice-to-a-freed-registration', 'aecp.c',
     'if ((slots & 1u) == 0u || r->controller == a->requester) {',
     'if (r->controller == a->requester) {',
     (CORE, COUNTED)),
    ('notice-to-the-one-that-asked', 'aecp.c',
     'if ((slots & 1u) == 0u || r->controller == a->requester) {',
     'if ((slots & 1u) == 0u) {',
     (CORE, COUNTED)),
    # a frame the fan port reports lost (#665): the walk resumes past it, as it did before the port reported one
    ('notice-lost-frame-skipped', 'aecp.c',
     '\t\t\t\tlost = taken == AECP_FAN_LOST;\n',
     '\t\t\t\tlost = false;\n',
     (LOST, ONCE)),
    ('notice-lost-frame-sequence-spent', 'aecp.c',
     '\t\t--held_r->sequence;\n',
     '\t\t(void)held_r;\n',
     (LOST, AGAIN)),
    ('notice-lost-last-frame-dropped', 'aecp.c',
     '\t\tlost = lost || end == AECP_FAN_LOST;\n',
     '',
     (LOST, ONCE)),
    ('notice-lost-frame-resumed-at-the-next', 'aecp.c',
     '\t\t\t\theld = k;\n',
     '\t\t\t\theld = k + 1u;\n',
     (LOST, ONCE)),
)
