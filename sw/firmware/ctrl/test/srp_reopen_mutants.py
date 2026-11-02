# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the SRP adapter's two-pass reset, one interface built a pass (#665, srp_bounds.h, the
share in ctrl_loop.h).

srp_mutants.py plants them with the rest of its table: each must fail its named observable,
never only a build.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

DEFER = "    i->reopen_polls = 1u;\n    i->reopening = true;\n"
OWE = "            --i->reopen_polls;\n            owed = true;\n"
DESTROY = ("    msrp_app_destroy(i->msrp); mvrp_app_destroy(i->mvrp);\n"
           "    i->msrp = NULL; i->mvrp = NULL; i->domain_owed = false;\n")
TEST = "LinkChangeBuildsTheNewParticipantsOnTheNextPass"
JOINT = "JointLinkChangeBuildsOneInterfaceAPass"


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect of the two-pass reset, built with srp_mutants.Defect."""
    return (
        kind("reset-builds-in-its-own-pass", TEST, DEFER,
             "    if (!open_interface(i)) {\n        ++m->refused;\n    }\n",
             "the pass that takes the link change withdraws", suite="srp_app.cpp"),
        kind("reset-builds-a-pass-late", TEST, "    i->reopen_polls = 1u;\n", "    i->reopen_polls = 2u;\n",
             "the next pass's poll builds the new participants", suite="srp_app.cpp"),
        kind("reset-receive-does-not-wait", TEST, "        if (m->ifs[n].reopening) {\n",
             "        if (false && m->ifs[n].reopening) {\n",
             "receive waits until the new participants are built", suite="srp_app.cpp"),
        kind("reset-receive-waits-on", TEST, "        i->reopening = false;\n", "",
             "the record that waited is taken on the pass after", suite="srp_app.cpp"),
        kind("reset-build-not-owed", TEST, OWE, "            --i->reopen_polls;\n",
             "a poll that withdraws owes the build", suite="srp_app.cpp"),
        kind("joint-reset-builds-both", JOINT, "        if (!i->msrp && (built || !builds_first(m,n))) {\n",
             "        if (!i->msrp && false) {\n", "a pass builds one interface at most", suite="srp_app.cpp"),
        kind("build-turn-ignored", JOINT, "    return n == m->build_turn || turn->msrp || turn->reopen_polls;\n",
             "    return true;\n", "the interface whose turn it is is built first", suite="srp_app.cpp"),
        kind("build-turn-not-moved", JOINT, "            m->build_turn = (n + 1u) % MBX_N_IF;\n", "",
             "the interface whose turn it is is built first", suite="srp_app.cpp"),
        kind("build-waits-beside-a-withdrawal", JOINT,
             "    return n == m->build_turn || turn->msrp || turn->reopen_polls;\n",
             "    return n == m->build_turn || turn->msrp;\n",
             "an interface due beside one still withdrawing is built at once", suite="srp_app.cpp"),
        kind("reset-keeps-listener-present", "InterfaceResetClearsListenerPresent",
             "        i->listener_present[k] = false;\n    }\n    publish_licence(i);\n",
             "    }\n    publish_licence(i);\n", "the interface reset clears listener_present"),
        kind("reset-each-edge-builds", "LinkEdgesOfOnePassBuildOnce", DESTROY,
             DESTROY + "    (void)open_interface(i); msrp_app_destroy(i->msrp); mvrp_app_destroy(i->mvrp);\n"
             "    i->msrp = NULL; i->mvrp = NULL;\n",
             "a pass of link edges builds once", suite="srp_app.cpp"),
    )
