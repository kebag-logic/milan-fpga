# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""adp_first_mutants.py - planted defects in the first ENTITY_AVAILABLE after a link-up (#970; test_adp.cpp G1
to G5): Milan's draws, 0 to 4 s on LINK_UP and 0 to 2 s at a startup, each spread over its range (IEEE
1722.1-2021 6.2.4.2.2); a grandmaster change in DELAY that re-arms nothing, one in WAITING announced after its own
0 to 4 s draw; available_index kept across a link loss (Milan v1.2 5.6.3.5.2, 5.6.3.5.3, 5.6.3.5.7, Table 5.51;
IEEE 1722.1-2021 6.2.2.15). The first three are the walk's and the stack's, with the G kills added.
ctrl_mutants.py appends this table to its own.
"""

from __future__ import annotations

from ctrl_mutant import ADP_C, Mutant

#: The draw's range by kind (tsn-c-stack adp.c draw_ms).
DRAW_RANGE = "kind == ADP_DRAW_STARTUP ? ADP_DELAY_STARTUP_MAX_MS : ADP_DELAY_MAX_MS"
#: GM_CHANGE in WAITING (Milan v1.2 5.6.3.5.7).
GM_WAITING = ("\tif (a->enabled && a->state == ADP_STATE_WAITING) {\n"
              "\t\tenter_delay(a, ADP_DRAW_DELAY);                         // Milan v1.2 5.6.3.5.7\n\t}\n")
G1 = "AdpFirstAvailable.G1G5WithinTheLinkUpDrawOfEveryLinkUp"
G2 = "AdpFirstAvailable.G2WithinTheStartupDraw"
G3 = "AdpFirstAvailable.G3AGrandmasterChangeBeforeItIsCarriedByIt"
G4 = "AdpFirstAvailable.G4AGrandmasterChangeAfterItIsAnnounced"
SPREAD = "G1 the LINK_UP delay is spread over 0 to 4 s"

MUTANTS: tuple[Mutant, ...] = (
    Mutant("gm-change-ignored", ADP_C, GM_WAITING,
           "\tif (a->enabled && a->state == ADP_STATE_WAITING) {\n\t\t(void)0;\n\t}\n",
           "walk", "Table551/AdpWalkCell.Graded/GM_CHANGE_x_WAITING", "GM_CHANGE x WAITING",
           also=(("adp", G4, "G4 a grandmaster change after the first ENTITY_AVAILABLE starts a delay at once"),)),
    Mutant("link-up-draws-startup-kind", ADP_C,
           ("\t\tif (a->state == ADP_STATE_DOWN) {\n"
            "\t\t\tenter_delay(a, ADP_DRAW_DELAY);                 // Milan v1.2 5.6.3.5.3\n\t\t}\n"),
           ("\t\tif (a->state == ADP_STATE_DOWN) {\n"
            "\t\t\tenter_delay(a, ADP_DRAW_STARTUP);               // Milan v1.2 5.6.3.5.3\n\t\t}\n"),
           "walk", "Table551/AdpWalkCell.Graded/LINK_UP_x_DOWN", "LINK_UP x DOWN", also=(("adp", G1, SPREAD),)),
    Mutant("draw-kinds-merged", ADP_C, DRAW_RANGE, "ADP_DELAY_MAX_MS", "adp", "AdpCore.A9DrawKinds",
           "A9 every startup draw",
           also=(("adp", G2, "G2 the first ENTITY_AVAILABLE, index 0, leaves within its 0 to 2 s draw"),)),
    # #970, R888-1-F1: a LINK_UP delay narrowed to 0 to 0.5 s is not Milan's draw (the ruling on #970)
    Mutant("link-up-draws-half-a-second", ADP_C, DRAW_RANGE,
           "kind == ADP_DRAW_STARTUP ? ADP_DELAY_STARTUP_MAX_MS : ADP_DELAY_MAX_MS / 8u", "adp", G1, SPREAD),
    Mutant("first-delays-not-drawn", ADP_C, "\tuint32_t ms = (r16 * (max_ms + 1u)) >> 16;\n",
           "\tuint32_t ms = kind == ADP_DRAW_DELAY ? (r16 * (max_ms + 1u)) >> 16 : 0u;\n", "adp", G2,
           "G2 the startup delay is spread over 0 to 2 s"),
    Mutant("gm-change-in-delay-restarts-the-delay", ADP_C,
           "\tif (a->enabled && a->state == ADP_STATE_WAITING) {\n\t\tenter_delay(a, ADP_DRAW_DELAY);",
           "\tif (a->enabled && a->state != ADP_STATE_DOWN) {\n\t\tenter_delay(a, ADP_DRAW_DELAY);",
           "adp", G3, "G3 a grandmaster change before the first ENTITY_AVAILABLE re-arms nothing"),
    Mutant("gm-change-draws-the-startup-kind", ADP_C, GM_WAITING,
           GM_WAITING.replace("enter_delay(a, ADP_DRAW_DELAY);       ", "enter_delay(a, ADP_DRAW_STARTUP);     "),
           "adp", G4, "G4 the grandmaster change's delay is the 0 to 4 s draw"),
    Mutant("link-loss-resets-the-index", ADP_C,
           ("\t\ttimer_stop(a);                                          // Milan v1.2 5.6.3.5.6 / 5.6.3.5.10\n"
            "\t\ta->available_owed = false;\n"),
           ("\t\ttimer_stop(a);                                          // Milan v1.2 5.6.3.5.6 / 5.6.3.5.10\n"
            "\t\ta->available_owed = false;\n\t\ta->available_index = 0;\n"),
           "adp", G1, "G1 each ENTITY_AVAILABLE carries the next available_index, across every link-up"),
)
