# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the retained receive's retry rule (#665, srp_mbx.c's poll): a refused record is retried only once
a pool returned a block or lwSRP reported an Applicant or Registrar change of its interface since its refusal, at most
once a centisecond, and with nothing changed its deadline is checked as the refusal a retry would meet checks it.

srp_mutants.py plants them with the rest of its table: each must fail its named observable, never only a build.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

RULE = "SrpRetry.RefusedRecordIsRetriedOnlyAfterAChangeAndAtMostOnceACentisecond"
ALONE = "SrpRetry.AnAttributeChangeAloneAllowsTheRetry"
DEADLINE = "SrpRetry.NothingChangedStillExpiresAtTheDeadline"
#: The poll's test of what the refusal depends on.
SEEN = "            if (!i->moved && ctrl_pool_returned == m->pending_freed) {\n                expire_receive(m);\n"
#: What a refusal saw (apply_receive).
SAW = "        i->moved = false;\n        m->pending_freed = ctrl_pool_returned;\n"


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect of the retained receive's retry rule, built with srp_mutants.Defect."""
    return (
        # a retry with nothing changed: every centisecond, as if the refusal could have turned
        kind("retry-without-a-change", RULE, SEEN, SEEN.replace("!i->moved && ctrl_pool_returned == m->pending_freed",
                                                                "false"),
             "a retry with neither the pool nor an attribute changed", suite="srp_rx_retry.cpp"),
        # no retry after a change: the record waits for its deadline
        kind("no-retry-after-a-change", RULE, SEEN, SEEN.replace("!i->moved && ctrl_pool_returned == m->pending_freed",
                                                                 "true"),
             "the retry a change allows", suite="srp_rx_retry.cpp"),
        # every pass a change allows retries, no centisecond between
        kind("retry-every-pass", RULE, "                m->retry_spent = true;\n", "",
             "at most one retry a centisecond", suite="srp_rx_retry.cpp"),
        # no centisecond ever given: one retry, then none
        kind("retry-tick-never-set", RULE, "    m->retry_spent = false;\n    // lwSRP arms", "    // lwSRP arms",
             "a refused record is taken on the first pass after the pool frees", suite="srp_rx_retry.cpp"),
        # a returned block not counted: the pool's freeing allows no retry
        kind("pool-return-uncounted", RULE, "\t\tctrl_pool_returned++;\n", "", "the retry a change allows",
             path="port/ctrl_pool.c", suite="srp_rx_retry.cpp"),
        # an Applicant's or a Registrar's change not counted
        kind("attribute-change-uncounted", ALONE, "    i->moved = true;\n", "",
             "every Applicant or Registrar change lwSRP reports is marked", suite="srp_rx_retry.cpp"),
        # a refusal's own Applicant and Registrar changes read as a change since it
        kind("refusal-moves-unrecorded", RULE, SAW, SAW.replace("        i->moved = false;\n", ""),
             "a retry with neither the pool nor an attribute changed", suite="srp_rx_retry.cpp"),
        # a refusal's own returned blocks read as a change since it
        kind("refusal-returns-unrecorded", RULE, SAW,
             SAW.replace("        m->pending_freed = ctrl_pool_returned;\n", ""),
             "a retry with neither the pool nor an attribute changed", suite="srp_rx_retry.cpp"),
        # with nothing changed the deadline is not checked: the record waits past it
        kind("unchanged-deadline-unchecked", DEADLINE, SEEN, SEEN.replace("expire_receive(m);", "(void)m;"),
             "the deadline holds with nothing changed", suite="srp_rx_retry.cpp"),
    )
