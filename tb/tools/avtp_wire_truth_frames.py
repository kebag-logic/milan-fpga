#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""avtp_wire_truth_frames.py - THE BYTE-VECTOR ORACLE: frames built by
hand from the figures, never from our RTL.

`build_aaf_frame` is written from IEEE 1722-2016 Figure 26 and `build_crf_frame`
from Figure 72, so a decoder and a packetizer that agree with each other can
still both disagree with the standard - which is the only way this file can
fail against us.  Each builder takes one frozen record of fields and accepts
those field names as keywords, so a call site reads as the figure does."""
from __future__ import annotations

import struct
from collections.abc import Sequence
from dataclasses import dataclass, replace

from avtp_wire_truth_wire import (AAF_FORMAT_BITS, ADP_CDL, ETH_P_AVTP,
                                  ETH_P_MSRP, ETH_P_MVRP, MRP_GROUP_DMAC,
                                  MSRP_ATTR_LEN, MSRP_LISTENER, MVRP_VID,
                                  SUBTYPE_AAF, SUBTYPE_ADP, SUBTYPE_CRF,
                                  TPID_C_TAG)


# ----------------------------------------------------- byte-vector builders --
def _b(*parts) -> bytes:
    return bytes.fromhex("".join(parts).replace(" ", ""))


@dataclass(frozen=True)
class AafFrame:
    """The fields of one hand-built AAF PCM frame: the Ethernet envelope
    (dmac, smac, tagged, vid, pcp) around the IEEE 1722-2016 Figure 26 AVTPDU
    header, plus the sample grid the payload carries.

    Frozen, so one instance can stand as the default below without becoming
    state shared between calls.
    """
    dmac: str = "91e0f000fe01"
    smac: str = "020000000002"
    vid: int = 2
    pcp: int = 3
    tagged: bool = True
    seq: int = 0
    sid: int = 0x020000000002_0000
    ts: int = 0
    channels: int = 2
    fmt: int = 0x02
    bit_depth: int = 32
    nsr: int = 5
    sample_frames: int = 6
    samples: list[list[int]] | None = None
    tv: int = 1
    tu: int = 0
    sp: int = 0
    mr: int = 0


def build_aaf_frame(spec: AafFrame = AafFrame(), **overrides: object) -> bytes:
    """An AAF PCM frame built to IEEE 1722-2016 Figure 26, by hand.

    This is the byte-vector oracle the decoder is tested against: it is written
    from the FIGURE, not from KL_aaf_packetizer, so the two can disagree.
    `spec.samples[frame][channel]` are 24-bit values, left-justified like the
    fabric does (sample << 8).

    `overrides` names `AafFrame` fields directly, which is how every call site
    reads - `build_aaf_frame(seq=7, channels=8)` - and it is `replace` that
    applies them, so a misspelled field is a TypeError here rather than a
    silently ignored keyword.
    """
    f = replace(spec, **overrides) if overrides else spec
    w = AAF_FORMAT_BITS.get(f.fmt, 32) // 8
    sdl = f.sample_frames * f.channels * w
    hdr = bytearray()
    hdr += bytes.fromhex(f.dmac) + bytes.fromhex(f.smac)
    if f.tagged:
        hdr += struct.pack(">H", TPID_C_TAG)
        hdr += struct.pack(">H", (f.pcp << 13) | (f.vid & 0xFFF))
    hdr += struct.pack(">H", ETH_P_AVTP)
    pdu = bytearray(24)
    pdu[0] = SUBTYPE_AAF
    pdu[1] = (1 << 7) | (f.mr << 3) | (f.tv & 1)
    pdu[2] = f.seq & 0xFF
    pdu[3] = f.tu & 1
    pdu[4:12] = f.sid.to_bytes(8, "big")
    pdu[12:16] = struct.pack(">I", f.ts & 0xFFFFFFFF)
    pdu[16] = f.fmt
    pdu[17] = ((f.nsr & 0xF) << 4) | ((f.channels >> 8) & 0x3)
    pdu[18] = f.channels & 0xFF
    pdu[19] = f.bit_depth
    pdu[20:22] = struct.pack(">H", sdl)
    pdu[22] = (f.sp << 4)
    body = bytearray()
    for n in range(f.sample_frames):
        for c in range(f.channels):
            v = 0 if f.samples is None else f.samples[n][c]
            body += ((v << 8) & 0xFFFFFFFF).to_bytes(w, "big")
    frame = bytes(hdr) + bytes(pdu) + bytes(body)
    return frame + b"\x00" * max(0, 60 - len(frame))


@dataclass(frozen=True)
class CrfFrame:
    """The fields of one hand-built CRF frame: the Ethernet envelope around
    the IEEE 1722-2016 Figure 72 AVTPDU header and its timestamp series.

    Frozen, for the same reason `AafFrame` is.
    """
    dmac: str = "91e0f000fe02"
    smac: str = "020000000002"
    vid: int = 2
    pcp: int = 3
    tagged: bool = True
    seq: int = 0
    sid: int = 0x020000000002_0001
    ts: int = 0
    base_hz: int = 48000
    interval: int = 96
    pull: int = 0
    ctype: int = 1
    tu: int = 0
    n_ts: int = 1


def build_crf_frame(spec: CrfFrame = CrfFrame(), **overrides: object) -> bytes:
    """A CRF frame built to IEEE 1722-2016 Figure 72, by hand.

    `overrides` names `CrfFrame` fields, exactly as `build_aaf_frame` takes
    `AafFrame` ones, and `replace` refuses a name the record does not have.
    """
    f = replace(spec, **overrides) if overrides else spec
    hdr = bytearray(bytes.fromhex(f.dmac) + bytes.fromhex(f.smac))
    if f.tagged:
        hdr += struct.pack(">H", TPID_C_TAG)
        hdr += struct.pack(">H", (f.pcp << 13) | (f.vid & 0xFFF))
    hdr += struct.pack(">H", ETH_P_AVTP)
    pdu = bytearray(20)
    pdu[0] = SUBTYPE_CRF
    pdu[1] = (1 << 7) | (f.tu & 1)
    pdu[2] = f.seq & 0xFF
    pdu[3] = f.ctype
    pdu[4:12] = f.sid.to_bytes(8, "big")
    pdu[12:16] = struct.pack(">I",
                             ((f.pull & 7) << 29) | (f.base_hz & 0x1FFFFFFF))
    pdu[16:18] = struct.pack(">H", 8 * f.n_ts)
    pdu[18:20] = struct.pack(">H", f.interval)
    body = b"".join((f.ts + i * f.interval * 1_000_000_000 // f.base_hz)
                    .to_bytes(8, "big") for i in range(f.n_ts))
    frame = bytes(hdr) + bytes(pdu) + body
    return frame + b"\x00" * max(0, 60 - len(frame))


def build_msrp_frame(
    *,
    smac: str = "020000000002",
    attrs: Sequence[tuple[int, bytes, list[int], list[int]]] | None = None,
) -> bytes:
    """An MSRPDU built by hand from 802.1Q-2018 10.8.1 + 35.2.2.

    `attrs` is a list of (attr_type, first_value_bytes, [events],
    [listener_declarations]).  Written from the CLAUSE, not from our RTL, so the
    decoder and the fabric can disagree - which is the point of a byte-vector
    oracle.
    """
    body = bytearray([0x00])                    # ProtocolVersion
    for atype, first, events, decls in (attrs or []):
        alen = MSRP_ATTR_LEN.get(atype, len(first))
        n = len(events)
        vec = bytearray()
        for i in range(0, n, 3):
            trio = (events + [4, 4])[i:i + 3]   # pad with Mt
            vec.append((trio[0] * 6 + trio[1]) * 6 + trio[2])
        fp = bytearray()
        if atype == MSRP_LISTENER:
            for i in range(0, n, 4):
                q = (decls + [0, 0, 0])[i:i + 4]
                fp.append((q[0] << 6) | (q[1] << 4) | (q[2] << 2) | q[3])
        vector = struct.pack(">H", n & 0x1FFF) + bytes(first) + bytes(vec) \
            + bytes(fp)
        body += bytes([atype, alen])
        body += struct.pack(">H", len(vector) + 2)      # AttributeListLength
        body += vector
        body += b"\x00\x00"                             # Message EndMark
    body += b"\x00\x00"                                 # PDU EndMark
    frame = MRP_GROUP_DMAC + bytes.fromhex(smac) + \
        struct.pack(">H", ETH_P_MSRP) + bytes(body)
    return frame + b"\x00" * max(0, 60 - len(frame))


@dataclass(frozen=True)
class TalkerAdvertise:
    """The fields of a Talker Advertise FirstValue, 802.1Q-2018 35.2.2.8:
    StreamID(8) + DataFrameParameters(dmac, vid) + TSpec(max_frame,
    max_interval) + PriorityAndRank(pcp, rank) + AccumulatedLatency.

    Frozen, so one instance can stand as the default below without becoming
    state shared between calls.
    """
    stream_id: int = 0x0200000000020000
    dmac: str = "91e0f000fe01"
    vid: int = 2
    max_frame: int = 1024
    max_interval: int = 1
    pcp: int = 3
    rank: int = 1
    latency: int = 0


def msrp_talker_advertise_value(spec: TalkerAdvertise = TalkerAdvertise(),
                                **overrides: object) -> bytes:
    """The 25-octet Talker Advertise FirstValue, per 802.1Q-2018 35.2.2.8.

    `overrides` names `TalkerAdvertise` fields, the same way the two frame
    builders above take theirs, so `msrp_talker_advertise_value(stream_id=x)`
    still says what it always said.
    """
    attr = replace(spec, **overrides) if overrides else spec
    return (attr.stream_id.to_bytes(8, "big") + bytes.fromhex(attr.dmac)
            + struct.pack(">HHH", attr.vid, attr.max_frame, attr.max_interval)
            + bytes([((attr.pcp & 7) << 5) | ((attr.rank & 1) << 4)])
            + struct.pack(">I", attr.latency))


def msrp_listener_value(stream_id: int = 0x0200000000020000) -> bytes:
    """The 8-octet Listener FirstValue: the StreamID and nothing else.

    Its declaration TYPE (Ready / Ready Failed / Asking Failed) rides the
    FourPackedEvents vector, not this value - 802.1Q-2018 35.2.2.8.2."""
    return stream_id.to_bytes(8, "big")


def msrp_domain_value(class_id: int = 6, priority: int = 3,
                      vid: int = 2) -> bytes:
    """The 4-octet Domain FirstValue: SRclassID, SRclassPriority, SRclassVID
    (802.1Q-2018 35.2.2.8) - the declaration that puts a VID in SR class A."""
    return bytes([class_id, priority]) + struct.pack(">H", vid)


def build_mvrp_frame(*, smac: str = "020000000002",
                     vids: Sequence[int] = (2,)) -> bytes:
    """An MVRPDU (802.1Q-2018 11.2.3.1.2): one attribute type, VID, length 2."""
    body = bytearray([0x00, MVRP_VID, 0x02])
    for v in vids:
        body += struct.pack(">H", 1) + struct.pack(">H", v) + bytes([1 * 36])
    body += b"\x00\x00\x00\x00"
    frame = MRP_GROUP_DMAC + bytes.fromhex(smac) + \
        struct.pack(">H", ETH_P_MVRP) + bytes(body)
    return frame + b"\x00" * max(0, 60 - len(frame))


def build_adp_frame(*, smac: str = "020000000002",
                    eid: int = 0x020000FFFE000002, available_index: int = 1,
                    cdl: int = ADP_CDL, body_len: int = 64) -> bytes:
    """An ENTITY_AVAILABLE ADPDU (1722.1-2021 6.2)."""
    hdr = bytes.fromhex("91e0f0010000") + bytes.fromhex(smac) + \
        struct.pack(">H", ETH_P_AVTP)
    pdu = bytearray(4)
    pdu[0] = SUBTYPE_ADP
    pdu[1] = 1 << 7                       # sv=1, version 0, message_type 0
    pdu[2:4] = struct.pack(">H", (31 << 11) | (cdl & 0x7FF))
    body = bytearray(body_len)
    body[0:8] = eid.to_bytes(8, "big")
    if body_len >= 36:
        body[32:36] = struct.pack(">I", available_index)
    return hdr + bytes(pdu) + bytes(body)
