# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""adp_first_mutants.py - planted defects in the first ENTITY_AVAILABLE after a link-up (#970; test_adp.cpp G1
to G5, H4 to H7, and test_plat_boot.cpp's B25 and B26): Milan's draws, 0 to 4 s on LINK_UP and 0 to 2 s at a startup, each spread over its range (IEEE
1722.1-2021 6.2.4.2.2), and the seed of its first (adp_mbx.h, THE DRAW); a grandmaster change in DELAY that re-arms nothing, one in WAITING announced after its own
0 to 4 s draw; available_index kept across a link loss (Milan v1.2 5.6.3.5.2, 5.6.3.5.3, 5.6.3.5.7, Table 5.51;
IEEE 1722.1-2021 6.2.2.15). The first three are the walk's and the stack's, with the G kills added.
ctrl_mutants.py appends this table to its own.
"""

from __future__ import annotations

from ctrl_mutant import ADP_C, Mutant

#: The adapter, its seed port (THE DRAW).
ADP_MBX = "adp/adp_mbx.c"
H4 = "AdpDraw.H4NeighbouringEntitiesDrawUniformly"
H5 = "AdpDraw.H5BootsDrawUniformly"
H6 = "AdpDraw.H6WithoutAClockBootsDrawUniformly"
H7 = "AdpDraw.H7TheSeedIsTheSumOfMacAndClockMixedWithTheEntityId"
NEIGHBOURS = "H4 neighbouring entities started together draw their first delay uniformly"
BOOTS = "H5 one entity's boots draw their first delay uniformly"
SEED_CLOCK = "clock_fn != NULL ? clock_fn(clock_ctx) : mbx_now_ms();"
SEED_SUM = "\tuint32_t sum = (uint32_t)e->mac + sample;\n\tsum += sum < sample;\n"
SEED_MIX = ("\treturn mix(mix(sum) ^ (uint32_t)e->entity_id ^ (uint32_t)(e->entity_id >> 32) ^ "
            "(seed_interface << 24));\n")
MIX_BODY = ("\tx = ~x + (x << 15);\n\tx ^= x >> 12;\n\tx += x << 2;\n\tx ^= x >> 4;\n"
            "\tx += (x << 3) + (x << 11);\n\treturn x ^ (x >> 16);\n")

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
    # #970: a LINK_UP delay narrowed to 0 to 0.5 s is not Milan's draw (the ruling on #970)
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
    # #970: the seed of the first draw (IEEE 1722.1-2021 6.2.4.2.2)
    Mutant("seed-is-now-ms", ADP_MBX, SEED_CLOCK, "mbx_now_ms();\n\t(void)clock_fn;", "adp", H5, BOOTS),
    Mutant("seed-fallback-constant", ADP_MBX, SEED_CLOCK, "clock_fn != NULL ? clock_fn(clock_ctx) : 0u;", "adp", H6,
           "H6 without a clock the seed's NOW_MS still spreads one entity's boots"),
    Mutant("seed-mix-is-the-identity", ADP_MBX, MIX_BODY, "\treturn x;\n", "adp", H5, BOOTS),
    Mutant("seed-one-round", ADP_MBX, SEED_MIX, SEED_MIX.replace("mix(mix(sum) ^", "mix(sum ^"), "adp", H4, NEIGHBOURS),
    Mutant("seed-without-the-entity-id", ADP_MBX, SEED_MIX,
           "\treturn mix(mix(sum) ^ (seed_interface << 24));\n", "adp", H4, NEIGHBOURS),
    Mutant("seed-without-the-mac", ADP_MBX, SEED_SUM, "\tuint32_t sum = sample;\n", "adp", H7,
           "H7 the MAC address is in the seed"),
    Mutant("seed-mac-not-summed", ADP_MBX, SEED_SUM, "\tuint32_t sum = (uint32_t)e->mac ^ sample;\n", "adp", H7,
           "H7 the seed is the sum of MAC address and clock"),
    Mutant("seed-carry-dropped", ADP_MBX, SEED_SUM, "\tuint32_t sum = (uint32_t)e->mac + sample;\n", "adp", H7,
           "H7 the sum carries end around"),
    Mutant("seed-without-the-interface", ADP_MBX, SEED_MIX, SEED_MIX.replace(" ^ (seed_interface << 24)", ""),
           "platboot2", "Boot.B26TwoInterfacesAreSeededApart",
           "B26 two interfaces enabled at one clock reading are seeded apart"),
    Mutant("seed-clock-not-wired", "plat/ctrl_plat.c", "\tadp_mbx_set_clock(adp_clock, p);\n",
           "\tadp_mbx_set_clock(NULL, NULL);\n\t(void)adp_clock;\n", "platboot1",
           "Boot.B25TheAdpDrawIsSeededFromThePlatformsClock", "B25 boots that differ only in the clock's origin"),
)
