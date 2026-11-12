# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of SRP's Talker declarations as MAAP's allocation moves them (#895).

srp_mutants.py plants each into a copy of sw/firmware/ctrl with the rest of its table, and the named test of
srp_talker.cpp must fail on its own words. The two-interface campaign plants them at 8x8/2if (ENTITY) and the
one-interface campaign at 1x1/1if (their names are in test_ctrl_firmware.run_srp_mutants's selection). One defect a
rule: a moved Talker withdraws (IEEE 802.1Q-2018 35.2.2.8), and declares again no sooner than two LeaveAllTime periods
after (Table 10-7), held across a reset, from its withdrawal and not from a later report; TALKER_DECL clears before
the Leave and the licence closes before it; a loss leaves no destination and a source past the count none; an
unchanged Talker is not declared again; an admission change withdraws; an allocated source that does not fit
declares code 1; a refused declaration is declared again; and the entry refuses before attach and on reentry.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

SUITE = "srp_talker.cpp"
#: The two-interface campaign's entity for these defects: 8x8/2if.
ENTITY = "endstation_ax7101_8x8"
ALLOCATE = "Talker.AllocationWithdrawsTheFailedThenAdvertisesTheDestination"
LOSE = "Talker.LossWithdrawsTheAdvertiseAndDeclaresFailedAfterTheHoldOff"
CHANGE = "Talker.ChangeWithdrawsTheOldDestinationAndAdvertisesTheNew"
REALLOCATE = "Talker.ReallocationDuringTheHoldOffAdvertisesTheLatest"
ADMIT = "Talker.AdmissionChangeWithdrawsAndAdvertisesAfterTheHoldOff"
RESET = "Talker.MoveBeforeAResetIsHeldByTheNewParticipants"
ENTRY = "Talker.AllocationEntryRecordsOnlyWhatChanged"
REFUSED = "Talker.RefusedRedeclarationIsDeclaredAgain"
#: declare_sources's withdrawal condition and its licence closure, as srp_mbx.c holds them.
WITHDRAWS = "        if ((i->talkers & bit) != 0u && (moved || admitted != i->admitted[n])) {\n"
LICENCE = ("            if (i->active[n]) {\n                i->active[n] = false;\n                ++m->stops;\n"
           "                publish_licence(i);\n                m->config.licence(m->config.ctx,i->index,n,false);\n"
           "            }\n")
ENTRY_GUARD = ("bool srp_mbx_allocation(struct srp_mbx *m, uint32_t sources, uint64_t base, uint16_t count, "
               "bool valid)\n{\n    if (!enter(m)) {\n        return false;\n    }\n")


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every Talker declaration defect, built with srp_mutants.Defect."""
    def d(name: str, test: str, old: str, new: str, needle: str) -> T:
        return kind(name, test, old, new, needle, suite=SUITE, entity=ENTITY)
    return (
        d("talker-moved-not-withdrawn", CHANGE, WITHDRAWS,
          "        if ((i->talkers & bit) != 0u && admitted != i->admitted[n]) {\n",
          "a changed destination withdraws the old destination's Advertise"),
        d("talker-hold-off-skipped", ALLOCATE, "            i->held_cs[n] = SRP_REDECLARE_CS;\n",
          "            i->held_cs[n] = 1u;\n",
          "no Talker of a moved destination is declared before the hold-off ends"),
        d("talker-hold-off-one-leaveall", ALLOCATE, "#define SRP_REDECLARE_CS (2u * 1000u + SRP_JOIN_CS",
          "#define SRP_REDECLARE_CS (1000u + SRP_JOIN_CS",
          "no Talker of a moved destination is declared before the hold-off ends"),
        d("talker-hold-off-never-ends", ALLOCATE,
          "        if (i->held_cs[n] != 0u && --i->held_cs[n] == 0u) {\n            i->sources_owed = true;\n"
          "            hold(i);\n",
          "        if (i->held_cs[n] != 0u && --i->held_cs[n] == 0u) {\n",
          "declares Talker Advertise with the allocated destination once the hold-off ends"),
        d("talker-hold-off-restarted-by-a-report", REALLOCATE, WITHDRAWS,
          "        if (((i->talkers & bit) != 0u || i->held_cs[n] != 0u) && (moved || admitted != i->admitted[n])) {\n",
          "a re-allocated source advertises its newest destination when the hold-off ends"),
        d("talker-reset-forgets-the-move", RESET, WITHDRAWS,
          "        if ((i->talkers & bit) != 0u && how != SRP_DECLARE_NEW && "
          "(moved || admitted != i->admitted[n])) {\n",
          "the new participants hold a source that moved before the reset"),
        d("talker-decl-kept-at-the-withdrawal", ALLOCATE,
          "            i->talkers &= ~bit;\n            i->held_cs[n] = SRP_REDECLARE_CS;\n",
          "            i->held_cs[n] = SRP_REDECLARE_CS;\n",
          "TALKER_DECL clears the withdrawn source before its Leave leaves"),
        d("talker-licence-closed-after-the-withdrawal", LOSE, LICENCE, "",
          "a loss closes LICENCE before TALKER_DECL drops the source"),
        d("talker-loss-kept-allocated", LOSE,
          "            m->allocated = valid && n < count ? m->allocated | bit : m->allocated & ~bit;\n",
          "            m->allocated = (valid || count != 0u) && n < count ? m->allocated | bit : "
          "m->allocated & ~bit;\n",
          "a loss withdraws the source's Talker Advertise"),
        d("talker-past-the-count-allocated", ENTRY,
          "            m->allocated = valid && n < count ? m->allocated | bit : m->allocated & ~bit;\n",
          "            m->allocated = valid && n <= count ? m->allocated | bit : m->allocated & ~bit;\n",
          "a source past the reported count has no destination"),
        d("talker-unchanged-declared-again", ALLOCATE,
          "(how != SRP_DECLARE_CHANGED || (i->talkers & bit) == 0u)",
          "(how != SRP_DECLARE_CHANGED || (i->talkers & bit) != 0u || (i->talkers & bit) == 0u)",
          "a Talker whose destination did not move is not declared again"),
        d("talker-admission-change-kept", ADMIT, WITHDRAWS,
          "        if ((i->talkers & bit) != 0u && moved) {\n",
          "a source whose admission changes withdraws its Talker Failed"),
        d("talker-allocated-unfit-declares-code-2", ADMIT,
          "            value.failure_info[8] = s->allocated ? 1 : 2;\n", "            value.failure_info[8] = 2;\n",
          "an allocated source whose bandwidth does not fit declares Talker Failed, code 1"),
        d("talker-refused-declaration-forgotten", REFUSED, "    i->sources_owed = !done;\n",
          "    i->sources_owed = false;\n", "a refused re-declaration is declared again"),
        d("talker-entry-before-attach", ENTRY, "    const bool ok = m->loop != NULL;\n",
          "    const bool ok = m->loop != NULL || m->initialized;\n", "refused before attach"),
        d("talker-entry-reentered", ENTRY, ENTRY_GUARD, ENTRY_GUARD.replace(
            "    if (!enter(m)) {\n        return false;\n    }\n", ""), "reentry is refused"),
    )
