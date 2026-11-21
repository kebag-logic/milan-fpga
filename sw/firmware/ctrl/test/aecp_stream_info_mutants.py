# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_stream_info_mutants.py - the AECP campaign's planted defects in SET_STREAM_INFO's response and accepted
bodies (IEEE 1722.1-2021 7.4.15; #665, #924). aecp_mutants.py plants each row, in its table where these stood;
every named check must fail on its own words."""

ROWS = (
    ('stream-info-request-echo', 'aecp_commands.c',
     'memcpy(out + 8, d->value + 74, 8u);',
     'memcpy(out + 8, in + 8, len >= 16u ? 8u : 0u);',
     ('Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal',
      'SET response uses current format')),
    ('stream-info-flags-echo', 'aecp_commands.c',
     'uint32_t flags = info.flags;',
     'uint32_t flags = (uint32_t)wire_be32(in + 4);',
     ('Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal',
      'SET response flags describe current state')),
    # the 48-octet IEEE 1722.1-2013 body is taken, and every other length short of the 2021 body refused (#924)
    ('stream-info-earlier-body-refused', 'aecp_commands.c',
     'if (set ? len != 48u && len < 84u : len < 4u) {',
     'if (len < (set ? 84u : 4u)) {',
     ('Core.SetStreamInfoTakesTheEarlierBodyOf48Octets', 'the 48-octet body is taken')),
    ('stream-info-short-bodies-taken', 'aecp_commands.c',
     'if (set ? len != 48u && len < 84u : len < 4u) {',
     'if (set ? len < 48u : len < 4u) {',
     ('Core.SetStreamInfoTakesTheEarlierBodyOf48Octets',
      'a body between 48 and 84 octets, or short of 48, is refused')),
    ('stream-info-noop-refused', 'aecp_commands.c',
     '(requested & 0xdaf80000u) != 0u',
     'requested != 0x20000000u',
     ('Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal',
      'status for command')),
)
