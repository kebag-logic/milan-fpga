# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_mutants.py - planted defects the control-plane firmware's host test must catch.

Each mutant is one substitution in a COPY of sw/firmware/ctrl (never the
checkout), the arm that must catch it, the GoogleTest test that must fail (its
full name, or the prefix every instance of a parameterised test shares) and a
fragment of the failing assertion's own words, the name the check had in the
hand-rolled suite this replaced. A mutant is caught only when that arm fails
AND a `[FAIL]` line names that test with those words: a build that breaks, or
another test failing, is reported as an escape, because neither proves the
test can see the defect. A mutant may name further (arm, test, words) kills in
`also`, each of which must hold too.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import acmp_mutants
import ctrl_arms
import fw_gtest
from maap_mutants import mutants as maap_mutants
from ctrl_build import CTRL, Outcome, Refusal, Tree
from ctrl_mutant import Mutant


#: ctrl_app_compose and ctrl_app_open, from the pool's bind to the mailbox's
#: open: the app binds lwSRP's pool before anything reads the mailbox window.
#: (Lane FC: the open also takes every interface's own MAC. Lane F3: the boot
#: is two calls, compose then open, with ACMP composed after ADP.)
APP_BRING = ("\tshlan_port_bind_pool(&app->pool);\n\tctrl_debug_bind(cfg->sink, cfg->sink_ctx);\n"
             "\tctrl_loop_init(&app->loop);\n"
             "\tif (!adp_mbx_init(&app->adp, cfg->entity, CTRL_APP_ADP_FIRST_SLOT, "
             "cfg->current_configuration_index) ||\n"
             "\t    !adp_mbx_attach(&app->adp, &app->loop)) {\n\t\treturn false;\n\t}\n"
             "\t// ACMP stands in front of ADP's binding of the adp channel, so it comes\n"
             "\t// after it\n"
             "\treturn cfg->acmp == NULL ||\n"
             "\t       (acmp_mbx_init(&app->acmp, cfg->acmp, cfg->acmp_env, CTRL_APP_ACMP_FIRST_SLOT) &&\n"
             "\t\tacmp_mbx_attach(&app->acmp, &app->loop));\n"
             "}\n\n"
             "bool ctrl_app_open(struct ctrl_app *app, const struct ctrl_app_config *cfg)\n{\n"
             "\t// ADP sends the entity's one MAC on every interface (adp.c), so it is\n"
             "\t// every interface's own unicast address\n"
             "\tuint64_t own_mac[MBX_N_IF];\n"
             "\tfor (unsigned i = 0; i < MBX_N_IF; ++i) {\n\t\town_mac[i] = cfg->entity->mac;\n\t}\n"
             "\tif (!ctrl_loop_open(&app->loop, cfg->entity->entity_id, own_mac)) {\n\t\treturn false;\n\t}\n")

#: The model's classifier entry, and the same with a front end that strips an
#: 802.1Q C-tag before it (lane FC, rule 1).
MODEL_CLASSIFY = "\tbool mismatch = false;\n\tint found = classify(m, frame, len, interface, &mismatch);\n"
MODEL_CLASSIFY_UNTAGGED = ("\tuint8_t stripped[MBX_FRAME_BYTES_MAX + 4u];\n"
                           "\tif (len > 16u && len <= sizeof stripped && wire_be16(frame + 12u) == 0x8100u) {\n"
                           "\t\tmemcpy(stripped, frame, 12u);\n\t\tmemcpy(stripped + 12u, frame + 16u, len - 16u);\n"
                           "\t\tframe = stripped;\n\t\tlen -= 4u;\n\t}\n" + MODEL_CLASSIFY)

#: ctrl_loop_open's identities and channel opening, and the same with the own
#: MACs written only once the channels are open.
LOOP_OWN_MAC = ("\tfor (unsigned i = 0; i < MBX_N_IF; ++i) {\n"
                "\t\t(void)mbx_filter_set_own_mac(i, own_mac[i]);    // every i is an interface of the contract\n"
                "\t}\n")
LOOP_OPEN = ("\tmbx_irq_enable(mbx_place(open, MBX_IRQ_ENABLE_RX_LSB, MBX_IRQ_ENABLE_RX_WIDTH) |\n"
             "\t\t       mbx_place(1u, MBX_IRQ_ENABLE_EVT_LSB, MBX_IRQ_ENABLE_EVT_WIDTH));\n"
             "\tmbx_tick_enable(l->n_ticks > 0u);\n\tmbx_filter_open(open);\n")

#: The model arm's test of one suite group.
MODEL_GROUP = "Suite/MbxModelGroup.PassesOnTheModel/"
#: The same with the pool bound only once the mailbox is open.
APP_BRING_LATE = APP_BRING.removeprefix("\tshlan_port_bind_pool(&app->pool);\n") + \
    "\tshlan_port_bind_pool(&app->pool);\n"

MUTANTS = (
    Mutant("reentry-guard-removed", "adp/adp.c",
           "\tassert(!port_active);\n\tif (port_active) {",
           "\tif (port_active && false) {",
           "reentry_debug", "AdpReentry.AdvertiseInlineExpiry", "inline ADVERTISE expiry asserts",
           (("reentry_debug", "AdpReentry.DelayInlineExpiryOnGmChange", "inline DELAY expiry asserts"),
            ("reentry_release", "AdpReentry.AdvertiseInlineExpiry", "inline ADVERTISE expiry is counted"),
            ("reentry_release", "AdpReentry.DelayInlineExpiryOnGmChange", "inline DELAY expiry is counted"))),
    Mutant("reentry-uncounted", "adp/adp.c", "\t\treentry_count++;\n", "",
           "reentry_release", "AdpReentry.AdvertiseInlineExpiry", "inline ADVERTISE expiry is counted"),
    Mutant("reentry-not-ignored", "adp/adp.c", "\t\treentry_count++;\n\t\treturn true;",
           "\t\treentry_count++;\n\t\treturn false;",
           "reentry_release", "AllPorts/AdpPortEntry.RefusesBeforeTouchingState/",
           "callback leaves core state unchanged"),
    Mutant("departing-keeps-index", "adp/adp.c",
           "\tuint32_t index = a->available_index;\n\ta->available_index = 0;\n",
           "\tuint32_t index = a->available_index;\n", "walk", "Table551/AdpWalkCell.Graded/", "available_index"),
    # R497-1-F2's reading, which the ruling on PR #668 (5994972330) rejects.
    Mutant("departing-sends-zero", "adp/adp.c", "if (!send(a, ADP_MSG_ENTITY_DEPARTING, a->departing_index)) {",
           "if (!send(a, ADP_MSG_ENTITY_DEPARTING, a->departing_index & 0u)) {",
           "adp", "AdpCore.A10toA14DepartingIndex", "A10 SHUTDOWN in WAITING"),
    # R497-2-F1: the restart's ENTITY_AVAILABLE takes the owed DEPARTING's place.
    Mutant("available-replaces-owed-departing", "adp/adp.c",
           "\ta->available_owed = true;\n\tif (a->departing_owed != 0u ||",
           "\ta->available_owed = true;\n\ta->departing_owed = 0u;\n\tif (a->departing_owed != 0u ||",
           "adp", "AdpCore.A15OwedDepartingAcrossARestart",
           "A15 with room, the next poll sends the owed ENTITY_DEPARTING first"),
    Mutant("available-passes-owed-departing", "adp/adp.c",
           "if (a->departing_owed != 0u || !send(a, ADP_MSG_ENTITY_AVAILABLE, a->available_index)) {",
           "if (!send(a, ADP_MSG_ENTITY_AVAILABLE, a->available_index)) {", "adp", "AdpCore.A17RoomBackBeforeAPoll",
           "A17 room back and TMR_DELAY expiring before a poll"),
    Mutant("second-departing-dropped", "adp/adp.c",
           "\t\ta->departing_owed++;                                    // queued behind the oldest, carrying 0\n",
           "", "adp", "AdpCore.A16SecondShutdownQueuesItsOwn", "A16 a SHUTDOWN while one is owed queues its own"),
    Mutant("second-shutdown-overwrites-index", "adp/adp.c",
           "\t} else if (a->departing_owed < ADP_DEPARTING_OWED_MAX) {\n",
           "\t} else if (a->departing_owed < ADP_DEPARTING_OWED_MAX) {\n\t\ta->departing_index = index;\n",
           "adp", "AdpCore.A16SecondShutdownQueuesItsOwn",
           "A16 a SHUTDOWN while one is owed queues its own"),
    # R496-3-F2: the legs of the owed-frame rule beyond A15 to A17.
    Mutant("link-loss-drops-owed-departing", "adp/adp.c",
           "\t\ta->available_owed = false;                              // an owed DEPARTING stays owed\n",
           "\t\ta->available_owed = false;\n\t\ta->departing_owed = 0u;\n",
           "adp", "AdpCore.A18LinkLossKeepsTheOwedDeparting",
           "A18 a link loss during the restart stops it and keeps the owed ENTITY_DEPARTING"),
    Mutant("gm-change-drops-owed-available", "adp/adp.c", "\ta->gm_changed++;\n",
           "\ta->gm_changed++;\n\ta->available_owed = false;\n", "adp", "AdpCore.A19IgnoredInputsKeepTheOwedAvailable",
           "A19 a GM change in DELAY leaves the owed ENTITY_AVAILABLE owed"),
    Mutant("discover-drops-owed-available", "adp/adp.c",
           "\tif (!a->enabled || a->state != ADP_STATE_WAITING) {             // Table 5.51: ignored\n",
           "\tif (!a->enabled || a->state != ADP_STATE_WAITING) {\n\t\ta->available_owed = false;\n",
           "adp", "AdpCore.A19IgnoredInputsKeepTheOwedAvailable",
           "A19 so does an ENTITY_DISCOVER"),
    Mutant("stray-expiry-drops-owed-available", "adp/adp.c", "\t\ta->stray_expiries++;\n\t\treturn;\n",
           "\t\ta->stray_expiries++;\n\t\ta->available_owed = false;\n\t\treturn;\n",
           "adp", "AdpCore.A19IgnoredInputsKeepTheOwedAvailable",
           "A19 and a stray expiry, which is counted"),
    Mutant("link-loss-keeps-owed-available", "adp/adp.c",
           "\t\ta->available_owed = false;                              // an owed DEPARTING stays owed\n", "",
           "adp", "AdpCore.A20LinkLossDropsTheOwedAvailable",
           "A20 a link loss drops the owed ENTITY_AVAILABLE at once"),
    # R497-3-F1: the bound on owed DEPARTINGs, and R496-3-F1: the pass it gives.
    Mutant("departing-queue-unbounded", "adp/adp.c",
           "\t} else if (a->departing_owed < ADP_DEPARTING_OWED_MAX) {\n",
           "\t} else if (a->departing_owed != UINT32_MAX) {\n",
           "adp", "Shutdowns/AdpOwedBound.E5CommittedInPassKPlusOne/",
           "E5 64 SHUTDOWNs behind a full ring, expiry taken before the room: the ENTITY_AVAILABLE is committed"),
    Mutant("coalesced-departing-uncounted", "adp/adp.c", "\t\ta->departing_coalesced++;", "\t\t(void)0;",
           "adp", "AdpCore.A21DepartingCapacity",
           "A21 the next SHUTDOWN is coalesced into the queued one and counted"),
    Mutant("coalesce-drops-queued-departing", "adp/adp.c", "\t\ta->departing_coalesced++;",
           "\t\ta->departing_coalesced++;\n\t\ta->departing_owed--;", "adp", "AdpCore.A21DepartingCapacity",
           "A21 the next SHUTDOWN is coalesced into the queued one and counted"),
    Mutant("coalesce-overwrites-oldest-index", "adp/adp.c", "\t\ta->departing_coalesced++;",
           "\t\ta->departing_coalesced++;\n\t\ta->departing_index = index;", "adp", "AdpCore.A21DepartingCapacity",
           "A21 the next SHUTDOWN is coalesced into the queued one and counted"),
    Mutant("own-discover-discarded", "adp/adp.c", "if (target != 0u && target != a->entity->entity_id) {",
           "if (target != 0u) {",
           "walk", "Table551/AdpWalkCell.Graded/RCV_ADP_DISCOVER_own_eid_x_WAITING",
           "RCV_ADP_DISCOVER(own eid) x WAITING"),
    Mutant("down-answers-discover", "adp/adp.c", "if (!a->enabled || a->state != ADP_STATE_WAITING) {",
           "if (!a->enabled) {",
           "walk", "Table551/AdpWalkCell.Graded/RCV_ADP_DISCOVER_eid_0_x_DOWN", "RCV_ADP_DISCOVER(eid 0) x DOWN"),
    Mutant("link-down-departs", "adp/adp.c", "\t\ttimer_stop(a);                                          // 5.6.3.5.6",
           "\t\t(void)send(a, ADP_MSG_ENTITY_DEPARTING, a->available_index);\n\t\ttimer_stop(a); // 5.6.3.5.6",
           "walk", "Table551/AdpWalkCell.Graded/LINK_DOWN_x_WAITING", "LINK_DOWN x WAITING: frames committed"),
    Mutant("gm-change-ignored", "adp/adp.c", "\t\tenter_delay(a, ADP_DRAW_DELAY);                         // 5.6.3.5.7",
           "\t\t(void)0;", "walk", "Table551/AdpWalkCell.Graded/GM_CHANGE_x_WAITING", "GM_CHANGE x WAITING"),
    Mutant("delay-ignores-link-down", "adp/adp.c", "\tif (a->state != ADP_STATE_DOWN) {\n\t\ttimer_stop(a);",
           "\tif (a->state == ADP_STATE_WAITING) {\n\t\ttimer_stop(a);",
           "walk", "Table551/AdpWalkCell.Graded/LINK_DOWN_x_DELAY_timer_armed", "LINK_DOWN x DELAY"),
    Mutant("shutdown-in-down-departs", "adp/adp.c",
           "\tif (a->state == ADP_STATE_DOWN) {\n\t\treturn;\n\t}\n\ttimer_stop(a);",
           "\ttimer_stop(a);", "walk", "Table551/AdpWalkCell.Graded/SHUTDOWN_x_DOWN", "SHUTDOWN x DOWN"),
    Mutant("advertise-expiry-skips-delay", "adp/adp.c",
           "\t\tenter_delay(a, ADP_DRAW_DELAY);                         // 5.6.3.5.5",
           "\t\ttimer_start(a, ADP_TIMER_DELAY, 0u); // 5.6.3.5.5 broken",
           "walk", "Table551/AdpWalkCell.Graded/TMR_ADVERTISE_x_WAITING", "TMR_ADVERTISE x WAITING"),
    Mutant("advertise-period-wrong", "adp/adp.c", "timer_start(a, ADP_TIMER_ADVERTISE, ADP_ADVERTISE_MS);",
           "timer_start(a, ADP_TIMER_ADVERTISE, ADP_ADVERTISE_MS + 1000u);",
           "walk", "Table551/AdpWalkCell.Graded/TMR_DELAY_x_DELAY_timer_armed", "TMR_DELAY x DELAY(timer armed)"),
    Mutant("link-up-draws-startup-kind", "adp/adp.c",
           "\t\t\tenter_delay(a, ADP_DRAW_DELAY);                 // 5.6.3.5.3",
           "\t\t\tenter_delay(a, ADP_DRAW_STARTUP);               // 5.6.3.5.3",
           "walk", "Table551/AdpWalkCell.Graded/LINK_UP_x_DOWN", "LINK_UP x DOWN"),
    Mutant("draw-kinds-merged", "adp/adp.c", "kind == ADP_DRAW_STARTUP ? ADP_DELAY_STARTUP_MAX_MS : ADP_DELAY_MAX_MS",
           "ADP_DELAY_MAX_MS", "adp", "AdpCore.A9DrawKinds", "A9 every startup draw"),
    Mutant("foreign-discover-answered", "adp/adp.c", "if (target != 0u && target != a->entity->entity_id) {",
           "if (target == 1u) {", "adp", "AdpCore.A3toA5DiscoverAndDiscard", "A4 a foreign DISCOVER"),
    Mutant("frame-misses-config-index", "adp/adp.c", "wire_put_be(pdu + 50, a->current_configuration_index, 2);",
           "wire_put_be(pdu + 50, 0u, 2);", "walk", "AdpWalk.P11ConfigurationIndexBytes", "P11"),
    Mutant("stale-tag-accepted", "adp/adp_mbx.c", "if (!i->armed || ev->timer_tag != i->tag) {",
           "if (!i->armed) {", "adp", "AdpAdapter.B1StaleTagDiscarded", "B1 an expiry of the arm a GM_CHANGE replaced"),
    Mutant("latency-extra-read", "adp/adp_mbx.c", "\tmbx_timer_arm(i->slot, i->tag, mbx_now_ms() + delay_ms);",
           "\t(void)mbx_link_up(0);\n\tmbx_timer_arm(i->slot, i->tag, mbx_now_ms() + delay_ms);",
           "adp", "AdpLatency.C0toC6EveryResponsePath",
           "C0 LINK_UP -> TMR_DELAY armed"),
    Mutant("pool-free-leaks", "port/ctrl_pool.c", "\t\tbin->free_head = ptr;\n\t\tbin->free_count++;",
           "\t\tbin->free_count++;", "port", "Pool.P2ReleaseAndBadFrees", "P2 a released block"),
    Mutant("calloc-overflow-unchecked", "port/ctrl_pool.c", "if (nmemb != 0u && bytes > SIZE_MAX / nmemb) {",
           "if (nmemb == 0u) {", "port", "Pool.P3CallocZeroesAndRefusesAWrap", "P3 calloc refuses"),
    Mutant("pool-double-free-accepted", "port/ctrl_pool.c",
           "if (offset % bin->stride != 0u || bin->used[index] == 0u) {",
           "if (offset % bin->stride != 0u) {", "port", "Pool.P2ReleaseAndBadFrees", "P2 a double free"),
    Mutant("debug-truncation-uncounted", "port/ctrl_debug.c", "\t\ttruncated++;\n", "",
           "port", "DebugSink.S2TruncatedToTheLine", "S2 the truncation"),
    Mutant("tick-count-ignored", "loop/ctrl_loop.c", "for (uint32_t k = 0; k < count; ++k) {",
           "for (uint32_t k = 0; k < (count != 0u ? 1u : 0u); ++k) {",
           "port", "Loop.L4TickFanOut", "L4 every centisecond"),
    Mutant("rx-pass-unbounded", "loop/ctrl_loop.c", "for (unsigned k = 0; k < CTRL_LOOP_RX_PER_PASS; ++k) {",
           "for (unsigned k = 0; k < 64u; ++k) {", "port", "Loop.L2PerPassRxBound", "L2 a pass takes at most"),
    Mutant("poll-owes-nothing", "adp/adp_mbx.c", "\treturn owed;\n}", "\treturn false;\n}",
           "adp", "AdpOwed.E0toE3PendingWake",
           "E1 the loop does not sleep while a frame is owed"),
    Mutant("events-halved", "loop/ctrl_loop.c", "while (n < CTRL_LOOP_EVENTS_PER_PASS && mbx_event_take(&ev)) {",
           "while (n < CTRL_LOOP_EVENTS_PER_PASS / 2u && mbx_event_take(&ev)) {",
           "adp", "AdpBacklog.F0toF7FullBacklogs",
           "F2 all 16 event records are taken by pass",
           (("acmp", "AcmpMailbox.F0ToF3FullRingsAreTakenWithinTheBound", "F1 every event is taken by pass 2"),)),
    Mutant("rx-before-events", "loop/ctrl_loop.c",
           "\tunsigned work = service_events(l);\n\tfor (unsigned ch = 0; ch < MBX_N_CH; ++ch) {\n"
           "\t\tif (l->rx[ch].fn != NULL) {\n\t\t\twork += service_rx(l, ch);\n\t\t}\n\t}\n",
           "\tunsigned work = 0;\n\tfor (unsigned ch = 0; ch < MBX_N_CH; ++ch) {\n"
           "\t\tif (l->rx[ch].fn != NULL) {\n\t\t\twork += service_rx(l, ch);\n\t\t}\n\t}\n"
           "\twork += service_events(l);\n", "adp", "AdpBacklog.F0toF7FullBacklogs", "F1 events first"),
    Mutant("carried-ticks-overwritten", "loop/ctrl_loop.c", "l->ticks_owed += ev.tick_count;",
           "l->ticks_owed = ev.tick_count;",
           "port", "Loop.L8TickRecordWhileCarried", "L8 a TICK record taken while centiseconds are carried"),
    Mutant("tick-slice-unbounded", "loop/ctrl_loop.c",
           "ticked += dispatch_ticks(l, CTRL_LOOP_TICKS_PER_PASS - ticked);",
           "ticked += dispatch_ticks(l, CTRL_LOOP_TICKS_PER_PASS - ticked + l->ticks_owed);",
           "port", "Loop.L7TickSlices",
           "L7 at most CTRL_LOOP_TICKS_PER_PASS"),
    Mutant("owed-ticks-let-it-sleep", "loop/ctrl_loop.c", "\tbool owed = l->ticks_owed != 0u;",
           "\tbool owed = false;", "port", "Loop.L7TickSlices", "L7 and the loop keeps passing"),
    Mutant("filter-opened-before-eid", "loop/ctrl_loop.c", "\tmbx_filter_set_own_eid(entity_id);\n",
           "\tmbx_filter_open(open);\n\tmbx_filter_set_own_eid(entity_id);\n",
           "port", "LoopBring.L1OpenOrder", "L1 OWN_EID is written before"),
    Mutant("rx-no-resync", "mbx/mbx.c",
           "\trx_tail[ch] = head;\n\tmbx_hal_write32(ch_reg(ch, MBX_CH_REG_RX_TAIL), head);",
           "\t(void)ch;\n\t(void)head;", "port", "Driver.D1MalformedRecordResynchronises",
           "D1 and the ring is resynchronised",
           (("unit", "Records/DriverMalformed.D7RefusedAndResynchronised/",
             "and the ring is resynchronised to RX_HEAD"),)),
    Mutant("tx-overfills", "mbx/mbx.c", "record > tx_words[ch] - used", "record > tx_words[ch] - used + 23u",
           "port", "Driver.D3HeldMergeFillsAndOrderAcrossChannels",
           "D3 a held merge fills the ring"),
    Mutant("lanes-big-endian", "mbx/mbx_wire.h", "\t\tword |= (uint32_t)p[i] << (8u * i);",
           "\t\tword |= (uint32_t)p[i] << (8u * (3u - i));",
           "model", "Suite/MbxModelGroup.PassesOnTheModel/", "F1 frame byte k is ring word"),
    Mutant("frame-sources-from-sinks", "adp/adp.c", "wire_put_be(pdu + 24, e->talker_stream_sources, 2);",
           "wire_put_be(pdu + 24, e->listener_stream_sinks, 2);",
           "entity", "Fabric/EntityField.MatchesTheFabric/talker_stream_sources", "talker_stream_sources"),
    # a heap the host test sees (the block is not the pool's) and the RV32
    # arm's symbol check sees (malloc left undefined)
    Mutant("pool-falls-back-to-heap", "port/shlan_port.c", "\treturn ctrl_pool_alloc(port_pool, size);",
           "\treturn __builtin_malloc(size);", "port", "Pool.P4ShlanFunctionsDrawOnTheBoundPool",
           "P4 shlan_malloc and shlan_calloc draw on the bound pool",
           (("rv32", "", "symbols outside the C library"),)),
    Mutant("model-rate-unlimited", "host/mbx_model.c", "\tif (ch->tokens == 0u) {",
           "\tif (ch->tokens == 0u && false) {",
           "model", "Suite/MbxModelGroup.PassesOnTheModel/RateLimit", "T0 the frames past it count in RATE_DROP"),
    Mutant("seq-not-stamped", "mbx/mbx.c", "\ttx_seq = (uint16_t)(tx_seq + 1u);\n", "",
           "port", "Driver.D3HeldMergeFillsAndOrderAcrossChannels",
           "D3 ACMP, ACMP, AECP committed by the driver"),
    Mutant("model-round-robin", "host/mbx_model.c",
           "if (c == MBX_N_CH || ((uint16_t)(seq - best) & 0x8000u) != 0u) {",
           "if (c == MBX_N_CH || ((uint16_t)(seq - best) & 0u) != 0u) {",
           "model", "Suite/MbxModelGroup.PassesOnTheModel/TxCommitOrder",
           "X2 ACMP, ACMP, then AECP committed behind a stalled ACMP frame"),
    Mutant("model-gm-hi-live", "host/mbx_model.c", "\t\treturn m->gm_hi_snap[i];",
           "\t\treturn (uint32_t)(m->gm_id[i] >> 32);",
           "model", "Suite/MbxModelGroup.PassesOnTheModel/GmSnapshot", "G0 GM_HI reads the snapshot"),
    # ---- #665 lane FT: the tests written for branch coverage ----
    Mutant("zero-byte-class-accepted", "port/ctrl_pool.c",
           "if (classes[i].blocks == 0u || classes[i].block_bytes == 0u) {", "if (classes[i].blocks == 0u) {",
           "port", "Pool.P5ClassTablesAndArenasRefused", "P5 a class of zero-byte blocks is refused"),
    Mutant("zero-size-refusal-uncounted", "port/ctrl_pool.c", "\tif (bytes == 0u) {\n\t\tpool->refused++;\n",
           "\tif (bytes == 0u) {\n", "port", "Pool.P6CallocOfNothingAndOnAnExhaustedPool",
           "P6 and both refusals are counted"),
    Mutant("foreign-free-uncounted", "port/ctrl_pool.c", "\t\treturn;\n\t}\n\tpool->bad_frees++;\n}",
           "\t\treturn;\n\t}\n}", "port", "Pool.P7FreeBelowTheArenaRefused",
           "P7 a free below the first class is refused and counted"),
    Mutant("port-pool-unreported", "port/shlan_port.c", "\treturn port_pool;\n", "\treturn NULL;\n",
           "port", "Pool.P8PortLayerUnbound", "P8 the bound pool is the one reported"),
    # R506-1-F1: a free list a client cut short. Followed to its end, the
    # NULL it ends in is dereferenced, and the crash report names the test.
    Mutant("pool-follows-a-cut-free-list", "port/ctrl_pool.c", " && bin->free_head != NULL) {", ") {",
           "port", "Pool.P9AFreeListShorterThanItsCountIsExhausted", "crashed on signal 11"),
    Mutant("pool-cut-list-refuses-outright", "port/ctrl_pool.c",
           "\t\tif (bin->stride >= bytes && bin->free_count > 0u && bin->free_head != NULL) {\n",
           "\t\tif (bin->stride >= bytes && bin->free_count > 0u && bin->free_head == NULL) {\n\t\t\tbreak;\n\t\t}\n"
           "\t\tif (bin->stride >= bytes && bin->free_count > 0u) {\n",
           "port", "Pool.P9AFreeListShorterThanItsCountIsExhausted", "P9 a class whose list ends before its count"),
    Mutant("encoding-failure-swallowed", "port/ctrl_debug.c", "return want < 0 ? want : 0;", "return 0;",
           "port", "DebugSink.S3UnencodablePrintDiscarded", "S3 an encoding failure is returned"),
    Mutant("rx-binds-no-function", "loop/ctrl_loop.c", "if (ch >= MBX_N_CH || fn == NULL) {",
           "if (ch >= MBX_N_CH) {", "port", "LoopBring.L9TablesRefuseNullAndOverflow",
           "L9 a channel bound to no function is refused"),
    Mutant("seed-left-at-zero", "adp/adp.c", "0x9E3779B9u;\n\tif (a->rng == 0u) {\n\t\ta->rng = 1u;\n\t}\n",
           "0x9E3779B9u;\n", "adp", "AdpCore.A22GeneratorNeverStuckAtZero",
           "A22 an entity id whose words cancel the seed constant"),
    Mutant("enable-not-idempotent", "adp/adp.c", "\tif (enable == a->enabled) {\n\t\treturn;\n\t}\n", "",
           "adp", "AdpCore.A23RepeatedEnableOrDisableChangesNothing",
           "A23 an enable while enabled draws and arms nothing"),
    Mutant("other-subtype-accepted", "adp/adp.c", "\t    frame[ADP_HEADER_BYTES] != ADP_SUBTYPE ||\n", "",
           "adp", "AdpCore.A24OtherEtherTypeOrSubtypeDiscarded",
           "A24 a DISCOVER under another EtherType or subtype is discarded"),
    # the unit arm: each seam on GoogleMock's mailbox window or port layer
    Mutant("app-binds-pool-after-the-mailbox", "app/ctrl_app.c", APP_BRING, APP_BRING_LATE,
           "unit", "AppComposition.U1BindsTheAppPoolBehindLwsrpBeforeTheMailbox", "unsatisfied and active"),
    Mutant("app-starts-on-an-uncarved-pool", "app/ctrl_app.c",
           "\tif (!ctrl_pool_init(&app->pool, cfg->arena, cfg->arena_bytes, cfg->classes, cfg->n_classes)) {\n"
           "\t\treturn false;\n\t}\n",
           "\t(void)ctrl_pool_init(&app->pool, cfg->arena, cfg->arena_bytes, cfg->classes, cfg->n_classes);\n",
           "unit", "AppComposition.U1AnUncarvablePoolStartsNothing", "over-saturated and active"),
    Mutant("major-unchecked", "mbx/mbx.c",
           "\t       mbx_field(id, MBX_ID_MAJOR_LSB, MBX_ID_MAJOR_WIDTH) == MBX_VERSION_MAJOR &&\n", "",
           "unit", "AppComposition.U1AnotherContractOpensNothing",
           "U1 a bitstream carrying another contract is refused",
           (("unit", "IdAndCaps/ContractField.U2RefusedAndNothingMoreRead/major", "U2 major differs"),)),
    Mutant("evt-words-unchecked", "mbx/mbx.c",
           " &&\n\t       (1u << mbx_field(caps, MBX_CAPS_EVT_WORDS_LOG2_LSB, MBX_CAPS_EVT_WORDS_LOG2_WIDTH)) == "
           "MBX_EVT_WORDS;", ";",
           "unit", "IdAndCaps/ContractField.U2RefusedAndNothingMoreRead/evt_words", "U2 evt_words differs"),
    Mutant("step-waits-twice", "loop/ctrl_loop.c", "\t\tmbx_hal_wait();\n",
           "\t\tmbx_hal_wait();\n\t\tmbx_hal_wait();\n",
           "unit", "LoopRun.U3TurnsForEverAndSleepsWhenNothingIsOwed", "U3 every turn is one pass"),
    Mutant("maap-base-shifted", "mbx/mbx.c", "mbx_hal_write32(MBX_REG_MAAP_BASE_LO, (uint32_t)base);",
           "mbx_hal_write32(MBX_REG_MAAP_BASE_LO, (uint32_t)(base >> 16));",
           "unit", "DriverUnit.D6MaapRangeWritten", "D6 MAAP_BASE_LO holds the base's low word"),
    Mutant("tx-negative-fill", "mbx/mbx.c", "if (used > tx_words[ch] || record > tx_words[ch] - used) {",
           "if (record > tx_words[ch] - used) {",
           "unit", "DriverUnit.D8TransmitRefusals", "D8 a TX_TAIL more than a ring behind TX_HEAD is no room"),
    Mutant("unknown-event-decoded-as-tick", "mbx/mbx.c", "\t} else if (ev->type == MBX_EV_TYPE_TICK) {",
           "\t} else {", "unit", "DriverUnit.D9UnknownEventTypeGrandmasterAndInterrupt",
           "D9 an event of a type the contract does not define"),
    Mutant("whole-field-loses-its-top-bit", "mbx/mbx_wire.h",
           "\tuint32_t mask = width >= 32u ? 0xFFFFFFFFu : ((1u << width) - 1u);\n\treturn (word >> lsb) & mask;",
           "\tuint32_t mask = width >= 32u ? 0x7FFFFFFFu : ((1u << width) - 1u);\n\treturn (word >> lsb) & mask;",
           "unit", "DriverUnit.D10LanesAndFieldsAtTheirBounds", "D10 and reads whole"),
    Mutant("slots-past-the-bank", "adp/adp_mbx.c", "if (first_slot + MBX_N_IF > MBX_N_TIMERS) {",
           "if (first_slot > MBX_N_TIMERS) {",
           "unit", "AdpAdapterUnit.B2SlotsPastTheTimerBankRefused", "B2 slots past the fabric's timer bank"),
    Mutant("foreign-frame-uncounted", "adp/adp_mbx.c", "\tif (i == NULL) {\n\t\tm->foreign_if++;\n\t\treturn;\n\t}",
           "\tif (i == NULL) {\n\t\t(void)m;\n\t\treturn;\n\t}",
           "unit", "AdpAdapterUnit.B3ForeignInterfaceCounted", "B3 a record, a LINK and a GM"),
    Mutant("attach-ignores-poll-room", "adp/adp_mbx.c", "&&\n\t       ctrl_loop_add_poll(l, on_poll, m);",
           "&&\n\t       (ctrl_loop_add_poll(l, on_poll, m) || true);",
           "unit", "AdpAdapterUnit.B4LoopWithNoRoomRefused", "B4 a loop with no room for the poll is refused"),
    Mutant("mmio-offset-as-index", "plat/mbx_plat_mmio.c", "(uintptr_t)(CTRL_MBX_BASE) + byte_offset)",
           "(uintptr_t)(CTRL_MBX_BASE) + byte_offset / 4u)",
           "unit", "MmioPlatform.M1OneWordAtBasePlusOffset", "M1 a write lands in the word at base + offset"),
    Mutant("wait-without-wfi", "plat/mbx_plat_mmio.c", "\tCTRL_MBX_WFI();\n", "",
           "unit", "MmioPlatform.M2WaitIsThePlatformWfi", "M2 each mbx_hal_wait() waits once"),
    # ---- #665 lane FC: the full-tuple filter on the model, one defect per rule, the RTL arms' twins ----
    # 1. tagged frames never reach a mailbox: a front end that strips a C-tag
    #    before the filter, and the RTL arm's twin, a TPID taken for any EtherType
    Mutant("model-tag-stripped", "host/mbx_model.c", MODEL_CLASSIFY, MODEL_CLASSIFY_UNTAGGED,
           "model", MODEL_GROUP + "TupleRejections", "Q1 tagged, it (adp): no RX record"),
    Mutant("model-tpid-matches-a-tuple", "host/mbx_model.c",
           "bool named = tuple_dst[j] != MBX_DST_NONE && et == tuple_ethertype[j];",
           "bool named = tuple_dst[j] != MBX_DST_NONE && (et == tuple_ethertype[j] || et == 0x8100u);",
           "model", MODEL_GROUP + "TupleRejections", "Q1 tagged, it (srp MSRP): no RX record"),
    # 2. each channel matches its exact tuple
    Mutant("model-multicast-dst-ignored", "host/mbx_model.c", "&& dst == mac &&",
           "&& (dst == mac || tuple_dst[j] == MBX_DST_MAC) &&",
           "model", MODEL_GROUP + "TupleRejections", "Q2 to another destination MAC, it (adp)"),
    Mutant("model-ethertype-ignored", "host/mbx_model.c", "if (named && tuple_dst_mac(m, j, interface, &mac)",
           "if (tuple_dst[j] != MBX_DST_NONE && tuple_dst_mac(m, j, interface, &mac)",
           "model", MODEL_GROUP + "TupleRejections", "Q3 under another control EtherType, it (adp)"),
    Mutant("model-subtype-ignored", "host/mbx_model.c", "frame[MBX_SUBTYPE_BYTE] == tuple_subtype[j])",
           "tuple_subtype[j] != 0u)", "model", MODEL_GROUP + "TupleRejections",
           "Q4 with an unassigned AVTP subtype, it (adp)"),
    # 3. own unicast is the arrival interface's MAC, never any unicast
    Mutant("model-own-any-unicast", "host/mbx_model.c", "&& dst == mac &&",
           "&& (dst == mac || (tuple_dst[j] == MBX_DST_OWN && ((dst >> 40) & 1u) == 0u)) &&",
           "model", MODEL_GROUP + "TupleRejections", "Q2 to another destination MAC, it (aecp, command)",
           (("acmp", "AcmpMailbox.B2OwnUnicastIsAToleranceAndForeignUnicastIsRefused",
             "B2 a foreign unicast is refused"),)),
    Mutant("model-own-mac-of-interface-0", "host/mbx_model.c",
           "if (tuple_dst[j] == MBX_DST_OWN && interface < MBX_N_IF) {\n\t\t*mac = m->own_mac[interface];",
           "if (tuple_dst[j] == MBX_DST_OWN) {\n\t\t(void)interface;\n\t\t*mac = m->own_mac[0];",
           "model", MODEL_GROUP + "OwnMacPerInterface",
           "Q8 another interface's own MAC, or one on an index with no interface, reaches no ring"),
    Mutant("model-own-mac-hi-dropped", "host/mbx_model.c",
           "((uint64_t)mbx_field(v, MBX_OWN_MAC_HI_MAC_LSB, MBX_OWN_MAC_HI_MAC_WIDTH) << 32)", "0u",
           "model", MODEL_GROUP + "ResetIdentityAndRegisterMasks",
           "R1 OWN_MAC_LO keeps every bit and OWN_MAC_HI keeps MAC[47:32] only"),
    # 4. AECP: (command AND target = own) OR (response AND controller = own),
    #    planted in the generated header the model reads its terms from
    Mutant("model-aecp-command-only", "mbx/mbx_contract.h", "#define MBX_CH_AECP_T1_TEST 2u",
           "#define MBX_CH_AECP_T1_TEST 0u", "model", MODEL_GROUP + "AecpBothDirections",
           "Q7 the CONTROLLER_AVAILABLE response for this controller reaches the AECP ring"),
    # 5. FILTER_MISMATCH: a tuple failure once, never an identity refusal; it sets ERR
    Mutant("model-mismatch-never-counted", "host/mbx_model.c", "\t*mismatch = control;",
           "\t*mismatch = control && false;",
           "model", MODEL_GROUP + "TupleRejections",
           "Q2 to another destination MAC, it (adp): FILTER_MISMATCH counts it once",
           (("acmp", "AcmpMailbox.B2OwnUnicastIsAToleranceAndForeignUnicastIsRefused",
             "B2 and counted once in FILTER_MISMATCH"),)),
    Mutant("model-mismatch-counts-identity-refusals", "host/mbx_model.c",
           "\tif (!rule_passes(m, c, frame, len, interface)) {\n\t\treturn false;",
           "\tif (!rule_passes(m, c, frame, len, interface)) {\n\t\tm->filter_mismatch = sat16(m->filter_mismatch);\n"
           "\t\treturn false;",
           "model", MODEL_GROUP + "TupleRejections",
           "Q5 ENTITY_DISCOVER for another entity: FILTER_MISMATCH does not count it"),
    Mutant("model-mismatch-sets-no-err", "host/mbx_model.c",
           "\t\tm->filter_mismatch = sat16(m->filter_mismatch);\n\t\tm->err = true;\n",
           "\t\tm->filter_mismatch = sat16(m->filter_mismatch);\n",
           "model", MODEL_GROUP + "FilterMismatchCount", "Q9 a mismatch sets IRQ_STATUS.ERR"),
    # ---- #665 lane FC round 2: the MAAP DEFEND to own unicast (IEEE 1722-2016 B.2.1), the RTL arms' twins ----
    # a DEFEND to this interface's own MAC is delivered: the message type read one byte early
    Mutant("model-msg-type-off-by-one", "host/mbx_model.c", "\tuint32_t msg = msg_type(frame, len);\n\tbool control",
           "\tuint32_t msg = frame[MBX_SUBTYPE_BYTE] & 0x0Fu;\n\tbool control", "model",
           MODEL_GROUP + "MaapDefendToOwnUnicast", "Q11 a DEFEND to this interface's own MAC reaches the MAAP ring"),
    # a PROBE or ANNOUNCE to it is rejected and counted: the tuple's message
    # types ignored; a message-type refusal taken as an identity refusal, uncounted
    Mutant("model-tuple-msg-type-ignored", "host/mbx_model.c",
           "((tuple_msg_mask[j] >> msg) & 1u) != 0u) {", "(((tuple_msg_mask[j] | 0xFFFFu) >> msg) & 1u) != 0u) {",
           "model",
           MODEL_GROUP + "MaapDefendToOwnUnicast", "Q11 a PROBE to this interface's own MAC: no RX record"),
    Mutant("model-msg-type-refusal-uncounted", "host/mbx_model.c",
           " &&\n\t\t    ((tuple_msg_mask[j] >> msg) & 1u) != 0u) {\n\t\t\treturn (int)(j / MBX_MAX_TUPLES);",
           ") {\n\t\t\treturn ((tuple_msg_mask[j] >> msg) & 1u) != 0u ? (int)(j / MBX_MAX_TUPLES) : -1;",
           "model", MODEL_GROUP + "MaapDefendToOwnUnicast",
           "Q11 a PROBE to this interface's own MAC: FILTER_MISMATCH counts it once"),
    # a DEFEND to a foreign unicast is rejected: the DEFEND tuple takes any unicast
    Mutant("model-defend-any-unicast", "host/mbx_model.c", "&& dst == mac &&",
           "&& (dst == mac || (tuple_msg_mask[j] != 0xFFFFu && ((dst >> 40) & 1u) == 0u)) &&",
           "model", MODEL_GROUP + "MaapDefendToOwnUnicast",
           "Q11 a DEFEND to a unicast MAC no interface owns: no RX record"),
    # the firmware's side: the own MAC per interface, the counter, the bring-up order
    Mutant("own-mac-unguarded", "mbx/mbx.c",
           "\tif (interface >= MBX_N_IF) {\n\t\treturn false;\n\t}\n\tmbx_hal_write32(iff_reg",
           "\tmbx_hal_write32(iff_reg", "unit", "DriverUnit.D11OwnMacPerInterfaceAndTheMismatchCount",
           "D11 an interface past the contract's is refused"),
    Mutant("own-mac-halves-swapped", "mbx/mbx.c",
           "mbx_place((uint32_t)mac, MBX_OWN_MAC_LO_MAC_LSB, MBX_OWN_MAC_LO_MAC_WIDTH)",
           "mbx_place((uint32_t)(mac >> 32), MBX_OWN_MAC_LO_MAC_LSB, MBX_OWN_MAC_LO_MAC_WIDTH)",
           "unit", "DriverUnit.D11OwnMacPerInterfaceAndTheMismatchCount", "D11 OWN_MAC_LO holds MAC[31:0]",
           (("port", "Driver.D12OwnMacAndMismatchOnTheModel", "D12 an AEM_COMMAND to it on interface 0 passes"),)),
    Mutant("mismatch-read-from-bus-err", "mbx/mbx.c", "mbx_hal_read32(MBX_REG_FILTER_MISMATCH)",
           "mbx_hal_read32(MBX_REG_BUS_ERR)", "unit", "DriverUnit.D11OwnMacPerInterfaceAndTheMismatchCount",
           "D11 FILTER_MISMATCH is read as its COUNT field",
           (("port", "Driver.D12OwnMacAndMismatchOnTheModel", "D12 FILTER_MISMATCH reads the one tuple failure"),)),
    Mutant("own-mac-after-the-channels-open", "loop/ctrl_loop.c", LOOP_OWN_MAC + LOOP_OPEN, LOOP_OPEN + LOOP_OWN_MAC,
           "port", "LoopBring.L1OpenOrder", "L1 every interface's OWN_MAC is written before any channel opens"),
    Mutant("app-own-mac-not-the-entity-mac", "app/ctrl_app.c", "\t\town_mac[i] = cfg->entity->mac;\n",
           "\t\town_mac[i] = cfg->entity->mac & 0xFFFFFFFFull;\n",
           "unit", "AppComposition.U4EveryInterfaceOwnsTheEntityMacBeforeAChannelOpens", "OWN_MAC is the entity's MAC",
           (("acmp", "AcmpMailbox.B2OwnUnicastIsAToleranceAndForeignUnicastIsRefused",
             "B2 a command to this interface's own unicast MAC passes"),)),
) + acmp_mutants.MUTANTS


#: Lane F3's test sources. Every test in them is named by at least one defect,
#: which `unnamed_tests` proves before any is planted (the rule lane F1's
#: store suite proves with nvm_mutants.unnamed_checks).
NAMED_SOURCES = ("test_acmp.cpp", "test_acmp_mbx.cpp", "acmp_walk.cpp", "test_acmp_nvm.cpp")


def unnamed_tests(test_dir: Path = Path(__file__).resolve().parent) -> list[str]:
    """The tests of NAMED_SOURCES no defect names: a test with no planted
    defect is unproven. A parameterised test is named through any instance."""
    named = {t.split("/")[1] if "/" in t else t for m in MUTANTS for _, t, _ in m.kills()}
    tests = [f"{suite}.{name}" for src in NAMED_SOURCES
             for suite, name in re.findall(r"^TEST(?:_F|_P)?\((\w+), (\w+)\)", (test_dir / src).read_text(), re.M)]
    return [t for t in tests if t not in named]


MUTANTS += maap_mutants(Mutant)


def plant(m: Mutant, root: Path) -> Path:
    """A copy of the firmware tree with the mutant written into it."""
    copy = root / m.name / "ctrl"
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(CTRL, copy, ignore=shutil.ignore_patterns("__pycache__"))
    target = copy / m.path
    text = target.read_text(encoding="utf-8")
    if text.count(m.old) != 1:
        raise Refusal(f"mutant {m.name}: its fixture occurs {text.count(m.old)} times in {m.path}")
    target.write_text(text.replace(m.old, m.new), encoding="utf-8")
    return copy


def names(line: str, test: str, needle: str) -> bool:
    """A `[FAIL] <test>: ...` line of that test (or of an instance of it)
    carrying the check's words. The RV32 arm's lines name no test ("")."""
    rest = line.split("[FAIL]", 1)[1] if "[FAIL]" in line else None
    if rest is None:
        return False
    return rest.split(":", 1)[0].strip().startswith(test) and needle in rest


def caught(test: str, needle: str, outcome: Outcome) -> bool:
    """The named test failed on the check's words in a completed run of its arm."""
    return outcome.rc == 1 and any(names(ln, test, needle) for ln in outcome.log.splitlines())


def lwsrp_pin_arms(root: Path, lwsrp: Path) -> int:
    """The lwSRP pin refuses, by name, a scratch clone of the pin with one
    edit to a compiled source, and the same clone at another revision.
    Returns the escapes."""
    clone = root / "lwsrp-pin"
    if clone.exists():
        shutil.rmtree(clone)
    res = ctrl_arms.run(["git", "clone", "--quiet", "--no-hardlinks", str(lwsrp), str(clone)])
    if res.returncode != 0:
        raise Refusal(f"cannot clone {lwsrp} for the pin arms: {res.stderr.strip()}")
    ctrl_arms.run(["git", "-C", str(clone), "checkout", "--quiet", ctrl_arms.LWSRP_REV])
    escaped = 0
    target = clone / ctrl_arms.LWSRP_SOURCES[0]
    pristine = target.read_text(encoding="utf-8")
    arms = (("a compiled source edited", lambda: target.write_text(pristine + "/* local */\n", encoding="utf-8"),
             "differs from the pinned"),
            ("another revision checked out",
             lambda: ctrl_arms.run(["git", "-C", str(clone), "checkout", "--quiet", "HEAD~1"]), "is not the pinned"))
    for what, spoil, needle in arms:
        target.write_text(pristine, encoding="utf-8")
        spoil()
        try:
            ctrl_arms.lwsrp_pin(clone)
            ok, detail = False, "accepted"
        except Refusal as exc:
            ok, detail = needle in str(exc), str(exc)
        print(f"[{'ok' if ok else 'ESCAPED'}] lwSRP pin, {what}: {detail}")
        escaped += 0 if ok else 1
    shutil.rmtree(clone)
    return escaped


def sliced(part: tuple[int, int]) -> tuple[Mutant, ...]:
    """Slice k of n of the table, contiguous and in table order: every mutant
    is in exactly one slice, so n runs together plant the whole table."""
    k, n = part
    size = -(-len(MUTANTS) // n)
    return MUTANTS[(k - 1) * size:k * size]


def campaign(root: Path, reuse: Path, jobs: int, part: tuple[int, int] = (1, 1)) -> bool:
    """Plant every mutant of slice `part` (k of n; the whole table by
    default); True when one escaped. One build serves every copy, so a test
    object is compiled again only where a planted header changes what it
    sees."""
    arms = {"model": ctrl_arms.arm_model, "port": ctrl_arms.arm_port, "adp": ctrl_arms.arm_adp,
            "unit": ctrl_arms.arm_unit, "walk": ctrl_arms.arm_walk, "acmp": ctrl_arms.arm_acmp,
            "acmpwalk": ctrl_arms.arm_acmpwalk, "acmpnvm": ctrl_arms.arm_acmpnvm, "acmpif2": ctrl_arms.arm_acmpif2,
            "entity": ctrl_arms.arm_entity,
            "maap": ctrl_arms.arm_maap, "maap_debug": ctrl_arms.arm_maap_debug, "maap_if2": ctrl_arms.arm_maap_if2,
            "rv32": lambda tree: ctrl_arms.arm_rv32(tree, True),
            "reentry_debug": ctrl_arms.arm_reentry_debug, "reentry_release": ctrl_arms.arm_reentry_release}
    build = fw_gtest.Build(jobs=jobs)
    unnamed = unnamed_tests()
    for test in unnamed:
        print(f"[ESCAPED] no defect names the test {test}")
    escaped = 0
    table = sliced(part)
    for m in table:
        tree = Tree(plant(m, root), root / m.name / "build", reuse, build)
        missed = []
        fails: list[str] = []
        for arm, test, needle in m.kills():
            try:
                outcome = arms[arm](tree)
            except Refusal as exc:
                outcome = Outcome(arm, 2, f"refused: {exc}")
            fails += [ln.strip() for ln in outcome.log.splitlines() if "[FAIL]" in ln]
            if not caught(test, needle, outcome):
                missed.append(f"{arm}: {test or 'its check'} on {needle!r}")
        print(f"[{'ok' if not missed else 'ESCAPED'}] mutant {m.name} ({', '.join(k[0] for k in m.kills())}): "
              f"{len(fails)} check(s) failed{'' if not missed else ', none named ' + '; '.join(missed)}")
        if fails:
            print(f"    first: {fails[0]}")
        escaped += 0 if not missed else 1
        shutil.rmtree(root / m.name, ignore_errors=True)
    where = "" if part == (1, 1) else f" (slice {part[0]} of {part[1]} of {len(MUTANTS)})"
    print(f"mutants: {len(table) - escaped} of {len(table)} caught{where}"
          f"{'' if not unnamed else f'; {len(unnamed)} test(s) named by no defect'}")
    return escaped != 0 or bool(unnamed)
