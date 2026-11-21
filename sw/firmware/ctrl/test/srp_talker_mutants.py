# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of SRP's Talker declarations as the validity of each source's SRP parameters moves them (#895).

srp_mutants.py plants each into a copy of sw/firmware/ctrl with the rest of its table, and the named test must fail on
its own words: srp_talker.cpp's (SRP alone) or test_acmp_mbx.cpp's SrpGate (the composition: ACMP's probe and its 15 s
window, SRP's Listener registration, MAAP's DA gate and a range MAAP loses). The two-interface campaign plants them at
8x8/2if (ENTITY), the one-interface campaign at 1x1/1if (test_ctrl_firmware.run_srp_mutants selects them by name). One
defect a rule: a source declares only while valid (Milan v1.2 4.3.3.1, 5.3.7.4) and at once; a lapse withdraws, its
licence and TALKER_DECL bit first; an unchanged destination comes back at once and a changed one is held from its
Leave's request for two of the longest LeaveAll periods less a JoinTime and THE TRANSMIT's MRPDU, so it reaches the
wire no later than the two periods (IEEE 802.1Q-2018 35.2.2.8, 10.7.4.3; #951, #956), whether it changed while
declared or while lapsed, at the latest THE TRANSMIT allows, and held across a reset; never at the two LeaveAllTime
periods it was before #951, alone or after a range lost to a conflict, nor with #951's terms added past the two
periods, nor a centisecond short of the hold-off or with its terms taken twice; an admission change swaps in
place; a refused declaration is declared again; a withdrawal lwSRP refuses keeps the source declared and owed until
lwSRP takes its Leave; THE TRANSMIT's call publishes within srp_bounds.h's terms; the entry refuses before attach and
on reentry; and the composition feeds each interface's DA gate and range. The source's frames carry the stream_id
its Talker declares (#905): the MAAP adapter writes each source's SRC_SID before its DA_GATE bit first opens, each
word in its own register, again before each reopening, read from the source port, and only while the bit is clear
(KL_mbx_pkg.sv SRC_SID_LO). Each change of a source's
declaration its STREAM_OUTPUT shows is noticed for its GET_STREAM_INFO notice (#936; Milan v1.2 5.4.5.2, Table 5.22):
a declaration, a withdrawal, a type swapped in place (only once made) and an adopted Domain's other VID, and nothing
else, a reset that declares an unchanged source again included; the SRP delivery takes the record and an attach
starts with none (ctrl_app_srp.c). Each change of the Listener registered for a source's stream, which its
STREAM_OUTPUT shows too (#957; #943's REGISTERING and REGISTERING_FAILED), is recorded on its interface: a Listener
appearing, replacing another or going, a reset with one registered, and nothing else, a Listener declared again or
registered again after a LeaveAll included; its declaration as well as its presence, each copy compared.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

SUITE = "srp_talker.cpp"
COMPOSED = "test_acmp_mbx.cpp"
APP = "app/ctrl_app_srp.c"
#: The two-interface campaign's entity for these defects: 8x8/2if.
ENTITY = "endstation_ax7101_8x8"
VALID = "Talker.ValidSourceDeclaresAtOnceAndNothingBefore"
LAPSE = "Talker.LapseWithdrawsTheAdvertiseAndDeclaresNothing"
AGAIN = "Talker.UnchangedDestinationIsDeclaredAgainAtOnce"
CHANGED = "Talker.ChangedDestinationWaitsTwoLongestLeaveAllPeriods"
LATEST = "Talker.ChangedDestinationReachesTheWireWithinTwoLongestLeaveAllPeriodsAtTheLatest"
MOVED = "Talker.DestinationChangeWhileValidWithdrawsTheOld"
ADMIT = "Talker.AdmissionChangeSwapsTheTypeInPlace"
RESET = "Talker.ResetKeepsAnUnchangedSourceAndHoldsAMovedOne"
ENTRY = "Talker.GateEntryRecordsOnlyWhatChanged"
REFUSED = "Talker.RefusedDeclarationIsDeclaredAgain"
TERMS = "Talker.TransmitPublishesWithinItsTermsAfterARefusedJoin"
WITHDRAWN = "Talker.RefusedWithdrawalIsWithdrawnOnceLwsrpTakesIt"
NOTICED = "Talker.DeclarationAndWithdrawalAreNoticed"
SWAP_NOTICED = "Talker.TypeSwapIsNoticed"
VID_NOTICED = "Talker.AdoptedDomainVidIsNoticed"
RESET_NOTICED = "Talker.ResetNoticesNothingUnchanged"
REGISTRATION = "Talker.ListenerRegistrationChangeIsNoticed"
TAKEN = "SrpGate.F936AProbeAndItsExpiryEachNoticeTheSource"
TAKEN_PASS = "SrpGate.F936BThePassThatTakesTheRecordOwesItsNotice"
PROBE = "SrpGate.F895AProbeDeclaresTheSourceAndItsExpiryWithdrawsIt"
LISTENER = "SrpGate.F895AListenerKeepsTheSourceDeclaredPastTheProbeWindow"
LOST = "SrpGate.F895ARangeLostWithdrawsAndTheNewRangeWaitsTheHoldOff"
SID_OPENS = "SrpGate.F905AEachSourceStreamIdIsWrittenBeforeItsGateOpens"
SID_CHANGED = "SrpGate.F905AStreamIdChangedWhileClosedIsWrittenBeforeTheGateReopens"
SID_AGAIN = "SrpGate.F905AGateReopensOnlyOnceItsStreamIdIsWrittenAgain"
MAAP = "maap/maap_mbx.c"
#: the start's two SRC_SID words of each source, as maap_mbx.c writes them (#905).
SID_START = ("\t\t\t(void)mbx_pub_src_sid(k, s, false, (uint32_t)id);\n"
             "\t\t\t(void)mbx_pub_src_sid(k, s, true, (uint32_t)(id >> 32));\n")
#: the poll's low word of a waiting source's SRC_SID, read from its port, as maap_mbx.c writes it (#905).
SID_LOW = "\tuint64_t id = stream_of(m, s);\n\t(void)mbx_pub_src_sid(k, s, false, (uint32_t)id);\n"
#: declare_sources's withdrawal and declaration conditions and its licence closure, as srp_mbx.c holds them.
WITHDRAWS = "        if ((i->talkers & bit) != 0u && (!valid || (i->readdressed & bit) != 0u)) {\n"
WAITS = "        const bool waits = (i->readdressed & bit) != 0u && m->held_cs[n] != 0u;\n"
DECLARES = ("        if (valid && !waits && (how != SRP_DECLARE_CHANGED || (i->talkers & bit) == 0u || "
            "admitted != was)) {\n")
#: the withdrawn Talker's hold-off, as srp_mbx.c derives it: two of the longest LeaveAll periods (#951) with a JoinTime
#: and THE TRANSMIT's MRPDU by every source, rounded up to the centisecond, counted inside them (#956).
REDECLARE = "#define SRP_REDECLARE_CS (2u * SRP_LEAVEALL_LONGEST_CS - SRP_JOIN_CS - (CTRL_LOOP_TX_MS + 9u) / 10u)\n"
#: #951's hold-off: both terms added past the two periods, about 30.2 s at one interface.
ADDED = REDECLARE.replace(" - SRP_JOIN_CS - ", " + SRP_JOIN_CS + ")
#: the hold-off before #951: two LeaveAllTime periods, the shortest two LeaveAll periods can be (10.7.4.3), and both
#: terms added.
TWO_LEAVEALLTIME = ADDED.replace("2u * SRP_LEAVEALL_LONGEST_CS", "2u * SRP_LEAVEALL_CS")
LICENCE = ("            if (i->active[n]) {\n                i->active[n] = false;\n                ++m->stops;\n"
           "                publish_licence(i);\n                m->config.licence(m->config.ctx,i->index,n,false);\n"
           "            }\n")
SWAP_LEAVE = ("                if ((i->talkers & bit) != 0u && admitted != was) {\n"
              "                    (void)mrp_mad_leave(i->msrp,0,was ? MSRP_ATTR_TYPE_TALKER_ADV : "
              "MSRP_ATTR_TYPE_TALKER_FAILED,\n                                        &value);\n                }\n")
ENTRY_GUARD = ("bool srp_mbx_gate(struct srp_mbx *m, unsigned interface, uint32_t valid, uint64_t base)\n"
               "{\n    if (!enter(m)) {\n        return false;\n    }\n")
#: the withdrawal's Leave and what lwSRP's answer makes of the source, as srp_mbx.c holds them.
LEAVE = ("            if (mrp_mad_leave(i->msrp,0,was ? MSRP_ATTR_TYPE_TALKER_ADV : "
         "MSRP_ATTR_TYPE_TALKER_FAILED,&value) != 0) {\n                done = false;\n            } else {\n"
         "                i->talkers &= ~bit;\n                m->held_cs[n] = SRP_REDECLARE_CS;\n            }\n")
FEED = ("        (void)srp_mbx_gate(app->srp,interface,app->maap.published_gate[interface],"
        "app->maap.ifs[interface].core.base);\n")
#: what declare_sources notices of each source's declaration (#936), as srp_mbx.c holds it.
NOTICE_MOVED = "    uint32_t moved = (i->talkers ^ i->shown) | ((advertise ^ i->shown_advertise) & kept);\n"
VID_MOVED = "    if (i->domain.vid != i->shown_vid) {\n        moved |= kept;\n    }\n"
ADVERTISE = ("        if (i->admitted[n]) {\n            used += slope;\n            advertise |= bit;\n"
             "        }\n")
#: the attach's clear of the record an earlier composition left (#936), as ctrl_app_srp.c holds it.
ATTACH_CLEARS = ("        // a recomposed application keeps no record of the SRP instance it attached before (#936)\n"
                 "        app->srp_noticed = 0u;\n")
#: the SRP delivery's take of each interface's record (#936), as ctrl_app_srp.c holds it.
TAKE = ("    for (unsigned interface = 0; interface < MBX_N_IF; ++interface) {\n"
        "        noticed = noticed || app->srp->ifs[interface].noticed != 0u;\n"
        "        app->srp_noticed |= app->srp->ifs[interface].noticed;\n"
        "        app->srp->ifs[interface].noticed = 0u;\n    }\n")
#: the SRP delivery's report of the record it took as owed output (#936; ctrl_loop.h, the polls).
OWED = "    bool pending = noticed;\n"
#: what a source's STREAM_OUTPUT shows of its Listener's registration and its record of a change (#957), as srp_mbx.c
#: holds them: the comparison, the indication's copy of the declaration, the observer's and the reset's comparisons.
SHOWN = "    const uint8_t shown = i->listener_present[n] ? i->declaration[n] : 0u;\n"
CHANGED = "    if (shown != i->shown_registration[n]) {\n"
RECORDED = "        i->registration_noticed |= 1u << n;\n"
COPIED = "            i->declaration[n] = (uint8_t)declaration;\n            show_registration(i,n);\n"
OBSERVED = ("            i->listener_present[n] = t->reg_to != MRP_REG_STATE_MT;\n"
            "            show_registration(i,n);\n")
RESET_SHOWN = ("    for (unsigned k = 0; k < CTRL_SRP_SOURCES; ++k) {\n        show_registration(i,k);\n    }\n"
               "    withdraw_declared(i->index);\n")


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every Talker declaration defect, built with srp_mutants.Defect: the declarations', then the entry's and the
    stream_id's, in that order."""
    return declaration_defects(kind) + entry_defects(kind) + notice_defects(kind)


def planter(kind: Callable[..., T]) -> Callable[..., T]:
    """The defect builder the tables use: one defect, its suite read off its test's name, planted at 8x8/2if by the
    two-interface campaign."""
    def d(name: str, test: str, old: str, new: str, needle: str, path: str = "srp/srp_mbx.c") -> T:
        """One defect, its suite read off its test's name, planted at 8x8/2if by the two-interface campaign."""
        return kind(name, test, old, new, needle, path=path, suite=COMPOSED if test.startswith("SrpGate.") else SUITE,
                    entity=ENTITY)
    return d


def declaration_defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """The declarations' defects: validity, the lapse, the hold-off, the admission's swap, the withdrawal's Leave and
    THE TRANSMIT's publications (srp_mbx.c)."""
    d = planter(kind)
    return (
        d("talker-declared-while-not-valid", VALID, DECLARES, DECLARES.replace("if (valid && !waits", "if (!waits"),
          "a source whose SRP parameters are not valid declares nothing"),
        d("talker-lapse-kept", LAPSE, WITHDRAWS,
          "        if ((i->talkers & bit) != 0u && (i->readdressed & bit) != 0u) {\n",
          "a source whose parameters lapse withdraws its Talker"),
        d("talker-lapse-ignored-by-the-entry", PROBE, "        bool changed = valid != i->gate;\n",
          "        bool changed = (valid & ~i->gate) != 0u;\n", "the probe's 15 s expiry withdraws the Talker"),
        d("talker-unchanged-held", AGAIN, WAITS,
          "        const bool waits = m->held_cs[n] != 0u;\n", "an unchanged destination is declared again at once"),
        d("talker-hold-off-skipped", CHANGED, "                m->held_cs[n] = SRP_REDECLARE_CS;\n",
          "                m->held_cs[n] = 1u;\n",
          "no Talker of a changed destination is declared before the hold-off ends"),
        d("talker-lapse-starts-no-hold-off", LOST, "                m->held_cs[n] = SRP_REDECLARE_CS;\n",
          "                m->held_cs[n] = (i->readdressed & bit) != 0u ? SRP_REDECLARE_CS : 0u;\n",
          "a changed destination waits two of the longest LeaveAll periods less its terms after the Leave"),
        d("talker-hold-off-one-leaveall", CHANGED, REDECLARE,
          REDECLARE.replace("2u * SRP_LEAVEALL_LONGEST_CS", "SRP_LEAVEALL_LONGEST_CS"),
          "no Talker of a changed destination is declared before the hold-off ends"),
        d("talker-hold-off-two-leavealltime-periods", CHANGED, REDECLARE, TWO_LEAVEALLTIME,
          "no Talker of a changed destination is declared before the hold-off ends"),
        d("talker-hold-off-two-leavealltime-periods-after-a-conflict", LOST, REDECLARE, TWO_LEAVEALLTIME,
          "a changed destination waits two of the longest LeaveAll periods less its terms after the Leave"),
        d("talker-hold-off-adds-its-terms", CHANGED, REDECLARE, ADDED,
          "the changed destination reaches the wire no later than two of the longest LeaveAll periods after the "
          "withdrawal"),
        d("talker-hold-off-adds-its-terms-at-the-latest", LATEST, REDECLARE, ADDED,
          "the changed destination reaches the wire no later than two of the longest LeaveAll periods after the "
          "withdrawal, at the latest"),
        d("talker-hold-off-adds-its-terms-after-a-conflict", LOST, REDECLARE, ADDED,
          "the new range's destination reaches the wire within two of the longest LeaveAll periods of the conflict"),
        d("talker-hold-off-a-centisecond-short", CHANGED, REDECLARE, REDECLARE.replace(" / 10u)", " / 10u - 1u)"),
          "TALKER_DECL holds a changed destination withdrawn while it waits"),
        d("talker-hold-off-takes-its-terms-twice", CHANGED, REDECLARE,
          REDECLARE.replace(" - SRP_JOIN_CS - (CTRL_LOOP_TX_MS + 9u) / 10u)",
                            " - 2u * (SRP_JOIN_CS + (CTRL_LOOP_TX_MS + 9u) / 10u))"),
          "no Talker of a changed destination is declared before the hold-off ends"),
        d("talker-hold-off-drops-the-transmit-term", LATEST, REDECLARE,
          REDECLARE.replace(" - (CTRL_LOOP_TX_MS + 9u) / 10u)", ")"),
          "the changed destination reaches the wire no later than two of the longest LeaveAll periods after the "
          "withdrawal, at the latest"),
        d("talker-hold-off-drops-the-join-and-transmit-terms", CHANGED, REDECLARE,
          "#define SRP_REDECLARE_CS (2u * SRP_LEAVEALL_LONGEST_CS)\n",
          "a changed destination is declared two of the longest LeaveAll periods less a JoinTime and THE "
          "TRANSMIT's term after its Leave's request"),
        d("talker-hold-off-rounds-the-transmit-term-down", LATEST, REDECLARE,
          REDECLARE.replace("(CTRL_LOOP_TX_MS + 9u) / 10u", "CTRL_LOOP_TX_MS / 10u"),
          "the changed destination reaches the wire no later than two of the longest LeaveAll periods after the "
          "withdrawal, at the latest"),
        d("talker-hold-off-never-ends", CHANGED,
          "                if (((i->gate & i->readdressed) >> n & 1u) != 0u) {\n",
          "                if (((i->gate & i->readdressed) >> n & 1u) != 0u && n > CTRL_SRP_SOURCES) {\n",
          "a changed destination is declared once the hold-off ends"),
        d("talker-change-while-valid-unmarked", MOVED,
          "                moved = moved || s->value.dest_mac[b] != (uint8_t)dest;\n",
          "                moved = moved || (s->value.dest_mac[b] != (uint8_t)dest && false);\n",
          "a changed destination withdraws the old destination's Advertise"),
        d("talker-reset-forgets-the-move", RESET, WITHDRAWS,
          "        if ((i->talkers & bit) != 0u && how != SRP_DECLARE_NEW &&\n"
          "            (!valid || (i->readdressed & bit) != 0u)) {\n",
          "the new participants hold a source that moved before the reset"),
        d("talker-decl-kept-at-the-withdrawal", LAPSE,
          "                i->talkers &= ~bit;\n                m->held_cs[n] = SRP_REDECLARE_CS;\n",
          "                m->held_cs[n] = SRP_REDECLARE_CS;\n",
          "TALKER_DECL clears the withdrawn source before its Leave leaves"),
        d("talker-licence-closed-after-the-withdrawal", LAPSE, LICENCE, "",
          "a lapse closes LICENCE before TALKER_DECL drops the source"),
        d("talker-unchanged-declared-again", VALID, DECLARES,
          DECLARES.replace("(i->talkers & bit) == 0u || admitted != was", "true"),
          "a Talker whose parameters did not change is not declared again"),
        d("talker-admission-change-held", ADMIT, WITHDRAWS,
          "        if ((i->talkers & bit) != 0u && (!valid || (i->readdressed & bit) != 0u || admitted != was)) {\n",
          "a swap whose join is refused keeps the declared type"),
        d("talker-swap-keeps-the-old-type", ADMIT, SWAP_LEAVE, "", "the Failed leaves as the Advertise joins"),
        d("talker-swap-leaves-a-failed-only", ADMIT, SWAP_LEAVE,
          SWAP_LEAVE.replace("was ? MSRP_ATTR_TYPE_TALKER_ADV : MSRP_ATTR_TYPE_TALKER_FAILED",
                             "MSRP_ATTR_TYPE_TALKER_FAILED"),
          "an admission lost swaps the Advertise to Talker Failed in place"),
        d("talker-withdrawal-leaves-an-advertise-only", ADMIT,
          "            if (mrp_mad_leave(i->msrp,0,was ? MSRP_ATTR_TYPE_TALKER_ADV : "
          "MSRP_ATTR_TYPE_TALKER_FAILED,&value) != 0) {\n",
          "            if (mrp_mad_leave(i->msrp,0,MSRP_ATTR_TYPE_TALKER_ADV,&value) != 0) {\n",
          "a lapse withdraws a Talker Failed too"),
        d("talker-refused-swap-takes-the-new-type", ADMIT,
          "        i->admitted[n] = advertised && (i->talkers & bit) != 0u;\n",
          "        (void)advertised;\n        i->admitted[n] = admitted && (i->talkers & bit) != 0u;\n",
          "an admission change swaps the type in place at once"),
        d("talker-allocated-unfit-declares-code-2", ADMIT,
          "            value.failure_info[8] = i->sources[n].allocated ? 1 : 2;\n",
          "            value.failure_info[8] = 2;\n",
          "an allocated source whose bandwidth does not fit declares Talker Failed, code 1"),
        d("talker-refused-declaration-forgotten", REFUSED, "    i->sources_owed = !done;\n",
          "    i->sources_owed = false;\n", "a refused declaration is declared again"),
        d("talker-refused-withdrawal-forgotten", WITHDRAWN, LEAVE,
          "            (void)mrp_mad_leave(i->msrp,0,was ? MSRP_ATTR_TYPE_TALKER_ADV : MSRP_ATTR_TYPE_TALKER_FAILED,"
          "&value);\n            i->talkers &= ~bit;\n            m->held_cs[n] = SRP_REDECLARE_CS;\n",
          "a withdrawal lwSRP refused keeps the source declared"),
        d("talker-refused-withdrawal-not-owed", WITHDRAWN, LEAVE, LEAVE.replace("                done = false;\n", ""),
          "the refused withdrawal's Leave leaves once lwSRP takes it"),
        d("talker-transmit-publishes-past-its-terms", TERMS, "    (void)mbx_pub_talker_decl(i->index,i->talkers);\n",
          "    (void)mbx_pub_talker_decl(i->index,i->talkers);\n    (void)mbx_pub_talker_decl(i->index,i->talkers);\n",
          "THE TRANSMIT's call publishes TALKER_DECL at most once a declarations pass"),
    )


def entry_defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """The gate entry's defects, the composition's feed and a Listener's demand (ctrl_app_srp.c), and each source's
    stream_id in SRC_SID (#905; maap_mbx.c, mbx.c)."""
    d = planter(kind)
    return (
        d("talker-gate-before-attach", ENTRY, "    const bool ok = m->loop != NULL && interface < MBX_N_IF;\n",
          "    const bool ok = (m->loop != NULL || m->initialized) && interface < MBX_N_IF;\n",
          "refused before attach"),
        d("talker-gate-reentered", ENTRY, ENTRY_GUARD,
          ENTRY_GUARD.replace("    if (!enter(m)) {\n        return false;\n    }\n", ""), "reentry is refused"),
        d("talker-gate-past-the-sources", ENTRY, "        valid &= (1u << CTRL_SRP_SOURCES) - 1u;\n", "",
          "a mask bit past the sources is no source"),
        d("talker-gate-repeat-ignores-its-base", MOVED,
          "if (i->gate_seen && valid == i->gate && base == i->gate_base) {", "if (i->gate_seen && valid == i->gate) {",
          "a changed destination withdraws the old destination's Advertise"),
        d("talker-gate-not-fed", PROBE, FEED, "", "a probe declares the source's Talker on its own interface",
          path=APP),
        d("talker-gate-of-another-range", PROBE, FEED, FEED.replace(".core.base);", ".core.base + 1u);"),
          "with MAAP's base + n", path=APP),
        d("talker-listener-demand-not-forwarded", LISTENER,
          "app->srp->ifs[interface].listener_present[source]", "false",
          "a registered Listener keeps the Talker past the probe window", path=APP),
        d("talker-sid-unwritten-at-start", SID_OPENS, SID_START, "\t\t\t(void)id;\n\t\t\t(void)k;\n",
          "SRC_SID holds the source's stream_id when its DA_GATE bit opens", path=MAAP),
        d("talker-sid-words-swapped", SID_OPENS,
          "(high ? MBX_PUB_SRC_REG_SRC_SID_HI : MBX_PUB_SRC_REG_SRC_SID_LO)",
          "(high ? MBX_PUB_SRC_REG_SRC_SID_LO : MBX_PUB_SRC_REG_SRC_SID_HI)",
          "SRC_SID_LO holds the stream_id's low word and SRC_SID_HI its high word", path="mbx/mbx.c"),
        d("talker-sid-never-held", SID_CHANGED,
          "\tuint32_t may = gate & (m->published_gate[interface] | m->sid_written);\n",
          "\tuint32_t may = gate;\n", "SRC_SID holds the source's stream_id when its DA_GATE bit opens", path=MAAP),
        d("talker-sid-opens-before-its-high-word", SID_AGAIN, SID_LOW,
          SID_LOW + "\tm->sid_written |= (uint16_t)(UINT32_C(1) << s);\n",
          "SRC_SID is written only while the source's DA_GATE bit is clear", path=MAAP),
        d("talker-sid-written-mark-kept", SID_AGAIN, "\tm->sid_written &= (uint16_t)~may;\n", "",
          "both SRC_SID words are written again between the bit's closing and its reopening", path=MAAP),
    )


def notice_defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """What a source's STREAM_OUTPUT GET_STREAM_INFO notice is raised from (#936; Milan v1.2 5.4.5.2, Table 5.22):
    declare_sources' record of each declaration, withdrawal, type swap and VID change against what was last shown
    (srp_mbx.c), and the SRP delivery's take of it (ctrl_app_srp.c)."""
    d = planter(kind)
    return (
        d("talker-notice-declaration-missed", NOTICED, NOTICE_MOVED,
          NOTICE_MOVED.replace("(i->talkers ^ i->shown)", "(i->shown & ~i->talkers)"), "a declaration is noticed"),
        d("talker-notice-withdrawal-missed", NOTICED, NOTICE_MOVED,
          NOTICE_MOVED.replace("(i->talkers ^ i->shown)", "(i->talkers & ~i->shown)"), "a withdrawal is noticed"),
        d("talker-notice-record-dropped", NOTICED, "    i->noticed |= moved;\n", "    (void)moved;\n",
          "a declaration is noticed"),
        d("talker-notice-every-declared-source", SWAP_NOTICED, "    i->noticed |= moved;\n",
          "    i->noticed |= moved | i->talkers;\n", "a Talker Failed withdrawn is noticed"),
        d("talker-notice-swap-missed", SWAP_NOTICED, NOTICE_MOVED, "    uint32_t moved = (i->talkers ^ i->shown);\n",
          "a type swapped in place is noticed"),
        d("talker-notice-refused-swap-noticed", SWAP_NOTICED, ADVERTISE,
          "        if (i->admitted[n]) {\n            used += slope;\n        }\n"
          "        if (admitted && (i->talkers & bit) != 0u) {\n            advertise |= bit;\n        }\n",
          "a swap lwSRP refuses is not noticed until it is made"),
        d("talker-notice-vid-missed", VID_NOTICED, VID_MOVED, "", "a declared Talker carrying another VID is noticed"),
        d("talker-notice-vid-on-every-domain", VID_NOTICED, VID_MOVED,
          VID_MOVED.replace("if (i->domain.vid != i->shown_vid) {", "if (i->domain.vid != i->shown_vid || how == "
                                                                     "SRP_DECLARE_EVERY) {"),
          "a Domain that keeps the VID notices nothing"),
        d("talker-notice-reset-forgets-what-was-shown", RESET_NOTICED, "    withdraw_declared(i->index);\n",
          "    withdraw_declared(i->index);\n    i->shown = 0u;\n",
          "a source a reset declares again unchanged is not noticed"),
        d("talker-notice-not-taken", TAKEN, TAKE, "", "a probe's declaration notices its source", path=APP),
        d("talker-notice-kept-across-a-recomposition", TAKEN, ATTACH_CLEARS, "",
          "an attached SRP instance starts with no record", path=APP),
        d("talker-notice-record-kept", TAKEN, TAKE,
          TAKE.replace("        app->srp->ifs[interface].noticed = 0u;\n", ""), "the SRP delivery takes SRP's record",
          path=APP),
        d("talker-notice-owed-unreported", TAKEN_PASS, OWED, "    bool pending = false;\n    (void)noticed;\n",
          "owes its notice", path=APP),
        # #957: a Listener registration change of a source's stream, what its STREAM_OUTPUT shows of it
        d("talker-registration-unrecorded", REGISTRATION, RECORDED, "", "a Listener Ready appearing is noticed"),
        d("talker-registration-unchanged-recorded", REGISTRATION, CHANGED, "    if (true) {\n",
          "a Listener registered again after a LeaveAll is not noticed"),
        d("talker-registration-presence-only", REGISTRATION, SHOWN,
          "    const uint8_t shown = i->listener_present[n] ? 1u : 0u;\n",
          "a Listener Ready Failed replacing a Ready is noticed"),
        d("talker-registration-declaration-only", REGISTRATION, SHOWN, "    const uint8_t shown = i->declaration[n];\n",
          "a reset with a Listener registered notices it going"),
        d("talker-registration-declaration-uncopied", REGISTRATION, COPIED, "            show_registration(i,n);\n",
          "a Listener Ready appearing is noticed"),
        d("talker-registration-indication-uncompared", REGISTRATION, COPIED,
          "            i->declaration[n] = (uint8_t)declaration;\n",
          "a Listener Ready Failed replacing a Ready is noticed"),
        d("talker-registration-observer-uncompared", REGISTRATION, OBSERVED,
          "            i->listener_present[n] = t->reg_to != MRP_REG_STATE_MT;\n",
          "a Listener Ready appearing is noticed"),
        d("talker-registration-reset-uncompared", REGISTRATION, RESET_SHOWN, "    withdraw_declared(i->index);\n",
          "a reset with a Listener registered notices it going"),
    )
