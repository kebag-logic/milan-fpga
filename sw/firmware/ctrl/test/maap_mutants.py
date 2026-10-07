# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted F2 defects, graded by named checks rather than any failed build."""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")
Plant = Callable[..., None]


def mutants(kind: Callable[..., T]) -> tuple[T, ...]:
    """Return the core, adapter, stream-output and hook sensitivity controls."""
    out: list[T] = []

    def add(name: str, path: str, old: str, new: str, check: tuple[str, str], arm: str = "maap") -> None:
        """Bind one source defect to its named test and failure text."""
        out.append(kind("maap-" + name, path, old, new, arm, *check))

    _wire(add)
    _lifecycle(add)
    _integration(add)
    _table(add)
    add("allocation-seam-disconnected", "maap/maap.c", "publish(m, m->count, true);",
        "publish(m, m->count, false);", ("MaapHost.AcquiredRangeFeedsExistingCsrPath", "allocation reaches AAF CSR"))
    _review_regressions(add)
    _generic_table(add)
    # R528-2-S1: preserve the review's escaping defect as a named control.
    out.append(kind("r2-saved-range-never-consumed", "maap/maap.c", "m->preferred = 0;",
                    "/* saved preference retained */;", "maap", "MaapCore.LinkBounceDrawsAfterSuppliedRange",
                    "link bounce draws after consuming supplied range"))
    return tuple(out)


def _review_regressions(add: Plant) -> None:
    """Standing R528-1 and R529-1 probes and their original escaping defects."""
    core = "maap/maap.c"
    csr = "maap/maap_csr.c"
    # F3 round 6: MAAP attaches before the open, so its interrupt and filter bits
    # are ctrl_loop_open's mask of bound channels; both defects drop MAAP there.
    add("app-missing-rx-interrupt", "loop/ctrl_loop.c",
        "mbx_irq_enable(mbx_place(open, MBX_IRQ_ENABLE_RX_LSB, MBX_IRQ_ENABLE_RX_WIDTH)",
        "mbx_irq_enable(mbx_place(open & ~(1u << MBX_CH_MAAP), MBX_IRQ_ENABLE_RX_LSB, MBX_IRQ_ENABLE_RX_WIDTH)",
        ("MaapHost.AppWaitWakesForMaapWithinBudget", "accepted MAAP wakes idle loop"))
    add("begin-down-forgets-range", core, "m->preferred = preferred;", "m->preferred = 0;",
        ("MaapCore.BeginBeforePortOperationalRetainsRange", "Begin supplied range survives port down"))
    add("restart-reuses-range", core, "m->state = MAAP_INITIAL;\n\treserve(m, 0);",
        "m->state = MAAP_INITIAL;\n\treserve(m, m->base);",
        ("MaapCore.RestartDrawsNewRange", "fixed seed Restart draws a new range"))
    priority = ("MaapCore.PriorityAfterTiedOctets", "every reversed octet decides")
    add("reverse-five-octets", core, "for (unsigned i = 0; i < 6u; ++i) {",
        "for (unsigned i = 0; i < 5u; ++i) {", priority)
    add("compare-mac-lsb-only", core, "reverse_mac(m->mac) >= reverse_mac(peer)",
        "(reverse_mac(m->mac) >> 40) >= (reverse_mac(peer) >> 40)", priority)
    add("csr-select-listener", csr, "STRM_SEL, 0x100u | k);", "STRM_SEL, k);",
        ("MaapCsr.EveryStreamAddressAndLossGate", "stream destination base plus index"))
    add("csr-enable-before-programming", csr,
        "\tif (c->aaf_outputs != 0u) {\n\t\taddress(c, interface, AAF_DMLO",
        "\twrite_word(c, interface, AAF_CTRL, c->aaf_control);\n"
        "\twrite_word(c, interface, CRFT_CTRL, c->crf_control);\n"
        "\tif (c->aaf_outputs != 0u) {\n\t\taddress(c, interface, AAF_DMLO",
        ("MaapCsr.AdmissionAfterEveryDestinationWrite", "enables follow every destination word"))
    add("poll-first-interface-only", "maap/maap_mbx.c",
        "for (unsigned k = 0; k < MBX_N_IF; ++k) {\n\t\towed = maap_poll",
        "for (unsigned k = 0; k < 1u; ++k) {\n\t\towed = maap_poll",
        ("MaapHost.InterfaceOneStallDrainsWithinBudget", "interface 1 poll drains deferred output"), "maap_if2")


def _generic_table(add: Plant) -> None:
    """R528-1-S1: alter production predicates without fixture MAC literals."""
    core = "maap/maap.c"
    for name, old, new, test, words in (
        ("initial-handles-conflict", "else if (m->state != MAAP_INITIAL) {", "else if (true) {",
         "AllStates/MaapCell.TableB7/0", "Table B.7"),
        ("probe-state-defends", "type == MAAP_MSG_PROBE && m->state == MAAP_DEFEND",
         "type == MAAP_MSG_PROBE && m->state == MAAP_PROBE", "AllStates/MaapCell.TableB7/12", "Table B.7"),
        ("probe-defend-uses-priority", "(m->state == MAAP_PROBE && type != MAAP_MSG_PROBE) ||",
         "false ||", "AllStates/MaapCell.TableB7/10", "Table B.7"),
        ("equal-mac-wins", "reverse_mac(m->mac) >= reverse_mac(peer)",
         "reverse_mac(m->mac) > reverse_mac(peer)", "MaapCore.ReverseOctetPriority", "equal MAC is not lower"),
    ):
        add("generic-" + name, core, old, new, (test, words))


def _wire(add: Plant) -> None:
    core = "maap/maap.c"
    add("down-start-keeps-owner", core, "\t\t} else {\n\t\t\tpublish(m, 0, false);",
        "\t\t} else {\n\t\t\t/* omitted withdrawal */;", ("MaapCore.ReleaseLossAndRetry",
        "starting down withdraws the prior owner"))
    initial = "MaapCore.InitialAndThreeRetransmissions"
    add("initial-send-absent", core, "request(m, MAAP_MSG_PROBE); // Table B.7", "/* omitted */; // Table B.7",
        (initial, "initial PROBE is immediate"))
    add("retransmit-count", "maap/maap.h", "#define MAAP_PROBE_RETRANSMITS 3u", "#define MAAP_PROBE_RETRANSMITS 2u",
        (initial, "three retransmissions remain"))
    add("probe-count-not-decremented", core, "m->probe_count--;", "m->probe_count -= 0u;", (initial,
        "retransmission decrements once"))
    for name, field, replacement in (
        ("version", "f[16] = 0x08u;", "f[16] = 0u;"),
        ("length", "f[17] = 16u;", "f[17] = 28u;"),
        ("source", "wire_put_be(f + 6, m->mac, 6);", "wire_put_be(f + 6, m->mac + 1u, 6);"),
        ("padding", "memset(f, 0, MAAP_FRAME_BYTES);", "memset(f, 1, MAAP_FRAME_BYTES);"),
    ):
        add("wire-" + name, core, field, replacement, (initial, "B.2 complete PROBE bytes"))
    for symbol, value in (("PROBE_BASE", 500), ("PROBE_VARIATION", 100),
                          ("ANNOUNCE_BASE", 30000), ("ANNOUNCE_VARIATION", 2000)):
        add("constant-" + symbol.lower(), "maap/maap.h", f"#define MAAP_{symbol}_MS {value}u",
            f"#define MAAP_{symbol}_MS {value + 1}u", ("MaapCore.ConstantsStrictTimersAndSeed", ""))
    add("seed-clock-ignored", core, "(uint32_t)m->mac + m->ports->clock(m->ports->ctx)",
        "(uint32_t)m->mac + (m->ports->clock(m->ports->ctx) & 0u)",
        ("MaapCore.ConstantsStrictTimersAndSeed", ""))
    add("zero-seed-sticks", core, "m->rng = 1u;", "m->rng = 0u;", ("MaapCore.ConstantsStrictTimersAndSeed",
        "zero sum cannot lock generator"))
    add("biased-random-bucket", core, "} while (word > limit);", "} while (word > limit && false);",
        ("MaapCore.UniformDrawRejectsIncompleteBucket", "incomplete random bucket rejected"))
    add("numeric-mac-priority", core, "reverse_mac(m->mac) >= reverse_mac(peer)",
        "(reverse_mac(m->mac) & 0u) + m->mac >= (reverse_mac(peer) & 0u) + peer",
        ("MaapCore.ReverseOctetPriority", "least significant octet decides first"))
    add("defend-multicast", core, "enqueue(m, MAAP_MSG_DEFEND, peer, start, count, overlap,",
        "enqueue(m, MAAP_MSG_DEFEND, MAAP_MULTICAST, start, count, overlap,",
        ("MaapCore.DefendEchoAndIntersection", "echo request and exact intersection"))
    add("defend-echo-own-range", core, "peer, start, count, overlap,", "peer, m->base, m->count, overlap,",
        ("MaapCore.DefendEchoAndIntersection", "echo request and exact intersection"))
    add("intersection-too-long", core, "(uint16_t)(last - overlap)", "(uint16_t)(last - overlap + 1u)",
        ("MaapCore.DefendEchoAndIntersection", "echo request and exact intersection"))
    add("adjacent-overlaps", core, "start < ours_end && m->base < end", "start <= ours_end && m->base <= end",
        ("MaapCore.DisjointAdjacentZeroAndDefendRange", "half open intervals"))
    add("zero-count-conflicts", core, "if (count != 0u && start < ours_end",
        "if ((count != 0u || true) && start < ours_end",
        ("MaapCore.DisjointAdjacentZeroAndDefendRange", "half open intervals"))
    add("defend-checks-request", core, "type == MAAP_MSG_DEFEND ? 34 : 26", "type == MAAP_MSG_DEFEND ? 26 : 26",
        ("MaapCore.DisjointAdjacentZeroAndDefendRange", "DEFEND tests conflict fields"))
    for name, old, new in (
        ("ethertype", "wire_be16(f + 12) != 0x22f0u", "false"),
        ("subtype", "f[14] != 0xfeu", "false"),
        ("version", "(f[15] & 0xf0u) != 0u", "false"),
        ("reserved-zero", "(f[15] & 0x0fu) < MAAP_MSG_PROBE", "false"),
        ("reserved-high", "(f[15] & 0x0fu) > MAAP_MSG_ANNOUNCE", "false"),
        ("cdl-short", "(wire_be16(f + 16) & 0x7ffu) < 16u", "false"),
        ("cdl-truncated", "(wire_be16(f + 16) & 0x7ffu) > len - 26u", "false"),
        ("cdl-current", "((f[16] >> 3) <= 1u && (wire_be16(f + 16) & 0x7ffu) != 16u)", "false"),
        ("source-zero", "mac_at(f + 6) == 0u", "false"),
        ("source-group", "(f[6] & 1u) != 0u", "false"),
        ("destination", "dst == MAAP_MULTICAST ||", "dst != 0u ||"),
        ("own-probe", "(f[15] == MAAP_MSG_DEFEND && dst == m->mac)", "dst == m->mac"),
    ):
        add("malformed-" + name, core, old, new, ("MaapCore.MalformedAndVersionCompatibility",
            "malformed input is rejected"))
    add("valid-minimum-refused", core, "len < 42u", "len < 43u",
        ("MaapCore.MalformedAndVersionCompatibility", "B.2.3 recognized future"))
    add("future-version-refused", core, "if (len < 42u ||", "if ((len >= 42u && (f[16] >> 3) > 1u) || len < 42u ||",
        ("MaapCore.MalformedAndVersionCompatibility", "B.2.3 recognized future"))


def _lifecycle(add: Plant) -> None:
    core = "maap/maap.c"
    add("range-end-off-by-one", core, "base <= MAAP_POOL_BASE + MAAP_POOL_SIZE - count",
        "base <= MAAP_POOL_BASE + MAAP_POOL_SIZE - count + 1u", ("MaapCore.InitAndPreferredRangeBounds", ""))
    add("port-up-keeps-claim", core, "restart(m); // Table B.7 PortOperational!",
        "/* omitted */; // Table B.7 PortOperational!",
        ("MaapCore.ReleaseLossAndRetry", "PortOperational invalidates acquired address"))
    add("release-keeps-enable", core, "m->enabled = false;", "m->enabled = true;",
        ("MaapCore.ReleaseLossAndRetry", "released instance stays idle"))
    add("expiry-forgotten-on-stall", core, "m->expiry_owed = true;", "m->expiry_owed = false;",
        ("MaapCore.StalledOutputRetainsOrderAndOriginalExpiry", "original expiry remains owed"))
    add("allocation-before-commit", core, "m->state = MAAP_DEFEND;",
        "m->state = MAAP_DEFEND; publish(m, m->count, true);",
        ("MaapCore.StalledOutputRetainsOrderAndOriginalExpiry", "allocation waits for committed ANNOUNCE"))
    add("probe-announce-reordered", core, "request(m, MAAP_MSG_ANNOUNCE);\n\t\t\tm->state = MAAP_DEFEND;",
        "request(m, MAAP_MSG_ANNOUNCE);\n\t\t\tm->queue[0][15] = MAAP_MSG_ANNOUNCE;\n\t\t\tm->state = MAAP_DEFEND;",
        ("MaapCore.StalledOutputRetainsOrderAndOriginalExpiry", ""))
    add("overflow-uncounted", core, "m->overflow++;", "m->overflow += 0u;",
        ("MaapCore.QueueBoundAndWithdrawal", "overload is counted as failure"))
    add("poll-unbounded", core, "n < 2u &&", "n < MAAP_QUEUE_FRAMES &&",
        ("MaapCore.QueueBoundAndWithdrawal", "poll has bounded work"))
    add("release-leaves-output", core, "m->state = MAAP_INITIAL;\n\tm->queued = 0;",
        "m->state = MAAP_INITIAL;\n\tm->queued += 0;", ("MaapCore.QueueBoundAndWithdrawal", ""))
    add("reentry-not-counted", core, "m->reentries++;", "m->reentries += 0u;",
        ("MaapCore.ReentrantPortsAreCountedAndIgnored", "all input guards fire"))
    add("debug-no-assert", core, "assert(!m->in_call);", "assert(true);",
        ("MaapDebug.SynchronousExpiryAsserts", "debug reentry assertion"), "maap_debug")


def _integration(add: Plant) -> None:
    core = "maap/maap.c"
    adapter = "maap/maap_mbx.c"
    csr = "maap/maap_csr.c"
    add("stream-index-missing", csr, "STRMW_DMLO, STRMW_DMHI, base + k", "STRMW_DMLO, STRMW_DMHI, base",
        ("MaapCsr.EveryStreamAddressAndLossGate", "stream destination base plus index"))
    add("selection-not-restored", csr, "STRM_SEL, selection);", "STRM_SEL, selection & 0u);",
        ("MaapCsr.EveryStreamAddressAndLossGate", "selection restored"))
    add("fabric-owner-kept", csr, "MAAP_CTRL, fabric & ~1u", "MAAP_CTRL, fabric",
        ("MaapCsr.EveryStreamAddressAndLossGate", "fabric MAAP disabled without touching seed"))
    add("loss-keeps-crf", csr, "CRFT_CTRL, c->crf_control & ~1u", "CRFT_CTRL, c->crf_control",
        ("MaapCsr.EveryStreamAddressAndLossGate", "loss closes both media gates"))
    add("count-mismatch-accepted", csr, "if (count != c->aaf_outputs", "if (false && count != c->aaf_outputs",
        ("MaapCsr.ShapesAndCountRefusal", "wrong shape stays disabled"))
    add("crf-index-wrong", csr, "base + c->aaf_outputs", "base + c->aaf_outputs + 1u",
        ("MaapCsr.ShapesAndCountRefusal", "CRF only shape"))
    add("timer-tag-ignored", adapter, "!i->armed || ev->timer_tag != i->tag", "!i->armed",
        ("MaapHost.StaleTagsForeignInputsAndLinkEdges", "old timer tag ignored"))
    add("foreign-not-counted", adapter, "m->foreign_if++;\n\t\treturn;", "m->foreign_if += 0u;\n\t\treturn;",
        ("MaapHost.StaleTagsForeignInputsAndLinkEdges", ""))
    add("half-attach", adapter, "loop->n_polls >= CTRL_LOOP_MAX_POLLS ||", "false ||",
        ("MaapHost.AttachRefusalsAndTimerWrap", "no partial attachment"))
    add("interface-zero", adapter, "maap_rx(&m->ifs[f->interface].core", "maap_rx(&m->ifs[0].core",
        ("MaapHost.InterfaceIsolationAndRangeEnvelope", "record index selects state"), "maap_if2")
    add("no-range-filter", adapter, "last > first ? (uint16_t)(last - first) : 0u",
        "last > first ? (uint16_t)0u : 0u", ("MaapHost.HMaapConflictLossAndRetry", ""))
    add("filter-destination-ignored", "host/mbx_model.c", "&& dst == mac &&", "&& (dst == mac || true) &&",
        ("MaapHost.HMaapFilterTupleAndRate", ""))
    add("late-service", adapter, "\t(void)ctx;\n\treturn mbx_tx_send",
        "\t(void)ctx;\n\tfor (unsigned k = 0; k < 100001u; ++k) { (void)mbx_now_ms(); }\n\treturn mbx_tx_send",
        ("MaapHost.HMaapTimerCommitsAndIntervals", "H-MAAP original timer deadline"))
    add("stall-unqueued", core, "m->deferred++;", "m->deferred++; m->queued = 0u;",
        ("MaapHost.HMaapBacklogAndStallNeverRestartClock", ""))
    add("app-channel-closed", "loop/ctrl_loop.c", "\tmbx_filter_open(open);\n",
        "\tmbx_filter_open(open & ~(1u << MBX_CH_MAAP));\n", ("MaapHost.ExplicitAppComposition", ""))
    add("callback-work-overrun", adapter, "\tstruct maap_mbx *m = ctx;\n\tif (ev->type",
        "\tstruct maap_mbx *m = ctx;\n\t(void)mbx_now_ms();\n\tif (ev->type",
        ("MaapHost.CallbackWorkAndEveryOutputCount", "callback work bound"))
    add("ignored-input-late", adapter, "\tmaap_rx(&m->ifs[f->interface].core",
        "\tfor (unsigned k = 0; k < 100001u; ++k) { (void)mbx_now_ms(); }\n"
        "\tmaap_rx(&m->ifs[f->interface].core",
        ("MaapHost.IgnoredInputCommitsStateWithinOriginalBudget", "state completion uses original RX budget"))


def _table(add: Plant) -> None:
    core = "maap/maap.c"
    # Each of the eighteen applied receive/state/priority cells gets its own
    # defect: suppress an action, or create one where the table ignores it.
    for state in range(3):
        for wins in (False, True):
            for msg in range(1, 4):
                key = state * 6 + (3 if wins else 0) + msg - 1
                acts = state != 0 and ((state == 2 and msg == 1) or
                       (state == 1 and msg != 1) or not wins)
                peer = "0x0200000000c0" if wins else "0x060000000040"
                injected = (f"\tif (len >= 42u && m->state == {state} && f[15] == {msg}u && "
                            f"mac_at(f + 6) == UINT64_C({peer})) {{\n"
                            + ("\t\trestart(m); (void)pump(m);\n" if not acts else "")
                            + "\t\tm->in_call = false; return;\n\t}\n\tif (!decode(m, f, len)) {")
                add(f"table-b7-{key}", core, "\tif (!decode(m, f, len)) {", injected,
                    (f"AllStates/MaapCell.TableB7/{key}", "Table B.7"))
