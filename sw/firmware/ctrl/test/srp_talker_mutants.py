# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of SRP's Talker declarations as the validity of each source's SRP parameters moves them (#895).

srp_mutants.py plants each into a copy of sw/firmware/ctrl with the rest of its table, and the named test must fail on
its own words: srp_talker.cpp's (SRP alone) or test_acmp_mbx.cpp's SrpGate (the composition: ACMP's probe and its 15 s
window, SRP's Listener registration, MAAP's DA gate and a range MAAP loses). The two-interface campaign plants them at
8x8/2if (ENTITY), the one-interface campaign at 1x1/1if (test_ctrl_firmware.run_srp_mutants selects them by name). One
defect a rule: a source declares only while valid (Milan v1.2 4.3.3.1, 5.3.7.4) and at once; a lapse withdraws, its
licence and TALKER_DECL bit first; an unchanged destination comes back at once and a changed one no sooner than two
LeaveAllTime periods after the Leave (IEEE 802.1Q-2018 35.2.2.8, Table 10-7), whether it changed while declared or
while lapsed, and held across a reset; an admission change swaps in place; a refused declaration is declared again;
a withdrawal lwSRP refuses keeps the source declared and owed until lwSRP takes its Leave; THE TRANSMIT's call publishes
within srp_bounds.h's terms; the entry refuses before attach and on reentry; and the composition feeds each interface's
DA gate and range. The source's frames carry the stream_id its Talker declares (#905): the MAAP adapter writes each
source's SRC_SID before its DA_GATE bit first opens, each word in its own register, again before each reopening,
read from the source port, and only while the bit is clear (KL_mbx_pkg.sv SRC_SID_LO).
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
CHANGED = "Talker.ChangedDestinationWaitsTwoLeaveAllTimePeriods"
MOVED = "Talker.DestinationChangeWhileValidWithdrawsTheOld"
ADMIT = "Talker.AdmissionChangeSwapsTheTypeInPlace"
RESET = "Talker.ResetKeepsAnUnchangedSourceAndHoldsAMovedOne"
ENTRY = "Talker.GateEntryRecordsOnlyWhatChanged"
REFUSED = "Talker.RefusedDeclarationIsDeclaredAgain"
TERMS = "Talker.TransmitPublishesWithinItsTermsAfterARefusedJoin"
WITHDRAWN = "Talker.RefusedWithdrawalIsWithdrawnOnceLwsrpTakesIt"
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


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every Talker declaration defect, built with srp_mutants.Defect."""
    def d(name: str, test: str, old: str, new: str, needle: str, path: str = "srp/srp_mbx.c") -> T:
        """One defect, its suite read off its test's name, planted at 8x8/2if by the two-interface campaign."""
        return kind(name, test, old, new, needle, path=path, suite=COMPOSED if test.startswith("SrpGate.") else SUITE,
                    entity=ENTITY)
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
          "a changed destination waits two LeaveAllTime periods after the Leave"),
        d("talker-hold-off-one-leaveall", CHANGED, "#define SRP_REDECLARE_CS (2u * 1000u + SRP_JOIN_CS",
          "#define SRP_REDECLARE_CS (1000u + SRP_JOIN_CS",
          "no Talker of a changed destination is declared before the hold-off ends"),
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
        d("talker-gate-before-attach", ENTRY, "    const bool ok = m->loop != NULL && interface < MBX_N_IF;\n",
          "    const bool ok = (m->loop != NULL || m->initialized) && interface < MBX_N_IF;\n",
          "refused before attach"),
        d("talker-gate-reentered", ENTRY, ENTRY_GUARD,
          ENTRY_GUARD.replace("    if (!enter(m)) {\n        return false;\n    }\n", ""), "reentry is refused"),
        d("talker-gate-past-the-sources", ENTRY, "        valid &= (1u << CTRL_SRP_SOURCES) - 1u;\n", "",
          "a mask bit past the sources is no source"),
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
