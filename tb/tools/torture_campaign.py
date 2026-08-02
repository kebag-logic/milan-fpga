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
  Milan v1.2 Table 5.4 / 5.6 wording that bites - FRAMES_TX and FRAMES_RX are
    "Incremented at the end of every observation interval during which at least
    one Stream Data AVTPDU has been transmitted/received", the interval being
    "implementation-specific and shall be less than or equal to 1 second".
    IEEE 1722.1-2021 Table 7-157/7-159 define the SAME symbols as PER-FRAME
    ("Increments on each Stream data AVTPDU received").  The two readings differ
    by the frame rate - 8000x at class A - so the campaign asserts a RATE BAND
    per reading and records which reading the device implements instead of
    hardcoding one.  Getting this wrong once already produced a "FRAMES_TX is
    8000x off" finding that was a units error in the test.
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
from dataclasses import dataclass, field, asdict
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


def counters_valid_mask(names, block) -> int:
    """The on-the-wire counters_valid mask for `names` within `block`."""
    m = 0
    for n in names:
        m |= 1 << block.index(n)
    return m


def decode_counters_arrays(counters_valid: int, raw, block) -> dict:
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


def decode_counters_payload(payload: bytes, block) -> dict:
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


def check_tv_tnv(decoded: dict, tolerance: int = 2) -> tuple:
    """TIMESTAMP_VALID + TIMESTAMP_NOT_VALID == FRAMES_RX - but only under one
    of the two readings of FRAMES_RX, and this returns WHICH.

    IEEE 1722.1-2021 Table 7-157 defines all three PER FRAME: TIMESTAMP_VALID
    "Increments on receipt of a Stream data AVTPDU with the tv bit set",
    TIMESTAMP_NOT_VALID on tv cleared, FRAMES_RX "Increments on each Stream
    data AVTPDU received".  Under that reading the identity is exact.

    Milan v1.2 Table 5.6 redefines FRAMES_RX as an INTERVAL counter:
    "Incremented at the end of every observation interval during which at least
    one Stream Data AVTPDU has been received on this Stream Input.  The duration
    of the observation interval is implementation-specific and shall be less
    than or equal to 1 second."  Under THAT reading FRAMES_RX is smaller than
    TV + TNV by the frame rate - about 8000:1 at class A - and the identity does
    not hold, without either counter being wrong.

    So this reports PASS with reading="1722.1-per-frame" when the identity
    holds, INFO with reading="milan-interval" when the ratio is consistent with
    the interval reading, and FAIL only when it is neither.  Deciding which
    reading a device implements by assertion rather than by measurement is how a
    correct interval counter gets filed as an 8000x defect.

    AND THE VACUITY GUARD, which is the whole reason this returns SKIP at all.
    Milan v1.2 5.3.8.10: "The PAAD-AE shall reset all of these counters to zero
    each time the Stream Input changes its state from not bound to bound."  A
    snapshot taken immediately after a bind therefore reads 0/0/0 on a CORRECT
    device - and abs(0 - 0) <= tolerance is a DEFINITE PASS that also concludes
    which of the two readings the device implements, from zero samples.  That
    was the only state this function was ever called in.  All three at zero is
    now SKIP: nothing was measured, so nothing may be concluded.
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
    if abs(total - frx) <= tolerance:
        return ("PASS", {"tv_plus_tnv": total, "frames_rx": frx,
                         "reading": "1722.1-per-frame"})
    if frx and total > frx:
        return ("INFO", {"tv_plus_tnv": total, "frames_rx": frx,
                         "ratio": total / frx,
                         "reading": "milan-interval",
                         "note": "FRAMES_RX is an interval tick per Milan "
                                 "Table 5.6, so it is smaller than the frame "
                                 "count by the frame rate; the identity is a "
                                 "1722.1 Table 7-157 property only"})
    return ("FAIL", {"tv_plus_tnv": total, "frames_rx": frx,
                     "why": "FRAMES_RX exceeds TV+TNV, which neither reading "
                            "permits: every frame is counted by exactly one of "
                            "the two tv tallies"})


def frames_rate_reading(rate_per_s: float, nominal_frame_rate: float = 8000.0,
                        max_interval_s: float =
                        MILAN_MAX_OBSERVATION_INTERVAL_S) -> dict:
    """Which reading a measured FRAMES_TX/FRAMES_RX rate is consistent with, and
    the observation interval it implies.

    band is "per-frame", "interval" or "neither", and "neither" is reserved for
    the two things the clauses genuinely exclude:

      * rate == 0 - nothing moved at all, under either reading;
      * an IMPLIED INTERVAL longer than a second - Milan v1.2 Table 5.4/5.6 say
        the interval "shall be less than or equal to 1 second", so a counter
        ticking at 0.4/s is claiming a 2.5 s interval and that is the only way
        an interval reading can be non-conformant.

    Everything between is an interval reading, because the clause bounds the
    interval from ABOVE ONLY.  The earlier band table mapped 4.001/s .. 3999/s
    to "neither" and so turned a conformant 5 ms interval - 200 ticks/s - into a
    SHALL failure.  `max_interval_s` is the Milan ceiling and IS used; it was a
    dead parameter before.
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
    if implied is not None and implied <= max_interval_s:
        return {"band": "interval", "rate_per_s": rate_per_s,
                "implied_interval_s": implied,
                "why": f"Milan v1.2 Table 5.4/5.6 interval reading; the implied "
                       f"observation interval is {implied:.4g} s, within the "
                       f"{max_interval_s:g} s ceiling"}
    return {"band": "neither", "rate_per_s": rate_per_s,
            "implied_interval_s": implied,
            "why": f"the implied observation interval is {implied:.4g} s, and "
                   f"Milan v1.2 Table 5.4/5.6 require it to be less than or "
                   f"equal to {max_interval_s:g} s"}


def frames_rate_band(rate_per_s: float, nominal_frame_rate: float = 8000.0,
                     max_interval_s: float =
                     MILAN_MAX_OBSERVATION_INTERVAL_S) -> str:
    """`frames_rate_reading()["band"]`, kept as the short form for callers that
    only need the label."""
    return frames_rate_reading(rate_per_s, nominal_frame_rate,
                               max_interval_s)["band"]


def check_no_growth(before: dict, after: dict, keys, *,
                    window_s: Optional[float] = None) -> tuple:
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
#: WHICH COUNTER MAY BE COMPARED WITH WHICH.  This is the semantic trap that
#: already cost this project a bogus "8000x off" finding, so it is encoded as
#: data and enforced by a raising function rather than written in a comment.
#:
#:   IEEE 1722.1-2021 Table 7-153 AVB_INTERFACE: FRAMES_TX "Total number of
#:     frames sent out of this interface", FRAMES_RX "Total number of frames
#:     received through this interface" - RAW TOTALS since boot.
#:   Milan v1.2 Table 5.4 STREAM_OUTPUT FRAMES_TX / Table 5.6 STREAM_INPUT
#:     FRAMES_RX: "Incremented at the end of every observation interval during
#:     which at least one Stream Data AVTPDU has been transmitted/received" -
#:     OBSERVATION-INTERVAL TICKS, <= 1 s each.
#:
#: The two carry the SAME NAME and differ by the frame rate, so a frame-accurate
#: cross-device comparison may use ONLY the first group.
FRAME_ACCURATE_SOURCES = ("avb_interface", "rmon", "nic", "pcap")
INTERVAL_SOURCES = ("stream_input", "stream_output")


class CounterSemanticError(ValueError):
    """Raised when a frame-accurate comparison is attempted against an
    observation-interval counter.  Making this an exception rather than a
    comment is what stops the trap being reintroduced: the comparison cannot be
    EXPRESSED, so it cannot be written by accident."""


def assert_frame_accurate(source: str) -> str:
    """Guard for every cross-device FRAME COUNT comparison."""
    s = str(source)
    if s in INTERVAL_SOURCES:
        raise CounterSemanticError(
            f"{s} FRAMES_TX/FRAMES_RX is an OBSERVATION-INTERVAL tick (Milan "
            f"v1.2 Table 5.4/5.6, <= 1 s each), not a frame count, so it cannot "
            f"be compared frame-for-frame with another side.  Use one of "
            f"{list(FRAME_ACCURATE_SOURCES)} - the AVB_INTERFACE totals (IEEE "
            f"1722.1-2021 Table 7-153), the DUT RMON lanes, the test machine's "
            f"NIC statistics or the pcap count - or compare in INTERVAL terms "
            f"with interval_ticks_agree()")
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
    "interval_ticks": 2,
    "interval_ticks_reason":
        "Milan v1.2 Table 5.4/5.6 leave the interval implementation-specific up "
        "to 1 s, and the window edges cut a partial interval at each end, so "
        "two ticks of disagreement is the window and not the device",
    "capture_edge_frames": 8000,
    "capture_edge_reason":
        "tcpdump starts and stops on its own schedule, so a capture can miss up "
        "to one second at each edge relative to a counter window",
    "perframe_floor_ticks": 600,
    "perframe_min_ticks_per_s": 150,
    "perframe_reason":
        "an observation interval is <= 1 s (Milan v1.2 Table 5.4/5.6) but has "
        "no LOWER bound, so interval-conformance cannot be a 1-tick-per-second "
        "test; 150 ticks/s (a 6.7 ms interval; 600 over the 4 s default "
        "window) is 50x above the 1-3/s band every conformant implementation "
        "on this bench sits in, while a per-frame deviant at class A rate "
        "reads ~8000/s - the two populations never meet, so a side above the "
        "floor is keeping the IEEE 1722.1-2021 Table 7-157 per-frame reading",
}


def interval_ticks_agree(talker_delta: Optional[int],
                         listener_delta: Optional[int], *,
                         tolerance: int = None,
                         window_s: float = None,
                         self_loop: bool = False) -> tuple:
    """Do the talker's and the listener's OBSERVATION-INTERVAL ticks agree?

    Named for what it is: this compares INTERVAL TICKS and never frames.  While
    one stream runs continuously both sides tick once per interval, so the two
    deltas are the same order (~1 per second at a 1 s interval); when it does not
    run BOTH must be static.  Milan v1.2 Table 5.4/5.6 leave the interval
    implementation-specific, so the two sides may legitimately differ in
    interval LENGTH - which is why this asserts agreement about MOVEMENT and a
    small tick difference, not equality of counts.

    EVERY PARTICIPANT IS A MEASURED PARTY.  A side whose delta exceeds what any
    sub-second observation interval could tick over the window is not keeping
    the Milan interval semantics at all - it is counting per frame (the IEEE
    1722.1-2021 Table 7-157 reading; the PEER's known deviation, settled
    2026-07-30).  That is a finding AGAINST THAT SIDE, returned in
    d["peer_findings"] for the caller to attribute by name as
    xside.peer-counter-semantics, while the pair verdict PASSes for the
    interval-conformant side instead of smearing it with a FAIL it did not
    earn.  Movement still binds both sides regardless of semantics: one side
    moving while the other is static stays the original FAIL.  Two per-frame
    sides leave no interval-conformant baseline, so that is a SKIP plus one
    finding per side - never a silent pass for either.
    """
    tol = XSIDE_TOLERANCE["interval_ticks"] if tolerance is None else tolerance
    if talker_delta is None or listener_delta is None:
        return ("SKIP", {"why": "one side's interval counter was unreadable",
                         "talker_interval_ticks": talker_delta,
                         "listener_interval_ticks": listener_delta})
    floor = XSIDE_TOLERANCE["perframe_floor_ticks"]
    if window_s:
        floor = max(floor,
                    XSIDE_TOLERANCE["perframe_min_ticks_per_s"] * window_s)
    ticks = {"talker": talker_delta, "listener": listener_delta}
    sem = {r: ("per-frame" if ticks[r] > floor else "interval")
           for r in ("talker", "listener")}
    deviant = [r for r in ("talker", "listener") if sem[r] == "per-frame"]
    d = {"talker_interval_ticks": talker_delta,
         "listener_interval_ticks": listener_delta,
         "tolerance_ticks": tol,
         "tolerance_reason": XSIDE_TOLERANCE["interval_ticks_reason"],
         "compares": "OBSERVATION INTERVALS (Milan Table 5.4/5.6), NOT frames",
         "talker_semantics": sem["talker"],
         "listener_semantics": sem["listener"],
         "perframe_bound_ticks": floor}
    if window_s:
        d["window_s"] = window_s
    if deviant:
        d["peer_findings"] = [
            {"role": r, "ticks": ticks[r],
             "ticks_per_s": (round(ticks[r] / window_s, 1)
                             if window_s else None),
             "perframe_bound_ticks": floor,
             "counter": {"talker": "FRAMES_TX (Milan v1.2 Table 5.4)",
                         "listener": "FRAMES_RX (Milan v1.2 Table 5.6)"}[r],
             "why": "this side's counter advanced far beyond what any <= 1 s "
                    "observation interval can tick over the window, so it is "
                    "keeping the IEEE 1722.1-2021 Table 7-157 per-frame "
                    "reading, not the Milan interval one"}
            for r in deviant]
    if (talker_delta > 0) != (listener_delta > 0):
        if self_loop and talker_delta > 0:
            # A single-port device bound to ITS OWN stream: the frames egress
            # the one port, and IEEE 802.1Q-2018 8.6.1 forbids the bridge
            # from forwarding a frame out the port it arrived on, so the
            # listener can never receive them.  Wire-proven on ax-rv32-e
            # triage (2026-08-02): 8000/s left the DUT port at the tap,
            # zero came back, listener FRAMES_RX and per-frame TV/TNV all
            # static - the honest zero.  The talker ticking IS conformant
            # (its Listener Ready stands, Milan v1.2 5.3.7.3), so one-sided
            # movement here is the topology, not a device.  A listener that
            # DID move on a self-loop falls through to the normal compare -
            # that would mean the network delivered after all.
            d["why"] = ("self-loop pair on a single-port DUT: the bridge "
                        "never returns a frame to its ingress port (802.1Q "
                        "8.6.1), so the listener side is structurally "
                        "unreachable and only the talker's licensed ticking "
                        "is observable")
            d["self_loop"] = True
            return ("SKIP", d)
        d["why"] = ("one side ticked and the other did not: a one-sided claim "
                    "of streaming is itself the defect (Milan v1.2 5.3.7.3 "
                    "licenses the talker only while a Listener Ready is being "
                    "received, so the two sides move together or neither does)")
        return ("FAIL", d)
    if len(deviant) == 2:
        d["why"] = ("both sides tick per-frame, so there is no interval-"
                    "conformant baseline to agree with; each side's deviation "
                    "is its own attributed finding, never a silent pass")
        return ("SKIP", d)
    if deviant:
        conf = "listener" if deviant == ["talker"] else "talker"
        d["attributed"] = True
        d["conformant_role"] = conf
        d["why"] = (f"the {conf} ticked interval-conformant and both sides "
                    f"moved; the {deviant[0]}'s per-frame counter semantics is "
                    f"the {deviant[0]}'s own finding "
                    f"(xside.peer-counter-semantics), not a pair disagreement "
                    f"- a generic pair-FAIL would smear the conformant side")
        return ("PASS", d)
    if abs(talker_delta - listener_delta) > tol:
        d["why"] = ("the two sides disagree by more than the window edges "
                    "explain; both are interval counters so the difference is "
                    "intervals, not frames")
        return ("FAIL", d)
    return ("PASS", d)


def check_concurrent_flowing(pair_ticks, *, licensed=None, torn_down=None,
                             under_load=None) -> tuple:
    """Do ALL concurrently bound pairs move TOGETHER, in INTERVAL terms?

    `pair_ticks` maps a pair label to {"tx_ticks": d, "rx_ticks": d} - the
    talker's FRAMES_TX and the listener's FRAMES_RX OBSERVATION-INTERVAL deltas
    (Milan v1.2 Table 5.4/5.6) over ONE shared window, never frames, and never
    one window per pair: a serial walk cannot see cross-stream interference,
    which is the defect class this verdict exists for (CBS shaping under
    aggregate load, the multi-slot rings, a per-index datapath fault).  A side
    that could not be read is None.

    The licence gates the whole question exactly as it gates the pairwise
    frames-advance verdicts: Milan v1.2 5.3.7.3 licenses each Stream Output by
    its OWN Talker Advertise + Listener Ready conjunction, so with the gate
    SHUT or UNKNOWN every bound talker may be correctly silent and the verdict
    is SKIP, never a violation.

    With the licence OPEN:
      * every readable pair moving on every readable side -> PASS;
      * ANY readable pair static - including one-sided movement, tx without rx
        - -> FAIL naming the dead pairs.  A measured dead pair outranks a
        measurement gap on another pair;
      * pairs unreadable on BOTH sides are named; if nothing else is dead the
        verdict is SKIP, because "every pair flows" cannot be certified
        through a hole.

    `torn_down` names the pair whose UNBIND preceded this window, for the
    staged-teardown flavour: the survivors kept their own licences, so a
    neighbour going dead right after an unbind is the cross-stream-independence
    defect.

    `under_load` names the best-effort load running during the window, for the
    stress flavour: 802.1Q-2018 8.6.8.2/34 put admitted SR class A streams in
    a reserved, credit-shaped queue ABOVE best-effort, so BE load SHALL NOT
    disturb them - coexistence is the design point of the reservation itself.
    (This is a different claim from the adverse-practice storm entries, which
    are line-rate hostile traffic and stay RECOMMENDED; a cooperative BE load
    inside the unreserved remainder is what the shaper exists to absorb.)
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
              "compares": "OBSERVATION INTERVALS (Milan Table 5.4/5.6), "
                          "NOT frames"}
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
    if unreadable:
        detail["why"] = (f"{unreadable} could not be read on either side, so "
                         f"'every pair flows{ctx}' cannot be certified; this "
                         f"is NOT a failure of the pairs that answered")
        return ("SKIP", detail)
    return ("PASS", detail)


def check_unbound_static(deltas) -> tuple:
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


#: The test machine's own loss lanes.  /sys/class/net/<iface>/statistics/ names
#: (net_device_stats; Documentation/networking/statistics.rst).
#: ONLY counters that can falsify this instrument's readings belong here:
#: rx_missed/over/fifo/errors mean a frame never reached rx_packets, and the
#: tx lanes mean this host's own injections failed.
NIC_LOSS_KEYS = ("tx_dropped", "rx_errors", "tx_errors",
                 "rx_missed_errors", "rx_over_errors", "rx_fifo_errors")
#: rx_dropped is NOT a loss lane for this instrument: it counts kernel demux
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
                                "expected /sys/class/net/<iface>/statistics/"})
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


def cross_side_growth(sides: dict, *, licensed: Optional[bool] = None,
                      registered_sides=None) -> list:
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
    out = []
    for _label, s in sides.items():
        assert_frame_accurate(s["source"])      # refuses an interval counter
    named = sorted(sides)
    unreadable = sorted(l for l, s in sides.items() if s.get("frames") is None)
    tol = XSIDE_TOLERANCE["snapshot_skew_frames"]

    def rec(name, verdict, **detail):
        detail.setdefault("sides_used", named)
        detail.setdefault("sides_unreadable", unreadable)
        detail.setdefault("sources", {l: sides[l]["source"] for l in named})
        detail.setdefault("devices", {l: sides[l].get("device") for l in named})
        detail.setdefault("frames", {l: sides[l].get("frames") for l in named})
        out.append((name, verdict, detail))

    talkers = {l: s for l, s in sides.items() if s["role"] == "talker"}
    listeners = {l: s for l, s in sides.items() if s["role"] == "listener"}
    wires = {l: s for l, s in sides.items() if s["role"] == "wire"}

    # (1) a one-sided claim of streaming is a defect in itself
    if unreadable:
        rec("xside.growth-corroborated", "SKIP",
            why=f"{unreadable} could not be read, so corroboration is "
                f"impossible; this is NOT a failure of the sides that answered")
    elif not talkers or not (listeners or wires):
        rec("xside.growth-corroborated", "SKIP",
            why="fewer than two independent sides were supplied, so there is "
                "nothing to corroborate against")
    else:
        moving = {l: s["frames"] > 0 for l, s in sides.items()
                  if s["role"] in ("talker", "listener", "wire")}
        agree = len(set(moving.values())) == 1
        rec("xside.growth-corroborated", "PASS" if agree else "FAIL",
            moving=moving, tolerance_frames=tol,
            tolerance_reason=XSIDE_TOLERANCE["snapshot_skew_reason"],
            why=None if agree else
            "the sides disagree about whether this stream is running.  Milan "
            "v1.2 5.3.7.3 ties the talker's streaming to the listener's "
            "declaration, so a talker that says it is streaming while the "
            "listener and the wire see nothing is the defect - and so is the "
            "reverse")

    # (2) an unlicensed stream must move on NO side
    if licensed is None:
        rec("xside.unlicensed-silent-everywhere", "SKIP",
            why="the streaming licence (LWSRP_STATUS bit 8) is unknown, so "
                "'must be silent everywhere' has no premise")
    elif licensed:
        rec("xside.unlicensed-silent-everywhere", "SKIP",
            why="the stream IS licensed, so this invariant does not apply")
    elif not any(s.get("frames") is not None for s in sides.values()
                 if s["role"] in ("talker", "listener")):
        rec("xside.unlicensed-silent-everywhere", "SKIP",
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
            rec("xside.unlicensed-silent-everywhere", "INFO", movers=movers,
                why="only the interface-global wire counter moved while every "
                    "readable device side was silent: ambient traffic on the "
                    "test host's port cannot be attributed to this stream's "
                    "gate, so this is not admissible evidence either way")
        else:
            rec("xside.unlicensed-silent-everywhere",
                "PASS" if not attributable else "FAIL", movers=movers,
                why=None if not attributable else
                "frames moved with the stream gate SHUT: Milan v1.2 5.3.7.3 "
                "licenses streaming only while a Listener Ready or Listener "
                "Ready Failed is being received, so these frames are "
                "unreserved")

    # (3) a listener that counts more than was sent
    if talkers and listeners and not unreadable:
        t = max(s["frames"] for s in talkers.values())
        worst = max(listeners.items(), key=lambda kv: kv[1]["frames"])
        ok = worst[1]["frames"] <= t + tol
        rec("xside.listener-not-more-than-talker", "PASS" if ok else "FAIL",
            talker_frames=t, listener=worst[0],
            listener_frames=worst[1]["frames"], tolerance_frames=tol,
            tolerance_reason=XSIDE_TOLERANCE["snapshot_skew_reason"],
            why=None if ok else
            "a listener counted more frames than the talker sent, beyond the "
            "snapshot skew: either a second talker shares this stream_id (a "
            "DMAC/stream_id collision) or one of the two counters is wrong")
    else:
        rec("xside.listener-not-more-than-talker", "SKIP",
            why="needs a readable talker side and a readable listener side")

    # (4) PRUNING: frames must be ABSENT where nothing registered
    if registered_sides is None:
        rec("xside.absent-where-not-registered", "SKIP",
            why="no registration set supplied, so where traffic must be ABSENT "
                "is unknown; pass the sides that declared a Listener attribute")
    else:
        reg = set(registered_sides)
        leaks = {l: s["frames"] for l, s in sides.items()
                 if l not in reg and s["role"] in ("listener", "bystander")
                 and (s.get("frames") or 0) > 0}
        rec("xside.absent-where-not-registered",
            "PASS" if not leaks else "FAIL", registered=sorted(reg),
            leaks=leaks,
            why=None if not leaks else
            "stream frames reached an interface that never registered as a "
            "listener for them; this bench has measured untagged frames "
            "flooding every port at 500 pps, so absence is asserted and never "
            "assumed")
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
    "IEEE 1722.1-2021 Table 7-157: TIMESTAMP_VALID 'Increments on receipt of a "
    "Stream data AVTPDU with the tv bit set' and TIMESTAMP_NOT_VALID on tv "
    "cleared, so TV + TNV == FRAMES_RX exactly when FRAMES_RX is the "
    "per-frame 1722.1 reading; under the Milan interval reading the identity "
    "does not hold and the assertion records which reading is in force")
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
    "counter advances exactly when the tu bit is set on the wire; tu = 1 is "
    "CORRECT for a board whose gPTP has not leased clock validity, so this "
    "assertion compares the counter to the WIRE and never to a wish")
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
    "statistics or the pcap count - because the stream-descriptor FRAMES_TX / "
    "FRAMES_RX are <= 1 s observation-interval ticks and not frame counts")
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
    "Milan v1.2 Table 5.4 STREAM_OUTPUT FRAMES_TX and Table 5.6 STREAM_INPUT "
    "FRAMES_RX are both 'incremented at the end of every observation interval "
    "during which at least one Stream Data AVTPDU has been "
    "transmitted/received', the interval being implementation-specific and <= 1 "
    "s.  So the two sides are compared in INTERVAL TERMS - both moving or both "
    "static - and NEVER frame for frame.  The assertion name says 'interval' so "
    "nobody later reads it as a frame count")
A_XSIDE_PEER_SEMANTICS = AssertSpec(
    "xside.peer-counter-semantics",
    "Milan v1.2 Table 5.4 FRAMES_TX / Table 5.6 FRAMES_RX increment 'at the "
    "end of every observation interval', the interval <= 1 s - a counter "
    "advancing at wire frame rate is keeping the IEEE 1722.1-2021 Table 7-157 "
    "per-frame semantics instead.  Every participant is a measured party: the "
    "deviation is attributed BY NAME to the side that ticks per-frame, with "
    "its measured rate against the clause bound, as that side's own finding - "
    "never smeared onto the conformant side of the pair as a generic pair "
    "disagreement, and never silently passed")
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
    "kernel demux drops such as unhandled MVRP, not capture loss).  A saturated "
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
    A_LOCK_INVARIANT, A_TALKER_INVARIANT, A_TV_TNV,
    A_NO_LATE_EARLY, A_NO_SEQ_MISMATCH, A_NO_UNSUPPORTED, A_TU_HANDLING,
    A_XSIDE_ERRORS_STATIC, A_INSTRUMENT_LOSSLESS)

#: The assertion set the LICENCE-OWNING step owes: the licence reading itself,
#: then everything that is only meaningful once the gate is known to be open,
#: including the cross-participant corroboration.
LICENSED_STREAMING_ASSERTS = (
    A_SRP_LICENCE, A_STREAM_ON_BIND_ALONE, A_TX_TICKING, A_RX_TICKING,
    A_XSIDE_CORROBORATED, A_XSIDE_UNLICENSED_SILENT, A_XSIDE_NOT_MORE,
    A_XSIDE_PRUNED, A_XSIDE_INTERVAL_AGREE, A_INSTRUMENT_LOSSLESS)

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
    "Ready), so with the gate open EVERY bound pair's interval counters "
    "(Table 5.4 FRAMES_TX / Table 5.6 FRAMES_RX) advance together over one "
    "shared window.  One stream going static while its neighbours flow is the "
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
    #: come from /sys/class/net/<iface>/statistics/ and from the capture.
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
    #: can never carry the secondaries.  The PEER on this bench serves ten
    #: STREAM_INPUTs that are five interleaved pairs - primaries at the EVEN
    #: indices (USER 2026-07-31).
    #:
    #: This has to be stated rather than probed.  ACMP answers SUCCESS on a
    #: secondary descriptor whether or not the secondary network exists (all
    #: of peer 0..7 returned SUCCESS on 2026-07-31), and the device does not
    #: serve GET_NAME (status 7 NOT_SUPPORTED), so neither the bind status nor
    #: the descriptor names can separate them at runtime.  Binding a secondary
    #: therefore looks exactly like a working bind that never carries audio -
    #: a DUT defect that is not one, which is the most expensive kind of
    #: fake red this campaign can produce.
    talker_index_set: Optional[tuple] = None
    listener_index_set: Optional[tuple] = None

    def talker_indices(self, include_crf=True) -> list:
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

    def listener_indices(self, include_crf=True) -> list:
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

    def stream_ids(self, include_crf=True) -> list:
        return [self.stream_id(i) for i in self.talker_indices(include_crf)]

    def is_crf_talker(self, i: int) -> bool:
        return self.crf_out is not None and i == self.crf_out

    def is_crf_listener(self, i: int) -> bool:
        return self.crf_in is not None and i == self.crf_in


#: The bench shape.  The Arty is the DUT; the PEER is the Milan-validated
#: reference device, so IT is the independent oracle (methodology L4/L5) and its
#: refusals are evidence about us, not bugs in it.
ARTY = Device(name="arty", entity_id="020000fffe000002", mac="020000000002",
              talkers=4, listeners=4, crf_out=4, crf_in=4,
              formats=("0205022001006000", "0205022000806000"),
              role="dut")
#: The PEER is REDUNDANT (Milan v1.2 seamless redundancy): its ten
#: STREAM_INPUTs are five interleaved pairs, a (p) primary at each even index
#: and its (s) secondary at the odd one.  This bench has ONE network, so the
#: secondaries can never carry a stream - and they still answer ACMP with
#: SUCCESS, so binding them yields a connection that never passes audio and
#: reads as a DUT defect.  USER 2026-07-31.  Override with
#: --peer 'listener_index_set=...' on a bench that has both networks.
PEER = Device(name="peer", entity_id="3cc0c60102030000", mac="3cc0c6010203",
               talkers=4, listeners=10, formats=("0205022001006000",),
               listener_index_set=(0, 2, 4, 6, 8),
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
        d = asdict(self)
        d["asserts"] = [a.name for a in self.asserts]
        d["assert_clauses"] = {a.name: a.clause for a in self.asserts}
        d["assert_severity"] = {a.name: a.severity for a in self.asserts}
        return d


def _pair_steps(prefix, area, tk: Device, ti: int, ls: Device, li: int,
                fmt: Optional[str]) -> list:
    """One talker index into one listener index: set the format, bind, verify,
    unbind.  The CRF pair carries its own format expectation."""
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
    steps.append(_start_if_needed_step(sid, area, tk, ti, ls, li))
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


def _start_if_needed_step(sid: str, area: str, tk: Device, ti: int,
                          ls: Device, li: int) -> "Step":
    """The step that OWNS the Milan 5.3.7.3 licence question.

    It is a separate step from the bind on purpose.  The bind can only ask
    "did the ACMP exchange succeed"; whether a silent talker is a defect needs
    the SRP licence, which is a different reading from a different place, and
    mixing the two is what made a conformant bound-but-ungated talker read as a
    SHALL failure.  It also carries the LISTENER, because the frames-advance
    verdict is cross-participant: the talker's claim is corroborated on the
    listener and on the test machine or it is not a fact.
    """
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
            steps += _pair_steps("out", "matrix", dut, ti, peer, li, fmt)
    if both_directions:
        for ti in peer.talker_indices():
            for li in dut.listener_indices():
                steps += _pair_steps("ret", "matrix", peer, ti, dut, li, fmt)
    # ---- intra-DUT loopback: the DUT's own talkers into its own listeners.
    # This is the only pair set that needs no peer at all, so it is what keeps
    # the campaign meaningful while the reference device is out of the rack.
    for ti in dut.talker_indices():
        for li in dut.listener_indices():
            steps += _pair_steps("loop", "matrix", dut, ti, dut, li, fmt)
    return steps


def _multi_pair(tk: Device, ti: int, ls: Device, li: int,
                fmt: Optional[str]) -> dict:
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
    only (the PEER serves 0/2/4/6/8; the (s) secondaries can never carry a
    stream on a one-network bench) - so nothing here is hardcoded to any
    device.  Talkers are the DUT's AAF set, assigned cyclically so every peer
    listener is fed even when the DUT has fewer talkers than the peer has
    listeners; a talker reused that way carries two listeners on ONE stream,
    which IEEE 1722.1-2021 8.2.2.6.2.1 permits.  On the AX 8x8 against the
    PEER this is a plain 1:1 zip: t0..t4 -> l0/2/4/6/8.
    """
    tks = dut.talker_indices(include_crf=False)
    lss = peer.listener_indices(include_crf=False)
    if not tks or not lss:
        return []
    return [_multi_pair(dut, tks[i % len(tks)], peer, li, fmt)
            for i, li in enumerate(lss)]


def _multi_pairs_selfloop(dut: Device, fmt) -> list:
    """The DUT's own talkers into its own listeners, tN -> lN, concurrently.

    This is the set that stresses the DUT on BOTH sides at once - every
    packetizer and every depacketizer live in the same fabric - and, like the
    matrix's loop prefix, it needs no peer at all.
    """
    tks = dut.talker_indices(include_crf=False)
    lss = dut.listener_indices(include_crf=False)
    return [_multi_pair(dut, t, dut, li, fmt) for t, li in zip(tks, lss)]


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
            out.append(_multi_pair(dut, ti, peer, plss[pi], fmt))
            pi += 1
        elif di < len(dlss):
            out.append(_multi_pair(dut, ti, dut, dlss[di], fmt))
            di += 1
    return out


def _multi_pairs_stress(dut: Device, peer: Device, fmt) -> list:
    """EVERYTHING the shapes allow, concurrently - the maximal stream set.

    (a) every DUT AAF talker outbound: the peer's reachable listeners first
        (cyclic when the DUT has fewer talkers than the peer has listeners,
        exactly as the primaries set), then SELF-LOOPS to fill the talkers
        the peer cannot absorb - on the AX 8x8 against the PEER that is
        t0..t4 -> the five primaries and t5..t7 looped home;
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
        out += [_multi_pair(dut, tks[i % len(tks)], peer, li, fmt)
                for i, li in enumerate(plss)]
    free = list(dlss)
    for ti in tks[len(plss):]:
        if not free:
            break
        out.append(_multi_pair(dut, ti, dut, free.pop(0), fmt))
    for ti in peer.talker_indices(include_crf=False):
        if not free:
            break
        out.append(_multi_pair(peer, ti, dut, free.pop(0), fmt))
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
        for direction, what in (
                ("rx", "host -> DUT best-effort TCP: RX stress on the "
                       "RSC-less ingress path"),
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
                            "(busybox rootfs); the RX fallback is a blind "
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
        (on the AX 8x8 against the PEER: t0..t4 -> l0/2/4/6/8);
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
            f"churn.implicit-rebind.l{li}", "churn", peer, t0, dut, li))
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
            f"churn.implicit-rebind.l{li}.rebind", "churn", peer, t1, dut, li))
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
                f"churn.bind-while-streaming.{i}", "churn", dut, 0, peer, li))
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


def plan_audio(dut: Device = ARTY, peer: Device = PEER) -> list:
    """AUDIO IS NEVER FORGOTTEN.  Three shapes, because presence testing cannot
    tell a correct channel map from a crossed one - and EVERY INDEX, because
    index 0 is the least representative index on this fabric.

    The index-0-only version of this area was the audio half of the same defect
    the matrix area exists to prevent: the walking tone was captured on talker 0
    only, the loop ran through peer listener 0 and peer talker 0 only, and the
    coverage audit could not see it because it was computed over the WHOLE plan,
    where the matrix's full coverage masked the audio area entirely.  Coverage is
    now audited PER AREA (plan_coverage_by_area) and this walks every index.
    """
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
             {"source": "pcm_ring_dump", "rate_hz": 48000, "f0_hz": 1000,
              "channels": 2, "accept_dbfs": -120.0,
              "analyser": "harness/milanharness/thdn.py"},
             asserts=(AssertSpec("audio.thdn.worst-channel",
                                 "USER acceptance: THD+N <= -120 dBFS end to "
                                 "end; the digital source itself measures "
                                 "-147.99 dBFS, so the wire+ring path must add "
                                 "nothing"),
                      AssertSpec("audio.thdn.coherent-not-windowed",
                                 "the pilot tone is exact-period (48 samples = "
                                 "1 kHz at 48 kHz), so a capture truncated to "
                                 "whole periods is coherently sampled; "
                                 "applying a window spreads the fundamental "
                                 "into neighbouring bins which the residual "
                                 "then counts as distortion - it MANUFACTURES "
                                 "the number it is supposed to measure")),
             clause="reuses harness/milanharness/thdn.py - do not reimplement",
             note="numpy is required for this one step and nowhere else"))
    return steps


# ------------------------------------------------------- adverse conditions --
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

    # --- 3. gPTP grandmaster changes and loss ------------------------------
    #  MOVED to the `physical` area (plan_physical): powering the switch off
    #  and back on IS the grandmaster loss (each end station becomes its own
    #  island GM) and the re-join IS the grandmaster change (BMCA re-elects
    #  with priority1 untouched - the USER standing rule that recovery must be
    #  automatic, never a forced win).  The physical area runs LAST because a
    #  partition mid-campaign would pollute every later verdict.

    # --- 4. malformed / truncated control frames --------------------------
    #  NOT from the adverse-conditions recommended practice, which covers only
    #  sustained high rate traffic, so each entry names its own 1722.1 clause.
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
    #  The DUT power cycle MOVED to the `physical` area (plan_physical), where
    #  it is powerstrip-automatable; its non-volatile assertions
    #  (A_STATE_RESTORED / A_COUNTERS_ZEROED) travelled with it.
    return S


# ---------------------------------------------- the physical (power) family --
#: docs/reference/REGISTER_MAP.md: `VERSION` (0x004) identifies the flashed
#: gateware; `CLKV_STAT` (0x77C) bit 0 is the tu bit as currently stamped on
#: every AVTPDU.  The CLKV lease behind that bit is SOFTWARE (gptp2csr.sh
#: renews it), so a boot or a recovery that loses the lease writer stamps
#: tu = 1 forever - exactly what the post-cycle tu assertion exists to catch.
VERSION_ADDR = 0x004
CLKV_STAT_ADDR = 0x77C
#: The healthy boot posture of the DUT's kernel interface:
#: /sys/class/net/eth0/flags == 0x1203 = IFF_UP | IFF_BROADCAST | IFF_ALLMULTI
#: | IFF_MULTICAST with IFF_PROMISC (0x100) ABSENT.  Promisc outranks even an
#: explicit TCAM drop in the RX filter's decision order (REGISTER_MAP.md), so
#: a boot that comes up promiscuous has silently voided its own RX shield and
#: starves the softcore under stream load.
DUT_IFACE_HEALTHY_FLAGS = 0x1203

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
    "count'.  A partition and a re-join are real BMCA elections, so the "
    "counter advances by a small bounded amount; one that never moved says "
    "the device slept through the partition")
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
A_TU_LEASE_REARMED = AssertSpec(
    "gptp.tu-lease-reestablished",
    "IEEE 1722-2016 4.4.4.7 tu: tu = 1 is the fail-safe and tu = 0 has to be "
    "EARNED - the CLKV lease (CLKV_STAT 0x77C bit 0, renewed by software in "
    "gptp2csr.sh) must be re-established once the GM is back, or every AVTPDU "
    "stamps tu = 1 forever.  The reading is a DUT CSR, so without a CSR path "
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
    "QSPI bitstream load + kernel + link guard measured ~5.5 min worst case "
    "on this DUT, so the default budget is 360 s and a boot that needs a "
    "hand at any rung is exactly the FAIL this exists to catch")
A_VERSION_UNCHANGED = AssertSpec(
    "boot.same-gateware-version",
    "the same-version rule (docs/testing/TORTURE_CAMPAIGN.md): a power cycle "
    "boots the QSPI image, so the VERSION CSR (0x004) must read back what the "
    "pre-snapshot read - a changed word means the golden-image fallback "
    "engaged (or a mid-campaign reflash), and every later verdict would be "
    "filed against the wrong gateware")
A_SHIELD_POSTURE = AssertSpec(
    "boot.shield-posture-restored",
    "REGISTER_MAP.md RX filter decision order: promisc outranks even an "
    "explicit TCAM drop, so the stream shield only exists while promisc "
    "stays gated - the healthy posture is eth0 flags 0x1203 (UP | BROADCAST "
    "| ALLMULTI | MULTICAST, PROMISC absent).  A boot that comes up "
    "promiscuous has voided its own RX shield and starves the softcore "
    "under stream load")
A_STATE_RESTORED = AssertSpec(
    "state.restored-after-power-cycle",
    "Milan v1.2 5.3.10.1: 'The PAAD-AE shall maintain a list of all its "
    "input channel mappings.  This list shall be saved in a non-volatile "
    "memory and restored after a power cycle.'  5.3.8.1 says the same for "
    "the current format and 5.3.7.6 for the presentation time offset")
A_COUNTERS_ZEROED = AssertSpec(
    "counters.zeroed-after-power-cycle",
    "IEEE 1722.1-2021 7.4.42: the counters are volatile state; a non-zero "
    "block straight after a power cycle is a restored-counter bug")


def plan_physical(dut: Device = ARTY, peer: Device = PEER) -> list:
    """The powerstrip-driven physical family - LAST, always, and never faked.

    USER AUTHORIZATION (2026-08-02): the amx-pi powerstrip may drive OUT4 =
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
        checks (VERSION unchanged, shield posture, tu lease).

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
        it back, which is what makes it a true cold boot), 360 s to the
        network (QSPI load + kernel + link guard measured ~5.5 min worst
        case on this bench), then 120 s more for gPTP.
    """
    S = []
    fmt = dut.formats[0] if dut.formats else None
    # the proof-pair indices: highest AAF (non-CRF) on each side - never 0
    tis = dut.talker_indices(include_crf=False)
    lis = peer.listener_indices(include_crf=False)
    ti = tis[-1] if tis else 0
    li = lis[-1] if lis else 0
    dlis = dut.listener_indices(include_crf=False)
    dli = dlis[-1] if dlis else 0

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
         "hold_s": 20, "ssh_budget_s": 240, "gptp_budget_s": 180,
         "settle_gap_s": 10, "gm_changes_max": 8,
         "clkv_stat_addr": CLKV_STAT_ADDR},
        needs_human=True,
        human_action="Power off the AVB switch (DN-1) at the powerstrip for "
                     "~20 s, then power it back on and wait for links, ssh "
                     "and gPTP to recover.  AUTOMATED when the runner is "
                     "given --powerstrip-cmd and --switch-outlet (bench: "
                     "amx-pi outlet 4).",
        asserts=(A_PARTITION_EXPECTED, A_GM_CHANGED_ADVANCES, A_GM_ID_FOLLOWS,
                 A_ONE_GM_RESTORED, A_GM_NOT_FLAPPING, A_AS_CAPABLE_RESTORED,
                 A_TU_LEASE_REARMED, A_NO_REBOOT, A_ADP_ALIVE),
        clause="802.1AS-2020 10.3 BMCA + IEEE 1722.1-2021 Table 7-153 "
               "GPTP_GM_CHANGED",
        note="the partition IS the GM loss and the re-join IS the GM change: "
             "priority1 is never touched (USER standing rule - recovery must "
             "be automatic).  Mid-partition nothing is verifiable from the "
             "controller host - it is inside the partition - so the "
             "own-island-GM claim is verified retroactively from the "
             "GM_CHANGED counters, and timeouts during the off-window are "
             "the expected condition, never failures"))
    S += _pair_steps("phys.switch-cycle.proof", "physical", dut, ti, peer, li,
                     fmt)

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
         "iface": "eth0", "iface_flags": DUT_IFACE_HEALTHY_FLAGS,
         "fmt_out_index": ti, "fmt_in_index": dli},
        needs_human=True,
        human_action="Power-cycle the DUT at the outlet (off for at least "
                     "8 s - the SRAM gateware is lost, QSPI boots it back), "
                     "then wait for the network to come up with NO manual "
                     "intervention.  AUTOMATED when the runner is given "
                     "--powerstrip-cmd and --dut-outlet (bench: amx-pi "
                     "outlet 0).",
        asserts=(A_ADP_ALIVE, A_BOOT_UNATTENDED, A_VERSION_UNCHANGED,
                 A_SHIELD_POSTURE, A_STATE_RESTORED, A_COUNTERS_ZEROED,
                 A_ONE_GM_RESTORED, A_TU_LEASE_REARMED),
        clause="Milan v1.2 5.3.10.1 / 5.3.8.1 / 5.3.7.6",
        note="the only test that can see the non-volatile requirements at "
             "all - and the zero-touch boot ladder (network, VERSION, shield "
             "posture, discovery, gPTP, tu lease) is the persistence story "
             "the flash rounds keep re-earning"))
    S += _pair_steps("phys.dut-cycle.proof", "physical", dut, ti, peer, li,
                     fmt)
    return S


AREAS = {
    "matrix": plan_matrix,
    "multi": plan_multi,
    "churn": plan_churn,
    "payload": plan_payload,
    "audio": plan_audio,
    "torture": plan_torture,
    #: LAST on purpose, and load-bearing: build_plan() emits areas in THIS
    #: order, and a switch partition or a DUT power cycle mid-matrix would
    #: pollute every verdict that follows it.  The runner additionally never
    #: drives two outlets concurrently.
    "physical": plan_physical,
}


def build_plan(areas=None, dut: Device = ARTY, peer: Device = PEER) -> list:
    """The whole campaign, or the named areas, in execution order."""
    want = list(AREAS) if not areas else list(areas)
    bad = [a for a in want if a not in AREAS]
    if bad:
        raise ValueError(f"unknown area(s) {bad}; known: {sorted(AREAS)}")
    out = []
    for a in want:
        fn = AREAS[a]
        try:
            out += fn(dut, peer)
        except TypeError:
            out += fn(dut)
    return out


# ------------------------------------------------------------- plan auditing --
def plan_covers_every_index(plan, dut: Device = ARTY,
                            peer: Device = PEER) -> dict:
    """Which talker/listener indices the plan actually touches.

    This is the audit that makes the standing "never index 0 only" rule
    executable at a desk instead of a habit.
    """
    seen = {"dut_talker": set(), "dut_listener": set(),
            "peer_talker": set(), "peer_listener": set()}
    for s in plan:
        a = s.args
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


def plan_coverage_by_area(plan, dut: Device = ARTY,
                          peer: Device = PEER) -> dict:
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
        # not per-index by nature either: the physical family's proof pair
        # deliberately walks ONE pair (the highest AAF indices - never the
        # index-0 alias path), and full per-index coverage already belongs to
        # the matrix that ran before the power was touched
        "physical": {},
    }


def area_covers_every_index(plan, area: str, dut: Device = ARTY,
                            peer: Device = PEER, *, expect=None) -> tuple:
    """(ok, detail) for ONE area against that area's own expectation."""
    cov = plan_coverage_by_area(plan, dut, peer).get(area, {})
    want = expect if expect is not None else \
        area_index_expectations(dut, peer).get(area, {})
    missing = {k: sorted(set(v) - set(cov.get(k, []))) for k, v in want.items()}
    missing = {k: v for k, v in missing.items() if v}
    return (not missing, {"area": area, "covered": cov, "expected": want,
                          "missing": missing})


def human_steps(plan) -> list:
    return [s for s in plan if s.needs_human]


def checklist_text(plan) -> str:
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
def verdict_record(step_id: str, assertion: str, verdict: str, *,
                   clause: str = "", severity: str = "SHALL",
                   area: str = "", run: str = "", **detail) -> dict:
    """The JSONL verdict shape every consumer emits.

    One line per ASSERTION, not per step: a step that emits one line can only
    report its worst outcome, and a morning diff then cannot tell which
    assertion changed.  `run` is a caller-supplied run id so two mornings sort.
    """
    return {"schema": "milan-torture/1", "run": run, "step": step_id,
            "area": area, "assertion": assertion, "verdict": verdict,
            "severity": severity, "clause": clause, "detail": detail}


VERDICTS = ("PASS", "FAIL", "SKIP", "INFO", "KNOWN-PENDING",
            "CONFORMANT-REFUSAL", "NEEDS-HUMAN", INSTRUMENT_SUSPECT)


def exit_code(records) -> int:
    """0 all good; 1 a SHALL-severity FAIL; 2 only RECOMMENDED failures or
    NEEDS-HUMAN entries outstanding.  A SKIP alone never fails the run - it is
    honest - but it is counted in the summary so it cannot hide.

    INSTRUMENT-SUSPECT never fails the run either, for the same reason: it says
    the TEST MACHINE lost frames, so the measurement is inadmissible.  Grading it
    as a device failure would be reporting the instrument's defect against the
    device - and it is counted in the summary, so a run that is all suspect
    cannot read as a clean one."""
    hard = any(r["verdict"] == "FAIL" and r.get("severity") == "SHALL"
               for r in records)
    soft = any(r["verdict"] in ("FAIL", "NEEDS-HUMAN") for r in records)
    return 1 if hard else (2 if soft else 0)


def summarise(records) -> dict:
    out = {v: 0 for v in VERDICTS}
    for r in records:
        out[r["verdict"]] = out.get(r["verdict"], 0) + 1
    out["total"] = len(records)
    out["exit_code"] = exit_code(records)
    return out


# ------------------------------------------------------------------ self test --
def self_test() -> int:
    import unittest

    class T(unittest.TestCase):
        def test_counter_tables_match_the_standards(self):
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

        def test_counters_payload_decode_and_unnamed_slots(self):
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

        def test_lock_and_talker_invariants(self):
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

        def test_tv_tnv_distinguishes_the_two_frames_rx_readings(self):
            # 1722.1 per-frame reading: the identity is exact
            v, d = check_tv_tnv({"TIMESTAMP_VALID": 1000,
                                 "TIMESTAMP_NOT_VALID": 0, "FRAMES_RX": 1000})
            self.assertEqual((v, d["reading"]), ("PASS", "1722.1-per-frame"))
            # Milan interval reading: 8000 frames in 1 s, FRAMES_RX ticks once
            v, d = check_tv_tnv({"TIMESTAMP_VALID": 8000,
                                 "TIMESTAMP_NOT_VALID": 0, "FRAMES_RX": 1})
            self.assertEqual((v, d["reading"]), ("INFO", "milan-interval"))
            # neither reading permits FRAMES_RX above TV+TNV
            self.assertEqual(check_tv_tnv({"TIMESTAMP_VALID": 5,
                                           "TIMESTAMP_NOT_VALID": 0,
                                           "FRAMES_RX": 99})[0], "FAIL")
            self.assertEqual(check_tv_tnv({})[0], "SKIP")

        def test_frames_rate_band(self):
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

        def test_no_growth_is_a_verdict_and_not_a_note(self):
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

        def test_licence_decode_and_the_shut_gate(self):
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

        def test_the_frame_versus_interval_semantic_trap_cannot_be_expressed(self):
            # AVB_INTERFACE FRAMES_TX/RX are TOTALS (1722.1 Table 7-153); the
            # stream-descriptor ones are <= 1 s interval TICKS (Milan Table
            # 5.4/5.6).  Same name, ~8000:1 apart.  A frame-accurate comparison
            # against the interval counters must be IMPOSSIBLE TO WRITE.
            for good in FRAME_ACCURATE_SOURCES:
                self.assertEqual(assert_frame_accurate(good), good)
            for bad in INTERVAL_SOURCES:
                with self.assertRaises(CounterSemanticError):
                    assert_frame_accurate(bad)
            with self.assertRaises(CounterSemanticError):
                assert_frame_accurate("vibes")
            # and the interval comparison is named for what it compares
            v, d = interval_ticks_agree(4, 4)
            self.assertEqual(v, "PASS")
            self.assertIn("OBSERVATION INTERVALS", d["compares"])
            self.assertEqual(interval_ticks_agree(4, 0)[0], "FAIL")
            self.assertEqual(interval_ticks_agree(0, 0)[0], "PASS")
            self.assertEqual(interval_ticks_agree(9, 4)[0], "FAIL")
            self.assertEqual(interval_ticks_agree(None, 4)[0], "SKIP")

        def test_interval_agreement_attributes_a_per_frame_side(self):
            # EVERY PARTICIPANT IS A MEASURED PARTY.  The three shapes:
            # (1) both interval-conformant and agreeing -> PASS, no finding
            v, d = interval_ticks_agree(4, 4, window_s=4.0)
            self.assertEqual(v, "PASS")
            self.assertNotIn("peer_findings", d)
            # (2) both interval-conformant and genuinely disagreeing -> the
            #     ORIGINAL pair FAIL, untouched by attribution
            v, d = interval_ticks_agree(9, 4, window_s=4.0)
            self.assertEqual(v, "FAIL")
            self.assertNotIn("peer_findings", d)
            # (3) one side per-frame (the PEER deviation, ~8000/s): the pair
            #     verdict PASSes FOR THE CONFORMANT SIDE and the deviation is
            #     an attributed finding naming the deviant ROLE and its rate
            v, d = interval_ticks_agree(4, 31982, window_s=4.0)
            self.assertEqual(v, "PASS")
            self.assertTrue(d["attributed"])
            self.assertEqual(d["conformant_role"], "talker")
            self.assertEqual(d["listener_semantics"], "per-frame")
            pf = d["peer_findings"]
            self.assertEqual([f["role"] for f in pf], ["listener"])
            self.assertGreater(pf[0]["ticks_per_s"], 150)
            self.assertIn("Table 7-157", pf[0]["why"])
            # ... and mirrored, the talker can be the deviant
            v, d = interval_ticks_agree(72880, 9, window_s=8.0)
            self.assertEqual(v, "PASS")
            self.assertEqual(d["conformant_role"], "listener")
            self.assertEqual(d["peer_findings"][0]["role"], "talker")
            # movement disagreement OUTRANKS attribution: a deviant side
            # pumping frames while the conformant side saw nothing is the
            # original one-sided-streaming FAIL, with the finding kept
            v, d = interval_ticks_agree(0, 31982, window_s=4.0)
            self.assertEqual(v, "FAIL")
            self.assertEqual(d["peer_findings"][0]["role"], "listener")
            # two per-frame sides leave no baseline: SKIP + one finding EACH,
            # never a silent pass for either
            v, d = interval_ticks_agree(31982, 31982, window_s=4.0)
            self.assertEqual(v, "SKIP")
            self.assertEqual(len(d["peer_findings"]), 2)
            # without a window the absolute floor still catches wire rate
            v, d = interval_ticks_agree(4, 31982)
            self.assertEqual(v, "PASS")
            self.assertEqual(d["peer_findings"][0]["role"], "listener")
            self.assertIsNone(d["peer_findings"][0]["ticks_per_s"])
            # and a fast-but-plausible interval implementation is NOT deviant:
            # 40 ticks over 4 s (a legal 100 ms interval) stays an interval
            # reading, so the disagreement with a 1/s peer is the pair's
            v, d = interval_ticks_agree(4, 40, window_s=4.0)
            self.assertEqual(v, "FAIL")
            self.assertNotIn("peer_findings", d)

        def test_cross_side_growth_bites_every_way(self):
            def sides(t, l, w=None, **kw):
                s = {"dut": {"role": "talker", "source": "avb_interface",
                             "frames": t, "device": "arty"},
                     "peer": {"role": "listener", "source": "avb_interface",
                              "frames": l, "device": "peer"}}
                if w is not None:
                    s["testhost"] = {"role": "wire", "source": "nic",
                                     "frames": w, "device": "testhost"}
                s.update(kw)
                return s

            def one(res, name):
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
            # and the semantic guard applies to the cross-check too
            with self.assertRaises(CounterSemanticError):
                cross_side_growth({"x": {"role": "talker",
                                         "source": "stream_output",
                                         "frames": 1}})

        def test_the_test_machine_is_an_instrument_before_a_witness(self):
            base = {k: 0 for k in
                    NIC_LOSS_KEYS + NIC_DEMUX_KEYS + NIC_TRAFFIC_KEYS}
            v, d = instrument_health(base, dict(base, rx_packets=8000))
            self.assertEqual(v, "PASS")
            self.assertEqual(d["traffic_delta"]["rx_packets"], 8000)
            v, d = instrument_health(base, dict(base, rx_missed_errors=17))
            self.assertEqual(v, "FAIL")
            self.assertEqual(d["moved"]["rx_missed_errors"], 17)
            # rx_dropped alone is the switch's unhandled MVRP hitting kernel
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

        def test_topology_is_configuration_not_a_source_edit(self):
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

        def test_coverage_is_audited_PER_AREA(self):
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

        def test_ieee_bit_numbering_conversion(self):
            # Table 7-156 calls the counter at block offset 0 "Bit # 31"
            self.assertEqual(counters_valid_bit_ieee(0), 31)
            self.assertEqual(counters_valid_bit_ieee(44), 20)   # FRAMES_RX
            self.assertEqual(counters_valid_bit_ieee(124), 0)   # ENT_SPECIFIC_1
            with self.assertRaises(ValueError):
                counters_valid_bit_ieee(3)

        def test_milan_and_ieee_stream_output_layouts_differ(self):
            # the trap: the same NAME sits at a different offset in the two
            # layouts, so a decoder that picks the wrong one mislabels
            self.assertEqual(MILAN_TABLE_54.index("FRAMES_TX"), 4)
            self.assertEqual(IEEE_STREAM_OUTPUT_BLOCK.index("FRAMES_TX"), 7)
            self.assertEqual(MILAN_TABLE_54.index("MEDIA_RESET"), 2)
            self.assertEqual(IEEE_STREAM_OUTPUT_BLOCK.index("MEDIA_RESET"), 3)

        def test_matrix_walks_every_index_both_directions_and_crf(self):
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

        def test_every_bound_step_carries_the_full_assertion_set(self):
            need = {a.name for a in BOUND_STREAMING_ASSERTS}
            for s in build_plan(["matrix", "churn"]):
                if s.op == "connect" and "rebind" not in s.sid:
                    got = {a.name for a in s.asserts}
                    self.assertTrue(need <= got,
                                    f"{s.sid} is missing {need - got}")

        def test_every_step_has_a_clause_or_says_it_is_info(self):
            for s in build_plan():
                for a in s.asserts:
                    self.assertTrue(a.clause.strip(),
                                    f"{s.sid}/{a.name} has no clause")
                    self.assertIn(a.severity, ("SHALL", "RECOMMENDED", "INFO"))

        def test_storm_entries_are_recommended_not_shall(self):
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

        def test_human_entries_are_emitted_not_skipped(self):
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

        def test_physical_family_contract(self):
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
            self.assertIn("gptp.tu-lease-reestablished", sw)
            du = {a.name for a in cyc["dut_power_cycle"].asserts}
            self.assertIn("state.restored-after-power-cycle", du)
            self.assertIn("counters.zeroed-after-power-cycle", du)
            self.assertIn("boot.reaches-network-unattended", du)
            self.assertIn("boot.same-gateware-version", du)
            self.assertIn("boot.shield-posture-restored", du)
            # the budget floors from the bench facts: switch boot before any
            # board is reachable, ~5.5 min worst-case DUT boot, and a hold an
            # order of magnitude past the announce-receipt timeout
            a = cyc["switch_power_cycle"].args
            self.assertGreaterEqual(a["hold_s"], 15)
            self.assertGreaterEqual(a["ssh_budget_s"], 180)
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

        def test_churn_includes_the_implicit_rebind_to_a_different_talker(self):
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

        def test_areas_selector(self):
            self.assertEqual({s.area for s in build_plan(["audio"])},
                             {"audio"})
            with self.assertRaises(ValueError):
                build_plan(["nope"])
            self.assertEqual({s.area for s in build_plan()},
                             {"matrix", "multi", "churn", "payload", "audio",
                              "torture", "physical"})

        def test_multi_area_walks_concurrent_sets_and_serialises(self):
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
            # PEER's (p) primaries), never a hardcoded list
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

        def test_multi_stress_set_is_maximal_and_loads_both_directions(self):
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
            # on the AX 8x8 shape: all 8 talkers out, t5..t7 looped home
            ax = parse_device_spec("talkers=8,listeners=8,crf_out=8,"
                                   "crf_in=8", ARTY)
            axb = next(s for s in plan_multi(ax, PEER)
                       if s.sid == "multi.stress.bind-all")
            self.assertEqual(sorted({p["talker_index"]
                                     for p in axb.args["pairs"]
                                     if p["talker"] == ax.entity_id}),
                             list(range(8)))
            self.assertEqual(sorted(p["talker_index"]
                                    for p in axb.args["pairs"]
                                    if p["talker"] == ax.entity_id
                                    and p["listener"] == ax.entity_id),
                             [5, 6, 7])
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

        def test_multi_concurrent_flowing_bites_every_way(self):
            def P(tx, rx):
                return {"tx_ticks": tx, "rx_ticks": rx}
            # all pairs flowing together, licence open -> PASS, and the
            # comparison names itself as INTERVALS
            v, d = check_concurrent_flowing({"a": P(4, 4), "b": P(5, 4)},
                                            licensed=True)
            self.assertEqual(v, "PASS")
            self.assertIn("OBSERVATION INTERVALS", d["compares"])
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

        def test_multi_unbound_isolation_bites(self):
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

        def test_plan_steps_serialise(self):
            for s in build_plan():
                d = s.as_dict()
                json.dumps(d)
                self.assertEqual(set(d["assert_clauses"]), set(d["asserts"]))

        def test_exit_codes(self):
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

        def test_audio_is_never_forgotten(self):
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

    r = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T))
    return 0 if r.wasSuccessful() else 1


# ------------------------------------------------------------------------ CLI --
def main() -> int:
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
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    dut = parse_device_spec(a.dut, ARTY) if a.dut else ARTY
    peer = parse_device_spec(a.peer, PEER) if a.peer else PEER
    areas = a.areas.split(",") if a.areas else None
    plan = build_plan(areas, dut, peer)
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
    print(f"\n{len(plan)} steps, "
          f"{sum(len(s.asserts) for s in plan)} assertions, "
          f"{len(human_steps(plan))} need a human")
    return 0


if __name__ == "__main__":
    sys.exit(main())
