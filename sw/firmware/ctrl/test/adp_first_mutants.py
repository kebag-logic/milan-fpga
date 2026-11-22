# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""adp_first_mutants.py - planted defects in the ADP draw an interface makes as it leaves DOWN (#970): the
startup and LINK_UP kinds and their 0 to 0.5 s range, so the first ENTITY_AVAILABLE leaves within 1 s of the
link-up (test_adp.cpp G1 to G5), a grandmaster change in DELAY still ignored, every later delay still drawn from
0 to 4 s, the delay still random and available_index kept across a link loss (Milan v1.2 5.6.3.5.2, 5.6.3.5.3,
5.6.3.5.5 and Table 5.51; IEEE 1722.1-2021 6.2.2.15).
ctrl_mutants.py appends this table to its own.
"""

from __future__ import annotations

from ctrl_mutant import ADP_C, ADP_H, Mutant

#: The draw's range by kind (tsn-c-stack adp.c draw_ms; #970): the startup and LINK_UP draws their own, every other
#: the 0..4 s one.
FIRST_DRAWS = ("\tuint32_t max_ms = ADP_DELAY_MAX_MS;\n\tif (kind == ADP_DRAW_STARTUP) {\n"
               "\t\tmax_ms = ADP_DELAY_STARTUP_MAX_MS;\n\t}\n\tif (kind == ADP_DRAW_LINK_UP) {\n"
               "\t\tmax_ms = ADP_DELAY_LINK_UP_MAX_MS;\n\t}\n")

MUTANTS: tuple[Mutant, ...] = (
    Mutant("link-up-draws-startup-kind", ADP_C,
           ("\t\tif (a->state == ADP_STATE_DOWN) {\n"
            "\t\t\tenter_delay(a, ADP_DRAW_LINK_UP);               // Milan v1.2 5.6.3.5.3\n\t\t}\n"),
           ("\t\tif (a->state == ADP_STATE_DOWN) {\n"
            "\t\t\tenter_delay(a, ADP_DRAW_STARTUP);               // Milan v1.2 5.6.3.5.3\n\t\t}\n"),
           "walk", "Table551/AdpWalkCell.Graded/LINK_UP_x_DOWN", "LINK_UP x DOWN"),
    Mutant("draw-kinds-merged", ADP_C, FIRST_DRAWS, "\tuint32_t max_ms = ADP_DELAY_MAX_MS;\n",
           "adp", "AdpCore.A9DrawKinds", "A9 every startup draw and every LINK_UP draw is 0..0.5 s"),
    Mutant("link-up-draws-the-delay-kind", ADP_C,
           "\t\t\tenter_delay(a, ADP_DRAW_LINK_UP);               // Milan v1.2 5.6.3.5.3\n",
           "\t\t\tenter_delay(a, ADP_DRAW_DELAY);                 // Milan v1.2 5.6.3.5.3\n",
           "adp", "AdpFirstAvailable.G1G5WithinOneSecondOfEveryLinkUp",
           "G1 the first ENTITY_AVAILABLE leaves within 1 s of every LINK_UP",
           also=(("adp", "AdpFirstAvailable.G3AGrandmasterChangeBeforeItIsCarriedByIt",
                  "G3 a grandmaster change before the first ENTITY_AVAILABLE does not hold it past 1 s"),
                 ("walk", "Table551/AdpWalkCell.Graded/LINK_UP_x_DOWN", "the draw is the 0..0.5 s LINK_UP kind"))),
    Mutant("startup-range-two-seconds", ADP_H,
           "#define ADP_DELAY_STARTUP_MAX_MS 500u   // Milan v1.2 5.6.3.5.2\n",
           "#define ADP_DELAY_STARTUP_MAX_MS 2000u  // Milan v1.2 5.6.3.5.2\n",
           "adp", "AdpFirstAvailable.G2WithinOneSecondOfAStartupWithTheLinkUp",
           "G2 the first ENTITY_AVAILABLE, index 0, leaves within 1 s of a startup with the link up"),
    Mutant("gm-change-in-delay-restarts-the-delay", ADP_C,
           "\tif (a->enabled && a->state == ADP_STATE_WAITING) {\n\t\tenter_delay(a, ADP_DRAW_DELAY);",
           "\tif (a->enabled && a->state != ADP_STATE_DOWN) {\n\t\tenter_delay(a, ADP_DRAW_DELAY);",
           "adp", "AdpFirstAvailable.G3AGrandmasterChangeBeforeItIsCarriedByIt",
           "G3 a grandmaster change before the first ENTITY_AVAILABLE does not hold it past 1 s"),
    Mutant("every-draw-the-first-range", ADP_C,
           "\tuint32_t max_ms = ADP_DELAY_MAX_MS;\n\tif (kind == ADP_DRAW_STARTUP) {\n",
           "\tuint32_t max_ms = ADP_DELAY_LINK_UP_MAX_MS;\n\tif (kind == ADP_DRAW_STARTUP) {\n",
           "adp", "AdpFirstAvailable.G1G5WithinOneSecondOfEveryLinkUp",
           "G5 only the link-up's delay is shortened: the TMR_ADVERTISE delays pass 0.5 s"),
    Mutant("first-delays-not-drawn", ADP_C, "\tuint32_t ms = (r16 * (max_ms + 1u)) >> 16;\n",
           "\tuint32_t ms = kind == ADP_DRAW_DELAY ? (r16 * (max_ms + 1u)) >> 16 : 0u;\n",
           "adp", "AdpFirstAvailable.G1G5WithinOneSecondOfEveryLinkUp",
           "G1 the delay stays a random draw across the link-ups",
           also=(("adp", "AdpFirstAvailable.G2WithinOneSecondOfAStartupWithTheLinkUp",
                  "G2 the startup delay stays a random draw across the entities"),)),
    Mutant("link-loss-resets-the-index", ADP_C,
           ("\t\ttimer_stop(a);                                          // Milan v1.2 5.6.3.5.6 / 5.6.3.5.10\n"
            "\t\ta->available_owed = false;\n"),
           ("\t\ttimer_stop(a);                                          // Milan v1.2 5.6.3.5.6 / 5.6.3.5.10\n"
            "\t\ta->available_owed = false;\n\t\ta->available_index = 0;\n"),
           "adp", "AdpFirstAvailable.G1G5WithinOneSecondOfEveryLinkUp",
           "G1 each ENTITY_AVAILABLE carries the next available_index, across every link-up"),
)
