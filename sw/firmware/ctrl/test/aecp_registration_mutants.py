# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_registration_mutants.py - the AECP campaign's planted defects in a STREAM_OUTPUT's notice of a Listener
registration change (#957; Milan v1.2 5.4.5.2, Table 5.22; IEEE 1722.1-2021 7.5.2): SRP's record of a change of the
Listener declaration it indicates for the source's stream, while the source's DA gate is open on the interface, in the
record a Talker declaration's change is (srp_mbx.c, listener; #936), and the reset's clear of it with the
registrations it destroys. aecp_mutants.py plants each row; every named check must fail on its own words, in
AppOutputs.ListenerRegistrationChangeIsItsStreamOutputsNotice or, across a link reset,
AppOutputs.ListenerRegistrationAfterALinkResetIsItsStreamOutputsNotice (real MSRP Listener MRPDUs, the notices read on
the wire) at two interfaces."""

SRP = 'srp/srp_mbx.c'
NOTICE = 'AppOutputs.ListenerRegistrationChangeIsItsStreamOutputsNotice'
RESET = 'AppOutputs.ListenerRegistrationAfterALinkResetIsItsStreamOutputsNotice'
#: SRP's record of a change of the Listener declaration it indicates (#957), as srp_mbx.c holds it.
RECORDED = '            i->noticed |= (uint32_t)(i->declaration[n] != declaration) << n & i->gate;\n'
#: the reset's clear of the declaration a registration it destroys held (#957), as srp_mbx.c holds it.
FORGOTTEN = '        i->declaration[k] = 0u;\n'

ROWS = (
    # the split before #957: a Listener registration change raises no notice
    ('registration-notice-unrecorded', SRP, RECORDED, '',
     (NOTICE, 'a Listener registration change is one notice of its STREAM_OUTPUT to every registered controller')),
    # the gate not read: a Listener on another interface, whose gate is closed for the source, notifies the output
    ('registration-notice-ungated', SRP, RECORDED, RECORDED.replace(' & i->gate;', ';'),
     (NOTICE, 'a Listener on another interface notifies nothing')),
    # every indication recorded: a Listener declared New again unchanged notifies the output
    ('registration-notice-unchanged-recorded', SRP, RECORDED,
     RECORDED.replace('(uint32_t)(i->declaration[n] != declaration) << n', '1u << n'),
     (NOTICE, 'a Listener declared New again unchanged notifies nothing')),
    # the split before the correction: the destroyed registration's declaration kept across a link reset, so the
    # Listener's return with the same declaration notifies nothing
    ('registration-notice-kept-across-a-reset', SRP, FORGOTTEN, '',
     (RESET, "a Listener's return after a link reset is one notice of its STREAM_OUTPUT to every registered "
             "controller")),
)
