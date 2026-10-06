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
           "F2 all 16 event records are taken by pass"),
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
           "D1 and the ring is resynchronised"),
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
)


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


def campaign(root: Path, reuse: Path) -> bool:
    """Plant every mutant; True when one escaped. One build serves every
    copy, so a test object is compiled again only where a planted header
    changes what it sees."""
    arms = {"model": ctrl_arms.arm_model, "port": ctrl_arms.arm_port, "adp": ctrl_arms.arm_adp,
            "walk": ctrl_arms.arm_walk, "entity": ctrl_arms.arm_entity,
            "rv32": lambda tree: ctrl_arms.arm_rv32(tree, True)}
    build = fw_gtest.Build()
    escaped = 0
    for m in MUTANTS:
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
    print(f"mutants: {len(MUTANTS) - escaped} of {len(MUTANTS)} caught")
    return escaped != 0
