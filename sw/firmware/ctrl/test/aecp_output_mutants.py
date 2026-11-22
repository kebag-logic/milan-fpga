# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_output_mutants.py - the AECP campaign's planted defects in a STREAM_OUTPUT's GET_STREAM_INFO as the split's
application bridge completes it (#943; Milan v1.2 5.4.2.10.2, Tables 5.8, 5.11 and 5.12): its Talker's MAAP address
and the Listener SRP registers for its stream, for a whole observation of an output the face reports declaring, and
a map edit's check of its output stream observed briefly. aecp_mutants.py plants each row; every named check must fail
on its own words, in AppOutputs.OutputInfoCarriesItsTalkersAddressAndItsListenersRegistration (and, for the map edit's
running check, Core.TheRunningCheckObservesEveryStreamBriefly) at two interfaces."""

APP = 'app/ctrl_app_aecp.c'
TEST = 'AppOutputs.OutputInfoCarriesItsTalkersAddressAndItsListenersRegistration'
GATE = '\t} else if (!v->brief && (v->flags & 0x10000000u) != 0u) {\n'
DEST = '\tv->dest_mac = st.dest_mac_valid ? st.stream.dest_mac : 0u;\n'
LISTENING = '\tbool listening = i != NULL && i->listener_present[index];\n'
FAILED = '\tv->flags |= listening && !i->registered[index] ? 0x40u : 0u;\n'
EX = '\tv->flags_ex = listening ? 1u : 0u;\n'
GUARD = '\tif (index >= a->n_sources) return false;\n'
INTERFACE = '? &c->app->srp->ifs[a->source_interface[index]] : NULL;'

ROWS = (
    # the split before #943: the face's stream_dest_mac, 0, and no Listener read
    ('output-dest-mac-the-faces', APP, DEST, '',
     (TEST, "a declaring STREAM_OUTPUT's stream_dest_mac is its Talker's MAAP address")),
    ('output-listener-unread', APP, FAILED + EX, '\t(void)listening;\n',
     (TEST, 'REGISTERING while declaring and registering a matching Listener (Table 5.8)'),
     (TEST, 'REGISTERING_FAILED for a Listener Asking Failed alone (Table 5.11)')),
    # an output the face reports undeclared completed too: its address and its Listener's flags while it declares none
    ('output-completed-undeclared', APP, GATE, '\t} else if (!v->brief) {\n',
     (TEST, "an undeclared STREAM_OUTPUT's stream_dest_mac is 0, as the fabric answers"),
     (TEST, 'both clear once the Talker withdraws')),
    # a brief observation, a running check's, completed as a whole one: the work a map edit's or SET_CONFIGURATION's
    # check of every output would pay, which none of them reads
    ('output-brief-completed', APP, GATE, '\t} else if ((v->flags & 0x10000000u) != 0u) {\n',
     (TEST, "a brief observation of an output, a running check's, is the face's: bound and running alone")),
    ('output-dest-mac-unallocated', APP, DEST, '\tv->dest_mac = st.stream.dest_mac;\n',
     (TEST, 'no address MAAP does not hold')),
    # REGISTERING for Ready and Ready Failed alone, the ruling's parenthesis read as exclusive
    ('output-registering-ready-only', APP, LISTENING, '\tbool listening = i != NULL && i->registered[index];\n',
     (TEST, 'REGISTERING while declaring and registering a matching Listener (Table 5.8)')),
    ('output-registering-failed-any-listener', APP, FAILED, '\tv->flags |= listening ? 0x40u : 0u;\n',
     (TEST, 'REGISTERING_FAILED for a Listener Asking Failed alone (Table 5.11)')),
    # the STREAM_INPUT's failure constant copied: MSRP_FAILURE_VALID beside REGISTERING_FAILED, so a controller reads
    # the zero failure code and bridge ID as a Talker Failed's (Table 5.11)
    ('output-registering-failed-msrp-failure-valid', APP, FAILED,
     '\tv->flags |= listening && !i->registered[index] ? 0x08000040u : 0u;\n',
     (TEST, 'never MSRP_FAILURE_VALID')),
    ('output-registering-failed-without-a-listener', APP, FAILED,
     '\tv->flags |= i == NULL || !i->registered[index] ? 0x40u : 0u;\n',
     (TEST, 'the face\'s flags, and no REGISTERING_FAILED with no Listener')),
    ('output-registering-without-a-listener', APP, EX, '\tv->flags_ex = 1u;\n',
     (TEST, 'no REGISTERING with no Listener'),
     (TEST, 'both clear once the Listener leaves')),
    # interface 0, as the descriptor's AVB interface is at every shape, for the one the output's Talker is declared on:
    # at two interfaces output 1 reads interface 0's copy, where its stream's Listener on the other interface is
    # registered (one interface is the output's own, the same defect's equivalent)
    ('output-listener-on-interface-zero', APP, INTERFACE, '? &c->app->srp->ifs[0] : NULL;',
     (TEST, "another interface's Listener is not its own")),
    # another output's Listener: output 0's, which every other output then shows
    ('output-listener-of-output-zero', APP, LISTENING, '\tbool listening = i != NULL && i->listener_present[0];\n',
     (TEST, 'no other output shows its Listener')),
    # either interface's copy of its stream's Listener, not its own interface's: at two interfaces a Listener
    # registered on the other one raises both flags (one interface is the output's own, the defect's equivalent)
    ('output-listener-any-interface', APP, LISTENING,
     '\tbool listening = i != NULL && (c->app->srp->ifs[0].listener_present[index] ||\n'
     '\t\tc->app->srp->ifs[MBX_N_IF - 1u].listener_present[index]);\n',
     (TEST, "another interface's Listener is not its own")),
    ('output-answered-past-acmps-sources', APP, GUARD, '\tif (index > a->n_sources) return false;\n',
     (TEST, 'an output ACMP holds no source for is not answered')),
    ('output-unanswered-without-srp', APP, GUARD,
     '\tif (index >= a->n_sources || c->app->srp == NULL) return false;\n',
     (TEST, 'without SRP, an output is still answered')),
    ('output-unanswered-past-srps-shape', APP, GUARD,
     '\tif (index >= a->n_sources || index >= CTRL_SRP_SOURCES) return false;\n',
     (TEST, "a source past SRP's shape is answered")),
    # an output map edit's check of its stream read whole again, as before #943 (aecp_maps.c, idle)
    ('map-idle-reads-whole', 'aecp_maps.c', '\treturn aecp_running(a, 6u, r->stream) == AECP_SUCCESS;\n',
     '\tstruct aecp_stream_info info = {.brief = false};\n'
     '\treturn aecp_stream_read(a, 6u, r->stream, &info) && !info.running;\n',
     ('Core.TheRunningCheckObservesEveryStreamBriefly', "an output map edit's running check is brief")),
)
