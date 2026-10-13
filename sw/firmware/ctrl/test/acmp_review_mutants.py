# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""acmp_review_mutants.py - lane F3's round-2 planted defects (#665, issue
comment 6030067436): one or more for each finding of the R531-1 and R530-1
reviews and for the adp channel's bound-talker term (comment 6029368753),
on the core, the adapter, the binding owner, the driver and the host model;
round 4's (comment 6034423349) for R531-2-F1; round 6's (comment
6037650104) for the app composing ADP, ACMP and lane F2's MAAP together;
and round 7's (comment 6041160063) for R530-5-F1 and S1. acmp_mutants.py
appends this table to its own.
"""

from __future__ import annotations

from ctrl_mutant import ACMP_C, ACMP_H, Mutant

APP = "app/ctrl_app.c"
#: ctrl_app_open from its first line to ADP's enable: what lies between the
#: compose's MAAP step and the open's MAAP start.
APP_OPEN = ("\n\nbool ctrl_app_open(struct ctrl_app *app, const struct ctrl_app_config *cfg)\n{\n"
            "\t// ADP sends the entity's one MAC on every interface (adp.c), so it is\n"
            "\t// every interface's own unicast address\n"
            "\tuint64_t own_mac[MBX_N_IF];\n"
            "\tfor (unsigned i = 0; i < MBX_N_IF; ++i) {\n\t\town_mac[i] = cfg->entity->mac;\n\t}\n"
            "\tif (!ctrl_loop_open(&app->loop, cfg->entity->entity_id, own_mac)) {\n\t\treturn false;\n\t}\n"
            "\t// the bindings the store restored between compose and open, into the\n"
            "\t// adp channel's bound-talker table, before any protocol starts\n"
            "\tif (cfg->acmp != NULL) {\n\t\tacmp_mbx_open(&app->acmp);\n\t}\n"
            "\tadp_mbx_set_enable(&app->adp, true);\n"
            "\t// MAAP reads each interface's link and begins once the channels are open\n"
            "\t// (maap_mbx.h); compose refused a preferred range it would refuse\n"
            "\tif (cfg->maap_allocation != NULL) {\n")
#: The compose's ACMP step and its MAAP step, in that order.
APP_ACMP_THEN_MAAP = ("\tif (cfg->acmp != NULL &&\n"
                      "\t    (!acmp_mbx_init(&app->acmp, cfg->acmp, cfg->acmp_env, CTRL_APP_ACMP_FIRST_SLOT) ||\n"
                      "\t     !acmp_mbx_attach(&app->acmp, &app->loop))) {\n\t\treturn false;\n\t}\n"
                      "\treturn cfg->maap_allocation == NULL || maap_compose(app, cfg);\n")
MAAP_INIT = ("\treturn maap_mbx_init(&app->maap, mac, count, CTRL_APP_MAAP_FIRST_SLOT, cfg->maap_allocation, "
             "cfg->maap_ctx) &&\n\t       maap_mbx_attach(&app->maap, &app->loop);\n")
U6 = "AcmpMailbox.U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen"
U7 = "AcmpMailbox.U7TheThreeWayCompositionRefusesWithNothingOpened"
F6 = "AcmpMailbox.F6WithMaapComposedEveryPassStaysWithinTheThreeWayBound"
EXPLICIT = "MaapHost.ExplicitAppComposition"

MUTANTS = (
    # R531-1-F1: only AVTP version 0 is read, in both receive paths, before anything changes
    Mutant("acmp-version-unchecked", ACMP_C,
           "\t    frame[PDU] != ACMP_SUBTYPE || AVTP_VERSION(frame) != ACMP_AVTP_VERSION) {",
           "\t    frame[PDU] != ACMP_SUBTYPE) {",
           "acmp", "AcmpCore.A26AnotherAvtpVersionIsDiscardedBeforeItIsRead", "A26 a BIND_RX of AVTP version 1",
           (("acmp", "AcmpMailbox.B9AnotherAvtpVersionPassesTheFilterAndChangesNothing", "B9 the core discards it"),)),
    Mutant("acmp-adp-version-unchecked", ACMP_C,
           "\t    frame[PDU] != ACMP_ADP_SUBTYPE || AVTP_VERSION(frame) != ACMP_AVTP_VERSION ||",
           "\t    frame[PDU] != ACMP_ADP_SUBTYPE ||",
           "acmp", "AcmpCore.A26AnotherAvtpVersionIsDiscardedBeforeItIsRead", "A26 an ENTITY_AVAILABLE of version 1",
           (("acmp", "AcmpMailbox.B9AnotherAvtpVersionPassesTheFilterAndChangesNothing",
             "B9 and discovers nothing"),)),
    Mutant("acmp-version-bits-misread", ACMP_C, "#define AVTP_VERSION(frame) (((frame)[O_MSG] >> 4) & 0x07u)",
           "#define AVTP_VERSION(frame) (((frame)[O_MSG] >> 5) & 0x07u)",
           "acmp", "AcmpCore.A26AnotherAvtpVersionIsDiscardedBeforeItIsRead", "A26 a BIND_RX of AVTP version 1"),
    # a wrong version constant reads no ACMPDU at all: the first bind of the run fails
    Mutant("acmp-header-version-1", ACMP_H, "#define ACMP_AVTP_VERSION 0u", "#define ACMP_AVTP_VERSION 1u",
           "acmp", "AcmpCore.A1BindFromUnboundRespondsThenProbes",
           "A1 BIND_RX sends two frames: the response and the probe"),
    # R531-1-F2: TMR_NO_RESP from the accepted send of each attempt
    Mutant("acmp-owed-probe-timer-runs", ACMP_C,
           "\t} else if (sent == OWED) {\n\t\ts->timer = ACMP_TIMER_NO_RESP;\n\t\ts->timer_held = true;\n",
           "\t} else if (sent == OWED) {\n\t\tsm_timer(a, s, ACMP_TIMER_NO_RESP, ACMP_TMR_NO_RESP_MS);\n",
           "acmp", "AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves",
           "A27 a probe with no transmit room: PRB_W_RESP, its TMR_NO_RESP held",
           (("acmp", "AcmpCore.A27AStalledDuplicateGetsItsWholeInterval",
             "A27 the first TMR_NO_RESP finds no room"),
            ("acmp", "AcmpCore.A23EveryEntryRefusesACallFromInsideAPort",
             "A23 and the outer call completes as if it had not been made"))),
    Mutant("acmp-owed-probe-never-starts", ACMP_C,
           "\tif (s->timer_held && wire_be16(o->frame + O_SEQ) == s->probe_seq) {\n"
           "\t\tno_resp_from_send(a, s);\n\t}",
           "\t(void)s;",
           "acmp", "AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves",
           "A27 the probe leaves 5 ms late and TMR_NO_RESP runs 200 ms from that send",
           (("acmp", "AcmpCore.A27AStalledDuplicateGetsItsWholeInterval", "A27 the duplicate, the first probe's"),)),
    Mutant("acmp-owed-probe-no-resp-2s", ACMP_C,
           "== s->probe_seq) {\n\t\tno_resp_from_send(a, s);",
           "== s->probe_seq) {\n\t\tno_resp_from_send(a, s);\n\t\ts->timer_deadline += 9u * ACMP_TMR_NO_RESP_MS;",
           "acmp", "AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves",
           "A27 the probe leaves 5 ms late and TMR_NO_RESP runs 200 ms from that send"),
    Mutant("acmp-owed-probe-sequence-unchecked", ACMP_C,
           "\tif (s->timer_held && wire_be16(o->frame + O_SEQ) == s->probe_seq) {", "\tif (s->timer_held) {",
           "acmp", "AcmpCore.A27AProbeOwedPastAnUnbindARebindOrASuccessStartsNothing",
           "A27 the old probe leaving starts no timer for the new one"),
    Mutant("acmp-owed-probe-unnamed", ACMP_C, "\to->probe_of = (uint8_t)probe_of;",
           "\to->probe_of = (uint8_t)(probe_of > ACMP_MAX_SINKS + 1u);",
           "acmp", "AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves",
           "A27 the probe leaves 5 ms late and TMR_NO_RESP runs 200 ms from that send"),
    Mutant("acmp-owed-probe-names-the-next-sink", ACMP_C, "transmit(a, s->interface, frame, 0u, k + 1u);",
           "transmit(a, s->interface, frame, 0u, k + 2u);",
           "acmp", "AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves",
           "A27 the probe leaves 5 ms late and TMR_NO_RESP runs 200 ms from that send"),
    # R531-2-F1: TMR_NO_RESP from the clock after the port took the probe, whatever the entry read before
    Mutant("acmp-probe-timer-before-its-send", ACMP_C,
           "\tenum sent sent = transmit(a, s->interface, frame, 0u, k + 1u);\n\tif (sent == SENT) {\n"
           "\t\tno_resp_from_send(a, s);",
           "\tsm_timer(a, s, ACMP_TIMER_NO_RESP, ACMP_TMR_NO_RESP_MS);\n"
           "\tenum sent sent = transmit(a, s->interface, frame, 0u, k + 1u);\n\tif (sent == SENT) {\n"
           "\t\ts->timer_held = false;",
           "acmp", "AcmpCore.A30AProbeTakenAtOnceRunsFromTheClockAfterItsSend",
           "A30 the probe taken at once: TMR_NO_RESP 200 ms from the clock after its send",
           (("acmp", "AcmpCore.A30ADuplicateTakenAtOnceRunsFromTheClockAfterItsSend",
             "A30 the duplicate taken at once"),)),
    Mutant("acmp-taken-probe-timer-from-the-entry-clock", ACMP_C,
           "\tif (sent == SENT) {\n\t\tno_resp_from_send(a, s);",
           "\tif (sent == SENT) {\n\t\tsm_timer(a, s, ACMP_TIMER_NO_RESP, ACMP_TMR_NO_RESP_MS);",
           "acmp", "AcmpCore.A30ADuplicateTakenAtOnceRunsFromTheClockAfterItsSend",
           "A30 the duplicate taken at once: TMR_NO_RESP 200 ms from the clock after its send, not the expiry's"),
    Mutant("acmp-expiry-due-at-its-first-read", ACMP_C,
           ("\ta->timer_armed[interface] = false;\n\tfor (unsigned k = 0; k < a->cfg.n_sinks; ++k) {\n"
            "\t\tstruct acmp_sink *s = &a->sinks[k];\n\t\tif (s->interface != interface) {\n\t\t\tcontinue;\n\t\t}\n"
            "\t\tif (s->adp_armed && due(s->adp_deadline, now(a))) {      // Milan v1.2 5.6.4.5.4\n"
            "\t\t\ts->adp_armed = false;\n\t\t\ttk_departed(s);\n\t\t}\n"
            "\t\twhile (sm_running(s) && due(s->timer_deadline, now(a))) {\n\t\t\tsm_expired(a, k);\n"),
           ("\ta->timer_armed[interface] = false;\n\tconst uint32_t t = now(a);\n"
            "\tfor (unsigned k = 0; k < a->cfg.n_sinks; ++k) {\n\t\tstruct acmp_sink *s = &a->sinks[k];\n"
            "\t\tif (s->interface != interface) {\n\t\t\tcontinue;\n\t\t}\n"
            "\t\tif (s->adp_armed && due(s->adp_deadline, t)) {\n\t\t\ts->adp_armed = false;\n\t\t\ttk_departed(s);\n"
            "\t\t}\n\t\twhile (sm_running(s) && due(s->timer_deadline, t)) {\n\t\t\tsm_expired(a, k);\n"),
           "acmp", "AcmpCore.A30ATimerDueAfterAnEarlierSinksSendIsTakenInTheSameExpiry",
           "A30 sink 1's 0 ms TMR_DELAY, drawn after sink 0's duplicate moved the clock"),
    Mutant("acmp-held-timer-expires", ACMP_C, "\t\twhile (sm_running(s) && due(s->timer_deadline, now(a))) {",
           "\t\twhile (s->timer != ACMP_TIMER_NONE && due(s->timer_deadline, now(a))) {",
           "acmp", "AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves",
           "A27 an expiry of the interface while the probe is owed takes nothing"),
    Mutant("acmp-held-timer-armed", ACMP_C,
           "\t\t\t\tearliest(&any, &at, sm_running(s), s->timer_deadline);",
           "\t\t\t\tearliest(&any, &at, s->timer != ACMP_TIMER_NONE, s->timer_deadline);",
           "acmp", "AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves",
           "A27 a probe with no transmit room: PRB_W_RESP, its TMR_NO_RESP held, no timer armed"),
    Mutant("acmp-lost-probe-held", ACMP_C,
           "\t} else {\n\t\tsm_timer(a, s, ACMP_TIMER_NO_RESP, ACMP_TMR_NO_RESP_MS);\n\t\ta->probes_lost++;",
           "\t} else {\n\t\ts->timer = ACMP_TIMER_NO_RESP;\n\t\ts->timer_held = true;\n\t\ta->probes_lost++;",
           "acmp", "AcmpCore.A19AProbeWithoutRoomIsLostAndRecovered", "A19 and it does"),
    Mutant("acmp-stop-keeps-the-hold", ACMP_C,
           "\ts->timer = ACMP_TIMER_NONE;\n\ts->timer_held = false;\n}", "\ts->timer = ACMP_TIMER_NONE;\n}",
           "acmp", "AcmpCore.A27AProbeOwedPastAnUnbindARebindOrASuccessStartsNothing",
           "A27 an UNBIND_RX while the probe is owed stops its timer"),
    # R531-1-F3: the slot range is compared, never summed or narrowed
    Mutant("acmp-slot-sum-wraps", "acmp/acmp_mbx.c", "\tif (first_slot > MBX_N_TIMERS - MBX_N_IF ||",
           "\tif (first_slot + MBX_N_IF > MBX_N_TIMERS ||",
           "acmp", "AcmpAdapterUnit.B7RefusalsOfTheAdapter", "B7 a first slot of 4294967295 is refused"),
    Mutant("acmp-slot-narrowed-first", "acmp/acmp_mbx.c", "\tif (first_slot > MBX_N_TIMERS - MBX_N_IF ||",
           "\tif ((uint8_t)first_slot > MBX_N_TIMERS - MBX_N_IF ||",
           "acmp", "AcmpAdapterUnit.B7RefusalsOfTheAdapter", "B7 a first slot of 256 is refused"),
    Mutant("acmp-slots-one-short", "acmp/acmp_mbx.c", "\tif (first_slot > MBX_N_TIMERS - MBX_N_IF ||",
           "\tif (first_slot >= MBX_N_TIMERS - MBX_N_IF ||",
           "acmp", "AcmpAdapterUnit.B7RefusalsOfTheAdapter", "B7 the last slot range that fits is taken"),
    # R530-1-F1: the adapter's per-interface wiring, graded at two interfaces
    Mutant("acmp-one-slot-for-all-interfaces", "acmp/acmp_mbx.c", "\t\tm->ifs[k].slot = (uint8_t)(first_slot + k);",
           "\t\tm->ifs[k].slot = (uint8_t)first_slot;",
           "acmpif2", "AcmpMailbox.B3TheTimersRunOnTheInterfaceSlot",
           "B3 TMR_NO_RESP is armed on interface 1's ACMP slot"),
    Mutant("acmp-expiry-to-interface-0", "acmp/acmp_mbx.c", "\t\tacmp_timer_expired(&m->acmp, k);",
           "\t\tacmp_timer_expired(&m->acmp, 0u);",
           "acmpif2", "AcmpMailbox.B3TheTimersRunOnTheInterfaceSlot",
           "B3 the duplicate leaves at 200 ms exactly, on interface 1"),
    Mutant("acmp-gptp-of-interface-0", "acmp/acmp_mbx.c", "\t*gm_id = mbx_gm_id(interface, domain);",
           "\t*gm_id = mbx_gm_id(interface & 0u, domain);",
           "acmpif2", "AcmpMailbox.B6TheGrandmasterIsTheInterfaces",
           "B6 one from interface 1's grandmaster and domain is taken"),
    # R530-1-F2: the BINDING record is the processor's payload, flag for flag and 20 bytes
    Mutant("acmp-record-flag-defines-swapped", ACMP_C,
           "#define BIND_STARTED 0x02u\n#define BIND_STREAMING_WAIT 0x04u",
           "#define BIND_STARTED 0x04u\n#define BIND_STREAMING_WAIT 0x02u",
           "acmp", "AcmpCore.A24TheRecordIsTheProcessorsPayloadOneFlagAtATime",
           "A24 bound and started: flags 0x03"),
    Mutant("acmp-record-valid-bit-moved", ACMP_C, "#define BIND_VALID 0x01u", "#define BIND_VALID 0x08u",
           "acmp", "AcmpCore.A24TheRecordIsTheProcessorsPayloadOneFlagAtATime",
           "A24 bound and stopped: the valid flag alone, 0x01"),
    Mutant("acmp-longer-record-applied", ACMP_C, "if (sink >= a->cfg.n_sinks || len != ACMP_BINDING_BYTES) {",
           "if (sink >= a->cfg.n_sinks || len < ACMP_BINDING_BYTES) {",
           "acmp", "AcmpCore.A24UnboundRecordsRefusalsAndRollback", "A24 a payload of 21 bytes is refused"),
    # R530-1-F3: a D3 roll-back leaves the bindings applied
    Mutant("acmp-nvm-d3-rollback-drops-bindings", "acmp/acmp_nvm.c",
           "\tstruct acmp_nvm *n = ctx;\n\tif (walk != NVM_W_BIND) {",
           "\tstruct acmp_nvm *n = ctx;\n\tacmp_restore_rollback(n->acmp);\n\tif (walk != NVM_W_BIND) {",
           "acmpnvm", "AcmpStore.N7AD3RollBackKeepsTheBindings", "N7 and leaves the applied binding",
           (("acmpnvm", "AcmpStore.N7AD3RollBackKeepsTheBindings", "N7 and the saved binding still comes back"),)),
    # R530-1-F4: every timer across the 32-bit millisecond wrap
    Mutant("acmp-due-unsigned", ACMP_C, "\treturn (int32_t)(deadline - at) <= 0;", "\treturn deadline <= at;",
           "acmp", "AcmpCore.A28EveryTimerExpiresAtItsDeadlineAcrossTheWrap",
           "A28 TMR_NO_RESP: nothing at the wrap or 1 ms before its deadline",
           (("acmp", "AcmpCore.A28TheEarliestDeadlineIsChosenAcrossTheWrap",
             "A28 the first expiry takes sink 0 only"),)),
    Mutant("acmp-earliest-unsigned", ACMP_C, "(!*any || (int32_t)(deadline - *at) < 0)",
           "(!*any || deadline < *at)",
           "acmp", "AcmpCore.A28TheEarliestDeadlineIsChosenAcrossTheWrap",
           "A28 the interface timer holds the earlier deadline"),
    Mutant("acmp-no-adp-due-unsigned", ACMP_C, "\t\tif (s->adp_armed && due(s->adp_deadline, now(a))) {",
           "\t\tif (s->adp_armed && s->adp_deadline <= now(a)) {",
           "acmp", "AcmpCore.A28EveryTimerExpiresAtItsDeadlineAcrossTheWrap", "A28 TMR_NO_ADP: nothing before"),
    *[Mutant(f"acmp-{name}-deadline-saturates", ACMP_C, "\ts->timer_deadline = now(a) + delay_ms;",
             f"\ts->timer_deadline = kind == {kind} && now(a) > 0xFFFFFFFFu - delay_ms ? 0xFFFFFFFFu : "
             "now(a) + delay_ms;",
             "acmp", "AcmpCore.A28EveryTimerExpiresAtItsDeadlineAcrossTheWrap", f"A28 {label}: nothing")
      for name, kind, label in (("no-resp", "ACMP_TIMER_NO_RESP", "TMR_NO_RESP"),
                                ("retry", "ACMP_TIMER_RETRY", "TMR_RETRY"),
                                ("no-tk", "ACMP_TIMER_NO_TK", "TMR_NO_TK"),
                                ("delay", "ACMP_TIMER_DELAY", "TMR_DELAY"))],
    Mutant("acmp-no-adp-deadline-saturates", ACMP_C, "\ts->adp_deadline = now(a) + valid_ms;",
           "\ts->adp_deadline = now(a) > 0xFFFFFFFFu - valid_ms ? 0xFFFFFFFFu : now(a) + valid_ms;",
           "acmp", "AcmpCore.A28EveryTimerExpiresAtItsDeadlineAcrossTheWrap", "A28 TMR_NO_ADP: nothing before"),
    # the adp channel's bound-talker term (#665 comment 6029368753): the core's admit port
    Mutant("acmp-admit-never-called", ACMP_C, "\t\t\tp_admit(a, s->interface, k, s->bound, talker);",
           "\t\t\t(void)p_admit;",
           "acmp", "AcmpCore.A29TheAdmitPortFollowsEachSinksBoundTalker", "A29 a BIND_RX admits its talker once",
           (("acmp", "AcmpMailbox.B8TheBoundTalkerTableFollowsEachBinding", "B8 a BIND_RX writes its sink's entry"),
            ("acmp", "AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem",
             "C0 and its talker admitted in that pass"))),
    Mutant("acmp-admit-on-every-entry", ACMP_C,
           "if (s->bound != s->admitted || (s->bound && talker != s->admitted_talker)) {",
           "if (s->bound != s->admitted || s->bound) {",
           "acmp", "AcmpCore.A29TheAdmitPortFollowsEachSinksBoundTalker",
           "A29 a re-bind to the same talker, from any controller or source, admits nothing",
           (("acmp", "AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem", "C1 GET_RX_STATE -> response"),)),
    # #697: the stack's test (tsn-c-stack tests/test_acmp.cpp) asserts the admission count first, in its own
    # words, which are this killer's, as they are its own table's.
    Mutant("acmp-admit-ignores-another-talker", ACMP_C,
           "if (s->bound != s->admitted || (s->bound && talker != s->admitted_talker)) {",
           "if (s->bound != s->admitted) {",
           "acmp", "AcmpCore.A29TheAdmitPortFollowsEachSinksBoundTalker", "A29 re-binding emits one admission",
           (("acmp", "AcmpMailbox.B8TheBoundTalkerTableFollowsEachBinding",
             "B8 a BIND_RX of another talker rewrites the entry"),)),
    Mutant("acmp-admit-on-interface-0", ACMP_C, "\t\t\tp_admit(a, s->interface, k, s->bound, talker);",
           "\t\t\tp_admit(a, 0u, k, s->bound, talker);",
           "acmp", "AcmpCore.A29TheAdmitPortFollowsEachSinksBoundTalker", "A29 sink 2's talker on interface 1",
           (("acmpif2", "AcmpMailbox.B8TheBoundTalkerTableFollowsEachBinding",
             "B8 a BIND_RX writes its sink's entry of interface 1's table"),)),
    Mutant("acmp-admit-port-unflagged", ACMP_C,
           "\ta->in_port = true;\n\ta->ports->admit(a->ports->ctx, interface, sink, bound, talker);",
           "\ta->ports->admit(a->ports->ctx, interface, sink, bound, talker);",
           "acmp", "AcmpCore.A23EveryPortIsGuarded", "A23 the port kind 10 is guarded"),
    # #697: likewise the withdrawal count, first and in the stack's words.
    Mutant("acmp-reset-forgets-the-admitted", ACMP_C,
           "\tmemset(s, 0, sizeof *s);\n\ts->admitted = admitted;\n\ts->admitted_talker = admitted_talker;",
           "\tmemset(s, 0, sizeof *s);\n\t(void)admitted;\n\t(void)admitted_talker;",
           "acmp", "AcmpCore.A29RestoredBindingsAreAdmittedWhenTheTransportOpens",
           "A29 opening after reset emits one withdrawal"),
    Mutant("acmp-open-does-nothing", ACMP_C,
           "void acmp_open(struct acmp *a)\n{\n\tif (!enter(a)) {\n\t\treturn;\n\t}\n\tfinish(a);\n}",
           "void acmp_open(struct acmp *a)\n{\n\t(void)a;\n}",
           "acmp", "AcmpCore.A29RestoredBindingsAreAdmittedWhenTheTransportOpens",
           "A29 acmp_open admits each restored binding's talker",
           (("acmp", "AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract",
             "U5 and writes the bound-talker entry of the binding restored"),)),
    Mutant("acmp-open-unguarded", ACMP_C,
           "void acmp_open(struct acmp *a)\n{\n\tif (!enter(a)) {\n\t\treturn;\n\t}\n",
           "void acmp_open(struct acmp *a)\n{\n",
           "acmp", "AcmpCore.A23EveryEntryRefusesACallFromInsideAPort",
           "A23 a call made from inside the send port is refused, counted and trapped, entry 10"),
    Mutant("app-acmp-never-opened", "app/ctrl_app.c", "\t\tacmp_mbx_open(&app->acmp);\n", "",
           "acmp", "AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract",
           "U5 and writes the bound-talker entry of the binding restored",
           (("acmp", "AcmpMailbox.B5TheTapHandsAvailableToDiscoveryAndTheRestToAdp",
             "B5 the open wrote the restored binding's talker"),)),
    Mutant("acmp-mbx-admit-on-entry-0", "acmp/acmp_mbx.c",
           "\t(void)mbx_filter_set_bound_talker(interface, sink, bound, talker_entity_id);",
           "\t(void)mbx_filter_set_bound_talker(interface, sink & 0u, bound, talker_entity_id);",
           "acmp", "AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract",
           "U5 and writes the bound-talker entry of the binding restored"),
    Mutant("acmp-mbx-admit-always-bound", "acmp/acmp_mbx.c",
           "\t(void)mbx_filter_set_bound_talker(interface, sink, bound, talker_entity_id);",
           "\t(void)bound;\n\t(void)mbx_filter_set_bound_talker(interface, sink, true, talker_entity_id);",
           "acmp", "AcmpMailbox.B8TheBoundTalkerTableFollowsEachBinding", "B8 an UNBIND_RX clears the entry's BOUND_EN",
           (("acmp", "AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem",
             "C3 UNBIND_RX answered in one pass, its talker withdrawn"),)),
    # the driver's bound-talker entries (mbx.c)
    Mutant("mbx-bound-unguarded", "mbx/mbx.c",
           "\tif (interface >= MBX_N_IF || entry >= MBX_N_BOUND) {\n\t\treturn false;\n\t}\n"
           "\tmbx_hal_write32(bnd_reg(", "\tmbx_hal_write32(bnd_reg(",
           "unit", "DriverUnit.D13BoundTalkerEntries", "D13 an interface past the contract's is refused"),
    Mutant("mbx-bound-entry-unguarded", "mbx/mbx.c", "\tif (interface >= MBX_N_IF || entry >= MBX_N_BOUND) {",
           "\tif (interface >= MBX_N_IF) {",
           "unit", "DriverUnit.D13BoundTalkerEntries", "D13 an entry past the table's is refused"),
    Mutant("mbx-bound-withdraw-writes-nothing", "mbx/mbx.c",
           "\tmbx_hal_write32(bnd_reg(interface, entry, MBX_BND_REG_BOUND_EN), 0u);\n\tif (bound) {",
           "\tif (bound) {\n\t\tmbx_hal_write32(bnd_reg(interface, entry, MBX_BND_REG_BOUND_EN), 0u);",
           "unit", "DriverUnit.D13BoundTalkerEntries", "D13 a withdrawn entry: BOUND_EN cleared",
           (("acmp", "AcmpMailbox.B8TheBoundTalkerTableFollowsEachBinding",
             "B8 an UNBIND_RX clears the entry's BOUND_EN"),)),
    Mutant("mbx-bound-enabled-before-the-identity", "mbx/mbx.c",
           "\tmbx_hal_write32(bnd_reg(interface, entry, MBX_BND_REG_BOUND_EN), 0u);\n\tif (bound) {\n",
           "\tmbx_hal_write32(bnd_reg(interface, entry, MBX_BND_REG_BOUND_EN), bound ? 1u : 0u);\n\tif (bound) {\n",
           "unit", "DriverUnit.D13BoundTalkerEntries",
           "D13 BOUND_EN is cleared before the identity is written"),
    Mutant("mbx-bound-halves-swapped", "mbx/mbx.c",
           "mbx_place((uint32_t)talker_entity_id, MBX_BOUND_EID_LO_EID_LSB, MBX_BOUND_EID_LO_EID_WIDTH)",
           "mbx_place((uint32_t)(talker_entity_id >> 32), MBX_BOUND_EID_LO_EID_LSB, MBX_BOUND_EID_LO_EID_WIDTH)",
           "unit", "DriverUnit.D13BoundTalkerEntries", "D13 BOUND_EID_LO holds talker[31:0]",
           (("acmp", "AcmpMailbox.B8TheBoundTalkerTableFollowsEachBinding", "B8 a BIND_RX writes its sink's entry"),)),
    Mutant("mbx-bound-entry-stride-ignored", "mbx/mbx.c",
           "MBX_BND_STRIDE * (uint32_t)interface + MBX_BND_ENTRY_STRIDE * (uint32_t)entry + reg;",
           "MBX_BND_STRIDE * (uint32_t)interface + 0u * (uint32_t)entry + reg;",
           "unit", "DriverUnit.D13BoundTalkerEntries", "D13 BOUND_EID_LO holds talker[31:0]",
           (("acmp", "AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract",
             "U5 and writes the bound-talker entry of the binding restored"),)),
    # the host model's twins of the RTL's eq_bound arms (tb/verilator/mbx/mutants.py)
    Mutant("model-bound-term-misses", "host/mbx_model.c",
           "\t\treturn field_ok && bound_talker(m, interface, wire_be64(frame + off));",
           "\t\treturn field_ok && bound_talker(m, interface, wire_be64(frame + off) + 1u);",
           "model", "Suite/MbxModelGroup.PassesOnTheModel/AdpBoundTalkers",
           "Q12 an ENTITY_AVAILABLE of a bound talker reaches the adp ring"),
    Mutant("model-bound-enable-ignored", "host/mbx_model.c",
           "\t\tif (m->bound_en[interface][e] && m->bound_eid[interface][e] == field) {",
           "\t\tif (m->bound_eid[interface][e] == field) {",
           "model", "Suite/MbxModelGroup.PassesOnTheModel/AdpBoundTalkers",
           "Q12 an entry with BOUND_EN clear, its identity still written"),
    Mutant("model-bound-low-word-only", "host/mbx_model.c", "&& m->bound_eid[interface][e] == field) {",
           "&& (uint32_t)m->bound_eid[interface][e] == (uint32_t)field) {",
           "model", "Suite/MbxModelGroup.PassesOnTheModel/AdpBoundTalkers",
           "Q12 an entity_id differing from the entry in [63:32] only"),
    Mutant("model-bound-table-of-interface-0", "host/mbx_model.c",
           "\tif (interface >= MBX_N_IF) {\n\t\treturn false;\n\t}\n\tfor (unsigned e = 0; e < MBX_N_BOUND; ++e) {\n"
           "\t\tif (m->bound_en[interface][e] && m->bound_eid[interface][e] == field) {",
           "\t(void)interface;\n\tfor (unsigned e = 0; e < MBX_N_BOUND; ++e) {\n"
           "\t\tif (m->bound_en[0][e] && m->bound_eid[0][e] == field) {",
           "model", "Suite/MbxModelGroup.PassesOnTheModel/AdpBoundTalkers",
           "Q13 on another interface, or an index with no interface, it reaches no ring"),
    Mutant("model-bound-term-any-type", "host/mbx_model.c",
           "\t\tif (((term_mask[j] >> msg) & 1u) != 0u && term_holds(m, j, frame, len, interface)) {",
           "\t\tif ((((term_mask[j] | (term_test[j] == MBX_TEST_EQ_BOUND ? 0xFFFFu : 0u)) >> msg) & 1u) != 0u &&\n"
           "\t\t    term_holds(m, j, frame, len, interface)) {",
           "model", "Suite/MbxModelGroup.PassesOnTheModel/AdpBoundTalkers",
           "Q12 no other message_type of a bound talker passes on its entity_id"),
    Mutant("model-bound-entry-decoded-as-0", "host/mbx_model.c",
           "\t*e = (rel % MBX_BND_STRIDE) / MBX_BND_ENTRY_STRIDE;", "\t*e = 0u;",
           "model", "Suite/MbxModelGroup.PassesOnTheModel/ResetIdentityAndRegisterMasks",
           "R1 each bound-talker entry keeps"),
    Mutant("model-bound-en-reads-the-eid", "host/mbx_model.c",
           "\treturn reg == MBX_BND_REG_BOUND_EN && m->bound_en[i][e] ? 1u : 0u;",
           "\treturn reg == MBX_BND_REG_BOUND_EN ? (uint32_t)m->bound_eid[i][e] : 0u;",
           "model", "Suite/MbxModelGroup.PassesOnTheModel/ResetIdentityAndRegisterMasks",
           "R1 each bound-talker entry keeps"),
    # round 6: the timer slots of the three modules
    Mutant("app-maap-slots-overlap-acmp", "app/ctrl_app.h",
           "#define CTRL_APP_MAAP_FIRST_SLOT (CTRL_APP_ACMP_FIRST_SLOT + MBX_N_IF)",
           "#define CTRL_APP_MAAP_FIRST_SLOT (CTRL_APP_ACMP_FIRST_SLOT)",
           "acmp", U6, "U6 every interface's ADP, ACMP and MAAP slots are distinct and inside the timer bank"),
    Mutant("app-maap-slots-overlap-adp", "app/ctrl_app.h",
           "#define CTRL_APP_MAAP_FIRST_SLOT (CTRL_APP_ACMP_FIRST_SLOT + MBX_N_IF)",
           "#define CTRL_APP_MAAP_FIRST_SLOT (CTRL_APP_ADP_FIRST_SLOT)",
           "maap", EXPLICIT, "protocol timer slots disjoint",
           (("acmp", U6, "U6 every interface's ADP, ACMP and MAAP slots are distinct"),)),
    # round 6: the attach order, and every channel opened by the open
    Mutant("app-maap-attached-after-open", APP,
           "\treturn cfg->maap_allocation == NULL || maap_compose(app, cfg);\n}" + APP_OPEN +
           "\t\t(void)maap_mbx_start(",
           "\treturn true;\n}" + APP_OPEN + "\t\t(void)maap_compose(app, cfg);\n\t\t(void)maap_mbx_start(",
           "acmp", U6, "U6 opening opens the adp, acmp and maap channels and no other",
           (("maap", EXPLICIT, ""),)),
    Mutant("app-maap-before-acmp", APP, APP_ACMP_THEN_MAAP,
           "\tif (cfg->maap_allocation != NULL && !maap_compose(app, cfg)) {\n\t\treturn false;\n\t}\n"
           "\treturn cfg->acmp == NULL ||\n"
           "\t       (acmp_mbx_init(&app->acmp, cfg->acmp, cfg->acmp_env, CTRL_APP_ACMP_FIRST_SLOT) &&\n"
           "\t\tacmp_mbx_attach(&app->acmp, &app->loop));\n",
           "acmp", U6, "U6 ADP, then ACMP, then MAAP attach, each with its sink and its poll",
           (("acmp", U7, "U7 before MAAP attaches"),)),
    Mutant("app-maap-started-in-compose", APP, "\t       maap_mbx_attach(&app->maap, &app->loop);\n}",
           "\t       maap_mbx_attach(&app->maap, &app->loop) && maap_mbx_start(&app->maap, preferred);\n}",
           "acmp", U6, "U6 composing the three touches no mailbox register"),
    Mutant("app-maap-never-started", APP, "\t\t(void)maap_mbx_start(&app->maap, cfg->maap_preferred);\n", "",
           "acmp", U6, "U6 MAAP probes from the open", (("maap", EXPLICIT, ""),)),
    Mutant("app-maap-channel-unbound", "maap/maap_mbx.c",
           "\t(void)ctrl_loop_bind_rx(loop, MBX_CH_MAAP, receive, m);\n", "\t(void)receive;\n",
           "acmp", F6, "F6 events, acmp and maap records wait",
           (("acmp", U6, "U6 ACMP still stands in front of ADP's handler, and MAAP holds its own channel"),)),
    # round 6: the refusals
    Mutant("app-maap-preferred-unchecked", APP, "\tif (preferred != 0u && (preferred < MAAP_POOL_BASE ||\n",
           "\tif (false && (preferred < MAAP_POOL_BASE ||\n",
           "acmp", U7, "U7 a preferred range below the B.4 pool is refused", (("maap", EXPLICIT, ""),)),
    Mutant("app-maap-last-range-refused", APP, "\t    preferred > MAAP_POOL_BASE + MAAP_POOL_SIZE - count)) {",
           "\t    preferred >= MAAP_POOL_BASE + MAAP_POOL_SIZE - count)) {",
           "acmp", U7, "U7 the pool's last range is not"),
    Mutant("app-maap-range-past-the-pool", APP, "\t    preferred > MAAP_POOL_BASE + MAAP_POOL_SIZE - count)) {",
           "\t    preferred > MAAP_POOL_BASE + MAAP_POOL_SIZE)) {",
           "acmp", U7, "U7 one that runs past the pool's end is refused"),
    Mutant("app-maap-refusal-ignored", APP, MAAP_INIT,
           "\t(void)maap_mbx_init(&app->maap, mac, count, CTRL_APP_MAAP_FIRST_SLOT, cfg->maap_allocation, "
           "cfg->maap_ctx);\n\treturn maap_mbx_attach(&app->maap, &app->loop);\n",
           "acmp", U7, "U7 MAAP for an entity with no talker source is refused"),
    Mutant("app-acmp-refusal-ignored", APP,
           "\t     !acmp_mbx_attach(&app->acmp, &app->loop))) {\n\t\treturn false;\n\t}\n",
           "\t     !acmp_mbx_attach(&app->acmp, &app->loop))) {\n\t\t;\n\t}\n",
           "acmp", U7, "U7 a refused ACMP configuration fails the three-way composition",
           (("acmp", "AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract",
             "U5 an ACMP configuration the module refuses fails the composition"),)),
    Mutant("app-maap-entry-takes-no-port", APP, "\treturn allocation != NULL && ctrl_app_start(app, &with);",
           "\treturn ctrl_app_start(app, &with);",
           "acmp", U7, "U7 the explicit MAAP entry refuses a missing stream-address port", (("maap", EXPLICIT, ""),)),
    Mutant("app-maap-entry-drops-preferred", APP, "\twith.maap_preferred = preferred;\n", "\t(void)preferred;\n",
           "maap", EXPLICIT, ""),
    # round 6: the three-way pass bound (CTRL_APP_THREE_PASS_MAX)
    Mutant("app-three-way-pass-overrun", "maap/maap_mbx.c", "\tmaap_rx(&m->ifs[f->interface].core",
           "\tfor (unsigned k = 0; k < 2000u; ++k) {\n\t\t(void)mbx_now_ms();\n\t}\n"
           "\tmaap_rx(&m->ifs[f->interface].core",
           "acmp", F6, "F6 the worst pass of the three-way backlog"),
    # round 7 (R530-5-F1): MAAP's source on each interface is the own unicast MAC the filter holds there
    Mutant("app-maap-mac-per-interface", APP, "\t\tmac[k] = cfg->entity->mac;\n",
           "\t\tmac[k] = cfg->entity->mac + k;\n",
           "acmpif2", U6, "U6 MAAP sends from its own unicast MAC, where a DEFEND is admitted, interface 1"),
    Mutant("app-own-mac-per-interface", APP, "\t\town_mac[i] = cfg->entity->mac;\n",
           "\t\town_mac[i] = cfg->entity->mac + i;\n",
           "acmpif2", U6, "U6 MAAP sends from its own unicast MAC, where a DEFEND is admitted, interface 1"),
    # round 7 (R530-5-S1): the three-way bound against the two published passes
    Mutant("app-three-way-bound-drops-maap", "app/ctrl_app.h",
           "#define CTRL_APP_THREE_PASS_MAX (ACMP_MBX_PASS_MAX + CTRL_APP_MAAP_PASS_SHARE)",
           "#define CTRL_APP_THREE_PASS_MAX (ACMP_MBX_PASS_MAX)",
           "acmp", F6, "F6 the three-way bound is both modules' passes",
           (("acmpif2", F6, "F6 the three-way bound is both modules' passes"),)),
    Mutant("app-three-way-bound-one-maap-poll", "app/ctrl_app.h",
           "(CTRL_APP_MAAP_RX_RECORD_MAX + MAAP_MBX_RX_MAX) + MBX_N_IF * MAAP_MBX_POLL_MAX)",
           "(CTRL_APP_MAAP_RX_RECORD_MAX + MAAP_MBX_RX_MAX) + MAAP_MBX_POLL_MAX)",
           "acmpif2", F6, "F6 the three-way bound is both modules' passes"),
)
