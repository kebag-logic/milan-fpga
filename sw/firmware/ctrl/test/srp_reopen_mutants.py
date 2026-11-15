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
MIRROR = "JointLinkChangeBuildsInterfaceOneBesideAWithdrawal"
TURN_RULE = "        if (!i->msrp && (built || (n != turn && turn_due))) {\n"


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
        # no deferral: every interface due builds in the poll (with the turn read as the poll starts, `built` alone
        # never defers at two interfaces: the turn rule defers the other one)
        kind("joint-reset-builds-both", JOINT, TURN_RULE, TURN_RULE.replace(" {\n", " && false) {\n").replace(
             "(!i->msrp && ", "((!i->msrp && "), "a pass builds one interface at most", suite="srp_app.cpp"),
        kind("build-turn-ignored", JOINT, TURN_RULE, TURN_RULE.replace("turn_due))", "turn_due && false))"),
             "the interface whose turn it is is built first", suite="srp_app.cpp"),
        kind("build-turn-not-moved", JOINT, "            m->build_turn = (n + 1u) % MBX_N_IF;\n", "",
             "the interface whose turn it is is built first", suite="srp_app.cpp"),
        kind("build-waits-beside-a-withdrawal", JOINT,
             "    return !turn->msrp && !turn->reopen_polls && turn->link == link[t];\n",
             "    return !turn->msrp && turn->link == link[t];\n",
             "an interface due beside one still withdrawing is built at once", suite="srp_app.cpp"),
        # the turn interface's state read during the visits: visited first, it has spent its withdrawal
        kind("build-turn-read-after-its-visit", MIRROR, TURN_RULE,
             TURN_RULE.replace("turn_due))", "(turn_due || turn_builds(m, links))))"),
             "interface 1, due beside interface 0 still withdrawing with the turn, is built at once",
             suite="srp_app.cpp"),
        kind("reset-keeps-listener-present", "InterfaceResetClearsListenerPresent",
             "        i->listener_present[k] = false;\n    }\n    publish_licence(i);\n",
             "    }\n    publish_licence(i);\n", "the interface reset clears listener_present"),
        kind("reset-each-edge-builds", "LinkEdgesOfOnePassBuildOnce", DESTROY,
             DESTROY + "    (void)open_interface(i); msrp_app_destroy(i->msrp); mvrp_app_destroy(i->mvrp);\n"
             "    i->msrp = NULL; i->mvrp = NULL;\n",
             "a pass of link edges builds once", suite="srp_app.cpp"),
    )
