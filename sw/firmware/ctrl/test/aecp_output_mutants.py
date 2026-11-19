# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_output_mutants.py - the AECP campaign's planted defects in a STREAM_OUTPUT's GET_STREAM_INFO as the split's
application bridge completes it (#943; Milan v1.2 5.4.2.10.2, Tables 5.8, 5.11 and 5.12): its Talker's MAAP address
and the Listener SRP registers for its stream. aecp_mutants.py plants each row; every named check must fail on its
own words, in AppOutputs.OutputInfoCarriesItsTalkersAddressAndItsListenersRegistration at two interfaces."""

APP = 'app/ctrl_app_aecp.c'
TEST = 'AppOutputs.OutputInfoCarriesItsTalkersAddressAndItsListenersRegistration'
DEST = '\t\tv->dest_mac = declaring && st.dest_mac_valid ? st.stream.dest_mac : 0u;\n'
LISTENING = '\t\tbool listening = declaring && i != NULL && i->listener_present[index];\n'
FAILED = '\t\tv->flags |= listening && !i->registered[index] ? 0x40u : 0u;\n'
EX = '\t\tv->flags_ex = listening ? 1u : 0u;\n'
GUARD = '\t\tif (index >= a->n_sources) return false;\n'
INTERFACE = '? &c->app->srp->ifs[a->source_interface[index]] : NULL;'

ROWS = (
    # the split before #943: the face's stream_dest_mac, 0, and no Listener read
    ('output-dest-mac-the-faces', APP, DEST, '',
     (TEST, "a declaring STREAM_OUTPUT's stream_dest_mac is its Talker's MAAP address")),
    ('output-listener-unread', APP, FAILED + EX, '\t\t(void)listening;\n',
     (TEST, 'REGISTERING while declaring and registering a matching Listener (Table 5.8)'),
     (TEST, 'REGISTERING_FAILED for a Listener Asking Failed alone (Table 5.11)')),
    ('output-dest-mac-undeclared', APP, DEST,
     '\t\tv->dest_mac = st.dest_mac_valid ? st.stream.dest_mac : 0u;\n',
     (TEST, "an undeclared STREAM_OUTPUT's stream_dest_mac is 0, as the fabric answers")),
    ('output-dest-mac-unallocated', APP, DEST,
     '\t\tv->dest_mac = declaring ? st.stream.dest_mac : 0u;\n',
     (TEST, 'no address MAAP does not hold')),
    # REGISTERING for Ready and Ready Failed alone, the ruling's parenthesis read as exclusive
    ('output-registering-ready-only', APP, LISTENING,
     '\t\tbool listening = declaring && i != NULL && i->registered[index];\n',
     (TEST, 'REGISTERING while declaring and registering a matching Listener (Table 5.8)')),
    ('output-registering-failed-any-listener', APP, FAILED,
     '\t\tv->flags |= listening ? 0x40u : 0u;\n',
     (TEST, 'REGISTERING_FAILED for a Listener Asking Failed alone (Table 5.11)')),
    ('output-registering-failed-without-a-listener', APP, FAILED,
     '\t\tv->flags |= declaring && (i == NULL || !i->registered[index]) ? 0x40u : 0u;\n',
     (TEST, 'the face\'s flags, and no REGISTERING_FAILED with no Listener')),
    ('output-registering-without-a-listener', APP, EX,
     '\t\tv->flags_ex = declaring ? 1u : 0u;\n',
     (TEST, 'no REGISTERING with no Listener'),
     (TEST, 'both clear once the Listener leaves')),
    ('output-registering-undeclared', APP, LISTENING,
     '\t\tbool listening = i != NULL && i->listener_present[index];\n',
     (TEST, 'both clear once the Talker withdraws')),
    # the descriptor's AVB interface, 0 at every shape, for the interface the output's Talker is declared on
    ('output-listener-on-the-descriptors-interface', APP, INTERFACE,
     '? &c->app->srp->ifs[interface] : NULL;',
     (TEST, 'REGISTERING while declaring and registering a matching Listener (Table 5.8)')),
    # another output's Listener: at two interfaces output 1 reads its interface's copy of output 0's, which is not
    # registered there, so REGISTERING fails; where outputs share an interface, 'no other output shows its Listener'
    ('output-listener-of-output-zero', APP, LISTENING,
     '\t\tbool listening = declaring && i != NULL && i->listener_present[0];\n',
     (TEST, 'REGISTERING while declaring and registering a matching Listener (Table 5.8)')),
    ('output-answered-past-acmps-sources', APP, GUARD,
     '\t\tif (index > a->n_sources) return false;\n',
     (TEST, 'an output ACMP holds no source for is not answered')),
    ('output-unanswered-without-srp', APP, GUARD,
     '\t\tif (index >= a->n_sources || c->app->srp == NULL) return false;\n',
     (TEST, 'without SRP, an output is still answered')),
    ('output-unanswered-past-srps-shape', APP, GUARD,
     '\t\tif (index >= a->n_sources || index >= CTRL_SRP_SOURCES) return false;\n',
     (TEST, "a source past SRP's shape is answered")),
)
