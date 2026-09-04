#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""avtp_wire_truth_identity.py - THE IDENTITY PROPERTY: which audio
channel is which, decided from the payload alone.

A walking tone puts a distinct, channel-derived value on every channel, so a
swap, a duplicate and a dropped channel are three different failures rather
than one indistinguishable "audio present".  Kept apart from
`avtp_wire_truth_checks.py` because this is the one property that reads SAMPLES
rather than headers, and `tests/steps/audio_identity_steps.py` is its
consumer."""
from __future__ import annotations

from collections.abc import Callable

from avtp_wire_truth_wire import AafPdu, Verdict, _v


# ------------------------------------------------------------- audio identity --
def channel_identity(pdu: AafPdu, shift: int = 8) -> list:
    """Per-channel sample lists in wire order (7.3.5), right-shifted by
    `shift` to undo a left-justified payload.

    Our packetizer writes 24-bit samples into 32-bit slots as sample << 8
    (KL_aaf_packetizer frame_bytes), so shift = 8 recovers the 24-bit value.
    The shift is an ARGUMENT and not a constant: a listener that guesses it is
    how a real bit-depth defect stays invisible.
    """
    n = pdu.sample_frames or 0
    return [[(pdu.sample(f, c) or 0) >> shift for f in range(n)]
            for c in range(pdu.channels_per_frame)]


def check_walking_tone(pdus: list, expect_channels: int,
                       tag_of: Callable[[int], int] | None = None,
                       ) -> list[Verdict]:
    """The identity property, shaped to match it (methodology R4).

    A walking/binary tone puts a DISTINCT, channel-derived value on every
    channel, so a swap, a duplicate and a dropped channel are three different
    failures instead of one indistinguishable "audio present".  `tag_of(ch)`
    returns the expected value for channel `ch`; the default is the binary
    walking pattern used by the fabric tone generator's per-channel tag
    (1 << ch), which is unambiguous up to 24 channels.
    """
    tag_of = tag_of or (lambda c: 1 << c)
    out = []
    if not pdus:
        return [Verdict("audio.identity", "FAIL", "IEEE 1722-2016 7.3.5",
                        {"why": "no AAF frames to check identity on"})]
    chans_seen = {p.channels_per_frame for p in pdus}
    out.append(_v("audio.identity.channel-count", chans_seen ==
                  {expect_channels},
                  "IEEE 1722-2016 7.3.3: channels_per_frame is what the frame "
                  "carries", expected=expect_channels,
                  observed=sorted(chans_seen)))
    crossed, duplicated, silent = [], [], []
    for n, p in enumerate(pdus):
        chans = channel_identity(p)
        for c, vals in enumerate(chans):
            want = tag_of(c)
            if not any(vals):
                silent.append({"pdu": n, "channel": c})
            elif not all(v == want for v in vals):
                where = [i for i, v in enumerate(vals) if v != want]
                crossed.append({"pdu": n, "channel": c, "expected": want,
                                "got": [vals[i] for i in where[:4]]})
        for c in range(1, len(chans)):
            if chans[c] and chans[c] == chans[c - 1]:
                duplicated.append({"pdu": n, "channel": c})
    out.append(_v("audio.identity.uncrossed", not crossed,
                  "IEEE 1722-2016 7.3.5: payload sample k belongs to wire "
                  "channel k mod channels_per_frame",
                  violations=crossed[:8], violation_count=len(crossed)))
    out.append(_v("audio.identity.no-duplicate-neighbour", not duplicated,
                  "IEEE 1722-2016 7.3.5: two channels carrying identical "
                  "content is the signature of a mux stuck on one pair",
                  violations=duplicated[:8], violation_count=len(duplicated)))
    out.append(_v("audio.identity.no-silent-channel", not silent,
                  "IEEE 1722-2016 7.3.5 + Milan 5.3.10.1: a mapped channel "
                  "that carries nothing is a dropped channel, and presence "
                  "testing cannot see it",
                  violations=silent[:8], violation_count=len(silent)))
    return out
