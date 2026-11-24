# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The sink index (#977, its ruling of 2026-11-23, item 5; srp_mbx.c index_sinks): every bound sink in the lane of its
StreamID's last byte, rebuilt by every binding, which a Talker's indication, the receive filter, the kept count and the
walk look a StreamID's sinks up in, and the walk a Listener declaration owes only where a source talks its StreamID.
Each defect and the test whose words must fail on it; both hold at every shape, so test_ctrl_firmware.py plants them
in every SRP campaign."""
from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")
#: The name every defect here starts with.
PREFIX = "srp-lane-"
LANE = "Srp.EveryBindingInASinkLaneTakesItsOwnStreamsTalkersAlone"
#: Each lookup's visit of its lane: the indication's, the filter's, the kept count's and the walk's.
INDICATION = ("    for (unsigned n = i->lane_first[last % SRP_SINK_LANES]; n != 0u; n = i->lane_next[n - 1u]) {\n"
              "        const unsigned k = n - 1u;\n")
FILTER = ("        for (unsigned n = i->lane_first[id[7] % SRP_SINK_LANES]; n != 0u; n = i->lane_next[n - 1u]) {\n"
          "            if (i->sinks[n - 1u].stream_id.bytes[7] == id[7] && same(")
COUNT = ("    for (unsigned n = i->lane_first[id[7] % SRP_SINK_LANES]; n != 0u; n = i->lane_next[n - 1u]) {\n"
         "        if (same(i->sinks[n - 1u].stream_id.bytes,id,8)) {\n")
WALK = ("        for (unsigned n = i->lane_first[last % SRP_SINK_LANES]; n != 0u; n = i->lane_next[n - 1u]) {\n"
        "            struct srp_sink *sink = &i->sinks[n - 1u];\n")
#: A Listener declaration's walk, owed only where a source talks its StreamID (prepare_declarations), and the whole
#: block that owes it, which srp_mutants.py's own-listener-declaration-not-copied removes.
DECLARED = "            i->stale = i->stale || sources_of(i,s->stream_id.bytes) != 0u;\n"
DECLARATION = ("        if (desired != s->declared) {\n"
               "            // A declaration rewrites the value of the attribute a registration shares (#665), "
               "which the walk copies\n"
               "            // only for a source of its StreamID (registrations, sources_of): one of a StreamID "
               "no source talks\n"
               "            // changes nothing the walk copies and owes it none (#977, its ruling of 2026-11-23, "
               "item 5).\n" + DECLARED + "        }\n")
WALKLESS = "Srp.ADeclarationOfAStreamNoSourceTalksOwesNoWalk"
#: A lane's head only: each visit stops at its lane's first sink.
HEAD_ONLY = ("n = i->lane_next[n - 1u]) {", "n = 0u) {")


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect, built with srp_mutants.Defect."""
    return (
        kind(PREFIX + "not-rebuilt", LANE,
             "    index_sinks(i); // the lookups' index of the bindings, this one among them (#977)\n",
             "    (void)index_sinks; // the lookups' index of the bindings, this one among them (#977)\n",
             "c's Advertise registers for its sink"),
        kind(PREFIX + "head-only", LANE, "            i->lane_next[k] = *first;\n",
             "            i->lane_next[k] = 0u;\n", "the walk finds c's Advertise for its lane's second"),
        kind(PREFIX + "indication-head-only", LANE, INDICATION, INDICATION.replace(*HEAD_ONLY),
             "c's Failed replaces its Advertise at its lane's second"),
        kind(PREFIX + "filter-head-only", LANE, FILTER, FILTER.replace(*HEAD_ONLY),
             "the filter keeps no Talker of a bound StreamID"),
        kind(PREFIX + "count-head-only", LANE, COUNT, COUNT.replace(*HEAD_ONLY),
             "the count before a's receive keeps no Talker of a bound StreamID"),
        kind(PREFIX + "walk-head-only", LANE, WALK, WALK.replace(*HEAD_ONLY),
             "the walk finds c's Advertise for its lane's second"),
        kind(PREFIX + "declaration-walks-always", WALKLESS, DECLARED, "            i->stale = true;\n",
             "a declaration of a StreamID no source talks owes no walk"),
    )
