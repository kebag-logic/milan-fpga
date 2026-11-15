# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""maap_gate_mutants.py - planted defects in the MAAP destination-address gate
and the ACMP demand behind it (#665): the query outside MAAP's callbacks, the
composition's owner and idle tick, the freshness interval, each arm of the
gate's predicate, its source validity and its expiry.
ctrl_mutants.py appends this table to its own.
"""

from __future__ import annotations

from ctrl_mutant import ACMP_C, Mutant

MUTANTS = (
    Mutant("f3b-query-inside-allocation", "maap/maap_mbx.c",
           "m->published_gate[interface] = declaring(m, interface, count, valid);",
           "refresh_demand(m); m->published_gate[interface] = declaring(m, interface, count, valid);",
           "maap", "MaapHost.DaGateIsPublishedBeforeEachAllocationIsReported",
           "declaration query stays outside MAAP callbacks"),
    Mutant("f3b-composition-owner", "app/ctrl_app.c",
           "cfg->acmp != NULL ? &app->acmp.acmp : NULL", "NULL",
           "acmp", "AcmpMailbox.F3bComposedGateExpiresAfterIdleTickWake",
           "composed mailbox publishes the accepted probe demand"),
    Mutant("f3b-idle-tick", "app/ctrl_app.c",
           "mbx_tick_enable(true);", "mbx_tick_enable(false);",
           "acmp", "AcmpMailbox.F3bComposedGateExpiresAfterIdleTickWake",
           "service tick wakes an idle platform for freshness expiry"),
    Mutant("f3b-config-interval", "acmp/acmp_mbx.c",
           "config.da_fresh_ms = 15000u;", "config.da_fresh_ms = 0u;",
           "acmp", "AcmpMailbox.F3bComposedGateExpiresAfterIdleTickWake",
           "mailbox composition supplies the Milan freshness interval"),
    Mutant("f3b-fresh-probe-arm", ACMP_C,
           "s->answered || s->listener_registered", "false || s->listener_registered",
           "maap", "MaapHost.DaGateFreshProbeDeclaresOnlyItsSource",
           "fresh probe opens only its configured source"),
    Mutant("f3b-listener-arm", ACMP_C,
           "s->answered || s->listener_registered", "s->answered || false",
           "maap", "MaapHost.DaGateListenerDeclaresWithoutProbe",
           "registered Listener opens the gate without a probe"),
    Mutant("f3b-no-demand-arm", ACMP_C,
           "s->answered || s->listener_registered", "s->answered || s->listener_registered || true",
           "maap", "MaapHost.DaGateWithoutDemandStaysClosed",
           "neither probe nor Listener keeps the gate closed"),
    Mutant("f3b-source-validity", "maap/maap_mbx.c",
           "if (acmp_declaring(m->acmp, s)) {",
           "(void)acmp_declaring(m->acmp, s);\n"
           "\t\t\tif (m->acmp->sources[s].answered || m->acmp->sources[s].listener_registered) {",
           "acmp", "AcmpMailbox.F3bListenerRequiresSourceDestination",
           "published source predicate includes destination validity and interface",
           (("acmp", "AcmpMailbox.F3bProbeRequiresSourceDestination",
             "published source predicate includes destination validity and interface"),
            ("acmpif2", "AcmpMailbox.F3bListenerRequiresSourceDestination",
             "published source predicate includes destination validity and interface"),
            ("acmpif2", "AcmpMailbox.F3bProbeRequiresSourceDestination",
             "published source predicate includes destination validity and interface"),
            ("maap", "MaapHost.DaGateWaitsForSourceOwnerAfterAllocation",
             "allocation report cannot replace source destination validity"))),
    Mutant("f3b-expiry-arm", ACMP_C,
           ">= a->cfg.da_fresh_ms", "> a->cfg.da_fresh_ms",
           "maap", "MaapHost.DaGateProbeExpiresAtFifteenSeconds",
           "probe expires at 15000 milliseconds without a Listener"),
    Mutant("f3b-expiry-refresh", "maap/maap_mbx.c",
           "if (gate != m->published_gate[k])", "if (gate != m->published_gate[k] && gate != 0u)",
           "maap", "MaapHost.DaGateProbeExpiresAtFifteenSeconds",
           "probe expires at 15000 milliseconds without a Listener"),
)
