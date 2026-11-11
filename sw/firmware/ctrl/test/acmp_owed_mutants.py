# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""acmp_owed_mutants.py - the planted defects of the ACMP owed frames (#665).

The owed frames and their changes (#653: A19, E1 to E3), the core's owed bound,
which declines a command it cannot answer yet (tsn-c-stack#26, ACMP-12), and
the mailbox adapter's kept command (K), which after each poll that sends an
owed frame offers that command again and then the records waiting behind it,
until the core declines one or none is left. acmp_mutants.py appends this
table to its own.
"""

from __future__ import annotations

from ctrl_mutant import ACMP_C, Mutant

MUTANTS = (
    # owed frames and #653 (A19, E1, E2)
    Mutant("acmp-response-passes-an-owed-frame", ACMP_C,
           "\tif (a->owed_count == 0u && p_send(a, interface, frame)) {", "\tif (p_send(a, interface, frame)) {",
           "acmp", "AcmpCore.A19NothingPassesAnOwedFrame", "A19 a response does not pass one already owed"),
    Mutant("acmp-poll-drains-everything", ACMP_C,
           "\tif (a->owed_count != 0u) {\n\t\tconst struct acmp_owed *o = &a->owed[a->owed_head];\n"
           "\t\tif (p_send(a, o->interface, o->frame)) {",
           "\twhile (a->owed_count != 0u &&\n"
           "\t       p_send(a, a->owed[a->owed_head].interface, a->owed[a->owed_head].frame)) {\n"
           "\t\tconst struct acmp_owed *o = &a->owed[a->owed_head];\n\t\t{",
           "acmp", "AcmpCore.A19AResponseWithoutRoomIsOwedAndItsChangeWaits", "A19 one frame per poll",
           (("acmp", "AcmpMailbox.E2AnOwedResponseIsCommittedInPassKPlus1", "E2 3 frames owed ahead"),)),
    Mutant("acmp-change-not-held-for-its-response", ACMP_C,
           ("\t\ta->sinks[k].change_owed = (uint8_t)(a->sinks[k].change_owed + ((o->release[k / 32u] >> (k % 32u)) & "
            "1u));"),
           "\t\t(void)release;",
           "acmp", "AcmpCore.A19AResponseWithoutRoomIsOwedAndItsChangeWaits",
           "A19 but its change is not reported while its response waits (#653)",
           (("acmp", "AcmpMailbox.E1AnOwedResponseLeavesFirstAndItsChangeAfterIt", "E1 nothing reported yet"),)),
    Mutant("acmp-full-queue-acts", ACMP_C,
           "\tif (a->owed_count + frames <= ACMP_OWED_MAX) {\n\t\treturn true;\n\t}\n\ta->busy_declined++;",
           "\tif (a->owed_count + frames <= ACMP_OWED_MAX || true) {\n\t\treturn true;\n\t}\n\ta->busy_declined++;",
           "acmp", "AcmpCore.A19AFullQueueDeclinesTheCommandBeforeItActs",
           "A19 a command whose response would find the queue full is declined before it changes anything",
           (("acmp", "AcmpOwed.HeldEgressDefersTheCommandBehindTheOwedSet", "is declined to the port, not taken"),)),
    Mutant("acmp-lost-probe-uncounted", ACMP_C,
           "\t\tsm_timer(a, s, ACMP_TIMER_NO_RESP, ACMP_TMR_NO_RESP_MS);\n\t\ta->probes_lost++;\n\t}",
           "\t\tsm_timer(a, s, ACMP_TIMER_NO_RESP, ACMP_TMR_NO_RESP_MS);\n\t}",
           "acmp", "AcmpCore.A19AProbeWithoutRoomIsLostAndRecovered",
           "A19 a probe the full queue cannot take is lost and counted"),
    Mutant("acmp-first-owed-releases-every-change", ACMP_C,
           ("\t\t\t\tif (((o->release[k / 32u] >> (k % 32u)) & 1u) != 0u) {\n\t\t\t\t\tmark(a, k);\n"
            "\t\t\t\t\ta->sinks[k].change_owed--;\n\t\t\t\t}"),
           "\t\t\t\tmark(a, k);\n\t\t\t\ta->sinks[k].change_owed = 0u;",
           "acmp", "AcmpCore.A19TwoOwedResponsesForOneSinkReleaseTogether",
           "A19 the bind's response left but the unbind's is still owed"),
    Mutant("acmp-poll-newest-first", ACMP_C,
           "\t\tconst struct acmp_owed *o = &a->owed[a->owed_head];\n\t\tif (p_send(a, o->interface, o->frame)) {",
           "\t\tconst struct acmp_owed *o = &a->owed[(a->owed_head + a->owed_count - 1u) % ACMP_OWED_MAX];\n"
           "\t\tif (p_send(a, o->interface, o->frame)) {",
           "acmp", "AcmpMailbox.E2AnOwedResponseIsCommittedInPassKPlus1", "E2 3 frames owed ahead",
           (("acmp", "AcmpCore.A19NothingPassesAnOwedFrame", "A19 they leave in the order they were made"),)),
    # the adapter's poll (E1)
    Mutant("acmp-poll-owes-nothing", "acmp/acmp_mbx.c", "\treturn m->acmp.owed_count != 0u;", "\treturn false;",
           "acmp", "AcmpMailbox.E1AnOwedResponseLeavesFirstAndItsChangeAfterIt",
           "E1 nothing reported yet, and the loop does not sleep"),
    Mutant("acmp-poll-owes-nothing-at-one", "acmp/acmp_mbx.c", "\treturn m->acmp.owed_count != 0u;",
           "\treturn m->acmp.owed_count > 1u;",
           "acmp", "AcmpMailbox.E3OneOwedFrameAloneKeepsTheLoopAwake",
           "E3 the ACMP poll says it still owes its one frame behind the held egress"),
    # THE KEPT COMMAND (K, tsn-c-stack ACMP-12): a command the core declines at its owed bound
    Mutant("acmp-kept-dropped", "acmp/acmp_mbx.c",
           "\tif (acmp_rx(&m->acmp, f->interface, f->bytes, f->len)) {\n\t\treturn;",
           "\tif (acmp_rx(&m->acmp, f->interface, f->bytes, f->len) || true) {\n\t\treturn;",
           "acmp", "AcmpMailbox.K1ACommandDeclinedAtTheOwedBoundIsKeptAndAnsweredInArrivalOrder",
           "K1 the first command behind the full owed set is declined once and kept",
           (("acmp", "AcmpMailbox.K2ABindDeclinedAtTheFullSetWaitsForTwoSlotsAndLosesNoProbe",
             "K2 the BIND_RX is declined, binds nothing and is kept"),)),
    Mutant("acmp-kept-passed", "acmp/acmp_mbx.c", "\treturn m->kept.len == 0u;", "\treturn m->kept.len == 0u || true;",
           "acmp", "AcmpMailbox.K1ACommandDeclinedAtTheOwedBoundIsKeptAndAnsweredInArrivalOrder",
           "the second left in the ring"),
    Mutant("acmp-kept-never-offered", "acmp/acmp_mbx.c",
           "\t\tif (!acmp_rx(&m->acmp, m->kept.interface, m->kept.frame, m->kept.len)) {\n\t\t\treturn;",
           "\t\tif (true) {\n\t\t\treturn;",
           "acmp", "AcmpMailbox.K1ACommandDeclinedAtTheOwedBoundIsKeptAndAnsweredInArrivalOrder",
           "K1 the kept command is answered in pass ACMP_OWED_MAX + 1 after the room returns"),
    Mutant("acmp-kept-after-it-is-taken", "acmp/acmp_mbx.c", "\t\tm->kept.len = 0u;\n\t}\n\tstruct ctrl_loop",
           "\t}\n\tstruct ctrl_loop",
           "acmp", "AcmpMailbox.K1ACommandDeclinedAtTheOwedBoundIsKeptAndAnsweredInArrivalOrder",
           "K1 the command kept behind it in pass n + 1 + f"),
    Mutant("acmp-kept-offered-on-a-refused-poll", "acmp/acmp_mbx.c",
           "\tif (m->acmp.owed_count < owed) {\n\t\tredeliver(m);",
           "\tif (m->acmp.owed_count <= owed) {\n\t\tredeliver(m);",
           "acmp", "AcmpMailbox.K1ACommandDeclinedAtTheOwedBoundIsKeptAndAnsweredInArrivalOrder",
           "K1 the first command behind the full owed set is declined once and kept"),
    Mutant("acmp-kept-on-interface-zero", "acmp/acmp_mbx.c", "\tm->kept.interface = f->interface;",
           "\tm->kept.interface = 0u;",
           "acmpif2", "AcmpMailbox.K1ACommandDeclinedAtTheOwedBoundIsKeptAndAnsweredInArrivalOrder",
           "K1 on the interface it arrived on",
           (("acmpif2", "AcmpMailbox.K2ABindDeclinedAtTheFullSetWaitsForTwoSlotsAndLosesNoProbe",
             "K2 the BIND_RX is answered SUCCESS in pass n + 1 after the room returns, on its interface"),)),
    Mutant("acmp-kept-dropped-when-declined-again", "acmp/acmp_mbx.c",
           ("\t\tif (!acmp_rx(&m->acmp, m->kept.interface, m->kept.frame, m->kept.len)) {\n\t\t\treturn;\n"
            "\t\t}\n\t\tm->kept.len = 0u;"),
           "\t\t(void)acmp_rx(&m->acmp, m->kept.interface, m->kept.frame, m->kept.len);\n\t\tm->kept.len = 0u;",
           "acmp", "AcmpMailbox.K2ABindDeclinedAtTheFullSetWaitsForTwoSlotsAndLosesNoProbe",
           "K2 offered again after the first send, one slot free: declined again and still kept"),
    Mutant("acmp-kept-survives-a-start", "acmp/acmp_mbx.c", "\tmemset(m, 0, sizeof *m);",
           "\tmemset(m, 0, sizeof *m - sizeof m->kept);",
           "acmp", "AcmpMailbox.K3AStartDropsTheKeptCommand", "K3 a start keeps no command from the run before"),
    # the redelivery (tsn-c-stack PORTING "ACMP owed bound"): the waiting records after the kept one
    Mutant("acmp-redelivery-takes-no-waiting-record", "acmp/acmp_mbx.c",
           "\tfor (unsigned k = 0; k < ACMP_MBX_REDELIVER_RECORDS && m->kept.len == 0u; ++k) {",
           "\tfor (unsigned k = 0; k < ACMP_MBX_REDELIVER_RECORDS && m->kept.len == 0u && false; ++k) {",
           "acmp", "AcmpMailbox.K4ACommandBehindFramesThatNeedNoAnswerKeepsItsPass",
           "K4 the command behind two frames that need no answer in pass n + 1 + f, f = 1"),
    Mutant("acmp-redelivery-only-behind-a-kept-command", "acmp/acmp_mbx.c",
           "\tif (m->acmp.owed_count < owed) {\n\t\tredeliver(m);",
           "\tif (m->acmp.owed_count < owed && m->kept.len != 0u) {\n\t\tredeliver(m);",
           "acmp", "AcmpMailbox.K5RecordsBehindTheReceiveBudgetAreOfferedAfterTheSend",
           "K5 a command the receive service left waiting is offered after the first send"),
    Mutant("acmp-redelivery-refusal-uncounted", "acmp/acmp_mbx.c",
           "\t\t\tl->stats.rx_bad += st == MBX_STATUS_BAD;", "\t\t\t(void)st;",
           "acmp", "AcmpMailbox.K6ARecordTheDriverRefusesEndsTheRedeliveryCounted",
           "K6 the kept command taken, the refused record counted in rx_bad"),
    Mutant("acmp-redelivery-records-uncounted", "acmp/acmp_mbx.c", "\t\tl->stats.rx_records++;\n", "",
           "acmp", "AcmpMailbox.K7TheRedeliveryTakesAFullRingInThePassThatSends",
           "K7 the kept command and the full ring behind it are taken, and counted"),
    Mutant("acmp-redelivery-short-of-a-full-ring", "acmp/acmp_mbx.c",
           "\tfor (unsigned k = 0; k < ACMP_MBX_REDELIVER_RECORDS &&",
           "\tfor (unsigned k = 0; k + 1u < ACMP_MBX_REDELIVER_RECORDS &&",
           "acmp", "AcmpMailbox.K7TheRedeliveryTakesAFullRingInThePassThatSends",
           "K7 the kept command and the full ring behind it are taken"),
)
