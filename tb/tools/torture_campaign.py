#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""torture_campaign.py - the reusable plan, check registry and verdict format
for the standing torture/compliance campaign.

    # what a full run WOULD do, without touching anything
    ./torture_campaign.py --plan
    # only one area, as JSON, for a runner to consume
    ./torture_campaign.py --plan --areas matrix --json
    # the entries a human has to perform (cables, power) as a checklist
    ./torture_campaign.py --checklist
    # the offline unit tests
    ./torture_campaign.py --self-test

WHAT THIS FILE IS.  The campaign's PLAN and its ASSERTION CONTRACT, with no
I/O.  It knows every talker x listener x index combination that must be walked,
every churn sequence, every adverse condition, and - for each - the exact set of
assertions that step owes and the clause each assertion comes from.  It does not
open a socket.  Two consumers drive it:

  * the on-bench runner (milan-tests-avb/tools/milan_torture.py), which executes
    the steps over avdecc_l2.py and emits one JSONL verdict per assertion;
  * the offline conformance suite (tests/features/torture_matrix_plan.feature),
    which asserts the PLAN's OWN coverage - that it walks every index and not
    just index 0, both directions, the CRF stream, and that no step is allowed
    to skip an assertion the clause requires.

Separating the plan from the wire is what makes the coverage testable at a desk.
A runner that decides its own coverage as it goes can only be audited by running
it on hardware, and hardware time is the scarce resource.

WHY INDEX 0 IS NEVER ENOUGH (standing user rule, and the evidence for it).
Index 0 is the least representative index on this device: the 0x800 per-stream
window makes index 0 a HARD ALIAS of the legacy flat registers
(docs/reference/REGISTER_MAP.md, "the alias rule"), so an index-0 pass exercises
the alias path and not the indexed one.  Four separate per-index defects hid
behind index-0-only testing: GET_STREAM_INFO served index 0's answer for every
index, MAX_TRANSIT_TIME existed only at index 0, GET_COUNTERS answered only
index 0 (and sinks >= 2 fell to an empty mask), and the window's talker state
bits were hardwired 0 at idx > 0.  Every plan this file emits therefore walks
EVERY index, and `plan_covers_every_index()` is asserted by the offline suite.

LEVEL AND ORACLE (docs/testing/methodology.md §2).  The plan itself is an L3
artifact: its oracle is the clause list below, and the offline suite checks the
plan against it.  When a runner executes the plan it becomes L5 (the wire, on
hardware, against a qualified reference device).  The plan cannot tell whether
the fabric is right - only that the right questions get asked.

THE CLAUSES THE ASSERTION CONTRACT IS BUILT FROM.

  Milan v1.2 5.3.8.10 + Table 5.6 - the TEN Stream Input diagnostic counters,
    and the invariant this campaign checks after every bind:
    "At any time, the PAAD-AE shall ensure that either
     MEDIA_LOCKED=MEDIA_UNLOCKED (in this case, the input stream is not
     synchronized on the media clock), or
     MEDIA_LOCKED=MEDIA_UNLOCKED+1 (in this case, the input stream is
     synchronized on the media clock)."
    Also: "The PAAD-AE shall reset all of these counters to zero each time the
    Stream Input changes its state from not bound to bound." - so a rebind is
    ALSO a counter-reset assertion, and the plan says so.
  Milan v1.2 5.3.7.7 + Table 5.4 - the FIVE Stream Output counters, and the
    talker invariant: "either STREAM_START=STREAM_STOP+1 (in this case, the
    Talker is currently streaming), or STREAM_START=STREAM_STOP".
    MEDIA_RESET / TIMESTAMP_UNCERTAIN / FRAMES_TX are "Reset to 0 each time the
    Talker starts streaming", which is why a FRAMES_TX delta is only meaningful
    inside one streaming episode.
  Ruling #726 (2026-10-12) resolves the ambiguous observation-interval
    wording in Milan v1.2 Tables 5.4/5.6 through IEEE 1722.1-2021 Tables
    7.159/7.157: FRAMES_TX and FRAMES_RX count every Stream Data AVTPDU.
    Cross-device comparisons use packet deltas within the same streaming
    episode. An interval-rate side on a measured flowing stream fails;
    the finding belongs to that side. Anomaly counters keep their own laws.
  IEEE 1722.1-2021 Table 7-156/7-157 - the STREAM_INPUT counters_valid bit
    field and the block offsets, and the trap that comes with them: the table
    numbers bits MSB-FIRST ("Bit # 31 ... MEDIA_LOCKED" is the counter at block
    offset 0), the same convention Table 6-2 uses for entity_capabilities where
    "Bit # 31 ... EFU_MODE" is the value la_avdecc calls 1u << 0.  So
    counters_valid bit (31 - offset/4) is the standard's numbering and
    1 << (offset/4) is the mask on the wire.  Reading the table without that
    conversion inverts every mask.
  Milan v1.2 5.4.2.25 - GET_COUNTERS is mandatory per descriptor, so every
    index must answer, not only index 0.
  Milan v1.2 5.5.3.5.43 - the SETTLED_RSV_OK / RCV_BIND_RX_CMD transition: a
    BIND_RX for a Stream Input that is already bound is honoured as an IMPLICIT
    REBIND without an intervening unbind.  That is a state transition with its
    own counter-reset consequence, and it is the churn case a naive
    bind/unbind/bind loop never reaches.
  Milan v1.2 5.3.7.3 - a bound talker STREAMS; STREAMING_WAIT "shall not be
    implemented", so there is no legitimate bound-and-silent state to excuse a
    missing FRAMES_TX.
  the Milan adverse-network-conditions recommended practice, §2 -
    "It is recommended that a Milan device, while in a streaming state ...
    shall not experience any stream interruption when subjected to high rate
    Non-Priority traffic.  Attention is drawn to the case of unicast traffic
    with a MAC addresses matching that of the device ... As AVDECC traffic is
    Non-Priority, it is not expected that a Milan device remains responsive to
    AVDECC commands while subjected to high rate Non-Priority traffic."
    TWO honesty notes that this file encodes rather than glosses:
      (1) that document is a RECOMMENDED PRACTICE - "It is not a current
          requirement for a Milan device to support the features mentioned" -
          so its entries are marked severity RECOMMENDED, and a failure is a
          finding, not a conformance failure;
      (2) it says explicitly that AVDECC responsiveness is NOT expected under
          storm, so a runner that fails an entity for not answering GET_COUNTERS
          during a storm is asserting the opposite of the document.  The storm
          entries therefore assert STREAM CONTINUITY and record control-plane
          responsiveness as INFO.
    It covers exactly ONE condition - sustained high rate traffic, in four
    traffic classes - and it says nothing about malformed frames, so the
    malformed/truncated-frame entries here are NOT sourced from it.  They cite
    1722.1-2021 9.2.1.1.6 (control_data_length) and 9.2.1.2 (a command with a
    bad payload gets a status, not silence) instead.
  Milan v1.2 5.3.7.3 again, for the LICENCE the whole streaming-verdict set
    depends on: "As long as a PAAD is declaring a Talker Advertise attribute
    and receiving a Listener Ready or Listener Ready Failed attribute for a
    Stream Output, it shall be streaming AVTP packets."  The licence is
    therefore a CONJUNCTION, and the second half of it is not ours: it arrives
    over MSRP from the listener through the bridge.  On this fabric the
    conjunction is readable as LWSRP_STATUS (CSR 0x694) bit 8, the stream gate.
    A bind that returns SUCCESS while the gate is SHUT is a talker that is
    CORRECTLY silent, so every frames-advance verdict in this file is
    conditional on that reading and SKIPs without it.  Asserting them
    unconditionally turns ~135-285 conformant steps into SHALL failures, which
    is the exact shape of a campaign that is worse than no campaign.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field, asdict, replace
from decimal import Decimal
from functools import lru_cache
from typing import Optional

# ------------------------------------------------------- counter definitions --
#: Milan v1.2 Table 5.6, in IEEE 1722.1-2021 Table 7-157 block order.
MILAN_TABLE_56 = (
    "MEDIA_LOCKED", "MEDIA_UNLOCKED", "STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH",
    "MEDIA_RESET", "TIMESTAMP_UNCERTAIN", "UNSUPPORTED_FORMAT",
    "LATE_TIMESTAMP", "EARLY_TIMESTAMP", "FRAMES_RX")
#: IEEE 1722.1-2021 Table 7-157 - the full STREAM_INPUT block, offsets 0..44.
IEEE_STREAM_INPUT_BLOCK = (
    "MEDIA_LOCKED", "MEDIA_UNLOCKED", "STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH",
    "MEDIA_RESET", "TIMESTAMP_UNCERTAIN", "TIMESTAMP_VALID",
    "TIMESTAMP_NOT_VALID", "UNSUPPORTED_FORMAT", "LATE_TIMESTAMP",
    "EARLY_TIMESTAMP", "FRAMES_RX")
#: Milan v1.2 Table 5.4 (la_avdecc StreamOutputCounterValidFlagMilan12) - the
#: Milan talker block is DENSE and is NOT the 1722.1-2021 layout.
MILAN_TABLE_54 = ("STREAM_START", "STREAM_STOP", "MEDIA_RESET",
                  "TIMESTAMP_UNCERTAIN", "FRAMES_TX")
#: IEEE 1722.1-2021 Table 7-159 - the OTHER STREAM_OUTPUT layout.  A device
#: serves one or the other; a controller picks by Milan compatibility.  Both are
#: named here so a runner never silently assumes.
IEEE_STREAM_OUTPUT_BLOCK = (
    "STREAM_START", "STREAM_STOP", "STREAM_INTERRUPTED", "MEDIA_RESET",
    "TIMESTAMP_UNCERTAIN", "TIMESTAMP_VALID", "TIMESTAMP_NOT_VALID",
    "FRAMES_TX")
#: IEEE 1722.1-2021 Table 7-153.
IEEE_AVB_INTERFACE_BLOCK = ("LINK_UP", "LINK_DOWN", "FRAMES_TX", "FRAMES_RX",
                            "RX_CRC_ERROR", "GPTP_GM_CHANGED")

#: The Milan mandatory ten as a counters_valid mask, in the ON-THE-WIRE
#: numbering (bit = block offset / 4).  0xF3F = the ten of Table 5.6; the two
#: 1722.1 tv-bit tallies are bits 6 and 7, so a device serving all twelve
#: publishes 0xFFF.
MILAN_INPUT_MANDATORY_MASK = 0xF3F
MILAN_INPUT_FULL_MASK = 0xFFF
MILAN_OUTPUT_MASK = 0x01F
AVB_INTERFACE_EXPECT_MASK = 0x023      # LINK_UP | LINK_DOWN | GPTP_GM_CHANGED


def counters_valid_bit_ieee(block_offset: int) -> int:
    """The IEEE table's own bit NUMBER for a counter at `block_offset`.

    IEEE 1722.1-2021 Table 7-156 numbers counters_valid MSB-first: the entry
    "Bit # 31" is the counter at block offset 0.  Table 6-2 numbers
    entity_capabilities the same way, and there the "Bit # 31" entry EFU_MODE is
    the value every implementation writes as 1u << 0 - which is what pins the
    convention.  So the wire mask for a counter is 1 << (offset/4) while the
    table calls that same bit number 31 - offset/4.  Both numbers are produced
    here so no reader has to reconstruct the conversion from memory.
    """
    if block_offset % 4:
        raise ValueError("counter block offsets are quadlet-aligned")
    slot = block_offset // 4
    if not 0 <= slot <= 31:
        raise ValueError("counter block holds 32 quadlets")
    return 31 - slot


def counters_valid_mask(names: Iterable[str], block: Sequence[str]) -> int:
    """The on-the-wire counters_valid mask for `names` within `block`."""
    m = 0
    for n in names:
        m |= 1 << block.index(n)
    return m


def decode_counters_arrays(counters_valid: int, raw: Sequence[int],
                           block: Sequence[str]) -> dict[str, object]:
    """The same decode from an already-parsed mask + 32-quadlet array.

    avdecc_l2.py hands a runner `counters_valid` and `raw` out of its JSON, so
    this is the entry point the bench uses; decode_counters_payload() is the
    same logic from octets and is what the offline byte-vector tests drive.
    """
    decoded, unnamed = {}, []
    vals = list(raw) + [0] * max(0, 32 - len(raw))
    for i in range(32):
        if counters_valid & (1 << i):
            if i < len(block):
                decoded[block[i]] = vals[i]
            else:
                unnamed.append(i)
    return {"counters_valid": counters_valid, "decoded": decoded,
            "claimed_but_unnamed_slots": unnamed, "raw": vals}


def decode_counters_payload(payload: bytes,
                            block: Sequence[str]) -> dict[str, object]:
    """A GET_COUNTERS response payload -> {name: value} for the claimed slots.

    Layout, IEEE 1722.1-2021 7.4.42.2: descriptor_type(2) descriptor_index(2)
    counters_valid(4) counters_block(128 = 32 quadlets).  `block` is the name
    tuple for the descriptor - and WHICH tuple is a decision, not a detail: a
    STREAM_OUTPUT block decoded with the 1722.1 layout when the device serves
    the Milan one mislabels FRAMES_TX as TIMESTAMP_UNCERTAIN, because those
    names sit at different offsets in the two tables.  The caller states the
    layout so the choice is visible in the caller.

    A slot the mask does not claim is NOT reported at all.  Reporting it as 0
    is exactly the failure methodology R5 names: a structural zero read as a
    measurement.
    """
    if len(payload) < 8 + 128:
        raise ValueError(f"counters payload is {len(payload)} octets, "
                         f"needs {8 + 128}")
    dtype = int.from_bytes(payload[0:2], "big")
    dindex = int.from_bytes(payload[2:4], "big")
    valid = int.from_bytes(payload[4:8], "big")
    vals = [int.from_bytes(payload[8 + 4 * i:12 + 4 * i], "big")
            for i in range(32)]
    out = decode_counters_arrays(valid, vals, block)
    out["descriptor_type"] = dtype
    out["descriptor_index"] = dindex
    return out


def check_lock_invariant(decoded: dict) -> tuple:
    """Milan v1.2 Table 5.6, verbatim: "At any time, the PAAD-AE shall ensure
    that either MEDIA_LOCKED=MEDIA_UNLOCKED ... or
    MEDIA_LOCKED=MEDIA_UNLOCKED+1"."""
    if "MEDIA_LOCKED" not in decoded or "MEDIA_UNLOCKED" not in decoded:
        return ("SKIP", {"why": "the mask does not claim both lock counters"})
    ml, mu = decoded["MEDIA_LOCKED"], decoded["MEDIA_UNLOCKED"]
    ok = ml in (mu, mu + 1)
    return ("PASS" if ok else "FAIL",
            {"media_locked": ml, "media_unlocked": mu,
             "synchronized": ml == mu + 1})


def check_talker_invariant(decoded: dict) -> tuple:
    """Milan v1.2 Table 5.4, verbatim: "either STREAM_START=STREAM_STOP+1 (in
    this case, the Talker is currently streaming), or
    STREAM_START=STREAM_STOP"."""
    if "STREAM_START" not in decoded or "STREAM_STOP" not in decoded:
        return ("SKIP", {"why": "the mask does not claim both start/stop"})
    a, b = decoded["STREAM_START"], decoded["STREAM_STOP"]
    ok = a in (b, b + 1)
    return ("PASS" if ok else "FAIL",
            {"stream_start": a, "stream_stop": b, "streaming": a == b + 1})


#: Milan v1.2 Table 5.4 / Table 5.6, verbatim: "The duration of the observation
#: interval is implementation-specific and shall be less than or equal to 1
#: second."  The clause bounds the interval from ABOVE ONLY.  So ANY interval in
#: (0, 1 s] is conformant, a 5 ms interval ticking 200/s is conformant, and only
#: an implied interval LONGER than a second violates anything.  A band table
#: that called 200/s "neither" was failing a conformant device.
MILAN_MAX_OBSERVATION_INTERVAL_S = 1.0

#: Ceiling slack for a rate measured WITHOUT a known window.  A conformant
#: counter at the exact 1 s ceiling, measured over a finite window, loses up to
#: one tick to phase - floor(W) ticks over W seconds - so its measured rate
#: sits BELOW 1/s: 0.996/s over the ~9 s spans this bench measures.  A
#: tolerance-free `implied <= 1 s` test therefore fails the MANDATED behaviour
#: at the boundary; ax-rv32-f filed 26 conformant rows that way (H2), the same
#: verdict inversion this classifier already had once at the other end of the
#: band.  When the window IS known the exact quantization bound floor(W/T)/W is
#: used instead and this slack does not apply.  15% covers one lost tick for
#: every span >= 8 s; callers measuring shorter windows must pass window_s.
INTERVAL_CEILING_SLACK = 0.15


def check_tv_tnv(decoded: dict, tolerance: int = 2) -> tuple:
    """Check the three per-AVTPDU totals under ruling #726 (2026-10-12).

    IEEE 1722.1-2021 Table 7.157 defines the packet law. FRAMES_RX publication
    may lag TV/TNV until the interval commit. A single lower FRAMES_RX snapshot
    is diagnostic only; grade_counter_semantics() checks growth with flow evidence.
    The all-zero and unclaimed cases still provide no measurement evidence.
    """
    need = ("TIMESTAMP_VALID", "TIMESTAMP_NOT_VALID", "FRAMES_RX")
    if any(k not in decoded for k in need):
        return ("SKIP", {"why": "the mask does not claim tv/tnv/frames_rx",
                         "missing": [k for k in need if k not in decoded]})
    tv, tnv, frx = (decoded[k] for k in need)
    total = tv + tnv
    if total == 0 and frx == 0:
        return ("SKIP", {"tv_plus_tnv": 0, "frames_rx": 0,
                         "why": "all three counters are zero, so neither "
                                "reading is distinguishable and the identity is "
                                "vacuous; Milan 5.3.8.10 zeroes the block on "
                                "not-bound -> bound, so re-read AFTER a "
                                "streaming window instead of at the bind"})
    if frx > 0 and abs(total - frx) <= tolerance:
        return ("PASS", {"tv_plus_tnv": total, "frames_rx": frx,
                         "reading": "1722.1-per-frame"})
    if total > frx:
        return ("INFO", {"tv_plus_tnv": total, "frames_rx": frx,
                         "ratio": total / frx if frx else None,
                         "reading": "unequal-packet-totals",
                         "why": "FRAMES_RX is below TV+TNV; coalesced "
                                "publication can lag between commits. "
                                "Grade FRAMES_RX growth over a measured "
                                "flowing window under Table 7.157."})
    return ("FAIL", {"tv_plus_tnv": total, "frames_rx": frx,
                     "why": "FRAMES_RX differs from TV+TNV: "
                            "every frame is counted by exactly one of "
                            "the two tv tallies"})


def frames_rate_reading(rate_per_s: float, nominal_frame_rate: float = 8000.0,
                        max_interval_s: float =
                        MILAN_MAX_OBSERVATION_INTERVAL_S,
                        window_s: Optional[float] = None) -> dict:
    """Describe a rate using historical packet/interval diagnostic bands.

    These labels do not grant conformance. Ruling #726 requires per-AVTPDU
    FRAMES_RX; grade_counter_semantics() applies that law with flow evidence.
    The legacy interval classifier retains its one-tick quantization allowance.
    """
    implied = (1.0 / rate_per_s) if rate_per_s > 0 else None
    if rate_per_s <= 0:
        return {"band": "neither", "rate_per_s": rate_per_s,
                "implied_interval_s": None,
                "why": "nothing moved: no frame was transmitted/received in the "
                       "window under either reading"}
    if rate_per_s >= 0.5 * nominal_frame_rate:
        return {"band": "per-frame", "rate_per_s": rate_per_s,
                "implied_interval_s": implied,
                "why": "IEEE 1722.1-2021 Table 7-157/7-159 per-frame reading "
                       "(the rate is within a factor of two of the nominal "
                       "frame rate)"}
    if window_s and window_s > 0:
        whole = int(window_s / max_interval_s)
        #! COMPARE IN TICKS, NOT RATES.  The rate arrives divided by the
        #! UNROUNDED span while window_s is deltas()'s 3-decimal stamp, so a
        #! rate-space compare at exact equality loses to ~5e-5 of rounding
        #! skew: ax-rv32-g re-filed 9 ticks / 9.0424 s (0.99531/s) as
        #! "neither" against a 9/9.042 = 0.99536/s bound.  The tick count is
        #! an integer and survives the rounding on either side.
        ticks = int(round(rate_per_s * window_s))
        interval_ok = whole == 0 or ticks >= whole
        quant = (f"a conformant counter at the exact {max_interval_s:g} s "
                 f"ceiling shows as few as {whole} ticks over the "
                 f"{window_s:.4g} s measured span; this measurement is "
                 f"{ticks} tick(s)")
    else:
        interval_ok = implied is not None and \
            implied <= max_interval_s * (1.0 + INTERVAL_CEILING_SLACK)
        quant = (f"no measured span was given, so the ceiling carries "
                 f"{INTERVAL_CEILING_SLACK:.0%} slack for tick quantization")
    if interval_ok:
        return {"band": "interval", "rate_per_s": rate_per_s,
                "implied_interval_s": implied,
                "why": f"Milan v1.2 Table 5.4/5.6 interval reading; the implied "
                       f"observation interval is {implied:.4g} s against the "
                       f"{max_interval_s:g} s ceiling ({quant})"}
    return {"band": "neither", "rate_per_s": rate_per_s,
            "implied_interval_s": implied,
            "why": f"the implied observation interval is {implied:.4g} s, and "
                   f"Milan v1.2 Table 5.4/5.6 require it to be less than or "
                   f"equal to {max_interval_s:g} s - beyond what tick "
                   f"quantization explains ({quant})"}


def frames_rate_band(rate_per_s: float, nominal_frame_rate: float = 8000.0,
                     max_interval_s: float =
                     MILAN_MAX_OBSERVATION_INTERVAL_S,
                     window_s: Optional[float] = None) -> str:
    """`frames_rate_reading()["band"]`, kept as the short form for callers that
    only need the label."""
    return frames_rate_reading(rate_per_s, nominal_frame_rate,
                               max_interval_s, window_s=window_s)["band"]


#: Per-counter laws after ruling #726 (2026-10-12).
#: FRAMES_RX follows IEEE 1722.1-2021 Table 7.157 per AVTPDU.
#: Six anomaly counters retain Milan Table 5.6 observation intervals.
STREAM_INPUT_COUNTER_LAW = {
    "MEDIA_LOCKED": ("per-event", "Milan v1.2 Table 5.6",
                     "the input stream gets synchronized on the media clock"),
    "MEDIA_UNLOCKED": ("per-event", "Milan v1.2 Table 5.6",
                       "the input stream gets unsynchronized on the media "
                       "clock"),
    "STREAM_INTERRUPTED": ("per-event", "Milan v1.2 Table 5.6",
                           "the stream playback is interrupted for any reason "
                           "other than a Controller Unbind operation"),
    "SEQ_NUM_MISMATCH": ("per-interval", "Milan v1.2 Table 5.6",
                         "a Stream Data AVTPDU has been received with a "
                         "non-sequential sequence_num field"),
    "MEDIA_RESET": ("per-interval", "Milan v1.2 Table 5.6",
                    "the 'mr' bit was toggled in any of the received Stream "
                    "Data AVTPDUs"),
    "TIMESTAMP_UNCERTAIN": ("per-interval", "Milan v1.2 Table 5.6",
                            "the 'tu' bit was set in any of the received "
                            "Stream Data AVTPDUs"),
    "TIMESTAMP_VALID": ("per-frame", "IEEE 1722.1-2021 Table 7-157",
                        "receipt of a Stream data AVTPDU with the tv bit set"),
    "TIMESTAMP_NOT_VALID": ("per-frame", "IEEE 1722.1-2021 Table 7-157",
                            "receipt of a Stream data AVTPDU with tv bit "
                            "cleared"),
    "UNSUPPORTED_FORMAT": ("per-interval", "Milan v1.2 Table 5.6",
                           "a Stream Data AVTPDU has been received with a "
                           "format that did not match the current format of "
                           "the Stream Input"),
    "LATE_TIMESTAMP": ("per-interval", "Milan v1.2 Table 5.6",
                       "a Stream Data AVTPDU has been received with an AVTP "
                       "timestamp field that was in the past"),
    "EARLY_TIMESTAMP": ("per-interval", "Milan v1.2 Table 5.6",
                        "a Stream Data AVTPDU has been received with an AVTP "
                        "timestamp field that was too far in the future to "
                        "process"),
    "FRAMES_RX": ("per-frame", "IEEE 1722.1-2021 Table 7.157",
                  "each Stream Data AVTPDU received on this Stream Input"),
}

#: The six Table 5.6 anomaly counters that are bounded by the observation interval.
MILAN_INTERVAL_COUNTERS = tuple(
    n for n, (law, _, _) in STREAM_INPUT_COUNTER_LAW.items()
    if law == "per-interval")


def counter_law(name: str) -> Optional[tuple]:
    """(law, clause, trigger) for a STREAM_INPUT counter, or None if unnamed."""
    return STREAM_INPUT_COUNTER_LAW.get(name)


def check_interval_ceiling(before: dict, after: dict, *,
                           window_s: Optional[float] = None) -> tuple:
    """Retain the anomaly-to-packet delta sanity check.

    FRAMES_RX counts AVTPDUs under ruling #726, not intervals. This loose
    cross-counter bound cannot determine an anomaly's observation interval.
    TV/TNV have their own packet-identity check in check_tv_tnv().
    """
    if before.get("FRAMES_RX") is None or after.get("FRAMES_RX") is None:
        return ("SKIP", {"why": "the mask does not claim FRAMES_RX, so the "
                                "packet total is unreadable"})
    d_frx = after["FRAMES_RX"] - before["FRAMES_RX"]
    if d_frx < 0:
        return ("SKIP", {"why": "FRAMES_RX went backwards: the block was "
                                "reset (Milan 5.3.8.10 not-bound -> bound) or "
                                "wrapped inside the window"})
    offenders, checked, deltas = [], [], {}
    for name in MILAN_INTERVAL_COUNTERS:
        if name == "FRAMES_RX" or before.get(name) is None \
                or after.get(name) is None:
            continue
        d = after[name] - before[name]
        if d < 0:
            continue                      # reset or wrap: says nothing
        checked.append(name)
        deltas[name] = d
        if d > d_frx:
            offenders.append({"counter": name, "delta": d,
                              "frames_rx_delta": d_frx,
                              "law": STREAM_INPUT_COUNTER_LAW[name][0],
                              "clause": STREAM_INPUT_COUNTER_LAW[name][1]})
    if not checked:
        return ("SKIP", {"why": "no other Table 5.6 interval counter is "
                                "claimed by the mask"})
    if d_frx == 0 and not any(deltas.values()):
        return ("SKIP", {"frames_rx_delta": 0,
                         "why": "no frame was received in the window, so the "
                                "packet total never advanced and the ceiling "
                                "is vacuous"})
    detail = {"frames_rx_delta": d_frx, "deltas": deltas,
              "window_s": window_s, "checked": checked}
    if offenders:
        detail["offenders"] = offenders
        detail["why"] = ("a Table 5.6 interval counter ticked more often than "
                         "FRAMES_RX; every one of its trigger conditions "
                         "arrives IN a received frame, so it cannot out-tick "
                         "the count of those frames")
        return ("FAIL", detail)
    return ("PASS", detail)


def _grade_per_frame(base, rate, nominal_frame_rate, stream_flowing):
    """A per-frame counter's rate: the 1722.1 Table 7-157 reading, or the
    wrong conversion to Milan's interval semantics that no clause licenses."""
    name, clause = base["counter"], base["clause"]
    if rate >= 0.5 * nominal_frame_rate:
        return ("PASS", dict(base, reading="per-frame"))
    if stream_flowing:
        return ("FAIL", dict(base, reading="interval",
                             why=f"{clause} defines {name} per frame, but "
                                 f"it moved at {rate:.4g}/s while the "
                                 f"stream was flowing at about "
                                 f"{nominal_frame_rate:g} frames/s - the "
                                 f"shape of a per-frame counter wrongly "
                                 f"converted to interval semantics; ruling "
                                 f"#726 retains the per-AVTPDU law"))
    return ("INFO", dict(base, reading="below-frame-rate",
                         why="the frame rate in the window is unknown, so "
                             "a below-nominal rate cannot be graded"))


def _grade_per_interval(base, rate, nominal_frame_rate, stream_flowing):
    """Classify a retained anomaly counter without inferring its interval."""
    name, clause, trigger = base["counter"], base["clause"], base["trigger"]
    window_s = base["window_s"]
    reading = frames_rate_reading(rate, nominal_frame_rate, window_s=window_s)
    base["implied_interval_s"] = reading["implied_interval_s"]
    if reading["band"] == "per-frame":
        return ("INFO", dict(base, reading="per-frame",
                             why=f"{name} moved at {rate:.4g}/s, the 1722.1 "
                                 f"per-frame reading; {clause} makes it an "
                                 f"observation-interval count, and only an "
                                 f"interval shorter than the frame period "
                                 f"makes the two agree"))
    return ("PASS", dict(base, reading="interval",
                         implied_interval_s=None,
                         why=f"{name} ticks only in intervals during which "
                             f"its condition ({trigger}) held; this rate "
                             f"does not reveal the observation interval"))


def grade_counter_semantics(name: str, delta: int, window_s: float, *,
                            nominal_frame_rate: float = 8000.0,
                            stream_flowing: Optional[bool] = None) -> tuple:
    """Grade ONE counter's observed movement against its clause update law.

    `window_s` is the MEASURED span the delta accumulated over, never the
    requested sleep.  The two differ by the bounded subprocess polls around the
    sleep - ~9 s real against a 4 s request on this bench - and dividing the
    real span's delta by the request inflates every rate by that ratio:
    ax-rv32-f's H1, which filed 74 conformant peer rows as "impossible"
    (7,982/s of physical class A traffic recorded as 18,048/s).

    Returns (verdict, detail) with detail["reading"] naming the law the
    measurement is consistent with, and detail["clause"] naming the clause the
    grade is made under - so a finding always arrives with its citation.

    FAIL is reserved for what the clauses genuinely exclude:
      * more ticks than frames could possibly have arrived;
      * a per-frame counter (FRAMES_RX, TIMESTAMP_VALID or TIMESTAMP_NOT_VALID)
        that moved at an interval-like rate while frames were flowing.
    Ruling #726 applies IEEE 1722.1-2021 Table 7.157 to FRAMES_RX.
    Everything else is classified, because Table 5.6 bounds the observation
    interval from ABOVE only and every interval in (0, 1 s] is conformant.
    """
    law = counter_law(name)
    if law is None:
        return ("SKIP", {"why": f"{name} is not a STREAM_INPUT counter"})
    kind, clause, trigger = law
    base = {"counter": name, "law": kind, "clause": clause, "trigger": trigger,
            "delta": delta, "window_s": window_s}
    if window_s is None or window_s <= 0:
        return ("SKIP", dict(base, why="no measurement window"))
    #! an UNREADABLE counter is not a zero one.  A delta of None means the
    #! descriptor did not answer, or the mask never claimed the counter, and
    #! grading that as "static" would turn an absent measurement into a clean
    #! result - the vacuity this file's tv/tnv guard already exists to refuse.
    if delta is None:
        return ("SKIP", dict(base, reading=None,
                             why="the counter was not readable over the "
                                 "window (unclaimed by the mask, or the "
                                 "descriptor did not answer)"))
    if delta < 0:
        return ("SKIP", dict(base, why="the counter went backwards: a bind "
                                       "reset (Milan 5.3.8.10) or a 32-bit "
                                       "wrap inside the window"))
    rate = delta / window_s
    base["rate_per_s"] = rate
    if nominal_frame_rate and rate > nominal_frame_rate * 1.05:
        return ("FAIL", dict(base, reading="impossible",
                             why=f"{rate:.4g} ticks/s exceeds the nominal "
                                 f"{nominal_frame_rate:g} frames/s: no reading "
                                 f"of any clause permits more ticks than "
                                 f"frames"))
    if delta == 0:
        return ("SKIP", dict(base, reading="static",
                             why=f"the counter did not move, and its trigger "
                                 f"({trigger}) may simply not have occurred"))
    if kind == "per-frame":
        return _grade_per_frame(base, rate, nominal_frame_rate, stream_flowing)
    if kind == "per-event":
        return ("PASS", dict(base, reading="per-event"))
    return _grade_per_interval(base, rate, nominal_frame_rate, stream_flowing)


def check_no_growth(before: dict, after: dict, keys: Sequence[str], *,
                    window_s: Optional[float] = None
                    ) -> tuple[str, dict[str, object]]:
    """The GROWTH verdict for the error counters, as a verdict and not as INFO.

    Milan v1.2 Table 5.6 defines LATE_TIMESTAMP, EARLY_TIMESTAMP,
    SEQ_NUM_MISMATCH and UNSUPPORTED_FORMAT as <= 1 s OBSERVATION-INTERVAL
    counts - "Incremented at the end of every observation interval during
    which ..." - so the question is "did it tick in ANY interval", never a rate.
    One tick is one bad interval and it is a FAIL; the magnitude is a detail.

    This exists because two real escapes passed a green run without it:
    296,294 of 296,294 frames discarded as UNSUPPORTED_FORMAT on 2026-07-27, and
    5.1 M LATE + 4.8 M EARLY timestamps hidden behind a register that had frozen.
    Both were emitted as INFO - never PASS, never FAIL - so at SHALL severity
    they contributed nothing to the exit code.

    A NEGATIVE delta is INFO, not PASS: either the block was reset mid-window
    (Milan 5.3.8.10 zeroes it on not-bound -> bound) or a 32-bit counter wrapped,
    and neither is evidence of health.
    """
    have = [k for k in keys if k in before and k in after]
    if not have:
        return ("SKIP", {"why": "counter not claimed by the mask on one or both "
                                "reads", "wanted": list(keys),
                         "before_has": sorted(k for k in keys if k in before),
                         "after_has": sorted(k for k in keys if k in after)})
    d = {k: after[k] - before[k] for k in have}
    detail = {"before": {k: before[k] for k in have},
              "after": {k: after[k] for k in have},
              "delta": d, "window_s": window_s,
              "note": "Milan Table 5.6 counts OBSERVATION INTERVALS (<= 1 s "
                      "each), so any non-zero delta is at least one bad "
                      "interval; this is a growth verdict and never a rate"}
    if any(v < 0 for v in d.values()):
        detail["why"] = ("a counter went DOWN: the block was reset mid-window "
                         "(Milan 5.3.8.10 not-bound -> bound) or a 32-bit "
                         "counter wrapped - either way the window measured "
                         "nothing")
        return ("INFO", detail)
    return ("PASS" if all(v == 0 for v in d.values()) else "FAIL", detail)


# ------------------------------------------------------- the streaming licence --
#: docs/reference/REGISTER_MAP.md 0x694 LWSRP_STATUS (RO).  This is the ONE
#: reading that decides whether a silent talker is a defect or a conformant
#: device, so it is a precondition of every frames-advance verdict and not a
#: nice-to-have.
LWSRP_STATUS_ADDR = 0x694
#: 0x85C A_STRMW_SRP - the same question PER STREAM INDEX (idx 0 is a live hard
#: alias of 0x694).  0xDEAD in the low half means the row is NOT BACKED in this
#: build, which is a shape defect and not a licence answer.
LWSRP_ROW_ADDR = 0x85C

#: LWSRP_STATUS[1:0] listener declaration.
LWSRP_DECL = {0: "none/ignore", 1: "asking-failed", 2: "ready",
              3: "ready-failed"}


def decode_lwsrp_status(word: int) -> dict:
    """LWSRP_STATUS (0x694) -> the named bits, per REGISTER_MAP.md.

    Milan v1.2 5.3.7.3 licenses a talker only "As long as a PAAD is declaring a
    Talker Advertise attribute AND receiving a Listener Ready or Listener Ready
    Failed attribute for a Stream Output".  Both halves of that conjunction are
    in this word: bit 4 is our Talker declaration, bits [1:0]/[3] are the
    Listener declaration that arrived over MSRP, and bit 8 is the fabric's own
    conclusion - the stream gate.  0x30 (talker declared + domain ok, gate SHUT)
    is the reading a bound-but-silent talker gives, and it is CONFORMANT.
    """
    w = int(word)
    decl = w & 0x3
    return {"raw": hex(w),
            "listener_declaration": LWSRP_DECL.get(decl, str(decl)),
            "listener_registered": bool(w & (1 << 2)),
            "listener_ready": bool(w & (1 << 3)),
            "talker_declared": bool(w & (1 << 4)),
            "domain_ok": bool(w & (1 << 5)),
            "reservation_active": bool(w & (1 << 6)),
            "tspec_over_75pct": bool(w & (1 << 7)),
            "stream_gate_open": bool(w & (1 << 8)),
            "slope_mux_engaged": bool(w & (1 << 9)),
            "talker_failed_seen": bool(w & (1 << 10)),
            "attribute_row_shortfall": bool(w & (1 << 11)),
            "msrp_failure_code": (w >> 16) & 0xFF,
            "ingress_fifo_drops": (w >> 24) & 0xFF}


def licence_state(word: Optional[int]) -> tuple:
    """(state, detail) for the streaming licence, where state is one of
    "OPEN", "SHUT" or "UNKNOWN".

    UNKNOWN is returned for a missing reading and is the case that matters most:
    the absence of the reading must never become a violation verdict.  0x694 sits
    on the DUT board, so a controller-host runner needs an explicit board-side
    path to it - and where there is none the frames-advance verdicts are SKIP
    with this state attached, never FAIL.
    """
    if word is None:
        return ("UNKNOWN", {
            "why": f"no LWSRP_STATUS ({LWSRP_STATUS_ADDR:#05x}) reading was "
                   f"supplied.  It is a DUT-board CSR, so a controller-host run "
                   f"needs --licence-status <word> from the documented pre-step "
                   f"(read 0x694 on the DUT) or --licence-cmd to fetch it.  "
                   f"Milan v1.2 5.3.7.3 makes the Listener Ready half of the "
                   f"licence a precondition, so without it a silent talker "
                   f"cannot be graded and every frames-advance verdict SKIPs",
            "register": f"{LWSRP_STATUS_ADDR:#05x} LWSRP_STATUS",
            "per_index_register": f"{LWSRP_ROW_ADDR:#05x} A_STRMW_SRP"})
    d = decode_lwsrp_status(word)
    if d["stream_gate_open"]:
        return ("OPEN", d)
    d["why"] = ("LWSRP_STATUS bit 8 (stream gate) is SHUT, so Milan v1.2 "
                "5.3.7.3's licence - a Talker Advertise AND a Listener Ready or "
                "Listener Ready Failed - is not complete.  A talker emitting "
                "nothing here is CORRECT, so the frames-advance assertions are "
                "SKIPped rather than failed")
    return ("SHUT", d)


# ------------------------------------------------- the participants and sides --
#: Packet-count sources under ruling #726. Interface totals include all traffic;
#: stream counters include only the selected stream and reset on start/bind.
#: Callers compare matching traffic and deltas within one counter era.
FRAME_ACCURATE_SOURCES = ("avb_interface", "rmon", "nic", "pcap",
                          "stream_input", "stream_output")
INTERVAL_SOURCES = ()  # FRAMES_TX/FRAMES_RX have no interval-count source.


class CounterSemanticError(ValueError):
    """Raised when a source has no declared packet-count contract."""


def assert_frame_accurate(source: str) -> str:
    """Accept declared packet counters, including both stream directions."""
    s = str(source)
    if s not in FRAME_ACCURATE_SOURCES:
        raise CounterSemanticError(
            f"unknown counter source {s!r}; frame-accurate sources are "
            f"{list(FRAME_ACCURATE_SOURCES)}")
    return s


#: Cross-side tolerances, each with the reason it is that size.  A cross-check
#: with an unjustified tolerance is a guess, so the reason travels with it.
XSIDE_TOLERANCE = {
    "snapshot_skew_frames": 8000,
    "snapshot_skew_reason":
        "the sides are not sampled atomically: two AECP round trips plus the "
        "DUT's STATS_CTRL (0x200) snapshot latch put up to ~1 s between the "
        "first and last read, and one second of class A is 8000 frames",
    "capture_edge_frames": 8000,
    "capture_edge_reason":
        "tcpdump starts and stops on its own schedule, so a capture can miss up "
        "to one second at each edge relative to a counter window",
    "packet_min_per_s": 150,
    "packet_min_reason":
        "a conservative flow discriminator for the supported AAF and CRF streams: "
        "150 AVTPDUs/s is below their nominal wire rates, but above a one-per-second "
        "regression. This is a rate-band check, not proof of exact packet equality; "
        "the pair comparison separately bounds snapshot skew",

}


def _perframe_deviant_sides(ticks: dict[str, int], floor: float | None) -> tuple:
    """Identify below-packet-rate sides over a measured flowing window."""
    sem = {role: ("static" if delta == 0 else "unmeasured" if floor is None
                  else "per-frame" if delta >= floor else "interval")
           for role, delta in ticks.items()}
    return sem, [role for role in ticks if sem[role] == "interval"]


def _perframe_findings(ticks: dict[str, int], deviant: list[str],
                       floor: float, window_s: float) -> list[dict]:
    """Attribute each interval-rate packet counter to its own measured side."""
    return [
        {"role": role, "ticks": ticks[role],
         "ticks_per_s": round(ticks[role] / window_s, 1),
         "perframe_bound_ticks": floor,
         "counter": {"talker": "FRAMES_TX (IEEE 1722.1-2021 Table 7.159)",
                     "listener": "FRAMES_RX (IEEE 1722.1-2021 Table 7.157)"}[role],
         "why": "this side advanced below the packet-rate band during the "
                "measured flowing window; ruling #726 requires one count per "
                "AVTPDU on both stream directions"}
        for role in deviant]


def _interval_ticks_verdict(d: dict, ticks: dict[str, int], deviant: list[str],
                            tol: int, self_loop: bool) -> tuple:
    """Grade packet deltas; retain the legacy helper name for existing callers."""
    talker_delta, listener_delta = ticks["talker"], ticks["listener"]
    if self_loop and talker_delta > 0 and listener_delta == 0 and not deviant:
        d["why"] = ("self-loop pair on a single-port DUT: the bridge never "
                    "returns a frame to its ingress port (802.1Q 8.6.1), so "
                    "the listener is structurally unreachable")
        d["self_loop"] = True
        return ("SKIP", d)
    if deviant:
        d["attributed"] = True
        if len(deviant) == 1:
            other = "listener" if deviant == ["talker"] else "talker"
            if d[other + "_semantics"] == "per-frame":
                d["conformant_role"] = other
        d["why"] = ("interval-rate packet counter on " + ", ".join(deviant)
                    + "; each finding names its own side under ruling #726")
        return ("FAIL", d)
    if (talker_delta > 0) != (listener_delta > 0):
        d["why"] = "one side counted packets and the other did not"
        return ("FAIL", d)
    if abs(talker_delta - listener_delta) > tol:
        d["why"] = "packet totals disagree beyond the measured-read skew allowance"
        return ("FAIL", d)
    if talker_delta > 0 and d["perframe_bound_ticks"] is None:
        d["why"] = "no measured duration; matching deltas do not establish packet-rate growth"
        return ("SKIP", d)
    return ("PASS", d)


def interval_ticks_agree(talker_delta: Optional[int],
                         listener_delta: Optional[int], *,
                         tolerance: int = None,
                         window_s: float = None,
                         self_loop: bool = False) -> tuple:
    """Compare per-AVTPDU deltas under the legacy public helper name.

    Both deltas must describe matching traffic in one streaming/binding era.
    The default packet allowance covers non-atomic reads and RX publication.
    A positive measured window enables the conservative packet-rate band;
    without it matching positive deltas are inconclusive. A negative
    delta indicates reset/wrap and cannot establish this comparison.
    """
    tol = XSIDE_TOLERANCE["snapshot_skew_frames"] if tolerance is None else tolerance
    if talker_delta is None or listener_delta is None:
        return ("SKIP", {"why": "one side's packet counter was unreadable",
                         "talker_frames": talker_delta, "listener_frames": listener_delta})
    if min(talker_delta, listener_delta) < 0 or (window_s is not None and window_s <= 0):
        return ("SKIP", {"why": "reset/wrap or a nonpositive measurement window"})
    floor = XSIDE_TOLERANCE["packet_min_per_s"] * window_s if window_s else None
    ticks = {"talker": talker_delta, "listener": listener_delta}
    sem, deviant = _perframe_deviant_sides(ticks, floor)
    d = {"talker_frames": talker_delta, "listener_frames": listener_delta,
         "tolerance_frames": tol,
         "tolerance_reason": XSIDE_TOLERANCE["snapshot_skew_reason"],
         "compares": "AVTPDU PACKETS (IEEE 1722.1-2021 Tables 7.159/7.157)",
         "talker_semantics": sem["talker"], "listener_semantics": sem["listener"],
         "perframe_bound_ticks": floor}
    if window_s:
        d["window_s"] = window_s
    if deviant:
        d["peer_findings"] = _perframe_findings(ticks, deviant, floor, window_s)
    return _interval_ticks_verdict(d, ticks, deviant, tol, self_loop)


def _concurrent_packet_findings(pair_ticks: dict, window_s: float | None) -> list[dict]:
    """Collect attributable low-rate sides across the shared measured window."""
    if window_s is None or window_s <= 0:
        return []
    floor = XSIDE_TOLERANCE["packet_min_per_s"] * window_s
    findings = []
    for label, pair in sorted(pair_ticks.items()):
        ticks = {role: pair[key] for role, key in (("talker", "tx_ticks"), ("listener", "rx_ticks"))
                 if pair.get(key) is not None}
        _, deviant = _perframe_deviant_sides(ticks, floor)
        findings.extend(dict(finding, pair=label)
                        for finding in _perframe_findings(ticks, deviant, floor, window_s))
    return findings


def check_concurrent_flowing(pair_ticks: dict[str, dict[str, int | None]], *,
                             licensed: bool | None = None, torn_down: str | None = None,
                             under_load: str | None = None,
                             window_s: float | None = None) -> tuple[str, dict[str, object]]:
    """Check concurrent packet growth in one shared streaming/binding window.

    The legacy tx_ticks/rx_ticks fields carry FRAMES_TX/FRAMES_RX packet deltas.
    An open licence requires every readable pair to move. A measured window
    additionally rejects interval-rate counts against their own side. Missing
    readings remain explicit; dead pairs outrank a measurement gap. Teardown
    and best-effort load retain their isolation and reserved-queue contracts.
    """
    ctx = (f" after tearing down {torn_down}" if torn_down else
           (f" while {under_load} best-effort load ran" if under_load else ""))
    if not pair_ticks:
        return ("SKIP", {"why": "no concurrently bound pairs were supplied, "
                                "so there is no concurrency to verify"})
    if licensed is None:
        return ("SKIP", {"why": "the streaming licence (LWSRP_STATUS "
                                f"{LWSRP_STATUS_ADDR:#05x} bit 8) is UNKNOWN, "
                                "so nothing is owed on any pair; supply "
                                "--licence-status <word> from the documented "
                                "pre-step",
                         "pairs": dict(sorted(pair_ticks.items()))})
    if licensed is False:
        return ("SKIP", {"why": "the stream gate is SHUT, so Milan v1.2 "
                                "5.3.7.3's licence is not complete and every "
                                "bound talker is CORRECTLY silent; concurrent "
                                "flow is not owed",
                         "pairs": dict(sorted(pair_ticks.items()))})
    flowing, dead, unreadable, one_sided = [], [], [], {}
    for label, t in sorted(pair_ticks.items()):
        tx, rx = t.get("tx_ticks"), t.get("rx_ticks")
        vals = [v for v in (tx, rx) if v is not None]
        if not vals:
            unreadable.append(label)
            continue
        if tx is None or rx is None:
            one_sided[label] = {"tx_ticks": tx, "rx_ticks": rx}
        if all(v > 0 for v in vals):
            flowing.append(label)
        else:
            dead.append(label)
    detail = {"pairs": dict(sorted(pair_ticks.items())), "flowing": flowing,
              "dead": dead, "unreadable": unreadable,
              "readable_on_one_side_only": one_sided,
              "compares": "AVTPDU PACKETS (IEEE 1722.1-2021 Tables 7.159/7.157)",
              "window_s": window_s}
    if dead:
        detail["why"] = (
            f"{len(dead)} of {len(pair_ticks)} concurrently bound pairs "
            f"{dead} went static{ctx} while the licence is OPEN and "
            f"{len(flowing)} neighbour(s) flowed.  Milan v1.2 5.3.7.3 "
            "licenses each Stream Output by its own conjunction, so every "
            "bound pair owes movement simultaneously"
            + (": a teardown that kills a neighbour stream is the "
               "cross-stream-independence defect this step exists to catch"
               if torn_down else
               (": 802.1Q-2018 8.6.8.2/34 credit-based shaping reserves the "
                "class A queue, so best-effort load SHALL NOT disturb "
                "reserved streams - this is the shaping/coexistence defect"
                if under_load else
                ": one stream starving under aggregate load is invisible to "
                 "a pairwise walk, which is why this area exists")))
        return ("FAIL", detail)
    findings = _concurrent_packet_findings(pair_ticks, window_s)
    if findings:
        detail["peer_findings"] = findings
        detail["why"] = "interval-rate stream counter(s) on the named pair and side"
        return ("FAIL", detail)
    if window_s is None or window_s <= 0:
        detail["why"] = "a positive measured shared window is required for packet-rate flow"
        return ("SKIP", detail)
    if unreadable:
        detail["why"] = (f"{unreadable} could not be read on either side, so "
                         f"'every pair flows{ctx}' cannot be certified; this "
                         f"is NOT a failure of the pairs that answered")
        return ("SKIP", detail)
    return ("PASS", detail)


def check_unbound_static(deltas: dict[str, dict[str, int | None]]
                         ) -> tuple[str, dict[str, object]]:
    """Per-index counter ISOLATION: the UNBOUND Stream Inputs stay static while
    their bound neighbours stream.

    `deltas` maps an unbound side label to {counter: delta-or-None} over the
    SAME shared window the bound pairs were measured in.  Milan v1.2 5.3.8.10
    keeps the Table 5.6 counters "For each Stream Input of the currently set
    Configuration" - PER Stream Input - so an unbound index that ticks while a
    neighbour streams is the per-index aliasing/bleed defect class: four such
    defects hid behind index-0-only testing on this fabric (GET_STREAM_INFO,
    MAX_TRANSIT_TIME, GET_COUNTERS, the talker state bits), which is exactly
    why this is asserted and not assumed.

    A negative delta is INFO, not PASS and not FAIL: the block was reset or a
    32-bit counter wrapped, so the window measured nothing on that index
    (same doctrine as check_no_growth()).
    """
    if not deltas:
        return ("SKIP", {"why": "no unbound stream inputs in this set - every "
                                "index is bound, so isolation has no subject "
                                "here (it is still asserted by the sets that "
                                "leave indices unbound)"})
    moved, wrapped, unreadable = {}, {}, []
    for label, ctrs in sorted(deltas.items()):
        vals = {k: v for k, v in (ctrs or {}).items() if v is not None}
        if not vals:
            unreadable.append(label)
            continue
        for k, v in vals.items():
            if v > 0:
                moved[f"{label}.{k}"] = v
            elif v < 0:
                wrapped[f"{label}.{k}"] = v
    detail = {"deltas": dict(sorted(deltas.items())), "moved": moved,
              "wrapped_or_reset": wrapped, "unreadable": unreadable}
    if moved:
        detail["why"] = ("an UNBOUND Stream Input's counters ticked while its "
                         "neighbours streamed: Milan v1.2 5.3.8.10 keeps the "
                         "counters PER Stream Input, so this is the per-index "
                         "aliasing/bleed defect class that index-0-only "
                         "testing can never see")
        return ("FAIL", detail)
    if unreadable and len(unreadable) == len(deltas):
        detail["why"] = ("no unbound stream input was readable, so isolation "
                         "was not measured; this is not evidence of health")
        return ("SKIP", detail)
    if wrapped:
        detail["why"] = ("an unbound counter went DOWN: the block was reset "
                         "or a 32-bit counter wrapped, so the window measured "
                         "nothing on it")
        return ("INFO", detail)
    return ("PASS", detail)


#: The test machine's own standard interface-counter loss lanes.
#: ONLY counters that can falsify this instrument's readings belong here:
#: rx_missed/over/fifo/errors mean a frame never reached rx_packets, and the
#: tx lanes mean this host's own injections failed.
NIC_LOSS_KEYS = ("tx_dropped", "rx_errors", "tx_errors",
                 "rx_missed_errors", "rx_over_errors", "rx_fifo_errors")
#: rx_dropped is NOT a loss lane for this instrument: it counts host demux
#: drops (typically no-protocol-handler, e.g. a switch's MVRP heartbeat on a
#: host with no MRP stack) that happen AFTER the frame was counted in
#: rx_packets and AFTER the AF_PACKET tap - measured on this bench at a steady
#: ~0.1/s of pure MVRP, which used to poison every window with
#: INSTRUMENT-SUSPECT.  Recorded in the detail, never in the verdict.
NIC_DEMUX_KEYS = ("rx_dropped",)
NIC_TRAFFIC_KEYS = ("rx_packets", "tx_packets", "rx_bytes", "tx_bytes")


def instrument_health(before: Optional[dict], after: Optional[dict]) -> tuple:
    """Was the TEST MACHINE itself lossless across the window?

    The rule this encodes, from repeated experience on this bench: a saturated
    capture host MANUFACTURES listener-side failures.  If rx_dropped /
    rx_errors / rx_missed_errors moved, every listener-side and capture-derived
    verdict in that window was taken THROUGH A LOSSY INSTRUMENT, so those
    verdicts are downgraded to INSTRUMENT-SUSPECT carrying the delta - never
    reported as a device failure.  Promiscuous mode drowning the softcore and an
    unscoped storm are both live histories of exactly this.
    """
    if not before or not after:
        return ("SKIP", {"why": "the test machine's NIC statistics were not "
                                "readable, so it is unknown whether the "
                                "instrument lost anything in this window; "
                                "expected the configured host-interface "
                                "statistics feed"})
    d = {k: after.get(k, 0) - before.get(k, 0) for k in NIC_LOSS_KEYS
         if k in before and k in after}
    moved = {k: v for k, v in d.items() if v}
    detail = {"loss_delta": d, "moved": moved,
              "demux_dropped": {k: after.get(k, 0) - before.get(k, 0)
                                for k in NIC_DEMUX_KEYS
                                if k in before and k in after},
              "traffic_delta": {k: after.get(k, 0) - before.get(k, 0)
                                for k in NIC_TRAFFIC_KEYS
                                if k in before and k in after}}
    if moved:
        detail["why"] = ("the test machine dropped or errored frames during the "
                         "window, so every listener-side and capture-derived "
                         "verdict in it was measured through a lossy "
                         "instrument; they are downgraded, not failed")
        return ("FAIL", detail)
    return ("PASS", detail)


#: The verdict a device-side check collapses to when the instrument was lossy.
#: NOT a failure of the device and NOT a pass: the measurement is inadmissible.
INSTRUMENT_SUSPECT = "INSTRUMENT-SUSPECT"


def downgrade_for_instrument(verdict: str, instrument: str) -> str:
    """PASS/FAIL -> INSTRUMENT-SUSPECT when the instrument itself lost frames."""
    if instrument == "FAIL" and verdict in ("PASS", "FAIL"):
        return INSTRUMENT_SUSPECT
    return verdict


def _triple(name, verdict, **detail):
    """One (assertion, verdict, detail) triple, before the shared side keys."""
    return (name, verdict, detail)


def _xside_corroborated(sides, talkers, listeners, wires, unreadable, tol):
    """(1) a one-sided claim of streaming is a defect in itself."""
    if unreadable:
        return _triple("xside.growth-corroborated", "SKIP",
                       why=f"{unreadable} could not be read, so corroboration is "
                           f"impossible; this is NOT a failure of the sides that answered")
    elif not talkers or not (listeners or wires):
        return _triple("xside.growth-corroborated", "SKIP",
                       why="fewer than two independent sides were supplied, so there is "
                           "nothing to corroborate against")
    else:
        moving = {l: s["frames"] > 0 for l, s in sides.items()
                  if s["role"] in ("talker", "listener", "wire")}
        agree = len(set(moving.values())) == 1
        return _triple("xside.growth-corroborated", "PASS" if agree else "FAIL",
                       moving=moving, tolerance_frames=tol,
                       tolerance_reason=XSIDE_TOLERANCE["snapshot_skew_reason"],
                       why=None if agree else
                       "the sides disagree about whether this stream is running.  Milan "
                       "v1.2 5.3.7.3 ties the talker's streaming to the listener's "
                       "declaration, so a talker that says it is streaming while the "
                       "listener and the wire see nothing is the defect - and so is the "
                       "reverse")


def _xside_unlicensed_silent(sides, licensed):
    """(2) an unlicensed stream must move on NO side."""
    if licensed is None:
        return _triple("xside.unlicensed-silent-everywhere", "SKIP",
                       why="the streaming licence (LWSRP_STATUS bit 8) is unknown, so "
                           "'must be silent everywhere' has no premise")
    elif licensed:
        return _triple("xside.unlicensed-silent-everywhere", "SKIP",
                       why="the stream IS licensed, so this invariant does not apply")
    elif not any(s.get("frames") is not None for s in sides.values()
                 if s["role"] in ("talker", "listener")):
        return _triple("xside.unlicensed-silent-everywhere", "SKIP",
                       why="no device side could be read, so frames on the wire cannot "
                           "be attributed to this stream's gate - the test host's own "
                           "capture carries its own traffic too")
    else:
        movers = {l: s["frames"] for l, s in sides.items()
                  if s["role"] in ("talker", "listener", "wire")
                  and (s.get("frames") or 0) > 0}
        # An interface-global wire counter ('nic' rx_packets) counts EVERY
        # frame on the test host's port - campaign control chatter included -
        # so it can corroborate silence but can never ATTRIBUTE movement to
        # this stream.  Only a device side or a stream-scoped capture ('pcap')
        # may convict.  Measured live 2026-08-02: 373 ambient frames/4 s
        # (~93 pps, two orders below any audio stream) fired a false FAIL
        # while the readable listener sat at 0.
        attributable = {l: n for l, n in movers.items()
                        if sides[l]["role"] in ("talker", "listener")
                        or sides[l].get("source") == "pcap"}
        if movers and not attributable:
            return _triple("xside.unlicensed-silent-everywhere", "INFO", movers=movers,
                           why="only the interface-global wire counter moved while every "
                               "readable device side was silent: ambient traffic on the "
                               "test host's port cannot be attributed to this stream's "
                               "gate, so this is not admissible evidence either way")
        else:
            return _triple("xside.unlicensed-silent-everywhere",
                           "PASS" if not attributable else "FAIL", movers=movers,
                           why=None if not attributable else
                           "frames moved with the stream gate SHUT: Milan v1.2 5.3.7.3 "
                           "licenses streaming only while a Listener Ready or Listener "
                           "Ready Failed is being received, so these frames are "
                           "unreserved")


def _xside_listener_not_more(talkers, listeners, unreadable, tol):
    """(3) a listener that counts more than was sent."""
    if talkers and listeners and not unreadable:
        t = max(s["frames"] for s in talkers.values())
        worst = max(listeners.items(), key=lambda kv: kv[1]["frames"])
        ok = worst[1]["frames"] <= t + tol
        return _triple("xside.listener-not-more-than-talker", "PASS" if ok else "FAIL",
                       talker_frames=t, listener=worst[0],
                       listener_frames=worst[1]["frames"], tolerance_frames=tol,
                       tolerance_reason=XSIDE_TOLERANCE["snapshot_skew_reason"],
                       why=None if ok else
                       "a listener counted more frames than the talker sent, beyond the "
                       "snapshot skew: either a second talker shares this stream_id (a "
                       "DMAC/stream_id collision) or one of the two counters is wrong")
    else:
        return _triple("xside.listener-not-more-than-talker", "SKIP",
                       why="needs a readable talker side and a readable listener side")


def _xside_absent_where_unregistered(sides, registered_sides):
    """(4) PRUNING: frames must be ABSENT where nothing registered."""
    if registered_sides is None:
        return _triple("xside.absent-where-not-registered", "SKIP",
                       why="no registration set supplied, so where traffic must be ABSENT "
                           "is unknown; pass the sides that declared a Listener attribute")
    else:
        reg = set(registered_sides)
        leaks = {l: s["frames"] for l, s in sides.items()
                 if l not in reg and s["role"] in ("listener", "bystander")
                 and (s.get("frames") or 0) > 0}
        return _triple("xside.absent-where-not-registered",
                       "PASS" if not leaks else "FAIL", registered=sorted(reg),
                       leaks=leaks,
                       why=None if not leaks else
                       "stream frames reached an interface that never registered as a "
                       "listener for them; this bench has measured untagged frames "
                       "flooding every port at 500 pps, so absence is asserted and never "
                       "assumed")


def cross_side_growth(sides: dict, *, licensed: Optional[bool] = None,
                      registered_sides: Iterable[str] | None = None
                      ) -> list[tuple[str, str, dict[str, object]]]:
    """The cross-participant invariants, as (assertion, verdict, detail) triples.

    `sides` maps a side label to
        {"role": "talker"|"listener"|"wire"|"bystander",
         "source": one of FRAME_ACCURATE_SOURCES,
         "frames": <frame-accurate delta over the window, or None>,
         "device": "<name>"}
    Every triple names EVERY side it used, so a morning review can see at a
    glance whether a green line was one-sided or corroborated.  A side that could
    not be read contributes a SKIP that NAMES it, never a FAIL of another side.

    `licensed` is the LWSRP_STATUS bit 8 answer (None = unknown).
    `registered_sides` is the set of side labels that DID register as a listener
    for this stream; any other side carrying frames is the pruning defect.
    """
    for _label, s in sides.items():
        assert_frame_accurate(s["source"])      # refuses an interval counter
    named = sorted(sides)
    unreadable = sorted(l for l, s in sides.items() if s.get("frames") is None)
    tol = XSIDE_TOLERANCE["snapshot_skew_frames"]
    talkers = {l: s for l, s in sides.items() if s["role"] == "talker"}
    listeners = {l: s for l, s in sides.items() if s["role"] == "listener"}
    wires = {l: s for l, s in sides.items() if s["role"] == "wire"}
    out = []
    for name, verdict, detail in (
            _xside_corroborated(sides, talkers, listeners, wires, unreadable,
                                tol),
            _xside_unlicensed_silent(sides, licensed),
            _xside_listener_not_more(talkers, listeners, unreadable, tol),
            _xside_absent_where_unregistered(sides, registered_sides)):
        detail.setdefault("sides_used", named)
        detail.setdefault("sides_unreadable", unreadable)
        detail.setdefault("sources", {l: sides[l]["source"] for l in named})
        detail.setdefault("devices", {l: sides[l].get("device") for l in named})
        detail.setdefault("frames", {l: sides[l].get("frames") for l in named})
        out.append((name, verdict, detail))
    return out


# ----------------------------------------------------------------- assertions --
@dataclass(frozen=True)
class AssertSpec:
    """One assertion a step owes, with the clause that requires it."""
    name: str
    clause: str
    #: PASS/FAIL against a clause, or recorded-only where the clause is silent
    severity: str = "SHALL"          # SHALL | RECOMMENDED | INFO
    detail: str = ""


A_ACMP_STATUS = AssertSpec(
    "acmp.status",
    "IEEE 1722.1-2021 8.2.2.5 / Milan v1.2 5.5.3: the response carries the "
    "status of the request, and SUCCESS is the only status a conformant bind of "
    "a compatible pair may return")
A_ADP_ALIVE = AssertSpec(
    "adp.alive",
    "IEEE 1722.1-2021 6.2.6: an available entity re-advertises within "
    "valid_time; the campaign asserts the entity is still discoverable AFTER "
    "every step, because a step that kills discovery is invisible to the step "
    "that follows it")
A_IFACE_MASK = AssertSpec(
    "counters.avb_interface.mask",
    "IEEE 1722.1-2021 Table 7-152/7-153 + Milan v1.2 5.4.2.25: the "
    "AVB_INTERFACE descriptor answers GET_COUNTERS with a mask that names "
    "every counter it serves")
A_IN_MASK = AssertSpec(
    "counters.stream_input.mandatory-mask",
    "Milan v1.2 5.3.8.10 + Table 5.6: every Stream Input keeps the ten "
    "counters; the mask must claim all ten (wire mask 0xF3F)")
A_OUT_MASK = AssertSpec(
    "counters.stream_output.mandatory-mask",
    "Milan v1.2 5.3.7.7 + Table 5.4: every Stream Output keeps the five "
    "counters (wire mask 0x01F in the Milan layout)")
A_LOCK_INVARIANT = AssertSpec(
    "counters.stream_input.lock-invariant",
    "Milan v1.2 Table 5.6: 'either MEDIA_LOCKED=MEDIA_UNLOCKED ... or "
    "MEDIA_LOCKED=MEDIA_UNLOCKED+1'")
A_TALKER_INVARIANT = AssertSpec(
    "counters.stream_output.start-stop-invariant",
    "Milan v1.2 Table 5.4: 'either STREAM_START=STREAM_STOP+1 ... or "
    "STREAM_START=STREAM_STOP'")
A_TV_TNV = AssertSpec(
    "counters.stream_input.tv-plus-tnv",
    "IEEE 1722.1-2021 Table 7.157 and ruling #726: TIMESTAMP_VALID plus "
    "TIMESTAMP_NOT_VALID equals the eventual FRAMES_RX packet total. "
    "Coalesced publication makes a lower FRAMES_RX snapshot inconclusive; "
    "the per-counter rate grader checks flowing-window growth. Empty or "
    "unclaimed samples cannot pass.")
A_RX_TICKING = AssertSpec(
    "counters.stream_input.frames-rx-advances",
    "Milan v1.2 5.3.7.3 + Table 5.6 FRAMES_RX: a bound listener fed by a "
    "streaming talker sees FRAMES_RX advance; a frozen FRAMES_RX beside a "
    "SUCCESS bind is the defect this campaign exists to catch")
A_TX_TICKING = AssertSpec(
    "counters.stream_output.frames-tx-advances",
    "Milan v1.2 5.3.7.3: 'As long as a PAAD is declaring a Talker Advertise "
    "attribute and receiving a Listener Ready or Listener Ready Failed "
    "attribute for a Stream Output, it shall be streaming AVTP packets' - so "
    "FRAMES_TX advances, and STREAMING_WAIT 'shall not be implemented' leaves "
    "no bound-and-silent excuse")
A_NO_LATE_EARLY = AssertSpec(
    "counters.stream_input.no-late-or-early-growth",
    "Milan v1.2 Table 5.6 LATE_TIMESTAMP / EARLY_TIMESTAMP: growth means "
    "presentation times outside the listener's processing window; on a healthy "
    "class A stream both stay put")
A_NO_SEQ_MISMATCH = AssertSpec(
    "counters.stream_input.no-seq-mismatch-growth",
    "Milan v1.2 Table 5.6 SEQ_NUM_MISMATCH + IEEE 1722-2016 4.4.4.6")
A_NO_UNSUPPORTED = AssertSpec(
    "counters.stream_input.no-unsupported-format-growth",
    "Milan v1.2 Table 5.6 UNSUPPORTED_FORMAT: a listener that passed the "
    "5.5.1.2 format check and then discards every frame is the 2026-07-27 "
    "escape (296,294 of 296,294 frames)")
A_TU_HANDLING = AssertSpec(
    "counters.stream_input.tu-consistent-with-wire",
    "Milan v1.2 Table 5.6 TIMESTAMP_UNCERTAIN + IEEE 1722-2016 4.4.4.7: the "
    "counter advances exactly when the tu bit is set on the wire; the product "
    "fabric owner derives it from live sync state, so this "
    "assertion compares the counter to the WIRE and never to a wish")
A_COUNTER_LAW = AssertSpec(
    "counters.stream_input.update-law-per-counter",
    "Ruling #726 (2026-10-12), IEEE 1722.1-2021 Table 7.157: FRAMES_RX, "
    "TIMESTAMP_VALID and TIMESTAMP_NOT_VALID count packets. Milan v1.2 "
    "Table 5.6 retains three event counters and six interval anomaly counters. "
    "Each measured delta is graded against its own law and cited clause.")
A_INTERVAL_CEILING = AssertSpec(
    "counters.stream_input.interval-ceiling",
    "Compare retained anomaly deltas with the FRAMES_RX packet delta. "
    "This sanity bound alone does not prove an observation interval.")
A_COUNTER_RESET_ON_BIND = AssertSpec(
    "counters.stream_input.reset-on-not-bound-to-bound",
    "Milan v1.2 5.3.8.10: 'The PAAD-AE shall reset all of these counters to "
    "zero each time the Stream Input changes its state from not bound to "
    "bound.'  Note the asymmetry the same clause states: it does NOT reset "
    "when going bound -> not bound.  And the trigger is the STATE TRANSITION, "
    "not the BIND_RX message: 5.5.3.5.43 handles a BIND_RX at an already-"
    "bound Stream Input by updating the binding parameters without ever "
    "transiting UNBOUND, so an implicit rebind owes no reset")
A_REBIND_NO_RESET = AssertSpec(
    "counters.stream_input.rebind-not-a-reset-boundary",
    "Milan v1.2 5.5.3.5.43 SETTLED_RSV_OK / RCV_BIND_RX_CMD: a BIND_RX at an "
    "already-bound Stream Input updates the binding parameters (same talker: "
    "step 2 exits immediately; different talker: steps 3-12 re-probe) and the "
    "input never transits UNBOUND - so the 5.3.8.10 reset trigger ('changes "
    "its state from not bound to bound') does not fire.  Whether the device "
    "reset its counters anyway is RECORDED here, never judged: the clause is "
    "silent on the rebind case in both directions",
    severity="INFO")
A_FORMAT_READBACK = AssertSpec(
    "aecp.stream-format-readback",
    "IEEE 1722.1-2021 7.4.9/7.4.10: a SET_STREAM_FORMAT that returns SUCCESS "
    "is readable back by GET_STREAM_FORMAT; Milan v1.2 5.5.1.2 then makes that "
    "value the one the bind is checked against")
A_WIRE_MATCHES_FORMAT = AssertSpec(
    "wire.matches-declared-format",
    "IEEE 1722-2016 I.2.4.1: the stream_format field 'matches the setting of "
    "the ... field in the Stream AVTPDU when this stream format is the current "
    "format for the stream'")
A_STREAM_ON_BIND_ALONE = AssertSpec(
    "stream.starts-on-bind-alone",
    "Milan v1.2 5.3.7.3: 'As long as a PAAD is declaring a Talker Advertise "
    "attribute and receiving a Listener Ready or Listener Ready Failed "
    "attribute for a Stream Output, it shall be streaming AVTP packets.  This "
    "specification excludes the possibility for a Stream Output to be stopped "
    "(STREAMING_WAIT state shall not be implemented).'  So a bind plus a "
    "Listener Ready is the WHOLE licence: a talker that needs an AECP "
    "START_STREAMING before it frames has implemented the state the clause "
    "forbids.  The runner therefore measures FIRST, sends START_STREAMING only "
    "if nothing moved, and RECORDS which of the two happened - a harness that "
    "always sends it cannot see the difference, which is how a workaround "
    "becomes an invisible permanent behaviour")
A_STREAM_CONTINUITY = AssertSpec(
    "stream.uninterrupted",
    "the Milan adverse-network-conditions recommended practice, §2: a device in "
    "a streaming state 'shall not experience any stream interruption when "
    "subjected to high rate Non-Priority traffic'",
    severity="RECOMMENDED")
A_CONTROL_RESPONSIVE = AssertSpec(
    "control.responsive",
    "the Milan adverse-network-conditions recommended practice, §2: 'As AVDECC "
    "traffic is Non-Priority, it is not expected that a Milan device remains "
    "responsive to AVDECC commands while subjected to high rate Non-Priority "
    "traffic' - so this is RECORDED, never failed, under storm",
    severity="INFO")
A_SRP_LICENCE = AssertSpec(
    "srp.streaming-licence",
    "Milan v1.2 5.3.7.3: the licence to stream is a CONJUNCTION - 'As long as a "
    "PAAD is declaring a Talker Advertise attribute AND receiving a Listener "
    "Ready or Listener Ready Failed attribute for a Stream Output, it shall be "
    "streaming AVTP packets.'  The second half arrives over MSRP from the "
    "listener, so it is not ours to assume: LWSRP_STATUS (0x694) bit 8 is the "
    "fabric's own answer, and 0x30 - talker declared, domain ok, GATE SHUT - is "
    "the reading a CORRECTLY silent talker gives.  Every frames-advance verdict "
    "is conditional on this one, and an unavailable reading is a SKIP")
A_STOP_TAKES_EFFECT = AssertSpec(
    "stream.stop-takes-effect",
    "Milan v1.2 5.3.7.3 + IEEE 1722.1-2021 7.4.36 STOP_STREAMING: after the "
    "unbind the Listener Ready is gone, so the licence is gone and the talker "
    "owes silence.  A talker still framing after an unbind is streaming without "
    "a reservation.  This assertion also PROTECTS THE NEXT PAIR: without a "
    "verified stop, the very first START_STREAMING latches the talker and every "
    "later pair measures an already-streaming talker, so "
    "stream.starts-on-bind-alone reports a false PASS for every pair after the "
    "first")
A_XSIDE_CORROBORATED = AssertSpec(
    "xside.growth-corroborated",
    "Milan v1.2 5.3.7.3 ties the talker's streaming to the listener's "
    "declaration, so 'this stream is running' must be true on EVERY measured "
    "side or on none: a one-sided claim of streaming is itself the defect.  The "
    "comparison uses only FRAME-ACCURATE sources - the IEEE 1722.1-2021 Table "
    "7-153 AVB_INTERFACE totals, the DUT RMON lanes, the test machine's NIC "
    "statistics or the pcap count, and stream-descriptor FRAMES_TX / FRAMES_RX "
    "packet deltas under Tables 7.159/7.157 and ruling #726. Compare matching "
    "traffic in one streaming/binding era")
A_XSIDE_UNLICENSED_SILENT = AssertSpec(
    "xside.unlicensed-silent-everywhere",
    "Milan v1.2 5.3.7.3: with no Listener Ready there is no licence, so an "
    "unlicensed stream must show growth on NO side; frames present anyway are "
    "unreserved and unshaped")
A_XSIDE_NOT_MORE = AssertSpec(
    "xside.listener-not-more-than-talker",
    "a listener that counts more frames than the talker sent, beyond the "
    "snapshot skew, means either a second talker shares the stream_id (the "
    "MAAP/DMAC collision class this bench has hit) or one of the two counters "
    "is wrong; IEEE 1722.1-2021 Table 7-153 frames are totals, so the "
    "comparison is well-defined")
A_XSIDE_PRUNED = AssertSpec(
    "xside.absent-where-not-registered",
    "802.1Q-2018 8.8.4: a bridge forwards a registered group address only to "
    "the ports that registered it, so stream frames must be ABSENT from an "
    "interface that never declared a Listener attribute.  This bench has "
    "measured untagged frames reaching every port at 500 pps, which is why "
    "absence is asserted and not assumed")
A_XSIDE_INTERVAL_AGREE = AssertSpec(
    "xside.interval-ticks-agree",
    "Legacy assertion id; ruling #726 applies IEEE 1722.1-2021 Tables "
    "7.159/7.157: FRAMES_TX and FRAMES_RX count AVTPDUs. Compare packet deltas "
    "from matching traffic in one counter era, allowing non-atomic read skew. "
    "Over a measured flowing window an interval-rate side FAILs by name")
A_XSIDE_PEER_SEMANTICS = AssertSpec(
    "xside.peer-counter-semantics",
    "Ruling #726 applies IEEE 1722.1-2021 Tables 7.159/7.157 to both stream "
    "directions. A per-AVTPDU pair is conformant. An interval-rate FRAMES_TX "
    "or FRAMES_RX on a measured flowing stream is a finding against that "
    "talker or listener, including when both sides regress")
A_XSIDE_ERRORS_STATIC = AssertSpec(
    "xside.errors-static-all-sides",
    "Milan v1.2 Table 5.6 (SEQ_NUM_MISMATCH, UNSUPPORTED_FORMAT, "
    "LATE_TIMESTAMP, EARLY_TIMESTAMP) + IEEE 1722.1-2021 Table 7-153 "
    "(RX_CRC_ERROR): on a healthy stream every participant's error and discard "
    "counters are static across the window, and the participant list includes "
    "the reference device and the test machine because a defect that only one "
    "side can see is still a defect")
A_INSTRUMENT_LOSSLESS = AssertSpec(
    "instrument.test-machine-lossless",
    "the test machine is an instrument before it is a witness: if its "
    "rx_errors / rx_missed / rx_over / rx_fifo or tx loss lanes moved during "
    "the window then every listener-side and capture-derived verdict in that "
    "window was taken through a lossy instrument, and those verdicts are "
    "downgraded to INSTRUMENT-SUSPECT rather than reported as device "
    "failures (rx_dropped is recorded but excluded: it counts post-tap "
    "host-demux drops such as unhandled MVRP, not capture loss).  A saturated "
    "test host manufacturing fake listener failures is a live history on this "
    "bench, not a hypothetical",
    severity="INFO")

#: The assertion set every bound-and-streaming step owes.  A step that carries
#: fewer is a step that can pass while something is wrong, and the offline
#: suite refuses it.
#:
#: NOTE what is DELIBERATELY NOT here: the two frames-advance assertions.  They
#: depend on the Milan 5.3.7.3 licence (LWSRP_STATUS bit 8), which the connect
#: step has no business reading, so they belong to the start-if-needed step that
#: owns the licence question - see LICENSED_STREAMING_ASSERTS.  Emitting them
#: from the bind step is what turned ~135-285 CONFORMANT bound-but-ungated steps
#: into SHALL failures.
BOUND_STREAMING_ASSERTS = (
    A_ACMP_STATUS, A_ADP_ALIVE, A_IFACE_MASK, A_IN_MASK, A_OUT_MASK,
    A_LOCK_INVARIANT, A_TALKER_INVARIANT, A_TV_TNV, A_INTERVAL_CEILING,
    A_NO_LATE_EARLY, A_NO_SEQ_MISMATCH, A_NO_UNSUPPORTED, A_TU_HANDLING,
    A_XSIDE_ERRORS_STATIC, A_INSTRUMENT_LOSSLESS)

#: The assertion set the LICENCE-OWNING step owes: the licence reading itself,
#: then everything that is only meaningful once the gate is known to be open,
#: including the cross-participant corroboration.
LICENSED_STREAMING_ASSERTS = (
    A_SRP_LICENCE, A_STREAM_ON_BIND_ALONE, A_TX_TICKING, A_RX_TICKING,
    A_COUNTER_LAW, A_INTERVAL_CEILING,
    A_XSIDE_CORROBORATED, A_XSIDE_UNLICENSED_SILENT, A_XSIDE_NOT_MORE,
    A_XSIDE_PRUNED, A_XSIDE_INTERVAL_AGREE, A_XSIDE_PEER_SEMANTICS, A_INSTRUMENT_LOSSLESS)

# ------------------------------------- the multi-stream concurrency asserts --
#: Real deployments run MANY streams at once, and the pairwise matrix - bind
#: one, verify, unbind, next - can never see what only happens under aggregate
#: load: CBS shaping with several class A streams in the shaped queue, the
#: multi-slot rings actually multiplexing, per-index counter isolation, and a
#: teardown disturbing its neighbours.  These three assertions are the ones
#: that only exist across concurrently bound pairs.
A_MULTI_ALL_FLOWING = AssertSpec(
    "multi.concurrent-all-flowing",
    "Milan v1.2 5.3.7.3 applied PER Stream Output: each concurrently bound "
    "pair holds its OWN licence (its Talker Advertise and its own Listener "
    "Ready), so with the gate open EVERY bound pair's packet counters "
    "(IEEE 1722.1-2021 Tables 7.159/7.157, ruling #726) advance at packet rate "
    "over one measured shared window.  One stream going static while its neighbours flow is the "
    "aggregate-load defect class - CBS credit starvation, ring-slot "
    "contention, a per-index datapath fault - and it is structurally "
    "invisible to a pairwise walk")
A_MULTI_ISOLATION = AssertSpec(
    "multi.unbound-counters-static",
    "Milan v1.2 5.3.8.10: 'For each Stream Input of the currently set "
    "Configuration, the PAAD-AE shall keep track of the counters in Table "
    "5.6' - PER Stream Input.  So while bound indices stream, the UNBOUND "
    "indices' counters stay static; an unbound index ticking is the per-index "
    "aliasing/bleed defect class, and four such defects hid behind "
    "index-0-only testing on this fabric")
A_MULTI_SURVIVORS = AssertSpec(
    "multi.neighbour-streams-survive-teardown",
    "Milan v1.2 5.3.7.3: the streaming licence is per Stream Output - a "
    "Talker Advertise AND that stream's own Listener Ready.  An UNBIND "
    "removes only the torn-down stream's Listener Ready, so every other "
    "bound pair keeps its licence and shall keep streaming, undisturbed "
    "(IEEE 1722.1-2021 8.2.2.6.2.1 makes the same independence argument for "
    "multiple listeners on one talker).  A teardown that kills a neighbour "
    "stream is the cross-stream-independence defect this step exists to "
    "catch")

A_STRESS_IMMUNE = AssertSpec(
    "multi.streams-immune-to-best-effort-load",
    "802.1Q-2018 8.6.8.2 (the credit-based shaper algorithm) + clause 34 "
    "(FQTSS): an admitted SR class A stream travels in a reserved, "
    "credit-shaped queue ABOVE best-effort traffic, so best-effort load "
    "SHALL NOT disturb it - coexistence inside the unreserved remainder is "
    "the design point of the reservation itself.  Measured in Milan Table "
    "5.4/5.6 interval terms over one shared window WHILE the load runs.  "
    "Distinct from the torture storm entries on purpose: those are line-rate "
    "adverse traffic and stay RECOMMENDED per the adverse-conditions "
    "recommended practice; a cooperative BE load is what the shaper exists "
    "to absorb, so this one is SHALL")
A_STRESS_HEADROOM = AssertSpec(
    "multi.best-effort-headroom",
    "info: no clause grades this - 802.1Q reserves the streams, not the "
    "leftover - so the achieved best-effort throughput is recorded as the "
    "measured BE headroom left by the reservations, a datum for capacity "
    "planning and never a verdict.  The record names the load mode "
    "(iperf3-tcp, or the udp-blast fallback whose number is a SEND rate, "
    "not goodput) so the datum cannot be over-read",
    severity="INFO")

#: What each phase of a concurrency set owes.  The bind phase is deliberately
#: lean - concurrency is the subject, format negotiation is the matrix's - and
#: the verify phase reuses the pairwise per-index machinery (interval ticks,
#: invariants, growth) so the tolerance doctrine stays in one place.
MULTI_BIND_ASSERTS = (A_ACMP_STATUS, A_FORMAT_READBACK, A_ADP_ALIVE)
MULTI_VERIFY_ASSERTS = (
    A_SRP_LICENCE, A_TX_TICKING, A_RX_TICKING, A_MULTI_ALL_FLOWING,
    A_MULTI_ISOLATION, A_LOCK_INVARIANT, A_TALKER_INVARIANT,
    A_COUNTER_LAW, A_INTERVAL_CEILING,
    A_NO_LATE_EARLY, A_NO_SEQ_MISMATCH, A_NO_UNSUPPORTED,
    A_XSIDE_INTERVAL_AGREE, A_INSTRUMENT_LOSSLESS)
#: The stress load step: streams immune (SHALL), the listener error counters
#: static across the loaded window (Table 5.6 coexistence), the BE throughput
#: recorded as INFO, the instrument as ever.
MULTI_STRESS_LOAD_ASSERTS = (
    A_SRP_LICENCE, A_STRESS_IMMUNE, A_NO_SEQ_MISMATCH, A_NO_LATE_EARLY,
    A_STRESS_HEADROOM, A_INSTRUMENT_LOSSLESS)
MULTI_TEARDOWN_ONE_ASSERTS = (
    A_ACMP_STATUS, A_STOP_TAKES_EFFECT, A_SRP_LICENCE, A_MULTI_SURVIVORS,
    A_INSTRUMENT_LOSSLESS)
MULTI_TEARDOWN_REST_ASSERTS = (A_ACMP_STATUS, A_STOP_TAKES_EFFECT,
                               A_ADP_ALIVE)


# ---------------------------------------------------------------- topology ----
@dataclass
class Device:
    """A device the campaign can address.  `crf_out`/`crf_in` are the
    descriptor INDICES of the CRF Media Clock streams, which on this fabric sit
    immediately after the AAF ones (Milan v1.2 7.2.2/7.2.3 make them mandatory
    on an AAF Media Listener with two or more AAF Media Inputs, so they are part
    of the matrix and not an extra)."""
    name: str
    entity_id: str
    mac: str
    talkers: int
    listeners: int
    crf_out: Optional[int] = None
    crf_in: Optional[int] = None
    formats: tuple = ()
    #: a device we do not control the firmware of; its refusals are evidence
    reference: bool = False
    #: "dut" | "reference" | "test-machine".  EVERY participant in a stream is a
    #: measured party, so the reference device gets verdicts of its own and the
    #: test machine is both a witness and a health gate.  A verdict derived from
    #: one side's counters is a claim; one corroborated across sides is a fact.
    role: str = "dut"
    #: the test machine is addressed by INTERFACE, not by entity_id: its numbers
    #: come from the configured host-interface statistics feed and capture.
    iface: Optional[str] = None
    #: a board-side path to this device's fabric CSRs exists (0x694 licence,
    #: 0x21C/0x230 RMON good-frame lanes behind the 0x200 snapshot latch,
    #: 0x85C per-stream SRP row).  False means those readings are REQUIRED
    #: INPUTS and their assertions SKIP naming the register.
    csr_path: bool = False
    #: EXPLICIT descriptor indices, when the served set is not a dense
    #: 0..N-1 range.  A count cannot express a gap, and a gap is the normal
    #: case for a REDUNDANT Milan device: Milan v1.2 seamless redundancy
    #: declares each stream twice, a (p) primary on the primary network and an
    #: (s) secondary on the secondary one, and a bench with only one network
    #: can never carry the secondaries.  The peer on this bench serves ten
    #: STREAM_INPUTs that are five interleaved pairs - primaries at the EVEN
    #: indices (USER 2026-07-31).
    #:
    #: This has to be stated rather than probed.  ACMP answers SUCCESS on a
    #: secondary descriptor whether or not the secondary network exists (all
    #: of the peer's 0..7 answered SUCCESS on 2026-07-31), and it does not
    #: serve GET_NAME (status 7 NOT_SUPPORTED), so neither the bind status nor
    #: the descriptor names can separate them at runtime.  Binding a secondary
    #: therefore looks exactly like a working bind that never carries audio -
    #: a DUT defect that is not one, which is the most expensive kind of
    #: fake red this campaign can produce.
    talker_index_set: Optional[tuple] = None
    listener_index_set: Optional[tuple] = None

    def talker_indices(self, include_crf: bool = True) -> list[int]:
        """The STREAM_OUTPUT indices this device really serves, CRF last.

        `talker_index_set` overrides the `talkers` count because a count
        cannot express a gap, and `include_crf=False` means AAF-only: a
        selector that leaves the Media Clock Output in picks the one talker
        whose format no audio sink will ever accept.
        """
        if self.talker_index_set is not None:
            idx = list(self.talker_index_set)
            if include_crf and self.crf_out is not None \
                    and self.crf_out not in idx:
                idx.append(self.crf_out)
            return idx
        idx = list(range(self.talkers))
        if include_crf and self.crf_out is not None:
            idx.append(self.crf_out)
        return idx

    def listener_indices(self, include_crf: bool = True) -> list[int]:
        """The STREAM_INPUT indices this device really serves, CRF last.

        The gap is the normal case here: the reference peer declares five
        interleaved redundancy pairs and this bench has one network, so only
        the even primaries can ever carry a stream.  `include_crf=False`
        additionally drops the Media Clock Input, which answers ACMP and then
        refuses every AAF format.
        """
        if self.listener_index_set is not None:
            idx = list(self.listener_index_set)
            if include_crf and self.crf_in is not None \
                    and self.crf_in not in idx:
                idx.append(self.crf_in)
            return idx
        idx = list(range(self.listeners))
        if include_crf and self.crf_in is not None:
            idx.append(self.crf_in)
        return idx

    def stream_id(self, talker_index: int) -> str:
        """Milan v1.2 5.3.7.5 / IEEE 1722-2016 4.4.4.4: the plug-and-play
        StreamID is {the sourcing interface's MAC, a 2-octet unique_id}, and on
        this fabric unique_id IS the talker index (the CRF Media Clock Output
        sits at unique_id = N_STREAMS).  Passing the WHOLE set to the wire
        analyser is what lets a capture answer "which of my Stream Outputs never
        declared a Talker Advertise" - the question that found a real defect."""
        return f"{self.mac}{talker_index:04x}"

    def stream_ids(self, include_crf: bool = True) -> list[str]:
        """Every StreamID this device sources, as the wire analyser wants them.

        Passing the WHOLE set rather than one id is what lets a capture answer
        "which of my Stream Outputs never declared a Talker Advertise" - the
        question a per-stream lookup cannot even be asked.
        """
        return [self.stream_id(i) for i in self.talker_indices(include_crf)]

    def is_crf_talker(self, i: int) -> bool:
        """True when Stream Output `i` is the CRF media clock, not an AAF talker."""
        return self.crf_out is not None and i == self.crf_out

    def is_crf_listener(self, i: int) -> bool:
        """True when Stream Input `i` is the CRF media clock sink, not an AAF one."""
        return self.crf_in is not None and i == self.crf_in


#: The bench shape.  The Arty is the DUT; the peer is the Milan-validated
#: reference device, so IT is the independent oracle (methodology L4/L5) and its
#: refusals are evidence about us, not bugs in it.
ARTY = Device(name="arty", entity_id="020000fffe000002", mac="020000000002",
              talkers=4, listeners=4, crf_out=4, crf_in=4,
              formats=("0205022001006000", "0205022000806000"),
              role="dut")
#: The peer device is REDUNDANT (Milan v1.2 seamless redundancy): its ten
#: STREAM_INPUTs are five interleaved pairs, a (p) primary at each even index
#: and its (s) secondary at the odd one.  This bench has ONE network, so the
#: secondaries can never carry a stream - and they still answer ACMP with
#: SUCCESS, so binding them yields a connection that never passes audio and
#: reads as a DUT defect.  USER 2026-07-31.  Override with
#: --peer 'listener_index_set=...' on a bench that has both networks.
#: ...and index 8 is its CRF MEDIA CLOCK INPUT, not a fifth AAF sink.  MEASURED,
#: not deduced: every peerl8 bind of ax-rv32-e came back with the listener's
#: own format 041060010000bb80 - AVTP subtype 0x04 = CRF, base 0xbb80 = 48 kHz -
#: and the message "Talker STREAM_OUTPUT and Listener STREAM_INPUT formats are
#: incompatible", which is the reference device being CORRECT.  Listing it among
#: the AAF primaries made every "highest AAF index" selector pick the one sink
#: that can never carry AAF: ax-phys-a's two proof pairs both aimed at l8, and
#: 32 of its 45 SKIPs are the post-bind contract of a bind that was never
#: bindable.  So the AAF primaries and the CRF primary are now separate fields -
#: include_crf=False really means AAF-only, and the matrix still walks the CRF.
#: THE TALKER SIDE IS THE SAME SHAPE, and it is NOT four AAF sources.  Read off
#: the device 2026-08-02 (hive_compliance C12/C4 against its own descriptors):
#: STREAM_OUTPUT 0 and 1 both answer 0205022001006000 (4ch AAF) and 2 and 3 both
#: answer 041060010000BB80 (AVTP subtype 0x04 = CRF, base 0xbb80 = 48 kHz).  So
#: the four outputs are ONE AAF pair and ONE CRF pair on the same (p)/(s)
#: interleave as the sinks: AAF primary 0, AAF secondary 1, CRF primary 2, CRF
#: secondary 3.  USER 2026-08-02: "do not stream on the (s) of the [peer], they
#: are the redundant part that is not connected" - one physical network, so only
#: the even (p) descriptors are bindable.  Treating 2 and 3 as AAF sources is
#: what produced ax-rv32-e's "ACMP nulls from t2 up" and the garbage the
#: controller's format pre-flight read back: they were never AAF to begin with.
PEER = Device(name="peer", entity_id="3cc0c60102030000", mac="3cc0c6010203",
              talkers=4, listeners=10, formats=("0205022001006000",),
              talker_index_set=(0,), crf_out=2,
              listener_index_set=(0, 2, 4, 6), crf_in=8,
              reference=True, role="reference")
#: The TEST MACHINE.  It carries the controller, and on this bench it also
#: carries the capture, so it is the third measured party in every pair: its NIC
#: statistics say whether a listener-side verdict was taken through a lossy
#: instrument.  The interface name is configuration (--test-machine / --iface),
#: never a source edit.
TESTHOST = Device(name="testhost", entity_id="", mac="", talkers=0, listeners=0,
                  role="test-machine", iface=None)

#: Which Device fields a --dut / --peer / --test-machine spec may set.  Keeping
#: this a table is what makes the topology configuration instead of a source
#: edit: hardcoded entity ids and MACs are how a campaign becomes single-bench.
DEVICE_SPEC_FIELDS = {
    "name": str, "entity": str, "entity_id": str, "mac": str, "iface": str,
    "talkers": int, "listeners": int, "crf_out": int, "crf_in": int,
    "formats": "csv", "role": str, "reference": bool, "csr_path": bool,
    #: e.g. --peer 'listener_index_set=0|2|4|6|8' for a redundant device whose
    #: (s) secondaries cannot be reached on a single-network bench
    "talker_index_set": "idxset", "listener_index_set": "idxset",
}


def parse_device_spec(spec: str, base: Device) -> Device:
    """`--dut name=arty,entity=...,mac=...,talkers=8,listeners=8,crf_out=8`.

    Unset fields keep `base`'s value, so a one-field override stays one field.
    An unknown key is refused rather than ignored: a silently dropped
    `--peer listners=10` typo would run the whole campaign against the wrong
    shape and report full coverage of it.
    """
    import dataclasses
    out = {}
    for part in [p for p in spec.split(",") if p.strip()]:
        if "=" not in part:
            raise ValueError(f"device spec field {part!r} is not key=value")
        k, v = part.split("=", 1)
        k, v = k.strip(), v.strip()
        if k not in DEVICE_SPEC_FIELDS:
            raise ValueError(f"unknown device spec field {k!r}; known: "
                             f"{sorted(DEVICE_SPEC_FIELDS)}")
        kind = DEVICE_SPEC_FIELDS[k]
        if k == "entity":
            k = "entity_id"
        if kind is int:
            out[k] = int(v, 0)
        elif kind is bool:
            out[k] = v.lower() in ("1", "true", "yes", "on")
        elif kind == "csv":
            out[k] = tuple(x for x in v.split("|") if x)
        elif kind == "idxset":
            #: refuse an EMPTY set rather than silently running no pairs - a
            #: campaign that walks nothing exits clean and reads as coverage
            ix = tuple(int(x, 0) for x in v.split("|") if x != "")
            if not ix:
                raise ValueError(f"{k}: an empty index set would run no "
                                 f"pairs at all; omit the key instead")
            out[k] = ix
        else:
            out[k] = v
    return dataclasses.replace(base, **out)


def participants(dut: Device, peer: Device,
                 host: Optional[Device] = None) -> list:
    """Every measured party, in a stable order.  The test machine is included
    whenever it has an interface to read, because "the counters from the test
    machine" is a first-class requirement and not an aside."""
    out = [dut, peer]
    if host is not None and host.iface:
        out.append(host)
    return out


# --------------------------------------------------------------------- steps --
@dataclass(frozen=True)
class Endpoint:
    """One end of a stream: a device and the descriptor index on it.

    A talker index means nothing without the device that carries it, and the
    two are passed together everywhere - which is what turned every plan
    builder into a four-argument (tk, ti, ls, li) call a reader had to count
    out.  As one value the order is a type, not a convention.
    """
    device: Device
    index: int


@dataclass
class Step:
    """One plan step.  `op` names what a runner does; `asserts` is what it owes.

    A step is data, deliberately: the runner supplies the wire, the plan
    supplies the questions, and the offline suite audits the questions.
    """
    sid: str
    area: str
    op: str
    args: dict = field(default_factory=dict)
    asserts: tuple = ()
    #: a human has to move a cable / cut power for this step
    needs_human: bool = False
    human_action: str = ""
    clause: str = ""
    note: str = ""

    def as_dict(self) -> dict:
        """The JSON-serialisable form a runner consumes, clauses included.

        `asdict()` alone would emit the AssertSpec objects; a runner needs the
        assertion NAMES plus the clause and severity behind each, so a verdict
        line can cite the requirement without importing this module.
        """
        d = asdict(self)
        d["asserts"] = [a.name for a in self.asserts]
        d["assert_clauses"] = {a.name: a.clause for a in self.asserts}
        d["assert_severity"] = {a.name: a.severity for a in self.asserts}
        return d


def _pair_steps(prefix, area, talker: Endpoint, listener: Endpoint,
                fmt: Optional[str]) -> list:
    """One talker index into one listener index: set the format, bind, verify,
    unbind.  The CRF pair carries its own format expectation."""
    tk, ti, ls, li = talker.device, talker.index, listener.device, listener.index
    sid = f"{prefix}.{tk.name}t{ti}-{ls.name}l{li}"
    steps = []
    crf = tk.is_crf_talker(ti) or ls.is_crf_listener(li)
    if fmt and not crf:
        steps.append(Step(
            sid + ".set-format", area, "set_format",
            #: the talker identity rides along so the RUNNER can read the
            #: talker's LIVE STREAM_OUTPUT format at execution time and write
            #: THAT to the listener; `format` is only the fallback when the
            #: live read fails.  The device-table tuple is a mirrored
            #: constant, and mirrored constants rot: the ax-rv32-c/-d
            #: out-matrix was refused end to end because the --dut spec
            #: inherited the Arty's 4ch formats[0] while the flashed 8x8
            #: talker (gateware 0x0021 derives its format from the elaborated
            #: wire width) answers 0205022002006000.
            {"target": ls.entity_id, "target_mac": ls.mac,
             "descriptor": "stream_input", "index": li, "format": fmt,
             "talker": tk.entity_id, "talker_mac": tk.mac,
             "talker_index": ti},
            asserts=(A_FORMAT_READBACK,),
            clause="Milan v1.2 5.5.1.2 - a Controller SHALL make the "
                   "Listener's format match the Talker's before binding; "
                   "refusing the bind instead is the behaviour the USER "
                   "directive forbids",
            note="listener adapts to the talker's LIVE format; a talker SET "
                 "may conformantly answer NOT_SUPPORTED because its wire "
                 "width is an elaboration fact"))
    steps.append(Step(
        sid + ".connect", area, "connect",
        {"talker": tk.entity_id, "talker_index": ti, "talker_mac": tk.mac,
         "listener": ls.entity_id, "listener_index": li,
         "listener_mac": ls.mac},
        asserts=BOUND_STREAMING_ASSERTS + (A_COUNTER_RESET_ON_BIND,
                                           A_WIRE_MATCHES_FORMAT),
        clause="Milan v1.2 5.5.3.5 BIND_RX + 5.3.8.10 counter reset on "
               "not-bound -> bound",
        note="CRF media-clock pair" if crf else ""))
    steps.append(_start_if_needed_step(sid, area, talker, listener))
    steps.append(Step(
        sid + ".disconnect", area, "disconnect",
        {"talker": tk.entity_id, "talker_index": ti, "talker_mac": tk.mac,
         "listener": ls.entity_id, "listener_index": li,
         "stop_streaming": True, "stop_window_s": 4.0},
        asserts=(A_ACMP_STATUS, A_ADP_ALIVE, A_TALKER_INVARIANT,
                 A_STOP_TAKES_EFFECT),
        clause="Milan v1.2 5.5.3.5 UNBIND_RX; 5.3.8.10 notes the counters are "
               "NOT reset on bound -> not bound, so a zeroed block here is "
               "itself a finding",
        note="the unbind removes the Listener Ready, so Milan v1.2 5.3.7.3's "
             "licence is gone and the talker owes silence - and the STOP is "
             "VERIFIED because an unverified one leaves the talker latched and "
             "makes stream.starts-on-bind-alone a false PASS for every "
             "subsequent pair"))
    return steps


def _start_if_needed_step(sid: str, area: str, talker: Endpoint,
                          listener: Endpoint) -> "Step":
    """The step that OWNS the Milan 5.3.7.3 licence question.

    It is a separate step from the bind on purpose.  The bind can only ask
    "did the ACMP exchange succeed"; whether a silent talker is a defect needs
    the SRP licence, which is a different reading from a different place, and
    mixing the two is what made a conformant bound-but-ungated talker read as a
    SHALL failure.  It also carries the LISTENER, because the frames-advance
    verdict is cross-participant: the talker's claim is corroborated on the
    listener and on the test machine or it is not a fact.
    """
    tk, ti, ls, li = talker.device, talker.index, listener.device, listener.index
    return Step(
        sid + ".start-if-needed", area, "start_stream_if_needed",
        {"talker": tk.entity_id, "talker_mac": tk.mac, "talker_index": ti,
         "listener": ls.entity_id, "listener_mac": ls.mac,
         "listener_index": li, "measure_first_s": 4.0},
        asserts=LICENSED_STREAMING_ASSERTS,
        clause="Milan v1.2 5.3.7.3 - the licence is the Talker Advertise plus "
               "the Listener Ready, and STREAMING_WAIT shall not be "
               "implemented",
        note="measure BEFORE sending START_STREAMING, then send it only if "
             "nothing moved, and record which happened; the SRP licence "
             "readback (LWSRP_STATUS bit 8) is a REQUIRED INPUT, so an "
             "unavailable reading and a shut gate are both SKIP and never a "
             "violation")


def plan_matrix(dut: Device = ARTY, peer: Device = PEER,
                both_directions: bool = True) -> list:
    """Every talker x listener pair, EVERY index, both directions, CRF included.

    The pair set is deliberately the full cross product rather than a rotation:
    a rotation covers the matrix only over many cycles, and a morning diff of
    one cycle then cannot tell a new defect from an unvisited cell.
    """
    steps = []
    fmt = dut.formats[0] if dut.formats else None
    for ti in dut.talker_indices():
        for li in peer.listener_indices():
            steps += _pair_steps("out", "matrix", Endpoint(dut, ti),
                                 Endpoint(peer, li), fmt)
    if both_directions:
        for ti in peer.talker_indices():
            for li in dut.listener_indices():
                steps += _pair_steps("ret", "matrix", Endpoint(peer, ti),
                                     Endpoint(dut, li), fmt)
    # ---- intra-DUT loopback: the DUT's own talkers into its own listeners.
    # This is the only pair set that needs no peer at all, so it is what keeps
    # the campaign meaningful while the reference device is out of the rack.
    for ti in dut.talker_indices():
        for li in dut.listener_indices():
            steps += _pair_steps("loop", "matrix", Endpoint(dut, ti),
                                 Endpoint(dut, li), fmt)
    return steps


def _multi_pair(talker: Endpoint, listener: Endpoint,
                fmt: Optional[str]) -> dict:
    tk, ti, ls, li = talker.device, talker.index, listener.device, listener.index
    p = {"talker": tk.entity_id, "talker_index": ti, "talker_mac": tk.mac,
         "listener": ls.entity_id, "listener_index": li,
         "listener_mac": ls.mac, "label": f"{tk.name}t{ti}-{ls.name}l{li}"}
    if fmt:
        p["format"] = fmt
    return p


def _multi_pairs_primaries(dut: Device, peer: Device, fmt) -> list:
    """EVERY reachable reference listener fed CONCURRENTLY.

    The listener set comes from the peer's spec exactly as the matrix's does -
    listener_indices(), which on a redundant device names the (p) primaries
    only (the peer's AAF sinks are 0/2/4/6 and its CRF Media Clock Input is
    8; the (s) secondaries can never carry a stream on a one-network bench) -
    so nothing here is hardcoded to any device.  Talkers are the DUT's AAF set, assigned cyclically so every peer
    listener is fed even when the DUT has fewer talkers than the peer has
    listeners; a talker reused that way carries two listeners on ONE stream,
    which IEEE 1722.1-2021 8.2.2.6.2.1 permits.  On the AX 8x8 against the
    reference device this is a plain 1:1 zip: t0..t3 -> l0/2/4/6.
    """
    tks = dut.talker_indices(include_crf=False)
    lss = peer.listener_indices(include_crf=False)
    if not tks or not lss:
        return []
    return [_multi_pair(Endpoint(dut, tks[i % len(tks)]), Endpoint(peer, li), fmt)
            for i, li in enumerate(lss)]


def _multi_pairs_selfloop(dut: Device, fmt) -> list:
    """The DUT's own talkers into its own listeners, tN -> lN, concurrently.

    This is the set that stresses the DUT on BOTH sides at once - every
    packetizer and every depacketizer live in the same fabric - and, like the
    matrix's loop prefix, it needs no peer at all.
    """
    tks = dut.talker_indices(include_crf=False)
    lss = dut.listener_indices(include_crf=False)
    return [_multi_pair(Endpoint(dut, t), Endpoint(dut, li), fmt)
            for t, li in zip(tks, lss)]


def _multi_pairs_mixed(dut: Device, peer: Device, fmt) -> list:
    """Outbound and self-loop pairs INTERLEAVED in one concurrent set, when
    the shapes allow (two or more DUT talkers, and a listener on each side).
    A defect that only appears when the egress path serves the wire and the
    loopback simultaneously is invisible to both homogeneous sets."""
    tks = dut.talker_indices(include_crf=False)
    plss = peer.listener_indices(include_crf=False)
    dlss = dut.listener_indices(include_crf=False)
    if len(tks) < 2 or not plss or not dlss:
        return []
    out, pi, di = [], 0, 0
    for n, ti in enumerate(tks):
        if n % 2 == 0 and pi < len(plss):
            out.append(_multi_pair(Endpoint(dut, ti), Endpoint(peer, plss[pi]), fmt))
            pi += 1
        elif di < len(dlss):
            out.append(_multi_pair(Endpoint(dut, ti), Endpoint(dut, dlss[di]), fmt))
            di += 1
    return out


def _multi_pairs_stress(dut: Device, peer: Device, fmt) -> list:
    """EVERYTHING the shapes allow, concurrently - the maximal stream set.

    (a) every DUT AAF talker outbound: the peer's reachable listeners first
        (cyclic when the DUT has fewer talkers than the peer has listeners,
        exactly as the primaries set), then SELF-LOOPS to fill the talkers
        the peer cannot absorb - on the AX 8x8 against the reference device
        that is t0..t4 -> the five primaries and t5..t7 looped home;
    (b) the INBOUND direction on top: peer AAF talkers into whatever DUT
        listeners are still free, so RX is loaded by real wire ingress and
        not only by the loopback path.

    All of it from the device specs, never hardcoded; a peer with no
    reachable listeners degenerates to self-loops plus inbound, which is
    still a maximal set for that bench.
    """
    tks = dut.talker_indices(include_crf=False)
    plss = peer.listener_indices(include_crf=False)
    dlss = dut.listener_indices(include_crf=False)
    out = []
    if tks and plss:
        out += [_multi_pair(Endpoint(dut, tks[i % len(tks)]), Endpoint(peer, li),
                            fmt)
                for i, li in enumerate(plss)]
    free = list(dlss)
    for ti in tks[len(plss):]:
        if not free:
            break
        out.append(_multi_pair(Endpoint(dut, ti), Endpoint(dut, free.pop(0)), fmt))
    for ti in peer.talker_indices(include_crf=False):
        if not free:
            break
        out.append(_multi_pair(Endpoint(peer, ti), Endpoint(dut, free.pop(0)), fmt))
    return out


def _multi_single_listener_pair(pairs: list) -> dict:
    """The pair the staged teardown unbinds FIRST: one whose talker serves
    exactly one listener in the set, so the stop-verification can expect
    silence.  A talker feeding two listeners keeps its licence through the
    remaining Listener Ready (Milan v1.2 5.3.7.3), so unbinding one of its
    listeners owes CONTINUED streaming, not silence - the plan states which
    expectation applies rather than leaving the runner to guess."""
    counts = {}
    for p in pairs:
        k = (p["talker"], p["talker_index"])
        counts[k] = counts.get(k, 0) + 1
    for p in pairs:
        if counts[(p["talker"], p["talker_index"])] == 1:
            return p
    return pairs[-1]


def _multi_stress_steps(sid, name, pairs, unbound):
    """The best-effort load sandwich: load RX, load TX, verify with it OFF.

    802.1Q-2018 8.6.8.2 puts an admitted class A stream in a reserved,
    credit-shaped queue, so best-effort load must not disturb it - and
    only the before/during/after sandwich can attribute a wound to the
    load rather than to the run.
    """
    steps = []
    for direction, what in (
            ("rx", "external peer -> DUT best-effort traffic: inbound "
                   "wire stress"),
            ("tx", "DUT -> host best-effort TCP: TX stress against the "
                   "shaped egress queues")):
        steps.append(Step(
            sid + f".load-{direction}", "multi", "multi_stress_load",
            {"set": name, "pairs": pairs, "direction": direction,
             "measure_s": 4.0, "load_seconds": 16.0},
            asserts=MULTI_STRESS_LOAD_ASSERTS,
            clause="802.1Q-2018 8.6.8.2/34: admitted SR class A streams "
                   "travel in a reserved, credit-shaped queue, so "
                   "best-effort load SHALL NOT disturb them; Milan "
                   "Table 5.4/5.6 interval terms for the measurement",
            note=what + ".  iperf3 on the board is PROBED, never assumed "
                        "(the board image need not carry it); the RX "
                        "fallback is a blind "
                        "UDP blast from the controller host, named as "
                        "such in every record; TX with no board tooling "
                        "cannot be generated from the host and SKIPs "
                        "naming what to supply"))
    steps.append(Step(
        sid + ".verify-after-load", "multi", "multi_verify",
        {"set": name, "pairs": pairs, "unbound": unbound,
         "measure_s": 4.0},
        asserts=MULTI_VERIFY_ASSERTS,
        clause="Milan v1.2 5.3.7.3 + Table 5.4/5.6: load OFF, the same "
               "full verification - a wound that persists past the load "
               "is a different finding from transient interference, and "
               "only the before/during/after sandwich can tell them "
               "apart",
        note="identical machinery to verify-concurrent on purpose, so "
             "the two windows diff line for line"))
    return steps


def _multi_set_steps(name: str, dut: Device, peer: Device, pairs: list,
                     note: str, *, stress: bool = False) -> list:
    """bind-all -> verify-concurrent [-> load-rx -> load-tx ->
    verify-after-load, for a stress set] -> teardown-one -> teardown-rest.

    The staged teardown is the point: unbind ONE stream, prove the others
    keep flowing, THEN take the rest down with the same stop-takes-effect
    discipline the matrix uses.  A stress set additionally runs best-effort
    load over the same link, both directions sequentially, WHILE every stream
    flows - and re-verifies with the load OFF, because the before/during/
    after sandwich is what attributes a failure to the load."""
    sid = f"multi.{name}"
    bound = {(p["listener"], p["listener_index"]) for p in pairs}
    unbound = []
    for dev in (dut, peer) if peer is not dut else (dut,):
        for li in dev.listener_indices(include_crf=False):
            if (dev.entity_id, li) not in bound:
                unbound.append({"entity": dev.entity_id, "mac": dev.mac,
                                "index": li, "label": f"{dev.name}l{li}"})
    tear = _multi_single_listener_pair(pairs)
    survivors = [p for p in pairs if p is not tear]
    tear_alone = sum(1 for p in pairs
                     if (p["talker"], p["talker_index"]) ==
                     (tear["talker"], tear["talker_index"])) == 1
    steps = [
        Step(sid + ".bind-all", "multi", "multi_connect",
             {"set": name, "pairs": pairs},
             asserts=MULTI_BIND_ASSERTS,
             clause="Milan v1.2 5.5.3.5 BIND_RX, once per pair, with the "
                    "5.5.1.2 listener-adapts format rule applied per pair",
             note=note),
        Step(sid + ".verify-concurrent", "multi", "multi_verify",
             {"set": name, "pairs": pairs, "unbound": unbound,
              "measure_s": 4.0},
             asserts=MULTI_VERIFY_ASSERTS,
             clause="Milan v1.2 5.3.7.3 per Stream Output + Table 5.4/5.6 "
                    "interval terms + 5.3.8.10 per-input counters",
             note="ONE shared window across every side, bound and unbound - "
                  "a serial walk cannot see cross-stream interference.  The "
                  "licence gates the flow expectations exactly as the "
                  "pairwise steps' do, and the comparison is interval ticks, "
                  "never frames"),
    ]
    if stress:
        steps += _multi_stress_steps(sid, name, pairs, unbound)
    steps += [
        Step(sid + ".teardown-one", "multi", "multi_teardown_one",
             {"set": name, "unbind": tear, "survivors": survivors,
              "expect_talker_silent": tear_alone,
              "stop_window_s": 4.0, "measure_s": 4.0},
             asserts=MULTI_TEARDOWN_ONE_ASSERTS,
             clause="Milan v1.2 5.5.3.5 UNBIND_RX + 5.3.7.3: only the "
                    "torn-down stream's licence ends; the survivors keep "
                    "flowing undisturbed",
             note="the cross-stream-independence probe: a teardown that "
                  "kills a neighbour stream is the defect this step exists "
                  "to catch"),
        Step(sid + ".teardown-rest", "multi", "multi_teardown_rest",
             {"set": name, "pairs": survivors, "stop_window_s": 4.0},
             asserts=MULTI_TEARDOWN_REST_ASSERTS,
             clause="Milan v1.2 5.5.3.5 UNBIND_RX + 5.3.7.3 + IEEE "
                    "1722.1-2021 7.4.36: after the last unbind each talker "
                    "owes silence, verified per talker",
             note="an unverified stop latches the talker and poisons every "
                  "later measurement (the 94-of-95 false-PASS history), so "
                  "the full teardown verifies per talker exactly as the "
                  "matrix unbind does"),
    ]
    return steps


def plan_multi(dut: Device = ARTY, peer: Device = PEER) -> list:
    """MULTI-STREAM CONCURRENCY: many streams bound and verified AT ONCE.

    The matrix walks pair by pair, and four whole defect classes are invisible
    to that walk because they only exist under aggregate load: CBS shaping
    with several class A streams in the shaped queue at once, the multi-slot
    rings actually multiplexing, per-index counter ISOLATION (an unbound index
    ticking while a neighbour streams - the alias/bleed class that produced
    four real defects under index-0-only testing), and cross-stream
    independence at teardown (an unbind that kills a neighbour).  Real
    deployments run many streams simultaneously, so a campaign that only ever
    binds one at a time certifies a shape no deployment uses.

    Four sets, each derived from the device SPECS and never hardcoded:
      * primaries - every reachable reference listener fed concurrently
        (on the AX 8x8 against the peer: t0..t3 -> l0/2/4/6);
      * selfloop  - the DUT's own tN -> lN, both directions of the fabric
        loaded at once, no peer needed;
      * mixed     - outbound and loopback interleaved, when the shapes allow;
      * stress    - EVERYTHING the shapes allow at once (all outbound:
        primaries + self-loop fill; plus the inbound direction), and then
        best-effort iperf load over the same link, both directions
        sequentially, WHILE it all flows - 802.1Q shaping says the reserved
        streams SHALL NOT notice.  Load off, the set is re-verified before
        the staged teardown.
    Each set runs bind-all -> verify-concurrent [-> the stress load
    sandwich] -> STAGED teardown (one stream out, prove the others
    undisturbed, then the rest with per-talker stop verification).  Sets run
    serially and each is fully torn down before the next, so a set's
    verdicts are never polluted by a predecessor.
    """
    fmt = dut.formats[0] if dut.formats else None
    steps = []
    for name, pairs, note, stress in (
            ("primaries", _multi_pairs_primaries(dut, peer, fmt),
             "every reachable reference listener fed concurrently; the "
             "listener set comes from the peer's spec (on a redundant device "
             "that is the (p) primaries only)", False),
            ("selfloop", _multi_pairs_selfloop(dut, fmt),
             "the DUT's own talkers into its own listeners, tN -> lN, so "
             "every packetizer and depacketizer works at once", False),
            ("mixed", _multi_pairs_mixed(dut, peer, fmt),
             "outbound and loopback interleaved in one concurrent set",
             False),
            ("stress", _multi_pairs_stress(dut, peer, fmt),
             "the MAXIMAL set: every DUT AAF talker outbound (reachable "
             "reference listeners first, self-loops to fill) plus the "
             "inbound direction, all concurrent - then best-effort load "
             "both ways while it flows", True)):
        if pairs:
            steps += _multi_set_steps(name, dut, peer, pairs, note,
                                      stress=stress)
    return steps


def plan_churn(dut: Device = ARTY, peer: Device = PEER) -> list:
    """Bind churn: the transitions a bind/unbind loop never reaches.

    (a) IMPLICIT REBIND - Milan v1.2 5.5.3.5.43: a BIND_RX arriving at a Stream
        Input already in SETTLED_RSV_OK rebinds it, with no unbind in between.
        Every listener index gets one, and the talker it moves to is a
        DIFFERENT talker index, because rebinding to the same talker cannot
        distinguish "handled the transition" from "ignored the command".
    (b) UNBIND then RE-BIND the same pair - the counter-reset assertion.
    (c) BIND WHILE STREAMING - a second listener joins a talker that is already
        streaming to a first.
    (d) REBIND STORM - N implicit rebinds back to back with no settle time.
    """
    steps = []
    for li in dut.listener_indices(include_crf=False):
        t0, t1 = 0, min(1, max(0, peer.talkers - 1))
        if peer.talkers < 2:
            continue
        steps.append(Step(
            f"churn.implicit-rebind.l{li}", "churn", "connect",
            {"talker": peer.entity_id, "talker_index": t0,
             "talker_mac": peer.mac, "listener": dut.entity_id,
             "listener_index": li, "listener_mac": dut.mac},
            asserts=BOUND_STREAMING_ASSERTS,
            clause="Milan v1.2 5.5.3.5.43 - the first bind of the pair"))
        steps.append(_start_if_needed_step(
            f"churn.implicit-rebind.l{li}", "churn",
            Endpoint(peer, t0), Endpoint(dut, li)))
        steps.append(Step(
            f"churn.implicit-rebind.l{li}.rebind", "churn", "connect",
            {"talker": peer.entity_id, "talker_index": t1,
             "talker_mac": peer.mac, "listener": dut.entity_id,
             "listener_index": li, "listener_mac": dut.mac,
             "no_unbind_first": True},
            asserts=BOUND_STREAMING_ASSERTS + (A_COUNTER_RESET_ON_BIND,
                                               A_REBIND_NO_RESET),
            clause="Milan v1.2 5.5.3.5.43 SETTLED_RSV_OK / RCV_BIND_RX_CMD: a "
                   "BIND_RX for an already-bound Stream Input is an implicit "
                   "rebind, NOT an error - and NOT a reset boundary: the "
                   "input never transits UNBOUND (same talker: step 2 exits; "
                   "different talker: steps 3-12 re-probe), so the 5.3.8.10 "
                   "trigger 'from not bound to bound' does not fire; whether "
                   "the counters reset anyway is recorded, never judged "
                   "(campaign ax-rv32-e filed 31 conformant rebinds as SHALL "
                   "violations before this distinction)",
            note="a refusal here is a known open finding on this fabric, and "
                 "the runner records the status rather than stopping"))
        steps.append(_start_if_needed_step(
            f"churn.implicit-rebind.l{li}.rebind", "churn",
            Endpoint(peer, t1), Endpoint(dut, li)))
        steps.append(Step(
            f"churn.implicit-rebind.l{li}.unbind", "churn", "disconnect",
            {"talker": peer.entity_id, "talker_index": t1,
             "talker_mac": peer.mac, "listener": dut.entity_id,
             "listener_index": li, "stop_streaming": True,
             "stop_window_s": 4.0},
            asserts=(A_ACMP_STATUS, A_ADP_ALIVE, A_STOP_TAKES_EFFECT)))
    # (c) bind while streaming - two listeners on one talker
    if peer.listeners >= 2:
        for i, li in enumerate(peer.listener_indices(include_crf=False)[:2]):
            steps.append(Step(
                f"churn.bind-while-streaming.{i}", "churn", "connect",
                {"talker": dut.entity_id, "talker_index": 0,
                 "talker_mac": dut.mac, "listener": peer.entity_id,
                 "listener_index": li, "listener_mac": peer.mac},
                asserts=BOUND_STREAMING_ASSERTS,
                clause="IEEE 1722.1-2021 8.2.2.6.2.1: a Talker supports "
                       "multiple Listeners on one stream up to "
                       "max_supported_streams; the second bind must not "
                       "interrupt the first (Milan v1.2 5.3.7.3)"))
            steps.append(_start_if_needed_step(
                f"churn.bind-while-streaming.{i}", "churn",
                Endpoint(dut, 0), Endpoint(peer, li)))
    # (d) rebind storm
    steps.append(Step(
        "churn.rebind-storm", "churn", "rebind_storm",
        {"listener": dut.entity_id, "listener_index":
            dut.listener_indices(include_crf=False)[-1],
         "talkers": [{"entity": peer.entity_id, "index": i}
                     for i in range(peer.talkers)],
         "iterations": 20, "settle_s": 0.0},
        asserts=(A_ACMP_STATUS, A_ADP_ALIVE, A_LOCK_INVARIANT,
                 A_IN_MASK, A_TALKER_INVARIANT),
        clause="Milan v1.2 5.5.3.5.43 + 5.3.8.10: after any number of implicit "
               "rebinds the lock invariant still holds and the entity is still "
               "discoverable; the invariant is what makes a storm auditable "
               "without knowing which bind won"))
    return steps


def plan_payload(dut: Device = ARTY) -> list:
    """Wire-truth captures.  Each entry names the tap, the declared format the
    capture must be judged against, and the analyser check set that applies."""
    steps = []
    for ti in dut.talker_indices():
        crf = dut.is_crf_talker(ti)
        steps.append(Step(
            f"payload.capture.t{ti}", "payload", "capture_and_analyse",
            {"tap": "dut", "seconds": 6, "talker": dut.entity_id,
             "talker_mac": dut.mac, "talker_index": ti,
             "expect_format": None if crf else (dut.formats[0]
                                                if dut.formats else None),
             "expect_crf": crf,
             "analyser": "avtp_wire_truth"},
            asserts=(A_WIRE_MATCHES_FORMAT, A_STREAM_CONTINUITY),
            clause="IEEE 1722-2016 I.2.4.1 (declared == emitted) + Milan v1.2 "
                   "7.3.2/7.3.3 for the CRF stream",
            note="the analyser adds its own verdict per check; this step "
                 "records the capture and the expectation it is judged under"))
    # THE SRP CAPTURE.  MSRP/MVRP go to 01:80:C2:00:00:0E, which a bridge does
    # NOT forward, so the Listener Ready half of the Milan 5.3.7.3 licence is
    # invisible from the controller host and visible ONLY from an inline tap.
    # This entry names the entity's WHOLE Stream Output set, so the capture can
    # answer which of them never declared - not merely which streamed undeclared.
    steps.append(Step(
        "payload.srp-declarations", "payload", "capture_and_analyse",
        {"tap": "dut", "seconds": 12, "talker": dut.entity_id,
         "talker_mac": dut.mac,
         "expect_talker_streams": dut.stream_ids(),
         "bpf": "ether[40:2]=0x22ea or ether[40:2]=0x88f5",
         "analyser": "avtp_wire_truth"},
        asserts=(A_SRP_LICENCE,
                 AssertSpec("wt.msrp.talker-advertise-declared",
                            "Milan v1.2 5.3.7.2: 'For each of the Stream "
                            "Outputs of its currently set Configuration, a PAAD "
                            "shall always declare an MSRP Talker attribute as "
                            "soon as it has valid SRP parameters for this "
                            "stream' - so a Stream Output that never declares is "
                            "a defect, and only the tap can see it"),
                 AssertSpec("wt.msrp.listener-declaration-present",
                            "Milan v1.2 5.3.7.3: the licence's second half is a "
                            "Listener Ready or Listener Ready Failed attribute, "
                            "which arrives over MSRP on 01:80:C2:00:00:0E"),
                 AssertSpec("wt.msrp.declared-dmac-matches-wire",
                            "Milan v1.2 5.3.7.4: the Stream Destination MAC "
                            "Address is an SRP parameter, so the declaration and "
                            "the wire DMAC are one value"),
                 AssertSpec("wt.msrp.declared-vid-matches-wire",
                            "Milan v1.2 5.3.7.4 + 802.1Q-2018 9.6: the Stream "
                            "VLAN ID is an SRP parameter")),
        clause="802.1Q-2018 35.2.2 + Milan v1.2 5.3.7.2/5.3.7.3/5.3.7.4",
        note="capture for a DURATION on the tap host and filter FOR MRP; MRP "
             "re-declares on its own timers, so a short frame budget on a "
             "running stream captures ~50 ms of wire and shows no MRP at all"))
    steps.append(Step(
        "payload.zero-fill", "payload", "capture_and_analyse",
        {"tap": "dut", "seconds": 4, "expect_silent_all_bound_talkers": True,
         "analyser": "avtp_wire_truth"},
        asserts=(A_TX_TICKING,),
        clause="Milan v1.2 5.3.7.3: a bound talker with no audio source still "
               "streams, so the capture must show FRAMES that are SILENT - "
               "absence and silence are different verdicts"))
    return steps


A_AUDIO_UNCROSSED = AssertSpec(
    "audio.identity.uncrossed",
    "IEEE 1722-2016 7.3.5: the payload is a chronological sequence of sample "
    "frames, each carrying one sample per channel IN CHANNEL ORDER, so channel "
    "k is payload sample k mod channels_per_frame")
A_AUDIO_NO_DUP = AssertSpec(
    "audio.identity.no-duplicate-neighbour",
    "IEEE 1722-2016 7.3.5: two channels carrying identical content is the "
    "signature of a mux stuck on one pair, and presence testing cannot see it")
A_AUDIO_NO_SILENT = AssertSpec(
    "audio.identity.no-silent-channel",
    "IEEE 1722-2016 7.3.5 + Milan v1.2 5.3.10.1: a mapped channel that carries "
    "nothing is a dropped channel")
A_AUDIO_PRESERVED = AssertSpec(
    "audio.identity.channel-preserved",
    "Milan v1.2 5.3.10.1 channel mapping: a channel-preserving loop through a "
    "Milan-validated device returns ch 1/2 on ch 1/2, which makes the test an "
    "IDENTITY test and not a counter test")


def plan_audio(dut: Device = ARTY, peer: Device = PEER,
               settings: "ReleaseSettings | None" = None) -> list:
    """AUDIO IS NEVER FORGOTTEN.  Three shapes, because presence testing cannot
    tell a correct channel map from a crossed one - and EVERY INDEX, because
    index 0 is the least representative index on this fabric.

    The index-0-only version of this area was the audio half of the same defect
    the matrix area exists to prevent: the walking tone was captured on talker 0
    only, the loop ran through peer listener 0 and peer talker 0 only, and the
    coverage audit could not see it because it was computed over the WHOLE plan,
    where the matrix's full coverage masked the audio area entirely.  Coverage is
    now audited PER AREA (plan_coverage_by_area) and this walks every index.

    The area ends with issue #396's release audio-integrity run, which rides
    inside the soak window, and its planted-drop negative control.
    """
    return _audio_identity_steps(dut, peer) + _audio_release_steps(
        dut, peer, settings if settings is not None else ReleaseSettings())


def _audio_identity_steps(dut: Device, peer: Device) -> list:
    """The channel-identity loop, the per-channel walking tone and THD+N."""
    steps = []
    for ti in dut.talker_indices(include_crf=False):
        li = ti if ti < peer.listeners else 0
        pt = ti if ti < peer.talkers else 0
        dl = ti if ti < dut.listeners else 0
        steps.append(Step(
            f"audio.identity.loop-ch12.t{ti}", "audio", "audio_identity_loop",
            {"talker": dut.entity_id, "talker_mac": dut.mac,
             "talker_index": ti, "peer": peer.entity_id, "peer_mac": peer.mac,
             "peer_listener": li, "peer_talker": pt,
             "listener": dut.entity_id, "listener_mac": dut.mac,
             "dut_listener": dl, "listener_index": dl,
             "channels": [1, 2], "pattern": "walking"},
            asserts=(A_ACMP_STATUS, A_RX_TICKING, A_AUDIO_UNCROSSED,
                     A_AUDIO_PRESERVED),
            clause="IEEE 1722-2016 7.3.5 + Milan v1.2 5.3.10.1",
            note=f"stream talker {ti} to the reference device's ch 1/2 and it "
                 f"returns on ch 1/2 into sink {dl}; the peer is the "
                 f"independent oracle"))
    for ti in dut.talker_indices(include_crf=False):
        steps.append(Step(
            f"audio.identity.walking-tone-all-channels.t{ti}", "audio",
            "audio_identity_capture",
            {"talker": dut.entity_id, "talker_mac": dut.mac,
             "talker_index": ti, "pattern": "walking",
             "per_channel_distinct": True},
            asserts=(A_AUDIO_UNCROSSED, A_AUDIO_NO_DUP, A_AUDIO_NO_SILENT),
            clause="IEEE 1722-2016 7.3.5",
            note="every driven sample is DISTINCT per (channel, sample event) - "
                 "a pattern that drove equal values on two channels could not "
                 "fail on a swap (methodology R4)"))
    steps.append(
        Step("audio.thdn", "audio", "thdn_gate",
             {"source": "wire_capture", "rate_hz": 48000, "f0_hz": 1000,
              "channels": 2, "accept_dbfs": -120.0,
              "analyser": "tb/tools/thdn.py"},
             asserts=(AssertSpec("audio.thdn.worst-channel",
                                 "USER acceptance: THD+N <= -120 dBFS end to "
                                 "end; the digital source itself measures "
                                 "-147.99 dBFS, so the wire+fabric path must add "
                                 "nothing"),
                      AssertSpec("audio.thdn.coherent-not-windowed",
                                 "the pilot tone is exact-period (48 samples = "
                                 "1 kHz at 48 kHz), so a capture truncated to "
                                 "whole periods is coherently sampled; "
                                 "applying a window spreads the fundamental "
                                 "into neighbouring bins which the residual "
                                 "then counts as distortion - it MANUFACTURES "
                                 "the number it is supposed to measure")),
             clause="reuses tb/tools/thdn.py - do not reimplement",
             note="numpy is required for this one step and nowhere else"))
    return steps


# ------------------------------------------------------- adverse conditions --
def _torture_storm_steps(dut):
    """1. Sustained high-rate traffic, one entry per traffic class."""
    S = []
    # --- 1. sustained high rate traffic, per traffic class -----------------
    for cls, desc, dst in (
            ("non-priority-broadcast",
             "untagged broadcast flood at line rate", "ff:ff:ff:ff:ff:ff"),
            ("non-priority-unicast-to-us",
             "unicast flood addressed to the DUT's own MAC - the case the "
             "recommendation draws attention to explicitly", dut.mac),
            ("avdecc-flood",
             "AVDECC (ethertype 0x22F0) command flood; AVDECC is Non-Priority",
             "91:e0:f0:01:00:00"),
            ("avb-management",
             "AVB Management group addresses 01:80:C2:00:00:00 / :0E / :21 "
             "(802.1Q-2018 Table 8-1 and 10-1)", "01:80:c2:00:00:0e"),
            ("class-b-stream",
             "SR class B tagged traffic at line rate", "91:e0:f0:00:fe:ff")):
        S.append(Step(
            f"torture.storm.{cls}", "torture", "background_load",
            {"traffic": cls, "dst": dst, "rate": "line", "seconds": 30,
             "while_streaming": True},
            asserts=(A_STREAM_CONTINUITY, A_NO_SEQ_MISMATCH, A_LOCK_INVARIANT,
                     A_CONTROL_RESPONSIVE),
            clause="the Milan adverse-network-conditions recommended "
                   "practice, §2: a device in a streaming state 'shall "
                   "not experience any stream interruption when subjected to "
                   "high rate Non-Priority traffic'",
            note=desc + ".  RECOMMENDED, not required - a failure is a finding "
                        "with a cost/benefit decision attached, and AVDECC "
                        "unresponsiveness under storm is EXPECTED by the same "
                        "clause"))
    return S


def _torture_link_steps(dut):
    """2. Link bounces: the CSR-driven one a runner can drive alone, and
    the cable pull that is the honest version of the same test."""
    S = []
    # --- 2. link bounces ---------------------------------------------------
    S.append(Step(
        "torture.link.bounce-software", "torture", "link_bounce",
        {"how": "phy-reset-via-csr", "count": 5, "down_s": 2},
        asserts=(A_IFACE_MASK, A_ADP_ALIVE, A_LOCK_INVARIANT,
                 AssertSpec("counters.avb_interface.link-up-down-pairs",
                            "IEEE 1722.1-2021 Table 7-153 LINK_UP / LINK_DOWN: "
                            "each counts its own events, so a bounce advances "
                            "both and LINK_UP is LINK_DOWN or LINK_DOWN+1 by "
                            "the same argument Milan uses for MEDIA_LOCKED"),
                 AssertSpec("stream.recovers-without-intervention",
                            "Milan v1.2 5.3.7.3: once the Talker Advertise and "
                            "the Listener Ready are back the talker streams "
                            "again; recovery must not need a controller")),
        clause="802.1AS-2020 10.2.4 portEnabled / IEEE 1722.1-2021 6.2.6",
        note="the software bounce is the one a runner can drive alone; the "
             "CABLE PULL below is the honest version of the same test"))
    S.append(Step(
        "torture.link.cable-pull", "torture", "human_action",
        {"target": dut.name},
        needs_human=True,
        human_action="Unplug the DUT's Ethernet cable for 5 s, then plug it "
                     "back into THE SAME switch port.  Then repeat into a "
                     "DIFFERENT port.",
        asserts=(A_IFACE_MASK, A_ADP_ALIVE,
                 AssertSpec("stream.recovers-without-intervention",
                            "Milan v1.2 5.3.7.3 + 802.1AS-2020 10.2.4"),
                 AssertSpec("srp.reservation-reestablished",
                            "802.1Q-2018 35.2.4: MSRP declarations are "
                            "re-registered after a port event; a stream that "
                            "returns without a reservation is streaming "
                            "unshaped")),
        clause="802.1AS-2020 10.2.4 / 802.1Q-2018 35.2.4",
        note="a real PHY link loss exercises the link guard, the MAC and the "
             "reservation together; a CSR-driven reset does not"))
    return S


def _torture_malformed_steps():
    """4. Malformed and truncated control frames, each citing its own clause."""
    S = []
    for name, mutation, clause in (
            ("cdl-overstated",
             "control_data_length larger than the frame that carries it",
             "IEEE 1722.1-2021 9.2.1.1.6: control_data_length counts the "
             "octets after target_entity_id.  A responder that trusts the "
             "field over the frame reads past the buffer; one that answers "
             "SUCCESS to a frame that lies has validated nothing"),
            ("cdl-understated",
             "control_data_length shorter than the payload present",
             "IEEE 1722.1-2021 9.2.1.1.6 - the surplus octets are not payload, "
             "and a responder that parses them is parsing pad"),
            ("truncated-mid-payload",
             "AECP command cut off inside its command-specific payload",
             "IEEE 1722.1-2021 9.2.1.2: a command whose payload is too short "
             "for its command_type gets a status response, not silence"),
            ("acmp-short-pdu",
             "ACMPDU one octet short of the 70-octet minimum",
             "IEEE 1722.1-2021 8.2.1: the ACMPDU is a fixed 70 octets; the "
             "68-byte frame this project once accepted was rightly rejected, "
             "so the assertion is that the SHORT frame is IGNORED and the "
             "correct one is answered"),
            ("avtp-bad-version",
             "AVTP version field non-zero on a stream frame",
             "IEEE 1722-2016 4.4.4.3: a Listener 'shall ignore' an AVTPDU "
             "whose version it does not support - and this fabric's current "
             "behaviour of ignoring the field is a recorded deviation, not a "
             "silent pass"),
            ("aaf-sdl-overstated",
             "AAF stream_data_length larger than the payload",
             "IEEE 1722-2016 4.4.4.10 + 7.3.5: the payload the field describes "
             "is not there, so the frame cannot be rendered; the listener owes "
             "a discard, not a buffer overrun"),
            ("aaf-channels-mismatch",
             "AAF channels_per_frame not the listener's current format",
             "Milan v1.2 Table 5.6 UNSUPPORTED_FORMAT: 'Incremented at the end "
             "of every observation interval during which a Stream Data AVTPDU "
             "has been received with a format that did not match the current "
             "format of the Stream Input'"),
            ("aecp-unknown-command",
             "AEM command_type this entity does not implement",
             "IEEE 1722.1-2021 9.2.1.3.3: an unimplemented command is answered "
             "NOT_IMPLEMENTED, and 7.4.1 the response is the same SIZE as a "
             "success response for that command"),
            ("aecp-wrong-target",
             "AECP command addressed to another entity_id",
             "IEEE 1722.1-2021 9.2.1.1.7: a command whose target_entity_id is "
             "not ours is not ours to answer - silence is correct here and a "
             "response is the defect")):
        S.append(Step(
            f"torture.malformed.{name}", "torture", "malformed_frame",
            {"mutation": name, "repeat": 50},
            asserts=(A_ADP_ALIVE, A_STREAM_CONTINUITY,
                     AssertSpec(f"malformed.{name}.handled",
                                clause),
                     AssertSpec("entity.no-wedge-after-malformed",
                                "IEEE 1722.1-2021 9.2.1.2: after any malformed "
                                "input the entity still answers a WELL-FORMED "
                                "command; a responder wedged by a bad frame is "
                                "the worst outcome and the easiest to miss")),
            clause=clause, note=mutation))
    return S


def _torture_maap_steps(dut):
    """5. MAAP conflicts."""
    S = []
    # --- 5. MAAP conflicts --------------------------------------------------
    S.append(Step(
        "torture.maap.conflict", "torture", "maap_conflict",
        {"claim_same_dmac_as": dut.name, "seconds": 20},
        asserts=(AssertSpec("maap.withdraws-and-reallocates",
                            "Milan v1.2 5.3.7.5 Table 5.3: 'While a Stream "
                            "Output is declaring a Talker attribute, if MAAP "
                            "reports a conflict, the PAAD withdraws the Talker "
                            "attribute, waits for 2 LeaveAll periods and "
                            "allocates a new Destination MAC Address, then "
                            "declares a new Talker attribute with the new "
                            "Destination MAC Address'"),
                 A_ADP_ALIVE,
                 AssertSpec("stream.dmac-follows-the-new-claim",
                            "Milan v1.2 5.3.7.4: the Stream Destination MAC "
                            "Address is an SRP parameter, so the wire DMAC and "
                            "the declaration move together")),
        clause="Milan v1.2 5.3.7.5 Table 5.3 + IEEE 1722-2016 Annex B",
        note="the 2 LeaveAll wait is part of the requirement: an immediate "
             "re-claim is a different behaviour"))
    return S


def _torture_vlan_steps():
    """6. VLAN misconfiguration."""
    S = []
    # --- 6. VLAN misconfiguration -----------------------------------------
    S.append(Step(
        "torture.vlan.wrong-sr-vid", "torture", "vlan_misconfig",
        {"set_vid": 1, "restore_vid": 2},
        asserts=(AssertSpec("srp.reservation-refused-or-withdrawn",
                            "802.1Q-2018 35.1.2: a reservation is per SR "
                            "domain; a stream tagged outside the SR VID is not "
                            "covered by any reservation and must not be "
                            "presented as reserved"),
                 AssertSpec("wire.vid-matches-declaration",
                            "802.1Q-2018 9.6 + Milan v1.2 5.3.7.4: the Stream "
                            "VLAN ID is an SRP parameter, so the tag and the "
                            "declaration are one value"),
                 A_ADP_ALIVE),
        clause="802.1Q-2018 35.1.2 / Milan v1.2 5.3.7.4",
        note="VID 0 is the specific past defect: the tag is stripped on egress "
             "and the frames flood unshaped, so the plan checks VID 0 as its "
             "own case below"))
    S.append(Step(
        "torture.vlan.vid-zero", "torture", "vlan_misconfig",
        {"set_vid": 0, "restore_vid": 2},
        asserts=(AssertSpec("wire.no-untagged-stream-frames",
                            "802.1Q-2018 9.5/9.6 + Milan v1.2 7.3.3: an SR "
                            "stream is carried tagged; VID 0 leaves the "
                            "reserved SR tree and floods"),
                 A_ADP_ALIVE),
        clause="802.1Q-2018 9.6",
        note="measured on this bench: an undeclared multicast DMAC reached a "
             "port with no listener at 500 pps while AAF was pruned correctly"))
    return S


def _torture_starvation_steps():
    """7. Starvation and restart, on either side of the stream."""
    S = []
    # --- 7. starvation and restart ----------------------------------------
    S.append(Step(
        "torture.starve.talker-source-removed", "torture", "starve_source",
        {"seconds": 20},
        asserts=(A_TX_TICKING,
                 AssertSpec("wire.zero-fill-not-absence",
                            "Milan v1.2 5.3.7.3: the talker keeps streaming, "
                            "so the wire carries SILENT frames and not no "
                            "frames; STREAMING_WAIT 'shall not be "
                            "implemented'"),
                 A_TALKER_INVARIANT),
        clause="Milan v1.2 5.3.7.3"))
    S.append(Step(
        "torture.starve.listener-stream-stops", "torture", "stop_talker",
        {"seconds": 20},
        asserts=(AssertSpec("counters.stream_input.stream-interrupted-advances",
                            "Milan v1.2 Table 5.6 STREAM_INTERRUPTED: "
                            "'Incremented each time the stream playback is "
                            "interrupted for any reason other than a "
                            "Controller Unbind operation'"),
                 A_LOCK_INVARIANT,
                 AssertSpec("counters.stream_input.media-unlocked-advances",
                            "Milan v1.2 Table 5.6 MEDIA_UNLOCKED + the lock "
                            "invariant: losing the stream unlocks the media "
                            "clock, so MEDIA_LOCKED == MEDIA_UNLOCKED again")),
        clause="Milan v1.2 Table 5.6"))
    return S


def plan_torture(dut: Device = ARTY, peer: Device = PEER) -> list:
    """The adverse-conditions matrix.

    SOURCING, stated plainly because it decides what a failure MEANS.  The
    Milan adverse-network-conditions recommended practice covers exactly ONE
    condition - sustained high rate traffic, in four traffic classes - and it is
    a RECOMMENDATION: "It is not a current requirement for a Milan device to
    support the features mentioned."  It says nothing about malformed packets.
    So:
      * storm entries cite that document and carry severity RECOMMENDED;
      * malformed/truncated-frame entries cite 1722.1-2021 instead;
      * link/gPTP/MAAP/VLAN entries cite 802.1AS, 1722.1 and 802.1Q.
    Anything with no clause in reach is marked INFO and recorded, never failed.
    """
    # --- 3. gPTP grandmaster changes and loss, and the DUT power cycle -----
    #  MOVED to the `physical` area (plan_physical): powering the switch off
    #  and back on IS the grandmaster loss (each end station becomes its own
    #  island GM) and the re-join IS the grandmaster change (BMCA re-elects
    #  with priority1 untouched - the USER standing rule that recovery must be
    #  automatic, never a forced win).  The physical area runs LAST because a
    #  partition mid-campaign would pollute every later verdict.  The DUT
    #  power cycle went the same way, where it is powerstrip-automatable, and
    #  its non-volatile assertions (A_STATE_RESTORED / A_COUNTERS_ZEROED)
    #  travelled with it.
    return (_torture_storm_steps(dut)
            + _torture_link_steps(dut)
            + _torture_malformed_steps()
            + _torture_maap_steps(dut)
            + _torture_vlan_steps()
            + _torture_starvation_steps())


# ---------------------------------------------- the physical (power) family --
#: docs/reference/REGISTER_MAP.md: `VERSION` (0x004) identifies the flashed
#: gateware; `CLKV_STAT` (0x77C) bit 0 is the tu bit as currently stamped on
#: every AVTPDU. The fabric gPTP engine owns the clock-validity state behind
#: that bit, so a boot or recovery that fails to re-establish validity stamps
#: tu = 1 forever - exactly what the post-cycle assertion exists to catch.
VERSION_ADDR = 0x004
CLKV_STAT_ADDR = 0x77C
#: The healthy bare-metal RX-filter posture. Firmware takes MAC_CTRL's reset
#: 0x13 and enables all-multicast (bit 3) for link-local control traffic, while
#: leaving promiscuous mode (bit 2) clear. Promiscuous mode outranks even an
#: explicit TCAM drop in the filter's decision order, so this value is read
#: back after boot rather than inferred from network reachability.
MAC_CTRL_ADDR = 0x100
DUT_RX_FILTER_HEALTHY_CTRL = 0x1B

A_PHYS_SNAPSHOT = AssertSpec(
    "physical.pre-snapshot-taken",
    "info: measure before AND after (the standing rule) - the retroactive "
    "verdicts of a physical cycle (the GPTP_GM_CHANGED delta, the counter "
    "reset, uptime monotonicity, the gateware VERSION word) are only decidable "
    "against a snapshot taken BEFORE the power event, so the snapshot is a "
    "step of its own and its absence turns those verdicts into SKIPs rather "
    "than guesses",
    severity="INFO")
A_PARTITION_EXPECTED = AssertSpec(
    "physical.partition-is-the-test",
    "info: the controller host reaches BOTH end stations through the switch "
    "under test, so total unreachability during the off-window is the "
    "condition APPLIED, not a result - timeouts inside the window are never "
    "failures, the CSR and board feeds are paused for its duration, and what "
    "happened mid-partition (each island electing its own GM per 802.1AS-2020 "
    "10.3) is verified RETROACTIVELY from the GPTP_GM_CHANGED counters and "
    "the gPTP logs after recovery",
    severity="INFO")
A_GM_CHANGED_ADVANCES = AssertSpec(
    "counters.avb_interface.gptp-gm-changed-advances",
    "IEEE 1722.1-2021 Table 7-153 GPTP_GM_CHANGED: 'gPTP grandmaster change "
    "count' (Milan v1.2 Table 5.3: 'Number of gPTP GM changes, since boot').  "
    "The counter counts changes of THE GRANDMASTER, so this assertion holds "
    "ONLY for a device that was FOLLOWING a remote GM before the partition: "
    "that device demonstrably lost its grandmaster, became its own island's "
    "GM and was re-elected a follower on the re-join, which is two changes, "
    "so its counter advances by a small bounded amount and one that never "
    "moved slept through the partition.  A device that was ALREADY the "
    "domain grandmaster is graded by gptp-gm-continuity instead: its own "
    "grandmasterIdentity never changed, and demanding an advance would "
    "demand a NON-conformant count.  (ax-phys-a 2026-08-02 filed exactly "
    "that fake red against the AX, which holds priority1 238 against the "
    "bridge's 246 and is GM before, during and after the partition.)")
A_GM_CONTINUITY = AssertSpec(
    "counters.avb_interface.gptp-gm-continuity",
    "IEEE 1722.1-2021 Table 7-153 + 802.1AS-2020 10.3: when the DUT wins "
    "BMCA on both sides of a partition (it is alone in its island while the "
    "domain is cut, and its priority1 is never touched), its OWN "
    "grandmasterIdentity is unchanged throughout - so the conformant "
    "GPTP_GM_CHANGED delta is exactly ZERO and the ADPDU carries the same "
    "gptp_grandmaster_id before and after.  A counter that moves here is "
    "counting something that is not a grandmaster change - a torn latch, a "
    "re-read of a partially written id, or a reset - which is the defect "
    "class this direction exists to catch.  Undecidable if the DUT "
    "restarted (7.4.42 makes the block volatile), so that case SKIPs")
A_PEER_GM_CHANGED = AssertSpec(
    "counters.avb_interface.peer-gptp-gm-changed-advances",
    "IEEE 1722.1-2021 Table 7-153 GPTP_GM_CHANGED, read on the OTHER end "
    "station: the side that was FOLLOWING the DUT's grandmaster is the side "
    "that provably lost it when the domain was cut, so the partition is "
    "observable there even when the DUT itself is the permanent GM.  A "
    "reference device that does not answer GET_COUNTERS for AVB_INTERFACE "
    "is a SKIP naming that, never a verdict about the DUT")
A_LINK_EVENT_SEEN = AssertSpec(
    "counters.avb_interface.link-event-observed",
    "info: IEEE 1722.1-2021 Table 7-153 LINK_UP/LINK_DOWN ('Total number of "
    "network link up/down events').  Whether a switch outage is a PHY event "
    "for the DUT is a CABLING fact, not a clause: this bench runs an inline "
    "regenerating tap on the DUT<->switch link, and such a tap holds the board-side link up while "
    "the switch side is dark - so a zero delta here is expected and a "
    "non-zero delta is equally conformant.  Recorded as a datum so the "
    "retroactive GM story can be read against what the DUT could actually "
    "see, and NEVER graded",
    severity="INFO")
A_GM_ID_FOLLOWS = AssertSpec(
    "adp.gptp-grandmaster-id-follows",
    "IEEE 1722.1-2021 6.2.2.13: the ADPDU carries gptp_grandmaster_id, so a "
    "controller sees the restored GM without asking")
A_ONE_GM_RESTORED = AssertSpec(
    "gptp.exactly-one-gm-after-heal",
    "802.1AS-2020 10.3: BMCA converges the healed domain on exactly one "
    "grandmaster - both end stations' ADPDUs carry the SAME non-zero "
    "gptp_grandmaster_id within the recovery budget, with priority1 untouched "
    "(USER standing rule: recovery must be automatic, never a forced win)")
A_GM_NOT_FLAPPING = AssertSpec(
    "gptp.gm-stable-not-flapping",
    "802.1AS-2020 10.3.13: after convergence the elected GM STAYS elected - "
    "GPTP_GM_CHANGED read twice across a settle gap advances by at most one "
    "more tick; a counter still climbing is a domain that never actually "
    "converged (the ever-changing-GM defect class)")
A_AS_CAPABLE_RESTORED = AssertSpec(
    "gptp.as-capable-restored",
    "802.1AS-2020 10.2.4.1 asCapable: the healed links exchange Pdelay and "
    "Announce again, evidenced by at least one end station following a REMOTE "
    "grandmaster; two boards each still claiming themselves GM after the "
    "budget are two islands that never re-joined")
A_TU_VALIDITY_RESTORED = AssertSpec(
    "gptp.tu-validity-restored",
    "IEEE 1722-2016 4.4.4.7 tu: tu = 1 is the fail-safe and tu = 0 has to be "
    "EARNED - the fabric-owned validity state (CLKV_STAT 0x77C bit 0) must be "
    "re-established once the GM is back, or every AVTPDU stamps tu = 1 "
    "forever. The reading is a DUT CSR, so without a CSR path "
    "this is a SKIP naming the register, never a guess")
A_NO_REBOOT = AssertSpec(
    "entity.survived-without-reboot",
    "IEEE 1722.1-2021 6.2.6: the entity stays available through a network "
    "partition - a link loss is not a reason to restart.  Graded from the "
    "board's own uptime (monotonic across the cycle) when a board path "
    "exists, else from counter monotonicity: IEEE 1722.1-2021 7.4.42 makes "
    "the counters volatile, so a post-cycle value BELOW the pre-snapshot is "
    "a restart")
A_BOOT_UNATTENDED = AssertSpec(
    "boot.reaches-network-unattended",
    "Milan v1.2 5.3.10.1 + IEEE 1722.1-2021 6.2.6: the persisted state is "
    "restored 'after a power cycle' and the entity advertises again, with "
    "ZERO manual intervention.  The budget is a bench fact, not a clause: "
    "the conservative QSPI-to-network-ready budget is 360 s, and a boot that "
    "needs a hand at any rung is exactly the FAIL this exists to catch")
A_VERSION_UNCHANGED = AssertSpec(
    "boot.same-gateware-version",
    "the same-version rule: a power cycle "
    "boots the QSPI image, so the VERSION CSR (0x004) must read back what the "
    "pre-snapshot read - a changed word means the golden-image fallback "
    "engaged (or a mid-campaign reflash), and every later verdict would be "
    "filed against the wrong gateware")
A_SHIELD_POSTURE = AssertSpec(
    "boot.rx-filter-posture-restored",
    "REGISTER_MAP.md RX filter decision order: promisc outranks even an "
    "explicit TCAM drop, so the stream shield only exists while promisc "
    "stays gated - the bare-metal healthy posture is MAC_CTRL 0x1B "
    "(TX/RX/all-multicast enabled, promiscuous absent). A boot that sets "
    "promiscuous mode has voided its own RX shield and starves the softcore "
    "under stream load")
A_STATE_RESTORED = AssertSpec(
    "state.restored-after-power-cycle",
    "Milan v1.2 5.3.8.1: 'The current format shall be saved in a "
    "non-volatile memory and restored after a power cycle.'  5.3.7.1 says "
    "the same for a Stream Output's format, 5.3.10.1 for the input channel "
    "mappings, 5.3.8.2/5.3.8.3 for the bound state and binding parameters "
    "and 5.3.7.6 for the presentation time offset - the clause is a SHALL "
    "and it is unconditional.  The verdict is nonetheless only DECIDABLE "
    "where a non-volatile store exists to hold it: on a build with no "
    "writable flash the revert is a KNOWN-PENDING gap of the build, and "
    "grading it FAIL every night would train the reader to ignore a red "
    "that never changes.  So a diff is FAIL where a store is present, "
    "KNOWN-PENDING where the store is provably absent (naming what must "
    "persist and where it would have to live), and SKIP where undecidable - "
    "and the day persistence lands the same assertion goes live untouched")
A_STATE_SELF_CONSISTENT = AssertSpec(
    "state.self-consistent-after-power-cycle",
    "Milan v1.2 5.3.8.1 first sentence: 'A Stream Input shall always be "
    "using a format that is one of the supported formats described by the "
    "formats list' (5.3.7.1 for a Stream Output) + IEEE 1722.1-2021 7.4.10 "
    "GET_STREAM_FORMAT.  This is what a build with NO non-volatile store "
    "still owes after a cold boot: every descriptor that was readable "
    "before the cycle answers again, with a well-formed format that the "
    "entity declares as supported.  It is the half of the persistence story "
    "that is gradable on this DUT today, so the cycle is never left with no "
    "verdict at all on its own state")
A_STATE_DEFAULTED = AssertSpec(
    "state.format-after-power-cycle",
    "info: what the dynamic formats actually READ BACK after the cycle, "
    "per descriptor, against the pre-snapshot.  A revert to the elaborated "
    "default is the expected shape of a build with no non-volatile store "
    "(SHAPE is static-from-elaboration by standing directive, but the "
    "per-stream CURRENT FORMAT is dynamic state under Milan 5.3.8.1), and "
    "recording it as a datum is what makes the gap measurable before it is "
    "fixed",
    severity="INFO")
A_COUNTERS_ZEROED = AssertSpec(
    "counters.zeroed-after-power-cycle",
    "IEEE 1722.1-2021 7.4.42: the counters are volatile state; a non-zero "
    "block straight after a power cycle is a restored-counter bug")


def _physical_switch_cycle_steps(dut, peer, fmt, ti, li, dli):
    """The switch power cycle: the partition, the re-join, and the proof
    that a bind still works across it."""
    S = []
    # ---- family 1: the switch cycle (partition + re-join) -----------------
    S.append(Step(
        "phys.switch-cycle.pre-snapshot", "physical", "phys_snapshot",
        {"family": "switch-cycle", "version_addr": VERSION_ADDR,
         "fmt_out_index": ti, "fmt_in_index": dli},
        asserts=(A_PHYS_SNAPSHOT,),
        clause="IEEE 1722.1-2021 Table 7-153 (the GM_CHANGED baseline) + the "
               "standing measure-before-and-after rule",
        note="GM identity on BOTH sides (ADPDU gptp_grandmaster_id), the "
             "AVB_INTERFACE counters, the licence word, the board uptime and "
             "the VERSION word - everything the retroactive verdicts need"))
    S.append(Step(
        "phys.switch-cycle.gm-partition", "physical", "switch_power_cycle",
        {"outlet_role": "switch", "family": "switch-cycle",
         "hold_s": 20, "link_budget_s": 240, "gptp_budget_s": 180,
         "settle_gap_s": 10, "gm_changes_max": 8,
         "clkv_stat_addr": CLKV_STAT_ADDR},
        needs_human=True,
        human_action="Power off the AVB switch (DN-1) at the powerstrip for "
                     "~20 s, then power it back on and wait for links and "
                     "gPTP to recover. AUTOMATED when the runner is "
                     "given --powerstrip-cmd and --switch-outlet (bench: "
                     "the powerstrip host, outlet 4).",
        asserts=(A_PARTITION_EXPECTED, A_GM_CHANGED_ADVANCES, A_GM_CONTINUITY,
                 A_PEER_GM_CHANGED, A_LINK_EVENT_SEEN, A_GM_ID_FOLLOWS,
                 A_ONE_GM_RESTORED, A_GM_NOT_FLAPPING, A_AS_CAPABLE_RESTORED,
                 A_TU_VALIDITY_RESTORED, A_NO_REBOOT, A_ADP_ALIVE),
        clause="802.1AS-2020 10.3 BMCA + IEEE 1722.1-2021 Table 7-153 "
               "GPTP_GM_CHANGED",
        note="the partition IS the GM loss and the re-join IS the GM change: "
             "priority1 is never touched (USER standing rule - recovery must "
             "be automatic).  Mid-partition nothing is verifiable from the "
             "controller host - it is inside the partition - so the "
             "own-island-GM claim is verified retroactively from the "
             "GM_CHANGED counters, and timeouts during the off-window are "
             "the expected condition, never failures.  WHICH counter tells "
             "the story is a TOPOLOGY question the runner answers from the "
             "pre-snapshot GM view, not a constant: the permanent GM owes "
             "CONTINUITY (zero delta, same id) and only a FOLLOWER owes an "
             "ADVANCE, so on this bench the DUT is graded for continuity "
             "and the peer - which does lose its GM - carries the advance"))
    S += _pair_steps("phys.switch-cycle.proof", "physical",
                     Endpoint(dut, ti), Endpoint(peer, li), fmt)
    return S


def _physical_dut_cycle_steps(dut, peer, fmt, ti, li, dli):
    """The DUT power cycle: what non-volatile state owes to survive it,
    and the proof that a bind still works after it."""
    S = []
    # ---- family 2: the DUT power cycle (the persistence story) ------------
    S.append(Step(
        "phys.dut-cycle.pre-snapshot", "physical", "phys_snapshot",
        {"family": "dut-cycle", "version_addr": VERSION_ADDR,
         "fmt_out_index": ti, "fmt_in_index": dli},
        asserts=(A_PHYS_SNAPSHOT,),
        clause="Milan v1.2 5.3.10.1 / 5.3.8.1 (what must survive the cycle "
               "is defined by what was set BEFORE it) + the standing "
               "measure-before-and-after rule"))
    S.append(Step(
        "phys.dut-cycle.power-cycle", "physical", "dut_power_cycle",
        {"outlet_role": "dut", "family": "dut-cycle",
         "off_s": 8, "net_budget_s": 360, "gptp_budget_s": 120,
         "settle_gap_s": 10, "version_addr": VERSION_ADDR,
         "clkv_stat_addr": CLKV_STAT_ADDR,
         "mac_ctrl_addr": MAC_CTRL_ADDR,
         "mac_ctrl": DUT_RX_FILTER_HEALTHY_CTRL,
         "fmt_out_index": ti, "fmt_in_index": dli},
        needs_human=True,
        human_action="Power-cycle the DUT at the outlet (off for at least "
                     "8 s - the SRAM gateware is lost, QSPI boots it back), "
                     "then wait for the network to come up with NO manual "
                     "intervention.  AUTOMATED when the runner is given "
                     "--powerstrip-cmd and --dut-outlet (bench: the "
                     "powerstrip host, outlet 0).",
        asserts=(A_ADP_ALIVE, A_BOOT_UNATTENDED, A_VERSION_UNCHANGED,
                 A_SHIELD_POSTURE, A_STATE_RESTORED, A_STATE_SELF_CONSISTENT,
                 A_STATE_DEFAULTED, A_COUNTERS_ZEROED,
                 A_ONE_GM_RESTORED, A_TU_VALIDITY_RESTORED),
        clause="Milan v1.2 5.3.10.1 / 5.3.8.1 / 5.3.7.6",
        note="the only test that can see the non-volatile requirements at "
             "all - and the zero-touch boot ladder (network, VERSION, shield "
             "posture, discovery, gPTP, clock validity) is the persistence story "
             "the flash rounds keep re-earning.  Milan 5.3.8.1 is a SHALL, "
             "so the restore assertion is never deleted; on a build with no "
             "writable flash it grades KNOWN-PENDING naming the missing "
             "store while the SELF-CONSISTENCY half stays a live SHALL"))
    S += _pair_steps("phys.dut-cycle.proof", "physical",
                     Endpoint(dut, ti), Endpoint(peer, li), fmt)
    return S


def plan_physical(dut: Device = ARTY, peer: Device = PEER) -> list:
    """The powerstrip-driven physical family - LAST, always, and never faked.

    USER AUTHORIZATION (2026-08-02): the bench powerstrip may drive OUT4 =
    the AVB switch ("DN-1") and OUT0 = the DUT (the AX cold-cycle precedent).
    Per-port CABLE PULLS stay needs_human in the torture area: a powerstrip
    cannot pull one cable, and simulating a port bounce by cutting the whole
    switch would assert something the cable-pull step does not claim.

    Two families:
      * switch-cycle - replaces the old gm-change and gm-loss human entries
        and adds the trunk-link bounce.  Cutting the switch IS the GM loss
        (each end station becomes its own island GM, verifiable only
        retroactively - the controller host is inside the partition), and the
        re-join IS the GM change (BMCA re-elects one GM with priority1
        untouched).  Both edges are real PHY link events on every port at
        once.
      * dut-cycle - the old power-cycle human entry: the persistence story,
        boot-to-healthy with zero manual intervention, plus the boot-posture
        checks (VERSION unchanged, shield posture, fabric validity/tu posture).

    Each family ends in a PROOF PAIR - a full set-format/bind/licence/unbind
    walk at the HIGHEST AAF indices (index 0 is the alias path and the least
    representative) - because "the bench recovered" is only a fact once a
    stream flows again.

    Ordering and safety are plan facts, not runner courtesy: the area is
    registered LAST in AREAS (a partition mid-matrix would pollute every
    later verdict), the two families are strictly serial, and the runner owes
    the bench-alive guarantee - on a failed recovery it retries the power-on
    ONCE with an extended wait, then STOPS the family and SKIPs the remaining
    physical steps naming the reason.  The campaign ends with the bench alive
    or loudly declared dead.

    Budgets (step args, so a bench overrides them without a source edit):
      * switch hold 20 s - an order of magnitude past the 802.1AS
        announce-receipt timeout (3 announce intervals = 3 s), so both
        islands provably re-elect their own GM before power returns;
      * switch recovery 240 s to reachability (the DN-1 must BOOT before any
        board is reachable through it - the 180 s floor plus switch boot
        margin), then 180 s more to ONE GM (BMCA + Pdelay asCapable + the
        servo, all automatic by standing rule; 120 s floor plus margin);
      * DUT off 8 s (a real drain - the SRAM gateware is LOST and QSPI boots
        it back, which is what makes it a true cold boot), a conservative
        360 s to a network-ready bare-metal image, then 120 s more for gPTP.
    """
    fmt = dut.formats[0] if dut.formats else None
    # the proof-pair indices: highest AAF (non-CRF) on each side - never 0
    tis = dut.talker_indices(include_crf=False)
    lis = peer.listener_indices(include_crf=False)
    ti = tis[-1] if tis else 0
    li = lis[-1] if lis else 0
    dlis = dut.listener_indices(include_crf=False)
    dli = dlis[-1] if dlis else 0
    return (_physical_switch_cycle_steps(dut, peer, fmt, ti, li, dli)
            + _physical_dut_cycle_steps(dut, peer, fmt, ti, li, dli))


# --------------------------------------------------------- release campaigns --
# Issue #396 round 2: retain the established minute counter-walk cadence as
# the qualification ceiling. Continuous event evidence is still required.
RELEASE_MAX_SOAK_INTERVAL_S = 60
# Issue #396 round 3: provisional ceiling; ratification uses #397 and #75.
RELEASE_RESTORE_BOUND_S = 30
# With relative error +/-R, h + R >= 0.25 can admit d=0 iff 2R >= 0.25.
RELEASE_TU_RESOLUTION_LIMIT_S = 0.25 / 2
# Issue #396 owner decision 2026-10-26 item 1: one continuous 24-hour window
# holds the soak and the audio-integrity run that rides inside it.
RELEASE_SOAK_DURATION_S = 24 * 60 * 60
# Item 2: 200 cycles. 150 cold cuts through the power strip, a third of them
# (50) inside a journal commit and the rest idle, and 50 soft resets.
RELEASE_POWER_PHASES = (("idle", 100), ("journal_commit", 50), ("soft_reset", 50))
# Item 3: every cycle restores the eight Milan v1.2 saved-state items of
# issue #70's inventory, and the binding that automatic restoration needs.
# Milan v1.2 states no non-volatile clause for the current configuration; it
# is in the inventory as issue #70 item 1.
RELEASE_PERSISTED_ITEMS = {
    "configuration": "issue #70 item 1: the currently set CONFIGURATION",
    "sampling_rate": "Milan v1.2 5.3.5.1: every AUDIO_UNIT",
    "stream_format": "Milan v1.2 5.3.7.1 / 5.3.8.1: every STREAM_OUTPUT and STREAM_INPUT",
    "presentation_time_offset": "Milan v1.2 5.3.7.6: every STREAM_OUTPUT",
    "channel_mappings": "Milan v1.2 5.3.9.1 / 5.3.10.1: both port directions",
    "clock_source": "Milan v1.2 5.3.11.1: every CLOCK_DOMAIN",
    "entity_names": "Milan v1.2 5.3.13: ENTITY entity_name and group_name",
    "object_names": "Milan v1.2 5.3.13: every other user-settable object_name",
    "stream_binding": "Milan v1.2 5.3.8.2 / 5.3.8.3 / 5.3.8.7: bound state, "
                      "binding parameters and started/stopped state",
}


@dataclass(frozen=True)
class ReleaseSettings:
    """Issue #396's release profile; smaller profiles are diagnostic only."""
    soak_duration_s: int = RELEASE_SOAK_DURATION_S
    soak_interval_s: int = 60
    power_cycles: int = 200
    idle_cycles: int = 100
    commit_cycles: int = 50
    reset_cycles: int = 50
    persisted_items: tuple[str, ...] = tuple(RELEASE_PERSISTED_ITEMS)
    # Provisional policy from #396 round 2; ratification uses #397 and #75.
    restore_bound_s: int = RELEASE_RESTORE_BOUND_S
    # Extra diagnostic observation never extends a pass deadline.
    boot_margin_s: int = 5
    # Caller attests that BOTH devices came from served descriptors.
    topology_explicit: bool = False
    # Existing phys.dut-cycle.power-cycle discharge hold, recorded separately.
    power_off_hold_s: int = 8
    # Issue #396 decision 2026-10-04 as amended 2026-10-26: the audio run
    # lasts the whole soak window, inside it.
    audio_duration_s: int = RELEASE_SOAK_DURATION_S
    # The same decision's "a few seconds either side" of every audio event:
    # the longest gap between the counter, SLIP and gPTP walks during the run.
    audio_context_s: int = 5

    def __post_init__(self) -> None:
        for name in ("soak_duration_s", "soak_interval_s", "power_cycles", "power_off_hold_s",
                     "idle_cycles", "commit_cycles", "reset_cycles", "restore_bound_s",
                     "boot_margin_s", "audio_duration_s", "audio_context_s"):
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if self.soak_interval_s > self.soak_duration_s:
            raise ValueError("soak interval exceeds duration")
        if self.audio_duration_s > self.soak_duration_s:
            raise ValueError("the audio run must fit inside the soak window")
        if self.audio_context_s > self.audio_duration_s:
            raise ValueError("audio context exceeds the audio run")
        if self.idle_cycles + self.commit_cycles + self.reset_cycles != self.power_cycles:
            raise ValueError("idle, commit and reset cycles must sum to power cycles")
        if type(self.topology_explicit) is not bool:
            raise ValueError("topology_explicit must be a boolean")
        items = self.persisted_items
        if (not isinstance(items, tuple) or not items
                or any(not isinstance(item, str) or not item.strip()
                       or item != item.strip() for item in items)
                or len(set(items)) != len(items)):
            raise ValueError("persisted items must be nonempty, unique names")


RELEASE_CLAUSE = "REQUIREMENTS.md REQ-VER-06; issue #396 owner/assignment decisions"
A_RELEASE_EVIDENCE = AssertSpec(
    "release.complete-evidence", RELEASE_CLAUSE + ": all required assertions "
    "need measured PASS records on the exact image; missing, NOT RUN, SKIP, INFO, "
    "KNOWN-PENDING, NEEDS-HUMAN and INSTRUMENT-SUSPECT cannot qualify a release")
SOAK_ASSERTS = (
    A_RELEASE_EVIDENCE,
    AssertSpec("soak.continuous-duration", RELEASE_CLAUSE +
               ": at least 86400 continuous seconds (24 h) after all pairs flow; "
               "no concatenating interrupted runs or counting setup time"),
    AssertSpec("soak.bound-both-directions", RELEASE_CLAUSE +
               ": keep the compatible AAF and CRF pairs bound and flowing "
               "in both directions throughout the observation window"),
    AssertSpec("soak.counter-walk", "Milan v1.2 Table 5.4 / Table 5.6; "
               "REQ-VER-06: read every declared input and output, CRF included, "
               "at baseline, each interval and the endpoint; validate masks "
               "and lock/start-stop invariants; no unexplained counter reset"),
    AssertSpec("soak.no-counter-errors", RELEASE_CLAUSE +
               "; Milan v1.2 5.3.8.10 Table 5.6; IEEE 1722-2016 4.4.4.6: "
               "zero SEQ_NUM_MISMATCH, STREAM_INTERRUPTED, LATE_TIMESTAMP and "
               "EARLY_TIMESTAMP growth on every Stream Input, CRF included; "
               "zero MEDIA_UNLOCKED growth of any cause, explained or not, "
               "outside a recorded planted event; an increment is excused only when "
               "both reads around it lie inside that input's planted window, so read "
               "the input at the window's start and end; each planted event excuses at "
               "most one increment per input; a decrease is a counter reset and fails; "
               "graded by check_release_soak_counters; missing reads or a missing "
               "planted-event log is NOT RUN"),
    AssertSpec("soak.mr-causes-and-hold", RELEASE_CLAUSE +
               "; IEEE 1722-2016 4.4.4.3; Milan v1.2 Annex B.1.2, Tables 5.4/5.6: "
               "every mr toggle and MEDIA_RESET increment needs a recorded "
               "media-clock-source change, CRF disruption, or received CRF mr toggle "
               "mapped to that stream's clock source; GM change alone fails; "
               "match causes within +/- observation_resolution_s of the toggle; "
               "hold each new value for at least 8 AVTPDUs of that stream; "
               "MEDIA_RESET counts observation intervals, not packets; "
               "missing packet, cause, counter or resolution evidence is NOT RUN; "
               "each cause excuses at most one toggle per stream; "
               "2 * observation_resolution_s must be less than the 1 s counter interval ceiling; "
               "capture must span [first read - 1 s - observation_resolution_s, last read]; "
               "a MEDIA_RESET decrease is a counter reset, not a wrap"),
    AssertSpec("soak.gptp-continuity", RELEASE_CLAUSE +
               "; Milan v1.2 4.2.6.2.4: coherent fabric "
               "publication reads and transition evidence prove no asCapable loss"),
    AssertSpec("soak.tu-within-holdover", RELEASE_CLAUSE +
               "; Milan v1.2 Annex B.1/B.1.1 / IEEE 1722-2016 4.4.4.7: "
               "each tu interval contains at least one recorded discontinuity: "
               "GM-identity edge, GM time-source change, or other detected gPTP discontinuity "
               "(including PHC settime/adjtime and fabric discontinuity); "
               "containment uses [observed_start - observation_resolution_s, clear); "
               "measure from the last recorded discontinuity before tu clears; "
               "it clears within 0.5 s plus "
               "the stated observation resolution; uncorrelated tu fails; "
               "resolution comes from wire capture and correlated event timestamps; "
               "it includes launch-to-capture latency and event-to-capture correlation error; "
               "after each GM change, clear + observation_resolution_s must be at least "
               "GM change + 0.25 s (Annex B.1.1 minimum); missing GM history is NOT RUN; clock validity "
               "implements 0.25-0.5 s; B.1's 5 s media-clock holdover is "
               "not a tu bound; "
               "periodic healthy samples alone cannot prove this; "
               "first discontinuity must be within observation_resolution_s of the rise; "
               "grade every GM change against the complete tu interval history; "
               "a GM change with no covering interval fails; "
               "true hold d is observed as h within +/- R, where R = observation_resolution_s; "
               "minimum accepts h + R >= 0.25 s, so d >= 0.25 s - 2 * R; "
               "require 2 * R < 0.25 s so an instant clear fails; "
               "upper bound requires h + R <= 0.5 s + R, equivalently h <= 0.5 s; "
               "resolution_limit_s is 0.125 s; "
               "coarser resolution is NOT RUN"),
    AssertSpec("soak.timestamp-margin", "docs/reference/REGISTER_MAP.md "
               "AVTPRX_TSD (0x6EC): record signed ns presentation margin for "
               "the last accepted STREAM_INPUT[0] PDU, with freshness evidence; "
               "never attribute this single-index register to other streams"),
    AssertSpec("soak.uptime-monotonic", RELEASE_CLAUSE +
               ": DUT uptime advances monotonically; reboot or unavailable "
               "uptime evidence cannot pass the continuous soak"),
)
POWER_ASSERTS = (
    A_RELEASE_EVIDENCE,
    AssertSpec("power.cycle-count-and-phase", RELEASE_CLAUSE +
               "; Milan v1.2 5.5.1.4 (a power cycle or a simple reset): "
               "200 cycles, 150 confirmed cold cuts (100 idle, 50 inside a "
               "journal commit window) and 50 soft resets with power held on; "
               "a reset never counts as a cold cut and a cut never as a reset; "
               "preserve each cycle's command timestamp and its cut-phase or "
               "reset evidence"),
    AssertSpec("power.state-restored", RELEASE_CLAUSE +
               "; Milan v1.2 5.3.5.1, 5.3.7.1/5.3.7.6, "
               "5.3.8.1/5.3.8.2/5.3.8.3/5.3.8.7, 5.3.9.1, 5.3.10.1, "
               "5.3.11.1, 5.3.13; issue #70's eight-item inventory: every "
               "cycle, cut or reset, restores the eight Milan items and the "
               "binding; set each item away from its default before the cycle "
               "so a revert is visible; compare each against the pre-cycle snapshot; "
               "commit cuts must restore a complete old or new committed "
               "snapshot, never mixed state; graded by check_release_state_restored; "
               "a pre-cycle value equal to its default or a missing readback is NOT RUN; "
               "so is a commit cut whose pending value equals its default, or whose cut "
               "instant lies outside its recorded commit window"),
    AssertSpec("power.adp-valid-time", RELEASE_CLAUSE +
               "; IEEE 1722.1-2021 6.2.2.5, 6.2.4/6.2.5; Milan v1.2 5.6.2/5.6.3: "
               "first post-cut ENTITY_AVAILABLE arrives within the advertised "
               "valid_time measured from T0, the host-timestamped power-strip "
               "ON command; decode the captured pre-cut PDU in two-second "
               "units and require valid_time=10 (20 s); power_off_hold_s and "
               "pre-cut advertisement age are provenance, not charged to "
               "this window; missing capture or a missed deadline fails; "
               "for a soft reset T0 is the host-timestamped reset command"),
    AssertSpec("power.automatic-restore-bound", RELEASE_CLAUSE +
               "; Milan v1.2 5.5.1.4 / 5.5.2.6: from T0 to first valid AVTP "
               "PDU of EACH persisted binding in both directions, including "
               "CRF, must be at most restore_bound_s; provisional 30 s, "
               "ratified by the manager using #397 boot-to-entity-enabled "
               "and #75 restart measurements; controller repair cannot count"),
    AssertSpec("power.rebind-bound", RELEASE_CLAUSE +
               "; Milan v1.2 5.5.2.4; issue #75: an additional per-cycle "
               "controller reconnect after automatic restoration succeeds; "
               "CONNECT_RX success to first valid AVTP PDU below 1 second; "
               "both restoration and reconnect must pass"),
    AssertSpec("power.single-boot", RELEASE_CLAUSE +
               "; issue #366: complete UART/reset observation from T0 through "
               "the next cycle or campaign end, at least boot_observation_s, "
               "records exactly one BIOS pass and no "
               "additional restart, after a cut and after a reset; check_release_boot "
               "refuses the repeated BIOS pass even if the second pass restores streaming"),
    AssertSpec("power.counter-walk", "Milan v1.2 Table 5.4 / Table 5.6; "
               "REQ-VER-06: snapshot every declared stream index, both "
               "directions and CRF, before and after every cycle; validate "
               "masks, supported formats, lock/start-stop invariants and flow"),
)
#: Issue #396 audio signal design of 2026-10-04 and REQ-VER-06: the audio
#: counter run shares the 24-hour soak window, by the 2026-10-26 owner decisions.
AUDIO_RELEASE_CLAUSE = RELEASE_CLAUSE + "; issue #396 audio signal design 2026-10-04"
AUDIO_RELEASE_ASSERTS = (
    A_RELEASE_EVIDENCE,
    AssertSpec("audio.inside-soak-window", AUDIO_RELEASE_CLAUSE +
               ": starts after soak.continuous binds every pair and starts timing, "
               "ends at or before the soak endpoint and lasts at least 86400 "
               "continuous seconds of qualified, observed capture, so it runs past them by "
               "its guards and any logged loss; a shorter run or one outside the window "
               "cannot qualify"),
    AssertSpec("audio.counter-every-digital-path", AUDIO_RELEASE_CLAUSE +
               "; IEEE 1722-2016 7.3.5: every channel of every bound AAF stream, in "
               "both directions, carries the bit-exact counter: the DUT talker to the "
               "reference peer to an external digital capture, the reference peer to "
               "the DUT listener to the DUT's TDM output and the direct TDM capture "
               "(#451), and the DUT's TDM loop"),
    AssertSpec("audio.counter-classified", AUDIO_RELEASE_CLAUSE +
               ": grade_audio_counter_capture classifies every discontinuity at its "
               "sample as n dropped, n repeated, n samples of silence (replaced or "
               "inserted), a bit-flip mask or a channel swap; the counter repeats only "
               "after 2^43 samples, so every slip is sized exactly; a slip of whole "
               "2048-sample blocks is located within 63 samples (located_within); the "
               "tag's integrity decides first: only a reciprocal exchange is a swap, any "
               "other foreign or corrupted channel number is corruption; a word equal to "
               "a neighbouring received word is a repeat; an excursion of two or more "
               "words with one constant XOR mask is one corruption at any length, beside "
               "any one-word event or slip; on every channel the slips reported sum to "
               "the shift the bytes decode, and a window no reading balances is one "
               "unresolved event; a slip and a corruption in one window are both graded "
               "in either order, except on and just before a planted arm as "
               "counter_limits states, and patterns the bytes cannot tell apart follow "
               "counter_limits, the planted-arm log deciding at a logged arm; a "
               "channel swapped from the first frame is a swap, its counters still "
               "tracked; at either end of a capture, words that differ from their track "
               "only in the code bit are one unresolved event, never an exact class; "
               "the verdict states its qualified interval, from 63 samples after the "
               "last channel's acquisition to 63 samples before the capture's end, and "
               "nothing outside it is proved clean"),
    AssertSpec("audio.planted-arms-found", AUDIO_RELEASE_CLAUSE +
               ": the source plants a drop, a repeat and a bit flip at logged capture "
               "indices at the start and at the end of the run, in its first and its "
               "last tenth and inside the qualified interval; each is found with its "
               "class and its size or mask; where the capture's bytes allow a reading "
               "that places an arm, the arm's log decides, never at the cost of another "
               "DUT event; a corruption on a planted arm's sample or just before it can "
               "still leave the arm missed, as counter_limits states; a missed arm, an "
               "arm outside the qualified interval, or arms that do not run at both ends, "
               "voids the run as NOT RUN, which blocks the release"),
    AssertSpec("audio.capture-losses-apart", AUDIO_RELEASE_CLAUSE +
               ": capture-side losses logged by the capture tool are attributed to the "
               "capture and reported apart, never counted against the DUT, and only "
               "when every counter channel shows the slip; a logged loss the capture does "
               "not show, or one outside the qualified interval, is NOT RUN; a loss still "
               "advances the acquisition index and both clocks, but it is not observed "
               "time"),
    AssertSpec("audio.event-record", AUDIO_RELEASE_CLAUSE +
               "; Milan v1.2 5.3.8.10 Table 5.6: each event records its wall and gPTP "
               "times, capture and acquisition indices, expected and received words and "
               "class, with walks of every stream's counters and the CRF sink's, the "
               "DUT's SLIP_LB and SLIP_TDM words and the gPTP state within "
               "audio_context_s on each side; times are interpolated between the capture "
               "tool's anchors, never extrapolated, and gPTP time never across a recorded "
               "discontinuity; an unsupported time is null with its reason"),
    AssertSpec("audio.analog-sine-pair", AUDIO_RELEASE_CLAUSE +
               ": 997 Hz and 9,973 Hz on another channel pair through the analog path, "
               "graded per block by THD+N and the sample-exact predictor residual; no "
               "limit is decided for either, so this assertion is NOT RUN until a "
               "recorded decision sets them"),
    AssertSpec("audio.zero-dut-glitches", AUDIO_RELEASE_CLAUSE +
               ": zero DUT-attributed events over the run on every bound channel, in "
               "both directions, with every planted arm found, over a qualified interval "
               "of at least 86400 observed seconds; a shorter qualified interval is NOT RUN"),
)
#: Each release repeat operation and the assertions it may never drop.
RELEASE_REQUIRED_ASSERTS = {
    "release_soak": frozenset(spec.name for spec in SOAK_ASSERTS),
    "release_audio_integrity": frozenset(spec.name for spec in AUDIO_RELEASE_ASSERTS),
    "release_power_cycles": frozenset(spec.name for spec in POWER_ASSERTS),
}
RELEASE_CONTROL_OP = "release_negative_control"
#: Acceptance 4's negative controls, each in the area whose assertion it fails.
RELEASE_CONTROLS = {
    "power": ("power.control.first-boot-restart", "power.control.persistence-disabled"),
    "audio": ("audio.control.planted-drop",),
}
A_RELEASE_CONTROL = AssertSpec(
    "release.control-fails-as-expected", RELEASE_CLAUSE + "; issue #396 acceptance 4: a "
    "negative control passes only when its expected assertion FAILs on the known "
    "defect; a PASS, SKIP or NOT RUN of that assertion means the gate cannot see it")


def _release_counter_targets(dut: Device, peer: Device) -> list[dict]:
    """All readable stream counters, independently of simultaneous bindings."""
    targets = []
    for device in (dut, peer):
        for descriptor, indices, crf_index in (
                ("stream_output", device.talker_indices(), device.crf_out),
                ("stream_input", device.listener_indices(), device.crf_in)):
            targets.extend({"entity": device.entity_id, "descriptor": descriptor,
                            "index": index, "crf": index == crf_index}
                           for index in indices)
    return targets


def _release_pairs(dut: Device, peer: Device) -> list[dict]:
    """Bind each reachable sink once; multicast sources where shapes differ."""
    if not dut.entity_id or not peer.entity_id or dut.entity_id == peer.entity_id:
        raise ValueError("release campaigns require a distinct DUT and peer")
    for device in (dut, peer):
        if (device.crf_out in device.talker_indices(False)
                or device.crf_in in device.listener_indices(False)):
            raise ValueError("release AAF indices must not include a CRF index")
    pairs = []
    for talker, listener in ((dut, peer), (peer, dut)):
        outputs = talker.talker_indices(include_crf=False)
        inputs = listener.listener_indices(include_crf=False)
        if not outputs or not inputs:
            raise ValueError("release campaigns require AAF in both directions")
        if talker.crf_out is None or listener.crf_in is None:
            raise ValueError("release campaigns require CRF in both directions")
        for index, sink in enumerate(inputs):
            pairs.append(_multi_pair(Endpoint(talker, outputs[index % len(outputs)]),
                                     Endpoint(listener, sink), None))
        pairs.append(_multi_pair(Endpoint(talker, talker.crf_out),
                                 Endpoint(listener, listener.crf_in), None))
    return pairs


def _release_args(dut: Device, peer: Device) -> dict:
    """Inputs a bench executor must resolve before any repeat operation."""
    return {"pairs": _release_pairs(dut, peer),
            "counter_targets": _release_counter_targets(dut, peer),
            "format_policy": "read talker live format; match listener before bind",
            "evidence": ["image_hashes", "manifest", "csr_map", "verdict_jsonl",
                         "uart_transcript", "wire_captures", "controller_log",
                         "timestamped_snapshots", "temperature_log"],
            "unsupported_operation": "refuse; never skip or claim PASS"}


def _release_profile_eligible(settings: ReleaseSettings) -> bool:
    """Common plan prerequisites; this judges no measured hardware evidence."""
    return (settings.topology_explicit
            and set(RELEASE_PERSISTED_ITEMS) <= set(settings.persisted_items)
            and settings.restore_bound_s <= RELEASE_RESTORE_BOUND_S
            and settings.soak_interval_s <= RELEASE_MAX_SOAK_INTERVAL_S)


def _release_topology_explicit(dut_spec: str | None, peer_spec: str | None) -> bool:
    """Require identity and complete AAF/CRF shapes instead of fixture defaults."""
    for spec in (dut_spec, peer_spec):
        keys = {part.split("=", 1)[0].strip() for part in (spec or "").split(",")
                if "=" in part and part.split("=", 1)[1].strip()}
        if (not {"entity", "mac", "crf_in", "crf_out"} <= keys
                or not {"talkers", "talker_index_set"} & keys
                or not {"listeners", "listener_index_set"} & keys):
            return False
    return True


def check_release_boot(boot_passes: int | None, restarts: int | None, *,
                       capture_complete: bool) -> tuple[str, dict]:
    """L3 #396/#366 oracle over a complete, per-cycle UART/reset observation."""
    if (capture_complete is not True or type(boot_passes) is not int
            or type(restarts) is not int or boot_passes < 0 or restarts < 0):
        return "SKIP", {"why": "complete UART/reset observation required"}
    return ("PASS" if boot_passes == 1 and restarts == 0 else "FAIL",
            {"boot_passes": boot_passes, "restarts": restarts,
             "why": "exactly one BIOS pass and no additional restart per cold cut"})


def _release_finite(value: object) -> bool:
    import math
    return type(value) in (int, float) and math.isfinite(value)


#: Issue #396 owner decision 2026-10-26 item 3: these Table 5.6 counters may
#: not grow at all over the soak.
RELEASE_ZERO_GROWTH_COUNTERS = ("SEQ_NUM_MISMATCH", "STREAM_INTERRUPTED",
                                "LATE_TIMESTAMP", "EARLY_TIMESTAMP")


def _release_counter_reads_valid(reads: list, names: Sequence[str]) -> bool:
    for read in reads:
        if (not isinstance(read, dict) or not isinstance(read.get("target"), str)
                or not read["target"] or not _release_finite(read.get("timestamp_s"))
                or not isinstance(read.get("values"), dict)):
            return False
        for name in names:
            value = read["values"].get(name)
            if type(value) is not int or not 0 <= value < 2**32:
                return False
    return True


def _release_planted_valid(planted: list) -> bool:
    for event in planted:
        window = event.get("window_s") if isinstance(event, dict) else None
        if (not isinstance(event, dict) or not isinstance(event.get("target"), str)
                or not event["target"] or not isinstance(event.get("kind"), str)
                or not event["kind"] or not isinstance(window, (tuple, list)) or len(window) != 2
                or any(not _release_finite(value) for value in window) or window[1] < window[0]):
            return False
    return True


def check_release_soak_counters(reads: list[dict] | None, planted_events: list[dict] | None, *,
                                targets: Sequence[str] | None,
                                capture_complete: bool) -> tuple[str, dict]:
    """L3 #396 item 3 over the whole soak window, for every Stream Input.

    Milan v1.2 5.3.8.10 Table 5.6. `reads` carry target, timestamp_s and
    values {name: count}, with a baseline and an endpoint for every name in
    `targets`, CRF inputs included. `planted_events` is the runner's complete
    log of deliberately planted disturbances, each with its target, kind and
    recorded window_s; an empty list attests that none was planted, None is
    missing evidence. A MEDIA_UNLOCKED increment between two reads is excused
    only by a distinct planted event of that input whose window holds both
    reads, so the increment is confined to the planted samples; an increment
    in a read interval that only meets a window stays unexcused, whatever
    else explains it. A decrease of any counter is a reset: Table 5.6 zeroes
    the block on a not-bound to bound transition, so the soak was interrupted.
    """
    names = RELEASE_ZERO_GROWTH_COUNTERS + ("MEDIA_UNLOCKED",)
    detail = {"zero_growth": list(RELEASE_ZERO_GROWTH_COUNTERS),
              "planted_only": "MEDIA_UNLOCKED"}
    if (capture_complete is not True or reads is None or planted_events is None
            or not targets or any(not isinstance(t, str) or not t for t in targets)):
        return "NOT RUN", dict(detail, why="complete reads, targets and planted-event log required")
    if not _release_counter_reads_valid(reads, names) or not _release_planted_valid(planted_events):
        return "NOT RUN", dict(detail, why="invalid counter reads or planted-event log")
    planted = {}
    for event in sorted(planted_events, key=lambda e: e["window_s"][0]):
        planted.setdefault(event["target"], []).append(event)
    used = 0
    for target in targets:
        series = [read for read in reads if read["target"] == target]
        if len(series) < 2:
            return "NOT RUN", dict(detail, target=target, why="baseline and endpoint reads required")
        unused = list(planted.get(target, []))
        for before, after in zip(series, series[1:]):
            interval = [before["timestamp_s"], after["timestamp_s"]]
            if not interval[0] < interval[1]:
                return "NOT RUN", dict(detail, target=target, why="ordered reads required")
            for name in names:
                delta = after["values"][name] - before["values"][name]
                if delta < 0:
                    return "FAIL", dict(detail, target=target, counter=name, interval_s=interval,
                                        why="counter decreased: a reset interrupted the soak")
                if delta and name != "MEDIA_UNLOCKED":
                    return "FAIL", dict(detail, target=target, counter=name, delta=delta,
                                        interval_s=interval, why="zero-growth counter grew")
            delta = after["values"]["MEDIA_UNLOCKED"] - before["values"]["MEDIA_UNLOCKED"]
            matches = [event for event in unused
                       if event["window_s"][0] <= interval[0] and interval[1] <= event["window_s"][1]]
            if delta > len(matches):
                return "FAIL", dict(detail, target=target, counter="MEDIA_UNLOCKED", delta=delta,
                                    interval_s=interval, why="MEDIA_UNLOCKED outside a planted event")
            for event in matches[:delta]:
                unused.remove(event)
            used += delta
    return "PASS", dict(detail, targets=len(targets), planted_unlocks=used)


@dataclass(frozen=True)
class ReleaseCommitCut:
    """A journal-commit cut's evidence for check_release_state_restored.

    `pending` is the snapshot being committed, `window_s` the commit's
    [start, end) and `cut_s` the cut instant, both on the host monotonic
    clock of the cycle's T0.
    """
    pending: dict
    window_s: tuple
    cut_s: float


def _release_cut_refusal(cut: ReleaseCommitCut | None) -> str | None:
    """Why a commit cut's phase evidence cannot place the cut in the commit."""
    window = None if cut is None else cut.window_s
    if (not isinstance(window, (tuple, list)) or len(window) != 2
            or not all(_release_finite(value) for value in (*window, cut.cut_s)) or window[1] <= window[0]):
        return "cut-phase evidence required: the commit window and the cut instant"
    if not window[0] <= cut.cut_s < window[1]:
        return "the cut hit no journal commit"
    return None


def check_release_state_restored(pre: dict | None, post: dict | None, defaults: dict | None, *,
                                 items: Sequence[str], phase: str,
                                 committed: dict | ReleaseCommitCut | None = None) -> tuple[str, dict]:
    """L3 #396 item 3: one cycle's readback of the persisted inventory.

    `pre` is the committed snapshot before the cycle and `post` the readback
    after it, as {item: value}; `defaults` holds the image's power-on values.
    Every pre-cycle value must differ from its default, or a build that
    restores nothing reads back as restored (issue #70's vacuity trap). Idle
    cuts and soft resets restore `pre` exactly, and any `committed` given to
    them is ignored. A journal_commit cut lands while the pending snapshot is
    being written: every pending value must differ from its default too, the
    readback must be all of `pre` or all of the pending snapshot, never a mix,
    and a PASS needs a ReleaseCommitCut placing the cut inside the commit
    window; a bare pending dict can only FAIL or be NOT RUN.
    """
    detail = {"phase": phase, "items": list(items)}
    if phase not in {name for name, _ in RELEASE_POWER_PHASES} or not items:
        return "NOT RUN", dict(detail, why="known phase and nonempty inventory required")
    cut = committed if isinstance(committed, ReleaseCommitCut) else None
    committed = cut.pending if cut is not None else committed
    snapshots = [pre, post, defaults] + ([committed] if phase == "journal_commit" else [])
    if any(not isinstance(snap, dict) or any(item not in snap for item in items)
           for snap in snapshots):
        return "NOT RUN", dict(detail, why="complete pre-cycle, readback and default snapshots required")
    at_default = [item for item in items if pre[item] == defaults[item]]
    if at_default:
        return "NOT RUN", dict(detail, at_default=at_default,
                               why="pre-cycle value equals its default, so a revert is invisible")
    if phase == "journal_commit":
        return _release_commit_restored(pre, post, defaults, committed, cut, detail)
    differs = [item for item in items if post[item] != pre[item]]
    if differs:
        return "FAIL", dict(detail, differs=differs,
                            reverted=[item for item in differs if post[item] == defaults[item]],
                            why="persisted state not restored")
    return "PASS", detail


def _release_commit_restored(pre: dict, post: dict, defaults: dict, committed: dict,
                             cut: ReleaseCommitCut | None, detail: dict) -> tuple[str, dict]:
    """The journal_commit half of check_release_state_restored."""
    items = detail["items"]
    pending_at_default = [item for item in items if committed[item] == defaults[item]]
    if pending_at_default:
        return "NOT RUN", dict(detail, pending_at_default=pending_at_default,
                               why="pending value equals its default, so a fallback is invisible")
    if all(committed[item] == pre[item] for item in items):
        return "NOT RUN", dict(detail, why="the interrupted commit changes nothing")
    if all(post[item] == pre[item] for item in items):
        restored = "old committed snapshot"
    elif all(post[item] == committed[item] for item in items):
        restored = "new committed snapshot"
    else:
        return "FAIL", dict(detail, why="mixed or partial state after a commit cut",
                            differs=[item for item in items if post[item] != pre[item]])
    refusal = _release_cut_refusal(cut)
    if refusal:
        return "NOT RUN", dict(detail, restored=restored, why=refusal)
    return "PASS", dict(detail, restored=restored)


# ------------------------------------------------- the audio-integrity counter --
#: Issue #396 audio signal design of 2026-10-04, REQ-VER-06: a bit-exact
#: counter on every digital path. Each S32 word carries a 24-bit sample in
#: bits 31:8 with bits 7:0 zero, the layout of the #451 and #629 captures.
#: Sample bits 15:12 hold the channel number, index + 1 so that no valid word
#: is zero and silence stays distinct. Bits 11:1 hold the sample position
#: modulo 2048, and bit 0 one bit of a block code: sample n carries bit
#: n mod 32 of the code of block n div 2048, so 32 consecutive samples of one
#: block give its number. The counter repeats only after 2^43 samples, about
#: 530 days at 192 kHz, the highest Milan v1.2 6.2 (Table 6.1) rate, where a
#: 24-hour run is 1.66e10 samples. Eight channels peak near -47 dBFS, and the
#: 2048-sample wrap is a 23.4 Hz sawtooth at 48 kHz: a low-level bench signal.
AUDIO_POSITION_BITS = 11
AUDIO_BLOCK_FRAMES = 1 << AUDIO_POSITION_BITS
AUDIO_CODE_BITS = 32
AUDIO_PERIOD_FRAMES = AUDIO_BLOCK_FRAMES << AUDIO_CODE_BITS
#: Block b's code is b * 0x9E3779B1 modulo 2^32, a bijection under which
#: nearby blocks differ in many bits. A slip of whole blocks leaves bits 11:1
#: unchanged, so the code bit is all that shows it.
AUDIO_CODE_MULTIPLIER = 0x9E3779B1
AUDIO_CODE_INVERSE = pow(AUDIO_CODE_MULTIPLIER, -1, 1 << AUDIO_CODE_BITS)
AUDIO_PAD_BITS = 8
AUDIO_TAG_SHIFT = AUDIO_PAD_BITS + 12
AUDIO_TAG_MAX = 15
#: Bits no valid counter word sets: the sample's bits 23:16 and the pad.
AUDIO_ZERO_MASK = 0xFF0000FF
#: Any 63 consecutive samples hold one aligned 32-sample group of one block,
#: so 64 clean samples fix a channel's absolute position, and a slip of whole
#: blocks shows within 63 samples.
AUDIO_CONFIRM_FRAMES = 64
#: REQ-VER-06, issue #396: a slip of whole blocks shows only through the code
#: bit, so a verdict qualifies a sample only when the 63 samples before it lie
#: on the acquired track and the 63 after it were captured. Nearer either end
#: of a capture an unseen slip cannot be excluded, so those samples are never
#: proved clean.
AUDIO_GUARD_FRAMES = AUDIO_CONFIRM_FRAMES - 1
#: Words one unresolved stretch may store before it is graded in pieces; a
#: channel that has not acquired the counter by then voids the run at once.
AUDIO_WINDOW_WORDS = 1 << 16
#: `unresolved` is a stretch at either end of a capture that differs from the
#: track only in the code bit: a slip of whole blocks or a code-bit corruption,
#: which the capture cannot tell apart; or a window no balanced reading explains.
AUDIO_CLASSES = ("dropped", "repeated", "silence", "bit-flip", "swap", "unresolved")
AUDIO_END_REASON = "the capture ended"
AUDIO_BOUND_REASON = "more than 65536 words without 64 clean samples"
#: Issue #396 REQ-VER-06: a window whose reported slips would not sum to the shift its bytes decode.
AUDIO_UNBALANCED_REASON = "an unclassified corruption: no reading's slips sum to the shift the bytes decode"
#: The source plants these at the start and at the end of every run, inside
#: the qualified interval. Mask 0x100 flips the code bit alone, so the arm
#: never equals a neighbouring sample, whose position bits differ.
AUDIO_PLANTED_ARMS = ({"class": "dropped", "n": 3}, {"class": "repeated", "n": 2},
                      {"class": "bit-flip", "mask": 0x00000100})
#: "At the start" is the first tenth of the capture, "at the end" the last.
AUDIO_ARM_EDGE_DIVISOR = 10
#: Frames compared at once on the per-channel fast path.
AUDIO_FAST_BLOCK = AUDIO_BLOCK_FRAMES
#: The plan's statement of what a counter verdict proves; required_s comes from the settings.
AUDIO_QUALIFICATION = {
    "interval": "from 63 samples after the last counter channel's acquisition to 63 samples before "
                "the capture's end",
    "guard_frames": AUDIO_GUARD_FRAMES,
    "observed_only": "logged capture losses are not observed time",
    "capture_rule": "capture past the required duration at both ends by the guards and by any "
                    "logged loss, inside the soak window",
    "verdict": "every verdict states the interval; PASS needs at least required_s observed "
               "seconds in it; a shorter interval is NOT RUN"}
#: Patterns the counter cannot tell apart, as the plan states them (TESTING.md 6d).
AUDIO_COUNTER_LIMITS = (
    "every slip is sized exactly from the decoded position",
    "on every channel the slips a reading reports sum to the shift its closing samples decode; a "
    "reading that does not is never taken, and a window no reading balances is one unresolved event "
    "at its first sample, never a slip that did not happen",
    "a slip of whole 2048-sample blocks is found within 63 samples and carries located_within, "
    "the samples it may have happened at: back over the words that fit both tracks, a corrupted "
    "word included where the tracks coincide, and on to the first word that shows it",
    "inside a cluster of events less than 64 samples apart, the slips between them take the "
    "smallest sizes the positions allow, and a code bit those sizes leave unexplained reads as a "
    "code-bit corruption; the cluster's total is exact",
    "a code-bit corruption less than 64 samples before a slip of whole blocks may make its word "
    "the new track's; when every word between them fits both tracks, the bytes are that slip "
    "alone at the corrupted word, and read so",
    "where a slip of whole blocks and a code-bit corruption less than 64 samples apart give the "
    "same bytes in either order, because the corrupted word is the other track's and only one "
    "word between them differs, the corruption reads first and the slip is located after it",
    "a slip followed, within the words that fit both tracks, by a slip of whole blocks gives the "
    "bytes of one slip of their sum, and reads so",
    "at a logged planted arm the arm log decides between readings with the same bytes, taking "
    "another only when it has fewer DUT events, or as many and more arms found, so a DUT slip "
    "that undoes a slip arm at the next sample reads as the arm and that slip; a DUT slip at a "
    "planted slip arm's own sample is one slip of their sum, so unless the DUT slip is whole "
    "blocks the arm is missed and the run is void",
    "a one-word corruption on a planted slip arm's own sample or the next one may read first, "
    "judged against the offset before the slip, with the slip placed after it within the arm "
    "tolerance: the bytes are the same either way",
    "beside a planted flip arm, on its channel, under a slip of whole blocks, the arm's word is the "
    "other track's where the two differ, so the bytes may be that slip on the other side of the arm "
    "with the arm's code bit one sample over; within the tolerance the arm is found, and "
    "located_within bounds the slip of that reading",
    "a corrupted word on a planted slip arm's own sample or the one before it, that is its "
    "channel's word at another position at most half a block (1024 samples) from the old or the "
    "new track's, reads as a slip to that position and on to the arm's track: the arm is missed "
    "and the run is void",
    "a corruption of a planted flip arm's own word, on its channel, combines with the arm's mask, "
    "and one beside it under the arm's own mask makes a two-word excursion of that mask: either "
    "way the arm is missed and the run is void",
    "a word equal to a neighbouring received word is a repeat",
    "an excursion of two or more words with one constant XOR mask is one corruption at any "
    "length, even where slips would produce the same words; a one-word event beside it, "
    "adjacent or not, a slip before it and a slip at its return are graded on their own, and a "
    "two-word excursion under two masks that no single offset explains is two one-word "
    "corruptions; a word on the old track is its return",
    "a constant-mask corruption that a slip interrupts, or whose words one offset explains up to "
    "a slip at its return, reads as the slips its words show",
    "a slip pair whose total is whole blocks and whose displaced words share one XOR mask reads "
    "as that bit-flip and a slip of whole blocks beside it, the corruption judged against "
    "whichever track gives its mask fewer bits set",
    "a stretch longer than 65536 words without 64 clean samples is graded in pieces; a "
    "constant-mask corruption stays a bit-flip with that mask in each",
    "at either end of a capture, words that differ from their track only in the code bit are one "
    "unresolved event: a slip of whole blocks or a code-bit corruption, with located_within for "
    "the slip",
    "any other slip that 64 clean samples cannot confirm, in a capture's last samples or inside a "
    "constant-mask excursion the capture ends in, carries unresolved",
    "nothing outside the qualified interval is proved clean")


def _audio_code(block: int) -> int:
    return (block * AUDIO_CODE_MULTIPLIER) % (1 << AUDIO_CODE_BITS)


def audio_counter_word(tag: int, position: int) -> int:
    """The S32 word carrying channel number `tag` at absolute sample `position`."""
    block, offset = divmod(position % AUDIO_PERIOD_FRAMES, AUDIO_BLOCK_FRAMES)
    bit = (_audio_code(block) >> (offset % AUDIO_CODE_BITS)) & 1
    return ((tag << 12) | (offset << 1) | bit) << AUDIO_PAD_BITS


def _audio_fields(word: int) -> tuple[int, int]:
    """(channel number, position modulo 2048) of a counter word."""
    return (word >> AUDIO_TAG_SHIFT) & 0xF, (word >> (AUDIO_PAD_BITS + 1)) % AUDIO_BLOCK_FRAMES


def _audio_signed(delta: int) -> int:
    """`delta` folded into one counter period around zero."""
    half = AUDIO_PERIOD_FRAMES // 2
    return (delta + half) % AUDIO_PERIOD_FRAMES - half


@lru_cache(maxsize=16)
def _audio_tag_base(tag: int) -> int:
    """One block of the channel's words, code bits clear, over native-order bytes."""
    from array import array
    words = array("I", [((tag << 12) | (offset << 1)) << AUDIO_PAD_BITS
                        for offset in range(AUDIO_BLOCK_FRAMES)])
    return int.from_bytes(words.tobytes(), "little")


@lru_cache(maxsize=64)
def _audio_code_pattern(block: int) -> int:
    """Block `block`'s code bits, each in its word, over native-order bytes."""
    from array import array
    code = _audio_code(block)
    group = array("I", [((code >> bit) & 1) << AUDIO_PAD_BITS for bit in range(AUDIO_CODE_BITS)])
    return int.from_bytes(group.tobytes() * (AUDIO_BLOCK_FRAMES // AUDIO_CODE_BITS), "little")


@lru_cache(maxsize=256)
def _audio_block_bytes(tag: int, block: int) -> bytes:
    """One block of channel `tag`'s counter words in native byte order."""
    return (_audio_tag_base(tag) ^ _audio_code_pattern(block)).to_bytes(4 * AUDIO_BLOCK_FRAMES, "little")


def _audio_expected_bytes(tag: int, position: int, count: int) -> bytes:
    """`count` consecutive words of channel `tag` from `position`, native order."""
    parts = []
    while count > 0:
        block, offset = divmod(position % AUDIO_PERIOD_FRAMES, AUDIO_BLOCK_FRAMES)
        take = min(count, AUDIO_BLOCK_FRAMES - offset)
        parts.append(_audio_block_bytes(tag, block)[4 * offset:4 * (offset + take)])
        position, count = position + take, count - take
    return b"".join(parts)


def _audio_decode(words: Sequence[int]) -> int | None:
    """Absolute position of words[0] when the 64 words are consecutive samples."""
    tag, first = _audio_fields(words[0])
    lead = -first % AUDIO_CODE_BITS
    code = 0
    for bit in range(AUDIO_CODE_BITS):
        code |= ((words[lead + bit] >> AUDIO_PAD_BITS) & 1) << bit
    block = code * AUDIO_CODE_INVERSE % (1 << AUDIO_CODE_BITS)
    position = block * AUDIO_BLOCK_FRAMES + (first + lead) % AUDIO_BLOCK_FRAMES - lead
    if all(word == audio_counter_word(tag, position + k) for k, word in enumerate(words)):
        return position % AUDIO_PERIOD_FRAMES
    return None


def synthesize_counter_capture(frames: int, channels: int, *, byteorder: str = "big",
                               start_counter: int = 0, events: Sequence[dict] = ()) -> bytes:
    """An interleaved S32 capture of the counter signal, for offline controls.

    Events are placed in capture-index terms: drop and repeat move the source
    position by n from `index` on; silence zeroes n frames from `index`, and
    an inserted silence also delays the content by n; flip XORs `mask` into
    one channel's word; swap exchanges two channels for n frames; copy puts
    the first channel's words on the second for n frames. A capture-side loss
    looks like a drop at the capture, so it is planted as one.
    """
    from array import array
    shifts = {}
    for event in events:
        if event["kind"] in ("drop", "repeat"):
            sign = 1 if event["kind"] == "drop" else -1
            shifts[event["index"]] = shifts.get(event["index"], 0) + sign * event["n"]
        elif event["kind"] == "silence" and event.get("inserted"):
            shifts[event["index"]] = shifts.get(event["index"], 0) - event["n"]
    marks = sorted({0, frames} | {index for index in shifts if 0 < index < frames})
    words = array("I", bytes(4 * frames * channels))
    for channel in range(channels):
        column, shift = array("I"), 0
        for start, end in zip(marks, marks[1:]):
            shift += shifts.get(start, 0)
            column.frombytes(_audio_expected_bytes(channel + 1, start_counter + start + shift, end - start))
        words[channel::channels] = column
    for event in events:
        if event["kind"] == "silence":
            start, end = event["index"], min(frames, event["index"] + event["n"])
            words[start * channels:end * channels] = array("I", bytes(4 * channels * (end - start)))
    if byteorder != sys.byteorder:
        words.byteswap()
    capture = bytearray(words.tobytes())

    def at(index: int, channel: int) -> slice:
        """The byte span of one channel's word in one frame."""
        offset = 4 * (index * channels + channel)
        return slice(offset, offset + 4)

    for event in events:
        if event["kind"] == "flip":
            word = int.from_bytes(capture[at(event["index"], event["channel"])], byteorder)
            capture[at(event["index"], event["channel"])] = (word ^ event["mask"]).to_bytes(4, byteorder)
        elif event["kind"] in ("swap", "copy"):
            a, b = event["channels"]
            for index in range(event["index"], min(frames, event["index"] + event["n"])):
                if event["kind"] == "swap":
                    capture[at(index, a)], capture[at(index, b)] = capture[at(index, b)], capture[at(index, a)]
                else:
                    capture[at(index, b)] = capture[at(index, a)]
    return bytes(capture)


def _audio_chunks(capture):
    if isinstance(capture, (bytes, bytearray, memoryview)):
        yield bytes(capture)
        return
    for chunk in capture:
        yield bytes(chunk)


@dataclass
class _AudioTrack:
    """What one window of a channel is graded against.

    `base` is the position the old track expects at `start`, `own` the
    channel number followed, `previous` the word received just before the
    window, `resync` the (index, number, position) of the 64 clean samples
    that close it and `follows` the first of them. The old track held from
    `since`. `owners` maps each channel number to its capture channel.
    """
    start: int
    base: int | None
    own: int | None
    previous: int | None
    resync: tuple | None
    follows: int | None
    since: int
    owners: dict
    reason: str | None
    acquiring: bool


def _audio_due(track: _AudioTrack, index: int, offset: int) -> int:
    return audio_counter_word(track.own, track.base + index - track.start + offset)


def _audio_labels(track: _AudioTrack, body: list, final: int | None, forced: dict | None = None) -> list[list]:
    """Each stored word as track at an offset, corruption, swap or open; zero runs kept.

    The tag's integrity decides first: a word of the followed channel is a
    track candidate; another channel's word is a swap only when the exchange
    was reciprocal at that sample, and corruption otherwise. A run of the
    channel's consecutive positions is cut at each word no offset explains, so
    one corrupted word never hides the slips beside it. The offset in force
    before the last change stays a candidate, so a corrupted word that fits
    the closing track never strands the words after it. At either end of the
    capture, words that differ from their track only in the code bit are
    open: a slip of whole blocks or a code-bit corruption. The words at the
    `forced` capture indices are read as corruption, for a reading that a
    logged flip arm decides; a forced word's offset, when given, is in force
    after it.
    """
    forced = forced or {}
    labels = []
    for token in body:
        if token[0] == "Z":
            labels.append(["Z", token[1], 0, token[2]])
            continue
        _, index, word, partner = token
        if index in forced:
            labels.append(["bad", index, word, None])
        elif track.own is not None and not word & AUDIO_ZERO_MASK and _audio_fields(word)[0] == track.own:
            labels.append(["own", index, word, None])
        elif partner is not None:
            labels.append(["swap", index, word, partner])
        else:
            labels.append(["bad", index, word, None])
    reference = held = None if track.acquiring else 0
    ending = track.reason == AUDIO_END_REASON and not track.acquiring
    k = 0
    while k < len(labels):
        if labels[k][0] != "own":
            if forced.get(labels[k][1]) not in (None, reference):
                held, reference = reference, forced[labels[k][1]]
            k += 1
            continue
        end = k + 1
        while (end < len(labels) and labels[end][0] == "own" and labels[end][1] == labels[end - 1][1] + 1
               and _audio_fields(labels[end][2])[1]
               == (_audio_fields(labels[end - 1][2])[1] + 1) % AUDIO_BLOCK_FRAMES):
            end += 1
        if track.base is not None and (track.acquiring and final is not None
                                       or ending and end == len(labels)):
            reference = _audio_boundary(track, labels, k, end, reference if reference is not None else final)
            k = end
            continue
        j = k
        while j < end:
            fit = _audio_fit(track, labels, j, end, (reference, held, final))
            if fit is None:
                labels[j][0] = "bad"
                j += 1
                continue
            offset, stop = fit
            for label in labels[j:stop]:
                label[0], label[3] = "track", offset
            held = reference if offset != reference else held
            reference, j = offset, stop
        k = end
    return labels


def _audio_candidates(track: _AudioTrack, label: list, anchors: tuple, toward: int | None = None) -> list[int]:
    """The offsets nearest each anchor that bits 11:1 of the word allow.

    A run shorter than 64 samples cannot fix its block, so it is tried at the
    nearest position its bits 11:1 allow from the offset before it, then from
    the offset in force before that one, then from the offset the window
    closes on; half a block away, both ways, the one nearer `toward` first.
    """
    offsets = []
    for anchor in anchors:
        if anchor is None or track.base is None:
            continue
        due = track.base + label[1] - track.start + anchor
        delta = (_audio_fields(label[2])[1] - due) % AUDIO_BLOCK_FRAMES
        near = anchor + (delta - AUDIO_BLOCK_FRAMES if delta > AUDIO_BLOCK_FRAMES // 2 else delta)
        pair = (near, near - AUDIO_BLOCK_FRAMES) if delta == AUDIO_BLOCK_FRAMES // 2 else (near,)
        for offset in sorted(pair, key=lambda o: 0 if toward is None else abs(o - toward)):
            if offset not in offsets:
                offsets.append(offset)
    return offsets


def _audio_fit(track: _AudioTrack, labels: list[list], j: int, end: int,
               anchors: tuple) -> tuple[int, int] | None:
    """(offset, stop): the run from labels[j] that one offset explains exactly.

    `anchors` are the offset in force, the one before it and the closing
    offset. The offset nearest the one in force is kept while it fits, so
    each slip takes the smallest size the positions allow and a slip of whole
    blocks is placed at the first word that shows it; half a block away, the
    longer run wins, then the one nearer the offset before. Otherwise the
    longest run from the other anchors wins.
    """
    reference, held, final = anchors
    first = _audio_candidates(track, labels[j], (reference,), held)
    for group in (first, [o for o in _audio_candidates(track, labels[j], (held, final)) if o not in first]):
        best = None
        for offset in group:
            stop = j
            while stop < end and labels[stop][2] == _audio_due(track, labels[stop][1], offset):
                stop += 1
            if stop > j and (best is None or stop > best[1]):
                best = (offset, stop)
        if best is not None:
            return best
    return None


def _audio_boundary(track: _AudioTrack, labels: list[list], k: int, end: int, anchor: int | None) -> int | None:
    """Label one run of consecutive positions at an end of the capture.

    Its words all fit one offset in bits 11:1. Where some differ in the code
    bit too, fewer than 64 clean samples lie beyond them, so a slip of whole
    blocks and a code-bit corruption read the same: those words are open.
    Before acquisition they run to the last such word; at the capture's end
    they run from the first one. Returns the offset.
    """
    offsets = _audio_candidates(track, labels[k], (anchor,))
    if not offsets:
        for label in labels[k:end]:
            label[0] = "bad"
        return anchor

    def misses(offset: int) -> list[int]:
        """The run's label indices whose word differs from the track at `offset`."""
        return [i for i in range(k, end) if labels[i][2] != _audio_due(track, labels[i][1], offset)]

    offset = min(offsets, key=lambda o: len(misses(o)))
    wrong = misses(offset)
    for i in range(k, end):
        labels[i][0], labels[i][3] = "track", offset
    if wrong:
        first, last = (wrong[0], wrong[-1]) if track.acquiring else (wrong[0], end - 1)
        for i in range(first, last + 1):
            labels[i][0] = "open"
    return offset


def _audio_duplicate(track: _AudioTrack, labels: list[list], k: int) -> bool:
    """Whether the word at labels[k] equals the word received next to it."""
    before = labels[k - 1] if k else None
    after = labels[k + 1] if k + 1 < len(labels) else None
    prior = track.previous if before is None else (0 if before[0] == "Z" else before[2])
    later = track.follows if after is None else (0 if after[0] == "Z" else after[2])
    return labels[k][2] in (prior, later)


@dataclass
class _AudioSteer:
    """How the planted-arm log steers one reading of a window.

    `slips` are the logged slip arms, (capture index, signed size), within
    `tolerance`. `judge` maps a corrupted word's index to the offset it is
    judged against, the slip to that offset coming before it. `keep` holds
    the capture indices where a logged slip arm keeps an excursion as its
    slips.
    """
    slips: Sequence = ()
    tolerance: int = 0
    judge: dict = field(default_factory=dict)
    keep: frozenset = frozenset()


def _audio_excursion(track: _AudioTrack, labels: list[list], k: int, current: int,
                     final: int | None, steer: _AudioSteer) -> int:
    """Read an excursion from `current` as corruption where it must be; the label index where it ends.

    An excursion leaves the track at labels[k]. One that returns to the same
    offset, where `_audio_return` finds, is read by `_audio_corruption`. A
    window cut at its word bound is graded in pieces, so there a
    constant-mask stretch reaching the cut stays one corruption.

    When its positions return at once but a whole number of blocks away, the
    stretch is judged the same way beside the slip of whole blocks: either
    reading is two events. It is judged against the offset after the slip,
    the slip coming first, when its mask there has fewer bits set; the
    steer's `judge` records that choice. An excursion that ends in a slip of
    another size is one corruption and that slip when one mask joins its
    words, no single offset explains them and none is on the slip's track:
    as slips it would be three events or more. An excursion that enters or
    leaves at a capture index in the steer's `keep`, where a logged slip arm
    decides, stays the slips it reads as.
    """
    end = k
    while end < len(labels) and (labels[end][0] == "bad"
                                 or (labels[end][0] == "track" and labels[end][3] != current)):
        end += 1
    back = (labels[end][3] if end < len(labels) and labels[end][0] in ("track", "open")
            else final if end == len(labels) else None)
    if back is None and end == len(labels) and end - k > 1 and track.reason == AUDIO_BOUND_REASON:
        back = current
    if back == current:
        end = _audio_return(track, labels, k, end, current)
    else:
        cut = k
        while cut < end and not (labels[cut][0] == "track"
                                 and (labels[cut][3] - current) % AUDIO_BLOCK_FRAMES == 0):
            cut += 1
        if cut == k or cut == end and (back is None or (back - current) % AUDIO_BLOCK_FRAMES):
            span = labels[k:end]
            if (cut == end and back is not None and len(span) > 1
                    and not steer.keep & {span[0][1], span[-1][1] + 1}
                    and len({label[2] ^ _audio_due(track, label[1], current) for label in span}) == 1
                    and len({label[3] if label[0] == "track" else None for label in span}) > 1
                    and all(label[2] != _audio_due(track, label[1], back) for label in span)):
                for label in span:
                    label[0], label[3] = "bad", span[0][1]
            return end
        end, ahead = cut, labels[cut][3] if cut < len(labels) else back
        masks = {offset: {label[2] ^ _audio_due(track, label[1], offset) for label in labels[k:end]}
                 for offset in (current, ahead)}
        if len(masks[ahead]) == 1 and 0 not in masks[ahead] and (
                len(masks[current]) > 1 or bin(*masks[ahead]).count("1") < bin(*masks[current]).count("1")):
            steer.judge[labels[k][1]] = current = ahead
    if not steer.keep & {labels[k][1], labels[end - 1][1] + 1}:
        _audio_corruption(track, labels, k, end, current)
    return end


def _audio_return(track: _AudioTrack, labels: list[list], k: int, end: int, current: int) -> int:
    """The label index where an excursion that returns to `current` really returns.

    Words fitted to another offset of whole blocks may fit the offset in
    force too. When only the leading stretch does not, the excursion is that
    stretch and returns at the next word. So does a leading stretch under one
    mask that no single offset of whole blocks explains, before the first
    word that fits the offset in force: a corruption, not a slip, so that word
    and the coincident words after it are its return, and what follows is
    graded on its own.
    """
    fits = [r for r in range(k + 1, end)
            if labels[r][0] == "track" and labels[r][2] == _audio_due(track, labels[r][1], current)]
    if fits and fits == list(range(fits[0], end)):
        for label in labels[fits[0]:end]:
            label[0], label[3] = "track", current
        return fits[0]
    if fits:
        lead = labels[k:fits[0]]
        offsets = {label[3] if label[0] == "track" else None for label in lead}
        if (len({label[2] ^ _audio_due(track, label[1], current) for label in lead}) == 1
                and (len(offsets) > 1 or None in offsets or (offsets.pop() - current) % AUDIO_BLOCK_FRAMES)):
            back = fits[0]
            while back in fits:
                labels[back][0], labels[back][3] = "track", current
                back += 1
            return fits[0]
    return end


def _audio_corruption(track: _AudioTrack, labels: list[list], k: int, end: int, current: int) -> None:
    """Relabel the net-zero excursion labels[k:end] as corruption where it must be.

    One word is a corruption unless it equals a neighbouring received word, a
    repeat. Two or more words whose XOR with the track is one constant mask
    are one corruption. When no single offset explains the words, a word at
    either end off the mask the others share is its own one-word corruption,
    and so is each word of a two-word excursion under two masks; a corrupted
    label's fourth field groups the words of one corruption, so a word beside
    it is never merged in. Otherwise each change of position is its own slip.
    """
    span = labels[k:end]
    if len(span) == 1:
        if span[0][0] != "bad" and not _audio_duplicate(track, labels, k):
            span[0][0], span[0][3] = "bad", None
        return
    masks = [label[2] ^ _audio_due(track, label[1], current) for label in span]
    first, last = 0, len(span)
    if len(set(masks)) > 1:
        if span[0][0] == "track" and len({label[3] if label[0] == "track" else None for label in span}) == 1:
            return
        for first, last in ((1, len(span)), (0, len(span) - 1), (1, len(span) - 1)):
            if (last - first > 1 or len(span) == 2) and len(set(masks[first:last])) == 1 and all(
                    span[i][0] == "bad" or not _audio_duplicate(track, labels, k + i)
                    for i in (*range(first), *range(last, len(span)))):
                break
        else:
            return
    for i, label in enumerate(span):
        label[0], label[3] = "bad", span[first][1] if first <= i < last else None


def _audio_slip(track: _AudioTrack, index: int, old: int, new: int, stretch: int,
                upto: int | None = None) -> dict:
    """A slip from offset `old` to `new` seen at `index`, on the new track up to `upto`.

    A slip of whole blocks leaves bits 11:1 alone, so the words around
    `index` may fit both tracks; `located_within` then bounds the sample:
    back over the words before it that fit both, after `stretch`, and on to
    the first word from `index` on that shows the slip.
    """
    shift, first, last = new - old, index, index
    if shift % AUDIO_BLOCK_FRAMES == 0:
        while first > stretch and _audio_due(track, first - 1, old) == _audio_due(track, first - 1, new):
            first -= 1
        while (upto is not None and last + 1 < upto
               and _audio_due(track, last, old) == _audio_due(track, last, new)):
            last += 1
    event = {"capture_index": index, "class": "dropped" if shift > 0 else "repeated", "n": abs(shift),
             "expected": _audio_due(track, index, old), "received": _audio_due(track, index, new)}
    if first < last:
        event["located_within"] = [first, last]
    return event


def _audio_net(events: Iterable[dict]) -> int:
    """The signed shift of the content that `events` read as: drops ahead, repeats and inserted silence back."""
    net = 0
    for event in events:
        if event["class"] in ("dropped", "repeated"):
            net += event["n"] if event["class"] == "dropped" else -event["n"]
        elif event["class"] == "silence" and event.get("inserted"):
            net -= event["n"]
    return net


def _audio_upto(track: _AudioTrack, labels: list[list], k: int, offset: int, final: int | None) -> int:
    """The capture index up to which the words from labels[k] stay on `offset`."""
    end = k
    while end < len(labels) and labels[end][0] == "track" and labels[end][3] == offset:
        end += 1
    if end == len(labels) and offset == final and track.resync is not None:
        return track.resync[0] + AUDIO_CONFIRM_FRAMES
    return labels[end - 1][1] + 1


def _audio_open(track: _AudioTrack, run: list[list], stretch: int) -> dict:
    """One `unresolved` event for the open words at an end of the capture.

    `located_within` bounds the sample a slip of whole blocks would be at. At
    the capture's end at most 62 coincident words precede the first open
    word; before acquisition at most 62 follow the last one, and at most 62
    of the 64 acquiring samples.
    """
    first, last, offset = run[0][1], run[-1][1], run[0][3]
    if track.acquiring:
        bounds = [last + 1, min(last + AUDIO_GUARD_FRAMES, track.resync[0] + AUDIO_GUARD_FRAMES - 1)]
        why = "before acquisition: a slip of whole blocks or a code-bit corruption"
    else:
        bounds = [max(first - AUDIO_GUARD_FRAMES + 1, stretch), first]
        why = AUDIO_END_REASON + ": a slip of whole blocks or a code-bit corruption"
    mask = 0
    for label in run:
        mask |= label[2] ^ _audio_due(track, label[1], offset)
    return {"capture_index": first, "class": "unresolved", "n": last - first + 1,
            "expected": _audio_due(track, first, offset), "received": run[0][2], "mask": mask,
            "located_within": bounds, "unresolved": why}


def _audio_extend(events: list, run: dict | None, cls: str, label: list, track: _AudioTrack,
                  current: int | None) -> dict:
    """Open or extend a corruption or swap run with one word.

    A run grows only with the next word of its class and its partner: for a
    corrupted word, the group `_audio_corruption` gave it.
    """
    _, index, word, partner = label
    due = None if current is None or track.own is None else _audio_due(track, index, current)
    match = None
    tag = _audio_fields(word)[0]
    if due is not None and tag in track.owners and not word & AUDIO_ZERO_MASK \
            and word == audio_counter_word(tag, track.base + index - track.start + current):
        match = track.owners[tag]
    if (run is not None and run["class"] == cls and run.get("partner") == partner
            and run["capture_index"] + run["n"] == index):
        run["n"] += 1
        run["mask"] |= word ^ (due or 0)
        run["matches"].add(match)
        return run
    _audio_flush(events, run)
    return {"capture_index": index, "class": cls, "n": 1, "expected": due, "received": word,
            "mask": word ^ (due or 0), "partner": partner, "matches": {match}}


def _audio_flush(events: list, run: dict | None) -> None:
    """Close an open corruption or swap run into its event."""
    if run is None:
        return
    matches = run.pop("matches")
    if run["class"] == "swap":
        run.pop("mask")
    else:
        run.pop("partner")
        if len(matches) == 1 and None not in matches:
            run["matches_channel"] = matches.pop()
    events.append(run)


def _audio_window_events(track: _AudioTrack, labels: list[list], final: int | None,
                         steer: _AudioSteer | None = None) -> tuple[list, int | None]:
    """The events of one window and the offset it ends on.

    Offsets count samples ahead of the old track. A change of offset is a
    slip; zero runs are silence, inserted when the content resumes where it
    stopped; foreign or corrupted words are corruption runs with the OR of
    their XOR masks; reciprocal exchanges are swaps; open words are one
    `unresolved` event. Each departure from the offset in force is judged
    against that offset, again after every slip.

    A corrupted word bounds a slip of whole blocks only where the two tracks
    differ: where they coincide its mask is the same on either side.

    `steer` carries the planted-arm log's say. A slip at a logged slip arm
    that differs from it by whole blocks is the arm and a slip of whole
    blocks beside it, which the capture cannot tell from their sum; the
    arm's log decides.
    """
    steer = _AudioSteer() if steer is None else steer

    def slip(index: int, old: int, new: int, stretch: int, upto: int) -> list:
        """The slip from `old` to `new` seen at `index`, split at a logged arm."""
        for at, size in steer.slips:
            rest = new - old - size
            if abs(at - index) <= steer.tolerance and rest and not rest % AUDIO_BLOCK_FRAMES:
                low = _audio_slip(track, index, old, old + rest, stretch).get("located_within", [index])[0]
                after = _audio_slip(track, index, old + size, new, index, upto)
                high = after.get("located_within", [index, index])[1]
                if low < high:
                    after["located_within"] = [low, high]
                return [_audio_slip(track, index, old, old + size, stretch), after]
        return [_audio_slip(track, index, old, new, stretch, upto)]

    events, run, excursion, checked = [], None, 0, None
    current = None if track.acquiring else 0
    stretch = track.since if current is not None else track.start
    ahead, later = [None] * len(labels), final
    for k in range(len(labels) - 1, -1, -1):
        ahead[k] = later
        later = labels[k][3] if labels[k][0] in ("track", "open") else later
    k = 0
    while k < len(labels):
        label = labels[k]
        if label[0] == "open":
            _audio_flush(events, run)
            run, end = None, k
            while end < len(labels) and labels[end][0] == "open":
                end += 1
            if current is not None and label[3] != current:
                events.append(_audio_slip(track, label[1], current, label[3], stretch))
            current = label[3]
            events.append(_audio_open(track, labels[k:end], stretch))
            stretch, k = labels[end - 1][1] + 1, end
            continue
        if current is not None and (k >= excursion or current != checked) and (
                label[0] == "bad" or (label[0] == "track" and label[3] != current)):
            excursion, checked = _audio_excursion(track, labels, k, current, final, steer), current
        kind, index, _, extra = label
        after, k = ahead[k], k + 1
        if kind == "bad" and steer.judge.get(index) not in (None, current) and current is not None:
            _audio_flush(events, run)
            run = None
            events += slip(index, current, steer.judge[index], stretch, index)
            current, stretch = steer.judge[index], index
        if kind in ("bad", "swap"):
            run = _audio_extend(events, run, "bit-flip" if kind == "bad" else "swap", label, track, current)
            if kind == "swap":
                stretch = index + 1
            continue
        _audio_flush(events, run)
        run = None
        if kind == "Z":
            inserted = None if current is None or after is None else after == current - extra
            events.append({"capture_index": index, "class": "silence", "n": extra, "inserted": inserted,
                           "expected": None if current is None else _audio_due(track, index, current),
                           "received": 0})
            current = current - extra if inserted else current
            stretch = index + extra
        elif current is None or extra != current:
            if current is not None:
                events += slip(index, current, extra, stretch, _audio_upto(track, labels, k - 1, extra, final))
            current, stretch = extra, index
    _audio_flush(events, run)
    if final is not None and current is not None and final != current:
        events += slip(track.resync[0], current, final, stretch, track.resync[0] + AUDIO_CONFIRM_FRAMES)
    if track.resync is None:
        for event in events:
            if event["class"] in ("dropped", "repeated"):
                event["unresolved"] = track.reason
    return events, final if final is not None else current


class _CounterWindow:
    """One channel's words from its first mismatch until 64 clean samples resume."""

    __slots__ = ("start", "base", "previous", "tokens", "stored", "tail")

    def __init__(self, start: int, base: int | None, previous: int | None) -> None:
        self.start, self.base, self.previous = start, base, previous
        self.tokens, self.stored, self.tail = [], 0, []

    def add(self, index: int, word: int, partner: int | None, numbers: frozenset) -> None:
        """Record one word; zero runs are counted, not stored."""
        if word == 0:
            last = self.tokens[-1] if self.tokens else None
            if last is not None and last[0] == "Z" and last[1] + last[2] == index:
                self.tokens[-1] = ("Z", last[1], last[2] + 1)
            else:
                self.tokens.append(("Z", index, 1))
            self.tail = []
            return
        self.tokens.append(("W", index, word, partner))
        self.stored += 1
        tag, position = _audio_fields(word)
        if word & AUDIO_ZERO_MASK or tag not in numbers:
            self.tail = []
            return
        if self.tail:
            last_tag, last_position = _audio_fields(self.tail[-1][1])
            if tag != last_tag or position != (last_position + 1) % AUDIO_BLOCK_FRAMES:
                self.tail = []
        self.tail.append((index, word))
        del self.tail[:-AUDIO_CONFIRM_FRAMES]

    def confirmed(self) -> tuple[int, int, int] | None:
        """(index, channel number, position) of 64 clean samples ending here."""
        if len(self.tail) < AUDIO_CONFIRM_FRAMES:
            return None
        position = _audio_decode([word for _, word in self.tail])
        if position is None:
            del self.tail[0]
            return None
        return self.tail[0][0], _audio_fields(self.tail[0][1])[0], position

    def end(self) -> int:
        """The capture index after the last recorded word."""
        last = self.tokens[-1]
        return last[1] + (last[2] if last[0] == "Z" else 1)


def _audio_image_mask(tag: int, base: int, start: int, tokens: list) -> int | None:
    """The one XOR mask every stored word shares with the track, 0 for none, else None."""
    masks = set()
    for token in tokens:
        if token[0] == "Z":
            return None
        masks.add(token[2] ^ audio_counter_word(tag, base + token[1] - start))
        if len(masks) > 1:
            return None
    return masks.pop() if masks else 0


@dataclass
class _AudioImage:
    """A slip whose words are all the old track under one XOR mask.

    Such a track is the old one corrupted, so its events wait: a return to the
    old track makes the whole excursion one corruption, at any length, and a
    word off that mask releases them as the slips they are. Past the region
    where the held track is the old one masked, a followed word can be the
    old track's own word: the return, or a coincidence of the slip. `clean`
    is the first of those words; a masked word after it parts the masks.
    """
    tag: int
    base: int
    start: int
    mask: int
    events: list
    clean: int | None = None

    def due(self, index: int) -> int:
        """The old track's word at capture index `index`."""
        return audio_counter_word(self.tag, self.base + index - self.start)

    def keeps(self, index: int, word: int) -> bool:
        """Whether a followed word keeps the hold: the mask, or the old track itself."""
        xor = word ^ self.due(index)
        if xor == 0:
            self.clean = index if self.clean is None else self.clean
            return True
        return xor == self.mask and self.clean is None

    def holds(self, first: int, column: Sequence[int]) -> bool:
        """Whether every word of a fast-path block keeps the mask."""
        from array import array
        expected = _audio_expected_bytes(self.tag, self.base + first - self.start, len(column))
        pattern = array("I", [self.mask]).tobytes() * len(column)
        if (self.clean is None and int.from_bytes(column.tobytes(), "little") ^ int.from_bytes(expected, "little")
                == int.from_bytes(pattern, "little")):
            return True
        return all(self.keeps(first + k, word) for k, word in enumerate(column))


class _CounterSlot:
    """One capture channel: the number it should carry and the track it follows."""

    __slots__ = ("want", "tag", "position", "window", "previous", "since", "timeline", "acquired", "image",
                 "shift", "reported")

    def __init__(self, want: int) -> None:
        self.want, self.tag, self.position = want, None, None
        self.window, self.previous, self.since = None, None, 0
        #: (index, channel number, position) where each carried identity begins.
        self.timeline = []
        #: The capture index of the 64 clean samples that first fixed the track.
        self.acquired = None
        self.image = None
        #: The content shift the closing samples decode since acquisition, and the one the recorded slips sum to.
        self.shift = self.reported = 0


class _CounterScan:
    """Per-channel tracks over one capture, every event classified at its sample.

    A channel's numbers and position are acquired from its first 64 clean
    samples, so a channel swapped from the first frame is followed and its
    swap is an event. A mismatch opens a window that closes at the next 64
    clean samples, whose decoded position sizes every slip in it exactly.
    The planted-arm log, with its index tolerance, decides between readings
    of a window that the capture cannot tell apart.
    """

    def __init__(self, tags: list, limit: int, arms: Sequence[dict] = (), tolerance: int = 0) -> None:
        self.channels = len(tags)
        self.slots = {c: _CounterSlot(tag) for c, tag in enumerate(tags) if tag is not None}
        #: Each logged arm with the channel number it was planted on, None for every channel.
        self.arms = [(arm, None if arm.get("channel") is None else tags[arm["channel"]]) for arm in arms]
        self.tolerance = tolerance
        self.numbers = frozenset(slot.want for slot in self.slots.values())
        self.owners = {slot.want: channel for channel, slot in self.slots.items()}
        self.events, self.limit, self.unrecorded = [], limit, 0

    def frames(self, first: int, data: Sequence[int]) -> None:
        """Grade a block of frames; `data` holds its words in native order."""
        count = len(data) // self.channels
        for channel, slot in self.slots.items():
            column = data[channel::self.channels]
            if (slot.window is None and slot.position is not None
                    and column.tobytes() == _audio_expected_bytes(slot.tag, slot.position, count)):
                slot.position += count
                slot.previous = column[-1]
                if slot.image is not None and not slot.image.holds(first, column):
                    self._release(channel, None)
                continue
            for k, word in enumerate(column):
                self._step(channel, first + k, word, data, k)

    def _step(self, channel: int, index: int, word: int, data: Sequence[int], k: int) -> None:
        slot = self.slots[channel]
        if slot.window is None:
            if slot.position is not None and word == audio_counter_word(slot.tag, slot.position):
                slot.position += 1
                slot.previous = word
                if slot.image is not None and not slot.image.keeps(index, word):
                    self._release(channel, None)
                return
            slot.window = _CounterWindow(index, slot.position, slot.previous)
        slot.window.add(index, word, self._partner(channel, word, data, k), self.numbers)
        slot.previous = word
        found = slot.window.confirmed()
        if found is not None:
            self._close(channel, found, None)
        elif slot.window.stored > AUDIO_WINDOW_WORDS:
            self._close(channel, None, AUDIO_BOUND_REASON)

    def _release(self, channel: int, why: str | None) -> None:
        """Record a held excursion's events as the slips they read as."""
        image, self.slots[channel].image = self.slots[channel].image, None
        for event in image.events:
            if why:
                event["unresolved"] = why
            self._record(channel, event)

    def _returned(self, image: _AudioImage, window: "_CounterWindow", body: list, track: _AudioTrack,
                  back: int) -> tuple[_AudioTrack, list, list, int]:
        """(track, events, tokens, final) of a window in which a held excursion returned.

        The excursion is one bit-flip. It ends where the old track's own words
        began, or after the window's leading words still under its mask. The
        rest of the window is graded against the old track, so an event beside
        the excursion is graded on its own.
        """
        lead = 0
        while (image.clean is None and lead < len(body) and body[lead][0] == "W"
               and body[lead][2] ^ image.due(body[lead][1]) == image.mask):
            lead += 1
        start = body[lead - 1][1] + 1 if lead else window.start
        end = start if image.clean is None else image.clean
        rest = _AudioTrack(start, image.base + start - image.start, image.tag,
                           body[lead - 1][2] if lead else window.previous, track.resync, track.follows,
                           end, self.owners, track.reason, False)
        flip = {"capture_index": image.start, "class": "bit-flip", "n": end - image.start,
                "expected": image.due(image.start), "received": image.due(image.start) ^ image.mask,
                "mask": image.mask}
        events, _ = self._read(rest, window.tokens[lead:], back)
        return rest, [flip] + events, window.tokens[lead:], back

    def _read(self, track: _AudioTrack, tokens: list, final: int | None) -> tuple[list, int | None]:
        """The events of a window and the offset it ends on, as the planted-arm log decides.

        Slip arms split a slip they differ from by whole blocks. A logged flip
        arm that the reading misses is tried as the corrupted word at each
        index its tolerance allows, judged against the offset in force or the
        closing one. A slip arm that it misses is tried as the slip into or out
        of an excursion read as a corruption. Another reading is taken only when
        it has fewer DUT events, or as many and finds more arms, so it never
        hides a DUT event. A reading whose slips do not sum to the shift the
        closing samples decode is never taken while one that does exists.
        """
        body = tokens[:-AUDIO_CONFIRM_FRAMES] if track.resync else tokens
        last = tokens[-1]
        end = last[1] + (last[2] if last[0] == "Z" else 1)
        reach = self.tolerance + AUDIO_GUARD_FRAMES
        arms = ([] if track.acquiring else
                [arm for arm, number in self.arms if number in (None, track.own)
                 and track.start - reach <= arm["index"] < end + self.tolerance])
        slips = [(arm["index"], arm["n"] if arm["class"] == "dropped" else -arm["n"])
                 for arm in arms if arm["class"] != "bit-flip"]
        read = _audio_window_events(track, _audio_labels(track, body, final), final,
                                    _AudioSteer(slips, self.tolerance))
        balance = final is not None and not track.acquiring

        def ranked(events: list) -> tuple:
            """(unbalanced, DUT events, minus the arms found) of one reading."""
            return (balance and _audio_net(events) != final, *self._score(events, arms))

        best = (ranked(read[0]), read)
        for arm in arms:
            if any(_audio_arm_found(e, arm, self.tolerance) for e in read[0]):
                continue
            if arm["class"] != "bit-flip":
                keep = frozenset(range(arm["index"] - self.tolerance, arm["index"] + self.tolerance + 1))
                other = _audio_window_events(track, _audio_labels(track, body, final), final,
                                             _AudioSteer(slips, self.tolerance, keep=keep))
                score = ranked(other[0])
                if score < best[0]:
                    best = (score, other)
                continue
            for index in range(arm["index"] - self.tolerance, arm["index"] + self.tolerance + 1):
                cut = self._cut(track, tokens, len(body), index)
                for judged in ((None, final) if cut and final else (None,) if cut else ()):
                    forced = {index: judged}
                    other = _audio_window_events(cut[0], _audio_labels(cut[0], cut[1], final, forced), final,
                                                 _AudioSteer(slips, self.tolerance, forced))
                    score = ranked(other[0])
                    if score < best[0]:
                        best = (score, other)
        return best[1]

    def _cut(self, track: _AudioTrack, tokens: list, stored: int, index: int) -> tuple | None:
        """(track, body) with the word at `index` in the body, or None when no word is there.

        A word among the 64 clean samples moves the resync one sample on: the
        words after it are on the same track. A word shortly before the window
        was followed on its track, so the window is opened there instead.
        """
        if index < track.start:
            if index <= track.since or track.start - index > AUDIO_GUARD_FRAMES:
                return None
            lead = [("W", i, _audio_due(track, i, 0), None) for i in range(index, track.start)]
            moved = replace(track, start=index, base=track.base + index - track.start,
                            previous=_audio_due(track, index - 1, 0))
            return moved, lead + tokens[:stored]
        for k, token in enumerate(tokens):
            if token[0] == "W" and token[1] == index:
                break
        else:
            return None
        if k < stored:
            return track, tokens[:stored]
        if k + 1 >= len(tokens):
            return None
        found = track.resync
        resync = (index + 1, found[1], (found[2] + index + 1 - found[0]) % AUDIO_PERIOD_FRAMES)
        return replace(track, resync=resync, follows=tokens[k + 1][2]), tokens[:k + 1]

    def _score(self, events: list, arms: list) -> tuple[int, int]:
        """(DUT events, minus the arms found) of one reading."""
        found = sum(any(_audio_arm_found(event, arm, self.tolerance) for event in events) for arm in arms)
        dut = sum(not any(_audio_arm_found(event, arm, self.tolerance) for arm in arms) for event in events)
        return dut, -found

    def _hold(self, slot: _CounterSlot, track: _AudioTrack, events: list, tokens: list,
              final: int | None) -> list:
        """Hold the slips into a track that is the old one under one mask; the events to record now.

        Only the window's trailing words under the closing mask decide, so an
        event before them is recorded and never stops the hold. The old one is
        the track at the offset in force where those words begin: the window's
        opening offset or one the reading reaches, whichever leaves the longest
        masked run, so a slip before the excursion sizes it. What is recorded
        now must end on that offset, as the bytes do, so a reading that reaches
        another is read again with the masked words restored, and the held
        slips are the ones those words read as from it.
        """
        if slot.image is not None or not final or track.resync is None or track.resync[1] != slot.tag:
            return events

        def masked(offset: int) -> tuple[int, int]:
            """(k, mask): tokens[k:] are the track at `offset` under one nonzero mask."""
            def xor(token: tuple) -> int | None:
                """The word's XOR with the track at `offset`; None for silence."""
                return None if token[0] == "Z" else token[2] ^ _audio_due(track, token[1], offset)

            mask, k = xor(tokens[-1]), len(tokens)
            while mask and k and xor(tokens[k - 1]) == mask:
                k -= 1
            return (k, mask) if mask else (len(tokens), 0)

        offsets, reached = [0], 0
        for event in events:
            reached += _audio_net((event,))
            offsets.append(reached)
        runs = [(*masked(offset), offset) for offset in dict.fromkeys(offsets)]
        for run in sorted(runs, key=lambda run: run[0]):
            split = self._split(track, events, tokens, run, final) if run[0] < len(tokens) else None
            if split is not None:
                before, held, at = split
                slot.image = _AudioImage(slot.tag, track.base + at - track.start + run[2], at, run[1], held)
                return before
        return events

    def _split(self, track: _AudioTrack, events: list, tokens: list, run: tuple,
               final: int) -> tuple[list, list, int] | None:
        """(recorded, held, start) of a hold of tokens[k:] under `mask` over the track at `offset`, or None.

        `run` is (k, mask, offset).

        None when the reading has no slip that may lie in the masked words, so
        there is nothing to hold, or when the words before them cannot be read
        apart from the masked ones.
        """
        k, mask, offset = run
        at = tokens[k][1]
        for event in events:
            if event["capture_index"] < at < event["capture_index"] + event["n"] and event["class"] == "bit-flip":
                at = event["capture_index"] + event["n"]
        before = [event for event in events if event["capture_index"] < at]
        held = [event for event in events if event["capture_index"] >= at]
        if not any(event["class"] in ("dropped", "repeated")
                   and event.get("located_within", [at - 1, event["capture_index"]])[1] >= at for event in events):
            return None
        if _audio_net(before) != offset:
            at, found = tokens[k][1], track.resync
            words = tokens[:k] + [(token[0], token[1], token[2] ^ mask, None) for token in tokens[k:]]
            if any(token[0] != "W" or token[2] != _audio_due(track, token[1], offset)
                   for token in words[-AUDIO_CONFIRM_FRAMES:]):
                return None
            restored = replace(track, follows=words[-AUDIO_CONFIRM_FRAMES][2], resync=(
                found[0], found[1], (track.base + found[0] - track.start + offset) % AUDIO_PERIOD_FRAMES))
            before, _ = self._read(restored, words, offset)
            previous = track.previous if k == 0 else tokens[k - 1][2] if tokens[k - 1][0] == "W" else 0
            excursion = replace(track, start=at, base=track.base + at - track.start + offset, previous=previous,
                                since=at)
            held, _ = self._read(excursion, tokens[k:], final - offset)
            if any(event["capture_index"] >= at for event in before):
                return None
        if not any(event["class"] in ("dropped", "repeated") for event in held):
            return None
        return before, held, at

    def _partner(self, channel: int, word: int, data: Sequence[int], k: int) -> int | None:
        """The channel this word was exchanged with, when the exchange is reciprocal."""
        own, tag = self.slots[channel].tag, _audio_fields(word)[0]
        if own is None or not word or word & AUDIO_ZERO_MASK or tag == own or tag not in self.numbers:
            return None
        for other, slot in self.slots.items():
            if other != channel and (slot.tag or slot.want) == tag:
                theirs = data[k * self.channels + other]
                exchanged = theirs and not theirs & AUDIO_ZERO_MASK and _audio_fields(theirs)[0] == own
                return other if exchanged else None
        return None

    def _close(self, channel: int, found: tuple | None, reason: str | None) -> None:
        """Grade the open window, then follow the track its clean samples fix."""
        slot = self.slots[channel]
        window, slot.window = slot.window, None
        acquiring = slot.position is None
        base, own = window.base, slot.tag
        if found is not None and acquiring:
            base, own = found[2] - (found[0] - window.start), found[1]
        track = _AudioTrack(window.start, base, own, window.previous, found,
                            window.tokens[-AUDIO_CONFIRM_FRAMES][2] if found else None,
                            slot.since, self.owners, reason, acquiring)
        final = None
        if found is not None:
            final = 0 if acquiring else _audio_signed(found[2] - (base + found[0] - window.start))
        body = window.tokens[:-AUDIO_CONFIRM_FRAMES] if found else window.tokens
        events, offset = self._read(track, window.tokens, final)
        truth = None if acquiring else final if found is not None else offset
        image, tokens = slot.image, window.tokens
        if image is not None:
            back = (None if found is None or found[1] != image.tag
                    else _audio_signed(found[2] - (image.base + found[0] - image.start)))
            if back is not None and _audio_image_mask(image.tag, image.base, image.start, tokens) == image.mask:
                image.events += events
                events = []
            elif back is not None and abs(back) <= abs(final):
                slot.image = None
                track, events, tokens, final = self._returned(image, window, body, track, back)
            else:
                self._release(channel, "the capture ended inside a constant-mask excursion"
                              if reason == AUDIO_END_REASON else None)
        events = self._hold(slot, track, events, tokens, None if acquiring else final)
        if truth is not None:
            slot.shift += truth
            held = 0 if slot.image is None else _audio_net(slot.image.events)
            if slot.reported + _audio_net(events) + held != slot.shift:
                events = [self._unbalanced(track, window, found)]
                slot.reported = slot.shift - held
        for event in events:
            self._record(channel, event)
        if acquiring:
            slot.shift = slot.reported
        if found is not None:
            if acquiring and slot.acquired is None:
                slot.acquired = found[0]
            if found[1] != slot.tag:
                slot.timeline.append(found)
            slot.tag, slot.position, slot.since = found[1], found[2] + AUDIO_CONFIRM_FRAMES, found[0]
        elif own is not None and base is not None and offset is not None:
            slot.position, slot.since = base + window.end() - window.start + offset, window.end()

    def _unbalanced(self, track: _AudioTrack, window: _CounterWindow, found: tuple | None) -> dict:
        """The window as one unresolved event: no reading's slips sum to the shift its bytes decode.

        Every reading balances by construction, so this is the guard behind
        it: the window is an unclassified corruption at its first sample,
        never a slip that did not happen.
        """
        end = found[0] + 1 if found is not None else window.end()
        mask = 0
        for token in window.tokens:
            if token[0] == "W" and token[1] < end:
                mask |= token[2] ^ _audio_due(track, token[1], 0)
        first = window.tokens[0]
        return {"capture_index": window.start, "class": "unresolved", "n": end - window.start,
                "expected": _audio_due(track, window.start, 0), "received": first[2] if first[0] == "W" else 0,
                "mask": mask, "located_within": [window.start, end - 1], "unresolved": AUDIO_UNBALANCED_REASON}

    def _record(self, channel: int, event: dict) -> None:
        self.slots[channel].reported += _audio_net((event,))
        if len(self.events) >= self.limit:
            self.unrecorded += 1
            return
        for key in ("expected", "received"):
            event[key] = None if event[key] is None else f"0x{event[key]:08X}"
        if "mask" in event:
            event["mask"] = f"0x{event['mask']:08X}"
        self.events.append(dict(event, channel=channel, attribution="dut"))

    def finish(self, frames: int) -> None:
        """Close every open window at the capture's end, then grade identities."""
        for channel, slot in self.slots.items():
            if slot.window is not None:
                self._close(channel, None, AUDIO_END_REASON)
            if slot.image is not None:
                self._release(channel, "the capture ended inside a constant-mask excursion")
        spans = {channel: _audio_spans(slot.timeline, frames) for channel, slot in self.slots.items()}
        for channel, slot in self.slots.items():
            for start, end, number, position in spans[channel]:
                if number == slot.want:
                    continue
                partner = self.owners.get(number)
                for first, last, exchanged in _audio_split(start, end, spans.get(partner, []), slot.want):
                    event = {"capture_index": first, "n": last - first,
                             "expected": audio_counter_word(slot.want, position + first - start),
                             "received": audio_counter_word(number, position + first - start)}
                    if exchanged:
                        event.update({"class": "swap", "partner": partner})
                    else:
                        event.update({"class": "bit-flip", "matches_channel": partner,
                                      "mask": (slot.want ^ number) << AUDIO_TAG_SHIFT})
                    self._record(channel, event)
        self.events.sort(key=lambda event: (event["capture_index"], event["channel"]))

    def unacquired(self) -> list:
        """The counter channels whose track no 64 clean samples have fixed yet."""
        return [channel for channel, slot in self.slots.items() if slot.acquired is None]

    def qualified(self, frames: int) -> tuple[int, int] | None:
        """[start, end) of the capture indices a verdict can prove clean.

        A slip of whole blocks shows within 63 samples on either side, so the
        interval begins 63 samples after the last channel's acquisition and
        ends 63 samples before the capture's end.
        """
        if self.unacquired():
            return None
        start = max(slot.acquired for slot in self.slots.values()) + AUDIO_GUARD_FRAMES
        return start, max(start, frames - AUDIO_GUARD_FRAMES)

    def carriers(self, channel: int, index: int) -> list:
        """The capture channels carrying channel `channel`'s number at `index`."""
        if channel not in self.slots:
            return [channel]
        number = self.slots[channel].want
        found = [other for other, slot in self.slots.items()
                 if any(start <= index < end and carried == number
                        for start, end, carried, _ in _audio_spans(slot.timeline, index + 1))]
        return found or [channel]


def _audio_spans(timeline: list, frames: int) -> list[tuple]:
    """(start, end, channel number, position at start) of each carried identity."""
    return [(index, timeline[k + 1][0] if k + 1 < len(timeline) else frames, number, position)
            for k, (index, number, position) in enumerate(timeline)]


def _audio_split(start: int, end: int, partner: list, want: int) -> list[tuple]:
    """[start, end) cut where the partner carries `want` (an exchange) or not."""
    cuts = sorted({start, end} | {edge for span in partner for edge in span[:2] if start < edge < end})
    return [(a, b, any(s <= a and b <= e and number == want for s, e, number, _ in partner))
            for a, b in zip(cuts, cuts[1:])]


def _audio_logs_valid(arms: list, losses: list, channels: int) -> bool:
    for arm in arms:
        if (not isinstance(arm, dict) or arm.get("class") not in ("dropped", "repeated", "bit-flip")
                or type(arm.get("index")) is not int or arm["index"] < 0):
            return False
        channel = arm.get("channel")
        if channel is not None and (type(channel) is not int or not 0 <= channel < channels):
            return False
        size = arm.get("mask" if arm["class"] == "bit-flip" else "n")
        if type(size) is not int or size <= 0:
            return False
    for loss in losses:
        if (not isinstance(loss, dict) or type(loss.get("index")) is not int or loss["index"] < 0
                or type(loss.get("frames")) is not int or loss["frames"] <= 0):
            return False
    return True


def _audio_at(event: dict, index: int, tolerance: int) -> bool:
    """Whether a logged index can be this event's sample, within `tolerance`."""
    first, last = event.get("located_within", (event["capture_index"], event["capture_index"]))
    return first - tolerance <= index <= last + tolerance


def _audio_arm_found(event: dict, arm: dict, tolerance: int) -> bool:
    """Whether a scanned event, its mask still a number, is this planted arm."""
    if event["class"] != arm["class"] or not _audio_at(event, arm["index"], tolerance):
        return False
    if arm["class"] == "bit-flip":
        return event["n"] == 1 and event["mask"] == arm["mask"]
    return event["n"] == arm["n"]


def _audio_attribute(events: list, log: "CounterRunLog", counter_channels: list,
                     scan: _CounterScan) -> tuple[str | None, list]:
    """Mark logged capture losses and planted arms; (refusal, missed arms)."""
    for loss in log.capture_losses:
        hits = [e for e in events if e["attribution"] == "dut" and e["class"] == "dropped"
                and e["n"] == loss["frames"] and _audio_at(e, loss["index"], 0)]
        if sorted({e["channel"] for e in hits}) != counter_channels:
            return "a logged capture loss is not in the capture", []
        for event in hits:
            event["attribution"] = "capture"
    missed, tolerance = [], log.arm_tolerance_frames
    for arm in log.planted_arms:
        want = counter_channels if arm.get("channel") is None else scan.carriers(arm["channel"], arm["index"])
        picks = {}
        for event in events:
            if (event["attribution"] != "dut" or event["class"] != arm["class"]
                    or event["channel"] not in want or not _audio_at(event, arm["index"], tolerance)):
                continue
            if arm["class"] == "bit-flip":
                if event["n"] != 1 or event["mask"] != f"0x{arm['mask']:08X}":
                    continue
            elif event["n"] != arm["n"]:
                continue
            best = picks.get(event["channel"])
            if best is None or (abs(event["capture_index"] - arm["index"])
                                < abs(best["capture_index"] - arm["index"])):
                picks[event["channel"]] = event
        if sorted(picks) != sorted(want):
            missed.append(arm)
            continue
        for event in picks.values():
            event["attribution"] = "planted"
    return None, missed


def _audio_anchors_valid(layout: "CounterCapture") -> bool:
    anchors, steps = layout.anchors, layout.gptp_steps_wall_s
    if not isinstance(anchors, (tuple, list)) or (steps is not None and (
            not isinstance(steps, (tuple, list)) or not all(_release_finite(s) for s in steps))):
        return False
    previous = (0, layout.start_wall_s)
    for anchor in anchors:
        if (not isinstance(anchor, (tuple, list)) or len(anchor) != 3 or type(anchor[0]) is not int
                or anchor[0] <= previous[0] or not all(_release_finite(v) for v in anchor[1:])
                or anchor[1] <= previous[1]):
            return False
        previous = anchor
    return True


def _audio_timing(events: list, layout: "CounterCapture", losses: list) -> int:
    """Each event's acquisition index and clocks; the count left unsupported.

    A logged capture loss stores no frames but time runs through it, so the
    acquisition index is the stored index plus every loss logged at or before
    it. Times are interpolated between the capture tool's anchors around the
    event, never extrapolated past the last one, and gPTP time never across a
    recorded gPTP discontinuity.
    """
    import bisect
    lost = sorted((loss["index"], loss["frames"]) for loss in losses)

    def acquired(index: int) -> int:
        """The acquisition index of stored frame `index`."""
        return index + sum(frames for at, frames in lost if at <= index)

    anchors = [(0, layout.start_wall_s, layout.start_gptp_s)] + [tuple(a) for a in layout.anchors]
    starts, unsupported = [anchor[0] for anchor in anchors], 0
    for event in events:
        index = event["capture_index"]
        k = bisect.bisect_right(starts, index) - 1
        here, there = anchors[k], anchors[k + 1] if k + 1 < len(anchors) else None
        wall = gptp = None
        if here[0] == index:
            wall, gptp, timing = here[1], here[2], "anchored"
        elif there is None:
            timing = "unsupported: no anchor after the event"
        else:
            part = (acquired(index) - acquired(here[0])) / (acquired(there[0]) - acquired(here[0]))
            wall, timing = here[1] + part * (there[1] - here[1]), "anchored"
            if layout.gptp_steps_wall_s is None:
                timing = "unsupported gPTP: no discontinuity record"
            elif any(here[1] < step <= there[1] for step in layout.gptp_steps_wall_s):
                timing = "unsupported gPTP: a recorded discontinuity lies between the anchors"
            else:
                gptp = here[2] + part * (there[2] - here[2])
        unsupported += wall is None or gptp is None
        event.update(acquisition_index=acquired(index), wall_s=wall, gptp_s=gptp, timing=timing,
                     anchors=[here[0], None if there is None else there[0]],
                     context_wall_s=None if wall is None else [wall - layout.context_s, wall + layout.context_s])
    return unsupported


@dataclass(frozen=True)
class CounterCapture:
    """One counter capture as recorded: its layout, clocks and channel numbers.

    Headerless interleaved S32 in `byteorder`, at `rate_hz`. The start times
    and `anchors`, each (capture index, wall s, gPTP s) recorded by the capture
    tool, put every event on the wall and gPTP clocks; `gptp_steps_wall_s`
    lists the run's recorded gPTP discontinuities on the wall clock, None when
    no record was kept. `context_s` brackets each event. `tags` names the
    channel number each capture channel must carry, None for a channel
    without the counter; None keeps the default, index + 1.
    """
    channels: int
    byteorder: str
    rate_hz: float
    start_wall_s: float | None
    start_gptp_s: float | None
    context_s: float = 5
    tags: tuple | None = None
    anchors: tuple = ()
    gptp_steps_wall_s: tuple | None = None


@dataclass(frozen=True)
class CounterRunLog:
    """The source's planted-arm log and the capture tool's loss log.

    Arms carry class, capture index, n or mask, and channel, None for every
    counter channel; losses carry capture index and frames. None is a missing
    log and an empty list attests none. `arm_tolerance_frames` is the arm
    log's recorded index error.
    """
    planted_arms: list | None
    capture_losses: list | None
    arm_tolerance_frames: int | None


def _audio_layout_refusal(layout: CounterCapture, log: CounterRunLog, max_events: int,
                          required_s: float) -> str | None:
    """Why the layout or logs cannot be graded, or None."""
    channels, rate_hz = layout.channels, layout.rate_hz
    if (type(channels) is not int or channels < 1 or layout.byteorder not in ("big", "little")
            or not _release_finite(rate_hz) or rate_hz <= 0
            or log.planted_arms is None or log.capture_losses is None
            or type(log.arm_tolerance_frames) is not int or log.arm_tolerance_frames < 0
            or not _release_finite(layout.start_wall_s) or not _release_finite(layout.start_gptp_s)
            or not _release_finite(layout.context_s) or layout.context_s < 0
            or type(max_events) is not int or max_events < 1 or not _audio_anchors_valid(layout)):
        return "capture layout, both logs, tolerance, start times and anchors required"
    if not _release_finite(required_s) or required_s <= 0:
        return "a positive required qualified duration in seconds"
    tags = [c + 1 for c in range(channels)] if layout.tags is None else list(layout.tags)
    numbers = [tag for tag in tags if tag is not None]
    if (len(tags) != channels or not numbers
            or any(type(tag) is not int or not 1 <= tag <= AUDIO_TAG_MAX for tag in numbers)
            or len(set(numbers)) != len(numbers)):
        return "one distinct channel number from 1 to 15 per counter channel"
    if not _audio_logs_valid(log.planted_arms, log.capture_losses, channels):
        return "invalid planted-arm or capture-loss log"
    return None


def _audio_qualified(bounds: tuple[int, int], losses: list, rate_hz: float, required_s: float) -> dict:
    """The qualified interval as stated in every verdict: observed frames only."""
    start, end = bounds

    def acquired(index: int) -> int:
        """The acquisition index of stored frame `index`."""
        return index + sum(loss["frames"] for loss in losses if loss["index"] <= index)

    return {"start": start, "end": end, "frames": end - start, "seconds": (end - start) / rate_hz,
            "required_s": required_s, "guard_frames": AUDIO_GUARD_FRAMES,
            "acquisition": [acquired(start), acquired(end - 1) + 1] if end > start else [None, None],
            "unobserved_frames": sum(loss["frames"] for loss in losses if start < loss["index"] < end)}


def _audio_anchor_gaps(layout: CounterCapture, frames: int, losses: list) -> list[list[int]]:
    """[from, to] capture indices between anchors more than context_s apart.

    The capture tool owes an anchor at least every audio_context_s and one
    at the capture's end, so a stretch after the last anchor is always a gap.
    Gaps never change the verdict; events after the last anchor carry null
    times, and events in a wider gap carry times its anchors interpolate.
    """
    marks = [0] + [anchor[0] for anchor in layout.anchors]

    def acquired(index: int) -> int:
        """The acquisition index of stored frame `index`."""
        return index + sum(loss["frames"] for loss in losses if loss["index"] <= index)

    gaps = [[a, b] for a, b in zip(marks, marks[1:])
            if acquired(b) - acquired(a) > layout.context_s * layout.rate_hz]
    return gaps + ([[marks[-1], frames]] if marks[-1] != frames else [])


def grade_audio_counter_capture(capture: "bytes | Iterable[bytes]", layout: CounterCapture,
                                log: CounterRunLog, *, max_events: int = 100000,
                                required_s: float = RELEASE_SOAK_DURATION_S) -> tuple[str, dict]:
    """L3 #396 audio grader over one interleaved S32 counter capture.

    `capture` is headerless interleaved S32, the format tb/tools/thdn.py and
    the #451/#629 captures use, given as bytes or as an iterable of chunks so
    that a 24-hour file streams. The counter never repeats within a run, so
    every slip is sized exactly; a slip of whole 2048-sample blocks carries
    `located_within`, the samples it may have happened at.

    A verdict proves only its qualified interval, stated in `qualified`: from
    63 samples after the last channel's acquisition to 63 samples before the
    capture's end. PASS needs zero DUT events and at least `required_s`
    observed seconds in that interval, 24 hours by default (REQ-VER-06).

    NOT RUN: missing or inconsistent evidence, a qualified interval shorter
    than `required_s`, or a void run, where a channel never acquired the
    counter, an arm was missed or lies outside the qualified interval, or the
    arms do not run in the first and the last tenth. FAIL: any event
    attributed to neither a planted arm nor a logged capture loss.
    """
    from array import array
    detail = {"channels": layout.channels, "byteorder": layout.byteorder, "rate_hz": layout.rate_hz,
              "period_frames": AUDIO_PERIOD_FRAMES, "classes": list(AUDIO_CLASSES)}
    refusal = _audio_layout_refusal(layout, log, max_events, required_s)
    if refusal:
        return "NOT RUN", dict(detail, why=refusal)
    channels = layout.channels
    tags = [c + 1 for c in range(channels)] if layout.tags is None else list(layout.tags)
    counter_channels = [c for c, tag in enumerate(tags) if tag is not None]
    scan = _CounterScan(tags, max_events, log.planted_arms, log.arm_tolerance_frames)
    width, swap = 4 * channels, layout.byteorder != sys.byteorder
    pending, index = b"", 0
    for chunk in _audio_chunks(capture):
        data = pending + chunk
        usable = len(data) - len(data) % width
        pending = data[usable:]
        for offset in range(0, usable, AUDIO_FAST_BLOCK * width):
            words = array("I", data[offset:min(usable, offset + AUDIO_FAST_BLOCK * width)])
            if swap:
                words.byteswap()
            scan.frames(index, words)
            index += len(words) // channels
            if index > AUDIO_WINDOW_WORDS and scan.unacquired():
                return "NOT RUN", dict(detail, frames=index, unacquired=scan.unacquired(),
                                       why="void: a counter channel did not acquire the counter in its "
                                           "first 65536 frames; check the layout and byte order, and that "
                                           "the DUT drives the counter on that channel")
    if pending or index == 0:
        return "NOT RUN", dict(detail, frames=index, why="empty capture or a torn final frame")
    if index < AUDIO_CONFIRM_FRAMES or any(anchor[0] > index for anchor in layout.anchors):
        return "NOT RUN", dict(detail, frames=index, why="fewer than 64 frames, or an anchor past the capture")
    scan.finish(index)
    events = scan.events
    bounds = scan.qualified(index)
    refusal, missed = _audio_attribute(events, log, counter_channels, scan)
    unsupported = _audio_timing(events, layout, log.capture_losses)
    counts = {}
    for event in events:
        bucket = counts.setdefault(event["attribution"], {})
        bucket[event["class"]] = bucket.get(event["class"], 0) + 1
    acquired = index + sum(loss["frames"] for loss in log.capture_losses)
    detail.update(frames=index, acquired_frames=acquired, duration_s=acquired / layout.rate_hz,
                  counts=counts, events=events, unrecorded_events=scan.unrecorded, planted_missed=missed,
                  timing_unsupported=unsupported,
                  anchor_gaps=_audio_anchor_gaps(layout, index, log.capture_losses),
                  qualified=None if bounds is None else _audio_qualified(
                      bounds, log.capture_losses, layout.rate_hz, required_s))
    if bounds is None:
        return "NOT RUN", dict(detail, unacquired=scan.unacquired(),
                               why="void: a counter channel never acquired the counter; "
                                   "check the layout and byte order, and that the DUT drives the "
                                   "counter on that channel")
    start, end = bounds
    if any(not start <= loss["index"] < end for loss in log.capture_losses):
        return "NOT RUN", dict(detail, why="a logged capture loss lies outside the qualified interval")
    if refusal:
        return "NOT RUN", dict(detail, why=refusal)
    if scan.unrecorded:
        return "FAIL", dict(detail, why=f"more than {max_events} events; the excess is counted, not recorded")
    if any(not start <= arm["index"] < end for arm in log.planted_arms):
        return "NOT RUN", dict(detail, why="void: a planted arm lies outside the qualified interval")
    if missed:
        return "NOT RUN", dict(detail, why="void: a planted arm was missed")
    edge = index // AUDIO_ARM_EDGE_DIVISOR
    ends = [{arm["class"] for arm in log.planted_arms if arm["index"] < edge},
            {arm["class"] for arm in log.planted_arms if arm["index"] >= index - edge}]
    if any(end != {"dropped", "repeated", "bit-flip"} for end in ends):
        return "NOT RUN", dict(detail, why="void: drop, repeat and flip arms must run in the first "
                                           "and the last tenth of the capture")
    if counts.get("dut"):
        return "FAIL", dict(detail, why="DUT-attributed audio events")
    if end - start < required_s * layout.rate_hz:
        return "NOT RUN", dict(detail, why="the qualified interval is shorter than the required duration")
    return "PASS", dict(detail, why="zero DUT-attributed events over the qualified interval; "
                                    "every planted arm found")


def check_release_tu(interval_s: tuple[float, float], discontinuities_s: list[float], *,
                     holdover_bound_s: float, observation_resolution_s: float | None,
                     capture_complete: bool, gm_changes_s: list[float] | None = None) -> tuple[str, dict]:
    """Grade a complete wire interval and timestamped gPTP discontinuities.

    The caller records accepted IEEE 1722-2016 4.4.4.7 discontinuities on
    the capture clock. GM identity changes are supplied separately, including
    an explicit empty list when none occurred. They also count as discontinuities.
    Resolution bounds the relative event/capture error, including frame launch.
    """
    resolution_limit_s = RELEASE_TU_RESOLUTION_LIMIT_S
    detail = {"observation_resolution_s": observation_resolution_s,
              "resolution_limit_s": resolution_limit_s}
    if (capture_complete is not True or gm_changes_s is None
            or interval_s is None or discontinuities_s is None or len(interval_s) != 2):
        return "NOT RUN", dict(detail, why="complete interval, discontinuity and GM history required")
    values = (*interval_s, *discontinuities_s, *gm_changes_s, holdover_bound_s, observation_resolution_s)
    if any(not _release_finite(value) for value in values):
        return "NOT RUN", dict(detail, why="finite interval, events and resolution required")
    observed_start_s, clear_s = (Decimal(str(value)) for value in interval_s)
    if clear_s <= observed_start_s or holdover_bound_s != 0.5 or observation_resolution_s < 0:
        return "NOT RUN", dict(detail, why="ordered interval, 0.5 s release bound and nonnegative resolution required")
    if observation_resolution_s >= resolution_limit_s:
        return "NOT RUN", dict(detail, why="resolution cannot decide the tu timing limits")
    observation_resolution_s = Decimal(str(observation_resolution_s))
    holdover_bound_s = Decimal(str(holdover_bound_s))
    discontinuities_s = [Decimal(str(value)) for value in discontinuities_s]
    gm_changes_s = [Decimal(str(value)) for value in gm_changes_s]
    # Frame launch and capture can lag the event; include that measured allowance.
    start_s = observed_start_s - observation_resolution_s
    events_s = [event_s for event_s in discontinuities_s + gm_changes_s if start_s <= event_s < clear_s]
    if not events_s:
        return "FAIL", {"why": "uncorrelated tu fails", **detail}
    if min(events_s) > observed_start_s + observation_resolution_s:
        return "FAIL", dict(detail, why="tu rises before its first recorded discontinuity")
    last_discontinuity_s = max(events_s)
    deadline_s = last_discontinuity_s + holdover_bound_s + observation_resolution_s
    # Grade the latest possible true clear against the allowed true deadline.
    latest_clear_s = clear_s + observation_resolution_s
    # This single-interval entry grades every supplied GM change. The history
    # entry below assigns each change to its covering interval first.
    gm_events_s = gm_changes_s
    minimum_clear_s = max(gm_events_s) + Decimal("0.25") if gm_events_s else None
    detail.update(last_discontinuity_s=float(last_discontinuity_s), deadline_s=float(deadline_s),
                  clear_s=float(clear_s), latest_clear_s=float(latest_clear_s),
                  minimum_clear_s=float(minimum_clear_s) if gm_events_s else None)
    if minimum_clear_s is not None and clear_s + observation_resolution_s < minimum_clear_s:
        return "FAIL", dict(detail, why="tu shorter than the GM minimum")
    return ("PASS" if latest_clear_s <= deadline_s else "FAIL", detail)


def check_release_tu_history(intervals_s: list[tuple[float, float]] | None,
                             discontinuities_s: list[float] | None, *,
                             observation_resolution_s: float | None,
                             capture_complete: bool,
                             gm_changes_s: list[float] | None) -> tuple[str, dict]:
    """Grade every interval and GM change in one complete observation window.

    Empty intervals attest observed tu=0 throughout; None is missing evidence.
    Include boundary tails until every GM change's minimum can be judged.
    """
    holdover_bound_s = 0.5
    detail = {"observation_resolution_s": observation_resolution_s,
              "resolution_limit_s": RELEASE_TU_RESOLUTION_LIMIT_S}
    if (capture_complete is not True or intervals_s is None or discontinuities_s is None
            or gm_changes_s is None or not _release_finite(observation_resolution_s)
            or not 0 <= observation_resolution_s < RELEASE_TU_RESOLUTION_LIMIT_S):
        return "NOT RUN", dict(detail, why="complete history and deciding resolution required")
    if any(not _release_finite(event) for event in [*discontinuities_s, *gm_changes_s]):
        return "NOT RUN", dict(detail, why="finite event history required")
    resolution_s = Decimal(str(observation_resolution_s))
    intervals = []
    for interval in intervals_s:
        if (not isinstance(interval, (tuple, list)) or len(interval) != 2
                or any(not _release_finite(value) for value in interval)):
            return "NOT RUN", dict(detail, why="finite interval endpoints required")
        start_s, clear_s = (Decimal(str(value)) for value in interval)
        if clear_s <= start_s or (intervals and start_s <= intervals[-1][1]):
            return "NOT RUN", dict(detail, why="ordered, separate positive intervals required")
        intervals.append((start_s, clear_s))
        covered_gm_s = [event for event in gm_changes_s
                        if start_s - resolution_s <= Decimal(str(event)) < clear_s]
        verdict, evidence = check_release_tu(
            interval, discontinuities_s, holdover_bound_s=holdover_bound_s,
            observation_resolution_s=observation_resolution_s, capture_complete=True,
            gm_changes_s=covered_gm_s)
        if verdict != "PASS":
            return verdict, dict(detail, interval=interval, evidence=evidence)
    for event in gm_changes_s:
        gm_s = Decimal(str(event))
        if not any(start_s - resolution_s <= gm_s < clear_s
                   for start_s, clear_s in intervals):
            return "FAIL", dict(detail, why="GM change lacks a covering tu minimum", gm_change_s=event)
    return "PASS", dict(detail, intervals=len(intervals), gm_changes=len(gm_changes_s))


def _release_mr_records_valid(pdus: list[dict], causes: list[dict], reads: list[dict]) -> bool:
    for record in [*pdus, *causes, *reads]:
        if (not isinstance(record, dict) or not isinstance(record.get("stream_id"), str)
                or not record["stream_id"] or not _release_finite(record.get("timestamp_s"))):
            return False
    for pdu in pdus:
        if (type(pdu.get("pdu_index")) is not int or pdu["pdu_index"] < 0
                or type(pdu.get("mr")) is not int or pdu["mr"] not in (0, 1)):
            return False
    for event in causes:
        if not isinstance(event.get("kind"), str):
            return False
    for read in reads:
        if type(read.get("value")) is not int or not 0 <= read["value"] < 2**32:
            return False
    return True


def _release_mr_toggles(pdus: list[dict], causes: list[dict], resolution_s: float) -> tuple[str, dict]:
    toggles = []
    for previous, current in zip(pdus, pdus[1:]):
        if (current["pdu_index"] != previous["pdu_index"] + 1
                or current["timestamp_s"] < previous["timestamp_s"]):
            return "NOT RUN", {"why": "ordered, contiguous per-stream PDU indices required"}
        if current["mr"] != previous["mr"]:
            toggles.append(current)
    allowed = {"media-clock-source change", "CRF disruption", "CRF mr toggle"}
    # Earliest eligible cause preserves later causes for later toggles.
    causes = sorted(causes, key=lambda event: event["timestamp_s"])
    for toggle in toggles:
        matches = [event for event in causes if (event["kind"] in allowed
                   and abs(Decimal(str(event["timestamp_s"])) - Decimal(str(toggle["timestamp_s"])))
                   <= Decimal(str(resolution_s))
                   )]
        if not matches:
            return "FAIL", {"why": "mr toggle without a recorded media-clock cause", "toggle": toggle}
        causes.remove(matches[0])
    for previous, current in zip(toggles, toggles[1:]):
        if current["pdu_index"] - previous["pdu_index"] < 8:
            return "FAIL", {"why": "mr held for fewer than 8 stream PDUs", "toggle": previous}
    if toggles and pdus[-1]["pdu_index"] - toggles[-1]["pdu_index"] + 1 < 8:
        return "NOT RUN", {"why": "capture ends before the final toggle's eighth PDU"}
    return "PASS", {"toggles_s": [toggle["timestamp_s"] for toggle in toggles]}


def _release_media_resets(reads: list[dict], toggles_s: list[float], resolution_s: float) -> tuple[str, dict]:
    # Tables 5.4/5.6 update at interval end, at most one second after a toggle.
    # Each increment consumes one distinct, already cause-correlated toggle.
    # Several toggles may share a device interval; equality is not required.
    unused_s = list(toggles_s)
    increments = 0
    for before, after in zip(reads, reads[1:]):
        if after["timestamp_s"] <= before["timestamp_s"]:
            return "NOT RUN", {"why": "ordered MEDIA_RESET reads required"}
        if after["value"] < before["value"]:
            return "FAIL", {"why": "MEDIA_RESET decreased: counter reset; check talker start evidence",
                            "before": before["value"], "after": after["value"]}
        delta = after["value"] - before["value"]
        lower_s = (Decimal(str(before["timestamp_s"])) - Decimal(str(MILAN_MAX_OBSERVATION_INTERVAL_S))
                   - Decimal(str(resolution_s)))
        upper_s = Decimal(str(after["timestamp_s"])) + Decimal(str(resolution_s))
        matches_s = [event_s for event_s in unused_s if lower_s <= Decimal(str(event_s)) <= upper_s]
        if delta > len(matches_s):
            return "FAIL", {"why": "MEDIA_RESET increment without a distinct caused toggle",
                            "delta": delta, "cause_window_s": [float(lower_s), float(upper_s)]}
        for event_s in matches_s[:delta]:
            unused_s.remove(event_s)
        increments += delta
    return "PASS", {"media_reset_increments": increments}


@dataclass(frozen=True)
class ReleaseCapture:
    """Recorded capture extent, including silence, on the correlated clock."""

    window_s: tuple[float, float]
    complete: bool = True


def check_release_mr(stream_id: str, pdus: list[dict] | None, causes: list[dict] | None,
                     media_reset_reads: list[dict] | None, *, observation_resolution_s: float | None,
                     capture_complete: bool | ReleaseCapture) -> tuple[str, dict]:
    """Grade one stream and one counter endpoint from complete recorded evidence.

    PDUs carry stream_id, timestamp_s, unwrapped per-stream pdu_index and mr.
    Causes carry stream_id, timestamp_s and kind; the controller maps a source
    change or a received CRF event to each affected talker stream. Counter reads
    carry stream_id, timestamp_s and value, from one descriptor's MEDIA_RESET.
    Call separately for input and output counters, including both directions.
    Complete evidence includes the pre-window PDU, counter baseline, every PDU,
    all relevant source events, and a tail proving the final eight-PDU hold.
    None is missing evidence; an empty complete event list proves no events.
    The recorded capture window is required for silence; otherwise PDU endpoints
    supply a conservative span when no explicit capture window is supplied.
    """
    capture_window_s = None
    if isinstance(capture_complete, ReleaseCapture):
        capture_window_s = capture_complete.window_s
        capture_complete = capture_complete.complete
    # The two-sided cause window must be narrower than one counter interval.
    resolution_limit_s = MILAN_MAX_OBSERVATION_INTERVAL_S / 2
    detail = {"stream_id": stream_id, "observation_resolution_s": observation_resolution_s,
              "resolution_limit_s": resolution_limit_s,
              "cause_window": "toggle timestamp +/- observation_resolution_s",
              "counter_update_bound_s": MILAN_MAX_OBSERVATION_INTERVAL_S}
    if (capture_complete is not True or not stream_id or pdus is None or causes is None
            or media_reset_reads is None or not _release_finite(observation_resolution_s)
            or observation_resolution_s < 0):
        return "NOT RUN", dict(detail, why="complete packet, cause, counter and resolution evidence required")
    if observation_resolution_s >= resolution_limit_s:
        return "NOT RUN", dict(detail, why="resolution cannot decide the mr cause window")
    if not _release_mr_records_valid(pdus, causes, media_reset_reads):
        return "NOT RUN", dict(detail, why="invalid recorded evidence")
    stream_pdus = [pdu for pdu in pdus if pdu["stream_id"] == stream_id]
    stream_causes = [event for event in causes if event["stream_id"] == stream_id]
    reads = [read for read in media_reset_reads if read["stream_id"] == stream_id]
    if len(reads) < 2:
        return "NOT RUN", dict(detail, why="MEDIA_RESET baseline and endpoint reads required")
    if capture_window_s is None and stream_pdus:
        capture_window_s = (stream_pdus[0]["timestamp_s"], stream_pdus[-1]["timestamp_s"])
    if (capture_window_s is None or len(capture_window_s) != 2
            or any(not _release_finite(value) for value in capture_window_s)):
        return "NOT RUN", dict(detail, why="recorded capture window required")
    capture_start_s, capture_end_s = (Decimal(str(value)) for value in capture_window_s)
    required_start_s = (Decimal(str(reads[0]["timestamp_s"]))
                        - Decimal(str(MILAN_MAX_OBSERVATION_INTERVAL_S))
                        - Decimal(str(observation_resolution_s)))
    detail.update(capture_window_s=list(capture_window_s),
                  required_capture_window_s=[float(required_start_s), reads[-1]["timestamp_s"]])
    if (capture_start_s >= capture_end_s or capture_start_s > required_start_s
            or capture_end_s < Decimal(str(reads[-1]["timestamp_s"]))
            or any(not capture_start_s <= Decimal(str(pdu["timestamp_s"])) <= capture_end_s
                   for pdu in stream_pdus)):
        return "NOT RUN", dict(detail, why="capture does not span the counter-read window and PDUs")
    verdict, evidence = _release_mr_toggles(stream_pdus, stream_causes, observation_resolution_s)
    detail.update(evidence)
    if verdict != "PASS":
        return verdict, detail
    verdict, evidence = _release_media_resets(reads, detail["toggles_s"], observation_resolution_s)
    detail.update(evidence)
    return verdict, detail


def plan_soak(dut: Device = ARTY, peer: Device = PEER,
              settings: ReleaseSettings = ReleaseSettings()) -> list[Step]:
    """One continuous repeat operation, with baseline and final counter walks."""
    args = _release_args(dut, peer)
    args["evidence"].append("planted_event_log")
    args.update(duration_s=settings.soak_duration_s,
                interval_s=settings.soak_interval_s,
                release_eligible=settings.soak_duration_s >= RELEASE_SOAK_DURATION_S,
                sample_at_start=True, sample_at_end=True,
                gptp_publication=["gm", "parent", "path", "pdelay_ns",
                                  "sync", "asCapable", "tu"],
                continuous_evidence=["asCapable_transitions", "tu_intervals",
                                     "stream_flow", "uptime", "mr_pdus", "media_clock_events",
                                     "MEDIA_RESET_reads", "gptp_discontinuities", "gm_changes",
                                     "planted_events"],
                counter_oracle="check_release_soak_counters",
                zero_growth_counters=list(RELEASE_ZERO_GROWTH_COUNTERS),
                media_unlocked_rule="zero growth outside a recorded planted event, explained or not",
                planted_event_log="every deliberately planted disturbance with its target, kind "
                                  "and window_s; an empty list when none was planted",
                planted_event_reads="read the target's counters at its window's start and end; "
                                    "only an increment between two reads inside the window is excused",
                mr_oracle="check_release_mr",
                mr_capture_window="[first read - 1 s - observation_resolution_s, last read]",
                mr_distinct_causes=True,
                mr_resolution_limit_s=MILAN_MAX_OBSERVATION_INTERVAL_S / 2,
                tu_oracle="check_release_tu_history",
                tu_resolution_limit_s=RELEASE_TU_RESOLUTION_LIMIT_S,
                tu_rise_check="first discontinuity <= observed_start + observation_resolution_s",
                mr_cause_kinds=["media-clock-source change", "CRF disruption", "CRF mr toggle"],
                mr_cause_window="toggle timestamp +/- observation_resolution_s",
                mr_hold_pdus=8, mr_pdu_index="unwrapped per-stream capture index",
                mr_counter_update_bound_s=MILAN_MAX_OBSERVATION_INTERVAL_S,
                missing_evidence="NOT RUN",
                tu_gm_minimum_s=0.25,
                tu_gm_minimum_check="clear + observation_resolution_s >= GM change + 0.25 s",
                tu_holdover_bound_s=0.5,
                tu_time_origin="last recorded discontinuity before tu clears",
                tu_event_window="[observed_start - observation_resolution_s, clear)",
                tu_discontinuity_kinds=["PHC settime/adjtime", "fabric discontinuity", "GM-identity edge",
                                        "GM time-source change", "other detected gPTP discontinuity"],
                tu_observation_resolution="record wire-capture and correlated event-timestamp resolution in seconds",
                tu_uncorrelated="fail",
                timestamp_margin={"register": "AVTPRX_TSD", "offset": 0x6EC,
                                  "stream_input": 0, "units": "signed ns"})
    args["release_eligible"] &= _release_profile_eligible(settings)
    args["max_soak_interval_s"] = RELEASE_MAX_SOAK_INTERVAL_S
    args["topology_explicit"] = settings.topology_explicit
    return [Step("soak.continuous", "soak", "release_soak", args,
                 asserts=SOAK_ASSERTS, clause=RELEASE_CLAUSE,
                 note="Bind all pairs before timing; sample at each interval "
                      "and the exact endpoint, including a partial final "
                      "interval. Monitor unbound outputs too; only bound "
                      "streams owe traffic. Teardown after the final snapshot.")]


def _audio_control_fixture() -> dict:
    """A synthetic capture: arms at both ends and one unplanted DUT drop."""
    frames, channels, n = 12 * AUDIO_BLOCK_FRAMES, 8, 5
    arm_at = (100, 300, 500, frames - 900, frames - 600, frames - 300)
    kinds = ("drop", "repeat", "flip") * 2
    arms, source = [], []
    for at, kind, arm in zip(arm_at, kinds, AUDIO_PLANTED_ARMS * 2):
        channel = 2 if at < frames // 2 else 5
        arms.append(dict(arm, index=at, **({"channel": channel} if kind == "flip" else {})))
        source.append({"kind": kind, "index": at, **({"channel": channel, "mask": arm["mask"]}
                                                      if kind == "flip" else {"n": arm["n"]})})
    return {"generator": "synthesize_counter_capture", "frames": frames, "channels": channels,
            "rate_hz": 48000, "byteorder": "big", "arm_tolerance_frames": 2,
            "required_s": (frames - 2 * AUDIO_GUARD_FRAMES) / 48000,
            "planted_arms": arms, "source_events": source,
            "dut_event": {"kind": "drop", "index": 6 * AUDIO_BLOCK_FRAMES + 7, "n": n},
            "expected_events": {"class": "dropped", "n": n,
                                "capture_index": 6 * AUDIO_BLOCK_FRAMES + 7,
                                "channels": list(range(channels))}}


def _audio_release_steps(dut: Device, peer: Device, settings: ReleaseSettings) -> list[Step]:
    """Issue #396's audio-integrity run inside the soak, and its control."""
    args = _release_args(dut, peer)
    args["evidence"] += ["audio_captures", "planted_arm_log", "capture_loss_log",
                         "audio_event_records"]
    args.update(
        duration_s=settings.audio_duration_s, context_s=settings.audio_context_s,
        window="soak.continuous",
        window_rule="start after soak.continuous binds every pair and starts timing; "
                    "end at or before its endpoint; the soak outlasts duration_s by the "
                    "capture's guards and logged losses",
        release_eligible=(settings.audio_duration_s >= RELEASE_SOAK_DURATION_S
                          and _release_profile_eligible(settings)),
        topology_explicit=settings.topology_explicit,
        digital_paths=[
            {"path": "outbound", "talker": dut.entity_id, "listener": peer.entity_id,
             "capture": "an external digital capture", "byteorder": "recorded per capture"},
            {"path": "return", "talker": peer.entity_id, "listener": dut.entity_id,
             "capture": "the DUT's TDM output and the direct TDM capture (#451)",
             "byteorder": "recorded per capture"},
            {"path": "dut-tdm-loop", "talker": dut.entity_id, "listener": dut.entity_id,
             "capture": "the direct TDM capture (#451)", "byteorder": "recorded per capture"}],
        graded_pairs="every AAF pair; a CRF stream carries no audio samples",
        counter_layout={"container": "S32; 24-bit sample in bits 31:8; bits 7:0 zero",
                        "channel_field": "sample bits 15:12 = channel index + 1",
                        "position_field": "sample bits 11:1 = absolute sample position modulo 2048",
                        "code_field": "sample bit 0 = bit (n mod 32) of block (n div 2048)'s code, "
                                      "the block number times 0x9E3779B1 modulo 2^32",
                        "period_frames": AUDIO_PERIOD_FRAMES,
                        "period_rate_basis": "Milan v1.2 6.2 Table 6.1: 48, 96 and 192 kHz; "
                                             "2^43 samples is about 530 days at 192 kHz"},
        counter_grader="grade_audio_counter_capture",
        counter_grader_required_s=settings.audio_duration_s,
        counter_classes=list(AUDIO_CLASSES),
        qualification=dict(AUDIO_QUALIFICATION, required_s=settings.audio_duration_s),
        counter_limits=list(AUDIO_COUNTER_LIMITS),
        planted_arms=[dict(arm) for arm in AUDIO_PLANTED_ARMS],
        planted_placement="a drop, a repeat and a flip in the first tenth of the capture and "
                          "again in its last tenth, inside the qualified interval, logged with "
                          "capture index, channel and size or mask",
        planted_missed="void: NOT RUN",
        capture_start="once the counter flows on every channel; words before a channel's "
                      "acquisition are graded against the track it acquires, so leading silence "
                      "fails; a channel that has not acquired within 65536 frames voids the run",
        capture_losses="logged by the capture tool inside the qualified interval; attributed to the "
                       "capture and reported apart; a loss advances the acquisition index and both clocks",
        capture_timing={"anchors": "capture index, wall s and gPTP s recorded by the capture tool "
                                   "at most audio_context_s apart and at the capture's end",
                        "gptp_steps": "the soak's recorded gPTP discontinuities on the wall clock",
                        "rule": "interpolate between the anchors around an event; never "
                                "extrapolate; gPTP never across a recorded discontinuity; "
                                "an unsupported time is null with its reason"},
        event_record=["wall_s", "gptp_s", "capture_index", "acquisition_index", "expected",
                      "received", "class", "located_within", "timing"],
        event_context={"counter_walk": "every stream and the CRF sink",
                       "csr": {"SLIP_LB": 0x8D4, "SLIP_TDM": 0x8D8},
                       "gptp": "publication and transition state",
                       "max_gap_s": settings.audio_context_s},
        analog={"tones_hz": [997, 9973], "path": "the analog chain, converters included",
                "grading": ["THD+N per block", "sample-exact predictor residual"],
                "limits": None, "limits_status": "undecided on #396; NOT RUN until decided"},
        pass_rule="zero DUT-attributed events on every bound channel, both directions, "
                  "with every planted arm found, over a qualified interval of at least "
                  "required_s observed seconds")
    control = {"control_of": "audio.integrity", "expected_failing_assertion": "audio.zero-dut-glitches",
               "expected_verdict": "FAIL", "oracle": "grade_audio_counter_capture",
               "offline": True, "context_s": settings.audio_context_s,
               "fixture": _audio_control_fixture()}
    return [
        Step("audio.integrity", "audio", "release_audio_integrity", args,
             asserts=AUDIO_RELEASE_ASSERTS, clause=AUDIO_RELEASE_CLAUSE, needs_human=True,
             human_action="Feed the counter source and the sine pair, start every capture, "
                          "and plant the logged arms at the start and the end of the run.",
             note="Runs concurrently with soak.continuous, inside its window. Grade "
                  "every capture offline; walk counters, SLIP words and gPTP state "
                  "at most context_s apart throughout."),
        Step("audio.control.planted-drop", "audio", RELEASE_CONTROL_OP, control,
             asserts=(A_RELEASE_CONTROL, _spec(AUDIO_RELEASE_ASSERTS, "audio.zero-dut-glitches"),
                      _spec(AUDIO_RELEASE_ASSERTS, "audio.counter-classified")),
             clause=AUDIO_RELEASE_CLAUSE + "; issue #396 acceptance 4",
             note="Graded offline on a synthetic capture: the unplanted drop must FAIL "
                  "and be classified exactly, every arm found.")]


def plan_power(dut: Device = ARTY, peer: Device = PEER,
               settings: ReleaseSettings = ReleaseSettings()) -> list[Step]:
    """Serial cycles; each phase repeats the full before/after contract.

    Two phases are cold cuts from the power strip and one is soft resets with
    power held on. The negative controls follow as their own entries.
    """
    steps = []
    minimum = dict(RELEASE_POWER_PHASES)
    for phase, count in (("idle", settings.idle_cycles),
                         ("journal_commit", settings.commit_cycles),
                         ("soft_reset", settings.reset_cycles)):
        cold = phase != "soft_reset"
        args = _release_args(dut, peer)
        args["evidence"].append("power_strip_log" if cold else "reset_command_log")
        args.update(cycles=count, total_cycles=settings.power_cycles,
                    phase=phase, cold=cold, soft_reset=not cold,
                    cycle_kind="cold cut" if cold else "soft reset",
                    outlet_role="dut")
        if cold:
            args.update(power_off_hold_s=settings.power_off_hold_s,
                        power_off_hold_origin="phys.dut-cycle.power-cycle: default 8 s; verify discharge",
                        power_off_hold_in_adp_window=False,
                        cold_confirmation="power removed; discharge verified",
                        time_origin="T0: power-strip ON command, host monotonic clock")
        else:
            args.update(reset_method="bench-declared reset with power held on; record the "
                                     "mechanism, its command timestamp and the outlet state per cycle",
                        cold_confirmation="power held on; outlet ON before and after the reset",
                        time_origin="T0: reset command, host monotonic clock")
        args.update(boot_observation_s=settings.restore_bound_s + settings.boot_margin_s,
                    boot_margin_s=settings.boot_margin_s,
                    restore_bound_s=settings.restore_bound_s,
                    restore_bound_provisional=True,
                    restore_bound_origin="issue #396 round 2; ratify with #397 and #75",
                    boot_observation_origin="restore_bound_s + boot_margin_s from T0",
                    restore_start="T0",
                    restore_end="first valid AVTP PDU of each persisted binding",
                    restore_limit_exclusive=False,
                    restore_requires="automatic; no controller repair; both directions and CRF",
                    boot_max_passes=1, boot_max_restarts=0,
                    boot_evidence="complete UART/reset observation from T0 through next cycle or campaign end; "
                                  "at least boot_observation_s",
                    persisted_items=list(settings.persisted_items),
                    persisted_item_clauses={item: RELEASE_PERSISTED_ITEMS.get(item, "project inventory")
                                            for item in settings.persisted_items},
                    state_oracle="check_release_state_restored",
                    state_values="set every item away from its default before the cycle",
                    release_eligible=(settings.power_cycles >= ReleaseSettings.power_cycles
                                      and settings.idle_cycles >= minimum["idle"]
                                      and settings.commit_cycles >= minimum["journal_commit"]
                                      and settings.reset_cycles >= minimum["soft_reset"]),
                    cut_requires=("journal_commit_window" if phase == "journal_commit"
                                  else "journal_idle"),
                    cut_evidence=("ReleaseCommitCut: the pending snapshot, the commit window "
                                  "[start, end) and the cut instant on the T0 clock; a cut "
                                  "outside the window hit no journal commit"
                                  if phase == "journal_commit" else None),
                    pending_values=("set every pending item away from its default"
                                    if phase == "journal_commit" else None),
                    adp_reference="last pre-cut DUT ENTITY_AVAILABLE, host timestamp and raw PDU",
                    adp_valid_time_unit_s=2,
                    adp_required_valid_time=10,
                    adp_start="T0",
                    adp_deadline="2 * pre_cut_valid_time",
                    adp_elapsed="first_post_cut_available_host_s - t0_host_s",
                    adp_limit_exclusive=True,
                    adp_missing_or_expired="fail; require captured valid_time=10 and arrival before T0 deadline",
                    rebind_limit_s=1, rebind_limit_exclusive=True,
                    rebind_start="CONNECT_RX success",
                    rebind_end="first valid AVTP PDU",
                    rebind_requires="automatic restoration passed for every persisted binding",
                    snapshot_policy=("complete old or new committed snapshot"
                                     if phase == "journal_commit"
                                     else "exact pre-cut committed snapshot"))
        args["release_eligible"] &= _release_profile_eligible(settings)
        args["topology_explicit"] = settings.topology_explicit
        steps.append(Step(
            "power." + phase, "power", "release_power_cycles", args,
            asserts=POWER_ASSERTS, clause=RELEASE_CLAUSE, needs_human=True,
            human_action=("Provide the bench power-strip hook and timestamped "
                          "cut-phase evidence; then run unattended cold cuts." if cold else
                          "Provide the bench reset hook with power held on and "
                          "timestamped reset evidence; then run unattended soft resets."),
            note=("Each cycle: establish pairs and saved state, snapshot, prove "
                  "cut phase, remove power, confirm discharge, restore power, "
                  "observe boot, verify automatic restore, measure reconnect, "
                  "walk all counters. No next cut before verification finishes. "
                  "Missing journal instrumentation leaves qualification open." if cold else
                  "Each cycle: establish pairs and saved state, snapshot, issue the "
                  "reset with power held on, observe boot, verify automatic restore, "
                  "measure reconnect, walk all counters. No next cycle before "
                  "verification finishes.")))
    return steps + _power_controls(dut, peer, settings)


def _spec(asserts: Sequence[AssertSpec], name: str) -> AssertSpec:
    return next(spec for spec in asserts if spec.name == name)


def _power_controls(dut: Device, peer: Device, settings: ReleaseSettings) -> list[Step]:
    """Acceptance 4's two power-campaign controls, each with its failing assertion.

    The desk fixture is the defect's signature for the named oracle, so the
    offline suite proves the assertion can fail on it; the bench run against
    the known-defect image is #396 part B.
    """
    items = list(settings.persisted_items)
    common = {"control_of": "power.idle", "phase": "idle", "cycles": 1,
              "expected_verdict": "FAIL", "pairs": _release_pairs(dut, peer),
              "evidence": ["image_hashes", "manifest", "verdict_jsonl", "uart_transcript",
                           "controller_log", "timestamped_snapshots"]}
    return [
        Step("power.control.first-boot-restart", "power", RELEASE_CONTROL_OP,
             dict(common, image="the shipping pair, first cold boot after its flash-pair (#366)",
                  expected_failing_assertion="power.single-boot", oracle="check_release_boot",
                  desk_fixture={"boot_passes": 2, "restarts": 1, "capture_complete": True},
                  retain="flash-to-first-cold-boot provenance and uninterrupted UART capture"),
             asserts=(A_RELEASE_CONTROL, _spec(POWER_ASSERTS, "power.single-boot")),
             clause=RELEASE_CLAUSE + "; issue #366", needs_human=True,
             human_action="Flash the shipping pair, then run one cold cut with "
                          "complete UART capture from T0.",
             note="Only the first cold boot after a flash shows the restart, so the "
                  "control is exactly one cycle after the flash."),
        Step("power.control.persistence-disabled", "power", RELEASE_CONTROL_OP,
             dict(common, image="a build with persistence disabled",
                  expected_failing_assertion="power.state-restored",
                  oracle="check_release_state_restored",
                  desk_fixture={"items": items,
                                "pre": {item: "set" for item in items},
                                "post": {item: "default" for item in items},
                                "defaults": {item: "default" for item in items}}),
             asserts=(A_RELEASE_CONTROL, _spec(POWER_ASSERTS, "power.state-restored")),
             clause=RELEASE_CLAUSE + "; issue #70", needs_human=True,
             human_action="Flash a persistence-disabled build, set every inventory "
                          "item away from its default, then run one cold cut.",
             note="Every item reads back at its default, which the restore "
                  "assertion must fail."),
    ]


def run_release_control(step: Step) -> tuple[str, dict]:
    """Run one control's desk fixture through its oracle; the verdict it earns."""
    args = step.args
    fixture = args.get("desk_fixture") or args.get("fixture")
    if step.op != RELEASE_CONTROL_OP or not isinstance(fixture, dict):
        return "NOT RUN", {"why": "not a negative control with a desk fixture"}
    if args.get("oracle") == "check_release_boot":
        return check_release_boot(fixture["boot_passes"], fixture["restarts"],
                                  capture_complete=fixture["capture_complete"])
    if args.get("oracle") == "check_release_state_restored":
        return check_release_state_restored(fixture["pre"], fixture["post"], fixture["defaults"],
                                            items=fixture["items"], phase=args["phase"])
    if args.get("oracle") == "grade_audio_counter_capture":
        capture = synthesize_counter_capture(
            fixture["frames"], fixture["channels"], byteorder=fixture["byteorder"],
            events=fixture["source_events"] + [fixture["dut_event"]])
        return grade_audio_counter_capture(
            capture, CounterCapture(fixture["channels"], fixture["byteorder"], fixture["rate_hz"],
                                    0.0, 0.0, args["context_s"]),
            CounterRunLog(fixture["planted_arms"], [], fixture["arm_tolerance_frames"]),
            required_s=fixture["required_s"])
    return "NOT RUN", {"why": f"unknown oracle {args.get('oracle')!r}"}


def _release_coverage(step: Step, dut: Device, peer: Device) -> dict:
    """Audit observations separately from bindings so neither masks the other."""
    missing = {}
    targets = step.args.get("counter_targets", [])
    for role, device in (("dut", dut), ("peer", peer)):
        for kind, descriptor, indices in (
                ("talker", "stream_output", device.talker_indices()),
                ("listener", "stream_input", device.listener_indices())):
            seen = {t.get("index") for t in targets
                    if t.get("entity") == device.entity_id
                    and t.get("descriptor") == descriptor}
            absent = sorted(set(indices) - seen)
            if absent:
                missing[role + "_" + kind] = absent
    pairs = step.args.get("pairs", [])
    for direction, talker, listener in (("outbound", dut, peer),
                                        ("return", peer, dut)):
        directional = [p for p in pairs if p.get("talker") == talker.entity_id
                       and p.get("listener") == listener.entity_id]
        if not any(p.get("talker_index") in talker.talker_indices(False)
                   and p.get("listener_index") in listener.listener_indices(False)
                   for p in directional):
            missing[direction] = "missing AAF binding"
        if (talker.crf_out is None or listener.crf_in is None
                or not any(p.get("talker_index") == talker.crf_out
                           and p.get("listener_index") == listener.crf_in
                           for p in directional)):
            missing[direction + "_crf"] = "missing CRF binding"
    return missing


AREAS = {
    "matrix": plan_matrix,
    "multi": plan_multi,
    "churn": plan_churn,
    "payload": plan_payload,
    "audio": plan_audio,
    "torture": plan_torture,
    "soak": plan_soak,
    "power": plan_power,
    #: LAST on purpose, and load-bearing: build_plan() emits areas in THIS
    #: order, and a switch partition or a DUT power cycle mid-matrix would
    #: pollute every verdict that follows it.  The runner additionally never
    #: drives two outlets concurrently.
    "physical": plan_physical,
}


def build_plan(areas: Iterable[str] | None = None, dut: Device = ARTY,
               peer: Device = PEER, *,
               release: ReleaseSettings = ReleaseSettings()) -> list[Step]:
    """The whole campaign, or the named areas, in execution order."""
    want = list(AREAS) if not areas else list(areas)
    bad = [a for a in want if a not in AREAS]
    if bad:
        raise ValueError(f"unknown area(s) {bad}; known: {sorted(AREAS)}")
    out = []
    for a in want:
        fn = AREAS[a]
        if a in ("soak", "audio", "power"):
            out += fn(dut, peer, release)
            continue
        try:
            out += fn(dut, peer)
        except TypeError:
            out += fn(dut)
    return out


# ------------------------------------------------------------- plan auditing --
def plan_covers_every_index(plan: Iterable[Step], dut: Device = ARTY,
                            peer: Device = PEER) -> dict[str, list[int]]:
    """Which talker/listener indices the plan actually touches.

    This is the audit that makes the standing "never index 0 only" rule
    executable at a desk instead of a habit.
    """
    seen = {"dut_talker": set(), "dut_listener": set(),
            "peer_talker": set(), "peer_listener": set()}
    for s in plan:
        a = s.args
        for target in a.get("counter_targets", []):
            for role, device in (("dut", dut), ("peer", peer)):
                if target.get("entity") == device.entity_id:
                    kind = {"stream_input": "listener",
                            "stream_output": "talker"}.get(target.get("descriptor"))
                    if kind is not None:
                        seen[role + "_" + kind].add(target["index"])
        t, ti = a.get("talker"), a.get("talker_index")
        l, li = a.get("listener"), a.get("listener_index")
        if t == dut.entity_id and ti is not None:
            seen["dut_talker"].add(ti)
        if t == peer.entity_id and ti is not None:
            seen["peer_talker"].add(ti)
        if l == dut.entity_id and li is not None:
            seen["dut_listener"].add(li)
        if l == peer.entity_id and li is not None:
            seen["peer_listener"].add(li)
        for tk in a.get("talkers", []):
            if tk.get("entity") == peer.entity_id:
                seen["peer_talker"].add(tk["index"])
            if tk.get("entity") == dut.entity_id:
                seen["dut_talker"].add(tk["index"])
        # the multi area's steps carry SETS of pairs, and the staged teardown
        # carries the torn-down pair and the survivors separately
        for p in (list(a.get("pairs", [])) + list(a.get("survivors", []))
                  + ([a["unbind"]] if isinstance(a.get("unbind"), dict)
                     else [])):
            t2, ti2 = p.get("talker"), p.get("talker_index")
            l2, li2 = p.get("listener"), p.get("listener_index")
            if t2 == dut.entity_id and ti2 is not None:
                seen["dut_talker"].add(ti2)
            if t2 == peer.entity_id and ti2 is not None:
                seen["peer_talker"].add(ti2)
            if l2 == dut.entity_id and li2 is not None:
                seen["dut_listener"].add(li2)
            if l2 == peer.entity_id and li2 is not None:
                seen["peer_listener"].add(li2)
    return {k: sorted(v) for k, v in seen.items()}


def plan_coverage_by_area(plan: Iterable[Step], dut: Device = ARTY,
                          peer: Device = PEER
                          ) -> dict[str, dict[str, list[int]]]:
    """The same audit, PER AREA - which is the only form that can say no.

    plan_covers_every_index() over the WHOLE plan is structurally blind: the
    matrix area walks every index, so its coverage MASKS every other area.  The
    audio area was index-0-only for exactly that reason and the audit reported
    full coverage.  An audit that cannot fail on the area you care about is the
    same defect class as an assertion that cannot fail.
    """
    areas = {}
    for s in plan:
        areas.setdefault(s.area, []).append(s)
    return {a: plan_covers_every_index(ss, dut, peer)
            for a, ss in sorted(areas.items())}


def area_index_expectations(dut: Device = ARTY, peer: Device = PEER) -> dict:
    """What EACH AREA is expected to walk, stated per area so the audit can say
    no about the area you care about.

    The expectations differ because the areas differ, and pretending otherwise
    would produce false reds instead of real ones:
      * matrix - the full cross product, every index, CRF included;
      * multi - every reachable PEER listener fed concurrently (the primaries
        set), every DUT AAF listener a talker can reach (the selfloop set),
        and every DUT AAF talker those two sets need; CRF EXCLUDED - a CRF
        pair inside an AAF concurrency set would poison it with conformant
        format refusals, and the CRF stream has its own matrix cells;
      * churn - every DUT listener index (the implicit rebind is a listener-side
        transition) and every peer talker index (the storm rotates them);
      * payload - every DUT talker index, CRF included (the CRF capture has its
        own Milan 7.3.2 expectations);
      * audio - every AAF talker index and every AAF DUT listener index, CRF
        EXCLUDED: a CRF Media Clock Stream carries timestamps, not audio
        samples, so there is no channel identity to check on it;
      * torture - not per-index by nature; the adverse conditions apply to the
        device, and an empty expectation says so out loud instead of silently.
    """
    aaf_t = dut.talker_indices(include_crf=False)
    aaf_l = dut.listener_indices(include_crf=False)
    p_l = peer.listener_indices(include_crf=False)
    return {
        "matrix": {"dut_talker": dut.talker_indices(),
                   "dut_listener": dut.listener_indices(),
                   "peer_talker": peer.talker_indices(),
                   "peer_listener": peer.listener_indices()},
        # stated independently of the pair builders on purpose: an expectation
        # derived from the same code it audits is a tautology that can never
        # say no
        "multi": {"dut_talker": (aaf_t if len(aaf_t) <= max(len(p_l),
                                                            len(aaf_l), 1)
                                 else sorted(set(aaf_t[:len(p_l)])
                                             | set(aaf_t[:len(aaf_l)]))),
                  "dut_listener": aaf_l[:len(aaf_t)] if aaf_t else [],
                  "peer_listener": p_l,
                  # the stress set's inbound leg: after the outbound fill
                  # consumes max(0, talkers - peer listeners) DUT listeners
                  # as self-loops, the peer's talkers take what is left
                  "peer_talker": peer.talker_indices(include_crf=False)[
                      :max(0, len(aaf_l) - max(0, len(aaf_t) - len(p_l)))]},
        "churn": {"dut_listener": dut.listener_indices(include_crf=False),
                  "peer_talker": peer.talker_indices()},
        "payload": {"dut_talker": dut.talker_indices()},
        "audio": {"dut_talker": dut.talker_indices(include_crf=False),
                  "dut_listener": [i for i in
                                   dut.listener_indices(include_crf=False)
                                   if i < peer.listeners]},
        "torture": {},
        "soak": {"dut_talker": dut.talker_indices(),
                 "dut_listener": dut.listener_indices(),
                 "peer_talker": peer.talker_indices(),
                 "peer_listener": peer.listener_indices()},
        "power": {"dut_talker": dut.talker_indices(),
                  "dut_listener": dut.listener_indices(),
                  "peer_talker": peer.talker_indices(),
                  "peer_listener": peer.listener_indices()},
        # not per-index by nature either: the physical family's proof pair
        # deliberately walks ONE pair (the highest AAF indices - never the
        # index-0 alias path), and full per-index coverage already belongs to
        # the matrix that ran before the power was touched
        "physical": {},
    }


def area_covers_every_index(plan: Iterable[Step], area: str,
                            dut: Device = ARTY, peer: Device = PEER, *,
                            expect: dict[str, list[int]] | None = None
                            ) -> tuple[bool, dict[str, object]]:
    """(ok, detail) for ONE area against that area's own expectation.

    The audio area's identity expectation is judged without its release
    steps: their counter targets walk every index and would otherwise mask an
    index-0-only identity loop. The release steps carry their own audit.
    """
    plan = list(plan)
    scoped = plan if area != "audio" else [
        s for s in plan if s.op not in RELEASE_REQUIRED_ASSERTS and s.op != RELEASE_CONTROL_OP]
    cov = plan_coverage_by_area(scoped, dut, peer).get(area, {})
    want = expect if expect is not None else \
        area_index_expectations(dut, peer).get(area, {})
    missing = {k: sorted(set(v) - set(cov.get(k, []))) for k, v in want.items()}
    missing = {k: v for k, v in missing.items() if v}
    if area in ("soak", "audio", "power"):
        missing.update(_release_area_defects(area, [s for s in plan if s.area == area],
                                             dut, peer))
    return (not missing, {"area": area, "covered": cov, "expected": want,
                          "missing": missing})


def _release_area_defects(area: str, steps: list[Step], dut: Device, peer: Device) -> dict:
    """Issue #396's per-area contract: repeats, assertions, cycle mix, controls."""
    defects = {}
    repeats = [s for s in steps if s.op in RELEASE_REQUIRED_ASSERTS]
    if not repeats:
        defects["release"] = "no release repeat in this area"
    for step in repeats:
        found = _release_coverage(step, dut, peer)
        owed = RELEASE_REQUIRED_ASSERTS[step.op] - {
            spec.name for spec in step.asserts if spec.severity == "SHALL"}
        if owed:
            found["asserts"] = sorted(owed)
        if found:
            defects[step.sid] = found
    if area == "power":
        if sorted(s.args.get("phase") for s in repeats) != sorted(p for p, _ in RELEASE_POWER_PHASES):
            defects["phases"] = "idle, journal_commit and soft_reset are each required once"
        totals = {s.args.get("total_cycles") for s in repeats}
        if len(totals) != 1 or sum(s.args.get("cycles", 0) for s in repeats) not in totals:
            defects["cycle_mix"] = "the phase cycles must add up to total_cycles"
    for sid in RELEASE_CONTROLS.get(area, ()):
        control = next((s for s in steps if s.sid == sid and s.op == RELEASE_CONTROL_OP), None)
        if (control is None or control.args.get("expected_verdict") != "FAIL"
                or control.args.get("expected_failing_assertion")
                not in {spec.name for spec in control.asserts}):
            defects[sid] = "negative control missing or not carrying its failing assertion"
    return defects


def human_steps(plan: Iterable[Step]) -> list[Step]:
    """The steps no runner can execute: a cable moved, an outlet cut, a box
    reconfigured.  They stay IN the plan so a bench without the powerstrip
    hook hands them back as NEEDS-HUMAN instead of dropping them."""
    return [s for s in plan if s.needs_human]


def checklist_text(plan: Iterable[Step]) -> str:
    """The printable checklist for the entries a human has to perform.

    These are emitted rather than silently skipped: a skipped adverse-condition
    entry that nobody sees is how "we tested link loss" becomes true in a
    report and false on the bench.
    """
    hs = human_steps(plan)
    if not hs:
        return "No human-action entries in this plan.\n"
    lines = ["MILAN TORTURE CAMPAIGN - HUMAN ACTION CHECKLIST",
             "=" * 62,
             f"{len(hs)} entries need a person at the bench: a cable moved,",
             "power cut, or another box reconfigured.  The physical-area",
             "power cycles run AUTOMATED instead when the runner is given",
             "--powerstrip-cmd (with --switch-outlet / --dut-outlet); the",
             "cable pulls always need a person.  Run the software areas",
             "first, then work down this list, re-running the named area",
             "after each.",
             ""]
    for i, s in enumerate(hs, 1):
        lines.append(f"[ ] {i}. {s.sid}")
        lines.append(f"       DO: {s.human_action}")
        lines.append(f"       THEN ASSERT: "
                     + "; ".join(a.name for a in s.asserts))
        lines.append(f"       CLAUSE: {s.clause}")
        if s.note:
            lines.append(f"       NOTE: {s.note}")
        lines.append("")
    return "\n".join(lines)


# ------------------------------------------------------------------ verdicts --
#: Every field of a verdict line beyond the three that identify it, with the
#: value a line carries when the caller says nothing.  A keyword that is NOT
#: one of these is the caller's own evidence and lands in `detail`, which is
#: what lets a runner attach whatever it measured without this shape growing a
#: parameter per measurement.
VERDICT_FIELDS = {"clause": "", "severity": "SHALL", "area": "", "run": ""}


def verdict_record(step_id: str, assertion: str, verdict: str, **fields) -> dict:
    """The JSONL verdict shape every consumer emits.

    One line per ASSERTION, not per step: a step that emits one line can only
    report its worst outcome, and a morning diff then cannot tell which
    assertion changed.  `run` is a caller-supplied run id so two mornings sort.
    Named fields are the keywords in `VERDICT_FIELDS`; every other keyword is
    evidence and goes to `detail`.
    """
    named = {k: fields.get(k, d) for k, d in VERDICT_FIELDS.items()}
    detail = {k: v for k, v in fields.items() if k not in VERDICT_FIELDS}
    return {"schema": "milan-torture/1", "run": named["run"], "step": step_id,
            "area": named["area"], "assertion": assertion, "verdict": verdict,
            "severity": named["severity"], "clause": named["clause"],
            "detail": detail}


VERDICTS = ("PASS", "FAIL", "NOT RUN", "SKIP", "INFO", "KNOWN-PENDING",
            "CONFORMANT-REFUSAL", "NEEDS-HUMAN", INSTRUMENT_SUSPECT)


def exit_code(records: Sequence[dict[str, object]]) -> int:
    """0 all good; 1 a SHALL-severity FAIL; 2 only RECOMMENDED failures or
    NEEDS-HUMAN or NOT RUN entries outstanding. A SKIP alone never fails the run - it is
    honest - but it is counted in the summary so it cannot hide.

    INSTRUMENT-SUSPECT never fails the run either, for the same reason: it says
    the TEST MACHINE lost frames, so the measurement is inadmissible.  Grading it
    as a device failure would be reporting the instrument's defect against the
    device - and it is counted in the summary, so a run that is all suspect
    cannot read as a clean one."""
    hard = any(r["verdict"] == "FAIL" and r.get("severity") == "SHALL"
               for r in records)
    soft = any(r["verdict"] in ("FAIL", "NEEDS-HUMAN", "NOT RUN") for r in records)
    return 1 if hard else (2 if soft else 0)


def summarise(records: Sequence[dict[str, object]]) -> dict[str, int]:
    """One count per verdict, plus the total and the exit code the run earns.

    EVERY verdict gets a key, including the ones that never fail a run: a SKIP
    or an INSTRUMENT-SUSPECT that is invisible in the summary is how a run
    that measured nothing reads as a clean one.
    """
    out = {v: 0 for v in VERDICTS}
    for r in records:
        out[r["verdict"]] = out.get(r["verdict"], 0) + 1
    out["total"] = len(records)
    out["exit_code"] = exit_code(records)
    return out


# ------------------------------------------------------------------ self test --
class _CounterLawChecks:
    """The counter tables, their payload decode and their per-counter update laws.

    A mixin, not a TestCase: `self_test` combines the five into the one
    `T` whose name the report prints, so the arms can be read apart
    without a single line of that report changing.
    """
    def test_counter_tables_match_the_standards(self) -> None:
        """The four counter tables still hold what the two standards define, and
        the Milan ten still fold to the 0xF3F wire mask the graders compare."""
        self.assertEqual(len(MILAN_TABLE_56), 10)
        self.assertEqual(len(MILAN_TABLE_54), 5)
        self.assertEqual(len(IEEE_STREAM_INPUT_BLOCK), 12)
        self.assertEqual(len(IEEE_STREAM_OUTPUT_BLOCK), 8)
        # the Milan ten, as a wire mask, is 0xF3F: bits 6/7 (the two tv
        # tallies) are the only holes
        self.assertEqual(
            counters_valid_mask(MILAN_TABLE_56, IEEE_STREAM_INPUT_BLOCK),
            MILAN_INPUT_MANDATORY_MASK)
        self.assertEqual(
            counters_valid_mask(IEEE_STREAM_INPUT_BLOCK,
                                IEEE_STREAM_INPUT_BLOCK),
            MILAN_INPUT_FULL_MASK)
        self.assertEqual(
            counters_valid_mask(MILAN_TABLE_54, MILAN_TABLE_54),
            MILAN_OUTPUT_MASK)

    def test_counters_payload_decode_and_unnamed_slots(self) -> None:
        """A GET_COUNTERS payload decodes BY NAME: an unclaimed slot is absent
        rather than reported as 0, and a slot the layout cannot name is
        reported rather than dropped - it means device and reader disagree."""
        pay = bytearray(8 + 128)
        pay[0:2] = (0x0005).to_bytes(2, "big")
        pay[2:4] = (0x0003).to_bytes(2, "big")
        pay[4:8] = MILAN_INPUT_FULL_MASK.to_bytes(4, "big")
        for i, v in enumerate(range(1, 13)):
            pay[8 + 4 * i:12 + 4 * i] = v.to_bytes(4, "big")
        d = decode_counters_payload(bytes(pay), IEEE_STREAM_INPUT_BLOCK)
        self.assertEqual(d["descriptor_index"], 3)
        self.assertEqual(d["decoded"]["MEDIA_LOCKED"], 1)
        self.assertEqual(d["decoded"]["FRAMES_RX"], 12)
        self.assertEqual(d["claimed_but_unnamed_slots"], [])
        # a mask claiming a slot the layout does not name is REPORTED, not
        # dropped: it means the device and the reader disagree on layout
        pay[4:8] = (MILAN_INPUT_FULL_MASK | (1 << 20)).to_bytes(4, "big")
        d = decode_counters_payload(bytes(pay), IEEE_STREAM_INPUT_BLOCK)
        self.assertEqual(d["claimed_but_unnamed_slots"], [20])
        # an unclaimed slot is ABSENT, never reported as 0 (methodology R5)
        pay[4:8] = (0x001).to_bytes(4, "big")
        d = decode_counters_payload(bytes(pay), IEEE_STREAM_INPUT_BLOCK)
        self.assertEqual(list(d["decoded"]), ["MEDIA_LOCKED"])
        with self.assertRaises(ValueError):
            decode_counters_payload(b"\x00" * 12, IEEE_STREAM_INPUT_BLOCK)

    def test_lock_and_talker_invariants(self) -> None:
        """Both Milan state invariants grade their legal shapes AND their illegal
        ones, and an unread counter pair SKIPs instead of passing."""
        self.assertEqual(check_lock_invariant(
            {"MEDIA_LOCKED": 5, "MEDIA_UNLOCKED": 4})[0], "PASS")
        self.assertEqual(check_lock_invariant(
            {"MEDIA_LOCKED": 4, "MEDIA_UNLOCKED": 4})[0], "PASS")
        self.assertEqual(check_lock_invariant(
            {"MEDIA_LOCKED": 6, "MEDIA_UNLOCKED": 4})[0], "FAIL")
        self.assertEqual(check_lock_invariant(
            {"MEDIA_LOCKED": 3, "MEDIA_UNLOCKED": 4})[0], "FAIL")
        self.assertEqual(check_lock_invariant({})[0], "SKIP")
        self.assertEqual(check_talker_invariant(
            {"STREAM_START": 3, "STREAM_STOP": 2})[0], "PASS")
        self.assertEqual(check_talker_invariant(
            {"STREAM_START": 3, "STREAM_STOP": 1})[0], "FAIL")

    def test_tv_tnv_grades_settled_and_coalesced_packet_snapshots(self) -> None:
        """A single coalesced snapshot cannot establish a packet-rate defect."""
        # 1722.1 per-frame reading: the identity is exact
        v, d = check_tv_tnv({"TIMESTAMP_VALID": 1000,
                             "TIMESTAMP_NOT_VALID": 0, "FRAMES_RX": 1000})
        self.assertEqual((v, d["reading"]), ("PASS", "1722.1-per-frame"))
        # Superseded interval reading: 8000 frames in 1 s, RX ticks once.
        v, d = check_tv_tnv({"TIMESTAMP_VALID": 8000,
                             "TIMESTAMP_NOT_VALID": 0, "FRAMES_RX": 1})
        self.assertEqual((v, d["reading"]), ("INFO", "unequal-packet-totals"))
        # neither reading permits FRAMES_RX above TV+TNV
        self.assertEqual(check_tv_tnv({"TIMESTAMP_VALID": 5,
                                       "TIMESTAMP_NOT_VALID": 0,
                                       "FRAMES_RX": 99})[0], "FAIL")
        self.assertEqual(check_tv_tnv({})[0], "SKIP")

    def test_unpublished_zero_receive_snapshot(self) -> None:
        """Real startup boundary: three accepted packets precede RX publication."""
        for packets in (1, 2, 3):
            sample = {"TIMESTAMP_VALID": packets, "TIMESTAMP_NOT_VALID": 0, "FRAMES_RX": 0}
            verdict, detail = check_tv_tnv(sample)
            self.assertEqual(verdict, "INFO", "[726 SNAPSHOT] unpublished zero")
            self.assertIsNone(detail["ratio"])
        sample = {"TIMESTAMP_VALID": 3, "TIMESTAMP_NOT_VALID": 0, "FRAMES_RX": 3}
        self.assertEqual(check_tv_tnv(sample)[0], "PASS")
        self.assertEqual(check_tv_tnv(dict.fromkeys(sample, 0))[0], "SKIP")
        self.assertEqual(check_tv_tnv({})[0], "SKIP")
        self.assertEqual(grade_counter_semantics(
            "FRAMES_RX", 4, 4.0, stream_flowing=True)[0], "FAIL")

    def test_every_stream_input_counter_has_an_update_law(self) -> None:
        """Every counter in the 1722.1 Stream Input block has an update law, so no
        grader silently falls back to one reading for a counter the two tables
        define differently."""
        # The law table is the oracle the RTL, the behave feature and the
        # bench grader all answer to, so it must cover the whole block.
        for n in IEEE_STREAM_INPUT_BLOCK:
            self.assertIsNotNone(counter_law(n), n)
        # The ruling includes FRAMES_RX among the three packet counters.
        self.assertEqual(
            {n for n, (k, _, _) in STREAM_INPUT_COUNTER_LAW.items()
             if k == "per-frame"},
            {"TIMESTAMP_VALID", "TIMESTAMP_NOT_VALID", "FRAMES_RX"})
        self.assertEqual(set(MILAN_INTERVAL_COUNTERS),
                         set(MILAN_TABLE_56) - {"MEDIA_LOCKED",
                                                "MEDIA_UNLOCKED",
                                                "STREAM_INTERRUPTED", "FRAMES_RX"})
        for n in MILAN_INTERVAL_COUNTERS:
            self.assertEqual(counter_law(n)[1], "Milan v1.2 Table 5.6", n)

    def test_interval_ceiling_catches_a_half_converted_counter(self) -> None:
        """Nothing whose trigger arrives in a frame may out-tick FRAMES_RX - except
        the two tv tallies Milan never defined, which are exempt.  That is what
        a half-converted counter looks like from outside."""
        # The retained sanity bound compares anomaly deltas to packet totals.
        b = {"FRAMES_RX": 0, "TIMESTAMP_UNCERTAIN": 0, "LATE_TIMESTAMP": 0}
        self.assertEqual(check_interval_ceiling(
            b, {"FRAMES_RX": 30, "TIMESTAMP_UNCERTAIN": 30,
                "LATE_TIMESTAMP": 2})[0], "PASS")
        v, d = check_interval_ceiling(
            b, {"FRAMES_RX": 30, "TIMESTAMP_UNCERTAIN": 240060,
                "LATE_TIMESTAMP": 2})
        self.assertEqual(v, "FAIL")
        self.assertEqual([o["counter"] for o in d["offenders"]],
                         ["TIMESTAMP_UNCERTAIN"])
        # TV/TNV use their separate packet-identity check.
        self.assertEqual(check_interval_ceiling(
            {"FRAMES_RX": 0, "TIMESTAMP_VALID": 0, "LATE_TIMESTAMP": 0},
            {"FRAMES_RX": 30, "TIMESTAMP_VALID": 240060,
             "LATE_TIMESTAMP": 2})[0], "PASS")
        # a window with no frames grades nothing
        self.assertEqual(check_interval_ceiling(
            b, {"FRAMES_RX": 0, "TIMESTAMP_UNCERTAIN": 0,
                "LATE_TIMESTAMP": 0})[0], "SKIP")
        # a reset inside the window is not a backwards counter finding
        self.assertEqual(check_interval_ceiling(
            {"FRAMES_RX": 500}, {"FRAMES_RX": 3})[0], "SKIP")

    def test_counter_semantics_grades_both_ways_round(self) -> None:
        """Packet counters follow the ruled rate; anomaly counters keep their law."""
        # Both TV and FRAMES_RX follow the packet rate. Interval RX fails.
        self.assertEqual(grade_counter_semantics(
            "TIMESTAMP_VALID", 240060, 30.0, stream_flowing=True)[0], "PASS")
        self.assertEqual(grade_counter_semantics(
            "FRAMES_RX", 30, 30.0, stream_flowing=True)[0], "FAIL")
        self.assertEqual(grade_counter_semantics(
            "FRAMES_RX", 240060, 30.0, stream_flowing=True)[0], "PASS")
        # OVER-conversion: a per-frame counter dragged onto the interval
        # tick alongside the six anomaly counters
        v, d = grade_counter_semantics("TIMESTAMP_VALID", 30, 30.0,
                                       stream_flowing=True)
        self.assertEqual((v, d["reading"]), ("FAIL", "interval"))
        # A slower packet counter also fails with known flowing traffic.
        self.assertEqual(grade_counter_semantics(
            "FRAMES_RX", 15, 30.0, stream_flowing=True)[0], "FAIL")
        # more ticks than frames: impossible under every reading
        self.assertEqual(grade_counter_semantics(
            "FRAMES_RX", 900000, 30.0, stream_flowing=True)[0], "FAIL")
        # AND THE TRAP THIS GRADER ITSELF FELL INTO, caught by running it
        # against real silicon: the AX7101's sink 0 on 2026-08-03 read
        # TIMESTAMP_UNCERTAIN 23 and LATE_TIMESTAMP 74 over ~7531 s beside
        # FRAMES_RX 7545 (a 0.998 s interval).  Those two tick only in the
        # intervals during which their own condition held, so dividing them
        # by the window implies intervals of minutes - and an earlier cut
        # of this function failed both as ceiling violations.
        for name, delta in (("TIMESTAMP_UNCERTAIN", 23),
                            ("LATE_TIMESTAMP", 74),
                            ("SEQ_NUM_MISMATCH", 1)):
            v, d = grade_counter_semantics(name, delta, 7531.0,
                                           stream_flowing=True)
            self.assertEqual((v, d["reading"]), ("PASS", "interval"),
                             f"{name} is intermittent by definition")
        self.assertEqual(grade_counter_semantics(
            "FRAMES_RX", 7545, 7531.0, stream_flowing=True)[0], "FAIL")
        # nothing measured, nothing concluded
        self.assertEqual(grade_counter_semantics(
            "UNSUPPORTED_FORMAT", 0, 30.0)[0], "SKIP")
        self.assertEqual(grade_counter_semantics("NOT_A_COUNTER", 1, 1.0)[0],
                         "SKIP")

    def test_frames_rate_band(self) -> None:
        """Milan bounds the observation interval from ABOVE only, so 200 ticks/s is
        a conformant 5 ms interval; only an implied interval past the 1 s
        ceiling is not.  Calling 200/s 'neither' once failed a good device."""
        self.assertEqual(frames_rate_band(7995.7), "per-frame")
        self.assertEqual(frames_rate_band(1.0), "interval")
        self.assertEqual(frames_rate_band(0.0), "neither")
        # Milan Table 5.4/5.6 bound the observation interval from ABOVE
        # ONLY ("shall be less than or equal to 1 second"), so a 5 ms
        # interval ticking 200/s is CONFORMANT.  Calling it "neither" - as
        # the first version of this band table did - failed a conformant
        # device, and a unit test asserting 200.0 was "the defect" cemented
        # it.
        self.assertEqual(frames_rate_band(200.0), "interval")
        self.assertEqual(frames_rate_band(3999.0), "interval")
        self.assertAlmostEqual(
            frames_rate_reading(200.0)["implied_interval_s"], 0.005)
        # the ONE way an interval reading is non-conformant: the implied
        # interval exceeds the 1 s ceiling
        self.assertEqual(frames_rate_band(0.4), "neither")
        self.assertIn("less than or equal to 1 s",
                      frames_rate_reading(0.4)["why"])
        # and the ceiling is a real parameter now, not a dead one
        self.assertEqual(frames_rate_band(0.4, max_interval_s=5.0),
                         "interval")

    def test_no_growth_is_a_verdict_and_not_a_note(self) -> None:
        """One tick of an error counter is one bad observation interval and FAILS.
        The two real escapes were emitted as INFO, so they graded nothing."""
        keys = ("LATE_TIMESTAMP", "EARLY_TIMESTAMP")
        v, d = check_no_growth({"LATE_TIMESTAMP": 7, "EARLY_TIMESTAMP": 3},
                               {"LATE_TIMESTAMP": 7, "EARLY_TIMESTAMP": 3},
                               keys)
        self.assertEqual(v, "PASS")
        # ONE tick is one bad observation interval, and it FAILS - the two
        # real escapes (296,294/296,294 UNSUPPORTED_FORMAT and 5.1 M LATE +
        # 4.8 M EARLY) were emitted as INFO and so could not fail anything
        v, d = check_no_growth({"LATE_TIMESTAMP": 7, "EARLY_TIMESTAMP": 3},
                               {"LATE_TIMESTAMP": 8, "EARLY_TIMESTAMP": 3},
                               keys)
        self.assertEqual(v, "FAIL")
        self.assertEqual(d["delta"]["LATE_TIMESTAMP"], 1)
        v, _ = check_no_growth({"UNSUPPORTED_FORMAT": 0},
                               {"UNSUPPORTED_FORMAT": 296294},
                               ("UNSUPPORTED_FORMAT",))
        self.assertEqual(v, "FAIL")
        # a counter that went DOWN measured nothing: reset or wrap
        v, _ = check_no_growth({"LATE_TIMESTAMP": 9},
                               {"LATE_TIMESTAMP": 0}, ("LATE_TIMESTAMP",))
        self.assertEqual(v, "INFO")
        # and an unclaimed counter is SKIP, never a pass
        self.assertEqual(check_no_growth({}, {}, keys)[0], "SKIP")

class _StreamingLicenceChecks:
    """The streaming licence and the cross-participant readings it gates.

    A mixin, not a TestCase: `self_test` combines the five into the one
    `T` whose name the report prints, so the arms can be read apart
    without a single line of that report changing.
    """
    def test_licence_decode_and_the_shut_gate(self) -> None:
        """LWSRP_STATUS decodes to OPEN, SHUT or UNKNOWN, and an absent reading
        stays UNKNOWN naming the flag to supply - never a violation verdict."""
        # 0x30 = talker declared + domain ok, gate SHUT: the reading a
        # CORRECTLY silent bound talker gives (Milan v1.2 5.3.7.3 needs a
        # Listener Ready too, and there is none)
        st, d = licence_state(0x30)
        self.assertEqual(st, "SHUT")
        self.assertTrue(d["talker_declared"])
        self.assertTrue(d["domain_ok"])
        self.assertFalse(d["stream_gate_open"])
        self.assertEqual(d["listener_declaration"], "none/ignore")
        st, d = licence_state(0x1FE)
        self.assertEqual(st, "OPEN")
        self.assertTrue(d["stream_gate_open"])
        self.assertTrue(d["reservation_active"])
        # a missing reading is UNKNOWN and says what to supply - it must
        # NEVER become a violation verdict
        st, d = licence_state(None)
        self.assertEqual(st, "UNKNOWN")
        self.assertIn("--licence-status", d["why"])
        self.assertEqual(d["register"], "0x694 LWSRP_STATUS")
        # the sticky shortfall and the MSRP failure code are decoded, not
        # swallowed
        self.assertTrue(decode_lwsrp_status(1 << 11)
                        ["attribute_row_shortfall"])
        self.assertEqual(decode_lwsrp_status(5 << 16)
                         ["msrp_failure_code"], 5)

    def test_stream_sources_count_packets(self) -> None:
        """Both stream directions are declared packet sources under #726."""
        for good in (*FRAME_ACCURATE_SOURCES, "stream_input", "stream_output"):
            self.assertEqual(assert_frame_accurate(good), good)
        self.assertEqual(INTERVAL_SOURCES, ())
        with self.assertRaises(CounterSemanticError):
            assert_frame_accurate("vibes")
        self.assertEqual(interval_ticks_agree(32000, 0, window_s=4)[0], "FAIL")
        self.assertEqual(interval_ticks_agree(32000, 0, window_s=4, self_loop=True)[0], "SKIP")
        self.assertEqual(interval_ticks_agree(0, 0)[0], "PASS")
        self.assertEqual(interval_ticks_agree(None, 32000)[0], "SKIP")
        self.assertEqual(interval_ticks_agree(-1, 32000, window_s=4)[0], "SKIP")
        self.assertEqual(interval_ticks_agree(32000, 32000, window_s=0)[0], "SKIP")

    def test_packet_agreement_attributes_interval_sides(self) -> None:
        """Ruled pairs pass; each interval regression belongs to its own side."""
        for tx, rx in ((32000, 32000), (31982, 32000), (2000, 2000)):
            verdict, detail = interval_ticks_agree(tx, rx, window_s=4.0)
            self.assertEqual(verdict, "PASS", "[726 XSIDE] ruled packet pair")
            self.assertNotIn("peer_findings", detail)
            self.assertIn("AVTPDU PACKETS", detail["compares"])
        for tx, rx, roles in ((4, 32000, ["talker"]), (32000, 4, ["listener"]),
                              (4, 4, ["talker", "listener"])):
            verdict, detail = interval_ticks_agree(tx, rx, window_s=4.0)
            self.assertEqual(verdict, "FAIL", "[726 XSIDE] interval-rate pair")
            self.assertEqual([f["role"] for f in detail.get("peer_findings", [])], roles,
                             "[726 XSIDE] attributed side")
            for finding in detail["peer_findings"]:
                self.assertEqual(finding["ticks_per_s"], 1.0)
                self.assertIn("IEEE 1722.1-2021", finding["counter"])
        self.assertEqual(interval_ticks_agree(32000, 48000, window_s=4)[0], "FAIL")
        self.assertEqual(interval_ticks_agree(32000, 32003, tolerance=2, window_s=4)[0], "FAIL")
        self.assertEqual(interval_ticks_agree(4, 4)[0], "SKIP")  # no duration, no rate claim

    def test_concurrent_packet_law_attributes_each_direction(self) -> None:
        """A shared flowing window cannot pass an interval-rate pair."""
        for tx, rx, roles in ((32000, 32000, []), (4, 32000, ["talker"]),
                              (32000, 4, ["listener"]), (4, 4, ["talker", "listener"])):
            verdict, detail = check_concurrent_flowing(
                {"tested": {"tx_ticks": tx, "rx_ticks": rx}}, licensed=True, window_s=4)
            self.assertEqual(verdict, "FAIL" if roles else "PASS", "[726 MULTI] packet rate")
            self.assertEqual([f["role"] for f in detail.get("peer_findings", [])], roles)
            self.assertTrue(all(f["pair"] == "tested" for f in detail.get("peer_findings", [])))
        self.assertEqual(check_concurrent_flowing(
            {"unmeasured": {"tx_ticks": 4, "rx_ticks": 4}}, licensed=True)[0], "SKIP")

    def test_cross_side_growth_bites_every_way(self) -> None:
        """Each cross-participant invariant fails on its own defect - one-sided
        streaming, an over-counting listener, frames with the gate shut, a leak
        to an unregistered port - and SKIPs, never convicts, on a side it could
        not read."""

        def sides(t: int | None, l: int | None, w: int | None = None,
                  **kw) -> dict[str, dict[str, object]]:
            """A reading set: a DUT talker, a peer listener, an optional
            wire witness, and any extra side passed as a keyword."""
            s = {"dut": {"role": "talker", "source": "avb_interface",
                         "frames": t, "device": "arty"},
                 "peer": {"role": "listener", "source": "avb_interface",
                          "frames": l, "device": "peer"}}
            if w is not None:
                s["testhost"] = {"role": "wire", "source": "nic",
                                 "frames": w, "device": "testhost"}
            s.update(kw)
            return s

        def one(res: list[tuple[str, str, dict[str, object]]],
                name: str) -> tuple[str, dict[str, object]]:
            """The (verdict, detail) of the one named triple in `res`."""
            return [(v, d) for n, v, d in res if n == name][0]

        # corroborated on three sides
        r = cross_side_growth(sides(8000, 8000, 8000), licensed=True,
                              registered_sides={"peer"})
        v, d = one(r, "xside.growth-corroborated")
        self.assertEqual(v, "PASS")
        self.assertEqual(d["sides_used"], ["dut", "peer", "testhost"])
        # a ONE-SIDED claim of streaming FAILS
        v, d = one(cross_side_growth(sides(8000, 0, 0), licensed=True,
                                     registered_sides={"peer"}),
                   "xside.growth-corroborated")
        self.assertEqual(v, "FAIL")
        self.assertFalse(d["moving"]["peer"])
        # a listener counting MORE than the talker sent, beyond the skew
        v, _ = one(cross_side_growth(sides(1000, 1000 + 8001),
                                     licensed=True),
                   "xside.listener-not-more-than-talker")
        self.assertEqual(v, "FAIL")
        # inside the skew it is the snapshot, not a defect
        v, _ = one(cross_side_growth(sides(1000, 1000 + 10),
                                     licensed=True),
                   "xside.listener-not-more-than-talker")
        self.assertEqual(v, "PASS")
        # frames with the gate SHUT are unreserved traffic
        v, _ = one(cross_side_growth(sides(8000, 8000), licensed=False),
                   "xside.unlicensed-silent-everywhere")
        self.assertEqual(v, "FAIL")
        v, _ = one(cross_side_growth(sides(0, 0), licensed=False),
                   "xside.unlicensed-silent-everywhere")
        self.assertEqual(v, "PASS")
        # both device sides unreadable: wire-only frames are the test
        # host's own traffic, not evidence against the gate
        v, d = one(cross_side_growth(sides(None, None, 42),
                                     licensed=False),
                   "xside.unlicensed-silent-everywhere")
        self.assertEqual(v, "SKIP")
        self.assertEqual(d["sides_unreadable"], ["dut", "peer"])
        # but ONE readable device side keeps the invariant armed
        v, _ = one(cross_side_growth(sides(7, None, 42), licensed=False),
                   "xside.unlicensed-silent-everywhere")
        self.assertEqual(v, "FAIL")
        # ambient wire-only movement (interface-global 'nic' source) with
        # every readable device side SILENT is unattributable: INFO, not
        # FAIL (373 campaign-chatter frames fired a false FAIL on silicon)
        v, d = one(cross_side_growth(sides(None, 0, 373), licensed=False),
                   "xside.unlicensed-silent-everywhere")
        self.assertEqual(v, "INFO")
        self.assertEqual(d["movers"], {"testhost": 373})
        # a stream-scoped pcap wire source still convicts alone
        pc = sides(None, 0)
        pc["tap"] = {"role": "wire", "source": "pcap", "frames": 99,
                     "device": "profishark"}
        v, _ = one(cross_side_growth(pc, licensed=False),
                   "xside.unlicensed-silent-everywhere")
        self.assertEqual(v, "FAIL")
        # PRUNING: a bystander that never registered must see nothing
        byst = sides(8000, 8000, bystander={"role": "bystander",
                                            "source": "pcap", "frames": 42,
                                            "device": "tap-port-3"})
        v, d = one(cross_side_growth(byst, licensed=True,
                                     registered_sides={"peer"}),
                   "xside.absent-where-not-registered")
        self.assertEqual(v, "FAIL")
        self.assertIn("bystander", d["leaks"])
        # an unreadable side SKIPs and NAMES itself, never fails the others
        v, d = one(cross_side_growth(sides(8000, None), licensed=True),
                   "xside.growth-corroborated")
        self.assertEqual(v, "SKIP")
        self.assertEqual(d["sides_unreadable"], ["peer"])
        # The guard still rejects sources without a packet-count contract.
        with self.assertRaises(CounterSemanticError):
            cross_side_growth({"x": {"role": "talker",
                                     "source": "unknown_counter",
                                     "frames": 1}})

    def test_the_test_machine_is_an_instrument_before_a_witness(self) -> None:
        """Host NIC loss DOWNGRADES a device verdict to INSTRUMENT-SUSPECT instead
        of failing the device, host demux drops are recorded and never graded,
        and a suspect verdict does not decide the run's exit code."""
        base = {k: 0 for k in
                NIC_LOSS_KEYS + NIC_DEMUX_KEYS + NIC_TRAFFIC_KEYS}
        v, d = instrument_health(base, dict(base, rx_packets=8000))
        self.assertEqual(v, "PASS")
        self.assertEqual(d["traffic_delta"]["rx_packets"], 8000)
        v, d = instrument_health(base, dict(base, rx_missed_errors=17))
        self.assertEqual(v, "FAIL")
        self.assertEqual(d["moved"]["rx_missed_errors"], 17)
        # rx_dropped alone is the switch's unhandled MVRP hitting host
        # demux AFTER rx_packets and the capture tap: recorded, never a
        # verdict (it used to poison every window on the live bench)
        v, d = instrument_health(base, dict(base, rx_dropped=2,
                                            rx_packets=9900))
        self.assertEqual(v, "PASS")
        self.assertEqual(d["demux_dropped"]["rx_dropped"], 2)
        self.assertNotIn("rx_dropped", d["moved"])
        self.assertEqual(instrument_health(None, base)[0], "SKIP")
        # a lossy instrument DOWNGRADES a device verdict; it never fails it
        self.assertEqual(downgrade_for_instrument("FAIL", "FAIL"),
                         INSTRUMENT_SUSPECT)
        self.assertEqual(downgrade_for_instrument("PASS", "FAIL"),
                         INSTRUMENT_SUSPECT)
        self.assertEqual(downgrade_for_instrument("FAIL", "PASS"), "FAIL")
        self.assertEqual(downgrade_for_instrument("SKIP", "FAIL"), "SKIP")
        # and it does not grade the run
        self.assertEqual(
            exit_code([verdict_record("a", "x", INSTRUMENT_SUSPECT)]), 0)
        self.assertEqual(
            summarise([verdict_record("a", "x", INSTRUMENT_SUSPECT)])
            [INSTRUMENT_SUSPECT], 1)

class _PlanContractChecks:
    """The plan's coverage and the assertion contract every step owes.

    A mixin, not a TestCase: `self_test` combines the five into the one
    `T` whose name the report prints, so the arms can be read apart
    without a single line of that report changing.
    """
    def test_topology_is_configuration_not_a_source_edit(self) -> None:
        """A bench of another shape is a --dut/--peer spec, and a misspelt key is
        REFUSED: a dropped 'listners=10' would run the whole campaign against
        the wrong shape and then report full coverage of it."""
        d = parse_device_spec("name=ax,entity=aa" + "11" * 7 +
                              ",mac=" + "22" * 6 + ",talkers=8,"
                              "listeners=8,crf_out=8,crf_in=8", ARTY)
        self.assertEqual((d.name, d.talkers, d.listeners), ("ax", 8, 8))
        self.assertEqual(d.talker_indices(), [0, 1, 2, 3, 4, 5, 6, 7, 8])
        # unset fields keep the base
        self.assertEqual(parse_device_spec("talkers=2", ARTY).formats,
                         ARTY.formats)
        # a typo is REFUSED, not ignored: a dropped "listners=10" would run
        # the whole campaign against the wrong shape and report full
        # coverage of it
        with self.assertRaises(ValueError):
            parse_device_spec("listners=10", ARTY)
        with self.assertRaises(ValueError):
            parse_device_spec("talkers", ARTY)
        # the test machine joins the participant list only once it has an
        # interface to read
        self.assertEqual([p.name for p in participants(ARTY, PEER)],
                         ["arty", "peer"])
        host = parse_device_spec("iface=enp6s0", TESTHOST)
        self.assertEqual([p.name for p in
                          participants(ARTY, PEER, host)],
                         ["arty", "peer", "testhost"])
        self.assertEqual([p.name for p in
                          participants(ARTY, PEER, TESTHOST)],
                         ["arty", "peer"])

    def test_coverage_is_audited_PER_AREA(self) -> None:
        """The per-area audit reddens on an index-0-only audio area while the
        matrix area still covers everything - the masking that let the audio
        area stay index-0-only under a green whole-plan coverage report."""
        plan = build_plan()
        for area in AREAS:
            ok, d = area_covers_every_index(plan, area)
            self.assertTrue(ok, (area, d["missing"]))
        # NEGATIVE CONTROL: an index-0-only AUDIO area must redden the AUDIO
        # audit even though the matrix area still covers everything.  The
        # whole-plan audit cannot do this, which is how the audio area
        # stayed index-0-only under a green coverage report.
        lonely = [s for s in plan if s.area != "audio"
                  or s.sid.endswith(".t0") or s.sid == "audio.thdn"]
        ok, d = area_covers_every_index(lonely, "audio")
        self.assertFalse(ok)
        self.assertEqual(d["missing"]["dut_talker"], [1, 2, 3])
        self.assertTrue(area_covers_every_index(lonely, "matrix")[0])
        # and the whole-plan audit is still green over the same plan, which
        # is the masking this exists to expose
        cov = plan_covers_every_index(lonely)
        self.assertEqual(cov["dut_talker"], ARTY.talker_indices())

    def test_ieee_bit_numbering_conversion(self) -> None:
        """Table 7-156's MSB-first 'Bit #' converts to the wire mask bit; reading
        the table without the conversion inverts every mask."""
        # Table 7-156 calls the counter at block offset 0 "Bit # 31"
        self.assertEqual(counters_valid_bit_ieee(0), 31)
        self.assertEqual(counters_valid_bit_ieee(44), 20)   # FRAMES_RX
        self.assertEqual(counters_valid_bit_ieee(124), 0)   # ENT_SPECIFIC_1
        with self.assertRaises(ValueError):
            counters_valid_bit_ieee(3)

    def test_milan_and_ieee_stream_output_layouts_differ(self) -> None:
        """FRAMES_TX and MEDIA_RESET sit at DIFFERENT offsets in the two Stream
        Output layouts, so a decoder handed the wrong one mislabels silently
        instead of failing - which is why the caller must state the layout."""
        # the trap: the same NAME sits at a different offset in the two
        # layouts, so a decoder that picks the wrong one mislabels
        self.assertEqual(MILAN_TABLE_54.index("FRAMES_TX"), 4)
        self.assertEqual(IEEE_STREAM_OUTPUT_BLOCK.index("FRAMES_TX"), 7)
        self.assertEqual(MILAN_TABLE_54.index("MEDIA_RESET"), 2)
        self.assertEqual(IEEE_STREAM_OUTPUT_BLOCK.index("MEDIA_RESET"), 3)

    def test_matrix_walks_every_index_both_directions_and_crf(self) -> None:
        """The matrix covers every index on both devices in both directions, CRF
        included, and a one-index device still reports only index 0 - the
        negative control that keeps the audit able to say no."""
        plan = plan_matrix()
        cov = plan_covers_every_index(plan)
        self.assertEqual(cov["dut_talker"], ARTY.talker_indices())
        self.assertEqual(cov["dut_listener"], ARTY.listener_indices())
        self.assertEqual(cov["peer_talker"], PEER.talker_indices())
        self.assertEqual(cov["peer_listener"], PEER.listener_indices())
        self.assertIn(ARTY.crf_out, cov["dut_talker"])
        self.assertIn(ARTY.crf_in, cov["dut_listener"])
        # NEGATIVE CONTROL: an index-0-only plan must FAIL the audit
        lonely = Device("solo", "aa" * 8, "bb" * 6, talkers=1, listeners=1)
        cov2 = plan_covers_every_index(plan_matrix(lonely, lonely), lonely,
                                       lonely)
        self.assertEqual(cov2["dut_talker"], [0])
        self.assertNotEqual(cov2["dut_talker"], ARTY.talker_indices())

    def test_every_bound_step_carries_the_full_assertion_set(self) -> None:
        """No bind may drop an assertion its clause requires: a step that asks
        fewer questions than the contract still counts as a step that ran."""
        need = {a.name for a in BOUND_STREAMING_ASSERTS}
        for s in build_plan(["matrix", "churn"]):
            if s.op == "connect" and "rebind" not in s.sid:
                got = {a.name for a in s.asserts}
                self.assertTrue(need <= got,
                                f"{s.sid} is missing {need - got}")

    def test_every_step_has_a_clause_or_says_it_is_info(self) -> None:
        """Every assertion cites a clause and declares a severity, so nothing in
        the plan can grade a device against an unstated requirement."""
        for s in build_plan():
            for a in s.asserts:
                self.assertTrue(a.clause.strip(),
                                f"{s.sid}/{a.name} has no clause")
                self.assertIn(a.severity, ("SHALL", "RECOMMENDED", "INFO"))

    def test_storm_entries_are_recommended_not_shall(self) -> None:
        """The adverse-practice storm entries stay RECOMMENDED and control
        responsiveness stays INFO, because that document says responsiveness is
        NOT expected under storm - failing it asserts the opposite of the text."""
        # the document is a RECOMMENDED PRACTICE; calling its entries
        # SHALL would make us fail a device for something no requirement
        # asks of it
        storms = [s for s in plan_torture() if ".storm." in s.sid]
        self.assertTrue(storms)
        for s in storms:
            sev = {a.name: a.severity for a in s.asserts}
            self.assertEqual(sev["stream.uninterrupted"], "RECOMMENDED")
            # and control responsiveness is INFO, because the same clause
            # says it is NOT expected under storm
            self.assertEqual(sev["control.responsive"], "INFO")

    def test_human_entries_are_emitted_not_skipped(self) -> None:
        """Every needs-human step reaches the printed checklist.  A silently
        skipped adverse-condition entry is how 'we tested link loss' becomes
        true in a report and false at the bench."""
        plan = build_plan()
        hs = human_steps(plan)
        # the cable pull (torture) plus the two physical cycle steps -
        # which stay needs_human in the PLAN so a bench without the
        # powerstrip hook hands them back as NEEDS-HUMAN, exactly as
        # before they were automatable
        self.assertGreaterEqual(len(hs), 3)
        txt = checklist_text(plan)
        for s in hs:
            self.assertIn(s.sid, txt)
            self.assertIn(s.human_action[:24], txt)
        self.assertIn("No human-action entries", checklist_text([]))

class _AreaContractChecks:
    """The physical, gPTP, CRF, persistence and churn areas' own contracts.

    A mixin, not a TestCase: `self_test` combines the five into the one
    `T` whose name the report prints, so the arms can be read apart
    without a single line of that report changing.
    """
    def test_physical_family_contract(self) -> None:
        """The physical area runs LAST, keeps both power cycles needs_human in the
        plan, owes BOTH directions of the GM story and the persistence story,
        and ends each family with a full proof pair at a non-zero index."""
        plan = build_plan()
        # LAST, always: a partition mid-matrix would pollute everything
        areas_in_order = []
        for s in plan:
            if s.area not in areas_in_order:
                areas_in_order.append(s.area)
        self.assertEqual(areas_in_order[-1], "physical")
        phys = [s for s in plan if s.area == "physical"]
        self.assertTrue(phys)
        # the old human entries moved here and NOWHERE else
        tort = plan_torture()
        self.assertFalse([s for s in tort if "gm-change" in s.sid
                          or "gm-loss" in s.sid
                          or "power-cycle" in s.sid])
        self.assertTrue(any("cable-pull" in s.sid and s.needs_human
                            for s in tort))
        # the two cycle steps: still needs_human in the PLAN (the
        # no-regression guarantee), with the outlet role named for the
        # runner that CAN automate them
        cyc = {s.op: s for s in phys
               if s.op in ("switch_power_cycle", "dut_power_cycle")}
        self.assertEqual(set(cyc), {"switch_power_cycle",
                                    "dut_power_cycle"})
        for s in cyc.values():
            self.assertTrue(s.needs_human, s.sid)
            self.assertTrue(s.human_action, s.sid)
            self.assertIn("outlet_role", s.args)
        self.assertEqual(cyc["switch_power_cycle"].args["outlet_role"],
                         "switch")
        self.assertEqual(cyc["dut_power_cycle"].args["outlet_role"],
                         "dut")
        # the assertion contract: the switch cycle owes the GM change AND
        # the GM loss story, the DUT cycle owes the persistence story
        sw = {a.name for a in cyc["switch_power_cycle"].asserts}
        self.assertIn("counters.avb_interface.gptp-gm-changed-advances",
                      sw)
        self.assertIn("physical.partition-is-the-test", sw)
        self.assertIn("gptp.exactly-one-gm-after-heal", sw)
        self.assertIn("entity.survived-without-reboot", sw)
        self.assertIn("gptp.tu-validity-restored", sw)
        # BOTH directions of the GM story are owed, plus the side that
        # actually loses its GM and the link-event datum.  Owing only
        # the ADVANCE is what filed a fake red against a permanent GM
        # on 2026-08-02 (ax-phys-a).
        self.assertIn("counters.avb_interface.gptp-gm-continuity", sw)
        self.assertIn(
            "counters.avb_interface.peer-gptp-gm-changed-advances", sw)
        self.assertIn("counters.avb_interface.link-event-observed", sw)
        du = {a.name for a in cyc["dut_power_cycle"].asserts}
        self.assertIn("state.restored-after-power-cycle", du)
        # and the half of the persistence story a build with no store
        # still owes, plus the datum that makes the gap measurable
        self.assertIn("state.self-consistent-after-power-cycle", du)
        self.assertIn("state.format-after-power-cycle", du)
        self.assertIn("counters.zeroed-after-power-cycle", du)
        self.assertIn("boot.reaches-network-unattended", du)
        self.assertIn("boot.same-gateware-version", du)
        self.assertIn("boot.rx-filter-posture-restored", du)
        # the budget floors from the bench facts: switch boot before any
        # board is reachable, ~5.5 min worst-case DUT boot, and a hold an
        # order of magnitude past the announce-receipt timeout
        a = cyc["switch_power_cycle"].args
        self.assertGreaterEqual(a["hold_s"], 15)
        self.assertGreaterEqual(a["link_budget_s"], 180)
        self.assertGreaterEqual(a["gptp_budget_s"], 120)
        b = cyc["dut_power_cycle"].args
        self.assertGreaterEqual(b["off_s"], 5)
        self.assertGreaterEqual(b["net_budget_s"], 120)
        # each family ends with a full PROOF PAIR at a NON-ZERO index
        # (index 0 is the alias path)
        for fam in ("switch-cycle", "dut-cycle"):
            proof = [s for s in phys
                     if s.sid.startswith(f"phys.{fam}.proof")]
            conn = [s for s in proof if s.op == "connect"]
            self.assertTrue(conn, fam)
            self.assertGreater(conn[0].args["talker_index"], 0)
            need = {x.name for x in BOUND_STREAMING_ASSERTS}
            got = {x.name for x in conn[0].asserts}
            self.assertTrue(need <= got, need - got)
        # snapshot-before-cycle ordering, per family
        sids = [s.sid for s in phys]
        for fam, cyc_sid in (("switch-cycle",
                              "phys.switch-cycle.gm-partition"),
                             ("dut-cycle",
                              "phys.dut-cycle.power-cycle")):
            self.assertLess(sids.index(f"phys.{fam}.pre-snapshot"),
                            sids.index(cyc_sid))

    def test_the_gm_story_states_its_own_precondition(self) -> None:
        """The GM clauses name WHICH device each direction is for.  Asserting the
        GM_CHANGED advance against a DUT that IS the grandmaster - whose own
        grandmasterIdentity never changed - filed a fake red on 2026-08-02."""
        # ax-phys-a 2026-08-02: "a partition and a re-join are real BMCA
        # elections, so the counter advances" was asserted against a DUT
        # that IS the grandmaster - whose own grandmasterIdentity never
        # changed, so 1722.1-2021 Table 7-153 requires exactly ZERO.
        # The clause text must now name which device each direction is
        # for, or the same fake red comes straight back.
        adv = A_GM_CHANGED_ADVANCES.clause.lower()
        self.assertIn("only for a device that was following", adv)
        self.assertIn("gptp-gm-continuity", adv)
        cont = A_GM_CONTINUITY.clause.lower()
        self.assertIn("zero", cont)
        self.assertIn("grandmasteridentity", cont)
        # the link-event reading is a DATUM: the bench's inline tap can
        # hold the DUT's PHY link up through a switch outage, so it must
        # never be able to fail a run
        self.assertEqual(A_LINK_EVENT_SEEN.severity, "INFO")
        self.assertEqual(A_STATE_DEFAULTED.severity, "INFO")
        for s in (A_GM_CHANGED_ADVANCES, A_GM_CONTINUITY,
                  A_PEER_GM_CHANGED, A_STATE_RESTORED,
                  A_STATE_SELF_CONSISTENT):
            self.assertEqual(s.severity, "SHALL", s.name)

    def test_the_peer_crf_input_is_not_an_aaf_sink(self) -> None:
        """No 'highest AAF index' selector may aim an AAF talker at the peer's CRF
        Media Clock Input, which answers ACMP and then refuses every AAF
        format: 32 of one run's 45 SKIPs were that bind's post-bind contract."""
        # ax-phys-a aimed BOTH proof pairs at peer l8 - which is the
        # CRF Media Clock INPUT, measured from the reference device's
        # own refusals (listener_format 041060010000bb80: AVTP subtype
        # 0x04 = CRF, 0xbb80 = 48 kHz).  An AAF talker can never bind
        # it, so 32 of that run's 45 SKIPs were the post-bind contract
        # of a bind that was never bindable.
        self.assertEqual(PEER.crf_in, 8)
        self.assertNotIn(8, PEER.listener_indices(include_crf=False))
        self.assertIn(8, PEER.listener_indices(include_crf=True))
        self.assertTrue(PEER.is_crf_listener(8))
        # Every "highest AAF index" SELECTOR now lands on an AAF sink.
        # The matrix is exempt by design - it is the full cross product
        # on purpose, and a format-incompatible cell there is a wanted
        # CONFORMANT-REFUSAL - but a step that CHOSE one index must not
        # choose the CRF one with an AAF talker.
        for s in build_plan():
            if s.op != "connect" or s.area == "matrix":
                continue
            if s.args.get("listener") != PEER.entity_id:
                continue
            if PEER.is_crf_listener(s.args.get("listener_index")):
                self.assertTrue(
                    ARTY.is_crf_talker(s.args.get("talker_index")), s.sid)

    def test_persistence_clause_is_quoted_and_never_deleted(self) -> None:
        """Milan 5.3.8.1 stays quoted in the assertion itself: a build with no
        store changes the VERDICT to KNOWN-PENDING, never the requirement."""
        # Milan v1.2 5.3.8.1 is an unconditional SHALL, so the assertion
        # stays; what a build with no store changes is the VERDICT, not
        # the requirement.  Both halves must be traceable from the text.
        c = A_STATE_RESTORED.clause
        self.assertIn("5.3.8.1", c)
        self.assertIn("non-volatile memory and restored after a power "
                      "cycle", c)
        self.assertIn("KNOWN-PENDING", c)
        self.assertIn("KNOWN-PENDING", VERDICTS)
        self.assertIn("5.3.8.1", A_STATE_SELF_CONSISTENT.clause)

    def test_churn_includes_the_implicit_rebind_to_a_different_talker(self) -> None:
        """The churn area reaches the implicit rebind - a BIND_RX over an already
        bound input, to a DIFFERENT talker - which a bind/unbind/bind loop can
        never produce and which carries its own counter-reset consequence."""
        reb = [s for s in plan_churn() if s.sid.endswith(".rebind")]
        self.assertTrue(reb)
        for s in reb:
            self.assertTrue(s.args.get("no_unbind_first"))
            self.assertIn("5.5.3.5.43", s.clause)
        # and it must move to a DIFFERENT talker index than the first bind
        first = {s.sid: s.args["talker_index"]
                 for s in plan_churn()
                 if s.op == "connect" and not s.sid.endswith(".rebind")
                 and s.sid.startswith("churn.implicit-rebind")}
        for s in reb:
            base = s.sid.rsplit(".", 1)[0]
            self.assertNotEqual(s.args["talker_index"], first[base])

    def test_areas_selector(self) -> None:
        """--areas selects exactly the named areas and REFUSES an unknown one, so
        a typo cannot quietly run a shorter campaign than the caller asked for."""
        self.assertEqual({s.area for s in build_plan(["audio"])},
                         {"audio"})
        with self.assertRaises(ValueError):
            build_plan(["nope"])
        self.assertEqual({s.area for s in build_plan()},
                         {"matrix", "multi", "churn", "payload", "audio",
                          "torture", "soak", "power", "physical"})


class _ReleasePlanChecks:
    """L3: issue #396's decisions, independently enumerated and fault planted."""

    def _release_repeats(self, plan: list[Step]) -> dict[str, Step]:
        return {s.sid: s for s in plan if s.op in RELEASE_REQUIRED_ASSERTS}

    def test_release_defaults_and_assertions(self) -> None:
        """L3 #396 2026-10-26: the 24-hour soak, its audio run and 100/50/50 cycles."""
        repeats = self._release_repeats(build_plan(
            ["soak", "audio", "power"], release=ReleaseSettings(topology_explicit=True)))
        soak, audio = repeats["soak.continuous"], repeats["audio.integrity"]
        idle, commit, reset = (repeats["power." + p] for p in ("idle", "journal_commit", "soft_reset"))
        self.assertEqual(len(repeats), 5)
        self.assertEqual((soak.args["duration_s"], soak.args["interval_s"]), (86400, 60))
        self.assertEqual((audio.args["duration_s"], audio.args["context_s"], audio.args["window"]),
                         (86400, 5, "soak.continuous"))
        self.assertEqual([s.args["cycles"] for s in (idle, commit, reset)], [100, 50, 50])
        self.assertEqual([s.args["phase"] for s in (idle, commit, reset)],
                         ["idle", "journal_commit", "soft_reset"])
        self.assertEqual([s.args["cold"] for s in (idle, commit, reset)], [True, True, False])
        self.assertEqual([s.args["soft_reset"] for s in (idle, commit, reset)], [False, False, True])
        self.assertEqual(soak.args["timestamp_margin"]["offset"], 0x6EC)
        self.assertEqual(soak.args["timestamp_margin"]["stream_input"], 0)
        self.assertEqual(soak.args["zero_growth_counters"],
                         ["SEQ_NUM_MISMATCH", "STREAM_INTERRUPTED", "LATE_TIMESTAMP", "EARLY_TIMESTAMP"])
        for step in (idle, commit, reset):
            self.assertEqual(step.args["total_cycles"], 200)
            self.assertEqual(step.args["persisted_items"], [
                "configuration", "sampling_rate", "stream_format", "presentation_time_offset",
                "channel_mappings", "clock_source", "entity_names", "object_names",
                "stream_binding"])
            self.assertEqual(step.args["boot_observation_s"], 35)
            self.assertEqual(step.args["restore_bound_s"], 30)
            self.assertEqual(step.args["boot_margin_s"], 5)
            self.assertEqual(step.args["rebind_limit_s"], 1)
            self.assertTrue(step.args["rebind_limit_exclusive"])
            self.assertTrue(step.needs_human)
        for step in (idle, commit):
            self.assertEqual(step.args["power_off_hold_s"], 8)
            self.assertEqual(step.args["time_origin"], "T0: power-strip ON command, host monotonic clock")
        self.assertNotIn("power_off_hold_s", reset.args)
        self.assertEqual(reset.args["time_origin"], "T0: reset command, host monotonic clock")
        self.assertEqual(commit.args["cut_requires"], "journal_commit_window")
        oracles = {"soak": soak.args["counter_oracle"], "audio": audio.args["counter_grader"],
                   "power": idle.args["state_oracle"]}
        self.assertEqual(oracles, {"soak": "check_release_soak_counters",
                                   "audio": "grade_audio_counter_capture",
                                   "power": "check_release_state_restored"})
        for name in oracles.values():
            self.assertTrue(callable(globals()[name]), name)
        self.assertIn("planted_event_log", soak.args["evidence"])
        self.assertIn("planted_events", soak.args["continuous_evidence"])
        self.assertTrue({"audio_captures", "planted_arm_log", "capture_loss_log"}
                        <= set(audio.args["evidence"]))
        self.assertEqual([arm["class"] for arm in audio.args["planted_arms"]],
                         ["dropped", "repeated", "bit-flip"])
        self.assertEqual(audio.args["counter_classes"],
                         ["dropped", "repeated", "silence", "bit-flip", "swap", "unresolved"])
        self.assertEqual((audio.args["counter_grader_required_s"], audio.args["qualification"]["required_s"],
                          audio.args["qualification"]["guard_frames"]), (86400, 86400, 63))
        self.assertEqual(audio.args["analog"]["tones_hz"], [997, 9973])
        self.assertIsNone(audio.args["analog"]["limits"])
        self.assertEqual({p["path"] for p in audio.args["digital_paths"]},
                         {"outbound", "return", "dut-tdm-loop"})
        self.assertEqual(reset.args["evidence"][-1], "reset_command_log")
        self.assertEqual(idle.args["evidence"][-1], "power_strip_log")
        expected = {
            "soak": {"release.complete-evidence", "soak.continuous-duration",
                     "soak.bound-both-directions", "soak.counter-walk",
                     "soak.no-counter-errors", "soak.gptp-continuity", "soak.mr-causes-and-hold",
                     "soak.tu-within-holdover", "soak.timestamp-margin",
                     "soak.uptime-monotonic"},
            "audio": {"release.complete-evidence", "audio.inside-soak-window",
                      "audio.counter-every-digital-path", "audio.counter-classified",
                      "audio.planted-arms-found", "audio.capture-losses-apart",
                      "audio.event-record", "audio.analog-sine-pair", "audio.zero-dut-glitches"},
            "power": {"release.complete-evidence", "power.cycle-count-and-phase",
                      "power.state-restored", "power.adp-valid-time",
                      "power.rebind-bound", "power.automatic-restore-bound",
                      "power.single-boot", "power.counter-walk"},
        }
        for step in repeats.values():
            data = json.loads(json.dumps(step.as_dict()))
            self.assertEqual(set(data["asserts"]), expected[step.area])
            self.assertEqual(set(data["assert_severity"].values()), {"SHALL"})
            self.assertTrue(data["args"]["release_eligible"])

    def test_release_counter_omissions_in_every_repeat(self) -> None:
        """L3 topology oracle: both devices, descriptor kinds, and all repeats."""
        from copy import deepcopy
        original = build_plan()
        for source in (s for s in original if s.op in RELEASE_REQUIRED_ASSERTS):
            self.assertTrue(area_covers_every_index(original, source.area)[0])
            for target in source.args["counter_targets"]:
                with self.subTest(repeat=source.sid, target=target):
                    broken = deepcopy(original)
                    step = next(s for s in broken if s.sid == source.sid)
                    step.args["counter_targets"].remove(target)
                    ok, detail = area_covers_every_index(broken, source.area)
                    self.assertFalse(ok, detail)
                    self.assertIn(source.sid, detail["missing"])
                    self.assertTrue(area_covers_every_index(broken, "matrix")[0])

    def test_release_binding_omissions_in_every_repeat(self) -> None:
        """AAF-only and CRF-only losses cannot mask one another in either direction."""
        from copy import deepcopy
        original = build_plan()
        for source in (s for s in original if s.op in RELEASE_REQUIRED_ASSERTS):
            for talker in (ARTY, PEER):
                for kind in ("all", "aaf", "crf"):
                    with self.subTest(repeat=source.sid, talker=talker.name, kind=kind):
                        broken = deepcopy(original)
                        step = next(s for s in broken if s.sid == source.sid)
                        step.args["pairs"] = [
                            pair for pair in step.args["pairs"]
                            if not (pair["talker"] == talker.entity_id and
                                    (kind == "all" or
                                     (pair["talker_index"] == talker.crf_out) == (kind == "crf")))]
                        ok, detail = area_covers_every_index(broken, source.area)
                        self.assertFalse(ok, detail)
                        self.assertIn(source.sid, detail["missing"])
                        self.assertTrue(area_covers_every_index(broken, "matrix")[0])
        for source in (s for s in original if s.op in RELEASE_REQUIRED_ASSERTS
                       or s.op == RELEASE_CONTROL_OP):
            without_repeat = [s for s in original if s.sid != source.sid]
            self.assertFalse(area_covers_every_index(without_repeat, source.area)[0], source.sid)
        for area in ("soak", "audio", "power"):
            self.assertFalse(area_covers_every_index([], area)[0])

    def test_release_sparse_shapes_and_compatible_pairs(self) -> None:
        """Counter coverage follows sparse topology, never a baked index range."""
        dut = parse_device_spec("talker_index_set=1|3,listener_index_set=2|5,"
                                "crf_out=7,crf_in=8", ARTY)
        for area in ("soak", "power"):
            plan = build_plan([area], dut, PEER)
            self.assertTrue(area_covers_every_index(plan, area, dut, PEER)[0])
            cov = plan_covers_every_index(plan, dut, PEER)
            self.assertEqual(cov["dut_talker"], [1, 3, 7])
            self.assertEqual(cov["dut_listener"], [2, 5, 8])
        plan = build_plan(["soak", "audio", "power"], dut, PEER)
        self.assertEqual(_release_area_defects(
            "audio", [s for s in plan if s.area == "audio"], dut, PEER), {})
        for area in ("soak", "audio", "power"):
            for step in (s for s in plan if s.area == area and "pairs" in s.args):
                sinks = [(p["listener"], p["listener_index"])
                         for p in step.args["pairs"]]
                self.assertEqual(len(sinks), len(set(sinks)))
                for pair in step.args["pairs"]:
                    tk, ls = (dut, PEER) if pair["talker"] == dut.entity_id else (PEER, dut)
                    self.assertEqual(tk.is_crf_talker(pair["talker_index"]),
                                     ls.is_crf_listener(pair["listener_index"]))

    def test_release_settings_validation(self) -> None:
        """Bad repeat inputs refuse; diagnostic inputs cannot qualify a release."""
        for changes in ({"soak_duration_s": 0}, {"soak_interval_s": -1},
                        {"soak_interval_s": 86401}, {"power_cycles": 201},
                        {"idle_cycles": 0}, {"commit_cycles": -1}, {"reset_cycles": 0},
                        {"reset_cycles": 51}, {"reset_cycles": True},
                        {"power_cycles": True}, {"soak_duration_s": float("nan")},
                        {"audio_duration_s": 86401}, {"audio_duration_s": 0},
                        {"audio_context_s": 0}, {"audio_context_s": False},
                        {"audio_duration_s": 4, "audio_context_s": 5},
                        {"persisted_items": ()}, {"persisted_items": ("",)},
                        {"persisted_items": ("binding", "binding")}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                ReleaseSettings(**changes)
        settings = ReleaseSettings(soak_duration_s=125, soak_interval_s=17, power_cycles=4,
                                   idle_cycles=2, commit_cycles=1, reset_cycles=1,
                                   persisted_items=("stream_binding", "clock_source"),
                                   audio_duration_s=100, audio_context_s=3)
        repeats = self._release_repeats(build_plan(["soak", "audio", "power"], release=settings))
        soak, audio = repeats["soak.continuous"], repeats["audio.integrity"]
        idle, commit, reset = (repeats["power." + p] for p in ("idle", "journal_commit", "soft_reset"))
        self.assertEqual(soak.args["duration_s"], 125)
        self.assertEqual(soak.args["interval_s"], 17)
        self.assertEqual((audio.args["duration_s"], audio.args["context_s"]), (100, 3))
        self.assertEqual(audio.args["event_context"]["max_gap_s"], 3)
        self.assertEqual([s.args["total_cycles"] for s in (idle, commit, reset)], [4, 4, 4])
        self.assertTrue(soak.args["sample_at_end"])
        self.assertEqual([s.args["cycles"] for s in (idle, commit, reset)], [2, 1, 1])
        self.assertEqual(commit.args["persisted_items"],
                         ["stream_binding", "clock_source"])
        for step in repeats.values():
            self.assertFalse(step.args["release_eligible"])
        no_crf = Device("dut", "aa" * 8, "bb" * 6, 1, 1)
        with self.assertRaisesRegex(ValueError, "CRF"):
            build_plan(["soak"], no_crf, PEER)
        with self.assertRaisesRegex(ValueError, "distinct"):
            build_plan(["power"], ARTY, ARTY)

    def test_release_cli_parameters(self) -> None:
        """The actual CLI threads every parameter into emitted JSON."""
        import contextlib
        import io
        from unittest.mock import patch
        argv = ["torture_campaign.py", "--plan", "--areas", "soak,audio,power",
                "--json", "--soak-duration-s", "125", "--soak-interval-s", "17",
                "--power-cycles", "4", "--idle-cycles", "2", "--commit-cycles", "1",
                "--reset-cycles", "1", "--persisted-items", "stream_binding,clock_source",
                "--restore-bound-s", "23", "--boot-margin-s", "7",
                "--power-off-hold-s", "13", "--audio-duration-s", "100",
                "--audio-context-s", "3"]
        output = io.StringIO()
        with patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
            self.assertEqual(main(), 0)
        steps = {step["sid"]: step for step in json.loads(output.getvalue())}
        soak, audio = steps["soak.continuous"], steps["audio.integrity"]
        idle, commit, reset = (steps["power." + p] for p in ("idle", "journal_commit", "soft_reset"))
        self.assertEqual(soak["args"]["duration_s"], 125)
        self.assertEqual(soak["args"]["interval_s"], 17)
        self.assertEqual((audio["args"]["duration_s"], audio["args"]["context_s"]), (100, 3))
        for step in (idle, commit, reset):
            self.assertEqual(step["args"]["total_cycles"], 4)
            self.assertEqual(step["args"]["restore_bound_s"], 23)
            self.assertEqual(step["args"]["boot_margin_s"], 7)
            self.assertEqual(step["args"]["boot_observation_s"], 30)
        for step in (idle, commit):
            self.assertEqual(step["args"]["power_off_hold_s"], 13)
        self.assertEqual([s["args"]["cycles"] for s in (idle, commit, reset)], [2, 1, 1])
        self.assertEqual(commit["args"]["persisted_items"],
                         ["stream_binding", "clock_source"])
        for extra in (["--power-cycles", "5"], ["--reset-cycles", "2"],
                      ["--audio-duration-s", "126"]):
            with self.subTest(extra=extra), patch.object(sys, "argv", argv + extra), \
                    contextlib.redirect_stderr(io.StringIO()), \
                    self.assertRaises(SystemExit) as failure:
                main()
            self.assertEqual(failure.exception.code, 2)

    def test_release_cli_power_hold_default(self) -> None:
        """L3 #396: an omitted CLI hold retains the decided eight seconds."""
        import contextlib
        import io
        from unittest.mock import patch
        output = io.StringIO()
        argv = ["torture_campaign.py", "--plan", "--areas", "power", "--json"]
        with patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
            self.assertEqual(main(), 0)
        steps = [step for step in json.loads(output.getvalue())
                 if step["op"] == "release_power_cycles"]
        self.assertEqual([step["args"]["phase"] for step in steps],
                         ["idle", "journal_commit", "soft_reset"])
        for step in steps[:2]:
            self.assertEqual(step["args"]["power_off_hold_s"], 8)
        self.assertNotIn("power_off_hold_s", steps[2]["args"])

    def test_release_timing_and_snapshot_contract(self) -> None:
        """L3 #396 round 3 pins T0 origins, separate off time, and phase policies."""
        settings = ReleaseSettings(restore_bound_s=19, boot_margin_s=11, power_off_hold_s=17)
        repeats = self._release_repeats(build_plan(["power"], release=settings))
        idle, commit, reset = (repeats["power." + p] for p in ("idle", "journal_commit", "soft_reset"))
        self.assertEqual(idle.args["snapshot_policy"], "exact pre-cut committed snapshot")
        self.assertEqual(reset.args["snapshot_policy"], "exact pre-cut committed snapshot")
        self.assertEqual(commit.args["snapshot_policy"], "complete old or new committed snapshot")
        self.assertEqual(idle.args["cut_requires"], "journal_idle")
        self.assertEqual(reset.args["cut_requires"], "journal_idle")
        self.assertEqual(reset.args["cycle_kind"], "soft reset")
        self.assertEqual(reset.args["cold_confirmation"], "power held on; outlet ON before and after the reset")
        self.assertIn("power held on", reset.args["reset_method"])
        self.assertEqual(reset.args["time_origin"], "T0: reset command, host monotonic clock")
        for key in ("power_off_hold_s", "power_off_hold_origin", "power_off_hold_in_adp_window"):
            self.assertNotIn(key, reset.args)
        for step in (idle, commit, reset):
            args = json.loads(json.dumps(step.as_dict()))["args"]
            self.assertEqual(args["restore_bound_s"], 19)
            self.assertEqual(args["boot_observation_s"], 30)
            self.assertEqual(args["restore_start"], "T0")
            self.assertEqual(args["adp_start"], "T0")
            self.assertEqual(args["state_oracle"], "check_release_state_restored")
            self.assertEqual(args["boot_evidence"],
                             "complete UART/reset observation from T0 through next cycle or campaign end; "
                             "at least boot_observation_s")
        for step in (idle, commit):
            args = json.loads(json.dumps(step.as_dict()))["args"]
            self.assertEqual(args["cold_confirmation"], "power removed; discharge verified")
            self.assertEqual(args["restore_bound_s"], 19)
            self.assertEqual(args["boot_margin_s"], 11)
            self.assertEqual(args["boot_observation_s"], 30)
            self.assertTrue(args["restore_bound_provisional"])
            self.assertEqual(args["restore_bound_origin"],
                             "issue #396 round 2; ratify with #397 and #75")
            self.assertEqual(args["boot_observation_origin"],
                             "restore_bound_s + boot_margin_s from T0")
            self.assertEqual(args["time_origin"],
                             "T0: power-strip ON command, host monotonic clock")
            self.assertEqual(args["restore_start"], "T0")
            self.assertEqual(args["restore_end"], "first valid AVTP PDU of each persisted binding")
            self.assertFalse(args["restore_limit_exclusive"])
            self.assertEqual(args["restore_requires"],
                             "automatic; no controller repair; both directions and CRF")
            self.assertEqual(args["power_off_hold_s"], 17)
            self.assertEqual(args["power_off_hold_origin"],
                             "phys.dut-cycle.power-cycle: default 8 s; verify discharge")
            self.assertFalse(args["power_off_hold_in_adp_window"])
            self.assertEqual(args["adp_reference"],
                             "last pre-cut DUT ENTITY_AVAILABLE, host timestamp and raw PDU")
            self.assertEqual(args["adp_valid_time_unit_s"], 2)
            self.assertEqual(args["adp_required_valid_time"], 10)
            self.assertEqual(args["adp_start"], "T0")
            self.assertEqual(args["adp_deadline"], "2 * pre_cut_valid_time")
            self.assertEqual(args["adp_elapsed"], "first_post_cut_available_host_s - t0_host_s")
            self.assertTrue(args["adp_limit_exclusive"])
            self.assertEqual(args["adp_missing_or_expired"],
                             "fail; require captured valid_time=10 and arrival before T0 deadline")
            self.assertEqual(args["rebind_start"], "CONNECT_RX success")
            self.assertEqual(args["rebind_end"], "first valid AVTP PDU")
            self.assertEqual(args["rebind_requires"],
                             "automatic restoration passed for every persisted binding")

    def test_release_eligibility_boundaries(self) -> None:
        """Each prerequisite can independently refuse an otherwise eligible area."""
        settings = ReleaseSettings(topology_explicit=True)
        items = tuple(RELEASE_PERSISTED_ITEMS)
        cases = [({}, (True, True, True)),
                 ({"restore_bound_s": 29}, (True, True, True)),
                 ({"restore_bound_s": 30}, (True, True, True)),
                 ({"restore_bound_s": 31}, (False, False, False)),
                 ({"restore_bound_s": 3600}, (False, False, False)),
                 ({"soak_duration_s": 86399, "audio_duration_s": 86399}, (False, False, True)),
                 ({"soak_duration_s": 604800}, (True, True, True)),
                 ({"audio_duration_s": 86399}, (True, False, True)),
                 ({"soak_interval_s": 61}, (False, False, False)),
                 ({"soak_interval_s": 86400}, (False, False, False)),
                 ({"persisted_items": ("stream_binding",)}, (False, False, False)),
                 ({"persisted_items": items + ("vendor_extra",)}, (True, True, True)),
                 ({"topology_explicit": False}, (False, False, False)),
                 ({"idle_cycles": 99, "commit_cycles": 51}, (True, True, False)),
                 ({"idle_cycles": 101, "commit_cycles": 49}, (True, True, False)),
                 ({"idle_cycles": 101, "reset_cycles": 49}, (True, True, False)),
                 ({"idle_cycles": 150, "commit_cycles": 50, "reset_cycles": 0}, None),
                 ({"power_cycles": 199, "idle_cycles": 99}, (True, True, False)),
                 ({"power_cycles": 201, "reset_cycles": 51}, (True, True, True)),
                 ({"power_cycles": 201, "idle_cycles": 101}, (True, True, True))]
        cases += [({"persisted_items": tuple(i for i in items if i != item)}, (False, False, False))
                  for item in items]
        for changes, expected in cases:
            with self.subTest(changes=changes):
                if expected is None:
                    with self.assertRaises(ValueError):
                        replace(settings, **changes)
                    continue
                repeats = self._release_repeats(build_plan(
                    ["soak", "audio", "power"], release=replace(settings, **changes)))
                soak_ok, audio_ok, power_ok = expected
                self.assertEqual({sid: step.args["release_eligible"] for sid, step in repeats.items()},
                                 {"soak.continuous": soak_ok, "audio.integrity": audio_ok,
                                  "power.idle": power_ok, "power.journal_commit": power_ok,
                                  "power.soft_reset": power_ok})
        for step in self._release_repeats(build_plan(["soak", "audio", "power"])).values():
            self.assertFalse(step.args["release_eligible"])
        for changes in ({"restore_bound_s": 0}, {"restore_bound_s": True},
                        {"restore_bound_s": float("nan")}, {"boot_margin_s": -1},
                        {"power_off_hold_s": 0}, {"power_off_hold_s": -1},
                        {"power_off_hold_s": True}, {"power_off_hold_s": float("nan")},
                        {"boot_margin_s": False}, {"topology_explicit": "yes"}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                ReleaseSettings(**changes)

    def test_release_topology_provenance_cli(self) -> None:
        """Full explicit inputs qualify; missing or partial device specs do not."""
        import contextlib
        import io
        from unittest.mock import patch
        dut = "entity=0011223344556677,mac=001122334455,talkers=2,listeners=2,crf_out=2,crf_in=2"
        peer = "entity=8899aabbccddeeff,mac=8899aabbccdd,talker_index_set=0|2,listener_index_set=0|2,crf_out=3,crf_in=3"
        for flags, expected in (([], False), (["--dut", dut], False),
                                (["--peer", peer], False),
                                (["--dut", "name=dut", "--peer", peer], False),
                                (["--dut", dut, "--peer", peer], True)):
            with self.subTest(flags=flags):
                output = io.StringIO()
                argv = ["torture_campaign.py", "--plan", "--areas", "soak,audio,power", "--json"] + flags
                with patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
                    self.assertEqual(main(), 0)
                repeats = [step for step in json.loads(output.getvalue())
                           if step["op"] in RELEASE_REQUIRED_ASSERTS]
                self.assertEqual(len(repeats), 5)
                for step in repeats:
                    self.assertEqual(step["args"]["topology_explicit"], expected)
                    self.assertEqual(step["args"]["release_eligible"], expected)

    def test_release_topology_each_key(self) -> None:
        """L3 explicit means each key on each role, not any partial override."""
        import contextlib
        import io
        from unittest.mock import patch
        # These shapes remain valid when fixture fields are inherited, so a
        # missing-key case reaches eligibility instead of an overlap refusal.
        dut = "entity=0011223344556677,mac=001122334455,talkers=2,listeners=2,crf_out=16,crf_in=16"
        peer = ("entity=8899aabbccddeeff,mac=8899aabbccdd,talker_index_set=0|1,"
                "listener_index_set=0|1,crf_out=16,crf_in=16")
        for role in (0, 1):
            fields = dict(part.split("=", 1) for part in (dut, peer)[role].split(","))
            cases = [({key}, False) for key in fields]
            cases += [({"crf_in", "crf_out"}, False), ({"mac"}, True)]
            for omitted, empty in cases:
                specs = [dut, peer]
                specs[role] = ",".join(
                    f"{key}={'' if key in omitted else value}"
                    for key, value in fields.items() if empty or key not in omitted)
                with self.subTest(role=role, omitted=omitted, empty=empty):
                    output = io.StringIO()
                    argv = ["torture_campaign.py", "--plan", "--areas", "soak,audio,power", "--json",
                            "--dut", specs[0], "--peer", specs[1]]
                    with patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
                        self.assertEqual(main(), 0)
                    repeats = [step for step in json.loads(output.getvalue())
                               if step["op"] in RELEASE_REQUIRED_ASSERTS]
                    self.assertEqual(len(repeats), 5)
                    for step in repeats:
                        self.assertFalse(step["args"]["topology_explicit"])
                        self.assertFalse(step["args"]["release_eligible"])
            # Empty numeric/index-set values are refused by the parser;
            # independently pin that none can attest explicit provenance.
            for key in fields:
                specs = [dut, peer]
                specs[role] = ",".join(f"{k}={'' if k == key else v}" for k, v in fields.items())
                self.assertFalse(_release_topology_explicit(*specs), (role, key))
        for specs in ((dut, peer),
                      (dut.replace("listeners=2", "listener_index_set=0|1"),
                       peer.replace("talker_index_set=0|1", "talkers=2"))):
            self.assertTrue(_release_topology_explicit(*specs))
        self.assertFalse(_release_topology_explicit(dut.replace("entity=", "entity_id="), peer))

    def test_release_tu_contract(self) -> None:
        """L3 #396 round 4 anchors each interval at its last discontinuity."""
        soak = build_plan(["soak"])[0]
        self.assertEqual(soak.args["tu_holdover_bound_s"], 0.5)
        self.assertEqual(soak.args["tu_time_origin"], "last recorded discontinuity before tu clears")
        self.assertEqual(soak.args["tu_event_window"], "[observed_start - observation_resolution_s, clear)")
        self.assertEqual(soak.args["tu_discontinuity_kinds"],
                         ["PHC settime/adjtime", "fabric discontinuity", "GM-identity edge",
                          "GM time-source change", "other detected gPTP discontinuity"])
        self.assertEqual(soak.args["tu_observation_resolution"],
                         "record wire-capture and correlated event-timestamp resolution in seconds")
        self.assertEqual(soak.args["tu_uncorrelated"], "fail")

    def test_release_tu_chained_discontinuities(self) -> None:
        """L3 #396 round 4 examples independently pin passing and late clears."""
        bound_s = build_plan(["soak"])[0].args["tu_holdover_bound_s"]
        for clear_s, events_s, resolution_s, expected in (
                (0.62, [0, 0.2], 0.001, "PASS"),
                (0.8, [0, 0.2], 0.001, "FAIL"),
                (0.62, [], 0.001, "FAIL"),
                (0.62, [-0.1, 0.62, 0.7], 0.001, "FAIL"),
                (0.62, [0.2, 0, 0.9], 0.001, "PASS"),
                (0.75, [0, 0.25], 0, "PASS"),
                (0.751, [0, 0.25], 0, "FAIL"),
                (0.75, [0, 0.25], 0.01, "PASS"),
                (0.76, [0, 0.25], 0.01, "FAIL"),
                (0.761, [0, 0.25], 0.01, "FAIL")):
            with self.subTest(clear_s=clear_s, events_s=events_s, resolution_s=resolution_s):
                verdict, evidence = check_release_tu(
                    (0, clear_s), events_s, holdover_bound_s=bound_s,
                    observation_resolution_s=resolution_s, capture_complete=True, gm_changes_s=[])
                self.assertEqual(verdict, expected, evidence)
        for interval_s, events_s, resolution_s, complete in (
                ((0, 0.62), [0, 0.2], None, True),
                ((0, 0.62), [0, 0.2], 0.001, False),
                ((0.62, 0), [0.2], 0.001, True),
                ((0, 0.62), [float("nan")], 0.001, True),
                ((0, 0.62), [0.2], -1, True),
                ((0, 0.62), [0.2], True, True)):
            self.assertEqual(check_release_tu(
                interval_s, events_s, holdover_bound_s=bound_s,
                observation_resolution_s=resolution_s, capture_complete=complete, gm_changes_s=[])[0], "NOT RUN")

    def test_release_tu_start_resolution(self) -> None:
        """L3 #396 round 5: lone events bracket the observed start independently."""
        for event_s, resolution_s, expected in (
                (-0.0005, 0.001, "PASS"),
                (-0.002, 0.001, "FAIL"),
                (0, 0.001, "PASS"),
                (0, 0, "PASS"),
                (-0.1, 0.001, "FAIL"),
                (-0.001, 0.001, "PASS"),
                (-0.001001, 0.001, "FAIL"),
                (0.4, 0.001, "FAIL"),
                (0.401, 0.001, "FAIL")):
            with self.subTest(event_s=event_s, resolution_s=resolution_s):
                verdict, evidence = check_release_tu(
                    (0, 0.4), [event_s], holdover_bound_s=0.5,
                    observation_resolution_s=resolution_s, capture_complete=True, gm_changes_s=[])
                self.assertEqual(verdict, expected, evidence)
                if expected == "PASS":
                    self.assertEqual(evidence["last_discontinuity_s"], event_s)

        self.assertEqual(check_release_tu((0, 0.0005), [0.0005], gm_changes_s=[],
            holdover_bound_s=0.5, observation_resolution_s=0.001, capture_complete=True)[0], "FAIL")

    def test_release_tu_before_first_discontinuity(self) -> None:
        """L3 #593: the rise must coincide with its first recorded event."""
        for clear_s, expected in ((10.4, "FAIL"), (10.6, "FAIL")):
            verdict, evidence = check_release_tu(
                (0, clear_s), [10], holdover_bound_s=0.5,
                observation_resolution_s=0.001, capture_complete=True, gm_changes_s=[])
            self.assertEqual(verdict, expected, evidence)

    def test_release_assertion_text(self) -> None:
        """L3 #396: operator-facing instructions must preserve the decided rules."""
        specs = {spec.name: spec.clause for step in build_plan(["soak", "power"])
                 for spec in step.asserts}
        for phrase in ("contains at least one recorded discontinuity",
                       "GM-identity edge, GM time-source change, or other detected gPTP discontinuity",
                       "containment uses [observed_start - observation_resolution_s, clear)",
                       "launch-to-capture latency and event-to-capture correlation error",
                       "last recorded discontinuity before tu clears", "within 0.5 s plus",
                       "uncorrelated tu fails", "wire capture and correlated event timestamps",
                       "after each GM change, clear + observation_resolution_s must be at least",
                       "GM change + 0.25 s (Annex B.1.1 minimum); missing GM history is NOT RUN",
                       "first discontinuity must be within observation_resolution_s of the rise",
                       "grade every GM change against the complete tu interval history",
                       "a GM change with no covering interval fails",
                       "(including PHC settime/adjtime and fabric discontinuity)",
                       "true hold d is observed as h within +/- R, where R = observation_resolution_s",
                       "minimum accepts h + R >= 0.25 s, so d >= 0.25 s - 2 * R",
                       "require 2 * R < 0.25 s so an instant clear fails",
                       "upper bound requires h + R <= 0.5 s + R, equivalently h <= 0.5 s",
                       "resolution_limit_s is 0.125 s",
                       "coarser resolution is NOT RUN"):
            self.assertIn(phrase, specs["soak.tu-within-holdover"])
        self.assertIn("missing, NOT RUN, SKIP, INFO", specs["release.complete-evidence"])
        for phrase in ("valid_time measured from T0", "require valid_time=10 (20 s)",
                       "pre-cut advertisement age are provenance, " "not charged to",
                       "missing capture or a missed deadline fails",
                       "for a soft reset T0 is the host-timestamped reset command"):
            self.assertIn(phrase, specs["power.adp-valid-time"])
        decided = {
            "soak.continuous-duration": ("at least 86400 continuous seconds (24 h)",),
            "soak.no-counter-errors": ("zero SEQ_NUM_MISMATCH, STREAM_INTERRUPTED, LATE_TIMESTAMP and ",
                                       "EARLY_TIMESTAMP growth on every Stream Input, CRF included",
                                       "zero MEDIA_UNLOCKED growth of any cause, explained or not",
                                       "outside a recorded planted event"),
            "power.cycle-count-and-phase": ("200 cycles, 150 confirmed cold cuts (100 idle, 50 inside a ",
                                            "and 50 soft resets with power held on",
                                            "a reset never counts as a cold cut and a cut never as a reset"),
            "power.state-restored": ("restores the eight Milan items and the binding",
                                     "set each item away from its default before the cycle",
                                     "never mixed state"),
            "power.single-boot": ("after a cut and after a reset",),
        }
        for name, phrases in decided.items():
            for phrase in phrases:
                self.assertIn(phrase, specs[name], name)
        audio = {spec.name: spec.clause for step in build_plan(["audio"]) for spec in step.asserts}
        for name, phrase in (
                ("audio.inside-soak-window", "lasts at least 86400 continuous seconds"),
                ("audio.counter-classified", "n dropped, n repeated, n samples of silence"),
                ("audio.counter-classified", "a bit-flip mask or a channel swap"),
                ("audio.planted-arms-found", "voids the run as NOT RUN"),
                ("audio.capture-losses-apart", "never counted against the DUT"),
                ("audio.analog-sine-pair", "997 Hz and 9,973 Hz"),
                ("audio.analog-sine-pair", "NOT RUN until a recorded decision sets them"),
                ("audio.zero-dut-glitches", "zero DUT-attributed events"),
                ("release.control-fails-as-expected", "only when its expected assertion FAILs")):
            self.assertIn(phrase, audio[name], name)

    def test_release_crf_overlap_refused(self) -> None:
        """An AAF range or explicit set cannot also designate the CRF stream."""
        for base in (ARTY, PEER):
            for field, index in (("talker_index_set", base.crf_out),
                                 ("listener_index_set", base.crf_in)):
                device = parse_device_spec(f"{field}=0|{index}", base)
                dut, peer = (device, PEER) if base is ARTY else (ARTY, device)
                with self.subTest(device=base.name, field=field), self.assertRaisesRegex(ValueError, "AAF"):
                    build_plan(["soak", "power"], dut, peer)
        with self.assertRaisesRegex(ValueError, "AAF"):
            build_plan(["power"], replace(ARTY, crf_out=0), PEER)
        with self.assertRaisesRegex(ValueError, "AAF"):
            build_plan(["audio"], replace(ARTY, crf_in=0), PEER)
        for step in self._release_repeats(build_plan(["soak", "audio", "power"])).values():
            for target in step.args["counter_targets"]:
                device = ARTY if target["entity"] == ARTY.entity_id else PEER
                crf = device.crf_in if target["descriptor"] == "stream_input" else device.crf_out
                self.assertEqual(target["crf"], target["index"] == crf)

    def test_release_boot_negative_control(self) -> None:
        """L3 #366: two BIOS passes fail even when the second boot is healthy."""
        self.assertEqual(check_release_boot(1, 0, capture_complete=True)[0], "PASS")
        for passes, restarts in ((2, 1), (2, 0), (1, 1), (0, 0)):
            self.assertEqual(check_release_boot(passes, restarts, capture_complete=True)[0], "FAIL")
        for passes, restarts in ((None, 0), (1, None), (-1, 0), (True, 0),
                                (1, True), (1, False), (1, -1)):
            self.assertEqual(check_release_boot(passes, restarts, capture_complete=True)[0], "SKIP")
        self.assertEqual(check_release_boot(1, 0, capture_complete=False)[0], "SKIP")
        repeats = self._release_repeats(build_plan(["power"])).values()
        self.assertEqual(len(repeats), 3)
        for step in repeats:
            self.assertIn("power.single-boot", {spec.name for spec in step.asserts})
            self.assertEqual(step.args["boot_max_passes"], 1)
            self.assertEqual(step.args["boot_max_restarts"], 0)
            self.assertEqual(step.args["boot_evidence"],
                             "complete UART/reset observation from T0 through next cycle or campaign end; "
                             "at least boot_observation_s")


class _ReleaseSoakChecks:
    """Issue #593 recorded-event controls, independent of the release constants."""

    def _mr_trace(self, *, second_toggle: int | None = None) -> list[dict]:
        return [{"stream_id": "stream-a", "timestamp_s": index / 100,
                 "pdu_index": index, "mr": int(index >= 1 and
                                              (second_toggle is None or index < second_toggle))}
                for index in range(20)]

    def _mr_grade(self, *, pdus=None, causes=None, reads=None, resolution_s=0.001) -> tuple[str, dict]:
        return check_release_mr(
            "stream-a", self._mr_trace() if pdus is None else pdus,
            [{"stream_id": "stream-a", "timestamp_s": 0.01,
              "kind": "media-clock-source change"}] if causes is None else causes,
            [{"stream_id": "stream-a", "timestamp_s": 0, "value": 0},
             {"stream_id": "stream-a", "timestamp_s": 0.19, "value": 1}] if reads is None else reads,
            observation_resolution_s=resolution_s, capture_complete=ReleaseCapture((-2, 2)))

    def test_release_mr_allowed_causes(self) -> None:
        """Each allowed clock cause independently explains a toggle and reset."""
        for kind in ("media-clock-source change", "CRF disruption", "CRF mr toggle"):
            with self.subTest(kind=kind):
                verdict, evidence = self._mr_grade(causes=[
                    {"stream_id": "stream-a", "timestamp_s": 0.01, "kind": kind}])
                self.assertEqual(verdict, "PASS", evidence)
                self.assertEqual(evidence["media_reset_increments"], 1)
                self.assertEqual(evidence["observation_resolution_s"], 0.001)

    def test_release_mr_no_cause(self) -> None:
        """A complete empty cause history cannot excuse an observed toggle."""
        self.assertEqual(self._mr_grade(causes=[])[0], "FAIL")

    def test_release_mr_gm_only(self) -> None:
        """A GM edge or PHC step alone is not a media-clock-source change."""
        for kind in ("GM-identity edge", "PHC settime/adjtime", "GM time-source change"):
            self.assertEqual(self._mr_grade(causes=[
                {"stream_id": "stream-a", "timestamp_s": 0.01, "kind": kind}])[0], "FAIL")

    def test_release_mr_resolution(self) -> None:
        """A measured relative timestamp bound controls both matching edges."""
        for timestamp_s, expected in ((0.009, "PASS"), (0.011, "PASS"),
                                      (0.0089, "FAIL"), (0.0111, "FAIL")):
            with self.subTest(timestamp_s=timestamp_s):
                self.assertEqual(self._mr_grade(causes=[
                    {"stream_id": "stream-a", "timestamp_s": timestamp_s,
                     "kind": "CRF disruption"}])[0], expected)
        self.assertEqual(self._mr_grade(resolution_s=0)[0], "PASS")
        self.assertEqual(self._mr_grade(causes=[
            {"stream_id": "stream-a", "timestamp_s": 0.02, "kind": "CRF disruption"}],
            resolution_s=0.02)[0], "PASS")

    def test_release_mr_stream_scope(self) -> None:
        """Neither another stream's cause nor its PDUs can satisfy this stream."""
        self.assertEqual(self._mr_grade(causes=[
            {"stream_id": "stream-b", "timestamp_s": 0.01, "kind": "CRF disruption"}])[0], "FAIL")
        pdus = self._mr_trace(second_toggle=8)
        mixed = []
        for pdu in pdus:
            mixed.extend([dict(pdu, stream_id="stream-b", mr=0), pdu])
        causes = [{"stream_id": "stream-a", "timestamp_s": stamp, "kind": "CRF disruption"}
                  for stamp in (0.01, 0.08)]
        self.assertEqual(self._mr_grade(pdus=mixed, causes=causes)[0], "FAIL")

    def test_release_mr_eight_pdus(self) -> None:
        """Seven PDUs fails; exactly eight passes, including a falling toggle."""
        for second_toggle, expected in ((8, "FAIL"), (9, "PASS")):
            causes = [{"stream_id": "stream-a", "timestamp_s": stamp, "kind": "CRF mr toggle"}
                      for stamp in (0.01, second_toggle / 100)]
            verdict, evidence = self._mr_grade(pdus=self._mr_trace(second_toggle=second_toggle), causes=causes)
            self.assertEqual(verdict, expected, evidence)
        self.assertEqual(self._mr_grade(pdus=self._mr_trace()[:8])[0], "NOT RUN")
        self.assertEqual(self._mr_grade(pdus=self._mr_trace()[:9])[0], "PASS")

    def test_release_media_reset_no_cause(self) -> None:
        """A counter increase without a caused wire toggle must fail."""
        steady = [dict(pdu, mr=0) for pdu in self._mr_trace()]
        self.assertEqual(self._mr_grade(pdus=steady, causes=[])[0], "FAIL")
        self.assertEqual(self._mr_grade(reads=[
            {"stream_id": "stream-a", "timestamp_s": 0, "value": 0},
            {"stream_id": "stream-a", "timestamp_s": 0.19, "value": 2}])[0], "FAIL")

    def test_release_media_reset_intervals(self) -> None:
        """Counts are per device interval, with bounded deferred updates."""
        for before_s, expected in ((1.01, "PASS"), (1.011, "PASS"), (1.0111, "FAIL")):
            reads = [{"stream_id": "stream-a", "timestamp_s": before_s, "value": 0},
                     {"stream_id": "stream-a", "timestamp_s": 1.5, "value": 1}]
            self.assertEqual(self._mr_grade(reads=reads)[0], expected)
        causes = [{"stream_id": "stream-a", "timestamp_s": stamp, "kind": "CRF disruption"}
                  for stamp in (0.01, 0.09)]
        self.assertEqual(self._mr_grade(pdus=self._mr_trace(second_toggle=9), causes=causes)[0], "PASS")
        reads = [{"stream_id": "stream-a", "timestamp_s": stamp, "value": value}
                 for stamp, value in ((0, 0), (0.1, 1), (0.19, 2))]
        self.assertEqual(self._mr_grade(reads=reads)[0], "FAIL")
        reads = [{"stream_id": "stream-a", "timestamp_s": 0, "value": 2**32 - 1},
                 {"stream_id": "stream-a", "timestamp_s": 0.19, "value": 0}]
        verdict, evidence = self._mr_grade(reads=reads)
        self.assertEqual(verdict, "FAIL", evidence)
        self.assertIn("counter reset", evidence["why"])

    def test_release_mr_missing_evidence(self) -> None:
        """Missing records, incomplete capture and invalid resolution never pass."""
        args = dict(stream_id="stream-a", pdus=self._mr_trace(), causes=[],
                    media_reset_reads=[{"stream_id": "stream-a", "timestamp_s": 0, "value": 0},
                                       {"stream_id": "stream-a", "timestamp_s": 1, "value": 0}],
                    observation_resolution_s=0.001, capture_complete=ReleaseCapture((-2, 2)))
        args["pdus"][0]["timestamp_s"] = -2
        args["pdus"][-1]["timestamp_s"] = 2
        for key, value in (("pdus", None), ("causes", None), ("media_reset_reads", None),
                           ("media_reset_reads", []), ("capture_complete", False),
                           ("observation_resolution_s", None), ("observation_resolution_s", -1),
                           ("observation_resolution_s", float("nan")), ("observation_resolution_s", True)):
            with self.subTest(key=key, value=value):
                self.assertEqual(check_release_mr(**dict(args, **{key: value}))[0], "NOT RUN")
        for pdus in (self._mr_trace()[::2], list(reversed(self._mr_trace())),
                     [dict(pdu, mr=2) for pdu in self._mr_trace()],
                     [dict(pdu, pdu_index=True) for pdu in self._mr_trace()]):
            self.assertEqual(self._mr_grade(pdus=pdus)[0], "NOT RUN")
        # Complete capture of a silent, unbound stream is different from missing capture.
        self.assertEqual(check_release_mr(**dict(args, pdus=[]))[0], "PASS")

    def test_release_tu_gm_minimum(self) -> None:
        """The latest GM edge requires 0.25 s, allowing recorded resolution."""
        for clear_s, gm_s, resolution_s, expected in (
                (0.24, [0], 0.001, "FAIL"), (0.25, [0], 0, "PASS"),
                (0.249, [0], 0.001, "PASS"), (0.248, [0], 0.001, "FAIL"),
                (0.4, [0, 0.2], 0.001, "FAIL"), (0.45, [0, 0.2], 0, "PASS"),
                (0.62, [0], 0.001, "PASS"), (0.8, [0], 0.001, "FAIL"),
                (0.1, [], 0.001, "PASS"), (0.249, [-0.001], 0, "PASS"),
                (0.24, [-0.002], 0.001, "FAIL")):
            with self.subTest(clear_s=clear_s, gm_s=gm_s, resolution_s=resolution_s):
                verdict, evidence = check_release_tu(
                    (0, clear_s), [0, 0.2] if clear_s > 0.2 else [0],
                    gm_changes_s=gm_s, holdover_bound_s=0.5,
                    observation_resolution_s=resolution_s, capture_complete=True)
                self.assertEqual(verdict, expected, evidence)
                self.assertEqual(evidence["observation_resolution_s"], resolution_s)
        verdict, evidence = check_release_tu((0, 0.25), [], gm_changes_s=[0], holdover_bound_s=0.5,
                                             observation_resolution_s=0, capture_complete=True)
        self.assertEqual(verdict, "PASS", evidence)

    def test_release_tu_missing_gm_history(self) -> None:
        """An omitted GM history cannot silently bypass the minimum check."""
        for gm_s in (None, [float("nan")], [True]):
            self.assertEqual(check_release_tu(
                (0, 0.1), [0], gm_changes_s=gm_s, holdover_bound_s=0.5,
                observation_resolution_s=0.001, capture_complete=True)[0], "NOT RUN")
        self.assertEqual(exit_code([verdict_record("soak", "mr", "NOT RUN")]), 2)

    def test_release_mr_plan_contract(self) -> None:
        """The emitted soak contract requires all inputs used by the checks."""
        step = build_plan(["soak"])[0]
        args = step.args
        self.assertEqual(args["mr_oracle"], "check_release_mr")
        self.assertEqual(args["mr_cause_kinds"],
                         ["media-clock-source change", "CRF disruption", "CRF mr toggle"])
        self.assertEqual(args["mr_hold_pdus"], 8)
        self.assertEqual(args["mr_cause_window"], "toggle timestamp +/- observation_resolution_s")
        self.assertEqual(args["mr_counter_update_bound_s"], 1)
        self.assertEqual(args["mr_pdu_index"], "unwrapped per-stream capture index")
        self.assertEqual(args["tu_gm_minimum_s"], 0.25)
        self.assertEqual(args["tu_gm_minimum_check"], "clear + observation_resolution_s >= GM change + 0.25 s")
        self.assertEqual(args["missing_evidence"], "NOT RUN")
        self.assertTrue({"mr_pdus", "media_clock_events", "MEDIA_RESET_reads", "gptp_discontinuities", "gm_changes"}
                        <= set(args["continuous_evidence"]))
        assertion = next(spec.clause for spec in step.asserts if spec.name == "soak.mr-causes-and-hold")
        for phrase in ("4.4.4.3", "B.1.2", "Tables 5.4/5.6", "GM change alone fails",
                       "at least 8 AVTPDUs of that stream",
                       "match causes within +/- observation_resolution_s of the toggle",
                       "mapped to that stream's clock source; GM change alone fails",
                       "missing packet, cause, counter or resolution evidence is NOT RUN",
                       "every mr toggle and MEDIA_RESET increment needs a recorded",
                       "media-clock-source change, CRF disruption, or received CRF mr toggle",
                       "MEDIA_RESET counts observation intervals, not packets",
                       "each cause excuses at most one toggle per stream",
                       "2 * observation_resolution_s must be less than the 1 s counter interval ceiling",
                       "capture must span [first read - 1 s - observation_resolution_s, last read]",
                       "a MEDIA_RESET decrease is a counter reset, not a wrap"):
            self.assertIn(phrase, assertion)

    def test_release_tu_rise_boundary(self) -> None:
        """The first event brackets the rise at both inclusive R edges."""
        for event, expected in ((0.001, "PASS"), (0.001001, "FAIL")):
            verdict, detail = check_release_tu((0, 0.3), [event], gm_changes_s=[],
                holdover_bound_s=0.5, observation_resolution_s=0.001, capture_complete=True)
            self.assertEqual(verdict, expected, detail)

    def test_release_tu_history(self) -> None:
        """Missing, absent and late tu are distinct even across several GM changes."""
        args = dict(discontinuities_s=[0], gm_changes_s=[0],
                    observation_resolution_s=0.001, capture_complete=True)
        for intervals, gm, expected in (
                (None, [0], "NOT RUN"), ([], [0], "FAIL"), ([], [], "PASS"),
                ([(0, 0.3)], [0], "PASS"), ([(0, 0.3)], [0, 0.3], "FAIL"),
                ([(0, 0.3)], [0, 0.35], "FAIL"), ([(0, 0.3)], [-0.002], "FAIL"),
                ([(0, 0.3)], [-0.001], "PASS"),
                ([(0, 0.3), (1, 1.3)], [0, 1], "PASS"),
                ([(0, 0.3), (1, 1.24)], [0, 1], "FAIL"),
                ([(0, 0.3), (1, 1.6)], [0, 1], "FAIL"),
                ([(0, 0.3), (1, 1.3)], [0, 1.1], "FAIL"),
                ([(0, 0.3), (0.2, 0.5)], [0], "NOT RUN"),
                ([(1, 1.3), (0, 0.3)], [0, 1], "NOT RUN"),
                ([(0, 0)], [0], "NOT RUN"), ([(0,)], [0], "NOT RUN"),
                ([(0, float("nan"))], [0], "NOT RUN")):
            with self.subTest(intervals=intervals, gm=gm):
                verdict, detail = check_release_tu_history(intervals, **dict(args, gm_changes_s=gm))
                self.assertEqual(verdict, expected, detail)
        for field, value in (("gm_changes_s", None), ("discontinuities_s", None),
                             ("gm_changes_s", [float("nan")]), ("capture_complete", False),
                             ("observation_resolution_s", 0.25), ("observation_resolution_s", None)):
            self.assertEqual(check_release_tu_history([], **dict(args, **{field: value}))[0], "NOT RUN")
        for gm in ([0.3], [0.35], [0, 0.5]):
            self.assertEqual(check_release_tu((0, 0.3), holdover_bound_s=0.5, **dict(args, gm_changes_s=gm))[0], "FAIL")

    def test_release_deciding_resolution(self) -> None:
        """An uncertainty as large as a decision limit cannot qualify evidence."""
        for resolution, expected in ((0.124999, "PASS"), (0.125, "NOT RUN"),
                                     (0.125001, "NOT RUN"), (0.249, "NOT RUN"), (0.25, "NOT RUN"),
                                     (0.3, "NOT RUN"), (0.5, "NOT RUN"), (60, "NOT RUN")):
            verdict, detail = check_release_tu((0, 0.3), [0], gm_changes_s=[0],
                holdover_bound_s=0.5, observation_resolution_s=resolution, capture_complete=True)
            self.assertEqual(verdict, expected, detail)
            self.assertEqual(detail.get("resolution_limit_s"), 0.125)
        for resolution, expected in ((0.499, "PASS"), (0.5, "NOT RUN"), (1, "NOT RUN")):
            verdict, detail = self._mr_grade(resolution_s=resolution)
            self.assertEqual(verdict, expected, detail)
            self.assertEqual(detail.get("resolution_limit_s"), 0.5)
        for interval, bound in (((0, 0), 0.5), ((0, 0.3), 5)):
            self.assertEqual(check_release_tu(interval, [-0.0005], gm_changes_s=[],
                holdover_bound_s=bound, observation_resolution_s=0.001, capture_complete=True)[0], "NOT RUN")

    def test_release_tu_two_sided_boundaries(self) -> None:
        """Instant clears fail below the derived limit; coarse evidence is refused."""
        for resolution, clear, expected in (
                (0.249, 0.002, "NOT RUN"), (0.2, 0.06, "NOT RUN"),
                (0.125, 0.13, "NOT RUN"), (0.124, 0.124, "FAIL"),
                (0.124999, 0.124999, "FAIL"), (0.125, 0.125, "NOT RUN"),
                (0.125001, 0.125001, "NOT RUN"),
                (0.124999, 0.125001, "PASS"), (0.124999, 0.125000, "FAIL"),
                (0, 0.25, "PASS"), (0, 0.249999, "FAIL")):
            with self.subTest(resolution=resolution, clear=clear):
                single = check_release_tu((0, clear), [], gm_changes_s=[0],
                    holdover_bound_s=0.5, observation_resolution_s=resolution, capture_complete=True)
                history = check_release_tu_history([(0, clear)], [], gm_changes_s=[0],
                    observation_resolution_s=resolution, capture_complete=True)
                for verdict, detail in (single, history):
                    self.assertEqual(verdict, expected, detail)
                    self.assertEqual(detail.get("resolution_limit_s"), 0.125)
        for resolution in (0, 0.001, 0.124999):
            for clear, expected in ((0.499999, "PASS"), (0.5, "PASS"), (0.500001, "FAIL")):
                # A true hold up to h + R is possible. h > 0.5 cannot pass.
                with self.subTest(resolution=resolution, clear=clear):
                    verdict, detail = check_release_tu((0, clear), [0], gm_changes_s=[],
                        holdover_bound_s=0.5, observation_resolution_s=resolution, capture_complete=True)
                    self.assertEqual(verdict, expected, detail)
                    self.assertAlmostEqual(detail["latest_clear_s"], clear + resolution)
                    self.assertAlmostEqual(detail["deadline_s"], 0.5 + resolution)
                    self.assertEqual(check_release_tu_history([(0, clear)], [0], gm_changes_s=[],
                        observation_resolution_s=resolution, capture_complete=True)[0], expected)
        for resolution, expected in ((0.124999, "PASS"), (0.125, "NOT RUN"), (0.125001, "NOT RUN")):
            self.assertEqual(check_release_tu_history([], [], gm_changes_s=[],
                observation_resolution_s=resolution, capture_complete=True)[0], expected)

    def test_release_tu_history_boundaries(self) -> None:
        """Both GM assignment edges and interval separateness affect real verdicts."""
        for intervals, events, gm, expected in (
                ([(0, 0.01)], [0], [-0.0005], "FAIL"),
                ([(0, 0.01)], [0], [-0.001], "FAIL"),
                ([(0, 0.3), (0.3005, 0.6)], [], [0, 0.3], "PASS"),
                ([(0, 0.3), (0.3, 0.6)], [0, 0.3], [0], "NOT RUN"),
                ([(0, 0.3), (0.300001, 0.6)], [0, 0.3], [0], "PASS")):
            with self.subTest(intervals=intervals, gm=gm):
                verdict, detail = check_release_tu_history(intervals, events, gm_changes_s=gm,
                    observation_resolution_s=0.001, capture_complete=True)
                self.assertEqual(verdict, expected, detail)
                self.assertEqual(detail.get("resolution_limit_s"), 0.125)
        self.assertEqual(check_release_tu_history([], [], gm_changes_s=[],
            observation_resolution_s=-1, capture_complete=True)[0], "NOT RUN")

    def test_release_resolution_evidence(self) -> None:
        """Every refusal path retains the measured resolution and deciding limit."""
        single = dict(interval_s=(0, 0.3), discontinuities_s=[0], gm_changes_s=[0],
                      holdover_bound_s=0.5, observation_resolution_s=0.001, capture_complete=True)
        history = dict(intervals_s=[], discontinuities_s=[], gm_changes_s=[],
                       observation_resolution_s=0.001, capture_complete=True)
        for oracle, args, cases in (
                (check_release_tu, single,
                 (("capture_complete", False), ("gm_changes_s", None), ("interval_s", None),
                  ("interval_s", (0,)), ("interval_s", (0, 0)), ("holdover_bound_s", 5),
                  ("observation_resolution_s", None), ("observation_resolution_s", -1),
                  ("observation_resolution_s", float("inf")), ("observation_resolution_s", 0.125))),
                (check_release_tu_history, history,
                 (("capture_complete", False), ("intervals_s", None), ("gm_changes_s", None),
                  ("discontinuities_s", [float("inf")]), ("intervals_s", [(0,)]),
                  ("intervals_s", [(0, 0)]), ("observation_resolution_s", None),
                  ("observation_resolution_s", -1), ("observation_resolution_s", 0.125)))):
            for key, value in cases:
                with self.subTest(oracle=oracle.__name__, key=key, value=value):
                    verdict, detail = oracle(**dict(args, **{key: value}))
                    self.assertEqual(verdict, "NOT RUN", detail)
                    self.assertEqual(detail.get("resolution_limit_s"), 0.125)
                    self.assertEqual(detail["observation_resolution_s"], value if
                                     key == "observation_resolution_s" else 0.001)
        args = dict(stream_id="s", pdus=[], causes=[], media_reset_reads=[],
                    observation_resolution_s=0.001, capture_complete=ReleaseCapture((-2, 2)))
        for key, value in (("capture_complete", False), ("pdus", None),
                           ("observation_resolution_s", None), ("observation_resolution_s", -1),
                           ("observation_resolution_s", 0.5), ("media_reset_reads", [])):
            verdict, detail = check_release_mr(**dict(args, **{key: value}))
            self.assertEqual(verdict, "NOT RUN", detail)
            self.assertEqual(detail.get("resolution_limit_s"), 0.5)
            self.assertEqual(detail["observation_resolution_s"], value if
                             key == "observation_resolution_s" else 0.001)
        self.assertEqual(self._mr_grade()[1]["cause_window"],
                         "toggle timestamp +/- observation_resolution_s")

    def test_release_mr_distinct_causes(self) -> None:
        """One cause cannot excuse a run of eight-PDU-spaced toggles."""
        pdus = [dict(pdu, timestamp_s=pdu["pdu_index"] / 8000)
                for pdu in self._mr_trace(second_toggle=9)]
        one = [{"stream_id": "stream-a", "timestamp_s": 0.000125, "kind": "CRF disruption"}]
        self.assertEqual(self._mr_grade(pdus=pdus, causes=one, resolution_s=0.002)[0], "FAIL")
        two = one + [dict(one[0], timestamp_s=0.001125)]
        self.assertEqual(self._mr_grade(pdus=pdus, causes=two, resolution_s=0.002)[0], "PASS")
        # Reverse recording order must not spend the later-only cause first.
        two = [dict(one[0], timestamp_s=0.001), dict(one[0], timestamp_s=-0.0008)]
        self.assertEqual(self._mr_grade(pdus=pdus, causes=two, resolution_s=0.001)[0], "PASS")

    def test_release_mr_record_boundaries(self) -> None:
        """Counter endpoints, record types and timestamp ordering are evidence."""
        reads = [{"stream_id": "stream-a", "timestamp_s": 0, "value": 0},
                 {"stream_id": "stream-a", "timestamp_s": 0.19, "value": 1}]
        foreign = [dict(read, stream_id="stream-b", value=9) for read in reads]
        self.assertEqual(self._mr_grade(reads=reads + foreign)[0], "PASS")
        for bad in (reads[:1], list(reversed(reads)), [reads[0], dict(reads[1], timestamp_s=0)],
                    [reads[0], dict(reads[1], value=-1)], [reads[0], dict(reads[1], value=2**32)]):
            self.assertEqual(self._mr_grade(reads=bad)[0], "NOT RUN")
        pdus = self._mr_trace()
        pdus[3] = dict(pdus[3], timestamp_s=0.015)
        self.assertEqual(self._mr_grade(pdus=pdus)[0], "NOT RUN")
        self.assertEqual(self._mr_grade(pdus=[dict(pdu, pdu_index=pdu["pdu_index"] - 5)
                                            for pdu in self._mr_trace()])[0], "NOT RUN")
        valid_cause = {"stream_id": "stream-a", "timestamp_s": 0.01, "kind": "CRF disruption"}
        self.assertEqual(self._mr_grade(causes=[valid_cause, dict(valid_cause, stream_id="")])[0], "NOT RUN")
        causes = [{"stream_id": "stream-a", "timestamp_s": 0.01, "kind": "CRF disruption"},
                  {"stream_id": "stream-a", "timestamp_s": 0.02, "kind": 1}]
        self.assertEqual(self._mr_grade(causes=causes)[0], "NOT RUN")

    def test_release_media_reset_window_edges(self) -> None:
        """Both counter edges and earliest-toggle consumption affect the verdict."""
        for after, expected in ((0.009, "PASS"), (0.008999, "FAIL")):
            reads = [{"stream_id": "stream-a", "timestamp_s": 0, "value": 0},
                     {"stream_id": "stream-a", "timestamp_s": after, "value": 1}]
            self.assertEqual(self._mr_grade(reads=reads)[0], expected)
        pdus = self._mr_trace(second_toggle=9)
        causes = [{"stream_id": "stream-a", "timestamp_s": stamp, "kind": "CRF disruption"}
                  for stamp in (0.01, 0.09)]
        reads = [{"stream_id": "stream-a", "timestamp_s": stamp, "value": value}
                 for stamp, value in ((0, 0), (1.05, 1), (1.1, 2))]
        self.assertEqual(self._mr_grade(pdus=pdus, causes=causes, reads=reads)[0], "PASS")

    def test_release_mr_capture_span(self) -> None:
        """A complete capture declaration still needs recorded span endpoints."""
        args = dict(stream_id="stream-a", pdus=self._mr_trace(),
                    causes=[{"stream_id": "stream-a", "timestamp_s": 0.01, "kind": "CRF disruption"}],
                    media_reset_reads=[{"stream_id": "stream-a", "timestamp_s": 0, "value": 0},
                                       {"stream_id": "stream-a", "timestamp_s": 0.19, "value": 1}],
                    observation_resolution_s=0.001)
        for window, expected in ((None, "NOT RUN"), ((-1.001, 0.19), "PASS"),
                                 ((-1, 0.19), "NOT RUN"), ((-1.001, 0.18), "NOT RUN"),
                                 ((0, 0), "NOT RUN"), ((-2,), "NOT RUN"),
                                 ((-2, float("nan")), "NOT RUN")):
            capture = ReleaseCapture(window) if window is not None else True
            verdict, detail = check_release_mr(**args, capture_complete=capture)
            self.assertEqual(verdict, expected, detail)
        # No packet outside the window can mask the endpoint-only guard.
        short = [dict(pdu, timestamp_s=pdu["timestamp_s"] / 2) for pdu in args["pdus"]]
        self.assertEqual(check_release_mr(**dict(args, pdus=short),
            capture_complete=ReleaseCapture((-2, 0.18)))[0], "NOT RUN")
        self.assertEqual(check_release_mr(**args,
            capture_complete=ReleaseCapture((-2, 2), complete=False))[0], "NOT RUN")
        outside = [dict(pdu) for pdu in args["pdus"]]
        outside[-1]["timestamp_s"] = 0.2
        self.assertEqual(check_release_mr(**dict(args, pdus=outside),
            capture_complete=ReleaseCapture((-2, 0.19)))[0], "NOT RUN")
        extended = [dict(pdu) for pdu in args["pdus"]]
        extended[0]["timestamp_s"] = -1.001
        self.assertEqual(check_release_mr(**dict(args, pdus=extended), capture_complete=True)[0], "PASS")
        self.assertEqual(check_release_mr(**dict(args, pdus=extended),
            capture_complete=ReleaseCapture((-1, 1)))[0], "NOT RUN")
        args.update(pdus=[], causes=[], media_reset_reads=[dict(read, value=0) for read in args["media_reset_reads"]])
        self.assertEqual(check_release_mr(**args, capture_complete=True)[0], "NOT RUN")
        self.assertEqual(check_release_mr(**args, capture_complete=ReleaseCapture((-2, 2)))[0], "PASS")

    def test_release_media_reset_decrease(self) -> None:
        """Talker-start resets never decode as billions of new events."""
        for before in (3, 2**32 - 1):
            reads = [{"stream_id": "stream-a", "timestamp_s": 0, "value": before},
                     {"stream_id": "stream-a", "timestamp_s": 0.19, "value": 0}]
            verdict, detail = self._mr_grade(reads=reads)
            self.assertEqual(verdict, "FAIL", detail)
            self.assertIn("counter reset", detail["why"])
            self.assertNotIn("delta", detail)

    def test_release_round2_plan_contract(self) -> None:
        """The plan selects the history oracle and states evidence limits."""
        args = build_plan(["soak"])[0].args
        expected = {"tu_oracle": "check_release_tu_history", "tu_resolution_limit_s": 0.125,
                    "tu_rise_check": "first discontinuity <= observed_start + observation_resolution_s",
                    "mr_capture_window": "[first read - 1 s - observation_resolution_s, last read]",
                    "mr_distinct_causes": True, "mr_resolution_limit_s": 0.5}
        for key, value in expected.items():
            self.assertEqual(args[key], value)


class _ReleaseGateChecks:
    """Issue #396 owner decisions 2026-10-26: stricter soak counters, the eight
    saved-state items, the audio counter grader and the negative controls."""

    _NAMES = ("SEQ_NUM_MISMATCH", "STREAM_INTERRUPTED", "LATE_TIMESTAMP",
              "EARLY_TIMESTAMP", "MEDIA_UNLOCKED")

    def _reads(self, target: str = "in-0", **after: int) -> list[dict]:
        base = {name: 7 for name in self._NAMES}
        return [{"target": target, "timestamp_s": 0, "values": dict(base)},
                {"target": target, "timestamp_s": 60, "values": dict(base, **after)}]

    def _counters(self, reads, planted=(), targets=("in-0",), complete=True):
        return check_release_soak_counters(reads, list(planted) if planted is not None else None,
                                           targets=list(targets), capture_complete=complete)

    def test_release_soak_counter_growth(self) -> None:
        """L3 #396 item 3: any growth of the four counters fails, each alone."""
        self.assertEqual(self._counters(self._reads())[0], "PASS")
        for name in ("SEQ_NUM_MISMATCH", "STREAM_INTERRUPTED", "LATE_TIMESTAMP", "EARLY_TIMESTAMP"):
            with self.subTest(name=name):
                verdict, detail = self._counters(self._reads(**{name: 8}))
                self.assertEqual(verdict, "FAIL", detail)
                self.assertEqual(detail["counter"], name)
                planted = [{"target": "in-0", "kind": "CRF disruption", "window_s": (10, 20)}]
                self.assertEqual(self._counters(self._reads(**{name: 8}), planted)[0], "FAIL")
        for name in self._NAMES:
            verdict, detail = self._counters(self._reads(**{name: 6}))
            self.assertEqual(verdict, "FAIL", detail)
            self.assertIn("reset", detail["why"])

    def test_release_soak_media_unlocked_planted(self) -> None:
        """L3 #396 item 3: an unlock passes only between two reads inside one planted window."""
        planted = {"target": "in-0", "kind": "CRF disruption", "window_s": (10, 20)}

        def bracketed(inside: int, outside: int) -> list[dict]:
            """Reads at 0, 10, 20 and 60 s; `inside` unlocks in (10, 20], `outside` in (20, 60]."""
            base = {name: 7 for name in self._NAMES}
            return [{"target": "in-0", "timestamp_s": t, "values": dict(base, MEDIA_UNLOCKED=7 + count)}
                    for t, count in ((0, 0), (10, 0), (20, inside), (60, inside + outside))]

        for events, inside, outside, expected in (
                ([], 1, 0, "FAIL"), ([planted], 1, 0, "PASS"), ([planted], 2, 0, "FAIL"),
                ([planted], 0, 1, "FAIL"), ([planted, dict(planted)], 2, 0, "PASS"),
                ([dict(planted, target="in-1")], 1, 0, "FAIL"),
                ([dict(planted, window_s=(5, 25))], 1, 0, "PASS"),
                ([dict(planted, window_s=(10, 19.999))], 1, 0, "FAIL"),
                ([dict(planted, window_s=(10.001, 20))], 1, 0, "FAIL"),
                ([dict(planted, window_s=(5, 25))], 1, 1, "FAIL"),
                # One window holding two read intervals still excuses one increment.
                ([dict(planted, window_s=(0, 60))], 1, 1, "FAIL"),
                ([dict(planted, window_s=(0, 60)), dict(planted, window_s=(0, 60))], 1, 1, "PASS")):
            with self.subTest(events=events, inside=inside, outside=outside):
                verdict, detail = self._counters(bracketed(inside, outside), events)
                self.assertEqual(verdict, expected, detail)
        # A planted window inside a periodic interval cannot excuse the whole interval:
        # an unlock 25 s after the window, between reads 60 s apart, fails.
        verdict, detail = self._counters(self._reads(MEDIA_UNLOCKED=8), [planted])
        self.assertEqual((verdict, detail.get("why")), ("FAIL", "MEDIA_UNLOCKED outside a planted event"))
        self.assertEqual(self._counters(self._reads(MEDIA_UNLOCKED=8),
                                        [dict(planted, window_s=(0, 60))])[0], "PASS")

    def test_release_soak_counter_evidence(self) -> None:
        """Missing reads, targets or log, and malformed records, are NOT RUN."""
        reads = self._reads()
        for args in ({"reads": None}, {"planted": None}, {"complete": False},
                     {"targets": ()}, {"targets": ("in-0", "crf-in")},
                     {"reads": reads[:1]}, {"reads": list(reversed(reads))},
                     {"reads": [reads[0], dict(reads[1], values={"SEQ_NUM_MISMATCH": 7})]},
                     {"reads": [reads[0], dict(reads[1], values=dict(reads[1]["values"],
                                                                     LATE_TIMESTAMP=2**32))]},
                     {"planted": [{"target": "in-0", "kind": "x", "window_s": (5, 1)}]},
                     {"planted": [{"target": "in-0", "kind": "", "window_s": (1, 5)}]}):
            with self.subTest(args=args):
                call = dict({"reads": reads, "planted": [], "targets": ("in-0",), "complete": True}, **args)
                self.assertEqual(self._counters(call["reads"], call["planted"], call["targets"],
                                                call["complete"])[0], "NOT RUN")
        crf = self._reads("crf-in", LATE_TIMESTAMP=8)
        self.assertEqual(self._counters(reads + crf, targets=("in-0", "crf-in"))[0], "FAIL")

    def _state(self, phase="idle", **changes):
        items = ("configuration", "stream_binding")
        call = {"pre": {item: "set" for item in items}, "post": {item: "set" for item in items},
                "defaults": {item: "default" for item in items}, "committed": None}
        call.update(changes)
        return check_release_state_restored(call["pre"], call["post"], call["defaults"],
                                            items=items, phase=phase, committed=call["committed"])

    def test_release_state_restored(self) -> None:
        """L3 #396 item 3: every item restored, each one independently graded."""
        for phase in ("idle", "soft_reset"):
            self.assertEqual(self._state(phase)[0], "PASS")
            for item in ("configuration", "stream_binding"):
                post = {"configuration": "set", "stream_binding": "set", item: "default"}
                verdict, detail = self._state(phase, post=post)
                self.assertEqual(verdict, "FAIL", detail)
                self.assertEqual((detail["differs"], detail["reverted"]), ([item], [item]))
        verdict, detail = self._state(pre={"configuration": "default", "stream_binding": "set"})
        self.assertEqual(verdict, "NOT RUN", detail)
        self.assertEqual(detail["at_default"], ["configuration"])
        for changes in ({"post": {"configuration": "set"}}, {"pre": None}, {"defaults": {}}):
            self.assertEqual(self._state(**changes)[0], "NOT RUN")
        self.assertEqual(self._state("warm")[0], "NOT RUN")

    def test_release_state_commit_cut(self) -> None:
        """A commit cut restores all old or all new state, never a mix, and passes only placed."""
        new = {"configuration": "new", "stream_binding": "new"}
        cut = ReleaseCommitCut(new, (10.0, 10.5), 10.2)
        for post, expected in (({"configuration": "set", "stream_binding": "set"}, "PASS"),
                               (new, "PASS"),
                               ({"configuration": "new", "stream_binding": "set"}, "FAIL"),
                               ({"configuration": "default", "stream_binding": "default"}, "FAIL")):
            with self.subTest(post=post):
                self.assertEqual(self._state("journal_commit", post=post, committed=cut)[0], expected)
                # A bare pending snapshot carries no cut-phase evidence, so it never passes.
                self.assertEqual(self._state("journal_commit", post=post, committed=new)[0],
                                 "FAIL" if expected == "FAIL" else "NOT RUN")
        self.assertEqual(self._state("journal_commit")[0], "NOT RUN")
        same = {"configuration": "set", "stream_binding": "set"}
        self.assertEqual(self._state("journal_commit", committed=ReleaseCommitCut(same, (10.0, 10.5), 10.2))[0],
                         "NOT RUN")

    def test_release_commit_cut_evidence(self) -> None:
        """L3 #396 item 3: pending defaults, or a cut outside its commit, never pass."""
        items = list(RELEASE_PERSISTED_ITEMS)
        pre = {item: f"set-{item}" for item in items}
        defaults = {item: f"default-{item}" for item in items}
        new = {item: f"new-{item}" for item in items}
        # Persistence disabled while the pending values sit at their defaults: the
        # readback equals the pending snapshot, and still cannot pass.
        verdict, detail = check_release_state_restored(pre, defaults, defaults, items=items,
                                                       phase="journal_commit", committed=defaults)
        self.assertEqual((verdict, detail.get("pending_at_default")), ("NOT RUN", items), detail)

        def grade(post: dict, pending: dict, window: object = (10.0, 10.5), cut_s: object = 10.2) -> tuple:
            """One commit cut of the full inventory with the given evidence."""
            return check_release_state_restored(pre, post, defaults, items=items, phase="journal_commit",
                                                committed=ReleaseCommitCut(pending, window, cut_s))

        # Persistence disabled while every pending value sits at its default.
        verdict, detail = grade(defaults, defaults)
        self.assertEqual((verdict, detail["pending_at_default"]), ("NOT RUN", items), detail)
        for item in items:
            pending = dict(new, **{item: defaults[item]})
            for post in (defaults, pending, dict(pre, **{item: defaults[item]})):
                with self.subTest(item=item, post=post):
                    verdict, detail = grade(post, pending)
                    self.assertEqual((verdict, detail.get("pending_at_default")), ("NOT RUN", [item]), detail)
        self.assertEqual(grade(pre, new), ("PASS", dict(phase="journal_commit", items=items,
                                                        restored="old committed snapshot")))
        self.assertEqual(grade(new, new)[1]["restored"], "new committed snapshot")
        self.assertEqual(grade(dict(pre, configuration=new["configuration"]), new)[0], "FAIL")
        self.assertEqual(grade(new, new, (10.0, 10.5), 10.0)[0], "PASS")
        for window, cut_s in (((10.0, 10.5), 10.5), ((10.0, 10.5), 9.99), ((10.0, 10.5), 11.0)):
            verdict, detail = grade(new, new, window, cut_s)
            self.assertEqual((verdict, detail.get("why")), ("NOT RUN", "the cut hit no journal commit"))
        for window, cut_s in ((None, 10.2), ((10.5, 10.0), 10.2), ((10.0, float("nan")), 10.2),
                              ((10.0, 10.5), None), ((10.0,), 10.2)):
            verdict, detail = grade(new, new, window, cut_s)
            self.assertEqual(verdict, "NOT RUN")
            self.assertIn("cut-phase evidence required", detail["why"])
        # Idle cuts and soft resets restore the pre-cycle snapshot; a pending one is ignored.
        for phase in ("idle", "soft_reset"):
            for committed in (new, ReleaseCommitCut(new, (10.0, 10.5), 10.2)):
                with self.subTest(phase=phase, committed=type(committed).__name__):
                    verdict, detail = check_release_state_restored(pre, new, defaults, items=items,
                                                                   phase=phase, committed=committed)
                    self.assertEqual(verdict, "FAIL", detail)
                    self.assertEqual(check_release_state_restored(pre, pre, defaults, items=items, phase=phase,
                                                                  committed=committed)[0], "PASS")

    def test_release_controls_fail_as_planted(self) -> None:
        """L3 acceptance 4: every control fails its own assertion, and only by its defect."""
        controls = {s.sid: s for s in build_plan(["audio", "power"]) if s.op == RELEASE_CONTROL_OP}
        self.assertEqual(sorted(controls), ["audio.control.planted-drop",
                                            "power.control.first-boot-restart",
                                            "power.control.persistence-disabled"])
        expected = {"audio.control.planted-drop": "audio.zero-dut-glitches",
                    "power.control.first-boot-restart": "power.single-boot",
                    "power.control.persistence-disabled": "power.state-restored"}
        for sid, step in controls.items():
            with self.subTest(sid=sid):
                self.assertEqual(step.args["expected_failing_assertion"], expected[sid])
                self.assertIn(expected[sid], {spec.name for spec in step.asserts})
                self.assertEqual(step.args["expected_verdict"], "FAIL")
                verdict, detail = run_release_control(step)
                self.assertEqual(verdict, "FAIL", detail)
        boot = controls["power.control.first-boot-restart"].args["desk_fixture"]
        self.assertEqual(check_release_boot(1, 0, capture_complete=boot["capture_complete"])[0], "PASS")
        state = controls["power.control.persistence-disabled"].args["desk_fixture"]
        self.assertEqual(set(state["items"]), set(RELEASE_PERSISTED_ITEMS))
        self.assertEqual(check_release_state_restored(
            state["pre"], state["pre"], state["defaults"], items=state["items"], phase="idle")[0], "PASS")

    def test_release_audio_control_classifies_exactly(self) -> None:
        """L3 acceptance 4: the planted drop is found at its sample, with its size."""
        step = next(s for s in build_plan(["audio"]) if s.sid == "audio.control.planted-drop")
        fixture = step.args["fixture"]
        verdict, detail = run_release_control(step)
        self.assertEqual(verdict, "FAIL", detail["why"])
        dut = [e for e in detail["events"] if e["attribution"] == "dut"]
        want = fixture["expected_events"]
        self.assertEqual(sorted((e["channel"], e["capture_index"], e["class"], e["n"]) for e in dut),
                         [(c, want["capture_index"], want["class"], want["n"]) for c in want["channels"]])
        self.assertEqual(detail["planted_missed"], [])
        self.assertEqual(detail["counts"]["planted"], {"dropped": 16, "repeated": 16, "bit-flip": 2})
        clean = synthesize_counter_capture(fixture["frames"], fixture["channels"],
                                           events=fixture["source_events"])
        verdict, detail = grade_audio_counter_capture(
            clean, CounterCapture(fixture["channels"], "big", fixture["rate_hz"], 0.0, 0.0),
            CounterRunLog(fixture["planted_arms"], [], 2), required_s=fixture["required_s"])
        self.assertEqual(verdict, "PASS", detail["why"])
        self.assertEqual((detail["qualified"]["start"], detail["qualified"]["end"]),
                         (63, fixture["frames"] - 63))

    @staticmethod
    def _word(tag: int, n: int) -> int:
        """The documented layout restated apart from the planner: tag in sample bits
        15:12, n mod 2048 in bits 11:1, bit n mod 32 of the block code in bit 0."""
        code = ((n // 2048) * 0x9E3779B1) % 2**32
        return ((tag << 12) | ((n % 2048) << 1) | ((code >> (n % 32)) & 1)) << 8

    def test_audio_counter_word_layout(self) -> None:
        """Independent byte vectors, the period against the run, and position decoding."""
        self.assertEqual(synthesize_counter_capture(1, 1, start_counter=5), bytes.fromhex("00100a00"))
        self.assertEqual(synthesize_counter_capture(1, 2, byteorder="little", start_counter=4101),
                         bytes.fromhex("000b1000000b2000"))
        self.assertEqual(audio_counter_word(1, 2048), 0x00100100)
        self.assertEqual(max(audio_counter_word(8, n) for n in range(4096)), 0x008FFF00)
        import math
        import random
        peak_dbfs = 20 * math.log10(0x008FFF00 / 2**31)
        self.assertTrue(-48 < peak_dbfs < -46, peak_dbfs)
        self.assertEqual(48000 / AUDIO_BLOCK_FRAMES, 23.4375)
        self.assertEqual(AUDIO_PERIOD_FRAMES, 2**43)
        day = 24 * 60 * 60
        for rate in (48000, 96000, 192000):
            self.assertGreater(AUDIO_PERIOD_FRAMES, 500 * day * rate, rate)
        # The planted flip touches the code bit alone, so it never equals a neighbour.
        self.assertEqual(AUDIO_PLANTED_ARMS[2]["mask"], 1 << AUDIO_PAD_BITS)
        for n in range(1, 5000):
            flipped = self._word(2, n) ^ AUDIO_PLANTED_ARMS[2]["mask"]
            self.assertNotIn(flipped, (self._word(2, n - 1), self._word(2, n + 1)))
        picks = random.Random(396)
        for n in [0, 5, 2047, 2048, 4096 + 13, day * 192000 - 70, AUDIO_PERIOD_FRAMES - 30] + [
                picks.randrange(AUDIO_PERIOD_FRAMES) for _ in range(40)]:
            with self.subTest(position=n):
                self.assertEqual(audio_counter_word(3, n), self._word(3, n))
                words = [self._word(3, (n + k) % AUDIO_PERIOD_FRAMES) for k in range(AUDIO_CONFIRM_FRAMES)]
                self.assertEqual(_audio_decode(words), n)
                self.assertIsNone(_audio_decode(words[:1] + [words[1] ^ 0x100] + words[2:]))

    @staticmethod
    def _independent_arms(frames: int) -> list:
        """The drop, repeat and flip arms in the first and the last tenth, as logged."""
        return [{"class": "dropped", "index": 100, "n": 3}, {"class": "repeated", "index": 300, "n": 2},
                {"class": "bit-flip", "index": 500, "mask": 0x100, "channel": 1},
                {"class": "dropped", "index": frames - 700, "n": 3},
                {"class": "repeated", "index": frames - 450, "n": 2},
                {"class": "bit-flip", "index": frames - 200, "mask": 0x100, "channel": 3}]

    def _independent(self, ops: Sequence[tuple], frames: int = 8192, arms: bool = True,
                     **layout: object) -> tuple[str, dict, list]:
        """Grade `_independent_bytes`; `order` and `chunk` restate it, `required_s`
        defaults to the clean qualified length and None leaves the release default."""
        order, chunk = layout.pop("order", "big"), layout.pop("chunk", None)
        capture = self._independent_bytes(ops, frames, arms, order)
        if chunk:
            capture = [capture[i:i + chunk] for i in range(0, len(capture), chunk)]
        losses = layout.pop("losses", [])
        required_s = layout.pop("required_s", (frames - 2 * 63) / 48000)
        extra = {} if required_s is None else {"required_s": required_s}
        verdict, detail = grade_audio_counter_capture(
            capture, CounterCapture(4, order, 48000, 0.0, 0.0, **layout),
            CounterRunLog(self._independent_arms(frames) if arms else [], losses, 0), **extra)
        dut = [(e["channel"], e["capture_index"], e["class"], e.get("n"), e.get("mask"), e.get("partner"))
               for e in detail.get("events", []) if e["attribution"] == "dut"]
        return verdict, detail, sorted(dut)

    def _independent_bytes(self, ops: Sequence[tuple], frames: int = 8192, arms: bool = True,
                           order: str = "big") -> bytes:
        """A four-channel capture built from `_word`, never the planner's synthesizer.

        ops: ("shift", index, k[, channel]) moves the source position from index on;
        ("zero", index, n); ("xor", index, channel, mask); ("swap", index, n, a, b);
        ("copy", index, n, source, destination). Drop, repeat and flip arms run in
        the first and the last tenth unless `arms` is false.
        """
        import struct
        planted = [("shift", 100, 3), ("shift", 300, -2), ("xor", 500, 1, 0x100),
                   ("shift", frames - 700, 3), ("shift", frames - 450, -2), ("xor", frames - 200, 3, 0x100)]
        ops = (planted if arms else []) + list(ops)
        deltas = [{} for _ in range(4)]
        for op in ops:
            if op[0] == "shift":
                for c in (range(4) if len(op) < 4 else (op[3],)):
                    deltas[c][op[1]] = deltas[c].get(op[1], 0) + op[2]
        columns = []
        for c in range(4):
            marks, shift, column = sorted({0, frames} | {i for i in deltas[c] if 0 < i < frames}), 0, []
            for start, end in zip(marks, marks[1:]):
                shift += deltas[c].get(start, 0)
                column += [self._word(c + 1, i + shift) for i in range(start, end)]
            columns.append(column)
        out = [list(frame) for frame in zip(*columns)]
        for op in ops:
            if op[0] == "zero":
                for i in range(op[1], op[1] + op[2]):
                    out[i] = [0] * 4
            elif op[0] == "xor":
                out[op[1]][op[2]] ^= op[3]
            elif op[0] in ("swap", "copy"):
                for i in range(op[1], min(frames, op[1] + op[2])):
                    if op[0] == "swap":
                        out[i][op[3]], out[i][op[4]] = out[i][op[4]], out[i][op[3]]
                    else:
                        out[i][op[4]] = out[i][op[3]]
        return struct.pack(f"{'>' if order == 'big' else '<'}{4 * frames}I", *(w for frame in out for w in frame))

    def test_audio_compound_and_edge_events(self) -> None:
        """Holds, slip pairs, bursts and capture edges, each in the design's classes."""
        at = 3000
        every = range(4)
        cases = (
            ([("shift", at, -1), ("shift", at + 1, 1)],
             [(c, at, "repeated", 1) for c in every] + [(c, at + 1, "dropped", 1) for c in every]),
            ([("shift", at, 1), ("shift", at + 1, -1)],
             [(c, at, "dropped", 1) for c in every] + [(c, at + 1, "repeated", 1) for c in every]),
            ([("shift", at, -1), ("shift", at + 5, 1)],
             [(c, at, "repeated", 1) for c in every] + [(c, at + 5, "dropped", 1) for c in every]),
            ([("shift", at, 3), ("shift", at + 5, 2)],
             [(c, at, "dropped", 3) for c in every] + [(c, at + 5, "dropped", 2) for c in every]),
            ([("zero", 0, 5)], [(c, 0, "silence", 5) for c in every]),
            ([("shift", 8191, 4)], [(c, 8191, "dropped", 4) for c in every]))
        for ops, want in cases:
            with self.subTest(ops=ops):
                verdict, detail, dut = self._independent(ops)
                self.assertEqual(verdict, "FAIL", detail["why"])
                self.assertEqual([event[:4] for event in dut], sorted(want))
        _, detail, _ = self._independent([("zero", 0, 5)])
        self.assertEqual({e["inserted"] for e in detail["events"] if e["class"] == "silence"}, {None})
        _, detail, _ = self._independent([("shift", 8191, 4)])
        self.assertEqual({e.get("unresolved") for e in detail["events"] if e["capture_index"] == 8191},
                         {"the capture ended"})
        # A slip pair whose two displaced words share one XOR mask with the track is
        # bit-identical to a two-word corruption, and reads as that corruption.
        pair = next(i for i in range(3000, 4000)
                    if self._word(1, i + 5) ^ self._word(1, i + 1) == self._word(1, i + 6) ^ self._word(1, i + 2))
        mask = f"0x{self._word(1, pair + 5) ^ self._word(1, pair + 1):08X}"
        self.assertEqual(self._independent([("shift", pair, 4), ("shift", pair + 2, -4)])[2],
                         [(c, pair, "bit-flip", 2, mask, None) for c in every])
        for mask, n in ((0x1, 3), (0x80000000, 2), (0x100, 2), (0x100, 3), (0x200, 2), (0x400, 2)):
            with self.subTest(mask=mask, n=n):
                verdict, detail, dut = self._independent([("xor", at + k, 2, mask) for k in range(n)])
                self.assertEqual((verdict, dut), ("FAIL", [(2, at, "bit-flip", n, f"0x{mask:08X}", None)]))

    def test_audio_tag_integrity_decides_first(self) -> None:
        """A channel-number flip or a copy is corruption; only a reciprocal exchange is a swap."""
        at, want = 3000, []
        # One flip of every container bit, each 120 samples apart so each closes alone.
        for bit in range(32):
            index = 1000 + 120 * bit
            word = self._word(3, index + 3 - 2) ^ (1 << bit)
            if word == self._word(3, index + 3 - 2 - 1):
                want += [(2, index, "repeated", 1, None, None), (2, index + 1, "dropped", 1, None, None)]
            elif word == self._word(3, index + 3 - 2 + 1):
                want += [(2, index, "dropped", 1, None, None), (2, index + 1, "repeated", 1, None, None)]
            else:
                want.append((2, index, "bit-flip", 1, f"0x{1 << bit:08X}", None))
        self.assertEqual(self._independent([("xor", 1000 + 120 * bit, 2, 1 << bit) for bit in range(32)])[2],
                         sorted(want))
        self.assertIn((2, 1000 + 120 * 21, "bit-flip", 1, "0x00200000", None), want)
        verdict, detail, dut = self._independent([("xor", at, 2, 0x00100000)])
        self.assertEqual(dut, [(2, at, "bit-flip", 1, "0x00100000", None)])
        self.assertEqual([e.get("matches_channel") for e in detail["events"] if e["attribution"] == "dut"], [1])
        verdict, detail, dut = self._independent([("copy", at, 3, 2, 0)])
        self.assertEqual(dut, [(0, at, "bit-flip", 3, "0x00200000", None)])
        self.assertEqual([e.get("matches_channel") for e in detail["events"] if e["attribution"] == "dut"], [2])
        self.assertEqual(self._independent([("swap", at, 3, 0, 2)])[2],
                         [(0, at, "swap", 3, None, 2), (2, at, "swap", 3, None, 0)])
        # A swap whose partner changes is two swaps, never one run.
        self.assertEqual(self._independent([("swap", at, 3, 0, 2), ("swap", at + 3, 3, 0, 3)])[2],
                         [(0, at, "swap", 3, None, 2), (0, at + 3, "swap", 3, None, 3),
                          (2, at, "swap", 3, None, 0), (3, at + 3, "swap", 3, None, 0)])
        self.assertEqual(self._independent([("swap", 8142, 50, 1, 3)])[2],
                         [(1, 8142, "swap", 50, None, 3), (3, 8142, "swap", 50, None, 1)])

    def test_audio_static_swap_fails_with_every_arm_found(self) -> None:
        """A channel map wrong from the first frame is a swap, and its counters stay tracked."""
        for a, b in ((0, 2), (1, 3)):
            with self.subTest(pair=(a, b)):
                verdict, detail, dut = self._independent([("swap", 0, 8192, a, b)])
                self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
                self.assertEqual(dut, [(a, 0, "swap", 8192, None, b), (b, 0, "swap", 8192, None, a)])
                self.assertEqual(detail["counts"]["planted"], {"dropped": 8, "repeated": 8, "bit-flip": 2})
        verdict, detail, dut = self._independent([("swap", 0, 8192, 0, 2), ("shift", 4000, 7)])
        self.assertEqual(dut, sorted([(0, 0, "swap", 8192, None, 2), (2, 0, "swap", 8192, None, 0)]
                                     + [(c, 4000, "dropped", 7, None, None) for c in range(4)]))

    def test_audio_block_slips_are_sized_exactly(self) -> None:
        """L3 #396: a slip of whole 2048-sample blocks fails, sized and bounded, both ways."""
        at = 2 * 4096 + 13
        for kind, n in (("drop", 2048), ("drop", 4096), ("drop", 8192), ("drop", 409600),
                        ("repeat", 2048), ("repeat", 4096), ("drop", 3000), ("repeat", 3000)):
            for options in ({}, {"byteorder": "little"}, {"chunk": True}, {"start": 24 * 3600 * 192000 - 9000}):
                with self.subTest(kind=kind, n=n, options=options):
                    verdict, detail, dut = self._grade([{"kind": kind, "index": at, "n": n}], **options)
                    self.assertEqual((verdict, len(dut)), ("FAIL", 4), detail["why"])
                    for record in dut:
                        self.assertEqual((record["class"], record["n"]),
                                         ("dropped" if kind == "drop" else "repeated", n))
                        first, last = record.get("located_within", (record["capture_index"],) * 2)
                        self.assertEqual(last, record["capture_index"])
                        self.assertTrue(first <= at <= last < first + AUDIO_CONFIRM_FRAMES, record)
                        if n % AUDIO_BLOCK_FRAMES:
                            self.assertEqual((first, last), (at, at), record)
        # The whole release: clean AVTP counters cannot rescue a 4096-sample content slip.
        self.assertEqual(self._counters(self._reads())[0], "PASS")
        self.assertEqual(self._grade([{"kind": "drop", "index": at, "n": 4096}])[0], "FAIL")
        verdict, detail, dut = self._independent([("shift", 3000, 4096)])
        self.assertEqual([(e[2], e[3]) for e in dut], [("dropped", 4096)] * 4)

    def test_audio_capture_losses_advance_the_clocks(self) -> None:
        """L3 #396: a logged loss is time that ran; events take anchored times or none."""
        frames, lost = 20000, 409600
        arms = [{"class": "dropped", "index": 100, "n": 3}, {"class": "repeated", "index": 300, "n": 2},
                {"class": "bit-flip", "index": 500, "mask": 0x100, "channel": 1},
                {"class": "dropped", "index": 19000, "n": 3}, {"class": "repeated", "index": 19300, "n": 2},
                {"class": "bit-flip", "index": 19600, "mask": 0x100, "channel": 3}]
        source = [{"kind": "drop" if a["class"] == "dropped" else "repeat" if a["class"] == "repeated"
                   else "flip", **{k: v for k, v in a.items() if k != "class"}} for a in arms]

        def grade(losses: list, **layout: object) -> dict:
            """Twenty thousand frames: the losses, a corrupted sample at 8000 and the arms."""
            extra = [{"kind": "drop", "index": loss["index"], "n": loss["frames"]} for loss in losses]
            capture = synthesize_counter_capture(frames, 4, events=source + extra + [
                {"kind": "flip", "index": 8000, "channel": 0, "mask": 1}])
            verdict, detail = grade_audio_counter_capture(
                capture, CounterCapture(4, "big", 48000, 100.0, 200.0, **layout), CounterRunLog(arms, losses, 0))
            self.assertEqual(verdict, "FAIL", detail["why"])
            return detail

        # With the start times alone, an event 8.6 s of acquisition later has no supported time.
        detail = grade([{"index": 7000, "frames": lost}])
        event = next(e for e in detail["events"] if e["attribution"] == "dut")
        self.assertEqual((event["wall_s"], event["gptp_s"]), (None, None), event)
        self.assertEqual(detail["duration_s"], (frames + lost) / 48000)
        span = (frames + lost) / 48000
        end = ((frames, 100.0 + span, 200.0 + span),)
        detail = grade([{"index": 7000, "frames": lost}], anchors=end, gptp_steps_wall_s=())
        event = next(e for e in detail["events"] if e["attribution"] == "dut")
        self.assertEqual((event["capture_index"], event["acquisition_index"]), (8000, 8000 + lost))
        self.assertAlmostEqual(event["wall_s"], 108.7)
        self.assertAlmostEqual(event["gptp_s"], 208.7)
        self.assertEqual(event["context_wall_s"], [event["wall_s"] - 5, event["wall_s"] + 5])
        self.assertEqual((detail["acquired_frames"], detail["duration_s"]), (frames + lost, span))
        self.assertEqual(detail["counts"]["capture"], {"dropped": 4})
        detail = grade([{"index": 7000, "frames": lost}, {"index": 7500, "frames": 48000}],
                       anchors=((frames, 100.0 + span + 1, 200.0 + span + 1),), gptp_steps_wall_s=())
        event = next(e for e in detail["events"] if e["attribution"] == "dut")
        self.assertEqual(event["acquisition_index"], 8000 + lost + 48000)
        self.assertAlmostEqual(event["wall_s"], 100.0 + (8000 + lost + 48000) / 48000)
        # A loss logged at an event's own index ran before that event: "at or before".
        short = (frames + 3000) / 48000
        detail = grade([{"index": 7000, "frames": 3000}], anchors=((frames, 100.0 + short, 200.0 + short),),
                       gptp_steps_wall_s=())
        at_loss = [e for e in detail["events"] if e["attribution"] == "capture"]
        self.assertEqual(sorted((e["channel"], e["capture_index"], e["n"]) for e in at_loss),
                         [(c, 7000, 3000) for c in range(4)])
        for event in at_loss:
            self.assertEqual(event["acquisition_index"], 10000, event)
            self.assertAlmostEqual(event["wall_s"], 100.0 + 10000 / 48000)
            self.assertAlmostEqual(event["gptp_s"], 200.0 + 10000 / 48000)
        for layout, why in (({}, "unsupported: no anchor after the event"),
                            ({"anchors": end}, "unsupported gPTP: no discontinuity record"),
                            ({"anchors": end, "gptp_steps_wall_s": (105.0,)},
                             "unsupported gPTP: a recorded discontinuity lies between the anchors")):
            with self.subTest(layout=layout):
                detail = grade([{"index": 7000, "frames": lost}], **layout)
                event = next(e for e in detail["events"] if e["attribution"] == "dut")
                self.assertEqual((event["gptp_s"], event["timing"]), (None, why))
                self.assertEqual(event["wall_s"] is None, "anchors" not in layout)
                self.assertGreater(detail["timing_unsupported"], 0)
        detail = grade([], anchors=((8000, 123.0, 456.0), (frames, 200.0, 500.0)))
        event = next(e for e in detail["events"] if e["attribution"] == "dut")
        self.assertEqual((event["wall_s"], event["gptp_s"], event["timing"]), (123.0, 456.0, "anchored"))
        # Graded against the clean capture's own qualified length, so only the anchors decide.
        layout_refusal = "capture layout, both logs, tolerance, start times and anchors required"
        for anchors, expected in ((((900, 101.0, 0.0), (frames, 102.0, 0.0)), "PASS"),
                                  (((0, 101.0, 0.0),), layout_refusal),
                                  (((900, 101.0, 0.0), (800, 102.0, 0.0)), layout_refusal),
                                  (((900, 99.0, 0.0),), layout_refusal), (((900, 100.0, 0.0),), layout_refusal),
                                  (((frames + 1, 999.0, 0.0),), "fewer than 64 frames, or an anchor past the capture"),
                                  (((900, 101.0),), layout_refusal)):
            with self.subTest(anchors=anchors):
                verdict, detail = grade_audio_counter_capture(
                    synthesize_counter_capture(frames, 4, events=source),
                    CounterCapture(4, "big", 48000, 100.0, 200.0, anchors=anchors), CounterRunLog(arms, [], 0),
                    required_s=(frames - 2 * 63) / 48000)
                self.assertEqual(verdict if expected == "PASS" else (verdict, detail["why"]),
                                 expected if expected == "PASS" else ("NOT RUN", expected))

    def test_audio_capture_loss_needs_every_channel(self) -> None:
        """A logged loss is a slip on every counter channel; on one channel it is not the capture's."""
        loss = [{"index": 3000, "frames": 9}]
        self.assertEqual(self._independent([("shift", 3000, 9)], losses=loss)[0], "PASS")
        verdict, detail, _ = self._independent([("shift", 3000, 9, 0)], losses=loss)
        self.assertEqual((verdict, detail.get("why")), ("NOT RUN", "a logged capture loss is not in the capture"))
        self.assertEqual(self._independent([("shift", 3000, 9, 0)])[2], [(0, 3000, "dropped", 9, None, None)])

    def test_audio_arms_run_at_both_edges(self) -> None:
        """'At the start and at the end' is the first and the last tenth of the capture."""
        frames = 4 * 4096
        edge = frames // 10
        logged = [{"class": "dropped", "index": 100, "n": 3}, {"class": "repeated", "index": 300, "n": 2},
                  {"class": "bit-flip", "index": 500, "mask": 0x100, "channel": 1},
                  {"class": "dropped", "index": frames - 900, "n": 3},
                  {"class": "repeated", "index": frames - 600, "n": 2},
                  {"class": "bit-flip", "index": frames - 300, "mask": 0x100, "channel": 3}]
        for index, expected in ((edge - 1, "PASS"), (edge, "NOT RUN")):
            source = [{"kind": "drop", "index": index, "n": 3}, {"kind": "repeat", "index": 300, "n": 2},
                      {"kind": "flip", "index": 500, "channel": 1, "mask": 0x100},
                      {"kind": "drop", "index": frames - 900, "n": 3},
                      {"kind": "repeat", "index": frames - 600, "n": 2},
                      {"kind": "flip", "index": frames - 300, "channel": 3, "mask": 0x100}]
            arms = [dict(logged[0], index=index)] + logged[1:]
            with self.subTest(index=index):
                verdict, detail = grade_audio_counter_capture(
                    synthesize_counter_capture(frames, 4, events=source),
                    CounterCapture(4, "big", 48000, 0.0, 0.0), CounterRunLog(arms, [], 0),
                    required_s=(frames - 2 * 63) / 48000)
                self.assertEqual(verdict, expected, detail["why"])
        mid = frames // 2
        source = [{"kind": "drop", "index": mid - 300, "n": 3}, {"kind": "repeat", "index": mid - 200, "n": 2},
                  {"kind": "flip", "index": mid - 100, "channel": 1, "mask": 0x100},
                  {"kind": "drop", "index": mid + 100, "n": 3}, {"kind": "repeat", "index": mid + 200, "n": 2},
                  {"kind": "flip", "index": mid + 300, "channel": 1, "mask": 0x100}]
        arms = [{"class": {"drop": "dropped", "repeat": "repeated", "flip": "bit-flip"}[e["kind"]],
                 **{k: v for k, v in e.items() if k != "kind"}} for e in source]
        verdict, detail = grade_audio_counter_capture(
            synthesize_counter_capture(frames, 4, events=source), CounterCapture(4, "big", 48000, 0.0, 0.0),
            CounterRunLog(arms, [], 0), required_s=(frames - 2 * 63) / 48000)
        self.assertEqual((verdict, detail["planted_missed"]), ("NOT RUN", []))
        self.assertIn("first and the last tenth", detail["why"])
        self.assertEqual(AUDIO_ARM_EDGE_DIVISOR, 10)

    def test_audio_offset_channel_and_mixed_capture(self) -> None:
        """One channel's slip and a channel without the counter are graded channel by channel."""
        verdict, detail, dut = self._independent([("shift", 3000, 7, 3)], tags=(1, 2, None, 4))
        self.assertEqual((verdict, dut), ("FAIL", [(3, 3000, "dropped", 7, None, None)]))
        verdict, detail, dut = self._independent([("xor", 5000, 2, 0x10)], tags=(1, 2, None, 4))
        self.assertEqual((verdict, dut), ("PASS", []), detail["why"])

    def test_audio_qualified_interval_is_stated_and_required(self) -> None:
        """L3 #396 REQ-VER-06: a verdict proves only its stated interval; PASS needs 24 h of it."""
        frames, rate = 8192, 48000
        whole = (frames - 2 * 63) / rate
        verdict, detail, dut = self._independent([], required_s=None)
        self.assertEqual((verdict, dut, detail["why"]),
                         ("NOT RUN", [], "the qualified interval is shorter than the required duration"))
        qualified = detail["qualified"]
        self.assertEqual({k: qualified[k] for k in ("start", "end", "frames", "seconds", "required_s",
                                                     "guard_frames", "acquisition", "unobserved_frames")},
                         {"start": 63, "end": frames - 63, "frames": frames - 126, "seconds": whole,
                          "required_s": 24 * 3600, "guard_frames": 63, "acquisition": [63, frames - 63],
                          "unobserved_frames": 0})
        self.assertEqual(self._independent([], required_s=whole)[0], "PASS")
        self.assertEqual(self._independent([], required_s=whole + 1 / rate)[0], "NOT RUN")
        for bad in (0, -1.0, float("nan"), "86400", True):
            with self.subTest(required_s=bad):
                self.assertEqual(self._independent([], required_s=bad)[0], "NOT RUN")
        # A logged loss is time that ran, but nothing in it was observed.
        loss = [{"index": 3000, "frames": 3000}]
        verdict, detail, _ = self._independent([("shift", 3000, 3000)], losses=loss)
        self.assertEqual(verdict, "PASS", detail["why"])
        self.assertEqual((detail["qualified"]["frames"], detail["qualified"]["unobserved_frames"],
                          detail["qualified"]["acquisition"]), (frames - 126, 3000, [63, frames - 63 + 3000]))
        self.assertEqual(self._independent([("shift", 3000, 3000)], losses=loss,
                                           required_s=whole + 3000 / rate)[0], "NOT RUN")
        # A late acquisition moves the interval's start; nothing before it is proved.
        verdict, detail, _ = self._independent([("shift", 10, 4096)])
        self.assertEqual((verdict, detail["qualified"]["start"], detail["qualified"]["end"]),
                         ("FAIL", 10 + 63, frames - 63))
        # Arms and losses outside the interval cannot be confirmed, so they are refused by name.
        arms = self._independent_arms(frames)
        source = [{"kind": {"dropped": "drop", "repeated": "repeat", "bit-flip": "flip"}[a["class"]],
                   **{k: v for k, v in a.items() if k != "class"}} for a in arms]
        for change, extra, losses, why in (
                ({0: 40}, [], [], "void: a planted arm lies outside the qualified interval"),
                ({5: frames - 10}, [], [], "void: a planted arm lies outside the qualified interval"),
                ({}, [{"kind": "drop", "index": 40, "n": 9}], [{"index": 40, "frames": 9}],
                 "a logged capture loss lies outside the qualified interval"),
                ({}, [{"kind": "drop", "index": frames - 30, "n": 4096}], [{"index": frames - 30, "frames": 4096}],
                 "a logged capture loss lies outside the qualified interval")):
            moved = [dict(arm, index=change.get(k, arm["index"])) for k, arm in enumerate(arms)]
            events = [dict(event, index=change.get(k, event["index"])) for k, event in enumerate(source)]
            with self.subTest(change=change, losses=losses):
                verdict, detail = grade_audio_counter_capture(
                    synthesize_counter_capture(frames, 4, events=events + extra),
                    CounterCapture(4, "big", rate, 0.0, 0.0), CounterRunLog(moved, losses, 0), required_s=whole)
                self.assertEqual((verdict, detail["why"]), ("NOT RUN", why))
        # A channel that never acquires the counter voids the run, early when the capture is long.
        capture = bytearray(self._independent_bytes([], frames))
        for frame in range(frames):
            capture[16 * frame + 8:16 * frame + 12] = bytes(4)
        verdict, detail = grade_audio_counter_capture(bytes(capture), CounterCapture(4, "big", rate, 0.0, 0.0),
                                                      CounterRunLog(arms, [], 0), required_s=whole)
        self.assertEqual((verdict, detail["unacquired"], detail["qualified"]), ("NOT RUN", [2], None))
        self.assertTrue(detail["why"].startswith("void: a counter channel never acquired"), detail["why"])
        long = synthesize_counter_capture(4 * AUDIO_WINDOW_WORDS, 2, byteorder="little")
        verdict, detail = grade_audio_counter_capture([long[i:i + 4096] for i in range(0, len(long), 4096)],
                                                      CounterCapture(2, "big", rate, 0.0, 0.0),
                                                      CounterRunLog([], [], 0))
        self.assertEqual((verdict, detail["unacquired"]), ("NOT RUN", [0, 1]))
        self.assertLessEqual(detail["frames"], AUDIO_WINDOW_WORDS + 512)
        self.assertIn("did not acquire the counter in its first 65536 frames", detail["why"])

    def test_audio_boundary_block_slips_are_unresolved(self) -> None:
        """L3 #396: a slip of whole blocks near either end is unresolved, never an exact class."""
        import hashlib
        frames, rate = 8192, 48000
        whole = (frames - 2 * 63) / rate
        # Byte-identical endpoint pairs: the slipped captures are the clean one.
        clean = "f395a643b6d210b302c6e8cd7a8e4b849fd420f307f44e6bb4c59951b7493c6f"
        for at, n in ((frames - 1, 2048), (frames - 2, 8192)):
            with self.subTest(pair=(at, n)):
                self.assertEqual(hashlib.sha256(self._independent_bytes([("shift", at, n)])).hexdigest(), clean)
                for options in ({}, {"chunk": 113}):
                    verdict, detail, dut = self._independent([("shift", at, n)], **options)
                    self.assertEqual((verdict, dut), ("PASS", []), detail["why"])
                    self.assertLess(detail["qualified"]["end"], at)
                    self.assertEqual(self._independent([("shift", at, n)], required_s=frames / rate, **options)[0],
                                     "NOT RUN")
        self.assertEqual(hashlib.sha256(self._independent_bytes([])).hexdigest(), clean)
        # Without guard samples a whole-block slip is one unresolved event that bounds the slip.
        cases = [(frames - back, n) for back in (1, 20, 40, 62, 63, 65) for n in (2048, 4096, -4096, 8192)]
        for at, n in cases:
            for options in ({}, {"order": "little"}, {"chunk": 113}) if n == 4096 else ({},):
                with self.subTest(at=at, n=n, options=options):
                    verdict, detail, dut = self._independent([("shift", at, n)], **options)
                    events = [e for e in detail["events"] if e["attribution"] == "dut"]
                    if not events:
                        self.assertEqual(verdict, "PASS")
                        self.assertLess(detail["qualified"]["end"], at + 1)
                        continue
                    self.assertEqual((verdict, len(events)), ("FAIL", 4), detail["why"])
                    for event in events:
                        self.assertIn(event["class"], ("unresolved", "dropped" if n > 0 else "repeated"))
                        first, last = event.get("located_within", (event["capture_index"],) * 2)
                        self.assertTrue(first <= at <= last < first + 63, event)
                        if event["class"] == "unresolved":
                            self.assertEqual((event["mask"], event["capture_index"] + event["n"]),
                                             ("0x00000100", frames))
                            self.assertEqual(event["unresolved"], "the capture ended: a slip of whole "
                                                                  "blocks or a code-bit corruption")
                        else:
                            self.assertEqual(event["n"], abs(n))
        self.assertIn("unresolved", {e[2] for e in self._independent([("shift", frames - 30, 4096)])[2]})
        # With 64 captured samples after its first differing word the same slip is sized exactly. The
        # qualified interval decides what is proved clean, not the class: nearer the end it is unresolved.
        for at in (frames - 300, 1000):
            for n in (2048, -4096):
                verdict, detail, dut = self._independent([("shift", at, n)])
                self.assertEqual({(e[2], e[3]) for e in dut}, {("dropped" if n > 0 else "repeated", abs(n))})
        # Before acquisition the same ambiguity is unresolved, and the interval starts later.
        # Where the code bits of the first samples happen to fit the old block, the channel
        # acquires the old track and the slip is sized exactly after it.
        starts = {}
        for at in (10, 30, 62):
            for options in ({}, {"order": "little"}, {"chunk": 113}):
                with self.subTest(at=at, options=options):
                    verdict, detail, _ = self._independent([("shift", at, 4096)], arms=False, **options)
                    events = [e for e in detail["events"] if e["attribution"] == "dut"]
                    self.assertEqual(len(events), 4, events)
                    for event in events:
                        self.assertIn(event["class"], ("unresolved", "dropped"), event)
                        first, last = event["located_within"]
                        self.assertTrue(first <= at <= last, event)
                        if event["class"] == "unresolved":
                            self.assertLess(event["capture_index"], first)
                            self.assertTrue(event["unresolved"].startswith("before acquisition"))
                        else:
                            self.assertEqual((event["class"], event["n"]), ("dropped", 4096))
                    start = at if events[0]["class"] == "unresolved" else 0
                    self.assertEqual(detail["qualified"]["start"], start + 63)
                    starts[at] = events[0]["class"]
        self.assertEqual(starts, {10: "unresolved", 30: "unresolved", 62: "dropped"})
        # A tail repeat of half a block is the slip it is, unresolved, never an open stretch.
        verdict, detail, dut = self._independent([("shift", frames - 30, -1024)])
        self.assertEqual({(e[2], e[3]) for e in dut}, {("repeated", 1024)})
        self.assertEqual({e.get("unresolved") for e in detail["events"] if e["attribution"] == "dut"},
                         {"the capture ended"})
        # A burst that returns into the open stretch is still its own corruption.
        self.assertEqual(self._independent([("xor", frames - 20, 2, 0x80000), ("xor", frames - 19, 2, 0x80000),
                                            ("xor", frames - 18, 2, 0x100)])[2],
                         [(2, frames - 20, "bit-flip", 2, "0x00080000", None),
                          (2, frames - 18, "unresolved", 18, "0x00000100", None)])

    def test_audio_constant_mask_at_every_length(self) -> None:
        """L3 #396: one XOR mask over an excursion is one corruption at every length."""
        for mask in (0x100, 0x80000, 0x40000, 0x200):
            for at, n in ((3000, 2), (3000, 63), (3000, 64), (3000, 65), (3000, 100), (4090, 100),
                          (3000, 2000), (2040, 70)):
                for options in ({}, {"chunk": 113}) if n == 100 else ({},):
                    with self.subTest(mask=mask, at=at, n=n, options=options):
                        verdict, detail, dut = self._independent(
                            [("xor", at + k, 2, mask) for k in range(n)], **options)
                        self.assertEqual((verdict, dut), ("FAIL", [(2, at, "bit-flip", n, f"0x{mask:08X}", None)]))
        # A slip whose track equals the old one under one mask for a while is still that slip,
        # released where the masks part: inside a block for half a block, at the block's end
        # for the slip whose blocks invert the code.
        block, code = 5596 // 2048, (5596 // 2048 * 0x9E3779B1) % 2**32
        inverting = (((code ^ 0xFFFFFFFF) - code) * pow(0x9E3779B1, -1, 2**32) % 2**32) * 2048
        signed = (inverting + 2**42) % 2**43 - 2**42
        self.assertEqual((self._word(1, 5596 + inverting) ^ self._word(1, 5596), block), (0x100, 2))
        for at, n, arms, frames in ((3000, 512, True, 8192), (2900, 1024, True, 8192), (3000, -512, True, 8192),
                                    (3100, 512, False, 4000), (5596, inverting, False, 8192)):
            with self.subTest(at=at, n=n):
                verdict, detail, dut = self._independent([("shift", at, n)], frames=frames, arms=arms)
                size = signed if n == inverting else n
                self.assertEqual({(e[1], e[2], e[3]) for e in dut},
                                 {(at, "dropped" if size > 0 else "repeated", abs(size))})
                self.assertEqual(len(dut), 4)
                self.assertNotIn("unresolved", {k for e in detail["events"] for k in e})
        # A repeat and a drop of half a block inside one block read as one corruption: bit-identical.
        verdict, detail, dut = self._independent([("shift", 3400, -1024), ("shift", 3500, 1024)])
        self.assertEqual(dut, [(c, 3400, "bit-flip", 100, "0x00080000", None) for c in range(4)])
        self.assertEqual(self._word(1, 3401 - 1024) ^ self._word(1, 3401), 0x00080000)
        # A constant-mask excursion the capture ends inside is never an exact corruption.
        verdict, detail, dut = self._independent([("xor", k, 2, 0x100) for k in range(8192 - 300, 8192)])
        events = [e for e in detail["events"] if e["attribution"] == "dut"]
        self.assertEqual({e["channel"] for e in events}, {2})
        self.assertNotIn(None, {e.get("unresolved") for e in events})
        self.assertIn("the capture ended inside a constant-mask excursion", {e.get("unresolved") for e in events})
        self.assertNotIn("bit-flip", {e["class"] for e in events})
        verdict, detail, dut = self._independent([("xor", k, 2, 0x100) for k in range(7700, 8000)], frames=8000)
        self.assertEqual({(e["channel"], e.get("unresolved")) for e in detail["events"] if e["attribution"] == "dut"},
                         {(2, "the capture ended inside a constant-mask excursion")})
        verdict, detail, dut = self._independent([("xor", k, 2, 0x100) for k in range(8192 - 40, 8192)])
        self.assertEqual([e[2:5] for e in dut], [("unresolved", 40, "0x00000100")])
        # Past the window bound a constant-mask corruption stays bit-flips with that mask.
        frames = AUDIO_WINDOW_WORDS + 6000
        verdict, detail, dut = self._independent([("xor", k, 2, 0x200) for k in range(2000, frames - 2000)],
                                                 frames=frames)
        self.assertEqual({(e[0], e[2], e[4]) for e in dut}, {(2, "bit-flip", "0x00000200")})
        self.assertEqual(sum(e[3] for e in dut), frames - 4000)
        self.assertEqual(dut[0][1], 2000)

    def _corruption_first(self, at: int, gap: int, n: int) -> list | None:
        """The ops that put a code-bit corruption first and channel 2's slip of `n` after `at + gap`.

        A slip of whole blocks at `at` and a code-bit corruption at `at + gap`
        give the same bytes when the slip's first differing word is the only
        one before the corruption, and the corrupted word is the old track's.
        """
        def differs(index: int) -> bool:
            """Whether channel 2's two tracks differ at `index`; the start arms add one."""
            return self._word(3, index + 1) != self._word(3, index + 1 + n)

        first = next((index for index in range(at, at + gap) if differs(index)), None)
        if first is None:
            return None
        return [("shift", at, n, c) for c in (0, 1, 3)] + [("xor", first, 2, 0x100), ("shift", at + gap + 1, n, 2)]

    def test_audio_slip_and_corruption_share_a_window(self) -> None:
        """L3 #396: a slip and a one-word corruption under 64 samples apart are both graded."""
        at = 3000
        for first, cls, size in ((3, "dropped", 3), (-2, "repeated", 2), (4096, "dropped", 4096)):
            for gap in (5, 40, 100):
                for masks in ((0x80000,), (0x40000,), (0x100,), (0x80000, 0x80000)):
                    ops = [("shift", at, first)] + [("xor", at + gap + k, 2, mask) for k, mask in enumerate(masks)]
                    with self.subTest(first=first, gap=gap, masks=masks):
                        verdict, detail, dut = self._independent(ops)
                        flips = [e for e in dut if e[2] == "bit-flip"]
                        slips = [e for e in dut if e[2] == cls]
                        other = self._corruption_first(at, gap, first) if masks == (0x100,) and first == 4096 else None
                        if other and self._independent_bytes(other) == self._independent_bytes(ops):
                            # The stated limit: the same bytes read as the corruption first.
                            corrupted = other[3][1]
                            self.assertEqual(flips, [(2, corrupted, "bit-flip", 1, "0x00000100", None)])
                            self.assertEqual(sorted((e[0], e[3]) for e in slips), [(c, size) for c in range(4)])
                            moved = [e for e in detail["events"]
                                     if e["class"] == cls and e["channel"] == 2 and e["attribution"] == "dut"]
                            low, high = moved[0]["located_within"]
                            self.assertTrue(corrupted < low <= at + gap + 1 <= high, moved)
                            continue
                        self.assertEqual(flips, [(2, at + gap, "bit-flip", len(masks), f"0x{masks[0]:08X}", None)])
                        self.assertEqual(sorted((e[0], e[3]) for e in slips), [(c, size) for c in range(4)])
                        for event in detail["events"]:
                            if event["class"] == cls and event["attribution"] == "dut":
                                low, high = event.get("located_within", (event["capture_index"],) * 2)
                                self.assertTrue(low <= at <= high, event)
        # A DUT slip beside a planted flip arm fails the run with the arm found.
        for slip_at in (440, 470, 495, 498, 505):
            verdict, detail, dut = self._independent([("shift", slip_at, 1)])
            self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
            self.assertEqual(dut, [(c, slip_at, "dropped", 1, None, None) for c in range(4)])
        # Arms closer than 64 samples are each found.
        frames = 4 * 4096
        for gap in (10, 40, 63):
            source, arms = [], []
            for start in (100, frames - 900):
                source += [{"kind": "drop", "index": start, "n": 3}, {"kind": "repeat", "index": start + gap, "n": 2},
                           {"kind": "flip", "index": start + 2 * gap, "channel": 1, "mask": 0x100}]
                arms += [{"class": "dropped", "index": start, "n": 3},
                         {"class": "repeated", "index": start + gap, "n": 2},
                         {"class": "bit-flip", "index": start + 2 * gap, "mask": 0x100, "channel": 1}]
            with self.subTest(gap=gap):
                verdict, detail = grade_audio_counter_capture(
                    synthesize_counter_capture(frames, 4, events=source), CounterCapture(4, "big", 48000, 0.0, 0.0),
                    CounterRunLog(arms, [], 0), required_s=(frames - 2 * 63) / 48000)
                self.assertEqual((verdict, detail["planted_missed"]), ("PASS", []), detail["why"])

    def test_audio_block_slip_after_a_corruption_or_a_slip(self) -> None:
        """L3 #396: a slip of whole blocks under 64 samples after a one-word corruption or a short
        slip is graded in its class, the first event at its sample and the slip located around its own."""
        at, steps = 3000, (1, 2, 3, 4, 5, 9, 17, 33, 63, 64)

        def slips(detail: dict) -> list:
            """(channel, n, first, last) of each DUT slip, `located_within` or its sample."""
            return sorted((e["channel"], e["n"]) + tuple(e.get("located_within", (e["capture_index"],) * 2))
                          for e in detail["events"]
                          if e["attribution"] == "dut" and e["class"] in ("dropped", "repeated"))

        def same(index: int, a: int, b: int) -> bool:
            """Whether offsets `a` and `b` give one word at `index`; the start arms add one."""
            return self._word(3, index + 1 + a) == self._word(3, index + 1 + b)

        for mask in (0x100, 0x80000):
            for n in (2048, -2048, 4096, -4096, 8192):
                for k in steps:
                    ops = [("xor", at, 2, mask), ("shift", at + k, n)]
                    with self.subTest(mask=mask, n=n, k=k):
                        verdict, detail, dut = self._independent(ops)
                        self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
                        found = slips(detail)
                        self.assertEqual([s[:2] for s in found], [(c, abs(n)) for c in range(4)])
                        if mask == 0x100 and not same(at, 0, n) and all(same(i, 0, n) for i in range(at + 1, at + k)):
                            # The stated limit: the corrupted word is the new track's and every word up
                            # to the slip fits both, so the bytes are the slip alone, at the corrupted word.
                            alone = [("shift", at, n, 2)] + [("shift", at + k, n, c) for c in (0, 1, 3)]
                            self.assertEqual(self._independent_bytes(alone), self._independent_bytes(ops))
                            self.assertNotIn("bit-flip", {e[2] for e in dut})
                            self.assertTrue(found[2][2] <= at <= found[2][3], found)
                            continue
                        self.assertEqual([e for e in dut if e[2] == "bit-flip"],
                                         [(2, at, "bit-flip", 1, f"0x{mask:08X}", None)])
                        for slip in found:
                            self.assertTrue(slip[2] <= at + k <= slip[3], found)
        for first in (3, -2):
            for n in (4096, -4096):
                for k in steps:
                    ops = [("shift", at, first), ("shift", at + k, n)]
                    with self.subTest(first=first, n=n, k=k):
                        verdict, detail, dut = self._independent(ops)
                        self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
                        found = slips(detail)
                        if all(same(i, first, first + n) for i in range(at, at + k)):
                            # The stated limit: every word up to the second slip fits both, so the
                            # bytes are one slip of the sum, at the first.
                            self.assertEqual(self._independent_bytes([("shift", at, first + n)]),
                                             self._independent_bytes(ops))
                            self.assertEqual(found, [(c, abs(first + n), at, at) for c in range(4)])
                            continue
                        self.assertEqual(sorted(s[:2] for s in found),
                                         sorted([(c, abs(first)) for c in range(4)] + [(c, abs(n)) for c in range(4)]))
                        for slip in found:
                            self.assertTrue(slip[2] <= (at if slip[1] == abs(first) else at + k) <= slip[3], found)
        # A half-block corruption next to a slip of whole blocks it follows keeps its own mask:
        # the reading whose mask has fewer bits set puts the slip first.
        for n in (2048, -4096, 4096, 8192):
            for j in (0, 1, 2, 3):
                ops = [("shift", at, n), ("xor", at + j, 2, 0x80000)]
                with self.subTest(n=n, j=j):
                    verdict, detail, dut = self._independent(ops)
                    self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
                    self.assertEqual([e for e in dut if e[2] == "bit-flip"],
                                     [(2, at + j, "bit-flip", 1, "0x00080000", None)])
                    found = slips(detail)
                    self.assertEqual([s[:2] for s in found], [(c, abs(n)) for c in range(4)])
                    for slip in found:
                        self.assertTrue(slip[2] <= at <= slip[3], found)

    def test_audio_planted_arms_beside_block_slips(self) -> None:
        """L3 #396: a DUT slip of whole blocks beside a planted arm fails with every arm found,
        where the capture alone would read the arm into the slip; the arm log decides."""
        frames = 8192
        for arm, channel, sizes in ((500, 1, (2048, -2048, 4096, -4096, 8192)),
                                    (frames - 200, 3, (2048, -2048, 4096, -4096, 8192)),
                                    (300, None, (4096, -4096)), (frames - 700, None, (4096, -4096))):
            for side in (1, -1):
                for k in (1, 2, 3, 9):
                    for n in sizes:
                        at = arm + side * k
                        ops = [[("shift", at, n)]] + ([[("shift", at, n, channel)]] if channel and k < 3 else [])
                        for op in ops:
                            with self.subTest(arm=arm, op=op):
                                verdict, detail, dut = self._independent(op)
                                self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
                                self.assertEqual({e[2:4] for e in dut}, {("dropped" if n > 0 else "repeated", abs(n))})
                                for event in detail["events"]:
                                    if event["attribution"] == "dut":
                                        low, high = event.get("located_within", (event["capture_index"],) * 2)
                                        self.assertTrue(low <= at <= high, event)
        # A DUT slip that undoes a slip arm at the next sample leaves one displaced word, which the
        # log reads as the arm and that slip, never as a corruption that voids the run.
        for at, n in ((299, 2), (301, 2), (99, -3), (101, -3)):
            verdict, detail, dut = self._independent([("shift", at, n)])
            self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), (at, detail["why"]))
            self.assertEqual({e[1:4] for e in dut}, {(at, "dropped" if n > 0 else "repeated", abs(n))})
        # The stated limit: a DUT slip at a planted slip arm's own sample is one slip of their sum.
        # Unless the two differ by whole blocks, the arm is then missed and the run is void.
        verdict, detail, dut = self._independent([("shift", 300, 1024)])
        self.assertEqual((verdict, [arm["index"] for arm in detail["planted_missed"]]), ("NOT RUN", [300]))
        self.assertEqual({e[2:4] for e in dut}, {("dropped", 1022)})
        verdict, detail, dut = self._independent([("shift", 300, 4096)])
        self.assertEqual((verdict, detail["planted_missed"], {e[2:4] for e in dut}), ("FAIL", [], {("dropped", 4096)}))
        # A logged arm the capture does not show is still missed: the log never invents an arm.
        def grade(ops: list, arms: list) -> tuple[str, dict]:
            """Grade `ops` against a given arm log over the clean qualified length."""
            return grade_audio_counter_capture(
                self._independent_bytes(ops), CounterCapture(4, "big", 48000, 0.0, 0.0),
                CounterRunLog(arms, [], 0), required_s=(frames - 2 * 63) / 48000)

        for change in ({"index": 507}, {"mask": 0x200}):
            arms = [dict(arm, **change) if arm["class"] == "bit-flip" and arm["index"] == 500 else arm
                    for arm in self._independent_arms(frames)]
            verdict, detail = grade([("shift", 503, 4096)], arms)
            self.assertEqual((verdict, len(detail["planted_missed"])), ("NOT RUN", 1), change)
        # An unplanted flip logged before a slip of whole blocks is found only where the bytes are that
        # flip and the slip; a reading that needs more DUT events to place it is never taken.
        def differs(index: int) -> bool:
            """Whether channel 2's track and its slip of 4096 differ at `index`; the start arms add one."""
            return self._word(3, index + 1) != self._word(3, index + 1 + 4096)

        marks = [x for x in range(2990, 3010) if differs(x)]
        for x in marks[-3:]:
            logged = self._independent_arms(frames) + [{"class": "bit-flip", "index": x, "mask": 0x100, "channel": 2}]
            verdict, detail = grade([("shift", 3010, 4096)], logged)
            hidden = any(differs(i) for i in range(x + 1, 3010))
            self.assertEqual((verdict, [arm["index"] for arm in detail["planted_missed"]]),
                             ("NOT RUN", [x]) if hidden else ("FAIL", []), x)

    def test_audio_constant_mask_beside_one_word_events(self) -> None:
        """L3 #396: a constant-mask excursion stays one bit-flip beside a one-word corruption."""
        start = 3000
        for mask in (0x80000, 0x40000):
            for gap in (1, 2, 5, 20, 63, 64):
                for flip in (start - gap, start + 100 + gap - 1):
                    ops = [("xor", start + k, 2, mask) for k in range(100)] + [("xor", flip, 2, 0x100)]
                    with self.subTest(mask=mask, flip=flip):
                        verdict, detail, dut = self._independent(ops)
                        self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
                        self.assertEqual(dut, sorted([(2, start, "bit-flip", 100, f"0x{mask:08X}", None),
                                                      (2, flip, "bit-flip", 1, "0x00000100", None)]))
        # A planted arm as the neighbour: the arm is found and the excursion is one bit-flip. A drop
        # at its return resumes nearer the old track than the held one, so the excursion returned.
        for channel, begin in ((1, 395), (1, 501), (0, 8192 - 800), (2, 8192 - 800)):
            verdict, detail, dut = self._independent([("xor", begin + k, channel, 0x80000) for k in range(100)])
            self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
            self.assertEqual(dut, [(channel, begin, "bit-flip", 100, "0x00080000", None)])
        # The stated limit: an excursion that a slip interrupts is the slips its words show.
        verdict, detail, dut = self._independent([("xor", 250 + k, 1, 0x80000) for k in range(100)])
        self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
        self.assertEqual({e[2] for e in dut}, {"dropped", "repeated"})
        # With no clean word between, across a block boundary or under a mask that leaves the channel
        # number, the neighbour is still its own one-word event; a slip at the return is that slip.
        for begin, length, mask, flip, sites in ((4080, 64, 0x100, 0x80000, (4079,)),
                                                  (4080, 64, 0x100, 0x80000, (4144,)),
                                                  (4089, 64, 0x80000, 0x100, (4088, 4153)),
                                                  (6140, 65, 0x100, 0x80000, (6139, 6205)),
                                                  (3000, 100, 0x00F00F00, 0x100, (2999,)),
                                                  (3000, 100, 0x00F00F00, 0x100, (3100,))):
            ops = [("xor", begin + k, 2, mask) for k in range(length)] + [("xor", at, 2, flip) for at in sites]
            with self.subTest(begin=begin, mask=mask, sites=sites):
                verdict, detail, dut = self._independent(ops)
                self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
                self.assertEqual(dut, sorted([(2, begin, "bit-flip", length, f"0x{mask:08X}", None)] + [
                    (2, at, "bit-flip", 1, f"0x{flip:08X}", None) for at in sites]))
        for begin, length, mask, n in ((4089, 64, 0x80000, 3), (4089, 65, 0x40000, -2), (6143, 64, 0x80100, -2)):
            ops = [("xor", begin + k, 2, mask) for k in range(length)] + [("shift", begin + length, n)]
            with self.subTest(begin=begin, mask=mask, n=n):
                verdict, detail, dut = self._independent(ops)
                self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
                self.assertEqual(dut, sorted([(2, begin, "bit-flip", length, f"0x{mask:08X}", None)] + [
                    (c, begin + length, "dropped" if n > 0 else "repeated", abs(n), None, None) for c in range(4)]))

    def test_audio_code_bit_corruption_ending_on_a_block(self) -> None:
        """L3 #396: a code-bit corruption over whole blocks is one bit-flip wherever it ends;
        the old track's own words are its return, never a release."""
        frames = 16384
        for begin in (5000, 6143, 6144):
            for end in (8191, 8192, 8193, 8200, 10239, 10240, 12288):
                ops = [("xor", k, 2, 0x100) for k in range(begin, end)]
                with self.subTest(begin=begin, end=end):
                    verdict, detail, dut = self._independent(ops, frames=frames)
                    self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
                    self.assertEqual(dut, [(2, begin, "bit-flip", end - begin, "0x00000100", None)])

    #: Issue #396 composition sweep: one mask for each class of bits a corruption can touch: the
    #: code bit, position bit 0, four position bits, position bits 9 and 10, bit 10 with the code
    #: bit, a channel-number bit and a pad bit.
    _SWEEP_MASKS = (0x100, 0x200, 0x1E00, 0x40000, 0x80000, 0x80100, 0x100000, 0x01000000)

    @staticmethod
    def _sweep_arms(frames: int) -> list:
        """(class, index, size or mask, channel) of the arms the composition sweep plants and logs."""
        return [("dropped", 300, 3, None), ("repeated", 500, 2, None), ("bit-flip", 700, 0x100, 1),
                ("dropped", frames - 700, 3, None), ("repeated", frames - 450, 2, None),
                ("bit-flip", frames - 200, 0x100, 1)]

    def _sweep_log(self, frames: int) -> list:
        """The sweep's arms as the source logs them."""
        return [{"class": cls, "index": index, "mask": size, "channel": channel} if cls == "bit-flip"
                else {"class": cls, "index": index, "n": size}
                for cls, index, size, channel in self._sweep_arms(frames)]

    def _sweep_shift(self, frames: int, index: int) -> int:
        """The content shift the sweep's slip arms put in force at capture index `index`."""
        return sum(size if cls == "dropped" else -size for cls, at, size, _ in self._sweep_arms(frames)
                   if cls != "bit-flip" and at <= index)

    def _sweep_grade(self, frames: int, extra: list, channels: int = 4) -> tuple[str, dict, list]:
        """Grade the sweep's arms and `extra` synthesizer events at the release arm tolerance of 2.

        Returns the verdict, the detail and each channel's received words.
        """
        from array import array
        source = [{"kind": "flip", "index": index, "channel": channel, "mask": size} if cls == "bit-flip"
                  else {"kind": "drop" if cls == "dropped" else "repeat", "index": index, "n": size}
                  for cls, index, size, channel in self._sweep_arms(frames)]
        capture = synthesize_counter_capture(frames, channels, byteorder=sys.byteorder, events=source + extra)
        verdict, detail = grade_audio_counter_capture(
            capture, CounterCapture(channels, sys.byteorder, 48000, 0.0, 0.0),
            CounterRunLog(self._sweep_log(frames), [], 2), required_s=(frames - 2 * 63) / 48000)
        words = array("I", capture)
        return verdict, detail, [words[channel::channels] for channel in range(channels)]

    def _sweep_independent(self, frames: int, ops: list) -> tuple[str, dict]:
        """Grade `_independent_bytes` of the sweep's arms and `ops` at the release arm tolerance of 2."""
        arms = [("xor", index, channel, size) if cls == "bit-flip"
                else ("shift", index, size if cls == "dropped" else -size)
                for cls, index, size, channel in self._sweep_arms(frames)]
        return grade_audio_counter_capture(
            self._independent_bytes(arms + ops, frames, arms=False), CounterCapture(4, "big", 48000, 0.0, 0.0),
            CounterRunLog(self._sweep_log(frames), [], 2), required_s=(frames - 2 * 63) / 48000)

    def _sweep_class(self, case: tuple, column) -> str:
        """The class one corruption beside one arm falls in, decided from the bytes alone.

        "void-flip": on a flip arm's own word, or beside it under the arm's mask, on its channel.
        "void-position": on a slip arm's sample or the one before it, the corrupted word being its
        channel's word at another position at most half a block from the old or the new track's.
        "neighbour": a corrupted word equal to a received neighbour. "first": on a slip arm's
        sample or the next one. "exact": any other.
        """
        frames, (cls, index, size, arm_channel), d, channel, mask = case
        at, word = index + d, column[index + d]
        if cls == "bit-flip" and channel == arm_channel and (d == 0 or abs(d) == 1 and mask == size):
            return "void-flip"
        if cls != "bit-flip" and d in (-1, 0):
            true = at + self._sweep_shift(frames, at)
            for base in (at + self._sweep_shift(frames, index - 1), at + self._sweep_shift(frames, index)):
                delta = ((word >> 9) - base) % AUDIO_BLOCK_FRAMES
                for q in (base + delta, base + delta - AUDIO_BLOCK_FRAMES):
                    if abs(q - base) <= AUDIO_BLOCK_FRAMES // 2 and q != true and self._word(channel + 1, q) == word:
                        return "void-position"
        if word in (column[at - 1], column[at + 1]):
            return "neighbour"
        return "first" if cls != "bit-flip" and d in (0, 1) else "exact"

    def _sweep_case(self, case: tuple, near: list, column) -> None:
        """Check one exact, neighbour or first case: the arm's event and the corruption's, or its stated reading."""
        frames, (cls, index, size, arm_channel), d, channel, mask, kind = case
        at = index + d
        if cls == "bit-flip":
            own = [e for e in near if channel == arm_channel and e["capture_index"] == index
                   and (e["class"], e["n"], e["mask"]) == (cls, 1, f"0x{size:08X}")]
        else:
            own = [e for e in near if e["class"] == cls and e["n"] == size and index <= e["capture_index"] <= index + 2]
        self.assertEqual(len(own), 0 if cls == "bit-flip" and channel != arm_channel else 1, near)
        rest = [(e["capture_index"], e["class"], e["n"], e.get("mask")) for e in near if e not in own]
        if rest == [(at, "bit-flip", 1, f"0x{mask:08X}")] and (not own or own[0]["capture_index"] == index):
            return
        self.assertIn(kind, ("neighbour", "first"), near)
        if kind == "neighbour":
            self.assertEqual(rest[0][0::2] + rest[1][0::2], (at, 1, at + 1, 1), near)
            self.assertEqual({rest[0][1], rest[1][1]}, {"dropped", "repeated"}, near)
            return
        # The stated reading: the corruption first, judged against the offset before the slip, the slip after it.
        (first, flip, one, masked), moved = rest[0], own[0]["capture_index"]
        self.assertEqual((len(rest), flip, one), (1, "bit-flip", 1), near)
        self.assertTrue(first < moved <= index + 2, near)
        old, new = self._sweep_shift(frames, index - 1), self._sweep_shift(frames, index)
        for i in range(first, moved + AUDIO_CONFIRM_FRAMES):
            want = self._word(channel + 1, i + (old if i < moved else new)) ^ (int(masked, 16) if i == first else 0)
            self.assertEqual(column[i], want, (i, near))

    def _sweep_check(self, case: tuple, graded: tuple) -> None:
        """Check one composition-sweep capture: each case's class from its bytes, then its reading."""
        frames, d, mask, pair = case
        verdict, detail, columns = graded
        self.assertNotIn(AUDIO_UNBALANCED_REASON, {e.get("unresolved") for e in detail["events"]})
        voids = set()
        for arm in self._sweep_arms(frames):
            cls, index, size, arm_channel = arm
            for channel in pair:
                column = columns[channel]
                planted = size if cls == "bit-flip" and channel == arm_channel and d == 0 else 0
                self.assertEqual(column[index + d], self._word(channel + 1, index + d + self._sweep_shift(
                    frames, index + d)) ^ mask ^ planted)
                kind = self._sweep_class((frames, arm, d, channel, mask), column)
                near = [e for e in detail["events"] if e["channel"] == channel and abs(e["capture_index"] - index) <= 8]
                # Every reading balances: the slips beside an arm sum to the arm's own shift.
                self.assertEqual(_audio_net(near), 0 if cls == "bit-flip" else size if cls == "dropped" else -size,
                                 (arm, channel, kind, near))
                if kind.startswith("void"):
                    voids.add(index)
                    continue
                self._sweep_case((frames, arm, d, channel, mask, kind), near, column)
        self.assertEqual((verdict, sorted(arm["index"] for arm in detail["planted_missed"])),
                         ("NOT RUN", sorted(voids)) if voids else ("FAIL", []), detail["why"])

    def _sweep_mirrored(self, frames: int, slip: dict, detail: dict, column) -> None:
        """The stated limit for a slip located away from its sample beside a flip arm: the bytes are
        that slip where the reading puts it, with the arm's code bit moved to the word the reading
        flips, within the tolerance."""
        flips = [e for e in detail["events"] if e["channel"] == slip["channel"] and e["class"] == "bit-flip"]
        arm = next(a for a in self._sweep_arms(frames) if a[0] == "bit-flip" and a[3] == slip["channel"]
                   and abs(a[1] - slip["capture_index"]) <= 8)
        flip = next(e for e in flips if abs(e["capture_index"] - arm[1]) <= 2 and e["mask"] == "0x00000100")
        size = slip["n"] if slip["class"] == "dropped" else -slip["n"]
        at, old = slip["capture_index"], self._sweep_shift(frames, slip["capture_index"])
        for i in range(min(at, arm[1]) - 2, max(at, arm[1]) + AUDIO_CONFIRM_FRAMES):
            want = self._word(slip["channel"] + 1, i + old + (size if i >= at else 0))
            self.assertEqual(column[i], want ^ (0x100 if i == flip["capture_index"] else 0), (i, slip, flip))

    def test_audio_composition_sweep(self) -> None:
        """L3 #396 REQ-VER-06: a one-word corruption 0 to 4 samples from each planted arm, on every
        channel, under each class of mask, on two capture lengths at the release tolerance, is graded
        exactly or as the stated limit its bytes fall in, and every reading balances.

        Each capture carries one case beside each of its six arms, on two channels whose numbers no
        one mask exchanges; its arms are 200 samples or more apart, so their windows never meet.
        """
        for frames in (8192, 16384):
            for d in range(-4, 5):
                for mask in self._SWEEP_MASKS:
                    for pair in ((0, 1), (2, 3)):
                        extra = [{"kind": "flip", "index": arm[1] + d, "channel": channel, "mask": mask}
                                 for arm in self._sweep_arms(frames) for channel in pair]
                        with self.subTest(frames=frames, d=d, mask=hex(mask), pair=pair):
                            self._sweep_check((frames, d, mask, pair), self._sweep_grade(frames, extra))
        # The stated voids, one of each: a word of another position before a slip arm and on it, the
        # flip arm's own word, and the word beside it under its mask.
        for at, channel, mask in ((299, 0, 0x40000), (500, 2, 0x80000), (700, 1, 0x200), (701, 1, 0x100)):
            verdict, detail, _ = self._sweep_grade(8192, [{"kind": "flip", "index": at, "channel": channel,
                                                           "mask": mask}])
            self.assertEqual((verdict, detail["why"]), ("NOT RUN", "void: a planted arm was missed"), at)

    def test_audio_slip_before_a_constant_mask(self) -> None:
        """L3 #396 REQ-VER-06: a drop of 3 or a repeat of 2 on every channel, 1 to 64 samples before a
        constant-mask excursion of 64 to 2049 words at three block positions, leaves the excursion one
        bit-flip and the slip exact. Each capture carries the excursion on five channels, one mask each:
        the channel numbers no mask here makes another channel's."""
        masks = (0x80000, 0x40000, 0x100, 0x00F00F00, 0x80100)
        for length in (64, 65, 100, 300, 2049):
            for begin in (3000, 4089, 6143):
                for gap in (1, 2, 17, 63, 64):
                    for n in (3, -2):
                        extra = [{"kind": "drop" if n > 0 else "repeat", "index": begin - gap, "n": abs(n)}]
                        extra += [{"kind": "flip", "index": begin + k, "channel": channel, "mask": mask}
                                  for channel, mask in enumerate(masks) for k in range(length)]
                        verdict, detail, _ = self._sweep_grade(16384, extra, channels=len(masks))
                        with self.subTest(length=length, begin=begin, gap=gap, n=n):
                            self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
                            slip = (begin - gap, "dropped" if n > 0 else "repeated", abs(n), "")
                            for channel, mask in enumerate(masks):
                                got = [(e["capture_index"], e["class"], e["n"], e.get("mask", ""))
                                       for e in detail["events"]
                                       if e["attribution"] == "dut" and e["channel"] == channel]
                                self.assertEqual(sorted(got), [slip, (begin, "bit-flip", length, f"0x{mask:08X}")])

    def test_audio_slip_totals_balance_the_bytes(self) -> None:
        """L3 #396 REQ-VER-06: the slips a reading reports sum, on every channel, to the shift its
        closing samples decode; a reading that does not is never taken, and where none does the
        window is one unclassified corruption, never a slip that did not happen."""
        def excursion(begin: int, length: int, mask: int) -> list:
            """Channel 2's words from `begin` under `mask`."""
            return [("xor", begin + k, 2, mask) for k in range(length)]

        # A one-word corruption 1 to 4 samples before a constant-mask excursion, near a block boundary,
        # is never a whole-block slip that never returns; nor beside both ends of a code-bit excursion.
        for neighbours, begin, length, mask in (([(4085, 0x100)], 4088, 100, 0x80000),
                                                ([(4087, 0x80000)], 4089, 100, 0x80100),
                                                ([(2997, 0x100)], 3000, 100, 0x80000),
                                                ([(4078, 0x80000), (4145, 0x80000)], 4080, 64, 0x100),
                                                ([(4077, 0x80000), (4146, 0x80000)], 4080, 64, 0x100),
                                                ([(4092, 0x80000)], 4094, 64, 0x100),
                                                ([(4086, 0x80000)], 4088, 64, 0x100)):
            ops = excursion(begin, length, mask) + [("xor", at, 2, flip) for at, flip in neighbours]
            with self.subTest(neighbours=neighbours, begin=begin):
                verdict, detail, dut = self._independent(ops)
                self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
                self.assertEqual(dut, sorted([(2, begin, "bit-flip", length, f"0x{mask:08X}", None)] + [
                    (2, at, "bit-flip", 1, f"0x{flip:08X}", None) for at, flip in neighbours]))
                for channel in range(4):
                    self.assertEqual(_audio_net(e for e in detail["events"] if e["channel"] == channel), 2)
        from unittest.mock import patch
        # The guard: a reading that loses a slip is never recorded as read.
        read = _CounterScan._read

        def lossy(scan: _CounterScan, track: _AudioTrack, tokens: list, final: int | None) -> tuple:
            """The reading with its slip of 1024 lost."""
            events, offset = read(scan, track, tokens, final)
            return [e for e in events if e["n"] != 1024], offset

        with patch.object(_CounterScan, "_read", lossy):
            verdict, detail, dut = self._independent([("shift", 3000, 1024), ("xor", 2990, 2, 0x01000000)])
        self.assertEqual(verdict, "FAIL", detail["why"])
        self.assertEqual(dut, sorted([(c, 3000, "unresolved", 1, "0x00080000", None) for c in (0, 1, 3)]
                                     + [(2, 2990, "unresolved", 11, "0x01080000", None)]))
        self.assertEqual({e["unresolved"] for e in detail["events"] if e["attribution"] == "dut"},
                         {AUDIO_UNBALANCED_REASON})
        # A reading with fewer DUT events that does not balance is never taken over one that does.
        events = _audio_window_events

        def tempting(track: _AudioTrack, labels: list, final: int | None, steer: _AudioSteer | None = None) -> tuple:
            """An arm-led reading that finds the arm with one DUT event but loses a sample."""
            read = events(track, labels, final, steer)
            if steer is not None and steer.keep:
                arm = {"capture_index": 300, "class": "dropped", "n": 3, "expected": 0, "received": 0}
                return [arm, dict(arm, capture_index=301, **{"class": "repeated", "n": 1})], read[1]
            return read

        with patch.dict(globals(), {"_audio_window_events": tempting}):
            verdict, detail, _ = self._sweep_grade(8192, [{"kind": "flip", "index": 299, "channel": 0,
                                                            "mask": 0x40000}])
        self.assertEqual((verdict, [arm["index"] for arm in detail["planted_missed"]]), ("NOT RUN", [300]))
        self.assertNotIn(AUDIO_UNBALANCED_REASON, {e.get("unresolved") for e in detail["events"]})
        self.assertEqual(sorted((e["capture_index"], e["class"], e["n"]) for e in detail["events"]
                                if e["channel"] == 0 and 290 < e["capture_index"] < 310),
                         [(299, "dropped", 512), (300, "repeated", 509)])

    def test_audio_arm_interplay_at_the_release_tolerance(self) -> None:
        """L3 #396: at the release arm tolerance of 2, a DUT slip of whole blocks beside a planted flip
        arm, on two capture lengths, and a slip arm inside a cluster of slips of whole blocks, fail with
        every arm found and every reading balanced; a flip arm is found only as one word under its mask."""
        for frames, at, n in ((16384, 16185, -2048), (16384, 16185, 8192), (16384, 701, 4096),
                              (8192, 7993, -2048), (8192, 699, -2048), (8192, 702, 4096), (8192, 3000, 4096)):
            source = [{"kind": "drop" if n > 0 else "repeat", "index": at, "n": abs(n)}]
            verdict, detail, columns = self._sweep_grade(frames, source)
            with self.subTest(frames=frames, at=at, n=n):
                self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
                dut = [e for e in detail["events"] if e["attribution"] == "dut"]
                self.assertEqual(sorted((e["channel"], e["class"], e["n"]) for e in dut),
                                 [(c, "dropped" if n > 0 else "repeated", abs(n)) for c in range(4)])
                for event in dut:
                    low, high = event.get("located_within", (event["capture_index"],) * 2)
                    if low <= at <= high:
                        continue
                    self._sweep_mirrored(frames, event, detail, columns[event["channel"]])
        # A slip arm inside a cluster of slips of whole blocks is split from them within the tolerance.
        frames = 16384
        for ops in ([("xor", 15664, 0, 0x100), ("shift", 15684, -4096), ("shift", 15696, -4096)],
                    [("shift", 15667, -4096, 0), ("xor", 15677, 2, 0x100), ("shift", 15705, -4096)],
                    [("shift", 15639, 8192), ("shift", 15661, 1024, 0), ("shift", 15693, 4096)]):
            with self.subTest(ops=ops):
                verdict, detail = self._sweep_independent(frames, ops)
                self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
                for channel in range(4):
                    shifts = [op[2] for op in ops if op[0] == "shift" and (len(op) < 4 or op[3] == channel)]
                    self.assertEqual(_audio_net(e for e in detail["events"] if e["channel"] == channel),
                                     sum(shifts) + 2)
        # A slip of half a block before the flip arm is a slip, not an excursion its arm word interrupts.
        verdict, detail, _ = self._sweep_grade(frames, [{"kind": "drop", "index": 684, "n": 1024}])
        self.assertEqual((verdict, detail["planted_missed"]), ("FAIL", []), detail["why"])
        self.assertEqual(sorted((e["channel"], e["capture_index"], e["class"], e["n"]) for e in detail["events"]
                                if e["attribution"] == "dut"), [(c, 684, "dropped", 1024) for c in range(4)])

    def test_audio_anchor_gaps_are_reported(self) -> None:
        """L3 #396: stretches the capture tool left unanchored are named; the verdict stands."""
        frames, rate = 8192, 48000
        verdict, detail, _ = self._independent([])
        self.assertEqual((verdict, detail["anchor_gaps"]), ("PASS", [[0, frames]]))
        verdict, detail, _ = self._independent([], anchors=((frames, 1.0, 1.0),))
        self.assertEqual((verdict, detail["anchor_gaps"]), ("PASS", []))
        verdict, detail, _ = self._independent([], anchors=((4000, 0.5, 0.5), (frames, 1.0, 1.0)), context_s=0.1)
        self.assertEqual(detail["anchor_gaps"], [])
        verdict, detail, _ = self._independent([], anchors=((frames, 1.0, 1.0),), context_s=0.1)
        self.assertEqual(detail["anchor_gaps"], [[0, frames]])
        verdict, detail, _ = self._independent(
            [("shift", 3000, 3000)], losses=[{"index": 3000, "frames": 3000}],
            anchors=((4000, 0.5, 0.5), (frames, 1.0, 1.0)), context_s=0.1)
        self.assertEqual((verdict, detail["anchor_gaps"]), ("PASS", [[0, 4000]]))
        self.assertGreater(4000 + 3000, 0.1 * rate)

    @staticmethod
    def _grade_args(capture, args: dict) -> tuple[str, dict]:
        args = dict(args)
        max_events = args.pop("max_events", 100000)
        required_s = args.pop("required_s", RELEASE_SOAK_DURATION_S)
        log = CounterRunLog(args.pop("planted_arms"), args.pop("capture_losses"),
                            args.pop("arm_tolerance_frames"))
        return grade_audio_counter_capture(capture, CounterCapture(**args), log,
                                           max_events=max_events, required_s=required_s)

    def _grade(self, extra=(), losses=(), arms=None, frames=4 * 4096, **kw):
        base = [{"kind": "drop", "index": 100, "n": 3}, {"kind": "repeat", "index": 300, "n": 2},
                {"kind": "flip", "index": 500, "channel": 1, "mask": 0x100},
                {"kind": "drop", "index": frames - 900, "n": 3},
                {"kind": "repeat", "index": frames - 600, "n": 2},
                {"kind": "flip", "index": frames - 300, "channel": 3, "mask": 0x100}]
        logged = [{"class": "dropped", "index": 100, "n": 3}, {"class": "repeated", "index": 300, "n": 2},
                  {"class": "bit-flip", "index": 500, "mask": 0x100, "channel": 1},
                  {"class": "dropped", "index": frames - 900, "n": 3},
                  {"class": "repeated", "index": frames - 600, "n": 2},
                  {"class": "bit-flip", "index": frames - 300, "mask": 0x100, "channel": 3}]
        order = kw.pop("byteorder", "big")
        capture = synthesize_counter_capture(frames, 4, byteorder=order if order == "little" else "big",
                                             start_counter=kw.pop("start", 0),
                                             events=base + list(extra)) + kw.pop("tail", b"")
        if kw.pop("chunk", None):
            capture = [capture[i:i + 1000] for i in range(0, len(capture), 1000)]
        args = dict(channels=4, byteorder=order, rate_hz=48000,
                    planted_arms=logged if arms is None else arms, capture_losses=list(losses),
                    arm_tolerance_frames=2, start_wall_s=100.0, start_gptp_s=7.0, context_s=5,
                    required_s=(frames - 2 * 63) / 48000)
        args.update(kw)
        verdict, detail = self._grade_args(capture, args)
        dut = [e for e in detail.get("events", []) if e["attribution"] == "dut"]
        return verdict, detail, dut

    def test_audio_grader_classes(self) -> None:
        """Each class is found at its sample with its size, mask or partner."""
        at = 2 * 4096 + 13
        cases = (({"kind": "drop", "index": at, "n": 5}, "dropped", {"n": 5}, 4),
                 ({"kind": "repeat", "index": at, "n": 4}, "repeated", {"n": 4}, 4),
                 ({"kind": "drop", "index": at, "n": 2047}, "dropped", {"n": 2047}, 4),
                 ({"kind": "repeat", "index": at, "n": 2047}, "repeated", {"n": 2047}, 4),
                 ({"kind": "drop", "index": at, "n": 2049}, "dropped", {"n": 2049}, 4),
                 ({"kind": "silence", "index": at, "n": 6}, "silence", {"n": 6, "inserted": False}, 4),
                 ({"kind": "silence", "index": at, "n": 6, "inserted": True}, "silence",
                  {"n": 6, "inserted": True}, 4),
                 ({"kind": "flip", "index": at, "channel": 2, "mask": 0x1}, "bit-flip",
                  {"n": 1, "mask": "0x00000001"}, 1),
                 ({"kind": "flip", "index": at, "channel": 2, "mask": 0x00000400}, "bit-flip",
                  {"n": 1, "mask": "0x00000400"}, 1),
                 ({"kind": "flip", "index": at, "channel": 2, "mask": 0x80000000}, "bit-flip",
                  {"n": 1, "mask": "0x80000000"}, 1),
                 ({"kind": "swap", "index": at, "n": 3, "channels": (0, 2)}, "swap", {"n": 3}, 2),
                 ({"kind": "drop", "index": 2 * 4096, "n": 1}, "dropped", {"n": 1}, 4))
        for event, cls, fields, count in cases:
            for options in ({}, {"chunk": True}, {"byteorder": "little"}):
                with self.subTest(event=event, options=options):
                    verdict, detail, dut = self._grade([event], **options)
                    self.assertEqual(verdict, "FAIL", detail["why"])
                    self.assertEqual(len(dut), count, dut)
                    for record in dut:
                        self.assertEqual(record["class"], cls)
                        self.assertEqual(record["capture_index"], event["index"])
                        self.assertEqual({k: record.get(k) for k in fields}, fields)
        verdict, detail, dut = self._grade([{"kind": "swap", "index": at, "n": 3, "channels": (0, 2)}])
        self.assertEqual(sorted((e["channel"], e["partner"]) for e in dut), [(0, 2), (2, 0)])
        end = 4 * 4096 / 48000
        verdict, detail, dut = self._grade([{"kind": "drop", "index": at, "n": 5}],
                                           anchors=((4 * 4096, 100.0 + end, 7.0 + end),), gptp_steps_wall_s=())
        # The start arms leave the source position at index + 3 - 2.
        self.assertEqual((dut[0]["expected"], dut[0]["received"]),
                         (f"0x{self._word(1, at + 3 - 2):08X}", f"0x{self._word(1, at + 3 - 2 + 5):08X}"))
        self.assertAlmostEqual(dut[0]["wall_s"], 100.0 + at / 48000)
        self.assertAlmostEqual(dut[0]["gptp_s"], 7.0 + at / 48000)
        self.assertEqual(dut[0]["context_wall_s"], [dut[0]["wall_s"] - 5, dut[0]["wall_s"] + 5])
        self.assertEqual((dut[0]["acquisition_index"], dut[0]["timing"]), (at, "anchored"))

    def test_audio_grader_attribution(self) -> None:
        """Logged capture losses go apart; planted arms must all be found at both ends."""
        loss = {"kind": "drop", "index": 2 * 4096 + 3, "n": 9}
        verdict, detail, dut = self._grade([loss], [{"index": loss["index"], "frames": 9}])
        self.assertEqual((verdict, dut), ("PASS", []), detail["why"])
        self.assertEqual(detail["counts"]["capture"], {"dropped": 4})
        self.assertEqual(self._grade([loss])[0], "FAIL")
        self.assertEqual(self._grade([], [{"index": loss["index"], "frames": 9}])[0], "NOT RUN")
        self.assertEqual(self._grade([loss], [{"index": loss["index"], "frames": 8}])[0], "NOT RUN")
        # The counter never repeats within a run, so even a whole-period loss must show.
        self.assertEqual(self._grade([], [{"index": 5, "frames": 4096}])[0], "NOT RUN")
        frames = 4 * 4096
        logged = [{"class": "dropped", "index": 100, "n": 3}, {"class": "repeated", "index": 300, "n": 2},
                  {"class": "bit-flip", "index": 500, "mask": 0x100, "channel": 1},
                  {"class": "dropped", "index": frames - 900, "n": 3},
                  {"class": "repeated", "index": frames - 600, "n": 2},
                  {"class": "bit-flip", "index": frames - 300, "mask": 0x100, "channel": 3}]
        self.assertEqual(self._grade(arms=logged)[0], "PASS")
        for change, expected in (({"index": 102}, "PASS"), ({"index": 103}, "NOT RUN"),
                                 ({"n": 4}, "NOT RUN"), ({"class": "repeated"}, "NOT RUN")):
            arms = [dict(logged[0], **change)] + logged[1:]
            with self.subTest(change=change):
                verdict, detail, _ = self._grade(arms=arms)
                self.assertEqual(verdict, expected, detail["why"])
        flip = [dict(arm, mask=0x200) if arm["class"] == "bit-flip" else arm for arm in logged]
        self.assertEqual(self._grade(arms=flip)[0], "NOT RUN")
        moved = [dict(arm, channel=2) if arm["class"] == "bit-flip" else arm for arm in logged]
        self.assertEqual(self._grade(arms=moved)[0], "NOT RUN")
        for half in (logged[:3], logged[3:]):
            verdict, detail, _ = self._grade(arms=half)
            self.assertEqual(verdict, "NOT RUN")
            self.assertIn("first and the last tenth", detail["why"])
        verdict, detail, dut = self._grade(arms=logged[:4] + logged[5:])
        self.assertEqual(verdict, "NOT RUN")
        self.assertEqual([e["class"] for e in dut], ["repeated"] * 4)

    def test_audio_grader_evidence(self) -> None:
        """Missing logs, bad layouts and torn captures are NOT RUN, never PASS."""
        for change in ({"planted_arms": None}, {"capture_losses": None},
                       {"arm_tolerance_frames": None}, {"start_wall_s": None},
                       {"start_gptp_s": float("nan")}, {"rate_hz": 0}, {"byteorder": "middle"},
                       {"tags": [1, 1, 2, 3]}, {"tags": [1, 2, 3]}, {"tags": [None] * 4},
                       {"tags": [0, 1, 2, 3]}, {"tags": [16, 1, 2, 3]}, {"context_s": -1},
                       {"planted_arms": [{"class": "dropped", "index": -1, "n": 3}]},
                       {"capture_losses": [{"index": 3, "frames": 0}]}):
            with self.subTest(change=change):
                self.assertEqual(self._grade(**change)[0], "NOT RUN")
        common = dict(channels=1, byteorder="big", rate_hz=48000, planted_arms=[], capture_losses=[],
                      arm_tolerance_frames=0, start_wall_s=0.0, start_gptp_s=0.0, context_s=5)
        self.assertEqual(self._grade_args(b"", common)[0], "NOT RUN")
        self.assertEqual(self._grade_args(b"\x00\x10\x05\x00\x00", common)[0], "NOT RUN")
        self.assertEqual(self._grade()[0], "PASS")
        verdict, detail, _ = self._grade(tail=b"\x00")
        self.assertEqual(verdict, "NOT RUN", detail["why"])
        self.assertIn("torn", detail["why"])
        # Channel 2 carries something else: its words are never graded.
        verdict, detail, dut = self._grade([{"kind": "flip", "index": 9000, "channel": 2, "mask": 1}],
                                           tags=[1, 2, None, 4])
        self.assertEqual((verdict, dut), ("PASS", []), detail["why"])
        verdict, detail, dut = self._grade([{"kind": "flip", "index": 9000, "channel": 1, "mask": 1}],
                                           tags=[1, 2, None, 4])
        self.assertEqual((verdict, [e["channel"] for e in dut]), ("FAIL", [1]))
        verdict, detail, _ = self._grade([{"kind": "silence", "index": 4000, "n": 3000}], max_events=3)
        self.assertEqual(verdict, "FAIL")
        self.assertGreater(detail["unrecorded_events"], 0)

    def test_release_area_audit_refuses_each_defect(self) -> None:
        """L3: phases, cycle mix, assertions and controls each redden their area."""
        from copy import deepcopy
        original = build_plan()
        for area in ("soak", "audio", "power"):
            self.assertTrue(area_covers_every_index(original, area)[0], area)
        repeats = [s.sid for s in original if s.op in RELEASE_REQUIRED_ASSERTS]
        for sid in repeats:
            source = next(s for s in original if s.sid == sid)
            for spec in source.asserts:
                for change in ("drop", "downgrade"):
                    with self.subTest(sid=sid, assertion=spec.name, change=change):
                        broken = deepcopy(original)
                        step = next(s for s in broken if s.sid == sid)
                        step.asserts = tuple(
                            replace(a, severity="INFO") if change == "downgrade" and a.name == spec.name
                            else a for a in step.asserts
                            if change == "downgrade" or a.name != spec.name)
                        ok, detail = area_covers_every_index(broken, step.area)
                        self.assertFalse(ok)
                        self.assertEqual(detail["missing"][sid]["asserts"], [spec.name])
        for phase in ("idle", "journal_commit", "soft_reset"):
            broken = deepcopy(original)
            step = next(s for s in broken if s.sid == "power." + phase)
            step.args["cycles"] -= 1
            ok, detail = area_covers_every_index(broken, "power")
            self.assertEqual((ok, detail["missing"].get("cycle_mix") is not None), (False, True), phase)
            step.args["phase"] = "idle" if phase != "idle" else "soft_reset"
            self.assertIn("phases", area_covers_every_index(broken, "power")[1]["missing"])
        for sid in (s for sids in RELEASE_CONTROLS.values() for s in sids):
            for change in ("remove", "verdict", "assertion"):
                broken = deepcopy(original)
                step = next(s for s in broken if s.sid == sid)
                if change == "remove":
                    broken.remove(step)
                elif change == "verdict":
                    step.args["expected_verdict"] = "PASS"
                else:
                    step.asserts = tuple(a for a in step.asserts
                                         if a.name != step.args["expected_failing_assertion"])
                with self.subTest(sid=sid, change=change):
                    ok, detail = area_covers_every_index(broken, step.area)
                    self.assertFalse(ok)
                    self.assertIn(sid, detail["missing"])
                    self.assertTrue(area_covers_every_index(broken, "matrix")[0])

    def test_release_audio_does_not_mask_identity(self) -> None:
        """The release run walks every index; it cannot cover an index-0-only identity loop."""
        plan = build_plan(["audio"])
        self.assertTrue(area_covers_every_index(plan, "audio")[0])
        lonely = [s for s in plan if s.op in RELEASE_REQUIRED_ASSERTS or s.op == RELEASE_CONTROL_OP
                  or s.sid.endswith(".t0") or s.sid == "audio.thdn"]
        ok, detail = area_covers_every_index(lonely, "audio")
        self.assertFalse(ok, detail)
        self.assertEqual(detail["missing"]["dut_talker"], [1, 2, 3])

    def test_release_cycle_mix_is_the_decision(self) -> None:
        """Independent arithmetic: 150 cold cuts, a third in a commit, and 50 resets."""
        repeats = [s for s in build_plan(["power"]) if s.op == "release_power_cycles"]
        cycles = {s.args["phase"]: s.args["cycles"] for s in repeats}
        cold = cycles["idle"] + cycles["journal_commit"]
        self.assertEqual((cold, cycles["journal_commit"] * 3, cycles["soft_reset"]), (150, 150, 50))
        self.assertEqual(sum(cycles.values()), 200)
        self.assertEqual({s.args["total_cycles"] for s in repeats}, {200})
        self.assertEqual({s.args["cycle_kind"] for s in repeats if s.args["cold"]}, {"cold cut"})


class _ConcurrencyChecks:
    """The multi-stream concurrency sets and the audio family.

    A mixin, not a TestCase: `self_test` combines the five into the one
    `T` whose name the report prints, so the arms can be read apart
    without a single line of that report changing.
    """
    def test_multi_area_walks_concurrent_sets_and_serialises(self) -> None:
        """Each concurrency set binds, verifies, then tears down in that order; no
        listener is bound twice inside a set (that would be a rebind, not
        concurrency), and a truncated set reddens the per-area audit."""
        plan = build_plan(["multi"])
        self.assertTrue(plan)
        sids = [s.sid for s in plan]
        # every set runs its phases in teardown-safe order; the stress
        # set carries the load sandwich between verify and teardown
        for name in ("primaries", "selfloop", "mixed"):
            phases = [s.rsplit(".", 1)[1] for s in sids
                      if s.startswith(f"multi.{name}.")]
            self.assertEqual(phases, ["bind-all", "verify-concurrent",
                                      "teardown-one", "teardown-rest"],
                             name)
        phases = [s.split(".", 2)[2] for s in sids
                  if s.startswith("multi.stress.")]
        self.assertEqual(phases, ["bind-all", "verify-concurrent",
                                  "load-rx", "load-tx",
                                  "verify-after-load",
                                  "teardown-one", "teardown-rest"])
        # the primaries set feeds EVERY reachable reference listener
        # CONCURRENTLY - the listener set comes from the peer's SPEC (the
        # peer's (p) primaries), never a hardcoded list
        bind = next(s for s in plan
                    if s.sid == "multi.primaries.bind-all")
        self.assertEqual(
            sorted(p["listener_index"] for p in bind.args["pairs"]),
            PEER.listener_indices(include_crf=False))
        self.assertTrue(all(p["listener"] == PEER.entity_id
                            for p in bind.args["pairs"]))
        # the selfloop set pairs tN -> lN on the DUT itself
        loop = next(s for s in plan
                    if s.sid == "multi.selfloop.bind-all")
        self.assertEqual([(p["talker_index"], p["listener_index"])
                          for p in loop.args["pairs"]],
                         [(i, i) for i in
                          ARTY.talker_indices(include_crf=False)])
        # within one set no listener is bound twice: the pairs must be
        # able to run CONCURRENTLY, and a doubled listener is a rebind
        for s in plan:
            if s.op == "multi_connect":
                ls = [(p["listener"], p["listener_index"])
                      for p in s.args["pairs"]]
                self.assertEqual(len(ls), len(set(ls)), s.sid)
        # the verify step carries the UNBOUND inputs for the isolation
        # verdict, and none of them is also bound in the set
        ver = next(s for s in plan
                   if s.sid == "multi.selfloop.verify-concurrent")
        self.assertTrue(ver.args["unbound"])
        bound = {(p["listener"], p["listener_index"])
                 for p in ver.args["pairs"]}
        for u in ver.args["unbound"]:
            self.assertNotIn((u["entity"], u["index"]), bound)
        # the staged teardown unbinds a SINGLE-listener talker (so silence
        # is owed) and carries the survivors it must prove undisturbed
        tear = next(s for s in plan
                    if s.sid == "multi.primaries.teardown-one")
        n = sum(1 for p in bind.args["pairs"]
                if (p["talker"], p["talker_index"]) ==
                (tear.args["unbind"]["talker"],
                 tear.args["unbind"]["talker_index"]))
        self.assertEqual(n, 1)
        self.assertTrue(tear.args["expect_talker_silent"])
        self.assertEqual(len(tear.args["survivors"]),
                         len(bind.args["pairs"]) - 1)
        # a plan step is DATA: everything serialises
        json.dumps([s.as_dict() for s in plan])
        # the per-area audit covers the multi area and passes
        ok, d = area_covers_every_index(build_plan(), "multi")
        self.assertTrue(ok, d)
        # NEGATIVE CONTROL: a multi area truncated to one pair per set
        # must redden the audit
        import dataclasses as _dc
        lonely = [_dc.replace(s, args={
            k: (v[:1] if k in ("pairs", "survivors") else v)
            for k, v in s.args.items()}) for s in plan]
        ok2, d2 = area_covers_every_index(lonely, "multi")
        self.assertFalse(ok2)
        self.assertTrue(d2["missing"])

    def test_multi_stress_set_is_maximal_and_loads_both_directions(self) -> None:
        """The stress set binds every DUT talker and feeds every reachable
        reference listener, loops the overflow home, and loads both directions
        with the 802.1Q shaping-immunity claim at SHALL and headroom at INFO."""
        plan = build_plan(["multi"])
        bind = next(s for s in plan if s.sid == "multi.stress.bind-all")
        pairs = bind.args["pairs"]
        # every DUT AAF talker is bound outbound (peer first, self-loops
        # to fill) ...
        self.assertEqual(sorted({p["talker_index"] for p in pairs
                                 if p["talker"] == ARTY.entity_id}),
                         ARTY.talker_indices(include_crf=False))
        # ... every reachable reference listener is fed ...
        self.assertEqual(sorted(p["listener_index"] for p in pairs
                                if p["listener"] == PEER.entity_id),
                         PEER.listener_indices(include_crf=False))
        # ... and the INBOUND direction rides on top
        self.assertEqual(sorted({p["talker_index"] for p in pairs
                                 if p["talker"] == PEER.entity_id}),
                         PEER.talker_indices(include_crf=False))
        # on the AX 8x8 shape: all 8 talkers out, the overflow looped
        # home.  The self-loop count is DERIVED from how many AAF sinks
        # the peer really has - it went 3 -> 4 the moment index 8 was
        # named as the peer's CRF input instead of a fifth AAF sink,
        # and a literal here would have hidden that
        ax = parse_device_spec("talkers=8,listeners=8,crf_out=8,"
                               "crf_in=8", ARTY)
        axb = next(s for s in plan_multi(ax, PEER)
                   if s.sid == "multi.stress.bind-all")
        self.assertEqual(sorted({p["talker_index"]
                                 for p in axb.args["pairs"]
                                 if p["talker"] == ax.entity_id}),
                         list(range(8)))
        n_peer = len(PEER.listener_indices(include_crf=False))
        self.assertEqual(sorted(p["talker_index"]
                                for p in axb.args["pairs"]
                                if p["talker"] == ax.entity_id
                                and p["listener"] == ax.entity_id),
                         list(range(n_peer, 8)))
        # two load steps, rx then tx, each owing the stress asserts with
        # honest severities: immune is SHALL on the 802.1Q shaping
        # contract, the headroom is INFO with the info reasoning stated
        loads = [s for s in plan if s.op == "multi_stress_load"]
        self.assertEqual([s.args["direction"] for s in loads],
                         ["rx", "tx"])
        for s in loads:
            names = {a.name: a for a in s.asserts}
            imm = names["multi.streams-immune-to-best-effort-load"]
            self.assertEqual(imm.severity, "SHALL")
            self.assertIn("802.1Q", imm.clause)
            hr = names["multi.best-effort-headroom"]
            self.assertEqual(hr.severity, "INFO")
            self.assertTrue(hr.clause.startswith("info:"))
            self.assertIn(A_NO_SEQ_MISMATCH.name, names)
            self.assertIn(A_NO_LATE_EARLY.name, names)
        # the coverage expectation now includes the inbound peer talkers
        self.assertIn("peer_talker", area_index_expectations()["multi"])
        ok, d = area_covers_every_index(build_plan(), "multi")
        self.assertTrue(ok, d)
        # the flowing verdict's stress flavour BITES and names the load
        v, d = check_concurrent_flowing(
            {"a": {"tx_ticks": 0, "rx_ticks": 0},
             "b": {"tx_ticks": 4, "rx_ticks": 4}},
            licensed=True, under_load="iperf3-tcp rx")
        self.assertEqual(v, "FAIL")
        self.assertIn("iperf3-tcp rx", d["why"])
        self.assertIn("SHALL NOT disturb", d["why"])
        # and the licence gates the stress flavour like everything else
        self.assertEqual(check_concurrent_flowing(
            {"a": {"tx_ticks": 0, "rx_ticks": 0}}, licensed=False,
            under_load="iperf3-tcp rx")[0], "SKIP")

    def test_multi_concurrent_flowing_bites_every_way(self) -> None:
        """One dead pair among many FAILs, a one-sided pair counts as dead, a pair
        unreadable on both sides SKIPs by name, and a MEASURED dead pair
        outranks a measurement gap on another pair."""

        def P(tx: int | None, rx: int | None) -> dict[str, int | None]:
            """One pair's packet deltas over the shared window."""
            return {"tx_ticks": tx, "rx_ticks": rx}
        # all pairs flowing together, licence open -> PASS, and the
        # comparison names itself as packets
        v, d = check_concurrent_flowing({"a": P(32000, 32000), "b": P(32001, 32000)},
                                        licensed=True, window_s=4)
        self.assertEqual(v, "PASS")
        self.assertIn("AVTPDU PACKETS", d["compares"])
        # ONE DEAD AMONG MANY - the defect this area exists for
        v, d = check_concurrent_flowing({"a": P(4, 4), "b": P(0, 0)},
                                        licensed=True)
        self.assertEqual(v, "FAIL")
        self.assertEqual(d["dead"], ["b"])
        self.assertEqual(d["flowing"], ["a"])
        # one-sided movement is a dead pair, not a flowing one
        v, d = check_concurrent_flowing({"a": P(4, 0)}, licensed=True)
        self.assertEqual(v, "FAIL")
        # the licence gates the whole question: SHUT and UNKNOWN are SKIP
        # and never a violation, exactly as the pairwise steps
        self.assertEqual(check_concurrent_flowing(
            {"a": P(0, 0)}, licensed=False)[0], "SKIP")
        v, d = check_concurrent_flowing({"a": P(0, 0)}, licensed=None)
        self.assertEqual(v, "SKIP")
        self.assertIn("--licence-status", d["why"])
        # a pair unreadable on BOTH sides SKIPs and NAMES itself...
        v, d = check_concurrent_flowing(
            {"a": P(4, 4), "b": P(None, None)}, licensed=True)
        self.assertEqual(v, "SKIP")
        self.assertEqual(d["unreadable"], ["b"])
        # ...but a MEASURED dead pair outranks a measurement gap
        v, d = check_concurrent_flowing(
            {"a": P(0, 0), "b": P(None, None), "c": P(4, 4)},
            licensed=True)
        self.assertEqual(v, "FAIL")
        self.assertEqual(d["dead"], ["a"])
        # the teardown flavour names the torn-down stream in the why
        v, d = check_concurrent_flowing({"a": P(0, 0)}, licensed=True,
                                        torn_down="artyt0-peerl0")
        self.assertEqual(v, "FAIL")
        self.assertIn("artyt0-peerl0", d["why"])
        self.assertIn("cross-stream-independence", d["why"])
        # and no pairs at all is a SKIP, not a vacuous pass
        self.assertEqual(check_concurrent_flowing({}, licensed=True)[0],
                         "SKIP")

    def test_multi_unbound_isolation_bites(self) -> None:
        """An UNBOUND Stream Input that ticks while its neighbours stream FAILs -
        the per-index aliasing/bleed defect class that index-0-only testing
        can never see - and a wrapped counter is INFO, not a pass."""
        v, d = check_unbound_static(
            {"peerl2": {"FRAMES_RX": 0, "MEDIA_LOCKED": 0}})
        self.assertEqual(v, "PASS")
        # an unbound index that TICKS is the per-index bleed defect
        v, d = check_unbound_static({"peerl2": {"FRAMES_RX": 37}})
        self.assertEqual(v, "FAIL")
        self.assertEqual(d["moved"]["peerl2.FRAMES_RX"], 37)
        self.assertIn("5.3.8.10", d["why"])
        # nothing to check / nothing readable / a wrap are not passes
        self.assertEqual(check_unbound_static({})[0], "SKIP")
        self.assertEqual(check_unbound_static(
            {"x": {"FRAMES_RX": None}})[0], "SKIP")
        self.assertEqual(check_unbound_static(
            {"x": {"FRAMES_RX": -5}})[0], "INFO")
        # a readable zero beside an unreadable neighbour still passes,
        # with the unreadable one NAMED
        v, d = check_unbound_static({"x": {"FRAMES_RX": 0},
                                     "y": {"FRAMES_RX": None}})
        self.assertEqual(v, "PASS")
        self.assertEqual(d["unreadable"], ["y"])

    def test_plan_steps_serialise(self) -> None:
        """Every plan step survives json.dumps and its assertion names agree with
        its clause map, so a runner can consume the plan without this module."""
        for s in build_plan():
            d = s.as_dict()
            json.dumps(d)
            self.assertEqual(set(d["assert_clauses"]), set(d["asserts"]))

    def test_exit_codes(self) -> None:
        """A SHALL failure exits 1, a RECOMMENDED-only one exits 2, and a SKIP
        alone exits 0 while still being counted in the summary."""
        ok = [verdict_record("a", "x", "PASS")]
        self.assertEqual(exit_code(ok), 0)
        soft = [verdict_record("a", "x", "FAIL",
                               severity="RECOMMENDED")]
        self.assertEqual(exit_code(soft), 2)
        hard = [verdict_record("a", "x", "FAIL")]
        self.assertEqual(exit_code(hard), 1)
        skip = [verdict_record("a", "x", "SKIP")]
        self.assertEqual(exit_code(skip), 0)
        self.assertEqual(summarise(hard)["FAIL"], 1)
        self.assertEqual(summarise(hard)["exit_code"], 1)

    def test_audio_is_never_forgotten(self) -> None:
        """The campaign is invalid without an identity step, a per-channel-DISTINCT
        pattern and a THD+N step that names the harness analyser: a pattern
        repeated across channels cannot fail on a swap."""
        # the campaign is invalid without an identity check, a per-channel
        # distinct pattern, and a THD+N gate
        ids = {s.sid for s in plan_audio()}
        self.assertTrue(any("identity" in i for i in ids))
        self.assertTrue(any("thdn" in i for i in ids))
        walk = [s for s in plan_audio() if "walking-tone" in s.sid][0]
        self.assertTrue(walk.args["per_channel_distinct"])
        thdn = [s for s in plan_audio() if s.sid == "audio.thdn"][0]
        self.assertIn("thdn.py", thdn.args["analyser"])
        self.assertTrue(any("coherent" in a.name for a in thdn.asserts))

def self_test() -> int:
    """The offline suite: every mixin's arms, exit 0 when all pass.

    Nothing here touches the wire.  What it audits is the PLAN and the
    GRADERS - the coverage each area owes, the assertion set each step
    carries, and that every verdict function can still say no - because a
    grader that cannot fail is the defect this campaign keeps finding.
    """
    import unittest

    class T(_CounterLawChecks, _StreamingLicenceChecks, _PlanContractChecks,
            _AreaContractChecks, _ReleasePlanChecks, _ReleaseSoakChecks, _ReleaseGateChecks,
            _ConcurrencyChecks, unittest.TestCase):
        """Every arm of the offline suite, under the one name the report uses."""

    r = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T))
    return 0 if r.wasSuccessful() else 1


# ------------------------------------------------------------------------ CLI --
def main() -> int:
    """The CLI: print the plan, the checklist, a coverage audit, or self-test.

    `--coverage-by-area` is the only arm that can exit non-zero on coverage,
    because it is the only one that asks each area about its OWN expectation
    instead of letting the matrix answer for everybody.
    """
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--plan", action="store_true", help="print the plan")
    ap.add_argument("--checklist", action="store_true",
                    help="print the human-action checklist")
    ap.add_argument("--areas", default=None,
                    help="comma list: " + ",".join(sorted(AREAS)))
    ap.add_argument("--coverage", action="store_true",
                    help="print the per-index coverage audit")
    ap.add_argument("--coverage-by-area", action="store_true",
                    help="the same audit PER AREA, with each area's own "
                         "expectation and what it is missing - the only form "
                         "that can say no about one area while another covers "
                         "everything")
    ap.add_argument("--dut", default=None,
                    help="topology override, key=value,...: "
                         + ",".join(sorted(DEVICE_SPEC_FIELDS)))
    ap.add_argument("--peer", default=None, help="same, for the peer device")
    ap.add_argument("--soak-duration-s", type=int, default=ReleaseSettings.soak_duration_s)
    ap.add_argument("--soak-interval-s", type=int, default=ReleaseSettings.soak_interval_s)
    ap.add_argument("--power-cycles", type=int, default=ReleaseSettings.power_cycles)
    ap.add_argument("--idle-cycles", type=int, default=ReleaseSettings.idle_cycles)
    ap.add_argument("--commit-cycles", type=int, default=ReleaseSettings.commit_cycles)
    ap.add_argument("--reset-cycles", type=int, default=ReleaseSettings.reset_cycles,
                    help="soft resets with power held on; #396 decision 2026-10-26")
    ap.add_argument("--persisted-items", default=",".join(ReleaseSettings.persisted_items),
                    help="comma-separated items persisted by the shipping image")
    ap.add_argument("--audio-duration-s", type=int, default=ReleaseSettings.audio_duration_s,
                    help="audio-integrity run inside the soak window")
    ap.add_argument("--audio-context-s", type=int, default=ReleaseSettings.audio_context_s,
                    help="longest gap between walks during the audio run")
    ap.add_argument("--restore-bound-s", type=int, default=ReleaseSettings.restore_bound_s,
                    help="provisional T0-to-automatic-AVTP bound; #396 round 2")
    ap.add_argument("--boot-margin-s", type=int, default=ReleaseSettings.boot_margin_s,
                    help="extra observation after the restore bound; never extends a pass deadline")
    ap.add_argument("--power-off-hold-s", type=int, default=ReleaseSettings.power_off_hold_s,
                    help="cold-cut discharge hold; recorded separately from T0 deadlines")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    dut = parse_device_spec(a.dut, ARTY) if a.dut else ARTY
    peer = parse_device_spec(a.peer, PEER) if a.peer else PEER
    areas = a.areas.split(",") if a.areas else None
    try:
        release = ReleaseSettings(
            soak_duration_s=a.soak_duration_s, soak_interval_s=a.soak_interval_s,
            power_cycles=a.power_cycles, idle_cycles=a.idle_cycles,
            commit_cycles=a.commit_cycles, reset_cycles=a.reset_cycles,
            persisted_items=tuple(a.persisted_items.split(",")),
            restore_bound_s=a.restore_bound_s, boot_margin_s=a.boot_margin_s,
            power_off_hold_s=a.power_off_hold_s,
            audio_duration_s=a.audio_duration_s, audio_context_s=a.audio_context_s,
            topology_explicit=_release_topology_explicit(a.dut, a.peer))
        plan = build_plan(areas, dut, peer, release=release)
    except ValueError as error:
        ap.error(str(error))
    if a.checklist:
        print(checklist_text(plan))
        return 0
    if a.coverage:
        print(json.dumps(plan_covers_every_index(plan, dut, peer), indent=2))
        return 0
    if a.coverage_by_area:
        out = {}
        for area in sorted({s.area for s in plan}):
            ok, d = area_covers_every_index(plan, area, dut, peer)
            out[area] = {"ok": ok, **d}
        print(json.dumps(out, indent=2))
        return 0 if all(v["ok"] for v in out.values()) else 1
    if a.json:
        print(json.dumps([s.as_dict() for s in plan], indent=2))
        return 0
    # default: the plan as a table
    for s in plan:
        flag = "HUMAN" if s.needs_human else "     "
        print(f"{flag} {s.area:8s} {s.op:22s} {s.sid}")
        print(f"           asserts: {', '.join(x.name for x in s.asserts)}")
        if s.op in RELEASE_REQUIRED_ASSERTS or s.op == RELEASE_CONTROL_OP:
            print(f"           args: {json.dumps(s.args, sort_keys=True)}")
    print(f"\n{len(plan)} steps, "
          f"{sum(len(s.asserts) for s in plan)} assertions, "
          f"{len(human_steps(plan))} need a human")
    return 0


if __name__ == "__main__":
    sys.exit(main())
