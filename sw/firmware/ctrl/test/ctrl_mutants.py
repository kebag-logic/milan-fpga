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
from dataclasses import dataclass
from pathlib import Path

import ctrl_arms
import fw_gtest
from ctrl_build import CTRL, Outcome, Refusal, Tree


@dataclass(frozen=True)
class Mutant:
    """One planted defect."""

    name: str
    path: str
    old: str
    new: str
    arm: str
    test: str
    needle: str
    also: tuple[tuple[str, str, str], ...] = ()

    def kills(self) -> tuple[tuple[str, str, str], ...]:
        """Every (arm, test, words) that must fail on this defect."""
        return ((self.arm, self.test, self.needle), *self.also)


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
           (("acmp", "AcmpMailbox.B2OwnUnicastIsAToleranceAndForeignUnicastIsRefused", "B2 a foreign unicast is refused"),)),
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
           "\tif (!rule_passes(m, c, frame, len)) {\n\t\treturn false;",
           "\tif (!rule_passes(m, c, frame, len)) {\n\t\tm->filter_mismatch = sat16(m->filter_mismatch);\n"
           "\t\treturn false;",
           "model", MODEL_GROUP + "TupleRejections",
           "Q5 ENTITY_DISCOVER for another entity: FILTER_MISMATCH does not count it"),
    Mutant("model-mismatch-sets-no-err", "host/mbx_model.c",
           "\t\tm->filter_mismatch = sat16(m->filter_mismatch);\n\t\tm->err = true;\n",
           "\t\tm->filter_mismatch = sat16(m->filter_mismatch);\n",
           "model", MODEL_GROUP + "FilterMismatchCount", "Q9 a mismatch sets IRQ_STATUS.ERR"),
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
    # ---- #665 lane F3: ACMP. Every check of the acmp, acmpwalk and acmpnvm arms has a defect of its own ----
    # the configuration (A0)
    Mutant("acmp-init-no-interface", "acmp/acmp.c",
           "if (cfg->n_interfaces == 0u || cfg->n_interfaces > ACMP_MAX_INTERFACES ||",
           "if (cfg->n_interfaces > ACMP_MAX_INTERFACES ||",
           "acmp", "AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold", "A0 no interface is refused"),
    Mutant("acmp-init-too-many-sinks", "acmp/acmp.c", "cfg->n_sinks > ACMP_MAX_SINKS ||",
           "cfg->n_sinks > ACMP_MAX_SINKS + 1u ||",
           "acmp", "AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold", "A0 more sinks than ACMP_MAX_SINKS"),
    Mutant("acmp-init-too-many-sources", "acmp/acmp.c", "cfg->n_sources > ACMP_MAX_SOURCES) {",
           "cfg->n_sources > ACMP_MAX_SOURCES + 1u) {",
           "acmp", "AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold", "A0 more sources than ACMP_MAX_SOURCES"),
    Mutant("acmp-init-sink-interface", "acmp/acmp.c", "\t\tif (cfg->sink_interface[k] >= cfg->n_interfaces) {",
           "\t\tif (cfg->sink_interface[k] > cfg->n_interfaces) {",
           "acmp", "AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold",
           "A0 a sink on an interface the entity lacks is refused"),
    Mutant("acmp-init-source-interface", "acmp/acmp.c", "\t\tif (cfg->source_interface[k] >= cfg->n_interfaces) {",
           "\t\tif (cfg->source_interface[k] > cfg->n_interfaces) {",
           "acmp", "AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold",
           "A0 a source on an interface the entity lacks is refused"),
    Mutant("acmp-init-reads-the-seed", "acmp/acmp.c",
           "\ta->rng = (uint32_t)cfg->entity_id ^ (uint32_t)(cfg->entity_id >> 32) ^ 0x7F4A7C15u;",
           "\ta->rng = (uint32_t)cfg->entity_id ^ (uint32_t)(cfg->entity_id >> 32) ^ 0x7F4A7C15u ^ p_seed(a);",
           "acmp", "AcmpCore.A0EverySinkStartsUnboundAndNothingIsCalled", "A0 init calls no port",
           (("acmp", "AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract",
             "U5 composing touches no mailbox register"),)),
    # a wrong number in acmp.h: the tests spell the standards' own (acmp_fake.hpp spec)
    Mutant("acmp-header-no-resp-2s", "acmp/acmp.h", "#define ACMP_TMR_NO_RESP_MS 200u", "#define ACMP_TMR_NO_RESP_MS 2000u",
           "acmp", "AcmpCore.A1BindFromUnboundRespondsThenProbes", "A1 and TMR_NO_RESP armed 200 ms",
           (("acmpwalk", "Table530/ListenerWalk.Graded/BIND_NEW_UNB", "the timer's deadline"),)),
    Mutant("acmp-header-retry-2s", "acmp/acmp.h", "#define ACMP_TMR_RETRY_MS 4000u", "#define ACMP_TMR_RETRY_MS 2000u",
           "acmp", "AcmpCore.A9FailureWaitsForTheRetry", "A9 and TMR_RETRY 4 s",
           (("acmpwalk", "Table530/ListenerWalk.Graded/PROBE_FAIL_PWR", "the timer's deadline"),)),
    Mutant("acmp-header-no-tk-5s", "acmp/acmp.h", "#define ACMP_TMR_NO_TK_MS 10000u", "#define ACMP_TMR_NO_TK_MS 5000u",
           "acmp", "AcmpCore.A8SuccessSettles", "A8 TMR_NO_RESP stopped and TMR_NO_TK 10 s started"),
    Mutant("acmp-header-valid-time-in-seconds", "acmp/acmp.h", "#define ACMP_VALID_TIME_UNIT_MS 2000u",
           "#define ACMP_VALID_TIME_UNIT_MS 1000u",
           "acmp", "AcmpCore.A22AvailableDiscoversWhenTheGrandmasterMatches",
           "A22 TMR_NO_ADP is the received valid_time in two-second units"),
    Mutant("acmp-header-listener-unknown-is-2", "acmp/acmp.h", "#define ACMP_STATUS_LISTENER_UNKNOWN_ID 1u",
           "#define ACMP_STATUS_LISTENER_UNKNOWN_ID 2u",
           "acmp", "AcmpCore.A2UnknownSinkIsAnsweredListenerUnknownId", "A2 LISTENER_UNKNOWN_ID, the command's fields echoed"),
    Mutant("acmp-header-registering-failed-bit", "acmp/acmp.h", "#define ACMP_FLAG_REGISTERING_FAILED 0x0040u",
           "#define ACMP_FLAG_REGISTERING_FAILED 0x0200u",
           "acmp", "AcmpCore.A2GetRxStateReportsStreamingWaitAndRegisteringFailed", "REGISTERING_FAILED 1 (Table 5.39)"),
    Mutant("acmp-header-cdl-84", "acmp/acmp.h", "#define ACMP_CONTROL_DATA_LENGTH 44u", "#define ACMP_CONTROL_DATA_LENGTH 84u",
           "acmp", "AcmpCore.A1BindFromUnboundRespondsThenProbes", "A1 every frame goes to the ACMP multicast address"),
    # BIND_RX from UNBOUND (A1, 5.5.3.5.3)
    Mutant("acmp-bind-count-0", "acmp/acmp.c", "\tr.count = 1u;\n\tr.flags = cmd->flags & ACMP_FLAG_STREAMING_WAIT;",
           "\tr.count = 0u;\n\tr.flags = cmd->flags & ACMP_FLAG_STREAMING_WAIT;",
           "acmp", "AcmpCore.A1BindFromUnboundRespondsThenProbes", "A1 BIND_RX_RESPONSE is Table 5.32",
           (("acmpwalk", "Table530/ListenerWalk.Graded/BIND_NEW_UNB", "frame 0 byte for byte"),)),
    Mutant("acmp-probe-without-fast-connect", "acmp/acmp.c",
           "\tp.flags = ACMP_FLAG_FAST_CONNECT;\n\tuint8_t frame[ACMP_FRAME_BYTES];",
           "\tp.flags = 0u;\n\tuint8_t frame[ACMP_FRAME_BYTES];",
           "acmp", "AcmpCore.A1BindFromUnboundRespondsThenProbes", "A1 PROBE_TX_COMMAND is Table 5.33",
           (("acmpwalk", "Table530/ListenerWalk.Graded/BIND_NEW_UNB", "frame 1 byte for byte"),)),
    Mutant("acmp-probe-before-response", "acmp/acmp.c",
           "\ts->started = !sw;\n\tbind_response(a, interface, k, cmd);\n\tdisc_start(s);\n\tprobe(a, k);",
           "\ts->started = !sw;\n\tdisc_start(s);\n\tprobe(a, k);\n\tbind_response(a, interface, k, cmd);",
           "acmp", "AcmpCore.A1BindFromUnboundRespondsThenProbes", "A1 BIND_RX_RESPONSE is Table 5.32"),
    Mutant("acmp-no-resp-2s", "acmp/acmp.c", "\tsm_timer(a, s, ACMP_TIMER_NO_RESP, ACMP_TMR_NO_RESP_MS);",
           "\tsm_timer(a, s, ACMP_TIMER_NO_RESP, ACMP_TMR_NO_RESP_MS * 10u);",
           "acmp", "AcmpCore.A1BindFromUnboundRespondsThenProbes", "A1 and TMR_NO_RESP armed 200 ms",
           (("acmp", "AcmpMailbox.B3TheTimersRunOnTheInterfaceSlot", "B3 TMR_NO_RESP is armed"),)),
    Mutant("acmp-bind-starts-no-discovery", "acmp/acmp.c",
           "\tbind_response(a, interface, k, cmd);\n\tdisc_start(s);\n", "\tbind_response(a, interface, k, cmd);\n",
           "acmp", "AcmpCore.A1BindFromUnboundRespondsThenProbes", "A1 the discovery machine starts",
           (("acmpwalk", "Table530/ListenerWalk.Graded/BIND_NEW_UNB", "discovery runs exactly while"),)),
    Mutant("acmp-bind-change-before-response", "acmp/acmp.c",
           "\tbind_response(a, interface, k, cmd);\n\tdisc_start(s);\n",
           "\tp_changed(a, k);\n\tbind_response(a, interface, k, cmd);\n\tdisc_start(s);\n",
           "acmp", "AcmpCore.A1BindFromUnboundRespondsThenProbes", "A1 the change is reported after the response"),
    Mutant("acmp-nothing-persisted", "acmp/acmp.c",
           "\t\t\tmemcpy(s->saved, record, ACMP_BINDING_BYTES);\n\t\t\tp_persist(a, k);",
           "\t\t\tmemcpy(s->saved, record, ACMP_BINDING_BYTES);\n\t\t\t(void)p_persist;",
           "acmp", "AcmpCore.A1BindFromUnboundRespondsThenProbes", "A1 the binding is saved",
           (("acmpnvm", "AcmpStore.N1ABindSurvivesAPowerCycleAndFastConnects", "N1 the bind marks its record"),)),
    Mutant("acmp-unbind-not-persisted", "acmp/acmp.c", "\t\tif (!same_record(record, s->saved)) {",
           "\t\tif (!same_record(record, s->saved) && s->bound) {",
           "acmpnvm", "AcmpStore.N2AnUnbindIsSavedAsAnUnboundRecord", "N2 the unbind marks the record",
           (("acmpwalk", "Table530/ListenerWalk.Graded/UNBIND_PWR", "the store marked"),)),
    Mutant("acmp-rebind-not-persisted", "acmp/acmp.c", "\t\tif (!same_record(record, s->saved)) {",
           "\t\tif (!same_record(record, s->saved) && (s->saved[0] & 0x01u) == 0u) {",
           "acmpnvm", "AcmpStore.N4AnUnreadSlotRefusesPersistence", "N4 a new bind is answered and taken, and its record marked",
           (("acmp", "AcmpCore.A6BindAnotherSourceRestartsTheSink", "A6 the new binding is saved"),)),
    Mutant("acmp-streaming-wait-ignored", "acmp/acmp.c",
           "\t// START_STREAMING (Milan v1.2 5.3.8.7)\n\ts->started = !sw;",
           "\t// START_STREAMING (Milan v1.2 5.3.8.7)\n\ts->started = true;",
           "acmp", "AcmpCore.A1BindFromUnboundRespondsThenProbes", "STREAMING_WAIT binds it stopped"),
    Mutant("acmp-sw-read-from-fast-connect", "acmp/acmp.c",
           "\tbool sw = (cmd->flags & ACMP_FLAG_STREAMING_WAIT) != 0u;",
           "\tbool sw = (cmd->flags & ACMP_FLAG_FAST_CONNECT) != 0u;",
           "acmp", "AcmpCore.A2GetRxStateReportsStreamingWaitAndRegisteringFailed", "STREAMING_WAIT saved"),
    # GET_RX_STATE (A2)
    Mutant("acmp-getrx-count-unbound", "acmp/acmp.c", "\tif (s->bound) {\n\t\tr.count = 1u;",
           "\tr.count = 1u;\n\tif (s->bound) {", "acmp", "AcmpCore.A2GetRxStateInEveryState",
           "A2 GET_RX_STATE_RESPONSE is Table 5.34/5.37/5.38/5.39",
           (("acmpwalk", "Table530/ListenerWalk.Graded/GETRX_UNB", "frame 0 byte for byte"),)),
    Mutant("acmp-getrx-no-fast-connect", "acmp/acmp.c",
           "\t\tr.flags = (uint16_t)(ACMP_FLAG_FAST_CONNECT | (s->binding.streaming_wait ? ACMP_FLAG_STREAMING_WAIT : 0u));",
           "\t\tr.flags = (uint16_t)(s->binding.streaming_wait ? ACMP_FLAG_STREAMING_WAIT : 0u);",
           "acmp", "AcmpCore.A2GetRxStateInEveryState", "A2 GET_RX_STATE_RESPONSE is Table 5.34/5.37/5.38/5.39",
           (("acmpwalk", "Table530/ListenerWalk.Graded/GETRX_PWR", "frame 0 byte for byte"),)),
    Mutant("acmp-getrx-no-registering-failed", "acmp/acmp.c", "\t\tr.flags |= ACMP_FLAG_REGISTERING_FAILED;",
           "\t\tr.flags |= 0u;", "acmp", "AcmpCore.A2GetRxStateReportsStreamingWaitAndRegisteringFailed",
           "REGISTERING_FAILED 1 (Table 5.39)"),
    Mutant("acmp-unknown-sink-silent", "acmp/acmp.c",
           "\t\tstruct pdu r = echo(cmd, ACMP_STATUS_LISTENER_UNKNOWN_ID);         // Table 5.27\n"
           "\t\trespond(a, interface, &r, 0u);",
           "\t\tstruct pdu r = echo(cmd, ACMP_STATUS_LISTENER_UNKNOWN_ID);         // Table 5.27\n\t\t(void)r;",
           "acmp", "AcmpCore.A2UnknownSinkIsAnsweredListenerUnknownId", "A2 a command for a sink the entity lacks"),
    # UNBIND_RX (A3)
    Mutant("acmp-unbind-echoes-the-talker", "acmp/acmp.c",
           "\tr.talker = 0u;\n\tr.talker_uid = 0u;\n\trespond(a, interface, &r, 1u << k);",
           "\trespond(a, interface, &r, 1u << k);",
           "acmp", "AcmpCore.A3UnbindInEveryState", "A3 UNBIND_RX_RESPONSE is Table 5.36",
           (("acmpwalk", "Table530/ListenerWalk.Graded/UNBIND_PWR", "frame 0 byte for byte"),)),
    Mutant("acmp-unbind-keeps-srp", "acmp/acmp.c",
           "\tstruct acmp_sink *s = &a->sinks[k];\n"
           "\tif (s->state == ACMP_SETTLED_NO_RSV || s->state == ACMP_SETTLED_RSV_OK) {\n"
           "\t\tsrp_stop(a, k);\n\t}\n\tdisc_stop(s);\n\ts->bound = false;",
           "\tstruct acmp_sink *s = &a->sinks[k];\n\tdisc_stop(s);\n\ts->bound = false;",
           "acmp", "AcmpCore.A3UnbindInEveryState", "A3 a settled sink stops SRP before the response",
           (("acmpwalk", "Table530/ListenerWalk.Graded/UNBIND_SNR", "SRP stopped"),)),
    Mutant("acmp-unbind-srp-after-response", "acmp/acmp.c",
           "\tstruct acmp_sink *s = &a->sinks[k];\n"
           "\tif (s->state == ACMP_SETTLED_NO_RSV || s->state == ACMP_SETTLED_RSV_OK) {\n"
           "\t\tsrp_stop(a, k);\n\t}\n\tdisc_stop(s);\n\ts->bound = false;\n"
           "\tmemset(&s->binding, 0, sizeof s->binding);\n\ts->started = false;\n"
           "\ts->probing = ACMP_PROBING_DISABLED;\n\ts->acmp_status = ACMP_STATUS_SUCCESS;\n\tsm_stop(s);\n"
           "\tstruct pdu r = echo(cmd, ACMP_STATUS_SUCCESS);             // Table 5.36\n"
           "\tr.talker = 0u;\n\tr.talker_uid = 0u;\n\trespond(a, interface, &r, 1u << k);\n",
           "\tstruct acmp_sink *s = &a->sinks[k];\n"
           "\tbool settled = s->state == ACMP_SETTLED_NO_RSV || s->state == ACMP_SETTLED_RSV_OK;\n"
           "\tdisc_stop(s);\n\ts->bound = false;\n"
           "\tmemset(&s->binding, 0, sizeof s->binding);\n\ts->started = false;\n"
           "\ts->probing = ACMP_PROBING_DISABLED;\n\ts->acmp_status = ACMP_STATUS_SUCCESS;\n\tsm_stop(s);\n"
           "\tstruct pdu r = echo(cmd, ACMP_STATUS_SUCCESS);\n"
           "\tr.talker = 0u;\n\tr.talker_uid = 0u;\n\trespond(a, interface, &r, 1u << k);\n"
           "\tif (settled) {\n\t\tsrp_stop(a, k);\n\t}\n",
           "acmp", "AcmpCore.A3UnbindInEveryState", "A3 a settled sink stops SRP before the response"),
    Mutant("acmp-unbind-keeps-discovery", "acmp/acmp.c", "\tdisc_stop(s);\n\ts->bound = false;",
           "\ts->bound = false;", "acmp", "AcmpCore.A3UnbindInEveryState", "A3 then UNBOUND, binding cleared",
           (("acmpwalk", "Table530/ListenerWalk.Graded/UNBIND_PWR", "discovery runs exactly while"),)),
    Mutant("acmp-unbind-change-before-response", "acmp/acmp.c",
           "\tr.talker_uid = 0u;\n\trespond(a, interface, &r, 1u << k);",
           "\tr.talker_uid = 0u;\n\tp_changed(a, k);\n\trespond(a, interface, &r, 1u << k);",
           "acmp", "AcmpCore.A3UnbindInEveryState", "A3 the change is reported after the response (#653)"),
    # the lock (A4)
    Mutant("acmp-not-authorized-is-13", "acmp/acmp.h", "#define ACMP_STATUS_CONTROLLER_NOT_AUTHORIZED 16u",
           "#define ACMP_STATUS_CONTROLLER_NOT_AUTHORIZED 13u",
           "acmp", "AcmpCore.A4LockedByAnotherControllerRefusesBindAndUnbind", "A4 CONTROLLER_NOT_AUTHORIZED (16",
           (("acmpwalk", "ListenerScenario.LD3TheLockRefusalStatus", "LD3 the firmware sends 16"),)),
    Mutant("acmp-lock-ignored", "acmp/acmp.c", "\tif (p_locked(a, &holder) && holder != cmd->controller) {",
           "\tif (p_locked(a, &holder) && holder != cmd->controller && false) {",
           "acmp", "AcmpCore.A4LockedByAnotherControllerRefusesBindAndUnbind", "A4 one response"),
    Mutant("acmp-lock-refuses-the-holder", "acmp/acmp.c",
           "\tif (p_locked(a, &holder) && holder != cmd->controller) {",
           "\tif (p_locked(a, &holder)) {\n\t\t(void)cmd;",
           "acmp", "AcmpCore.A4TheLockingControllerPassesAndGetRxStateIsNotLocked", "A4 the locking controller binds"),
    Mutant("acmp-get-rx-state-locked", "acmp/acmp.c",
           "\tif (cmd->msg == ACMP_MSG_GET_RX_STATE_COMMAND) {\n\t\tget_rx_state(a, interface, k, cmd);\n"
           "\t} else if (lock_refuses(a, cmd)) {",
           "\tif (lock_refuses(a, cmd)) {\n\t\tstruct pdu r = echo(cmd, ACMP_STATUS_CONTROLLER_NOT_AUTHORIZED);\n"
           "\t\trespond(a, interface, &r, 0u);\n"
           "\t} else if (cmd->msg == ACMP_MSG_GET_RX_STATE_COMMAND) {\n\t\tget_rx_state(a, interface, k, cmd);\n"
           "\t} else if (lock_refuses(a, cmd)) {",
           "acmp", "AcmpCore.A4TheLockingControllerPassesAndGetRxStateIsNotLocked", "A4 GET_RX_STATE asks no lock"),
    # re-binds (A5, A6)
    Mutant("acmp-rebind-same-reprobes", "acmp/acmp.c",
           "\t\ts->started = !sw;\n\t\tbind_response(a, interface, k, cmd);\n\t\treturn;\n\t}",
           "\t\ts->started = !sw;\n\t\tbind_response(a, interface, k, cmd);\n\t}",
           "acmp", "AcmpCore.A5RebindTheSameSourceUpdatesAndExits", "A5 a re-bind of the same source sends the response alone",
           (("acmpwalk", "Table530/ListenerWalk.Graded/BIND_SAME_PWR", "frames"),)),
    Mutant("acmp-rebind-same-keeps-the-controller", "acmp/acmp.c",
           "\t\ts->binding.controller_entity_id = cmd->controller;\n\t\ts->binding.streaming_wait = sw;",
           "\t\ts->binding.streaming_wait = sw;",
           "acmp", "AcmpCore.A5RebindTheSameSourceUpdatesAndExits", "A5 the controller and STREAMING_WAIT are updated"),
    Mutant("acmp-bind-new-keeps-srp", "acmp/acmp.c",
           "\t\tsrp_stop(a, k);                                 // 5.5.3.5.37 and .43 step 3", "\t\t(void)k;",
           "acmp", "AcmpCore.A6BindAnotherSourceRestartsTheSink", "A6 SRP is stopped and its parameters cleared",
           (("acmpwalk", "Table530/ListenerWalk.Graded/BIND_NEW_SNR", "SRP stopped"),)),
    Mutant("acmp-bind-same-talker-is-the-same-source", "acmp/acmp.c",
           "if (s->bound && cmd->talker == s->binding.talker_entity_id && "
           "cmd->talker_uid == s->binding.talker_unique_id) {",
           "if (s->bound && cmd->talker == s->binding.talker_entity_id) {",
           "acmp", "AcmpCore.A6TheSameTalkerAnotherSourceIsANewBinding",
           "A6 the same talker with another talker_unique_id is a new source"),
    Mutant("acmp-sequence-id-never-advances", "acmp/acmp.c",
           "\ta->sequence_id = (uint16_t)(a->sequence_id + 1u);\n", "",
           "acmp", "AcmpCore.A12DelaySendsANewProbe", "A12 a new PROBE_TX_COMMAND with the next sequence_id",
           (("acmp", "AcmpCore.A16OneCounterForEveryNewProbe", "A16 each new PROBE_TX_COMMAND takes the next"),)),
    Mutant("acmp-sequence-id-per-sink", "acmp/acmp.c",
           "\ts->probe_seq = a->sequence_id;\n\ta->sequence_id = (uint16_t)(a->sequence_id + 1u);",
           "\ts->probe_seq = (uint16_t)(s->probe_seq + 1u);",
           "acmp", "AcmpCore.A16OneCounterForEveryNewProbe", "A16 each new PROBE_TX_COMMAND takes the next",
           (("acmpwalk", "Table530/ListenerWalk.Graded/BIND_NEW_UNB", "frame 1 byte for byte"),)),
    # probe responses (A7 to A9)
    Mutant("acmp-response-keyed-on-the-source", "acmp/acmp.c",
           "\tunsigned k = rsp->listener_uid;\n\tif (k >= a->cfg.n_sinks) {\n"
           "\t\ta->unknown_sink++;                              // 5.5.3.1: ignored",
           "\tunsigned k = 0;\n\twhile (k < a->cfg.n_sinks && (a->sinks[k].probe_talker != rsp->talker ||\n"
           "\t\t\t\t\t a->sinks[k].probe_talker_uid != rsp->talker_uid)) {\n\t\tk++;\n\t}\n"
           "\tif (k >= a->cfg.n_sinks) {\n\t\ta->unknown_sink++;",
           "acmp", "AcmpCore.A7ResponsesKeyOnTheListenerUniqueId", "A7 the response belongs to the sink"),
    Mutant("acmp-guard-controller-dropped", "acmp/acmp.c",
           "\tif (rsp->controller != s->probe_controller || rsp->talker != s->probe_talker ||",
           "\tif (rsp->talker != s->probe_talker ||",
           "acmp", "AcmpCore.A7EachGuardTermIsChecked", "A7 a response with another controller",
           (("acmpwalk", "ListenerScenario.LW2GuardsUnknownSinksAndForeignMessages", "LW2 a probe response wrong in guard term 0"),)),
    Mutant("acmp-guard-talker-dropped", "acmp/acmp.c",
           "\tif (rsp->controller != s->probe_controller || rsp->talker != s->probe_talker ||",
           "\tif (rsp->controller != s->probe_controller ||",
           "acmp", "AcmpCore.A7EachGuardTermIsChecked", "A7 a response with another controller",
           (("acmpwalk", "ListenerScenario.LW2GuardsUnknownSinksAndForeignMessages", "LW2 a probe response wrong in guard term 1"),)),
    Mutant("acmp-guard-unique-id-dropped", "acmp/acmp.c",
           "\t    rsp->talker_uid != s->probe_talker_uid || rsp->seq != s->probe_seq) {",
           "\t    rsp->seq != s->probe_seq) {",
           "acmp", "AcmpCore.A7EachGuardTermIsChecked", "A7 a response with another controller",
           (("acmpwalk", "ListenerScenario.LW2GuardsUnknownSinksAndForeignMessages", "LW2 a probe response wrong in guard term 2"),)),
    Mutant("acmp-guard-sequence-id-dropped", "acmp/acmp.c",
           "\t    rsp->talker_uid != s->probe_talker_uid || rsp->seq != s->probe_seq) {",
           "\t    rsp->talker_uid != s->probe_talker_uid) {",
           "acmp", "AcmpCore.A7EachGuardTermIsChecked", "A7 a response with another controller",
           (("acmpwalk", "ListenerScenario.LW2GuardsUnknownSinksAndForeignMessages", "LW2 a probe response wrong in guard term 3"),)),
    Mutant("acmp-guard-reads-the-binding", "acmp/acmp.c", "\tif (rsp->controller != s->probe_controller ||",
           "\tif (rsp->controller != s->binding.controller_entity_id ||",
           "acmp", "AcmpCore.A7TheGuardReadsTheSentProbeNotTheBinding",
           "A7 the answer to the probe sent before a re-bind still matches"),
    Mutant("acmp-responses-taken-outside-probing", "acmp/acmp.c",
           "\tif (s->state != ACMP_PRB_W_RESP && s->state != ACMP_PRB_W_RESP2) {\n\t\ta->rx_ignored++;",
           "\tif (false) {\n\t\ta->rx_ignored++;",
           "acmp", "AcmpCore.A7ResponsesOutsideProbingAreIgnored", "A7 RCV_PROBE_TX_RESP is ignored outside",
           (("acmpwalk", "Table530/ListenerWalk.Graded/PROBE_OK_SNR", "SRP started"),)),
    Mutant("acmp-vlan-masked", "acmp/acmp.c", "\ts->stream.vlan_id = rsp->vlan;",
           "\ts->stream.vlan_id = (uint16_t)(rsp->vlan & 0x0FFFu);",
           "acmp", "AcmpCore.A8SuccessSettles", "A8 with the response's stream_id, stream_dest_mac and stream_vlan_id exactly"),
    Mutant("acmp-no-tk-1s", "acmp/acmp.c", "\tsm_timer(a, s, ACMP_TIMER_NO_TK, ACMP_TMR_NO_TK_MS);",
           "\tsm_timer(a, s, ACMP_TIMER_NO_TK, ACMP_TMR_NO_TK_MS / 10u);",
           "acmp", "AcmpCore.A8SuccessSettles", "A8 TMR_NO_RESP stopped and TMR_NO_TK 10 s started",
           (("acmpwalk", "Table530/ListenerWalk.Graded/PROBE_OK_PWR", "the timer's deadline"),)),
    Mutant("acmp-settle-starts-no-srp", "acmp/acmp.c", "\ts->stream.vlan_id = rsp->vlan;\n\tp_srp(a, k, &s->stream);",
           "\ts->stream.vlan_id = rsp->vlan;", "acmp", "AcmpCore.A8SuccessSettles", "A8 SRP is started",
           (("acmpwalk", "Table530/ListenerWalk.Graded/PROBE_OK_PWR", "SRP started"),)),
    Mutant("acmp-settle-swaps-stream-fields", "acmp/acmp.c",
           "\ts->stream.stream_id = rsp->stream_id;                   // step 4, kept exactly (Milan v1.2 5.3.8.9)\n"
           "\ts->stream.dest_mac = rsp->dest_mac;",
           "\ts->stream.stream_id = rsp->dest_mac;\n\ts->stream.dest_mac = rsp->stream_id;",
           "acmp", "AcmpCore.A8SuccessSettles", "stream_vlan_id exactly",
           (("acmpwalk", "Table530/ListenerWalk.Graded/PROBE_OK_PWR", "the settled stream"),)),
    Mutant("acmp-failure-status-dropped", "acmp/acmp.c", "\t\ts->acmp_status = rsp->status;",
           "\t\ts->acmp_status = ACMP_STATUS_SUCCESS;",
           "acmp", "AcmpCore.A9FailureWaitsForTheRetry", "A9 a failed response: PRB_W_RETRY, the ACMP status is its status",
           (("acmpwalk", "Table530/ListenerWalk.Graded/PROBE_FAIL_PWR", "state, probing and ACMP status"),)),
    Mutant("acmp-failure-retries-at-200ms", "acmp/acmp.c",
           "\t\tsm_timer(a, s, ACMP_TIMER_RETRY, ACMP_TMR_RETRY_MS);\n\t\ts->acmp_status = rsp->status;",
           "\t\tsm_timer(a, s, ACMP_TIMER_RETRY, ACMP_TMR_NO_RESP_MS);\n\t\ts->acmp_status = rsp->status;",
           "acmp", "AcmpCore.A9FailureWaitsForTheRetry", "A9 and TMR_RETRY 4 s",
           (("acmpwalk", "Table530/ListenerWalk.Graded/PROBE_FAIL_PWR", "the timer's deadline"),)),
    # the timers (A10 to A13)
    Mutant("acmp-duplicate-takes-a-new-sequence-id", "acmp/acmp.c",
           "\t\ts->probe_retried = true;\n\t\tsend_probe(a, k);                               // the same sequence_id",
           "\t\tprobe(a, k);\n\t\ts->probe_retried = true;",
           "acmp", "AcmpCore.A10NoResponseSendsTheDuplicateThenGivesUp", "A10 an exact duplicate of the first probe",
           (("acmpwalk", "Table530/ListenerWalk.Graded/TMR_CMD_PWR", "frame 0 byte for byte"),)),
    Mutant("acmp-second-timeout-keeps-status-0", "acmp/acmp.c",
           "\t\ts->acmp_status = ACMP_STATUS_LISTENER_TALKER_TIMEOUT;", "\t\ts->acmp_status = ACMP_STATUS_SUCCESS;",
           "acmp", "AcmpCore.A10NoResponseSendsTheDuplicateThenGivesUp", "A10 the second: no frame, LISTENER_TALKER_TIMEOUT",
           (("acmp", "AcmpCore.A25OnlyTable522ItemsAreReported", "A25 the ACMP status LISTENER_TALKER_TIMEOUT does"),
            ("acmpwalk", "Table530/ListenerWalk.Graded/TMR_CMD_PW2", "state, probing and ACMP status"))),
    Mutant("acmp-no-duplicate", "acmp/acmp.c",
           "\t} else if (kind == ACMP_TIMER_NO_RESP && s->state == ACMP_PRB_W_RESP) {   // 5.5.3.5.16",
           "\t} else if (kind == ACMP_TIMER_NO_RESP && s->state == ACMP_PRB_W_RESP && false) {",
           "acmp", "AcmpCore.A10NoResponseSendsTheDuplicateThenGivesUp", "A10 the first TMR_NO_RESP sends one frame",
           (("acmpwalk", "Table530/ListenerWalk.Graded/TMR_CMD_PWR", "frames"),)),
    Mutant("acmp-retry-ignores-discovery", "acmp/acmp.c",
           "\t} else if (kind == ACMP_TIMER_RETRY && !s->discovered) {   // 5.5.3.5.30 step 1",
           "\t} else if (kind == ACMP_TIMER_RETRY) {",
           "acmp", "AcmpCore.A11RetryWaitsForTheTalkerOrDelays", "A11 TMR_RETRY, talker discovered: TMR_DELAY",
           (("acmpwalk", "Table530/ListenerWalk.Graded/TMR_RETRY_PWT_disc", "state, probing and ACMP status"),)),
    Mutant("acmp-retry-zeroes-the-status", "acmp/acmp.c",
           "\t\tdelay(a, s);\n\t} else {                                                // 5.5.3.5.36, TMR_NO_TK",
           "\t\ts->acmp_status = ACMP_STATUS_SUCCESS;\n\t\tdelay(a, s);\n\t} else {",
           "acmp", "AcmpCore.A11RetryWaitsForTheTalkerOrDelays", "A11 and the ACMP status stays",
           (("acmpwalk", "Table530/ListenerWalk.Graded/TMR_RETRY_PWT_disc", "state, probing and ACMP status"),)),
    Mutant("acmp-delay-resends-the-old-probe", "acmp/acmp.c",
           "\tif (kind == ACMP_TIMER_DELAY) {                         // 5.5.3.5.10\n\t\tprobe(a, k);",
           "\tif (kind == ACMP_TIMER_DELAY) {\n\t\tsend_probe(a, k);",
           "acmp", "AcmpCore.A12DelaySendsANewProbe", "A12 a new PROBE_TX_COMMAND with the next sequence_id",
           (("acmpwalk", "Table530/ListenerWalk.Graded/TMR_DELAY_PWD", "frame 0 byte for byte"),)),
    Mutant("acmp-no-tk-keeps-srp", "acmp/acmp.c",
           "\t} else {                                                // 5.5.3.5.36, TMR_NO_TK\n\t\tsrp_stop(a, k);",
           "\t} else {\n\t\t(void)k;",
           "acmp", "AcmpCore.A13NoTalkerAttributeReprobes", "A13 TMR_NO_TK clears the SRP parameters and stops SRP",
           (("acmpwalk", "Table530/ListenerWalk.Graded/TMR_NOTK_SNR", "SRP stopped"),)),
    Mutant("acmp-reprobe-ignores-discovery", "acmp/acmp.c",
           "\tif (!s->discovered) {\n\t\tpassive(s);\n\t\treturn;\n\t}\n\ts->probing = ACMP_PROBING_ACTIVE;",
           "\tif (true) {\n\t\tpassive(s);\n\t\treturn;\n\t}\n\ts->probing = ACMP_PROBING_ACTIVE;",
           "acmp", "AcmpCore.A13NoTalkerAttributeReprobes", "A13 talker discovered: TMR_DELAY, PRB_W_DELAY",
           (("acmp", "AcmpCore.A15UnregisteredReprobes", "A15 talker discovered: TMR_DELAY, PRB_W_DELAY"),
            ("acmpwalk", "Table530/ListenerWalk.Graded/TMR_NOTK_SNR_disc", "state, probing and ACMP status"))),
    # the SRP side (A14, A15)
    Mutant("acmp-registered-anywhere", "acmp/acmp.c",
           "\tif (sink >= a->cfg.n_sinks || a->sinks[sink].state != ACMP_SETTLED_NO_RSV) {",
           "\tif (sink >= a->cfg.n_sinks) {",
           "acmp", "AcmpCore.A14RegisteredSettlesTheReservation", "A14 EVT_TK_REGISTERED anywhere else",
           (("acmpwalk", "Table530/ListenerWalk.Graded/TK_REG_PWR", "state, probing and ACMP status"),)),
    Mutant("acmp-registered-keeps-no-tk", "acmp/acmp.c",
           "\tstruct acmp_sink *s = &a->sinks[sink];                  // 5.5.3.5.42\n\tsm_stop(s);",
           "\tstruct acmp_sink *s = &a->sinks[sink];",
           "acmp", "AcmpCore.A14RegisteredSettlesTheReservation", "A14 EVT_TK_REGISTERED: TMR_NO_TK cleared",
           (("acmpwalk", "Table530/ListenerWalk.Graded/TK_REG_SNR", "the sink's timer armed or not"),)),
    Mutant("acmp-registered-kind-dropped", "acmp/acmp.c", "\ts->tk_failed = failed;",
           "\ts->tk_failed = false;\n\t(void)failed;",
           "acmp", "AcmpCore.A2GetRxStateReportsStreamingWaitAndRegisteringFailed", "REGISTERING_FAILED 1 (Table 5.39)",
           (("acmpwalk", "Table530/ListenerWalk.Graded/TK_REG_SNR", "registered state"),)),
    Mutant("acmp-unregistered-anywhere", "acmp/acmp.c",
           "\tif (sink >= a->cfg.n_sinks || a->sinks[sink].state != ACMP_SETTLED_RSV_OK) {",
           "\tif (sink >= a->cfg.n_sinks) {",
           "acmp", "AcmpCore.A15UnregisteredReprobes", "A15 EVT_TK_UNREGISTERED anywhere else",
           (("acmpwalk", "Table530/ListenerWalk.Graded/TK_UNREG_SNR", "state, probing and ACMP status"),)),
    Mutant("acmp-unregistered-keeps-srp", "acmp/acmp.c", "\tsrp_stop(a, sink);                                      // 5.5.3.5.48",
           "\t(void)sink;", "acmp", "AcmpCore.A15UnregisteredReprobes", "A15 EVT_TK_UNREGISTERED, talker not discovered: SRP stopped",
           (("acmpwalk", "Table530/ListenerWalk.Graded/TK_UNREG_SOK", "SRP stopped"),)),
    # one timer per interface (A17, A18)
    Mutant("acmp-timer-at-the-latest-deadline", "acmp/acmp.c",
           "\tif (armed && (!*any || (int32_t)(deadline - *at) < 0)) {",
           "\tif (armed && (!*any || (int32_t)(deadline - *at) > 0)) {",
           "acmp", "AcmpCore.A17EachInterfaceTimerHoldsItsEarliestDeadline", "A17 each interface's timer is armed at the earliest"),
    Mutant("acmp-timer-port-called-every-time", "acmp/acmp.c",
           "\t\tif (any && (!a->timer_armed[i] || a->timer_at[i] != at)) {", "\t\tif (any) {",
           "acmp", "AcmpCore.A17EachInterfaceTimerHoldsItsEarliestDeadline",
           "A17 the port is called only when the earliest deadline moves"),
    Mutant("acmp-timer-never-stopped", "acmp/acmp.c", "\t\t} else if (!any && a->timer_armed[i]) {",
           "\t\t} else if (!any && a->timer_armed[i] && false) {",
           "acmp", "AcmpCore.A17EachInterfaceTimerHoldsItsEarliestDeadline", "A17 an interface whose sinks hold no deadline",
           (("acmp", "AcmpMailbox.C10C11DiscoveryPathsAreServedInThePassThatTakesTheRecord", "C11 ENTITY_DEPARTING: PRB_W_AVAIL, the slot stopped"),)),
    Mutant("acmp-expiry-takes-every-interface", "acmp/acmp.c",
           "\t\tstruct acmp_sink *s = &a->sinks[k];\n\t\tif (s->interface != interface) {\n\t\t\tcontinue;\n\t\t}\n"
           "\t\tif (s->adp_armed && due(s->adp_deadline, t)) {",
           "\t\tstruct acmp_sink *s = &a->sinks[k];\n\t\tif (s->adp_armed && due(s->adp_deadline, t)) {",
           "acmp", "AcmpCore.A17EachInterfaceTimerHoldsItsEarliestDeadline", "A17 an expiry takes the due timers only"),
    Mutant("acmp-expiry-not-consumed", "acmp/acmp.c",
           "\ta->timer_armed[interface] = false;                      // the port's timer has fired\n", "",
           "acmp", "AcmpCore.A17EachInterfaceTimerHoldsItsEarliestDeadline",
           "A17 an expiry with nothing due changes nothing and re-arms the timer it consumed"),
    Mutant("acmp-zero-delay-waits", "acmp/acmp.c",
           "\t\twhile (s->timer != ACMP_TIMER_NONE && due(s->timer_deadline, t)) {",
           "\t\tif (s->timer != ACMP_TIMER_NONE && due(s->timer_deadline, t)) {",
           "acmp", "AcmpCore.A18AZeroDelayProbesInTheSameExpiry", "A18 TMR_RETRY drawing 0 ms sends its probe in the same expiry"),
    Mutant("acmp-delay-up-to-4s", "acmp/acmp.h", "#define ACMP_TMR_DELAY_MAX_MS 1000u",
           "#define ACMP_TMR_DELAY_MAX_MS 4000u",
           "acmp", "AcmpCore.A18AZeroDelayProbesInTheSameExpiry", "A18 the longest draw is 1000 ms"),
    Mutant("acmp-seed-at-every-draw", "acmp/acmp.c", "\t\ta->rng ^= p_seed(a);\n\t\ta->seeded = true;",
           "\t\ta->rng ^= p_seed(a);", "acmp", "AcmpCore.A18TheSeedIsTakenAtTheFirstDraw", "A18 and never again"),
    Mutant("acmp-rng-left-at-0", "acmp/acmp.c",
           "\t\tif (a->rng == 0u) {\n\t\t\ta->rng = 1u;                            // xorshift never leaves 0\n\t\t}\n", "",
           "acmp", "AcmpCore.A18TheSeedIsTakenAtTheFirstDraw", "A18 a seed that cancels the state to 0 leaves it 1"),
    # owed frames and #653 (A19, E1, E2)
    Mutant("acmp-response-passes-an-owed-frame", "acmp/acmp.c",
           "\tif (a->owed_count == 0u && p_send(a, interface, frame)) {", "\tif (p_send(a, interface, frame)) {",
           "acmp", "AcmpCore.A19NothingPassesAnOwedFrame", "A19 a response does not pass one already owed"),
    Mutant("acmp-poll-drains-everything", "acmp/acmp.c",
           "\tif (a->owed_count != 0u) {\n\t\tconst struct acmp_owed *o = &a->owed[a->owed_head];\n"
           "\t\tif (p_send(a, o->interface, o->frame)) {",
           "\twhile (a->owed_count != 0u &&\n"
           "\t       p_send(a, a->owed[a->owed_head].interface, a->owed[a->owed_head].frame)) {\n"
           "\t\tconst struct acmp_owed *o = &a->owed[a->owed_head];\n\t\t{",
           "acmp", "AcmpCore.A19AResponseWithoutRoomIsOwedAndItsChangeWaits", "A19 one frame per poll",
           (("acmp", "AcmpMailbox.E2AnOwedResponseIsCommittedInPassKPlus1", "E2 3 frames owed ahead"),)),
    Mutant("acmp-change-not-held-for-its-response", "acmp/acmp.c",
           "\t\ta->sinks[k].change_owed = (uint8_t)(a->sinks[k].change_owed + ((release >> k) & 1u));",
           "\t\t(void)release;",
           "acmp", "AcmpCore.A19AResponseWithoutRoomIsOwedAndItsChangeWaits",
           "A19 but its change is not reported while its response waits (#653)",
           (("acmp", "AcmpMailbox.E1AnOwedResponseLeavesFirstAndItsChangeAfterIt", "E1 nothing reported yet"),)),
    Mutant("acmp-full-queue-acts", "acmp/acmp.c",
           "\tif (a->owed_count < ACMP_OWED_MAX) {\n\t\treturn true;\n\t}\n\ta->busy_drops++;",
           "\tif (true) {\n\t\treturn true;\n\t}\n\ta->busy_drops++;",
           "acmp", "AcmpCore.A19AFullQueueDropsTheCommandBeforeItActs",
           "A19 a command whose response would find the queue full is dropped"),
    Mutant("acmp-lost-probe-uncounted", "acmp/acmp.c",
           "\tif (!transmit(a, s->interface, frame, 0u)) {\n\t\ta->probes_lost++;\n\t}",
           "\t(void)transmit(a, s->interface, frame, 0u);",
           "acmp", "AcmpCore.A19AProbeWithoutRoomIsLostAndRecovered", "A19 a probe the full queue cannot take is lost and counted"),
    Mutant("acmp-first-owed-releases-every-change", "acmp/acmp.c",
           "\t\t\t\ta->sinks[k].change_owed = (uint8_t)(a->sinks[k].change_owed - ((o->release >> k) & 1u));",
           "\t\t\t\ta->sinks[k].change_owed = 0u;",
           "acmp", "AcmpCore.A19TwoOwedResponsesForOneSinkReleaseTogether",
           "A19 the bind's response left but the unbind's is still owed"),
    Mutant("acmp-poll-newest-first", "acmp/acmp.c",
           "\t\tconst struct acmp_owed *o = &a->owed[a->owed_head];\n\t\tif (p_send(a, o->interface, o->frame)) {",
           "\t\tconst struct acmp_owed *o = &a->owed[(a->owed_head + a->owed_count - 1u) % ACMP_OWED_MAX];\n"
           "\t\tif (p_send(a, o->interface, o->frame)) {",
           "acmp", "AcmpMailbox.E2AnOwedResponseIsCommittedInPassKPlus1", "E2 3 frames owed ahead",
           (("acmp", "AcmpCore.A19NothingPassesAnOwedFrame", "A19 they leave in the order they were made"),)),
    # the talker (A20, TW)
    Mutant("acmp-probe-tx-reports-asking-failed", "acmp/acmp.c",
           "\t\t\tr.flags = cmd->flags & (ACMP_FLAG_FAST_CONNECT | ACMP_FLAG_STREAMING_WAIT);",
           "\t\t\tr.flags = (uint16_t)((cmd->flags & (ACMP_FLAG_FAST_CONNECT | ACMP_FLAG_STREAMING_WAIT)) |\n"
           "\t\t\t\t\t   (st.asking_failed ? ACMP_FLAG_REGISTERING_FAILED : 0u));",
           "acmp", "AcmpCore.A20ProbeTxIsAnsweredFromTheSource", "A20 PROBE_TX_RESPONSE is Table 5.43"),
    Mutant("acmp-probe-tx-echoes-every-flag", "acmp/acmp.c",
           "\t\t\tr.flags = cmd->flags & (ACMP_FLAG_FAST_CONNECT | ACMP_FLAG_STREAMING_WAIT);",
           "\t\t\tr.flags = cmd->flags;",
           "acmpwalk", "TalkerWalk.TW1ProbeTheFlagLawAndTheSource", "TW1 PROBE_TX: SUCCESS, FAST_CONNECT and STREAMING_WAIT echoed"),
    Mutant("acmp-probe-tx-any-interface", "acmp/acmp.c",
           "\tif (cmd->msg == ACMP_MSG_PROBE_TX_COMMAND && interface != a->cfg.source_interface[src]) {",
           "\tif (cmd->msg == ACMP_MSG_PROBE_TX_COMMAND && false) {",
           "acmp", "AcmpCore.A20ProbeTxIsAnsweredFromTheSource", "A20 a probe from another interface than the source's",
           (("acmpwalk", "TalkerWalk.TW4TheInterfaceAndTheStatelessProperty", "TW4 a probe from another interface"),)),
    Mutant("acmp-probe-tx-no-destination-mac-check", "acmp/acmp.c",
           "\t\tstruct pdu r = echo(cmd, st.dest_mac_valid ? ACMP_STATUS_SUCCESS : ACMP_STATUS_TALKER_DEST_MAC_FAIL);",
           "\t\tstruct pdu r = echo(cmd, ACMP_STATUS_SUCCESS);",
           "acmp", "AcmpCore.A20ProbeTxIsAnsweredFromTheSource", "A20 no destination MAC: TALKER_DEST_MAC_FAILED",
           (("acmpwalk", "TalkerWalk.TW1ProbeTheFlagLawAndTheSource", "TW1 no destination MAC"),)),
    Mutant("acmp-disconnect-always-succeeds", "acmp/acmp.c",
           "\tif (src >= a->cfg.n_sources) {\n\t\tstruct pdu r = echo(cmd, ACMP_STATUS_TALKER_UNKNOWN_ID);",
           "\tif (src >= a->cfg.n_sources && cmd->msg != ACMP_MSG_DISCONNECT_TX_COMMAND) {\n"
           "\t\tstruct pdu r = echo(cmd, ACMP_STATUS_TALKER_UNKNOWN_ID);",
           "acmp", "AcmpCore.A20DisconnectGetTxStateAndGetTxConnection",
           "A20 DISCONNECT_TX of an unknown source: TALKER_UNKNOWN_ID",
           (("acmpwalk", "TalkerWalk.TW3DisconnectAndGetTxConnection", "TD1 DISCONNECT_TX of an unknown source"),)),
    Mutant("acmp-unknown-source-answered", "acmp/acmp.c",
           "\tif (src >= a->cfg.n_sources) {\n\t\tstruct pdu r = echo(cmd, ACMP_STATUS_TALKER_UNKNOWN_ID);",
           "\tif (src >= a->cfg.n_sources && false) {\n\t\tstruct pdu r = echo(cmd, ACMP_STATUS_TALKER_UNKNOWN_ID);",
           "acmp", "AcmpCore.A20ProbeTxIsAnsweredFromTheSource", "A20 an unknown source: TALKER_UNKNOWN_ID",
           (("acmpwalk", "TalkerWalk.TW2GetTxStateReadsRegisteringFailedLive", "TW2 an unknown source"),)),
    Mutant("acmp-get-tx-state-echoes-the-listener", "acmp/acmp.c",
           "\tr.listener = 0u;\n\tr.listener_uid = 0u;\n\tr.flags = st.asking_failed",
           "\tr.flags = st.asking_failed",
           "acmp", "AcmpCore.A20DisconnectGetTxStateAndGetTxConnection", "A20 GET_TX_STATE: listener fields 0",
           (("acmpwalk", "TalkerWalk.TW2GetTxStateReadsRegisteringFailedLive", "TW2 GET_TX_STATE: listener fields 0"),)),
    Mutant("acmp-get-tx-state-registering-failed-0", "acmp/acmp.c",
           "\tr.flags = st.asking_failed ? ACMP_FLAG_REGISTERING_FAILED : 0u;", "\tr.flags = 0u;",
           "acmp", "AcmpCore.A20DisconnectGetTxStateAndGetTxConnection", "REGISTERING_FAILED live",
           (("acmpwalk", "TalkerWalk.TW2GetTxStateReadsRegisteringFailedLive", "TW2 GET_TX_STATE: listener fields 0"),)),
    Mutant("acmp-get-tx-state-unheld-mac", "acmp/acmp.c",
           "\tr.dest_mac = st.dest_mac_valid ? st.stream.dest_mac : 0u;", "\tr.dest_mac = st.stream.dest_mac;",
           "acmp", "AcmpCore.A20DisconnectGetTxStateAndGetTxConnection", "A20 with no destination MAC held, none is reported"),
    Mutant("acmp-get-tx-connection-supported", "acmp/acmp.c",
           "\t\tstruct pdu r = echo(cmd, ACMP_STATUS_NOT_SUPPORTED);              // 5.5.4.4, Table 5.48",
           "\t\tstruct pdu r = echo(cmd, ACMP_STATUS_SUCCESS);",
           "acmp", "AcmpCore.A20DisconnectGetTxStateAndGetTxConnection", "A20 GET_TX_CONNECTION: NOT_SUPPORTED",
           (("acmpwalk", "TalkerWalk.TW3DisconnectAndGetTxConnection", "TW3 GET_TX_CONNECTION: NOT_SUPPORTED"),)),
    # what the core does not take (A21)
    Mutant("acmp-every-listener-is-this-one", "acmp/acmp.c", "\tbool listener = cmd.listener == a->cfg.entity_id;",
           "\tbool listener = true;", "acmp", "AcmpCore.A21MessagesNotForThisEntityAreIgnored",
           "A21 commands for another listener or talker"),
    Mutant("acmp-every-talker-is-this-one", "acmp/acmp.c", "\tbool talker = cmd.talker == a->cfg.entity_id;",
           "\tbool talker = true;", "acmp", "AcmpCore.A21MessagesNotForThisEntityAreIgnored",
           "A21 commands for another listener or talker"),
    Mutant("acmp-short-pdu-read", "acmp/acmp.c",
           "\tif (interface >= a->cfg.n_interfaces || len < ACMP_FRAME_BYTES || wire_be16(frame + 12) != ACMP_ETHERTYPE ||",
           "\tif (interface >= a->cfg.n_interfaces || len < ACMP_FRAME_BYTES - 1u || wire_be16(frame + 12) != ACMP_ETHERTYPE ||",
           "acmp", "AcmpCore.A21MalformedFramesAreCounted", "A21 a frame shorter than the Milan ACMPDU"),
    Mutant("acmp-longer-pdu-refused", "acmp/acmp.c",
           "\tif (interface >= a->cfg.n_interfaces || len < ACMP_FRAME_BYTES || wire_be16(frame + 12) != ACMP_ETHERTYPE ||",
           "\tif (interface >= a->cfg.n_interfaces || len != ACMP_FRAME_BYTES || wire_be16(frame + 12) != ACMP_ETHERTYPE ||",
           "acmp", "AcmpCore.A21MalformedFramesAreCounted", "A21 the longer IEEE 1722.1-2021 PDU is accepted"),
    # discovery (A22, DW)
    Mutant("acmp-discovery-reads-no-grandmaster", "acmp/acmp.c",
           "\treturn d->gm == d->local_gm && d->domain == d->local_domain;", "\treturn true;",
           "acmp", "AcmpCore.A22AvailableDiscoversWhenTheGrandmasterMatches", "A22 TK_NOT_DISCOVERED: an AVAILABLE from another grandmaster",
           (("acmpwalk", "Table554/DiscoveryWalk.Graded/AVAILABLE_GM_mismatch__index____last__TK_NOT_DISCOVERED", "the discovery state"),)),
    Mutant("acmp-discovery-reads-no-domain", "acmp/acmp.c",
           "\treturn d->gm == d->local_gm && d->domain == d->local_domain;", "\treturn d->gm == d->local_gm;",
           "acmp", "AcmpCore.A22AvailableDiscoversWhenTheGrandmasterMatches", "A22 and from another domain",
           (("acmpwalk", "Table554/DiscoveryWalk.Graded/AVAILABLE_domain_mismatch__index____last__TK_DISCOVERED", "the discovery state"),)),
    Mutant("acmp-valid-time-in-seconds", "acmp/acmp.c",
           "\td.valid_ms = (uint32_t)(frame[A_VALID_TIME] >> 3) * ACMP_VALID_TIME_UNIT_MS;   // 6.2.2.5",
           "\td.valid_ms = (uint32_t)(frame[A_VALID_TIME] >> 3) * 1000u;",
           "acmp", "AcmpCore.A22AvailableDiscoversWhenTheGrandmasterMatches", "A22 TMR_NO_ADP is the received valid_time in two-second units",
           (("acmpwalk", "Table554/DiscoveryWalk.Graded/", "TMR_NO_ADP armed from the received valid_time"),)),
    Mutant("acmp-discovered-interface-unchecked", "acmp/acmp.c",
           "\tif (ifx != s->disc_interface_index) {\n\t\treturn;                                         // 5.6.4.5.2 step 1",
           "\tif (false) {\n\t\treturn;",
           "acmp", "AcmpCore.A22DiscoveredStateCells", "A22 TK_DISCOVERED: an AVAILABLE with another interface_index is ignored",
           (("acmpwalk", "Table554/DiscoveryWalk.Graded/AVAILABLE_interface_index_differs__TK_DISCOVERED", "TMR_NO_ADP untouched"),)),
    Mutant("acmp-restart-on-a-smaller-index-only", "acmp/acmp.c",
           "\tif (index <= s->disc_available_index) {                 // step 2: a new availability cycle",
           "\tif (index < s->disc_available_index) {",
           "acmp", "AcmpCore.A22DiscoveredStateCells", "A22 available_index 700 <= last"),
    Mutant("acmp-restart-raises-no-discovered", "acmp/acmp.c", "\t\ttk_discovered(a, s);                            // 2c\n", "",
           "acmp", "AcmpCore.A22DiscoveredStateCells", "EVT_TK_DEPARTED then EVT_TK_DISCOVERED",
           (("acmpwalk", "Table554/DiscoveryWalk.Graded/AVAILABLE_match__index____last__TK_DISCOVERED", "the events raised"),)),
    Mutant("acmp-restart-mismatch-keeps-aging", "acmp/acmp.c",
           "\t\t\ts->adp_armed = false;                   // 2b: TK_NOT_DISCOVERED, no step 3", "\t\t\t(void)s;",
           "acmp", "AcmpCore.A22DiscoveredStateCells", "A22 index <= last from another grandmaster",
           (("acmpwalk", "Table554/DiscoveryWalk.Graded/AVAILABLE_GM_mismatch__index____last__TK_DISCOVERED", "TMR_NO_ADP stopped"),)),
    Mutant("acmp-refresh-notes-no-index", "acmp/acmp.c", "\ts->disc_available_index = index;                        // step 3\n",
           "", "acmp", "AcmpCore.A22DiscoveredStateCells", "A22 a rising available_index is noted",
           (("acmpwalk", "Table554/DiscoveryWalk.Graded/AVAILABLE_match__index___last__TK_DISCOVERED", "the available_index noted"),)),
    Mutant("acmp-departing-taken-undiscovered", "acmp/acmp.c",
           "\tif (!s->discovered || ifx != s->disc_interface_index) {", "\tif (ifx != s->disc_interface_index) {",
           "acmp", "AcmpCore.A22DepartingAndAging", "A22 a DEPARTING in TK_NOT_DISCOVERED is ignored"),
    Mutant("acmp-departing-interface-unchecked", "acmp/acmp.c",
           "\tif (!s->discovered || ifx != s->disc_interface_index) {", "\tif (!s->discovered) {\n\t\t(void)ifx;",
           "acmp", "AcmpCore.A22DepartingAndAging", "A22 a DEPARTING with another interface_index is ignored",
           (("acmpwalk", "Table554/DiscoveryWalk.Graded/DEPARTING_interface_index_differs__TK_DISCOVERED", "the discovery state"),)),
    Mutant("acmp-departing-keeps-aging", "acmp/acmp.c", "\ts->adp_armed = false;\n\ttk_departed(s);\n}",
           "\ttk_departed(s);\n}", "acmp", "AcmpCore.A22DepartingAndAging", "A22 a DEPARTING: TMR_NO_ADP stopped",
           (("acmpwalk", "Table554/DiscoveryWalk.Graded/DEPARTING_interface_index_matches__TK_DISCOVERED", "TMR_NO_ADP stopped"),)),
    Mutant("acmp-no-aging", "acmp/acmp.c", "\t\tif (s->adp_armed && due(s->adp_deadline, t)) {   // 5.6.4.5.4",
           "\t\tif (s->adp_armed && due(s->adp_deadline, t) && false) {",
           "acmp", "AcmpCore.A22DepartingAndAging", "A22 TMR_NO_ADP: TK_NOT_DISCOVERED and EVT_TK_DEPARTED",
           (("acmpwalk", "Table554/DiscoveryWalk.Graded/TMR_NO_ADP_TK_DISCOVERED", "the discovery state"),)),
    Mutant("acmp-discovery-on-every-interface", "acmp/acmp.c",
           "\t\tif (!s->disc_running || s->interface != interface || s->binding.talker_entity_id != entity) {",
           "\t\tif (!s->disc_running || s->binding.talker_entity_id != entity) {",
           "acmp", "AcmpCore.A22OnlyBoundSinksOfThatTalkerOnThatInterface", "A22 every bound sink of the talker processes it"),
    Mutant("acmp-discovery-on-unbound-sinks", "acmp/acmp.c",
           "\t\tif (!s->disc_running || s->interface != interface || s->binding.talker_entity_id != entity) {",
           "\t\tif (s->interface != interface || s->binding.talker_entity_id != entity) {",
           "acmp", "AcmpCore.A22OnlyBoundSinksOfThatTalkerOnThatInterface", "A22 an unbound sink runs no discovery"),
    Mutant("acmp-grandmaster-sampled-for-the-refresh", "acmp/acmp.c",
           "\tuint16_t ifx = d->ifx;\n\tuint32_t index = d->index;",
           "\t(void)gm_matches(a, d);\n\tuint16_t ifx = d->ifx;\n\tuint32_t index = d->index;",
           "acmp", "AcmpCore.A22DiscoveredStateCells", "A22 TK_DISCOVERED: an AVAILABLE with another interface_index is ignored"),
    Mutant("acmp-grandmaster-sampled-per-sink", "acmp/acmp.c", "\t\td->sampled = true;\n", "",
           "acmp", "AcmpCore.A22OnlyBoundSinksOfThatTalkerOnThatInterface", "A22 and the grandmaster is sampled once for the frame"),
    # the no-callback rule (A23, #678)
    Mutant("acmp-reentry-unguarded", "acmp/acmp.c", "\tif (a->in_port) {\n\t\ta->reentries++;",
           "\tif (false) {\n\t\ta->reentries++;",
           "acmp", "AcmpCore.A23EveryEntryRefusesACallFromInsideAPort", "A23 a call made from inside the send port is refused",
           (("acmp", "AcmpCore.A23EveryPortIsGuarded", "A23 the port kind 1 is guarded"),)),
    Mutant("acmp-reentry-untrapped", "acmp/acmp.c", "\t\tREENTRY_TRAP();\n", "",
           "acmp", "AcmpCore.A23EveryEntryRefusesACallFromInsideAPort", "refused, counted and trapped"),
    Mutant("acmp-send-port-unflagged", "acmp/acmp.c", "\ta->in_port = true;\n\tbool ok = a->ports->send(",
           "\tbool ok = a->ports->send(",
           "acmp", "AcmpCore.A23EveryEntryRefusesACallFromInsideAPort", "A23 a call made from inside the send port is refused"),
    Mutant("acmp-timer-port-unflagged", "acmp/acmp.c", "\ta->in_port = true;\n\ta->ports->timer(", "\ta->ports->timer(",
           "acmp", "AcmpCore.A23EveryPortIsGuarded", "A23 the port kind 1 is guarded"),
    Mutant("acmp-gptp-port-unflagged", "acmp/acmp.c", "\ta->in_port = true;\n\ta->ports->gptp(", "\ta->ports->gptp(",
           "acmp", "AcmpCore.A23EveryPortIsGuarded", "A23 the port kind 2 is guarded"),
    Mutant("acmp-clock-port-unflagged", "acmp/acmp.c", "\t\ta->in_port = true;\n\t\ta->now = a->ports->now_ms(",
           "\t\ta->now = a->ports->now_ms(",
           "acmp", "AcmpCore.A23EveryPortIsGuarded", "A23 the port kind 3 is guarded"),
    Mutant("acmp-seed-port-unflagged", "acmp/acmp.c", "\ta->in_port = true;\n\tuint32_t seed = a->ports->seed(",
           "\tuint32_t seed = a->ports->seed(",
           "acmp", "AcmpCore.A23EveryPortIsGuarded", "A23 the port kind 4 is guarded"),
    Mutant("acmp-lock-port-unflagged", "acmp/acmp.c", "\ta->in_port = true;\n\tbool locked = a->env->locked(",
           "\tbool locked = a->env->locked(",
           "acmp", "AcmpCore.A23EveryPortIsGuarded", "A23 the port kind 5 is guarded"),
    Mutant("acmp-source-port-unflagged", "acmp/acmp.c", "\ta->in_port = true;\n\ta->env->source(", "\ta->env->source(",
           "acmp", "AcmpCore.A23EveryPortIsGuarded", "A23 the port kind 6 is guarded"),
    Mutant("acmp-srp-port-unflagged", "acmp/acmp.c", "\ta->in_port = true;\n\ta->env->srp(", "\ta->env->srp(",
           "acmp", "AcmpCore.A23EveryPortIsGuarded", "A23 the port kind 7 is guarded"),
    Mutant("acmp-persist-port-unflagged", "acmp/acmp.c", "\ta->in_port = true;\n\ta->env->persist(", "\ta->env->persist(",
           "acmp", "AcmpCore.A23EveryPortIsGuarded", "A23 the port kind 8 is guarded"),
    Mutant("acmp-changed-port-unflagged", "acmp/acmp.c", "\ta->in_port = true;\n\ta->env->changed(", "\ta->env->changed(",
           "acmp", "AcmpCore.A23EveryPortIsGuarded", "A23 the port kind 9 is guarded"),
    # the saved record (A24, N)
    Mutant("acmp-restore-lands-in-prb-w-resp", "acmp/acmp.c",
           "\t\ts->probing = ACMP_PROBING_PASSIVE;\n\t\ts->state = ACMP_PRB_W_AVAIL;\n\t}\n\tsink_settle(s);",
           "\t\ts->probing = ACMP_PROBING_PASSIVE;\n\t\ts->state = ACMP_PRB_W_RESP;\n\t}\n\tsink_settle(s);",
           "acmp", "AcmpCore.A24ARestoredBindingFastConnects", "A24 startup with a saved binding",
           (("acmpnvm", "AcmpStore.N1ABindSurvivesAPowerCycleAndFastConnects", "N1 into PRB_W_AVAIL"),)),
    Mutant("acmp-restore-starts-no-discovery", "acmp/acmp.c",
           "\t\tdisc_start(s);\n\t\ts->probing = ACMP_PROBING_PASSIVE;", "\t\ts->probing = ACMP_PROBING_PASSIVE;",
           "acmp", "AcmpCore.A24ARestoredBindingFastConnects", "A24 startup with a saved binding",
           (("acmpnvm", "AcmpStore.N1ABindSurvivesAPowerCycleAndFastConnects", "N1 into PRB_W_AVAIL"),)),
    Mutant("acmp-restore-announced", "acmp/acmp.c", "\t}\n\tsink_settle(s);\n\treturn ACMP_RESTORE_APPLIED;",
           "\t}\n\treturn ACMP_RESTORE_APPLIED;",
           "acmpnvm", "AcmpStore.N1ABindSurvivesAPowerCycleAndFastConnects", "N1 probing saves nothing"),
    Mutant("acmp-record-flags-swapped", "acmp/acmp.c",
           "\t\tpayload[0] = (uint8_t)(BIND_VALID | (s->started ? BIND_STARTED : 0u) |\n"
           "\t\t\t\t       (s->binding.streaming_wait ? BIND_STREAMING_WAIT : 0u));",
           "\t\tpayload[0] = (uint8_t)(BIND_VALID | (s->started ? BIND_STREAMING_WAIT : 0u) |\n"
           "\t\t\t\t       (s->binding.streaming_wait ? BIND_STARTED : 0u));",
           "acmpnvm", "AcmpStore.N3EachSinksStartedStateIsSaved", "N3 each sink's started state and STREAMING_WAIT come back"),
    Mutant("acmp-record-unique-id-little-endian", "acmp/acmp.c",
           "\t\twire_put_be(payload + 2, s->binding.talker_unique_id, 2);",
           "\t\tpayload[2] = (uint8_t)s->binding.talker_unique_id;\n"
           "\t\tpayload[3] = (uint8_t)(s->binding.talker_unique_id >> 8);",
           "acmp", "AcmpCore.A24ARestoredBindingFastConnects", "A24 the latch gives the same record back"),
    Mutant("acmp-restore-unique-id-little-endian", "acmp/acmp.c",
           "\t\ts->binding.talker_unique_id = wire_be16(payload + 2);",
           "\t\ts->binding.talker_unique_id = (uint16_t)(payload[2] | (payload[3] << 8));",
           "acmp", "AcmpCore.A24ARestoredBindingFastConnects", "A24 the record's flags and parameters, big-endian"),
    Mutant("acmp-roll-back-keeps-the-bindings", "acmp/acmp.c",
           "\tfor (unsigned k = 0; k < a->cfg.n_sinks; ++k) {\n\t\tsink_reset(a, k);\n\t\tsink_settle(&a->sinks[k]);\n\t}\n}",
           "\t(void)a;\n}",
           "acmp", "AcmpCore.A24UnboundRecordsRefusalsAndRollback", "A24 the roll-back drops every restored binding",
           (("acmpnvm", "AcmpStore.N6TheRollBackAndEveryOtherGroup", "N6 and drops what it applied"),)),
    Mutant("acmp-unbound-record-not-zero", "acmp/acmp.c", "\tmemset(payload, 0, ACMP_BINDING_BYTES);\n\tif (s->bound) {",
           "\tpayload[1] = 0u;\n\tif (s->bound) {",
           "acmp", "AcmpCore.A24UnboundRecordsRefusalsAndRollback", "A24 an unbound sink's record is all zeros"),
    Mutant("acmp-started-not-saved", "acmp/acmp.c", "\ta->sinks[sink].started = started;\n\tfinish(a);",
           "\ta->sinks[sink].started = started;",
           "acmp", "AcmpCore.A24StartedIsSavedAndReported", "A24 the started state is saved (5.3.8.7)",
           (("acmpnvm", "AcmpStore.N3EachSinksStartedStateIsSaved", "N3 the started state alone is a change"),)),
    # the notification follows Table 5.22 (A25, LW)
    Mutant("acmp-discovery-notifies", "acmp/acmp.c",
           "\t\t\t(uint64_t)(x->registering_failed != y->registering_failed);",
           "\t\t\t(uint64_t)(x->registering_failed != y->registering_failed) |\n"
           "\t\t\t(uint64_t)(x->talker_discovered != y->talker_discovered);",
           "acmp", "AcmpCore.A25OnlyTable522ItemsAreReported", "A25 discovery noted while settled moves no Table 5.22 item",
           (("acmpwalk", "Table530/ListenerWalk.Graded/TK_DISC_PWR", "notified exactly when a Table 5.22 item moved"),)),
    Mutant("acmp-status-not-notified", "acmp/acmp.c",
           "\t\t\t(uint64_t)(x->acmp_status ^ y->acmp_status) | (uint64_t)(x->bound != y->bound) |",
           "\t\t\t(uint64_t)(x->bound != y->bound) |",
           "acmp", "AcmpCore.A25OnlyTable522ItemsAreReported", "A25 the ACMP status LISTENER_TALKER_TIMEOUT does"),
    Mutant("acmp-probing-status-not-notified", "acmp/acmp.c",
           "\t\t\t(uint64_t)((unsigned)x->probing_status ^ (unsigned)y->probing_status) |\n", "",
           "acmpwalk", "Table530/ListenerWalk.Graded/TK_DEP_PWD", "notified exactly when a Table 5.22 item moved"),
    # the adapter on the model (B)
    Mutant("acmp-frames-on-the-adp-channel", "acmp/acmp_mbx.c",
           "\treturn mbx_tx_send(MBX_CH_ACMP, interface, frame, (uint16_t)len) == MBX_STATUS_OK;",
           "\treturn mbx_tx_send(MBX_CH_ADP, interface, frame, (uint16_t)len) == MBX_STATUS_OK;",
           "acmp", "AcmpMailbox.B1TheChannelCarriesCommandsAndResponsesInOrder", "B1 the response, then the probe, on the acmp channel"),
    Mutant("acmp-timer-on-the-next-slot", "acmp/acmp_mbx.c", "\tmbx_timer_arm(i->slot, i->tag, deadline_ms);",
           "\tmbx_timer_arm((unsigned)i->slot + 1u, i->tag, deadline_ms);",
           "acmp", "AcmpMailbox.B3TheTimersRunOnTheInterfaceSlot", "B3 TMR_NO_RESP is armed on the interface's ACMP slot"),
    Mutant("acmp-timer-deadline-taken-as-a-delay", "acmp/acmp_mbx.c", "\tmbx_timer_arm(i->slot, i->tag, deadline_ms);",
           "\tmbx_timer_arm(i->slot, i->tag, mbx_now_ms() + deadline_ms);",
           "acmp", "AcmpMailbox.B3TheTimersRunOnTheInterfaceSlot", "B3 TMR_NO_RESP is armed on the interface's ACMP slot at NOW_MS + 200"),
    Mutant("acmp-stale-tag-taken", "acmp/acmp_mbx.c", "\t\tif (!i->armed || ev->timer_tag != i->tag) {",
           "\t\tif (!i->armed) {",
           "acmp", "AcmpMailbox.B4AnExpiryThatRacedAStopOrAReArmIsDiscarded", "B4 the expiry of a replaced arm"),
    Mutant("acmp-tag-reused", "acmp/acmp_mbx.c", "\ti->tag_seq = (uint16_t)(i->tag_seq + 1u);\n\ti->tag = i->tag_seq;",
           "\ti->tag = i->tag_seq;",
           "acmp", "AcmpMailbox.B4AnExpiryThatRacedAStopOrAReArmIsDiscarded", "B4 the expiry of a replaced arm"),
    Mutant("acmp-stop-keeps-the-arm", "acmp/acmp_mbx.c", "\ti->armed = armed;\n\tif (!armed) {",
           "\ti->armed = true;\n\tif (!armed) {",
           "acmp", "AcmpMailbox.B4AnExpiryThatRacedAStopOrAReArmIsDiscarded", "B4 the expiry of a stopped arm is counted"),
    Mutant("acmp-tap-takes-discover", "acmp/acmp_mbx.c",
           "\tif ((f->bytes[ACMP_HEADER_BYTES + 1u] & 0x0Fu) <= ACMP_ADP_MSG_ENTITY_DEPARTING) {",
           "\tif ((f->bytes[ACMP_HEADER_BYTES + 1u] & 0x0Fu) <= 2u) {",
           "acmp", "AcmpMailbox.B5TheTapHandsAvailableToDiscoveryAndTheRestToAdp", "B5 an ENTITY_DISCOVER still goes to ADP"),
    Mutant("acmp-tap-drops-the-rest", "acmp/acmp_mbx.c", "\tm->adp_next.fn(m->adp_next.ctx, f);", "\t(void)f;",
           "acmp", "AcmpMailbox.B5TheTapHandsAvailableToDiscoveryAndTheRestToAdp", "B5 an ENTITY_DISCOVER still goes to ADP"),
    Mutant("acmp-no-tap", "acmp/acmp_mbx.c", "\t(void)ctrl_loop_bind_rx(l, MBX_CH_ADP, on_adp_frame, m);",
           "\t(void)on_adp_frame;",
           "acmp", "AcmpMailbox.B5TheTapHandsAvailableToDiscoveryAndTheRestToAdp",
           "B5 a record the contract's term would post reaches discovery through the tap",
           (("acmp", "AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract",
             "U5 ACMP binds its channel and stands in front of ADP's handler"),)),
    Mutant("acmp-domain-not-sampled", "acmp/acmp_mbx.c", "\t*gm_id = mbx_gm_id(interface, domain);",
           "\t*gm_id = mbx_gm_id(interface, NULL);\n\t*domain = 0u;",
           "acmp", "AcmpMailbox.B6TheGrandmasterIsTheInterfaces", "B6 one from the interface's grandmaster and domain is taken"),
    Mutant("acmp-attach-before-adp", "acmp/acmp_mbx.c",
           "\tif (l->rx[MBX_CH_ADP].fn == NULL || !ctrl_loop_add_sink(l, on_event, m) || !ctrl_loop_add_poll(l, on_poll, m)) {",
           "\tif (!ctrl_loop_add_sink(l, on_event, m) || !ctrl_loop_add_poll(l, on_poll, m)) {",
           "acmp", "AcmpAdapterUnit.B7RefusalsOfTheAdapter", "B7 attaching before ADP bound the adp channel is refused"),
    Mutant("acmp-attach-ignores-sink-room", "acmp/acmp_mbx.c", "|| !ctrl_loop_add_sink(l, on_event, m) ||",
           "|| (!ctrl_loop_add_sink(l, on_event, m) && false) ||",
           "acmp", "AcmpAdapterUnit.B7RefusalsOfTheAdapter", "B7 a loop with no room for the event sink is refused"),
    Mutant("acmp-attach-ignores-poll-room", "acmp/acmp_mbx.c", "|| !ctrl_loop_add_poll(l, on_poll, m)) {",
           "|| (!ctrl_loop_add_poll(l, on_poll, m) && false)) {",
           "acmp", "AcmpAdapterUnit.B7RefusalsOfTheAdapter", "B7 a loop with no room for the poll is refused"),
    Mutant("acmp-slots-past-the-bank", "acmp/acmp_mbx.c",
           "\tif (first_slot + MBX_N_IF > MBX_N_TIMERS || cfg->n_interfaces > MBX_N_IF) {",
           "\tif (cfg->n_interfaces > MBX_N_IF) {",
           "acmp", "AcmpAdapterUnit.B7RefusalsOfTheAdapter", "B7 slots past the fabric's timer bank are refused"),
    Mutant("acmp-interfaces-past-the-mailbox", "acmp/acmp_mbx.c",
           "\tif (first_slot + MBX_N_IF > MBX_N_TIMERS || cfg->n_interfaces > MBX_N_IF) {",
           "\tif (first_slot + MBX_N_IF > MBX_N_TIMERS) {",
           "acmp", "AcmpAdapterUnit.B7RefusalsOfTheAdapter", "B7 more interfaces than the mailbox has are refused"),
    Mutant("acmp-poll-owes-nothing", "acmp/acmp_mbx.c", "\treturn acmp_poll(&m->acmp);",
           "\t(void)acmp_poll(&m->acmp);\n\treturn false;",
           "acmp", "AcmpMailbox.E1AnOwedResponseLeavesFirstAndItsChangeAfterIt", "E1 nothing reported yet, and the loop does not sleep"),
    # the service cost (C), one extra access per path
    Mutant("acmp-bind-reads-the-clock-twice", "acmp/acmp.c", "\tdisc_start(s);\n\tprobe(a, k);",
           "\tdisc_start(s);\n\t(void)a->ports->now_ms(a->ports->ctx);\n\tprobe(a, k);",
           "acmp", "AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem", "C0 BIND_RX -> response, PROBE_TX, TMR_NO_RESP"),
    Mutant("acmp-get-rx-state-reads-the-clock", "acmp/acmp.c",
           "\tconst struct acmp_sink *s = &a->sinks[k];\n\tstruct pdu r = echo(cmd, ACMP_STATUS_SUCCESS);",
           "\tconst struct acmp_sink *s = &a->sinks[k];\n\t(void)now(a);\n\tstruct pdu r = echo(cmd, ACMP_STATUS_SUCCESS);",
           "acmp", "AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem", "C1 GET_RX_STATE -> response"),
    Mutant("acmp-probe-response-reads-the-clock-twice", "acmp/acmp.c",
           "\tsm_stop(s);                                             // step 2",
           "\tsm_stop(s);\n\t(void)a->ports->now_ms(a->ports->ctx);",
           "acmp", "AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem", "C2 PROBE_TX_RESPONSE -> TMR_NO_TK armed"),
    Mutant("acmp-unbind-reads-the-clock", "acmp/acmp.c", "\ts->acmp_status = ACMP_STATUS_SUCCESS;\n\tsm_stop(s);\n\tstruct pdu r",
           "\ts->acmp_status = ACMP_STATUS_SUCCESS;\n\tsm_stop(s);\n\t(void)now(a);\n\tstruct pdu r",
           "acmp", "AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem", "C3 UNBIND_RX -> response, timer stopped"),
    Mutant("acmp-talker-reads-the-clock", "acmp/acmp.c",
           "\tunsigned src = cmd->talker_uid;\n\tif (cmd->msg == ACMP_MSG_GET_TX_CONNECTION_COMMAND) {",
           "\tunsigned src = cmd->talker_uid + 0u * now(a);\n\tif (cmd->msg == ACMP_MSG_GET_TX_CONNECTION_COMMAND) {",
           "acmp", "AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem", "C4 talker command -> response"),
    Mutant("acmp-expiry-reads-the-clock-twice", "acmp/acmp.c", "\tuint32_t t = now(a);",
           "\tuint32_t t = now(a) + 0u * a->ports->now_ms(a->ports->ctx);",
           "acmp", "AcmpMailbox.C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry", "C5 TMR_NO_RESP -> duplicate PROBE_TX, TMR_NO_RESP"),
    Mutant("acmp-available-reads-the-clock-twice", "acmp/acmp.c", "\ts->adp_deadline = now(a) + valid_ms;",
           "\ts->adp_deadline = now(a) + valid_ms + 0u * a->ports->now_ms(a->ports->ctx);",
           "acmp", "AcmpMailbox.C10C11DiscoveryPathsAreServedInThePassThatTakesTheRecord", "C10 ENTITY_AVAILABLE -> TMR_DELAY armed"),
    Mutant("acmp-departing-samples-the-grandmaster", "acmp/acmp.c", "\t\t\tdisc_departing(s, d.ifx);",
           "\t\t\t(void)gm_matches(a, &d);\n\t\t\tdisc_departing(s, d.ifx);",
           "acmp", "AcmpMailbox.C10C11DiscoveryPathsAreServedInThePassThatTakesTheRecord", "C11 ENTITY_DEPARTING -> timer stopped"),
    Mutant("acmp-aging-samples-the-grandmaster", "acmp/acmp.c", "\t\t\ts->adp_armed = false;\n\t\t\ttk_departed(s);",
           "\t\t\ts->adp_armed = false;\n\t\t\t{\n\t\t\t\tuint64_t g;\n\t\t\t\tuint8_t dm;\n"
           "\t\t\t\tp_gptp(a, interface, &g, &dm);\n\t\t\t}\n\t\t\ttk_departed(s);",
           "acmp", "AcmpMailbox.C12AgingIsServedInThePassThatTakesTheExpiry", "C12 TMR_NO_ADP -> TK_NOT_DISCOVERED"),
    # the backlog figures (F)
    Mutant("acmp-smallest-record-overstated", "acmp/acmp_mbx.h",
           "#define ACMP_MBX_RX_MIN_RECORD_WORDS (MBX_RX_HDR_WORDS + (MBX_CH_ACMP_T0_OFFSET + MBX_TERM_FIELD_BYTES + 3u) / 4u)",
           "#define ACMP_MBX_RX_MIN_RECORD_WORDS (MBX_RX_HDR_WORDS + 1u + (MBX_CH_ACMP_T0_OFFSET + MBX_TERM_FIELD_BYTES + 3u) / 4u)",
           "acmp", "AcmpMailbox.F4TheSmallestRecordsTheFilterPassesFillTheRing",
           "F4 the ring holds ACMP_MBX_RX_BACKLOG records of the smallest frame"),
    Mutant("acmp-pass-bound-understated", "acmp/acmp_mbx.h", "#define ACMP_MBX_PASS_MAX      ",
           "#define ACMP_MBX_PASS_MAX (CTRL_LOOP_EVENTS_PER_PASS * MBX_EV_WORDS)\n#define ACMP_MBX_PASS_MAX_UNUSED      ",
           "acmp", "AcmpMailbox.F0ToF3FullRingsAreTakenWithinTheBound", "F3 the worst pass of the backlog"),
    Mutant("acmp-adp-ring-bound-understated", "acmp/acmp_mbx.h",
           "#define ACMP_MBX_ADP_RX_ACCESSES ((CTRL_LOOP_RX_PASSES(MBX_CH_ADP_RX_WORDS) + 1u) * ACMP_MBX_PASS_MAX)",
           "#define ACMP_MBX_ADP_RX_ACCESSES (CTRL_LOOP_RX_PASSES(MBX_CH_ADP_RX_WORDS) * MBX_RX_HDR_WORDS)",
           "acmp", "AcmpMailbox.F5AnAvailableBehindAFullAdpRingIsServedWithinTheBound",
           "F5 ENTITY_AVAILABLE behind a full adp ring"),
    Mutant("acmp-discovery-takes-the-first-sink", "acmp/acmp.c",
           "\tfor (unsigned k = 0; k < a->cfg.n_sinks; ++k) {        // 5.6.4.1: every bound sink of this talker",
           "\tfor (unsigned k = 0; k < a->cfg.n_sinks && taken == 0u; ++k) {",
           "acmp", "AcmpMailbox.F5AnAvailableBehindAFullAdpRingIsServedWithinTheBound",
           "F5 every matching bound sink takes it in the same pass"),
    Mutant("rx-one-record-per-pass", "loop/ctrl_loop.c", "for (unsigned k = 0; k < CTRL_LOOP_RX_PER_PASS; ++k) {",
           "for (unsigned k = 0; k < 1u; ++k) {",
           "acmp", "AcmpMailbox.F5AnAvailableBehindAFullAdpRingIsServedWithinTheBound",
           "F5 the ENTITY_AVAILABLE is taken by pass",
           (("acmp", "AcmpMailbox.F0ToF3FullRingsAreTakenWithinTheBound", "F2 every acmp record is taken by"),)),
    # the timer paths' own bounds (C6 to C9): each path made to read the bus more than its figure
    Mutant("acmp-second-no-resp-samples-the-grandmaster", "acmp/acmp.c",
           "\t} else if (kind == ACMP_TIMER_NO_RESP) {                // 5.5.3.5.23, in PRB_W_RESP2\n",
           "\t} else if (kind == ACMP_TIMER_NO_RESP) {                // 5.5.3.5.23, in PRB_W_RESP2\n\t\t{\n\t\t\tuint64_t g;\n\t\t\tuint8_t dm;\n\t\t\tp_gptp(a, s->interface, &g, &dm);\n\t\t}\n",
           "acmp", "AcmpMailbox.C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry", "C6 TMR_NO_RESP -> TMR_RETRY armed"),
    Mutant("acmp-retry-samples-the-grandmaster", "acmp/acmp.c",
           "\t} else if (kind == ACMP_TIMER_RETRY) {                  // step 2: the ACMP status stays\n",
           "\t} else if (kind == ACMP_TIMER_RETRY) {                  // step 2: the ACMP status stays\n\t\t{\n\t\t\tuint64_t g;\n\t\t\tuint8_t dm;\n\t\t\tp_gptp(a, s->interface, &g, &dm);\n\t\t}\n",
           "acmp", "AcmpMailbox.C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry", "C7 TMR_RETRY -> TMR_DELAY armed"),
    Mutant("acmp-delay-reads-the-clock-again", "acmp/acmp.c",
           "\tif (kind == ACMP_TIMER_DELAY) {                         // 5.5.3.5.10\n\t\tprobe(a, k);",
           "\tif (kind == ACMP_TIMER_DELAY) {                         // 5.5.3.5.10\n"
           "\t\t(void)a->ports->now_ms(a->ports->ctx);\n\t\tprobe(a, k);",
           "acmp", "AcmpMailbox.C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry", "C8 TMR_DELAY -> PROBE_TX, TMR_NO_RESP"),
    Mutant("acmp-no-tk-samples-the-grandmaster", "acmp/acmp.c", "\t\tsrp_stop(a, k);\n\t\treprobe(a, s);",
           "\t\t{\n\t\t\tuint64_t g;\n\t\t\tuint8_t dm;\n\t\t\tp_gptp(a, s->interface, &g, &dm);\n\t\t}\n\t\tsrp_stop(a, k);\n\t\treprobe(a, s);",
           "acmp", "AcmpMailbox.C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry", "C9 TMR_NO_TK -> TMR_DELAY armed"),
    # the backlog's own preconditions (F0)
    Mutant("acmp-backlog-understated", "acmp/acmp_mbx.h",
           "#define ACMP_MBX_RX_BACKLOG (MBX_CH_ACMP_RX_WORDS / ACMP_MBX_RX_MIN_RECORD_WORDS)",
           "#define ACMP_MBX_RX_BACKLOG (MBX_CH_ACMP_RX_WORDS / ACMP_MBX_RX_MIN_RECORD_WORDS / 2u)",
           "acmp", "AcmpMailbox.F0ToF3FullRingsAreTakenWithinTheBound",
           "F0 the acmp ring holds no more records than A1 assumes",
           (("acmp", "AcmpMailbox.F4TheSmallestRecordsTheFilterPassesFillTheRing",
             "F4 the ring holds ACMP_MBX_RX_BACKLOG records of the smallest frame"),)),
    Mutant("model-event-ring-a-record-short", "host/mbx_model.c",
           "uint16_t free_words = used > MBX_EVT_WORDS ? 0u : (uint16_t)(MBX_EVT_WORDS - used);",
           "uint16_t free_words = used >= MBX_EVT_WORDS - MBX_EV_WORDS ? 0u : "
           "(uint16_t)(MBX_EVT_WORDS - MBX_EV_WORDS - used);",
           "acmp", "AcmpMailbox.F0ToF3FullRingsAreTakenWithinTheBound", "F0 the event ring is full"),
    # a bind without STREAMING_WAIT (A1), the view's flags (A2)
    Mutant("acmp-new-bind-never-started", "acmp/acmp.c",
           "\t// START_STREAMING (Milan v1.2 5.3.8.7)\n\ts->started = !sw;",
           "\t// START_STREAMING (Milan v1.2 5.3.8.7)\n\ts->started = false;",
           "acmp", "AcmpCore.A1BindWithoutStreamingWaitBindsStarted", "A1 a bind without STREAMING_WAIT lands started"),
    Mutant("acmp-bind-response-always-streaming-wait", "acmp/acmp.c",
           "\tr.flags = cmd->flags & ACMP_FLAG_STREAMING_WAIT;\n\trespond(",
           "\tr.flags = ACMP_FLAG_STREAMING_WAIT;\n\trespond(",
           "acmp", "AcmpCore.A1BindWithoutStreamingWaitBindsStarted", "A1 a bind without STREAMING_WAIT lands started"),
    Mutant("acmp-view-without-registering-failed", "acmp/acmp.c",
           "\tv->registering_failed = v->talker_registered && s->tk_failed;",
           "\tv->registering_failed = false;",
           "acmp", "AcmpCore.A2GetRxStateReportsStreamingWaitAndRegisteringFailed", "A2 and the view says so"),
    # discovery from PRB_W_AVAIL (A22, 5.5.3.5.9) and the one grandmaster sample
    Mutant("acmp-discovered-probing-stays-passive", "acmp/acmp.c",
           "\t\ts->probing = ACMP_PROBING_ACTIVE;\n\t\ts->acmp_status = ACMP_STATUS_SUCCESS;\n\t\tdelay(a, s);",
           "\t\ts->acmp_status = ACMP_STATUS_SUCCESS;\n\t\tdelay(a, s);",
           "acmp", "AcmpCore.A22DiscoveredStartsTheProbeFromPrbWAvail", "A22 EVT_TK_DISCOVERED in PRB_W_AVAIL"),
    Mutant("acmp-grandmaster-read-twice", "acmp/acmp.c",
           "\t\tp_gptp(a, d->interface, &d->local_gm, &d->local_domain);\n\t\td->sampled = true;",
           "\t\tp_gptp(a, d->interface, &d->local_gm, &d->local_domain);\n"
           "\t\tp_gptp(a, d->interface, &d->local_gm, &d->local_domain);\n\t\td->sampled = true;",
           "acmp", "AcmpCore.A22DiscoveredStartsTheProbeFromPrbWAvail", "A22 the grandmaster is sampled once for the frame",
           (("acmp", "AcmpMailbox.C10C11DiscoveryPathsAreServedInThePassThatTakesTheRecord",
             "C10 ENTITY_AVAILABLE -> TMR_DELAY armed"),)),
    # what discovery takes (A22): each term of acmp_adp_rx's guard but the interface's,
    # which no sink can match past the configuration
    Mutant("acmp-adp-short-frame-taken", "acmp/acmp.c",
           "if (interface >= a->cfg.n_interfaces || len < ACMP_ADP_FRAME_BYTES || ",
           "if (interface >= a->cfg.n_interfaces || len < ACMP_ADP_FRAME_BYTES - 1u || ",
           "acmp", "AcmpCore.A22OtherAdpFramesAreIgnored", "A22 a short ADPDU, a DISCOVER"),
    Mutant("acmp-adp-ethertype-unchecked", "acmp/acmp.c",
           "len < ACMP_ADP_FRAME_BYTES || wire_be16(frame + 12) != ACMP_ETHERTYPE ||",
           "len < ACMP_ADP_FRAME_BYTES ||",
           "acmp", "AcmpCore.A22OtherAdpFramesAreIgnored", "A22 a short ADPDU, a DISCOVER"),
    Mutant("acmp-adp-subtype-unchecked", "acmp/acmp.c",
           "\t    frame[PDU] != ACMP_ADP_SUBTYPE || (frame[O_MSG] & 0x0Fu) > ACMP_ADP_MSG_ENTITY_DEPARTING) {",
           "\t    (frame[O_MSG] & 0x0Fu) > ACMP_ADP_MSG_ENTITY_DEPARTING) {",
           "acmp", "AcmpCore.A22OtherAdpFramesAreIgnored", "A22 a short ADPDU, a DISCOVER"),
    Mutant("acmp-adp-discover-taken", "acmp/acmp.c",
           "(frame[O_MSG] & 0x0Fu) > ACMP_ADP_MSG_ENTITY_DEPARTING) {",
           "(frame[O_MSG] & 0x0Fu) > ACMP_ADP_MSG_ENTITY_DEPARTING + 1u) {",
           "acmp", "AcmpCore.A22OtherAdpFramesAreIgnored", "A22 a short ADPDU, a DISCOVER"),
    # every frame to the ACMP multicast address (B1, B2; IEEE 1722.1-2021 8.2.1)
    Mutant("acmp-frames-to-the-own-mac", "acmp/acmp.c", "\twire_put_be(frame, ACMP_MULTICAST_MAC, 6);",
           "\twire_put_be(frame, a->cfg.mac[interface], 6);",
           "acmp", "AcmpMailbox.B2OwnUnicastIsAToleranceAndForeignUnicastIsRefused",
           "B2 and is answered, to the multicast address",
           (("acmp", "AcmpMailbox.B1TheChannelCarriesCommandsAndResponsesInOrder",
             "B1 to the ACMP multicast address from the interface's MAC"),)),
    # the composition (U5)
    Mutant("app-acmp-before-adp", "app/ctrl_app.c", "\tctrl_loop_init(&app->loop);\n\tif (!adp_mbx_init(",
           "\tctrl_loop_init(&app->loop);\n"
           "\tif (cfg->acmp != NULL && (!acmp_mbx_init(&app->acmp, cfg->acmp, cfg->acmp_env, CTRL_APP_ACMP_FIRST_SLOT) ||\n"
           "\t\t\t\t  !acmp_mbx_attach(&app->acmp, &app->loop))) {\n\t\treturn false;\n\t}\n\tif (!adp_mbx_init(",
           "acmp", "AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract", "B0 the app with ACMP starts on the model"),
    Mutant("app-acmp-never-composed", "app/ctrl_app.c", "\treturn cfg->acmp == NULL ||", "\treturn true ||",
           "acmp", "AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract",
           "U5 ACMP binds its channel and stands in front of ADP's handler"),
    # the binding owner on the store (N)
    Mutant("acmp-nvm-bindings-to-the-others", "acmp/acmp_nvm.c", "\tif (group != n->bind_group) {\n\t\treturn n->others->apply(",
           "\tif (true) {\n\t\treturn n->others->apply(",
           "acmpnvm", "AcmpStore.N1ABindSurvivesAPowerCycleAndFastConnects", "N1 the binding parameters come back"),
    Mutant("acmp-nvm-refusal-applied", "acmp/acmp_nvm.c", "== ACMP_RESTORE_APPLIED ? NVM_APPLIED : NVM_REFUSED;",
           "== ACMP_RESTORE_APPLIED ? NVM_APPLIED : NVM_APPLIED;",
           "acmpnvm", "AcmpStore.N5ARecordTheCoreRefusesKeepsItsDefault", "N5 a binding record of a sink the configuration lacks is refused",
           (("acmpnvm", "AcmpStore.N6TheRollBackAndEveryOtherGroup", "N6 one of another length is refused"),)),
    Mutant("acmp-nvm-d3-roll-back-kept", "acmp/acmp_nvm.c",
           "\tif (walk != NVM_W_BIND) {\n\t\treturn n->others->rollback(n->others->ctx, walk);\n\t}",
           "\tif (walk != NVM_W_BIND && false) {\n\t\treturn n->others->rollback(n->others->ctx, walk);\n\t}",
           "acmpnvm", "AcmpStore.N6TheRollBackAndEveryOtherGroup", "N6 every other group"),
    Mutant("acmp-nvm-latch-length-unchecked", "acmp/acmp_nvm.c",
           "\treturn len == ACMP_BINDING_BYTES && acmp_binding_latch(", "\treturn acmp_binding_latch(",
           "acmpnvm", "AcmpStore.N6TheRollBackAndEveryOtherGroup", "N6 a latch of another length gives nothing"),
    Mutant("acmp-nvm-bindings-latched-by-the-others", "acmp/acmp_nvm.c",
           "\tif (group != n->bind_group) {\n\t\treturn n->others->latch(", "\tif (true) {\n\t\treturn n->others->latch(",
           "acmpnvm", "AcmpStore.N1ABindSurvivesAPowerCycleAndFastConnects", "N1 the binding parameters come back"),
    Mutant("acmp-nvm-release-dropped", "acmp/acmp_nvm.c", "\tn->others->release(n->others->ctx);", "\t(void)n;",
           "acmpnvm", "AcmpStore.N6TheRollBackAndEveryOtherGroup", "N6 every other group"),
    Mutant("acmp-nvm-settle-dropped", "acmp/acmp_nvm.c", "\treturn n->others->settle(n->others->ctx);",
           "\t(void)n;\n\treturn NVM_APPLIED;",
           "acmpnvm", "AcmpStore.N6TheRollBackAndEveryOtherGroup", "N6 every other group"),
    Mutant("acmp-nvm-model-always-ready", "acmp/acmp_nvm.c", "\treturn n->others->model_ready(n->others->ctx);",
           "\t(void)n;\n\treturn 1;",
           "acmpnvm", "AcmpStore.N6TheRollBackAndEveryOtherGroup", "N6 the model's readiness is the other owners'"),
)


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


def campaign(root: Path, reuse: Path, part: tuple[int, int] = (1, 1)) -> bool:
    """Plant every mutant of slice `part` (k of n; the whole table by
    default); True when one escaped. One build serves every copy, so a test
    object is compiled again only where a planted header changes what it
    sees."""
    arms = {"model": ctrl_arms.arm_model, "port": ctrl_arms.arm_port, "adp": ctrl_arms.arm_adp,
            "unit": ctrl_arms.arm_unit, "walk": ctrl_arms.arm_walk, "acmp": ctrl_arms.arm_acmp,
            "acmpwalk": ctrl_arms.arm_acmpwalk, "acmpnvm": ctrl_arms.arm_acmpnvm, "entity": ctrl_arms.arm_entity,
            "rv32": lambda tree: ctrl_arms.arm_rv32(tree, True)}
    build = fw_gtest.Build()
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
