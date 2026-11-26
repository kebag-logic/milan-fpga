# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""adp_first_mutants.py - planted defects in the first ENTITY_AVAILABLE after a link-up (#970).

test_adp.cpp G1 to G5 and H4 to H10, and test_plat_boot.cpp B25 to B27, hold them: Milan's draws, 0 to 4 s on
LINK_UP and 0 to 2 s at a startup, each spread over its range (IEEE 1722.1-2021 6.2.4.2.2); one fresh clock sample at
each qualified rise and at the startup draw, none at a duplicate or disabled LINK_UP, mixed with the MAC address, the
entity ID and the interface (adp_mbx.h, THE DRAW); the platform's microsecond clock wired before ADP starts; a
grandmaster change in DELAY that re-arms nothing, one in WAITING announced after its own 0 to 4 s draw;
available_index kept across a link loss (Milan v1.2 5.6.3.5.2, 5.6.3.5.3, 5.6.3.5.7, Table 5.51; IEEE 1722.1-2021
6.2.2.15). The first three are the walk's and the stack's, with the G kills added. ctrl_mutants.py appends this table
to its own.
"""

from __future__ import annotations

from pathlib import Path

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
SEED_SUM = "\tuint32_t sum = (uint32_t)e->mac + sample;\n"
SEED_MIX = "\tuint32_t x = mix(mix(a->rng ^ sum) ^ id ^ ((uint32_t)a->interface << 24));\n"
MIX_BODY = ("\tx = ~x + (x << 15);\n\tx ^= x >> 12;\n\tx += x << 2;\n\tx ^= x >> 4;\n"
            "\tx += (x << 3) + (x << 11);\n\treturn x ^ (x >> 16);\n")
H8 = "AdpDraw.H8ALaterLinkUpTakesAFreshSample"
H9 = "AdpDraw.H9EachQualifiedRiseReadsTheClockOnce"
H10 = "AdpDraw.H10TheClockAtTheLinkUpSetsItsDraw"
B25 = "Boot.B25TheAdpDrawIsSeededFromThePlatformsClock"
B27 = "Boot.B27ALinkUpReadsThePlatformsClockAtTheLinkUp"
B25_WORDS = "B25 boots one microsecond apart in the clock's origin seed ADP's draw differently"
#: The core's LINK_UP from DOWN, its duplicate guard and its sample (tsn-c-stack adp.c).
RISE = "\t\t\tleave_down(a, ADP_DRAW_DELAY);  "
GUARD = "\tif (!a->enabled || up == was) {\n\t\treturn;\n\t}\n"
SAMPLE = "\tuint32_t sample = a->ports->seed(a->ports->ctx);\n"
#: The platform's clock and its wiring (ctrl_plat.c).
PLAT_CLOCK = "\treturn (uint32_t)p->env->flash->now_us(p->env->flash->ctx);\n"
PLAT_WIRE = "\tadp_mbx_set_clock(adp_clock, p);\n"
PLAT_RELEASE = "\tctrl_app_release_adp(&p->app);\n"
#: The boot from the clock's wiring to ADP's release, read from the source: the plant moves the wiring past the
#: release, so ADP's startup draw reads NOW_MS.
_PLAT = (Path(__file__).resolve().parents[1] / "plat/ctrl_plat.c").read_text(encoding="utf-8")
WIRED_TO_RELEASE = _PLAT[_PLAT.index(PLAT_WIRE):_PLAT.index(PLAT_RELEASE) + len(PLAT_RELEASE)]

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
            "\t\t\tleave_down(a, ADP_DRAW_DELAY);                  // Milan v1.2 5.6.3.5.3\n\t\t}\n"),
           ("\t\tif (a->state == ADP_STATE_DOWN) {\n"
            "\t\t\tleave_down(a, ADP_DRAW_STARTUP);                // Milan v1.2 5.6.3.5.3\n\t\t}\n"),
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
    Mutant("seed-mix-is-the-identity", ADP_C, MIX_BODY, "\treturn x;\n", "adp", H5, BOOTS),
    Mutant("seed-one-round", ADP_C, SEED_MIX, SEED_MIX.replace("mix(mix(a->rng ^ sum) ^", "mix(a->rng ^ sum ^"),
           "adp", H4, NEIGHBOURS),
    Mutant("seed-without-the-entity-id", ADP_C, SEED_MIX,
           SEED_MIX.replace(" ^ id ^", " ^ (id & 0u) ^"), "adp", H4, NEIGHBOURS),
    Mutant("seed-without-the-mac", ADP_C, SEED_SUM, "\tuint32_t sum = sample;\n", "adp", H7,
           "H7 the MAC address is in the seed"),
    Mutant("seed-mac-not-summed", ADP_C, SEED_SUM, "\tuint32_t sum = (uint32_t)e->mac ^ sample;\n", "adp", H7,
           "H7 the seed is the sum of MAC address and clock"),
    Mutant("seed-end-around-carry-added", ADP_C, SEED_SUM, SEED_SUM + "\tsum += sum < sample;\n", "adp", H7,
           "H7 the seed is the sum modulo 2^32"),
    Mutant("seed-without-the-interface", ADP_C, SEED_MIX,
           SEED_MIX.replace(" ^ ((uint32_t)a->interface << 24)", ""),
           "platboot2", "Boot.B26TwoInterfacesAreSeededApart",
           "B26 two interfaces enabled at one clock reading are seeded apart"),
    Mutant("seed-clock-not-wired", "plat/ctrl_plat.c", "\tadp_mbx_set_clock(adp_clock, p);\n",
           "\tadp_mbx_set_clock(NULL, NULL);\n\t(void)adp_clock;\n", "platboot1", B25, B25_WORDS),
    Mutant("later-link-up-not-reseeded", ADP_C, "\t\t\tleave_down(a, ADP_DRAW_DELAY);  ",
           "\t\t\t(a->draws == 0u ? leave_down : enter_delay)(a, ADP_DRAW_DELAY);  ", "adp", H8,
           "H8 a LINK_UP after a link loss draws from a fresh sample"),
    # #970, the reviews of PR #1015: each qualified rise samples, through the adapter and the platform
    Mutant("link-up-not-sampled", ADP_C, RISE, "\t\t\tenter_delay(a, ADP_DRAW_DELAY);  ", "adp", H9,
           "H9 each qualified LINK_UP reads the clock once through the adapter",
           also=(("platboot1", B27, "B27 boots apart only in the clock at the LINK_UP draw apart"),)),
    Mutant("duplicate-up-sampled", ADP_C, GUARD,
           "\tif (up && up == was) {\n\t\t(void)a->ports->seed(a->ports->ctx);\n\t}\n" + GUARD, "adp", H9,
           "H9 a duplicate LINK_UP reads no clock"),
    Mutant("disabled-up-sampled", ADP_C, GUARD,
           "\tif (up && !a->enabled) {\n\t\t(void)a->ports->seed(a->ports->ctx);\n\t}\n" + GUARD, "adp", H9,
           "H9 a LINK_UP while disabled reads no clock"),
    Mutant("link-up-sample-ignored", ADP_C, SAMPLE,
           "\tuint32_t sample = a->ports->seed(a->ports->ctx) & (kind == ADP_DRAW_DELAY ? 0u : 0xFFFFFFFFu);\n",
           "adp", H10, "H10 boots apart only at the LINK_UP draw apart"),
    Mutant("plat-clock-in-milliseconds", "plat/ctrl_plat.c", PLAT_CLOCK,
           "\treturn (uint32_t)(p->env->flash->now_us(p->env->flash->ctx) / 1000u);\n", "platboot1", B25, B25_WORDS),
    Mutant("plat-clock-1024-us-granule", "plat/ctrl_plat.c", PLAT_CLOCK,
           "\treturn (uint32_t)p->env->flash->now_us(p->env->flash->ctx) & ~0x3FFu;\n", "platboot1", B25, B25_WORDS),
    Mutant("plat-clock-wired-after-release", "plat/ctrl_plat.c", WIRED_TO_RELEASE,
           WIRED_TO_RELEASE.removeprefix(PLAT_WIRE) + PLAT_WIRE, "platboot1", B25, B25_WORDS),
)
