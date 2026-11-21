# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_registration_mutants.py - the AECP campaign's planted defects in a STREAM_OUTPUT's notice of a Listener
registration change (#957; Milan v1.2 5.4.5.2, Table 5.22; IEEE 1722.1-2021 7.5.2): the SRP delivery's take of SRP's
record into the application's, of each source on its own interface only, its record cleared and the pass that takes it
owing output (ctrl_app_srp.c). aecp_mutants.py plants each row; every named check must fail on its own words, in
AppOutputs.ListenerRegistrationChangeIsItsStreamOutputsNotice (real MSRP Listener MRPDUs, the notices read on the wire)
and App.NoPassIsIdleWhileAListenerRegistrationNoticeIsOwed, at two interfaces."""

APP = 'app/ctrl_app_srp.c'
NOTICE = 'AppOutputs.ListenerRegistrationChangeIsItsStreamOutputsNotice'
IDLE = 'App.NoPassIsIdleWhileAListenerRegistrationNoticeIsOwed'
#: the SRP delivery's take of each interface's record (#957), as ctrl_app_srp.c holds it.
READ = '        uint32_t changed = app->srp->ifs[interface].registration_noticed;\n'
CLEAR = '        app->srp->ifs[interface].registration_noticed = 0u;\n'
OWN = '            if ((changed & 1u) != 0u && app->acmp.acmp.cfg.source_interface[source] == interface) {\n'
OWED = '                app->srp_noticed |= 1u << source;\n                noticed = true;\n'

ROWS = (
    # the split before #957: SRP's record of a Listener registration change never reaches AECP
    ('registration-notice-not-taken', APP, READ, '        uint32_t changed = 0u;\n',
     (NOTICE, 'a Listener registration change is one notice of its STREAM_OUTPUT to every registered controller'),
     (IDLE, "no pass is idle while a Listener registration's notice is owed")),
    # a Listener on any interface notifies the output, whose GET_STREAM_INFO reads its own interface's alone
    ('registration-notice-any-interface', APP, OWN, '            if ((changed & 1u) != 0u) {\n',
     (NOTICE, 'a Listener on another interface notifies nothing'),
     (IDLE, "a record on another interface than its source's notifies nothing")),
    # the record never cleared: every pass notifies the output again
    ('registration-notice-record-kept', APP, CLEAR, '',
     (NOTICE, 'a Listener registration change is one notice of its STREAM_OUTPUT to every registered controller')),
    # the pass that takes the record reports no output owed, so the loop may sleep before the notice leaves
    ('registration-notice-owed-unreported', APP, OWED, '                app->srp_noticed |= 1u << source;\n',
     (IDLE, "no pass is idle while a Listener registration's notice is owed")),
)
