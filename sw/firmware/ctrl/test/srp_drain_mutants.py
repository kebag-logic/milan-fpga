# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The SRP drain's charge, THE SETTLE's owe and THE TRANSMIT's re-declarations in a pass of their own (#977, its ruling
of 2026-11-23, items 3 and 4): each defect and the test whose words must fail on it. They bite only at the one-interface
shapes, where the registration cost and THE SETTLE are set (ctrl_loop.h, CTRL_LOOP_SRP_REG_US, CTRL_LOOP_SETTLE_ALONE),
so test_ctrl_firmware.py plants them in the one-interface campaigns alone; those named with PREFIX_8X8 only at 8x8/1if,
where CTRL_LOOP_DECLARE_ALONE is set and the kept are bounded below the sinks (V less the bound, SRP_RECORD_VALUES), and
those named with PREFIX_1X1 only at 1x1/1if, where V is past the sinks (#977, its ruling of 2026-11-27, item 2)."""
from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")
#: The name every defect here starts with, and the 8x8/1if-only ones'.
PREFIX = "srp-977-"
PREFIX_8X8 = PREFIX + "8x8-"
PREFIX_1X1 = PREFIX + "1x1-"
POPULATION = "SrpEarlyTalker.AVectorOfBoundAndKeptTalkersRegistersVAndIsChargedForEach"
CHARGE = "Srp.TheDrainChargesARecordTheTalkersItsVectorsCanRegister"
REDECLARE = "Srp.ARedeclarationBuildsItsMrpduInTheNextCallWhereTheShapeSaysSo"
SETTLE = "SrpBinding.ARegistrationIsCompletedAsTheNextOrdinaryPassStarts"
TALKERS = ("while ((type == MSRP_ATTR_TYPE_TALKER_ADV || type == MSRP_ATTR_TYPE_TALKER_FAILED) && "
           "at + 2u <= end) {")


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect, built with srp_mutants.Defect."""
    return (
        kind(PREFIX + "charge-vector-uncapped", CHARGE,
             "values += count < SRP_RECORD_VALUES ? count : SRP_RECORD_VALUES;", "values += count;",
             "a Talker Failed's values past V"),
        kind(PREFIX + "charge-leaveall-ends-the-message", CHARGE,
             "                if (header == 0u) {\n"
             "                    break; // the Message's EndMark\n                }\n"
             "                const unsigned count = mrp_vh_nv((uint16_t)header);\n",
             "                const unsigned count = mrp_vh_nv((uint16_t)header);\n"
             "                if (count == 0u) {\n                    break;\n                }\n",
             "a LeaveAll of no values ahead of two Talker values"),
        kind(PREFIX_1X1 + "charge-vector-at-the-sinks", POPULATION,
             "values += count < SRP_RECORD_VALUES ? count : SRP_RECORD_VALUES;",
             "values += count < CTRL_SRP_SINKS ? count : CTRL_SRP_SINKS;",
             "R1 THE DRAIN charges every Talker the record registers"),
        kind(PREFIX_1X1 + "charge-fallback-at-the-sinks", CHARGE,
             "values += SRP_RECORD_VALUES * ((len - at) / SRP_TALKER_VECTOR_MIN);",
             "values += CTRL_SRP_SINKS * ((len - at) / SRP_TALKER_VECTOR_MIN);", "past eight Messages, by its length"),
        kind(PREFIX_8X8 + "keep-past-v", POPULATION, "    if (*count >= bound) {\n        return false;\n    }\n",
             "    if (*count >= SRP_KEPT_TALKERS) {\n        return false;\n    }\n",
             "R1 the bound and the kept a vector registers fill V"),
        kind(PREFIX_8X8 + "keep-bound-sinks-uncounted", POPULATION, "            ++i->bound_sinks;\n", "",
             "R1 the bound and the kept a vector registers fill V"),
        kind(PREFIX + "charge-every-message", CHARGE, TALKERS, "while (at + 2u <= end) {", "a Listener's"),
        kind(PREFIX + "charge-past-the-endmark", CHARGE, "            if ((type | alen) == 0u) {\n",
             "            if (false) {\n", "a Talker past the EndMark"),
        kind(PREFIX + "charge-every-message-read", CHARGE, "if (messages == SRP_CHARGE_MESSAGES) {",
             "if (messages == SRP_CHARGE_MESSAGES + 1000u) {", "past eight Messages, by its length"),
        kind(PREFIX + "settle-in-the-records-pass", SETTLE,
             "const bool settles = CTRL_LOOP_SETTLE_ALONE && app->loop.drain_taken != 0u;",
             "const bool settles = false;", "the record's pass leaves ACMP's completion owed",
             path="app/ctrl_app_srp.c", suite="test_acmp_mbx.cpp"),
        kind(PREFIX_8X8 + "redeclaration-records-taken", REDECLARE,
             "return m->owed_len == 0 && m->loop->ticks_owed == 0 && !m->declared_alone;",
             "return m->owed_len == 0 && m->loop->ticks_owed == 0;", "no SRP record is taken before the build"),
        kind(PREFIX_8X8 + "redeclaration-built-at-once", REDECLARE,
             "if (k == MBX_N_IF && CTRL_LOOP_DECLARE_ALONE && !declared_alone && m->declarations != 0u) {",
             "if (k == MBX_N_IF && CTRL_LOOP_DECLARE_ALONE && !declared_alone && m->declarations == 255u) {",
             "the call that re-declared builds nothing"),
    )
