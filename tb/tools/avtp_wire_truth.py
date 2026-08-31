#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""avtp_wire_truth.py - decode AVTP off a capture and check the invariants that
declarations cannot see.

    # CLI over a ProfiShark inline tap (28-byte record header, FCS present)
    ./avtp_wire_truth.py capture.pcap --tap --expect-aaf-format 0205022001006000
    # every check as one JSON line per verdict, for a morning diff
    ./avtp_wire_truth.py capture.pcap --jsonl > verdicts.jsonl
    # the offline byte-vector self test (no capture, no hardware)
    ./avtp_wire_truth.py --self-test

WHY THIS EXISTS.  Every gate in this repo compares a DECLARATION against
another declaration.  The escape that started the whole accountability effort
(docs/testing/methodology.md, escape 1) was a talker advertising eight audio
channels while its framer emitted two: config, generated header, CSR and AEM
descriptor all agreed, and the only thing that disagreed was the wire.  This
module's oracle is THE WIRE plus THE CLAUSE - never our own model - so it can
fail against us.

LEVEL AND ORACLE (docs/testing/methodology.md §2).  L5 when it is handed a
capture from a tap (the wire, on hardware); L3 when it is handed hand-built
byte vectors from the standards, which is how its own decoders are tested.
It is structurally blind to anything that never reaches a frame: an internal
counter, a CSR, a controller's view.  Those are the matrix runner's job
(tb/tools/torture_campaign.py) and they are deliberately NOT duplicated here.

THE CLAUSES, quoted where a check depends on the exact words.

  IEEE 1722-2016 Figure 26 - the AAF PCM AVTPDU field layout used by
    decode_aaf(): subtype, sv/version/mr/tv, sequence_num, tu, stream_id,
    avtp_timestamp, format, nsr, channels_per_frame, bit_depth,
    stream_data_length, sp, evt.
  IEEE 1722-2016 Annex I.2.4/I.2.4.1 - the ATDECC AAF stream_format qword, and
    the sentence the declared-vs-actual check rests on: "This field matches the
    setting of the channels_per_frame field in the Stream AVTPDU when this
    stream format is the current format for the stream."  The same sentence is
    written for nsr, format and bit_depth.  That is what makes a mismatch a
    DEFECT rather than a difference of opinion.
  IEEE 1722-2016 7.3.3 - "The channels_per_frame field shall be set to the
    number of audio channels represented in the audio sample frame, a positive
    integer greater than zero (0)."
  IEEE 1722-2016 7.3.4 - "The bit_depth field ... shall not be set to a value
    of zero (0).  The value of bit_depth shall not be set to a number which is
    larger than the size of the format set in the format field."
  IEEE 1722-2016 7.3.5 - the PCM payload is a chronological sequence of sample
    frames, each carrying one sample per channel IN CHANNEL ORDER.  That is the
    whole basis of the per-channel identity decode.
  IEEE 1722-2016 4.4.4.6 - sequence_num "shall be incremented by one (1), with
    wrapping, on each subsequent" AVTPDU of the stream.
  IEEE 1722-2016 10.4.6 - the CRF sequence_num is ONE OCTET and wraps
    "from 11111111(2) to 00000000(2) (FF16 to 0016)".  A 16-bit reading of it
    is a silent bug, so the CRF decoder takes the octet.
  IEEE 1722-2016 Figure 72 / 10.4.x - the CRF AVTPDU layout: sv/mr/fs/tu,
    sequence_num, type, stream_id, pull, base_frequency, crf_data_length,
    timestamp_interval, crf_data.
  IEEE 1722-2016 Annex I.2.6 - the ATDECC CRF stream_format qword.  Its
    base_frequency width is the ONE field this file resolves from a known-good
    constant instead of the prose: Milan v1.2 Table 7.1 pins the CRF Media Clock
    Stream Format string at 0x041060010000BB80, which only decodes with a 29-bit
    base_frequency (0xBB80 = 48000), so that is the width used.
  Milan v1.2 7.3.2 - "The base frequency shall be 48000Hz.  Each PDU shall
    contain 1 timestamp, and the timestamp interval shall be 96."  48000/96 =
    500 PDU/s = one CRF PDU every 2 ms; that is where the expected rate comes
    from, not from measuring ourselves.
  Milan v1.2 7.3.3 - a Class A Stream Reservation "shall be used to
    transmit" a CRF Media Clock Stream.  So an UNTAGGED CRF
    frame is a finding, and this project has measured exactly that: 4001
    untagged CRF frames in 8 s on 2026-07-28.
  Milan v1.2 5.3.7.3 - "As long as a PAAD is declaring a Talker Advertise
    attribute and receiving a Listener Ready or Listener Ready Failed attribute
    for a Stream Output, it shall be streaming AVTP packets."  A bound talker
    with nothing to send therefore owes FRAMES, not silence - which is why
    "all-zero payload" is a PASS for a stream declared silent and a FAIL for
    one declared fed, and why the absence of frames is a FAIL for both.
  802.1Q-2018 9.5/9.6 - the C-TAG: TPID 0x8100 then TCI {PCP, DEI, VID}.
  IEEE 1722.1-2021 9.2.1.1.6 - control_data_length counts the octets after the
    field it follows; a frame shorter than that is malformed however correct
    its status byte is.  The frame that LIES about its length is a defect class
    this project has hit, so the control-plane check is length-first.

WHAT THIS FILE DELIBERATELY DOES NOT DO.
  * It does not judge presentation time against gPTP unless a gPTP reference is
    SUPPLIED (--gptp-ref-ns / gptp_ref_ns=).  A pcap timestamp is the capture
    host's CLOCK_REALTIME, not the gPTP timebase, and comparing the two
    produces a confident number that means nothing.  Without a reference the
    class-A transit check reports SKIP with that reason attached (methodology
    R5: a structural zero is not a measurement).
  * It does not reserve, bind, or read a counter.  It reads frames.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from dataclasses import dataclass, field, asdict
from typing import Iterable, Iterator, Optional

# ----------------------------------------------------------------- constants --
ETH_P_AVTP = 0x22F0
TPID_C_TAG = 0x8100

SUBTYPE_AAF = 0x02
SUBTYPE_CRF = 0x04
SUBTYPE_ADP = 0xFA
SUBTYPE_AECP = 0xFB
SUBTYPE_ACMP = 0xFC
SUBTYPE_MAAP = 0xFE
SUBTYPE_NAMES = {SUBTYPE_AAF: "AAF", SUBTYPE_CRF: "CRF", SUBTYPE_ADP: "ADP",
                 SUBTYPE_AECP: "AECP", SUBTYPE_ACMP: "ACMP",
                 SUBTYPE_MAAP: "MAAP"}
CONTROL_SUBTYPES = (SUBTYPE_ADP, SUBTYPE_AECP, SUBTYPE_ACMP, SUBTYPE_MAAP)

#: SR class A priority code point (802.1Q-2018 34.5 default; Milan 4.2.7.2.1)
SR_CLASS_A_PCP = 3
#: The bench SR VID.  VID 0 is not "the default", it is the defect: an
#: untagged-on-egress frame leaves the reserved SR tree and floods unshaped.
SR_VID_DEFAULT = 2

#: IEEE 1722-2016 Table 11 - nsr field values, in Hz.  0 = "user specified",
#: which carries NO rate on the wire, so it decodes to None and never to a
#: number we made up.
NSR_HZ = {0x0: None, 0x1: 8000, 0x2: 16000, 0x3: 32000, 0x4: 44100,
          0x5: 48000, 0x6: 88200, 0x7: 96000, 0x8: 176400, 0x9: 192000,
          0xA: 24000}
#: IEEE 1722-2016 Table 9 - AAF format field values and the sample width each
#: implies, in BITS.  This is the width of the sample SLOT in the payload, not
#: bit_depth (which says how many of those bits carry data - 7.3.4).
AAF_FORMAT_NAMES = {0x0: "USER", 0x1: "FLOAT_32BIT", 0x2: "INT_32BIT",
                    0x3: "INT_24BIT", 0x4: "INT_16BIT", 0x5: "AES3_32BIT"}
AAF_FORMAT_BITS = {0x1: 32, 0x2: 32, 0x3: 24, 0x4: 16, 0x5: 32}

#: IEEE 1722-2016 Table 26 - CRF type values (only the one Milan uses is named)
CRF_TYPE_AUDIO_SAMPLE = 0x01

#: Milan v1.2 Table 7.1 - the CRF Media Clock Stream Format.
MILAN_CRF_FORMAT = 0x041060010000BB80
MILAN_CRF_BASE_HZ = 48000
MILAN_CRF_TS_INTERVAL = 96
MILAN_CRF_TS_PER_PDU = 1

#: IEEE 1722.1-2021 6.2.1: the ADPDU is a 4-octet AVTP control header + an
#: 8-octet entity_id + 56 further octets = 68, so 82 octets on the wire once
#: the 14-octet Ethernet header is counted, and control_data_length = 56.
ADP_CDL = 56
ADP_AVTPDU_LEN = 68
ADP_FRAME_LEN = 82

# ------------------------------------------------------------------- MRP/SRP --
#: 802.1Q-2018 Table 35-1 / 11.2.3.1.2: MSRP and MVRP are their OWN EtherTypes,
#: not AVTP, and they go to the Nearest Customer Bridge group address
#: 01:80:C2:00:00:0E - which a bridge does NOT forward.  So the SRP exchange is
#: invisible to any host that is not inline on the link: an INLINE TAP is the
#: only way to see a Listener Ready, and therefore the only way to see the second
#: half of the Milan v1.2 5.3.7.3 streaming licence on the wire.
ETH_P_MSRP = 0x22EA
ETH_P_MVRP = 0x88F5
MRP_GROUP_DMAC = bytes.fromhex("0180c200000e")

#: 802.1Q-2018 Table 35-1: the MSRP attribute types and their AttributeLengths.
MSRP_TALKER_ADVERTISE = 1
MSRP_TALKER_FAILED = 2
MSRP_LISTENER = 3
MSRP_DOMAIN = 4
MSRP_ATTR_NAMES = {1: "Talker Advertise", 2: "Talker Failed", 3: "Listener",
                   4: "Domain"}
MSRP_ATTR_LEN = {1: 25, 2: 34, 3: 8, 4: 4}
#: 802.1Q-2018 35.2.2.8.2 FourPackedEvents - the Listener declaration type.
MSRP_LISTENER_DECL = {0: "Ignore", 1: "Asking Failed", 2: "Ready",
                      3: "Ready Failed"}
#: 802.1Q-2018 10.7.6.2 ThreePackedEvents - the MRP AttributeEvent.
MRP_ATTR_EVENT = {0: "New", 1: "JoinIn", 2: "In", 3: "JoinMt", 4: "Mt",
                  5: "Lv"}
#: A declaration is PRESENT on the wire for these events; Lv/Mt withdraw it.
MRP_DECLARING_EVENTS = ("New", "JoinIn", "In", "JoinMt")
#: MVRP (802.1Q-2018 11.2.3.1.2): one attribute type, VID, AttributeLength 2.
MVRP_VID = 1

#: Class A max transit time, 802.1BA-2011 / Milan: 2 ms over up to 7 hops.
CLASS_A_MAX_TRANSIT_NS = 2_000_000
#: The AVTP timestamp is the low 32 bits of the gPTP nanosecond time.
AVTP_TS_MOD = 1 << 32


# ------------------------------------------------------------------ verdicts --
@dataclass
class Verdict:
    """One assertion outcome.  `check` is stable across runs so mornings diff."""
    check: str
    verdict: str                   # PASS | FAIL | SKIP | INFO
    clause: str = ""
    detail: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return asdict(self)

    def as_json(self) -> str:
        return json.dumps(self.as_dict(), separators=(",", ":"), sort_keys=True)


def _v(check, ok, clause, **detail) -> Verdict:
    return Verdict(check, "PASS" if ok else "FAIL", clause, detail)


def _nothing_to_check(check, clause, what) -> Verdict:
    """THE EMPTY-COLLECTION RULE, and it is a rule because the alternative bit
    us: a check whose loop body never runs must emit SKIP, never PASS and never
    nothing at all.

    On an empty capture eight of these twelve families used to emit NOTHING -
    so the JSONL simply had no line for them and a reviewer could not tell "did
    not apply" from "was not run" - and wt.control.length-honest emitted PASS,
    because `not []` is True.  An empty capture is the commonest false green in
    this project (a mirror port that never subscribed to the group), so it now
    produces one SKIP per family, each naming what was absent.
    """
    return Verdict(check, "SKIP", clause,
                   {"why": f"no {what} in the capture, so this check had "
                           f"nothing to run on; an EMPTY collection is a SKIP "
                           f"and never a PASS",
                    "absent": what})


# ------------------------------------------------------------ capture readers --
def _pcap_records(blob: bytes) -> Iterator[tuple[float, bytes]]:
    """Classic libpcap, either endianness, us or ns timestamps."""
    magic = blob[:4]
    if magic in (b"\xd4\xc3\xb2\xa1", b"\x4d\x3c\xb2\xa1"):
        endian, nano = "<", magic[0] == 0x4D
    elif magic in (b"\xa1\xb2\xc3\xd4", b"\xa1\xb2\x3c\x4d"):
        endian, nano = ">", magic[3] == 0x4D
    else:
        raise ValueError(f"not a classic pcap (magic {magic.hex()})")
    off = 24
    div = 1e9 if nano else 1e6
    while off + 16 <= len(blob):
        s, us, caplen, _orig = struct.unpack(endian + "IIII", blob[off:off + 16])
        off += 16
        if caplen > len(blob) - off:            # truncated final record
            break
        yield (s + us / div, blob[off:off + caplen])
        off += caplen


def _pcapng_records(blob: bytes) -> Iterator[tuple[float, bytes]]:
    """pcapng: Enhanced Packet Blocks only, timestamp resolution from the IDB."""
    off, endian, tsres = 0, "<", 6
    while off + 12 <= len(blob):
        btype = struct.unpack(endian + "I", blob[off:off + 4])[0]
        if btype == 0x0A0D0D0A:                 # Section Header Block
            bom = blob[off + 8:off + 12]
            endian = "<" if bom == b"\x4d\x3c\x2b\x1a" else ">"
            btype = 0x0A0D0D0A
        blen = struct.unpack(endian + "I", blob[off + 4:off + 8])[0]
        if blen < 12 or off + blen > len(blob):
            break
        body = blob[off + 8:off + blen - 4]
        if btype == 0x00000001 and len(body) >= 8:          # IDB
            # options carry if_tsresol (code 9, one octet)
            o = 8
            while o + 4 <= len(body):
                code, olen = struct.unpack(endian + "HH", body[o:o + 4])
                val = body[o + 4:o + 4 + olen]
                if code == 9 and olen >= 1:
                    tsres = val[0] & 0x7F
                o += 4 + ((olen + 3) & ~3)
                if code == 0:
                    break
        elif btype == 0x00000006 and len(body) >= 20:       # EPB
            _iface, tsh, tsl, caplen, _orig = struct.unpack(
                endian + "IIIII", body[0:20])
            ts = ((tsh << 32) | tsl) / float(10 ** tsres)
            yield (ts, body[20:20 + caplen])
        off += blen


def read_capture(path: str, tap_header: int = 0,
                 strip_fcs: bool = False) -> list[tuple[float, bytes]]:
    """Every frame of a pcap/pcapng as (timestamp, ethernet bytes).

    `tap_header` strips a fixed per-record prefix.  A ProfiShark inline tap
    writes a 28-BYTE RECORD HEADER before the Ethernet frame - every ether[]
    offset shifts by +28 - and it keeps the FCS, which is 4 trailing octets
    that are NOT part of the frame's own length arithmetic.  Both are documented
    in docs/findings/BENCH_TOPOLOGY.md and both have cost this project time.
    """
    with open(path, "rb") as f:
        blob = f.read()
    if blob[:4] == b"\x0a\x0d\x0d\x0a":
        recs = _pcapng_records(blob)
    else:
        recs = _pcap_records(blob)
    out = []
    for ts, data in recs:
        if tap_header:
            if len(data) <= tap_header:
                continue
            data = data[tap_header:]
        if strip_fcs and len(data) > 4:
            data = data[:-4]
        out.append((ts, data))
    return out


# -------------------------------------------------------------- frame decode --
@dataclass
class EthFrame:
    dst: bytes
    src: bytes
    tagged: bool
    pcp: Optional[int]
    dei: Optional[int]
    vid: Optional[int]
    ethertype: int
    payload: bytes
    wire_len: int

    @property
    def subtype(self) -> Optional[int]:
        if self.ethertype != ETH_P_AVTP or not self.payload:
            return None
        #: IEEE 1722-2016 4.4.3.2: "The 1-octet subtype field" - the WHOLE
        #: octet.  Masking off the top bit (the 1722-2011 cd bit) turns every
        #: control subtype into a stream one: 0xFA & 0x7F = 0x7A, and ADP
        #: silently stops being ADP.  Byte 0 is taken whole here.
        return self.payload[0]


def decode_eth(frame: bytes) -> Optional[EthFrame]:
    """Ethernet + at most one 802.1Q C-TAG (9.5/9.6).  None if too short."""
    if len(frame) < 14:
        return None
    dst, src = frame[0:6], frame[6:12]
    et = struct.unpack(">H", frame[12:14])[0]
    if et == TPID_C_TAG:
        if len(frame) < 18:
            return None
        tci = struct.unpack(">H", frame[14:16])[0]
        return EthFrame(dst, src, True, (tci >> 13) & 0x7, (tci >> 12) & 0x1,
                        tci & 0x0FFF, struct.unpack(">H", frame[16:18])[0],
                        frame[18:], len(frame))
    return EthFrame(dst, src, False, None, None, None, et, frame[14:],
                    len(frame))


@dataclass
class MrpAttribute:
    """One decoded MRP VectorAttribute value, flattened to one record per VALUE.

    802.1Q-2018 10.8.1.3 / 35.2.2: a VectorAttribute carries a FirstValue and
    NumberOfValues consecutive values, with a ThreePackedEvents vector giving each
    value's AttributeEvent, plus - for the MSRP Listener attribute only - a
    FourPackedEvents vector giving each value's declaration type.  Flattening to
    one record per value is what makes "is THIS stream_id declared" answerable.
    """
    protocol: str                       # "MSRP" | "MVRP"
    attr_type: int
    attr_name: str
    index: int                          # position within the vector
    event: str                          # New | JoinIn | In | JoinMt | Mt | Lv
    leave_all: int
    value: bytes                        # the FirstValue advanced to this index
    fields: dict = field(default_factory=dict)

    @property
    def declaring(self) -> bool:
        return self.event in MRP_DECLARING_EVENTS


def _three_packed(octet: int) -> tuple:
    """802.1Q-2018 10.7.6.2: three events packed as ((a*6)+b)*6+c."""
    a, rest = divmod(octet, 36)
    b, c = divmod(rest, 6)
    return (a, b, c)


def _four_packed(octet: int) -> tuple:
    """802.1Q-2018 35.2.2.8.2: four 2-bit declaration types per octet, MSB
    first."""
    return ((octet >> 6) & 3, (octet >> 4) & 3, (octet >> 2) & 3, octet & 3)


def _advance_stream_id(first: bytes, n: int) -> bytes:
    """802.1Q-2018 35.2.2.8: successive values of a Talker/Listener attribute
    increment the StreamID's unique_id (the low 2 octets of the 8-octet id)."""
    if n == 0 or len(first) < 8:
        return first
    sid = int.from_bytes(first[0:8], "big")
    return (((sid + n) & ((1 << 64) - 1)).to_bytes(8, "big") + first[8:])


def _decode_msrp_fields(attr_type: int, val: bytes) -> dict:
    """The FirstValue layouts, from 802.1Q-2018 35.2.2.8.

    Talker Advertise, 25 octets and measured on this bench:
      StreamID(8 = 6-octet MAC + 2-octet unique_id)
      DataFrameParameters(destination_address 6 + vlan_identifier 2)
      TSpec(MaxFrameSize 2 + MaxIntervalFrames 2)
      PriorityAndRank(1)   AccumulatedLatency(4)
    Listener, 8 octets: StreamID only - the declaration TYPE rides the
    FourPackedEvents vector, not the value.
    Domain, 4 octets: SRclassID(1) SRclassPriority(1) SRclassVID(2).
    """
    d = {}
    if attr_type in (MSRP_TALKER_ADVERTISE, MSRP_TALKER_FAILED) \
            and len(val) >= 25:
        d["stream_id"] = int.from_bytes(val[0:8], "big")
        d["stream_mac"] = val[0:6].hex()
        d["unique_id"] = int.from_bytes(val[6:8], "big")
        d["destination_address"] = val[8:14].hex()
        d["vlan_identifier"] = int.from_bytes(val[14:16], "big")
        d["max_frame_size"] = int.from_bytes(val[16:18], "big")
        d["max_interval_frames"] = int.from_bytes(val[18:20], "big")
        d["priority"] = (val[20] >> 5) & 0x7
        d["rank"] = (val[20] >> 4) & 0x1
        d["accumulated_latency"] = int.from_bytes(val[21:25], "big")
        if attr_type == MSRP_TALKER_FAILED and len(val) >= 34:
            d["failure_bridge_id"] = val[25:33].hex()
            d["failure_code"] = val[33]
    elif attr_type == MSRP_LISTENER and len(val) >= 8:
        d["stream_id"] = int.from_bytes(val[0:8], "big")
        d["stream_mac"] = val[0:6].hex()
        d["unique_id"] = int.from_bytes(val[6:8], "big")
    elif attr_type == MSRP_DOMAIN and len(val) >= 4:
        d["sr_class_id"] = val[0]
        d["sr_class_priority"] = val[1]
        d["sr_class_vid"] = int.from_bytes(val[2:4], "big")
    return d


def decode_mrpdu(payload: bytes, protocol: str) -> list:
    """An MRPDU -> a flat list of MrpAttribute, one per VALUE.

    802.1Q-2018 10.8.1: ProtocolVersion(1) then Message*, each
    AttributeType(1) AttributeLength(1) [AttributeListLength(2) for MSRP]
    VectorAttribute* EndMark(2), and the PDU ends with its own EndMark.

    Deliberately TOLERANT: a truncated capture is normal (a tap can start
    mid-PDU), so parsing stops at the first thing it cannot read and returns what
    it got.  A decoder that raised would turn a partial capture into no SRP
    visibility at all, which is worse than partial.
    """
    out: list = []
    if len(payload) < 2:
        return out
    off = 1                                     # ProtocolVersion
    while off + 1 < len(payload):
        atype = payload[off]
        if atype == 0:                          # PDU EndMark
            break
        alen = payload[off + 1]
        off += 2
        if protocol == "MSRP":
            if off + 2 > len(payload):
                break
            off += 2                            # AttributeListLength
        if alen == 0:
            break
        while off + 2 <= len(payload):
            vh = int.from_bytes(payload[off:off + 2], "big")
            if vh == 0:                         # Message EndMark
                off += 2
                break
            leave_all, nvals = (vh >> 13) & 0x7, vh & 0x1FFF
            off += 2
            if nvals == 0 or off + alen > len(payload):
                off = len(payload)
                break
            first = payload[off:off + alen]
            off += alen
            nev = (nvals + 2) // 3
            if off + nev > len(payload):
                break
            events = []
            for o in payload[off:off + nev]:
                events += list(_three_packed(o))
            off += nev
            decls = []
            if protocol == "MSRP" and atype == MSRP_LISTENER:
                nfp = (nvals + 3) // 4
                if off + nfp > len(payload):
                    break
                for o in payload[off:off + nfp]:
                    decls += list(_four_packed(o))
                off += nfp
            for i in range(nvals):
                val = _advance_stream_id(first, i) \
                    if atype in (MSRP_TALKER_ADVERTISE, MSRP_TALKER_FAILED,
                                 MSRP_LISTENER) else first
                f = _decode_msrp_fields(atype, val) if protocol == "MSRP" \
                    else {"vid": int.from_bytes(val[:2], "big")
                          if len(val) >= 2 else None}
                if i < len(decls):
                    f["declaration"] = MSRP_LISTENER_DECL.get(decls[i],
                                                              str(decls[i]))
                out.append(MrpAttribute(
                    protocol=protocol, attr_type=atype,
                    attr_name=(MSRP_ATTR_NAMES.get(atype, f"type{atype}")
                               if protocol == "MSRP" else "VID"),
                    index=i,
                    event=MRP_ATTR_EVENT.get(events[i] if i < len(events)
                                             else -1, "?"),
                    leave_all=leave_all, value=val, fields=f))
    return out


@dataclass
class AafPdu:
    sv: int
    version: int
    mr: int
    tv: int
    sequence_num: int
    tu: int
    stream_id: int
    avtp_timestamp: int
    fmt: int
    nsr: int
    channels_per_frame: int
    bit_depth: int
    stream_data_length: int
    sp: int
    evt: int
    payload: bytes

    @property
    def format_name(self) -> str:
        return AAF_FORMAT_NAMES.get(self.fmt, f"reserved({self.fmt:#x})")

    @property
    def sample_bits(self) -> Optional[int]:
        return AAF_FORMAT_BITS.get(self.fmt)

    @property
    def sample_frames(self) -> Optional[int]:
        """Sample events in the payload = sdl / (channels * sample octets)."""
        bits = self.sample_bits
        if not bits or not self.channels_per_frame:
            return None
        per = (bits // 8) * self.channels_per_frame
        return None if per == 0 or self.stream_data_length % per else \
            self.stream_data_length // per

    def sample(self, frame_idx: int, channel: int) -> Optional[int]:
        """One signed sample, per 7.3.5 (chronological, channels in order).

        Returns the sample as a signed integer of `sample_bits` width.  The
        left-justification our packetizer uses (24 valid bits in a 32-bit slot,
        sample << 8) is NOT undone here: the caller decides, because undoing it
        silently is how a real bit-depth defect would be hidden.
        """
        bits = self.sample_bits
        if bits is None or channel >= self.channels_per_frame:
            return None
        w = bits // 8
        off = (frame_idx * self.channels_per_frame + channel) * w
        if off + w > len(self.payload):
            return None
        raw = int.from_bytes(self.payload[off:off + w], "big")
        return raw - (1 << bits) if raw >> (bits - 1) else raw


def decode_aaf(pdu: bytes) -> Optional[AafPdu]:
    """IEEE 1722-2016 Figure 26.  None when the octets cannot be an AAF PCM
    AVTPDU - too short, or a subtype that is not AAF.  It does NOT reject a
    malformed-but-parseable frame: the checks report that, so a truncated
    payload has to survive decoding to be reported at all."""
    if len(pdu) < 24 or pdu[0] != SUBTYPE_AAF:
        return None
    b1 = pdu[1]
    sdl = struct.unpack(">H", pdu[20:22])[0]
    return AafPdu(
        sv=(b1 >> 7) & 1, version=(b1 >> 4) & 0x7, mr=(b1 >> 3) & 1,
        tv=b1 & 1, sequence_num=pdu[2], tu=pdu[3] & 1,
        stream_id=int.from_bytes(pdu[4:12], "big"),
        avtp_timestamp=struct.unpack(">I", pdu[12:16])[0],
        fmt=pdu[16], nsr=(pdu[17] >> 4) & 0xF,
        channels_per_frame=((pdu[17] & 0x03) << 8) | pdu[18],
        bit_depth=pdu[19], stream_data_length=sdl,
        sp=(pdu[22] >> 4) & 1, evt=pdu[22] & 0x0F,
        payload=pdu[24:24 + sdl] if sdl else pdu[24:])


@dataclass
class CrfPdu:
    sv: int
    version: int
    mr: int
    fs: int
    tu: int
    sequence_num: int
    type: int
    stream_id: int
    pull: int
    base_frequency: int
    crf_data_length: int
    timestamp_interval: int
    timestamps: list


def decode_crf(pdu: bytes) -> Optional[CrfPdu]:
    """IEEE 1722-2016 Figure 72 (the alternative header, clause 10.4)."""
    if len(pdu) < 20 or pdu[0] != SUBTYPE_CRF:
        return None
    b1 = pdu[1]
    dlen = struct.unpack(">H", pdu[16:18])[0]
    body = pdu[20:20 + dlen] if dlen else b""
    ts = [int.from_bytes(body[i:i + 8], "big")
          for i in range(0, (len(body) // 8) * 8, 8)]
    return CrfPdu(
        sv=(b1 >> 7) & 1, version=(b1 >> 4) & 0x7, mr=(b1 >> 3) & 1,
        fs=(b1 >> 1) & 1, tu=b1 & 1,
        sequence_num=pdu[2], type=pdu[3],
        stream_id=int.from_bytes(pdu[4:12], "big"),
        pull=(pdu[12] >> 5) & 0x7,
        base_frequency=int.from_bytes(pdu[12:16], "big") & 0x1FFFFFFF,
        crf_data_length=dlen,
        timestamp_interval=struct.unpack(">H", pdu[18:20])[0],
        timestamps=ts)


@dataclass
class ControlPdu:
    """The three header fields every AVTP control PDU shares (1722.1 9.2.1.1)
    plus the length arithmetic.  This is all the control-plane truth this file
    claims: the payload semantics belong to hive_compliance.py."""
    subtype: int
    sv: int
    version: int
    message_type: int
    valid_time_or_status: int
    control_data_length: int
    target_entity_id: int
    avtpdu_len: int

    @property
    def declared_avtpdu_len(self) -> int:
        """4 header octets + 8 target_entity_id octets + control_data_length.

        1722.1-2021 9.2.1.1.6: control_data_length counts the octets that
        FOLLOW the target_entity_id field.  A frame that carries fewer is the
        frame that lies about its own length.
        """
        return 12 + self.control_data_length


def decode_control(pdu: bytes) -> Optional[ControlPdu]:
    if len(pdu) < 12 or pdu[0] not in CONTROL_SUBTYPES:
        return None
    b1 = pdu[1]
    w = struct.unpack(">H", pdu[2:4])[0]
    return ControlPdu(subtype=pdu[0], sv=(b1 >> 7) & 1,
                      version=(b1 >> 4) & 0x7, message_type=b1 & 0x0F,
                      valid_time_or_status=(w >> 11) & 0x1F,
                      control_data_length=w & 0x07FF,
                      target_entity_id=int.from_bytes(pdu[4:12], "big"),
                      avtpdu_len=len(pdu))


# ------------------------------------------------------ stream_format qwords --
@dataclass
class AafStreamFormat:
    """IEEE 1722-2016 Annex I.2.4 / I.2.4.1."""
    subtype: int
    ut: int
    nsr: int
    fmt: int
    bit_depth: int
    channels_per_frame: int
    samples_per_frame: int

    @property
    def rate_hz(self) -> Optional[int]:
        return NSR_HZ.get(self.nsr)


def parse_aaf_stream_format(qword) -> Optional[AafStreamFormat]:
    n = int(str(qword), 16) if isinstance(qword, str) else int(qword)
    if (n >> 56) & 0x7F != SUBTYPE_AAF:
        return None
    return AafStreamFormat(subtype=SUBTYPE_AAF, ut=(n >> 52) & 1,
                           nsr=(n >> 48) & 0xF, fmt=(n >> 40) & 0xFF,
                           bit_depth=(n >> 32) & 0xFF,
                           channels_per_frame=(n >> 22) & 0x3FF,
                           samples_per_frame=(n >> 12) & 0x3FF)


@dataclass
class CrfStreamFormat:
    """IEEE 1722-2016 Annex I.2.6.  The base_frequency width is resolved from
    Milan v1.2 Table 7.1's own constant (see the module docstring)."""
    subtype: int
    type: int
    timestamp_interval: int
    timestamps_per_pdu: int
    pull: int
    base_frequency: int


def parse_crf_stream_format(qword) -> Optional[CrfStreamFormat]:
    n = int(str(qword), 16) if isinstance(qword, str) else int(qword)
    if (n >> 56) & 0x7F != SUBTYPE_CRF:
        return None
    return CrfStreamFormat(subtype=SUBTYPE_CRF, type=(n >> 52) & 0xF,
                           timestamp_interval=(n >> 40) & 0xFFF,
                           timestamps_per_pdu=(n >> 32) & 0xFF,
                           pull=(n >> 29) & 0x7,
                           base_frequency=n & 0x1FFFFFFF)


# ---------------------------------------------------------------- expectation --
@dataclass
class Expectation:
    """What the CONTROLLER was told, so the wire can be held to it.

    Every field is optional and an absent field makes its check SKIP rather
    than invent a value.  `aaf_format` is the 8-octet stream_format the
    controller read back with GET_STREAM_FORMAT - that is the whole point: the
    comparison is wire-versus-what-a-controller-was-promised.
    """
    aaf_format: Optional[int] = None
    crf_format: Optional[int] = None
    sr_vid: Optional[int] = SR_VID_DEFAULT
    sr_class_a_pcp: int = SR_CLASS_A_PCP
    #: stream_ids whose talker is bound but has no audio source; Milan 5.3.7.3
    #: says they still stream, so their payload must be present AND all-zero.
    silent_stream_ids: tuple = ()
    #: stream_ids that must carry non-zero audio
    fed_stream_ids: tuple = ()
    #: gPTP nanoseconds at the capture's first frame; without it the class-A
    #: transit check cannot run and says so.
    gptp_ref_ns: Optional[int] = None
    #: entity_ids expected to keep advertising through the capture
    adp_entity_ids: tuple = ()
    #: expected max transit / presentation offset in ns (SET_MAX_TRANSIT_TIME)
    max_transit_ns: int = CLASS_A_MAX_TRANSIT_NS
    #: stream_ids that MUST carry an MSRP Talker Advertise declaration.  Supply
    #: the entity's whole Stream Output set and the capture answers "which of my
    #: talkers never declared" - which is how a real fabric defect (only 2 of 5
    #: stream_ids declaring) was found from the wire alone.  Empty falls back to
    #: the stream_ids seen in the capture, which can only find a stream that is
    #: streaming WITHOUT a declaration, never one that is silently undeclared.
    talker_stream_ids: tuple = ()


# ------------------------------------------------------------------- analysis --
def _mod_delta(a: int, b: int, mod: int) -> int:
    """Forward distance from b to a, modulo `mod`."""
    return (a - b) % mod


class WireTruth:
    """Accumulates per-stream state over a capture, then renders verdicts.

    Every check has a stable name and carries its clause.  Adding one is a
    method plus one line in `checks()`; that is the extension contract, and it
    is the same contract torture_campaign.py uses (see
    docs/testing/RUNNING_TESTS.md).
    """

    def __init__(self, expect: Optional[Expectation] = None):
        self.expect = expect or Expectation()
        self.frames = 0
        self.non_avtp = 0
        self.aaf: dict[int, list] = {}
        self.crf: dict[int, list] = {}
        self.adp: dict[int, list] = {}
        self.control: list = []
        self.untagged_stream_frames = 0
        self.short_frames = 0
        #: MSRP / MVRP attributes, one record per VALUE.  These frames go to
        #: 01:80:C2:00:00:0E, which a bridge does NOT forward, so an INLINE TAP
        #: is the only place they can be seen - and therefore the only place the
        #: Listener Ready half of the Milan v1.2 5.3.7.3 licence is visible.
        self.mrp: list = []
        self.msrp_frames = 0
        self.mvrp_frames = 0

    # -- ingest ------------------------------------------------------------
    def feed(self, ts: float, raw: bytes) -> None:
        self.frames += 1
        eth = decode_eth(raw)
        if eth is None:
            self.short_frames += 1
            return
        if eth.ethertype in (ETH_P_MSRP, ETH_P_MVRP):
            proto = "MSRP" if eth.ethertype == ETH_P_MSRP else "MVRP"
            if proto == "MSRP":
                self.msrp_frames += 1
            else:
                self.mvrp_frames += 1
            for at in decode_mrpdu(eth.payload, proto):
                self.mrp.append((ts, eth, at))
            return
        if eth.ethertype != ETH_P_AVTP:
            self.non_avtp += 1
            return
        st = eth.subtype
        if st == SUBTYPE_AAF:
            pdu = decode_aaf(eth.payload)
            if pdu:
                self.aaf.setdefault(pdu.stream_id, []).append((ts, eth, pdu))
                if not eth.tagged:
                    self.untagged_stream_frames += 1
        elif st == SUBTYPE_CRF:
            pdu = decode_crf(eth.payload)
            if pdu:
                self.crf.setdefault(pdu.stream_id, []).append((ts, eth, pdu))
                if not eth.tagged:
                    self.untagged_stream_frames += 1
        elif st in CONTROL_SUBTYPES:
            c = decode_control(eth.payload)
            if c:
                self.control.append((ts, eth, c))
                if st == SUBTYPE_ADP:
                    ai = (struct.unpack(">I", eth.payload[36:40])[0]
                          if len(eth.payload) >= 40 else None)
                    self.adp.setdefault(c.target_entity_id, []).append(
                        (ts, eth.wire_len, c, ai))

    def feed_capture(self, records: Iterable[tuple[float, bytes]]) -> "WireTruth":
        for ts, raw in records:
            self.feed(ts, raw)
        return self

    # -- checks ------------------------------------------------------------
    def checks(self) -> list[Verdict]:
        out: list[Verdict] = []
        out += self.check_capture_shape()
        out += self.check_aaf_declared_vs_wire()
        out += self.check_aaf_header_legality()
        out += self.check_aaf_payload_arithmetic()
        out += self.check_sequence_continuity()
        out += self.check_aaf_timestamps()
        out += self.check_vlan_class()
        out += self.check_zero_fill()
        out += self.check_crf_format()
        out += self.check_crf_rate()
        out += self.check_adp_frame_rule()
        out += self.check_control_length_honesty()
        out += self.check_srp_declarations()
        return out

    def check_capture_shape(self) -> list[Verdict]:
        """A capture with no stream frames must not read as a clean pass - the
        commonest false green in this project is an empty capture (a mirror
        port that never subscribed to the multicast group)."""
        n = sum(len(v) for v in self.aaf.values()) + \
            sum(len(v) for v in self.crf.values())
        return [Verdict("wt.capture.stream-frames-present",
                        "PASS" if n else "FAIL",
                        "docs/findings/BENCH_TOPOLOGY.md - a mirror port sees "
                        "control frames only; stream truth needs an inline tap",
                        {"frames": self.frames, "stream_frames": n,
                         "aaf_streams": len(self.aaf),
                         "crf_streams": len(self.crf),
                         "non_avtp": self.non_avtp,
                         "undecodable": self.short_frames})]

    def check_aaf_declared_vs_wire(self) -> list[Verdict]:
        want = self.expect.aaf_format
        if want is None:
            return [Verdict("wt.aaf.declared-vs-wire", "SKIP",
                            "IEEE 1722-2016 I.2.4.1",
                            {"why": "no declared stream_format supplied - pass "
                                    "the GET_STREAM_FORMAT readback with "
                                    "--expect-aaf-format"})]
        d = parse_aaf_stream_format(want)
        if d is None:
            return [Verdict("wt.aaf.declared-vs-wire", "FAIL",
                            "IEEE 1722-2016 I.2.4",
                            {"why": "declared format is not an AAF format",
                             "declared": f"{int(want):016x}"})]
        out = []
        for sid, recs in sorted(self.aaf.items()):
            _, _, p = recs[0]
            bad = {}
            if p.channels_per_frame != d.channels_per_frame:
                bad["channels_per_frame"] = [d.channels_per_frame,
                                             p.channels_per_frame]
            if p.nsr != d.nsr:
                bad["nsr"] = [d.nsr, p.nsr]
            if p.fmt != d.fmt:
                bad["format"] = [d.fmt, p.fmt]
            if p.bit_depth != d.bit_depth:
                bad["bit_depth"] = [d.bit_depth, p.bit_depth]
            spf = p.sample_frames
            if spf is not None and d.samples_per_frame and \
                    spf != d.samples_per_frame:
                bad["samples_per_frame"] = [d.samples_per_frame, spf]
            out.append(_v(f"wt.aaf.declared-vs-wire.{sid:016x}", not bad,
                          "IEEE 1722-2016 I.2.4.1: the stream_format field "
                          "'matches the setting of the ... field in the Stream "
                          "AVTPDU when this stream format is the current "
                          "format for the stream'",
                          declared=f"{int(want):016x}", mismatches=bad,
                          measured_on_frames=len(recs)))
        return out or [Verdict("wt.aaf.declared-vs-wire", "SKIP",
                               "IEEE 1722-2016 I.2.4.1",
                               {"why": "no AAF frames in the capture"})]

    def check_aaf_header_legality(self) -> list[Verdict]:
        """The field-legality rules that hold with NO declaration at all."""
        if not self.aaf:
            return [_nothing_to_check(
                "wt.aaf.header-legal",
                "IEEE 1722-2016 7.3.3, 7.3.4, Tables 9 and 11", "AAF frames")]
        out = []
        for sid, recs in sorted(self.aaf.items()):
            bad = []
            for _, _, p in recs:
                if p.channels_per_frame == 0:
                    bad.append("channels_per_frame 0 (7.3.3: > 0)")
                if p.bit_depth == 0:
                    bad.append("bit_depth 0 (7.3.4: not zero)")
                sb = p.sample_bits
                if sb and p.bit_depth > sb:
                    bad.append(f"bit_depth {p.bit_depth} > format width {sb} "
                               "(7.3.4)")
                if p.fmt not in AAF_FORMAT_NAMES:
                    bad.append(f"format {p.fmt:#x} reserved (Table 9)")
                if p.nsr not in NSR_HZ:
                    bad.append(f"nsr {p.nsr:#x} reserved (Table 11)")
                if p.sv != 1:
                    bad.append("sv 0 with a stream_id present (4.4.4.2)")
                if p.version != 0:
                    bad.append(f"version {p.version} (4.4.4.3: 0)")
                if bad:
                    break
            out.append(_v(f"wt.aaf.header-legal.{sid:016x}", not bad,
                          "IEEE 1722-2016 7.3.3, 7.3.4, Tables 9 and 11",
                          violations=sorted(set(bad)), frames=len(recs)))
        return out

    def check_aaf_payload_arithmetic(self) -> list[Verdict]:
        """stream_data_length must describe the payload that is really there,
        and must divide evenly into whole sample events (7.3.5)."""
        if not self.aaf:
            return [_nothing_to_check(
                "wt.aaf.payload-arithmetic",
                "IEEE 1722-2016 4.4.4.10 + 7.3.5", "AAF frames")]
        out = []
        for sid, recs in sorted(self.aaf.items()):
            bad = []
            for _, eth, p in recs:
                if len(p.payload) < p.stream_data_length:
                    bad.append(f"sdl {p.stream_data_length} > payload "
                               f"{len(p.payload)}")
                if p.sample_frames is None:
                    bad.append(f"sdl {p.stream_data_length} is not a whole "
                               f"number of {p.channels_per_frame}-channel "
                               f"sample events at format "
                               f"{p.format_name}")
                if bad:
                    break
            spf = {p.sample_frames for _, _, p in recs}
            out.append(_v(f"wt.aaf.payload-arithmetic.{sid:016x}", not bad,
                          "IEEE 1722-2016 4.4.4.10 stream_data_length + 7.3.5 "
                          "interleaved sample events",
                          violations=bad, sample_frames_seen=sorted(
                              x for x in spf if x is not None)))
        return out

    def check_sequence_continuity(self) -> list[Verdict]:
        """4.4.4.6 for AAF and 10.4.6 for CRF: +1 with wrapping.  A Listener
        may JOIN at any value (10.4.6), so the first frame sets the base and is
        never a gap."""
        out = []
        for kind, table, mod, clause in (
                ("aaf", self.aaf, 256, "IEEE 1722-2016 4.4.4.6"),
                ("crf", self.crf, 256, "IEEE 1722-2016 10.4.6 (ONE octet, "
                                       "FF16 -> 0016)")):
            if not table:
                out.append(_nothing_to_check(f"wt.{kind}.seq-continuity",
                                             clause, f"{kind.upper()} frames"))
                continue
            for sid, recs in sorted(table.items()):
                gaps, prev = [], None
                for i, (ts, _, p) in enumerate(recs):
                    if prev is not None:
                        step = _mod_delta(p.sequence_num, prev, mod)
                        if step != 1:
                            gaps.append({"at_frame": i, "prev": prev,
                                         "got": p.sequence_num, "step": step})
                    prev = p.sequence_num
                out.append(_v(f"wt.{kind}.seq-continuity.{sid:016x}",
                              not gaps, clause,
                              gaps=gaps[:8], gap_count=len(gaps),
                              frames=len(recs)))
        return out

    def check_aaf_timestamps(self) -> list[Verdict]:
        """Three separate properties, kept separate on purpose.

        (a) tv: with sp = 0 every AVTPDU carries a valid presentation time
            (4.4.4.5 / 7.5), so tv = 0 on a normal frame is a finding.
        (b) the presentation-time STEP between consecutive frames equals
            sample_frames / fs - that is a property of the wire alone and needs
            no gPTP reference.
        (c) the presentation OFFSET against gPTP, which needs a reference and
            SKIPS without one rather than guessing.
        """
        if not self.aaf:
            return [_nothing_to_check(n, c, "AAF frames") for n, c in (
                ("wt.aaf.tv-set", "IEEE 1722-2016 4.4.4.5 tv / 7.5"),
                ("wt.aaf.pts-step", "IEEE 1722-2016 7.5 / Milan 5.3.7.6"),
                ("wt.aaf.class-a-transit", "802.1BA-2011 class A 2 ms"))]
        out = []
        for sid, recs in sorted(self.aaf.items()):
            tv_bad = [i for i, (_, _, p) in enumerate(recs)
                      if p.sp == 0 and p.tv == 0]
            out.append(_v(f"wt.aaf.tv-set.{sid:016x}", not tv_bad,
                          "IEEE 1722-2016 4.4.4.5 tv / 7.5 sparse mode",
                          frames_without_tv=len(tv_bad),
                          first_offenders=tv_bad[:8]))

            _, _, p0 = recs[0]
            fs = NSR_HZ.get(p0.nsr)
            spf = p0.sample_frames
            if fs and spf:
                want = round(spf * 1e9 / fs)
                steps, bad = [], []
                for i in range(1, len(recs)):
                    a = recs[i - 1][2].avtp_timestamp
                    b = recs[i][2].avtp_timestamp
                    d = _mod_delta(b, a, AVTP_TS_MOD)
                    steps.append(d)
                    # one media clock tick of slack: the framer times off the
                    # audio clock, so +/- 1 sample period is honest jitter
                    if abs(d - want) > round(1e9 / fs) + 1:
                        bad.append({"at_frame": i, "step_ns": d})
                out.append(_v(f"wt.aaf.pts-step.{sid:016x}",
                              not bad and len(steps) > 0,
                              "IEEE 1722-2016 7.5 / Milan 5.3.7.6: the "
                              "presentation time advances by one AVTPDU of "
                              "media, so the step is sample_frames/fs",
                              expected_step_ns=want, steps=len(steps),
                              violations=bad[:8], violation_count=len(bad)))
            else:
                out.append(Verdict(f"wt.aaf.pts-step.{sid:016x}", "SKIP",
                                   "IEEE 1722-2016 7.5",
                                   {"why": "nsr is 'user specified' or the "
                                           "payload is not a whole number of "
                                           "sample events - no nominal step "
                                           "exists on the wire"}))

            if self.expect.gptp_ref_ns is None:
                out.append(Verdict(f"wt.aaf.class-a-transit.{sid:016x}", "SKIP",
                                   "802.1BA-2011 class A 2 ms",
                                   {"why": "no gPTP reference supplied; a pcap "
                                           "timestamp is the capture host's "
                                           "CLOCK_REALTIME and comparing it to "
                                           "an AVTP timestamp produces a "
                                           "confident number that means "
                                           "nothing (methodology R5)",
                                    "supply": "--gptp-ref-ns"}))
            else:
                t0 = recs[0][0]
                bad = []
                for i, (ts, _, p) in enumerate(recs):
                    now = (self.expect.gptp_ref_ns
                           + round((ts - t0) * 1e9)) % AVTP_TS_MOD
                    ahead = _mod_delta(p.avtp_timestamp, now, AVTP_TS_MOD)
                    # a presentation time in the past decodes as ~2^32 ahead
                    if ahead > self.expect.max_transit_ns:
                        bad.append({"at_frame": i, "ahead_ns": ahead})
                out.append(_v(f"wt.aaf.class-a-transit.{sid:016x}", not bad,
                              "802.1BA-2011 / Milan: class A presentation is "
                              "within 2 ms of transmission",
                              budget_ns=self.expect.max_transit_ns,
                              violations=bad[:8], violation_count=len(bad)))
        return out

    def check_vlan_class(self) -> list[Verdict]:
        """802.1Q 9.5/9.6 + Milan 7.3.3 for CRF: every SR stream frame carries
        a C-TAG with the SR class A PCP, DEI 0, and the SR VID.  VID 0 gets its
        own verdict line because it is not merely wrong, it is the specific
        past defect that made frames flood unshaped."""
        out = []
        for kind, table in (("aaf", self.aaf), ("crf", self.crf)):
            if not table:
                out += [_nothing_to_check(
                    f"wt.{kind}.c-tag-{w}",
                    "802.1Q-2018 9.5/9.6 + Milan v1.2 7.3.3 / 4.2.7.2.1",
                    f"{kind.upper()} frames")
                    for w in ("present", "pcp", "dei", "vid")]
                continue
            for sid, recs in sorted(table.items()):
                untagged = sum(1 for _, e, _ in recs if not e.tagged)
                pcps = sorted({e.pcp for _, e, _ in recs if e.tagged})
                deis = sorted({e.dei for _, e, _ in recs if e.tagged})
                vids = sorted({e.vid for _, e, _ in recs if e.tagged})
                out.append(_v(f"wt.{kind}.c-tag-present.{sid:016x}",
                              untagged == 0,
                              "802.1Q-2018 9.5 + Milan v1.2 7.3.3 (CRF) / "
                              "4.2.7.2.1: an SR stream is carried tagged; an "
                              "undeclared multicast DMAC is just multicast and "
                              "floods (measured 2026-07-28: 4001 untagged CRF "
                              "frames in 8 s)",
                              untagged_frames=untagged, frames=len(recs)))
                out.append(_v(f"wt.{kind}.c-tag-pcp.{sid:016x}",
                              pcps == [self.expect.sr_class_a_pcp],
                              "802.1Q-2018 34.5 / Milan v1.2 4.2.7.2.1: SR "
                              "class A priority",
                              expected=self.expect.sr_class_a_pcp,
                              observed=pcps))
                out.append(_v(f"wt.{kind}.c-tag-dei.{sid:016x}",
                              deis in ([0], []),
                              "802.1Q-2018 9.6: an SR class A stream is never "
                              "drop-eligible", observed=deis))
                if self.expect.sr_vid is None:
                    out.append(Verdict(f"wt.{kind}.c-tag-vid.{sid:016x}",
                                       "SKIP", "802.1Q-2018 9.6",
                                       {"why": "no SR VID supplied"}))
                else:
                    out.append(_v(f"wt.{kind}.c-tag-vid.{sid:016x}",
                                  vids == [self.expect.sr_vid],
                                  "802.1Q-2018 9.6 + the bench SR VID: VID 0 "
                                  "leaves the reserved SR tree, is stripped on "
                                  "egress and floods unshaped",
                                  expected=self.expect.sr_vid, observed=vids,
                                  vid_zero_seen=0 in vids))
        return out

    def check_zero_fill(self) -> list[Verdict]:
        """Milan 5.3.7.3: a bound talker STREAMS.  So a talker with no audio
        source owes present-and-silent frames, and a fed one owes non-zero
        samples.  Both directions are asserted, because a check that can only
        say 'silent' cannot tell zero-fill from a dead framer."""
        out = []
        if not self.expect.silent_stream_ids and not self.expect.fed_stream_ids:
            out.append(Verdict(
                "wt.aaf.zero-fill", "SKIP", "Milan v1.2 5.3.7.3",
                {"why": "no stream was declared silent-but-bound or fed, so "
                        "'silence' and 'absence' cannot be told apart here; "
                        "pass --silent-stream / --fed-stream",
                 "absent": "a silent/fed declaration"}))
        for sid in self.expect.silent_stream_ids:
            recs = self.aaf.get(int(sid), [])
            if not recs:
                out.append(_v(f"wt.aaf.zero-fill-present.{int(sid):016x}",
                              False,
                              "Milan v1.2 5.3.7.3: 'As long as a PAAD is "
                              "declaring a Talker Advertise attribute and "
                              "receiving a Listener Ready or Listener Ready "
                              "Failed attribute for a Stream Output, it shall "
                              "be streaming AVTP packets'",
                              why="declared silent-but-bound and NO frames "
                                  "reached the tap - silence is not the same "
                                  "as absence"))
                continue
            nz = [i for i, (_, _, p) in enumerate(recs)
                  if any(b for b in p.payload)]
            out.append(_v(f"wt.aaf.zero-fill-silent.{int(sid):016x}", not nz,
                          "Milan v1.2 5.3.7.3 + 5.3.7.3 zero-fill: an unfed "
                          "bound talker frames silence",
                          frames=len(recs), non_zero_frames=len(nz)))
        for sid in self.expect.fed_stream_ids:
            recs = self.aaf.get(int(sid), [])
            nz = [i for i, (_, _, p) in enumerate(recs)
                  if any(b for b in p.payload)]
            out.append(_v(f"wt.aaf.fed-non-silent.{int(sid):016x}",
                          bool(recs) and len(nz) == len(recs),
                          "IEEE 1722-2016 7.3.5: a fed talker's payload "
                          "carries samples; all-zero on a fed stream is the "
                          "silence defect, not zero-fill",
                          frames=len(recs), non_zero_frames=len(nz)))
        return out

    def check_crf_format(self) -> list[Verdict]:
        """Milan 7.3.2 pins base_frequency, timestamps_per_pdu and
        timestamp_interval; Table 7.1 pins type and pull too."""
        out = []
        if not self.crf:
            return [_nothing_to_check("wt.crf.milan-format",
                                      "Milan v1.2 7.3.2 + Table 7.1",
                                      "CRF frames")]
        want = self.expect.crf_format if self.expect.crf_format is not None \
            else MILAN_CRF_FORMAT
        d = parse_crf_stream_format(want)
        for sid, recs in sorted(self.crf.items()):
            _, _, p = recs[0]
            bad = {}
            if p.base_frequency != d.base_frequency:
                bad["base_frequency"] = [d.base_frequency, p.base_frequency]
            if p.timestamp_interval != d.timestamp_interval:
                bad["timestamp_interval"] = [d.timestamp_interval,
                                             p.timestamp_interval]
            if p.type != d.type:
                bad["type"] = [d.type, p.type]
            if p.pull != d.pull:
                bad["pull"] = [d.pull, p.pull]
            tspp = p.crf_data_length // 8
            if tspp != d.timestamps_per_pdu:
                bad["timestamps_per_pdu"] = [d.timestamps_per_pdu, tspp]
            if p.crf_data_length % 8:
                bad["crf_data_length"] = ["multiple of 8", p.crf_data_length]
            out.append(_v(f"wt.crf.milan-format.{sid:016x}", not bad,
                          "Milan v1.2 7.3.2: 'The base frequency shall be "
                          "48000Hz.  Each PDU shall contain 1 timestamp, and "
                          "the timestamp interval shall be 96.' + Table 7.1",
                          declared=f"{int(want):016x}", mismatches=bad,
                          frames=len(recs)))
        return out

    def check_crf_rate(self) -> list[Verdict]:
        """The PDU rate the format DEMANDS versus the rate on the wire, and the
        timestamp step inside the stream.  base_frequency / (interval * per_pdu)
        = 48000/96 = 500 PDU/s = one every 2 ms."""
        if not self.crf:
            return [_nothing_to_check(n, "Milan v1.2 7.3.2 + IEEE 1722-2016 "
                                         "10.4.12/10.4.13", "CRF frames")
                    for n in ("wt.crf.pdu-rate", "wt.crf.timestamp-step")]
        out = []
        for sid, recs in sorted(self.crf.items()):
            _, _, p = recs[0]
            per = max(1, p.crf_data_length // 8)
            if not p.timestamp_interval or not p.base_frequency:
                out.append(Verdict(f"wt.crf.pdu-rate.{sid:016x}", "SKIP",
                                   "Milan v1.2 7.3.2",
                                   {"why": "interval or base_frequency is 0"}))
                continue
            want_pps = p.base_frequency / (p.timestamp_interval * per)
            span = recs[-1][0] - recs[0][0]
            got = (len(recs) - 1) / span if span > 0 else None
            ok = got is not None and abs(got - want_pps) <= max(
                1.0, 0.05 * want_pps)
            out.append(Verdict(f"wt.crf.pdu-rate.{sid:016x}",
                               "PASS" if ok else ("SKIP" if got is None
                                                  else "FAIL"),
                               "Milan v1.2 7.3.2 + IEEE 1722-2016 10.4.12: "
                               "base_frequency / (timestamp_interval x "
                               "timestamps_per_pdu)",
                               {"expected_pps": want_pps, "observed_pps": got,
                                "frames": len(recs), "span_s": span}))
            step_ns = round(p.timestamp_interval * 1e9 / p.base_frequency)
            bad = []
            for i in range(1, len(recs)):
                a = recs[i - 1][2].timestamps[-1] if recs[i - 1][2].timestamps \
                    else None
                b = recs[i][2].timestamps[0] if recs[i][2].timestamps else None
                if a is None or b is None:
                    continue
                d = b - a
                if abs(d - step_ns * per) > step_ns:
                    bad.append({"at_frame": i, "step_ns": d})
            out.append(_v(f"wt.crf.timestamp-step.{sid:016x}", not bad,
                          "IEEE 1722-2016 10.4.12/10.4.13: consecutive CRF "
                          "timestamps are one timestamp_interval of media "
                          "events apart",
                          expected_step_ns=step_ns * per,
                          violations=bad[:8], violation_count=len(bad)))
        return out

    def check_adp_frame_rule(self) -> list[Verdict]:
        """The 82-byte ADPDU rule and the available_index monotonicity.

        1722.1-2021 6.2.1: the ADPDU is 68 octets, so 82 on the wire, and
        control_data_length is 56.  6.2.2.10: available_index increments on
        every transmitted ADPDU - a repeated value makes a controller treat the
        entity as incoherent, which is exactly what bump-on-change-only did to
        us in 2026-07-12.
        """
        out = []
        if not self.adp:
            out += [_nothing_to_check(n, "IEEE 1722.1-2021 6.2.1 / 6.2.2.10",
                                      "ADPDUs")
                    for n in ("wt.adp.frame-82",
                              "wt.adp.available-index-advances")]
        for eid, recs in sorted(self.adp.items()):
            wrong_len = [(n, l) for n, (_, l, _, _) in enumerate(recs)
                         if l != ADP_FRAME_LEN]
            wrong_cdl = [(n, c.control_data_length)
                         for n, (_, _, c, _) in enumerate(recs)
                         if c.control_data_length != ADP_CDL]
            out.append(_v(f"wt.adp.frame-82.{eid:016x}",
                          not wrong_len and not wrong_cdl,
                          "IEEE 1722.1-2021 6.2.1: a 4-octet control header + "
                          "an 8-octet entity_id + 56 octets = 68, i.e. 82 on "
                          "the wire with the Ethernet header",
                          expected_frame_len=ADP_FRAME_LEN,
                          expected_cdl=ADP_CDL,
                          wrong_length=wrong_len[:8],
                          wrong_cdl=wrong_cdl[:8], adpdus=len(recs)))
            idx = [ai for _, _, _, ai in recs if ai is not None]
            repeats = [i for i in range(1, len(idx))
                       if _mod_delta(idx[i], idx[i - 1], 1 << 32) == 0]
            out.append(_v(f"wt.adp.available-index-advances.{eid:016x}",
                          not repeats and len(idx) > 1,
                          "IEEE 1722.1-2021 6.2.2.10: available_index "
                          "increments on every transmitted ADPDU; a repeated "
                          "index reads as an incoherent entity",
                          adpdus=len(idx), repeats=len(repeats),
                          first=idx[0] if idx else None,
                          last=idx[-1] if idx else None))
        for eid in self.expect.adp_entity_ids:
            e = int(eid)
            out.append(_v(f"wt.adp.alive.{e:016x}", e in self.adp,
                          "IEEE 1722.1-2021 6.2.6: an available entity "
                          "re-advertises within valid_time; silence for the "
                          "whole capture is the dormancy signature",
                          adpdus=len(self.adp.get(e, []))))
        return out

    def check_control_length_honesty(self) -> list[Verdict]:
        """The frame must be at least as long as it claims to be.  This is the
        check a status-byte-only tool cannot make, and the defect it catches is
        real: a frame that declares control_data_length 84 and puts 20 octets
        on the wire."""
        if not self.control:
            return [_nothing_to_check(
                "wt.control.length-honest",
                "IEEE 1722.1-2021 9.2.1.1.6", "control frames (ADP/AECP/ACMP/"
                "MAAP)")]
        liars = []
        for i, (_, eth, c) in enumerate(self.control):
            if c.avtpdu_len < c.declared_avtpdu_len:
                liars.append({"n": i, "subtype": SUBTYPE_NAMES.get(c.subtype),
                              "cdl": c.control_data_length,
                              "declared_avtpdu": c.declared_avtpdu_len,
                              "actual_avtpdu": c.avtpdu_len})
        return [_v("wt.control.length-honest", not liars,
                   "IEEE 1722.1-2021 9.2.1.1.6: control_data_length counts the "
                   "octets after target_entity_id; a shorter frame is "
                   "malformed however correct its status byte is",
                   control_frames=len(self.control), liars=liars[:8],
                   liar_count=len(liars))]


    # -- SRP, which only the inline tap can see ---------------------------
    def srp_state(self) -> dict:
        """The SRP declarations the capture actually contains, per stream_id."""
        talkers, listeners, domains, vids = {}, {}, [], []
        for _ts, _e, at in self.mrp:
            f = at.fields
            if at.protocol == "MVRP":
                if at.declaring and f.get("vid") is not None:
                    vids.append(f["vid"])
                continue
            if at.attr_type in (MSRP_TALKER_ADVERTISE, MSRP_TALKER_FAILED):
                sid = f.get("stream_id")
                if sid is None:
                    continue
                rec = talkers.setdefault(sid, {"advertise": False,
                                               "failed": False,
                                               "withdrawn": False, "fields": f})
                if at.attr_type == MSRP_TALKER_ADVERTISE:
                    rec["advertise"] = rec["advertise"] or at.declaring
                else:
                    rec["failed"] = rec["failed"] or at.declaring
                if not at.declaring:
                    rec["withdrawn"] = True
                rec["fields"] = f
                rec["last_event"] = at.event
            elif at.attr_type == MSRP_LISTENER:
                sid = f.get("stream_id")
                if sid is None:
                    continue
                rec = listeners.setdefault(sid, {"declarations": [],
                                                 "ready": False})
                rec["declarations"].append(
                    {"event": at.event,
                     "declaration": f.get("declaration")})
                if at.declaring and f.get("declaration") in ("Ready",
                                                             "Ready Failed"):
                    rec["ready"] = True
            elif at.attr_type == MSRP_DOMAIN and at.declaring:
                domains.append(f)
        return {"talkers": talkers, "listeners": listeners,
                "domains": domains, "mvrp_vids": sorted(set(vids))}

    def check_srp_declarations(self) -> list[Verdict]:
        """The SRP half of the Milan v1.2 5.3.7.3 licence, from the WIRE.

        5.3.7.3: "As long as a PAAD is declaring a Talker Advertise attribute
        and receiving a Listener Ready or Listener Ready Failed attribute for a
        Stream Output, it shall be streaming AVTP packets."  Both halves of that
        conjunction are MSRP declarations on 01:80:C2:00:00:0E, which no bridge
        forwards - so this is the ONE check set that CANNOT be made from the
        controller host and CAN be made from an inline tap.  Its value is proven:
        it is how "only 2 of 5 talker stream_ids declare a Talker Advertise" was
        found, from the wire, with no board access at all.

        5.3.7.4 makes the Stream Destination MAC Address and the Stream VLAN ID
        SRP parameters of the Stream Output, so the declaration and the frames
        must agree about both - a stream whose DMAC or VID differs from its own
        declaration is riding outside its reservation.
        """
        out = []
        if not self.mrp:
            return [_nothing_to_check(
                n, "802.1Q-2018 35.2.2 + Milan v1.2 5.3.7.3: MSRP/MVRP go to "
                   "01:80:C2:00:00:0E, which a bridge does not forward, so only "
                   "an INLINE TAP can see them",
                "MSRP/MVRP frames (an inline tap capture is required; a mirror "
                "port and the controller host can never see these)")
                for n in ("wt.msrp.talker-advertise-declared",
                          "wt.msrp.listener-declaration-present",
                          "wt.msrp.declared-dmac-matches-wire",
                          "wt.msrp.declared-vid-matches-wire",
                          "wt.msrp.tspec-declared",
                          "wt.msrp.domain-declared",
                          "wt.mvrp.sr-vid-declared")]
        st = self.srp_state()
        streaming = sorted(self.aaf) + sorted(self.crf)
        expected = sorted(int(s) for s in self.expect.talker_stream_ids) \
            or streaming

        # (1) every stream that IS on the wire, and every stream the controller
        #     says should be, must have a Talker Advertise declared for it
        if not expected:
            out.append(Verdict("wt.msrp.talker-advertise-declared", "SKIP",
                               "Milan v1.2 5.3.7.4",
                               {"why": "no stream frames in the capture and no "
                                       "--talker-stream given, so there is no "
                                       "stream whose declaration to look for"}))
        else:
            missing = [f"{s:016x}" for s in expected
                       if not st["talkers"].get(s, {}).get("advertise")]
            failed = [f"{s:016x}" for s in expected
                      if st["talkers"].get(s, {}).get("failed")]
            out.append(_v("wt.msrp.talker-advertise-declared", not missing,
                          "Milan v1.2 5.3.7.2: 'For each of the Stream Outputs "
                          "of its currently set Configuration, a PAAD shall "
                          "always declare an MSRP Talker attribute as soon as it "
                          "has valid SRP parameters for this stream' + 802.1Q-"
                          "2018 35.2.2.8.3",
                          expected=[f"{s:016x}" for s in expected],
                          declared=sorted(f"{s:016x}" for s, r
                                          in st["talkers"].items()
                                          if r.get("advertise")),
                          missing=missing, talker_failed=failed,
                          streams_on_the_wire=[f"{s:016x}" for s in streaming]))

        # (2) the LISTENER half of the licence
        if not streaming:
            out.append(Verdict("wt.msrp.listener-declaration-present", "SKIP",
                               "Milan v1.2 5.3.7.3",
                               {"why": "no stream frames in the capture, so no "
                                       "stream needs a Listener declaration"}))
        else:
            unlicensed = [f"{s:016x}" for s in streaming
                          if not st["listeners"].get(s, {}).get("ready")]
            out.append(_v("wt.msrp.listener-declaration-present",
                          not unlicensed,
                          "Milan v1.2 5.3.7.3: a talker is licensed to stream "
                          "only while it is 'receiving a Listener Ready or "
                          "Listener Ready Failed attribute for a Stream "
                          "Output', so frames on the wire without one are "
                          "unreserved",
                          streaming=[f"{s:016x}" for s in streaming],
                          listener_declarations={
                              f"{s:016x}": r["declarations"][-3:]
                              for s, r in st["listeners"].items()},
                          without_listener_ready=unlicensed))

        # (3) the declaration and the frames must agree about DMAC and VID
        for name, key, getter, clause in (
                ("wt.msrp.declared-dmac-matches-wire", "destination_address",
                 lambda e: e.dst.hex(),
                 "Milan v1.2 5.3.7.4: the Stream Destination MAC Address is an "
                 "SRP parameter of the Stream Output, so the declared "
                 "DataFrameParameters.destination_address and the wire DMAC are "
                 "one value"),
                ("wt.msrp.declared-vid-matches-wire", "vlan_identifier",
                 lambda e: e.vid,
                 "Milan v1.2 5.3.7.4 + 802.1Q-2018 9.6: the Stream VLAN ID is "
                 "an SRP parameter, so the declared vlan_identifier and the "
                 "C-TAG VID are one value")):
            bad, checked = {}, []
            for table in (self.aaf, self.crf):
                for sid, recs in table.items():
                    decl = st["talkers"].get(sid, {}).get("fields", {})
                    if key not in decl:
                        continue
                    _t, eth, _p = recs[0]
                    got = getter(eth)
                    want = decl[key]
                    checked.append(f"{sid:016x}")
                    if key == "destination_address":
                        if got.lower() != str(want).lower():
                            bad[f"{sid:016x}"] = {"declared": want,
                                                  "on_the_wire": got}
                    elif got != want:
                        bad[f"{sid:016x}"] = {"declared": want,
                                              "on_the_wire": got}
            if not checked:
                out.append(Verdict(name, "SKIP", clause,
                                   {"why": "no stream in the capture has a "
                                           "Talker Advertise declaring this "
                                           "parameter, so there is nothing to "
                                           "compare"}))
            else:
                out.append(_v(name, not bad, clause, checked=checked,
                              mismatches=bad))

        # (4) the TSpec, recorded against the frames actually seen
        tspec, tbad = {}, {}
        for sid, r in st["talkers"].items():
            f = r.get("fields", {})
            if "max_frame_size" not in f:
                continue
            tspec[f"{sid:016x}"] = {
                "max_frame_size": f["max_frame_size"],
                "max_interval_frames": f["max_interval_frames"],
                "priority": f.get("priority"), "rank": f.get("rank"),
                "accumulated_latency_ns": f.get("accumulated_latency")}
            recs = self.aaf.get(sid) or self.crf.get(sid) or []
            if recs:
                # the tap adds no octets to wire_len here (read_capture strips the
                # record header), and MaxFrameSize excludes the 4-octet FCS and
                # the 14/18-octet Ethernet header per 802.1Q-2018 35.2.2.8.5
                biggest = max(len(p.payload) + 24 for _t, _e, p in recs
                              if hasattr(p, "payload"))
                if f["max_frame_size"] and biggest > f["max_frame_size"]:
                    tbad[f"{sid:016x}"] = {
                        "declared_max_frame_size": f["max_frame_size"],
                        "largest_avtpdu_seen": biggest}
            if f["max_interval_frames"] == 0:
                tbad.setdefault(f"{sid:016x}", {})["max_interval_frames"] = 0
        if not tspec:
            out.append(Verdict("wt.msrp.tspec-declared", "SKIP",
                               "802.1Q-2018 35.2.2.8.5",
                               {"why": "no Talker Advertise in the capture "
                                       "carries a TSpec"}))
        else:
            out.append(_v("wt.msrp.tspec-declared", not tbad,
                          "802.1Q-2018 35.2.2.8.5 TSpec: MaxFrameSize is the "
                          "largest frame the reservation covers and "
                          "MaxIntervalFrames the count per class measurement "
                          "interval; a frame larger than the declaration is "
                          "outside the reservation it claims",
                          declared=tspec, violations=tbad))

        # (5) the SR Domain, and the MVRP VID registration
        if not st["domains"]:
            out.append(Verdict("wt.msrp.domain-declared", "SKIP",
                               "802.1Q-2018 35.2.2.9 + Milan v1.2 4.2.7.2",
                               {"why": "no MSRP Domain attribute in the "
                                       "capture; a short capture can miss one "
                                       "because Domain is re-declared on the "
                                       "MRP timers, not per frame",
                                "absent": "MSRP Domain attribute"}))
        else:
            want_pcp = self.expect.sr_class_a_pcp
            bad = [d for d in st["domains"]
                   if d.get("sr_class_id") == 6
                   and d.get("sr_class_priority") != want_pcp]
            out.append(_v("wt.msrp.domain-declared", not bad,
                          "802.1Q-2018 35.2.2.9 + Milan v1.2 4.2.7.2.1: the SR "
                          "class A Domain attribute carries the class's "
                          "priority and VID, and the frames must use them",
                          domains=st["domains"], expected_class_a_pcp=want_pcp,
                          mismatches=bad))
        if not st["mvrp_vids"]:
            out.append(Verdict("wt.mvrp.sr-vid-declared", "SKIP",
                               "802.1Q-2018 11.2.3.1.2",
                               {"why": "no MVRP VID declaration in the capture; "
                                       "MVRP re-declares on its own timers, so "
                                       "a short capture can miss it",
                                "absent": "MVRP VID attribute"}))
        elif self.expect.sr_vid is None:
            out.append(Verdict("wt.mvrp.sr-vid-declared", "SKIP",
                               "802.1Q-2018 11.2.3.1.2",
                               {"why": "no expected SR VID supplied",
                                "observed": st["mvrp_vids"]}))
        else:
            out.append(_v("wt.mvrp.sr-vid-declared",
                          self.expect.sr_vid in st["mvrp_vids"],
                          "802.1Q-2018 11.2.3.1.2: the SR VID is registered by "
                          "MVRP; an unregistered VID is not pruned to the "
                          "listeners and the stream floods",
                          expected=self.expect.sr_vid,
                          observed=st["mvrp_vids"]))
        return out


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
                       tag_of=None) -> list[Verdict]:
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


# ------------------------------------------------------------------ self test --
def _b(*parts) -> bytes:
    return bytes.fromhex("".join(parts).replace(" ", ""))


def build_aaf_frame(*, dmac="91e0f000fe01", smac="020000000002", vid=2, pcp=3,
                    tagged=True, seq=0, sid=0x020000000002_0000, ts=0,
                    channels=2, fmt=0x02, bit_depth=32, nsr=5,
                    sample_frames=6, samples=None, tv=1, tu=0, sp=0,
                    mr=0) -> bytes:
    """An AAF PCM frame built to IEEE 1722-2016 Figure 26, by hand.

    This is the byte-vector oracle the decoder is tested against: it is written
    from the FIGURE, not from KL_aaf_packetizer, so the two can disagree.
    `samples[frame][channel]` are 24-bit values, left-justified like the
    fabric does (sample << 8).
    """
    w = AAF_FORMAT_BITS.get(fmt, 32) // 8
    sdl = sample_frames * channels * w
    hdr = bytearray()
    hdr += bytes.fromhex(dmac) + bytes.fromhex(smac)
    if tagged:
        hdr += struct.pack(">H", TPID_C_TAG)
        hdr += struct.pack(">H", (pcp << 13) | (vid & 0xFFF))
    hdr += struct.pack(">H", ETH_P_AVTP)
    pdu = bytearray(24)
    pdu[0] = SUBTYPE_AAF
    pdu[1] = (1 << 7) | (mr << 3) | (tv & 1)
    pdu[2] = seq & 0xFF
    pdu[3] = tu & 1
    pdu[4:12] = sid.to_bytes(8, "big")
    pdu[12:16] = struct.pack(">I", ts & 0xFFFFFFFF)
    pdu[16] = fmt
    pdu[17] = ((nsr & 0xF) << 4) | ((channels >> 8) & 0x3)
    pdu[18] = channels & 0xFF
    pdu[19] = bit_depth
    pdu[20:22] = struct.pack(">H", sdl)
    pdu[22] = (sp << 4)
    body = bytearray()
    for f in range(sample_frames):
        for c in range(channels):
            v = 0 if samples is None else samples[f][c]
            body += ((v << 8) & 0xFFFFFFFF).to_bytes(w, "big")
    frame = bytes(hdr) + bytes(pdu) + bytes(body)
    return frame + b"\x00" * max(0, 60 - len(frame))


def build_crf_frame(*, dmac="91e0f000fe02", smac="020000000002", vid=2, pcp=3,
                    tagged=True, seq=0, sid=0x020000000002_0001, ts=0,
                    base_hz=48000, interval=96, pull=0, ctype=1, tu=0,
                    n_ts=1) -> bytes:
    """A CRF frame built to IEEE 1722-2016 Figure 72, by hand."""
    hdr = bytearray(bytes.fromhex(dmac) + bytes.fromhex(smac))
    if tagged:
        hdr += struct.pack(">H", TPID_C_TAG)
        hdr += struct.pack(">H", (pcp << 13) | (vid & 0xFFF))
    hdr += struct.pack(">H", ETH_P_AVTP)
    pdu = bytearray(20)
    pdu[0] = SUBTYPE_CRF
    pdu[1] = (1 << 7) | (tu & 1)
    pdu[2] = seq & 0xFF
    pdu[3] = ctype
    pdu[4:12] = sid.to_bytes(8, "big")
    pdu[12:16] = struct.pack(">I", ((pull & 7) << 29) | (base_hz & 0x1FFFFFFF))
    pdu[16:18] = struct.pack(">H", 8 * n_ts)
    pdu[18:20] = struct.pack(">H", interval)
    body = b"".join((ts + i * interval * 1_000_000_000 // base_hz)
                    .to_bytes(8, "big") for i in range(n_ts))
    frame = bytes(hdr) + bytes(pdu) + body
    return frame + b"\x00" * max(0, 60 - len(frame))


def build_msrp_frame(*, smac="020000000002", attrs=None) -> bytes:
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


def msrp_talker_advertise_value(*, stream_id=0x0200000000020000,
                                dmac="91e0f000fe01", vid=2, max_frame=1024,
                                max_interval=1, pcp=3, rank=1,
                                latency=0) -> bytes:
    """The 25-octet Talker Advertise FirstValue, per 802.1Q-2018 35.2.2.8."""
    return (stream_id.to_bytes(8, "big") + bytes.fromhex(dmac)
            + struct.pack(">HHH", vid, max_frame, max_interval)
            + bytes([((pcp & 7) << 5) | ((rank & 1) << 4)])
            + struct.pack(">I", latency))


def msrp_listener_value(stream_id=0x0200000000020000) -> bytes:
    return stream_id.to_bytes(8, "big")


def msrp_domain_value(class_id=6, priority=3, vid=2) -> bytes:
    return bytes([class_id, priority]) + struct.pack(">H", vid)


def build_mvrp_frame(*, smac="020000000002", vids=(2,)) -> bytes:
    """An MVRPDU (802.1Q-2018 11.2.3.1.2): one attribute type, VID, length 2."""
    body = bytearray([0x00, MVRP_VID, 0x02])
    for v in vids:
        body += struct.pack(">H", 1) + struct.pack(">H", v) + bytes([1 * 36])
    body += b"\x00\x00\x00\x00"
    frame = MRP_GROUP_DMAC + bytes.fromhex(smac) + \
        struct.pack(">H", ETH_P_MVRP) + bytes(body)
    return frame + b"\x00" * max(0, 60 - len(frame))


def build_adp_frame(*, smac="020000000002", eid=0x020000FFFE000002,
                    available_index=1, cdl=ADP_CDL, body_len=64) -> bytes:
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


def self_test() -> int:
    """Byte-vector tests for every decoder and every check.  No capture, no
    hardware, no network.  Each block ends with a NEGATIVE control, because a
    check that cannot fail is not a check (methodology R2)."""
    import unittest

    class T(unittest.TestCase):
        def test_aaf_decode_matches_the_figure(self):
            f = build_aaf_frame(seq=7, channels=8, ts=0x11223344, tu=1)
            eth = decode_eth(f)
            self.assertTrue(eth.tagged)
            self.assertEqual((eth.pcp, eth.dei, eth.vid), (3, 0, 2))
            self.assertEqual(eth.ethertype, ETH_P_AVTP)
            p = decode_aaf(eth.payload)
            self.assertEqual(p.sequence_num, 7)
            self.assertEqual(p.channels_per_frame, 8)
            self.assertEqual(p.avtp_timestamp, 0x11223344)
            self.assertEqual(p.tu, 1)
            self.assertEqual(p.tv, 1)
            self.assertEqual(p.bit_depth, 32)
            self.assertEqual(p.nsr, 5)
            self.assertEqual(p.format_name, "INT_32BIT")
            self.assertEqual(p.sample_frames, 6)
            self.assertEqual(p.stream_data_length, 6 * 8 * 4)

        def test_aaf_channels_per_frame_spans_two_octets(self):
            # 7.3.3 is a 10-bit field: 0x105 has to survive the 2+8 split
            f = build_aaf_frame(channels=0x105, sample_frames=1)
            p = decode_aaf(decode_eth(f).payload)
            self.assertEqual(p.channels_per_frame, 0x105)

        def test_aaf_stream_format_qword_round_trip(self):
            d = parse_aaf_stream_format("0205022001006000")
            self.assertEqual(d.channels_per_frame, 4)
            self.assertEqual(d.nsr, 5)
            self.assertEqual(d.fmt, 2)
            self.assertEqual(d.bit_depth, 32)
            self.assertEqual(d.samples_per_frame, 6)
            self.assertEqual(d.ut, 0)
            self.assertEqual(parse_aaf_stream_format(0x0205022000806000)
                             .channels_per_frame, 2)
            self.assertEqual(parse_aaf_stream_format(0x0205022002006000)
                             .channels_per_frame, 8)
            self.assertEqual(parse_aaf_stream_format(0x0215022002006000).ut, 1)
            self.assertIsNone(parse_aaf_stream_format(MILAN_CRF_FORMAT))

        def test_crf_stream_format_is_the_milan_constant(self):
            d = parse_crf_stream_format(MILAN_CRF_FORMAT)
            self.assertEqual(d.type, CRF_TYPE_AUDIO_SAMPLE)
            self.assertEqual(d.timestamp_interval, MILAN_CRF_TS_INTERVAL)
            self.assertEqual(d.timestamps_per_pdu, MILAN_CRF_TS_PER_PDU)
            self.assertEqual(d.pull, 0)
            self.assertEqual(d.base_frequency, MILAN_CRF_BASE_HZ)

        def test_crf_decode_matches_the_figure(self):
            p = decode_crf(decode_eth(build_crf_frame(seq=250)).payload)
            self.assertEqual(p.sequence_num, 250)
            self.assertEqual(p.type, 1)
            self.assertEqual(p.base_frequency, 48000)
            self.assertEqual(p.timestamp_interval, 96)
            self.assertEqual(p.crf_data_length, 8)
            self.assertEqual(len(p.timestamps), 1)

        def test_declared_vs_wire_catches_the_2026_07_27_escape(self):
            # a talker advertising 8 channels while the framer emits 2
            wt = WireTruth(Expectation(aaf_format=0x0205022002006000))
            wt.feed(0.0, build_aaf_frame(channels=2))
            bad = [v for v in wt.check_aaf_declared_vs_wire()
                   if v.verdict == "FAIL"]
            self.assertEqual(len(bad), 1)
            self.assertIn("channels_per_frame", bad[0].detail["mismatches"])
            # NEGATIVE CONTROL: the honest pair must pass
            wt = WireTruth(Expectation(aaf_format=0x0205022000806000))
            wt.feed(0.0, build_aaf_frame(channels=2))
            self.assertTrue(all(v.verdict == "PASS"
                                for v in wt.check_aaf_declared_vs_wire()))

        def test_sequence_gap_and_wrap(self):
            wt = WireTruth()
            for s in (254, 255, 0, 1):
                wt.feed(0.0, build_aaf_frame(seq=s))
            vs = wt.check_sequence_continuity()
            self.assertTrue(all(v.verdict == "PASS" for v in vs
                                if v.check.startswith("wt.aaf.")), vs)
            # and the CRF family, which had NO frames, says SKIP rather than
            # emitting nothing: an absent family and a passing one must be
            # distinguishable in the log
            crf = [v for v in vs if v.check.startswith("wt.crf.")]
            self.assertEqual([v.verdict for v in crf], ["SKIP"])
            self.assertIn("CRF frames", crf[0].detail["absent"])
            wt = WireTruth()
            for s in (1, 2, 4):
                wt.feed(0.0, build_aaf_frame(seq=s))
            v = wt.check_sequence_continuity()[0]
            self.assertEqual(v.verdict, "FAIL")
            self.assertEqual(v.detail["gap_count"], 1)

        def test_crf_sequence_is_one_octet(self):
            # 10.4.6: FF -> 00 is a WRAP, not a gap.  Reading the field as 16
            # bits would make this a gap of -255.
            wt = WireTruth()
            for s in (0xFE, 0xFF, 0x00):
                wt.feed(0.0, build_crf_frame(seq=s))
            v = [x for x in wt.check_sequence_continuity()
                 if x.check.startswith("wt.crf.seq")][0]
            self.assertEqual(v.verdict, "PASS")

        def test_vlan_checks_and_the_vid_zero_defect(self):
            wt = WireTruth()
            wt.feed(0.0, build_aaf_frame(vid=0))
            v = [x for x in wt.check_vlan_class()
                 if "c-tag-vid" in x.check][0]
            self.assertEqual(v.verdict, "FAIL")
            self.assertTrue(v.detail["vid_zero_seen"])
            wt = WireTruth()
            wt.feed(0.0, build_crf_frame(tagged=False))
            v = [x for x in wt.check_vlan_class()
                 if "crf.c-tag-present" in x.check][0]
            self.assertEqual(v.verdict, "FAIL")
            # NEGATIVE CONTROL: the conformant tag passes every VLAN check
            wt = WireTruth()
            wt.feed(0.0, build_aaf_frame())
            wt.feed(0.0, build_crf_frame())
            self.assertTrue(all(x.verdict == "PASS"
                                for x in wt.check_vlan_class()))

        def test_header_legality_negatives(self):
            for kw, needle in ((dict(channels=0, sample_frames=0),
                                "channels_per_frame 0"),
                               (dict(bit_depth=0), "bit_depth 0"),
                               (dict(fmt=0x4, bit_depth=32),
                                "bit_depth 32 > format width 16")):
                wt = WireTruth()
                wt.feed(0.0, build_aaf_frame(**kw))
                v = wt.check_aaf_header_legality()[0]
                self.assertEqual(v.verdict, "FAIL", kw)
                self.assertTrue(any(needle in s
                                    for s in v.detail["violations"]),
                                (kw, v.detail))

        def test_pts_step_is_one_avtpdu_of_media(self):
            wt = WireTruth()
            for i in range(5):                      # 6 samples @48k = 125 us
                wt.feed(0.0, build_aaf_frame(seq=i, ts=i * 125_000))
            v = [x for x in wt.check_aaf_timestamps()
                 if "pts-step" in x.check][0]
            self.assertEqual(v.verdict, "PASS")
            self.assertEqual(v.detail["expected_step_ns"], 125_000)
            wt = WireTruth()
            for i in range(5):
                wt.feed(0.0, build_aaf_frame(seq=i, ts=i * 500_000))
            v = [x for x in wt.check_aaf_timestamps()
                 if "pts-step" in x.check][0]
            self.assertEqual(v.verdict, "FAIL")

        def test_class_a_transit_skips_without_a_gptp_reference(self):
            wt = WireTruth()
            wt.feed(0.0, build_aaf_frame())
            v = [x for x in wt.check_aaf_timestamps()
                 if "class-a-transit" in x.check][0]
            self.assertEqual(v.verdict, "SKIP")
            # with a reference it becomes a real check, both ways
            wt = WireTruth(Expectation(gptp_ref_ns=1_000_000))
            wt.feed(0.0, build_aaf_frame(ts=1_000_000 + 1_500_000))
            self.assertEqual([x for x in wt.check_aaf_timestamps()
                              if "class-a-transit" in x.check][0].verdict,
                             "PASS")
            wt = WireTruth(Expectation(gptp_ref_ns=1_000_000))
            wt.feed(0.0, build_aaf_frame(ts=1_000_000 + 9_000_000))
            self.assertEqual([x for x in wt.check_aaf_timestamps()
                              if "class-a-transit" in x.check][0].verdict,
                             "FAIL")

        def test_zero_fill_both_directions(self):
            sid = 0x020000000002_0000
            wt = WireTruth(Expectation(silent_stream_ids=(sid,)))
            wt.feed(0.0, build_aaf_frame(sid=sid))
            self.assertTrue(all(v.verdict == "PASS"
                                for v in wt.check_zero_fill()))
            # a stream declared silent that carries audio is a FAIL...
            tone = [[0x123456] * 2 for _ in range(6)]
            wt = WireTruth(Expectation(silent_stream_ids=(sid,)))
            wt.feed(0.0, build_aaf_frame(sid=sid, samples=tone))
            self.assertEqual(wt.check_zero_fill()[0].verdict, "FAIL")
            # ...and a declared-silent stream with NO frames is also a FAIL:
            # Milan 5.3.7.3 says it streams, so absence != silence
            wt = WireTruth(Expectation(silent_stream_ids=(sid,)))
            self.assertEqual(wt.check_zero_fill()[0].verdict, "FAIL")
            # a fed stream that is all zeros is the silence defect
            wt = WireTruth(Expectation(fed_stream_ids=(sid,)))
            wt.feed(0.0, build_aaf_frame(sid=sid))
            self.assertEqual(wt.check_zero_fill()[0].verdict, "FAIL")

        def test_crf_rate_and_format(self):
            wt = WireTruth()
            for i in range(101):                     # 500 pps for 200 ms
                wt.feed(i * 0.002, build_crf_frame(seq=i & 0xFF,
                                                   ts=i * 2_000_000))
            self.assertTrue(all(v.verdict == "PASS"
                                for v in wt.check_crf_format()))
            rate = [v for v in wt.check_crf_rate()
                    if "pdu-rate" in v.check][0]
            self.assertEqual(rate.verdict, "PASS")
            self.assertAlmostEqual(rate.detail["expected_pps"], 500.0)
            # a non-Milan interval is a FAIL against Milan 7.3.2
            wt = WireTruth()
            wt.feed(0.0, build_crf_frame(interval=48))
            self.assertEqual(wt.check_crf_format()[0].verdict, "FAIL")

        def test_adp_82_byte_rule_and_available_index(self):
            wt = WireTruth()
            for i in (1, 2, 3):
                wt.feed(0.0, build_adp_frame(available_index=i))
            self.assertTrue(all(v.verdict == "PASS"
                                for v in wt.check_adp_frame_rule()))
            self.assertEqual(len(build_adp_frame()), ADP_FRAME_LEN)
            # a short body breaks the 82-byte rule
            wt = WireTruth()
            wt.feed(0.0, build_adp_frame(body_len=40, cdl=ADP_CDL))
            self.assertEqual([v for v in wt.check_adp_frame_rule()
                              if "frame-82" in v.check][0].verdict, "FAIL")
            # a repeated available_index is the 2026-07-12 incoherence
            wt = WireTruth()
            for i in (5, 5, 6):
                wt.feed(0.0, build_adp_frame(available_index=i))
            self.assertEqual([v for v in wt.check_adp_frame_rule()
                              if "available-index" in v.check][0].verdict,
                             "FAIL")

        def test_control_length_lie(self):
            wt = WireTruth()
            wt.feed(0.0, build_adp_frame())
            self.assertEqual(wt.check_control_length_honesty()[0].verdict,
                             "PASS")
            wt = WireTruth()
            wt.feed(0.0, build_adp_frame(cdl=200))     # claims 200, carries 56
            v = wt.check_control_length_honesty()[0]
            self.assertEqual(v.verdict, "FAIL")
            self.assertEqual(v.detail["liars"][0]["cdl"], 200)

        def test_empty_capture_is_not_a_pass(self):
            self.assertEqual(WireTruth().check_capture_shape()[0].verdict,
                             "FAIL")

        def test_an_empty_capture_produces_NO_PASS_AND_NO_SILENCE(self):
            """The empty-collection rule, both halves.

            Eight of the twelve check families used to emit NOTHING on an empty
            capture - so the log could not tell "did not apply" from "was not
            run" - and wt.control.length-honest emitted PASS, because `not []`
            is True.  An empty capture is this project's commonest false green
            (a mirror port that never joined the multicast group), so:
              * no check may PASS, and
              * every family must be REPRESENTED, by a SKIP naming what was
                absent.
            """
            vs = WireTruth(Expectation()).checks()
            self.assertEqual([v.check for v in vs if v.verdict == "PASS"], [])
            shape = [v for v in vs if v.check ==
                     "wt.capture.stream-frames-present"]
            self.assertEqual([v.verdict for v in shape], ["FAIL"])
            names = {v.check for v in vs}
            for family in ("wt.aaf.header-legal", "wt.aaf.payload-arithmetic",
                           "wt.aaf.seq-continuity", "wt.crf.seq-continuity",
                           "wt.aaf.tv-set", "wt.aaf.pts-step",
                           "wt.aaf.class-a-transit", "wt.aaf.c-tag-present",
                           "wt.aaf.c-tag-pcp", "wt.aaf.c-tag-dei",
                           "wt.aaf.c-tag-vid", "wt.crf.c-tag-present",
                           "wt.crf.milan-format", "wt.crf.pdu-rate",
                           "wt.crf.timestamp-step", "wt.adp.frame-82",
                           "wt.adp.available-index-advances",
                           "wt.aaf.zero-fill", "wt.control.length-honest"):
                self.assertIn(family, names, f"{family} emitted nothing")
            for v in vs:
                if v.verdict == "SKIP":
                    self.assertTrue(v.detail.get("why"), v.check)
            # and --fail-on-skip is what turns this honest SKIP set into a
            # non-zero exit for a gate that must be fully wired
            self.assertTrue(any(v.verdict == "SKIP" for v in vs))

        def test_msrp_decode_from_the_clause_byte_layout(self):
            """802.1Q-2018 35.2.2.8: StreamID(8) + DataFrameParameters(8) +
            TSpec(4) + PriorityAndRank(1) + AccumulatedLatency(4) = 25."""
            v = msrp_talker_advertise_value(stream_id=0x0200000000020003,
                                            dmac="91e0f000fe07", vid=2,
                                            max_frame=1024, max_interval=1,
                                            pcp=3, rank=1, latency=12345)
            self.assertEqual(len(v), 25)
            f = build_msrp_frame(attrs=[(MSRP_TALKER_ADVERTISE, v, [1], [])])
            got = decode_mrpdu(decode_eth(f).payload, "MSRP")
            self.assertEqual(len(got), 1)
            a = got[0]
            self.assertEqual(a.attr_name, "Talker Advertise")
            self.assertEqual(a.event, "JoinIn")
            self.assertTrue(a.declaring)
            self.assertEqual(a.fields["stream_id"], 0x0200000000020003)
            self.assertEqual(a.fields["destination_address"], "91e0f000fe07")
            self.assertEqual(a.fields["vlan_identifier"], 2)
            self.assertEqual(a.fields["max_frame_size"], 1024)
            self.assertEqual(a.fields["max_interval_frames"], 1)
            self.assertEqual(a.fields["priority"], 3)
            self.assertEqual(a.fields["accumulated_latency"], 12345)
            # a Listener attribute is 8 octets and its declaration TYPE rides
            # the FourPackedEvents vector, not the value
            f = build_msrp_frame(attrs=[(MSRP_LISTENER,
                                         msrp_listener_value(0x0200000000020003),
                                         [1], [2])])
            a = decode_mrpdu(decode_eth(f).payload, "MSRP")[0]
            self.assertEqual(a.fields["declaration"], "Ready")
            # a vector of N values increments the StreamID's unique_id
            f = build_msrp_frame(attrs=[(MSRP_LISTENER,
                                         msrp_listener_value(0x0200000000020000),
                                         [1, 1, 1], [2, 2, 3])])
            got = decode_mrpdu(decode_eth(f).payload, "MSRP")
            self.assertEqual([a.fields["stream_id"] for a in got],
                             [0x0200000000020000, 0x0200000000020001,
                              0x0200000000020002])
            self.assertEqual([a.fields["declaration"] for a in got],
                             ["Ready", "Ready", "Ready Failed"])
            # a truncated PDU decodes what it can rather than raising: a tap can
            # legitimately start mid-PDU
            self.assertEqual(decode_mrpdu(b"\x00\x01", "MSRP"), [])

        def test_the_srp_licence_is_visible_only_from_the_tap(self):
            """Milan v1.2 5.3.7.3 + 5.3.7.2, from the wire.

            This is the check set that found a real defect - only 2 of 5 talker
            stream_ids declaring a Talker Advertise - and it can only be made
            from an inline tap, because MSRP goes to 01:80:C2:00:00:0E and a
            bridge does not forward it.
            """
            sid = 0x0200000000020000
            w = WireTruth(Expectation(
                talker_stream_ids=(sid, sid + 1, sid + 2, sid + 3, sid + 4)))
            w.feed(0.0, build_aaf_frame(sid=sid, vid=2, pcp=3,
                                        dmac="91e0f000fe01"))
            w.feed(0.1, build_msrp_frame(attrs=[
                (MSRP_TALKER_ADVERTISE,
                 msrp_talker_advertise_value(stream_id=sid,
                                             dmac="91e0f000fe01", vid=2),
                 [1], []),
                (MSRP_TALKER_ADVERTISE,
                 msrp_talker_advertise_value(stream_id=sid + 1,
                                             dmac="91e0f000fe02", vid=2),
                 [1], []),
                (MSRP_LISTENER, msrp_listener_value(sid), [1], [2]),
                (MSRP_DOMAIN, msrp_domain_value(6, 3, 2), [1], [])]))
            w.feed(0.2, build_mvrp_frame(vids=(2,)))
            v = {x.check: x for x in w.check_srp_declarations()}
            # THE DEFECT: 3 of the 5 declared stream_ids never advertised
            t = v["wt.msrp.talker-advertise-declared"]
            self.assertEqual(t.verdict, "FAIL")
            self.assertEqual(t.detail["missing"],
                             [f"{sid + i:016x}" for i in (2, 3, 4)])
            # the licence half IS present for the stream that is running
            self.assertEqual(
                v["wt.msrp.listener-declaration-present"].verdict, "PASS")
            # the declaration and the frames agree about DMAC and VID
            self.assertEqual(v["wt.msrp.declared-dmac-matches-wire"].verdict,
                             "PASS")
            self.assertEqual(v["wt.msrp.declared-vid-matches-wire"].verdict,
                             "PASS")
            self.assertEqual(v["wt.msrp.domain-declared"].verdict, "PASS")
            self.assertEqual(v["wt.mvrp.sr-vid-declared"].verdict, "PASS")
            self.assertEqual(v["wt.msrp.tspec-declared"].verdict, "PASS")

            # NEGATIVE CONTROLS, one per check.
            # (a) frames on the wire with NO Listener Ready = unreserved
            w = WireTruth(Expectation(talker_stream_ids=(sid,)))
            w.feed(0.0, build_aaf_frame(sid=sid, dmac="91e0f000fe01"))
            w.feed(0.1, build_msrp_frame(attrs=[
                (MSRP_TALKER_ADVERTISE,
                 msrp_talker_advertise_value(stream_id=sid,
                                             dmac="91e0f000fe01"), [1], []),
                (MSRP_LISTENER, msrp_listener_value(sid), [1], [1])]))
            v = {x.check: x for x in w.check_srp_declarations()}
            self.assertEqual(
                v["wt.msrp.listener-declaration-present"].verdict, "FAIL")
            self.assertEqual(
                v["wt.msrp.listener-declaration-present"]
                .detail["without_listener_ready"], [f"{sid:016x}"])
            # (b) the DMAC on the wire is not the one declared
            w = WireTruth(Expectation(talker_stream_ids=(sid,)))
            w.feed(0.0, build_aaf_frame(sid=sid, dmac="91e0f000fe09"))
            w.feed(0.1, build_msrp_frame(attrs=[
                (MSRP_TALKER_ADVERTISE,
                 msrp_talker_advertise_value(stream_id=sid,
                                             dmac="91e0f000fe01", vid=2),
                 [1], [])]))
            v = {x.check: x for x in w.check_srp_declarations()}
            self.assertEqual(v["wt.msrp.declared-dmac-matches-wire"].verdict,
                             "FAIL")
            # (c) the VID on the wire is not the one declared
            w = WireTruth(Expectation(talker_stream_ids=(sid,)))
            w.feed(0.0, build_aaf_frame(sid=sid, dmac="91e0f000fe01", vid=5))
            w.feed(0.1, build_msrp_frame(attrs=[
                (MSRP_TALKER_ADVERTISE,
                 msrp_talker_advertise_value(stream_id=sid,
                                             dmac="91e0f000fe01", vid=2),
                 [1], [])]))
            v = {x.check: x for x in w.check_srp_declarations()}
            self.assertEqual(v["wt.msrp.declared-vid-matches-wire"].verdict,
                             "FAIL")
            # (d) a WITHDRAWN (Lv) Talker Advertise is not a declaration
            w = WireTruth(Expectation(talker_stream_ids=(sid,)))
            w.feed(0.1, build_msrp_frame(attrs=[
                (MSRP_TALKER_ADVERTISE,
                 msrp_talker_advertise_value(stream_id=sid), [5], [])]))
            v = {x.check: x for x in w.check_srp_declarations()}
            self.assertEqual(v["wt.msrp.talker-advertise-declared"].verdict,
                             "FAIL")
            # (e) a frame larger than the declared MaxFrameSize is outside its
            #     own reservation
            w = WireTruth(Expectation(talker_stream_ids=(sid,)))
            w.feed(0.0, build_aaf_frame(sid=sid, dmac="91e0f000fe01",
                                        channels=8, sample_frames=48))
            w.feed(0.1, build_msrp_frame(attrs=[
                (MSRP_TALKER_ADVERTISE,
                 msrp_talker_advertise_value(stream_id=sid,
                                             dmac="91e0f000fe01",
                                             max_frame=100), [1], [])]))
            v = {x.check: x for x in w.check_srp_declarations()}
            self.assertEqual(v["wt.msrp.tspec-declared"].verdict, "FAIL")
            # (f) the wrong SR class A priority in the Domain attribute
            w = WireTruth()
            w.feed(0.1, build_msrp_frame(attrs=[
                (MSRP_DOMAIN, msrp_domain_value(6, 2, 2), [1], [])]))
            v = {x.check: x for x in w.check_srp_declarations()}
            self.assertEqual(v["wt.msrp.domain-declared"].verdict, "FAIL")
            # (g) MVRP registering a VID that is not the SR VID
            w = WireTruth(Expectation(sr_vid=2))
            w.feed(0.1, build_mvrp_frame(vids=(7,)))
            v = {x.check: x for x in w.check_srp_declarations()}
            self.assertEqual(v["wt.mvrp.sr-vid-declared"].verdict, "FAIL")

        def test_a_capture_with_no_MRP_says_it_needs_the_tap(self):
            # A mirror port and the controller host can NEVER see these frames,
            # so the SKIP has to say that rather than reading as "no problem".
            w = WireTruth()
            w.feed(0.0, build_aaf_frame())
            vs = w.check_srp_declarations()
            self.assertTrue(vs)
            self.assertTrue(all(v.verdict == "SKIP" for v in vs))
            self.assertIn("INLINE TAP", vs[0].detail["absent"].upper()
                          + vs[0].clause.upper())

        def test_the_28_octet_tap_record_header_is_handled_and_tested(self):
            """The ProfiShark inline tap prepends a 28-octet record header, so
            EVERY ether offset shifts by +28: in a BPF filter the EtherType is
            ether[40:2] and the DMAC is at 28.  A decoder that ignores it sees
            garbage; one that assumes it on an already-stripped capture also sees
            garbage.  Both directions are tested."""
            import os
            import struct as _s
            import tempfile
            frames = [build_aaf_frame(seq=i) for i in range(3)]
            blob = bytearray(_s.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0,
                                     65535, 1))
            for i, fr in enumerate(frames):
                rec = b"\x00" * 28 + fr + b"\xde\xad\xbe\xef"
                blob += _s.pack("<IIII", i, 0, len(rec), len(rec)) + rec
            fd, path = tempfile.mkstemp(suffix=".pcap")
            try:
                os.write(fd, bytes(blob))
                os.close(fd)
                w = WireTruth().feed_capture(
                    read_capture(path, tap_header=28, strip_fcs=True))
                self.assertEqual(w.check_capture_shape()[0].verdict, "PASS")
                # and the same capture read WITHOUT the offset decodes to nothing
                w = WireTruth().feed_capture(
                    read_capture(path, tap_header=0, strip_fcs=False))
                self.assertEqual(w.check_capture_shape()[0].verdict, "FAIL")
                # the EtherType offset the BPF filter must use
                rec = b"\x00" * 28 + frames[0]
                self.assertEqual(rec[40:42], _s.pack(">H", TPID_C_TAG))
                self.assertEqual(rec[28:34], frames[0][0:6])
            finally:
                if os.path.exists(path):
                    os.unlink(path)

        def test_walking_tone_identity(self):
            n, ch = 6, 4
            good = [[1 << c for c in range(ch)] for _ in range(n)]
            p = decode_aaf(decode_eth(build_aaf_frame(
                channels=ch, sample_frames=n, samples=good)).payload)
            self.assertTrue(all(v.verdict == "PASS"
                                for v in check_walking_tone([p], ch)))
            # a SWAP of channels 1 and 2
            sw = [[1, 4, 2, 8] for _ in range(n)]
            p = decode_aaf(decode_eth(build_aaf_frame(
                channels=ch, sample_frames=n, samples=sw)).payload)
            vs = {v.check: v.verdict for v in check_walking_tone([p], ch)}
            self.assertEqual(vs["audio.identity.uncrossed"], "FAIL")
            # a DUPLICATE of channel 0 onto channel 1
            du = [[1, 1, 4, 8] for _ in range(n)]
            p = decode_aaf(decode_eth(build_aaf_frame(
                channels=ch, sample_frames=n, samples=du)).payload)
            vs = {v.check: v.verdict for v in check_walking_tone([p], ch)}
            self.assertEqual(vs["audio.identity.no-duplicate-neighbour"],
                             "FAIL")
            # a DROPPED channel 2
            dr = [[1, 2, 0, 8] for _ in range(n)]
            p = decode_aaf(decode_eth(build_aaf_frame(
                channels=ch, sample_frames=n, samples=dr)).payload)
            vs = {v.check: v.verdict for v in check_walking_tone([p], ch)}
            self.assertEqual(vs["audio.identity.no-silent-channel"], "FAIL")

        def test_pcap_round_trip_with_tap_header_and_fcs(self):
            import tempfile, os
            frames = [build_aaf_frame(seq=i) for i in range(3)]
            blob = bytearray(struct.pack("<IHHiIII", 0xa1b2c3d4, 2, 4, 0, 0,
                                         65535, 1))
            for i, fr in enumerate(frames):
                rec = b"\x00" * 28 + fr + b"\xde\xad\xbe\xef"   # tap + FCS
                blob += struct.pack("<IIII", 100 + i, 0, len(rec), len(rec))
                blob += rec
            fd, path = tempfile.mkstemp(suffix=".pcap")
            try:
                os.write(fd, bytes(blob))
                os.close(fd)
                recs = read_capture(path, tap_header=28, strip_fcs=True)
                self.assertEqual([r[1] for r in recs], frames)
                self.assertEqual(recs[1][0], 101.0)
                wt = WireTruth().feed_capture(recs)
                self.assertEqual(wt.check_capture_shape()[0].verdict, "PASS")
                # WITHOUT the tap offset the same file must NOT read as clean
                wt = WireTruth().feed_capture(read_capture(path))
                self.assertEqual(wt.check_capture_shape()[0].verdict, "FAIL")
            finally:
                if os.path.exists(path):
                    os.unlink(path)

    r = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T))
    return 0 if r.wasSuccessful() else 1


# ------------------------------------------------------------------------ CLI --
def main() -> int:
    ap = argparse.ArgumentParser(
        description="decode AVTP + MSRP/MVRP off a capture and check the wire "
                    "invariants - the oracle is the wire and the clause",
        epilog="FULL DOCS: docs/testing/RUNNING_TESTS.md.  HOW TO GET A "
               "CAPTURE: an INLINE tap, on the tap host (a different machine "
               "from the controller host).  `ip link set <if> up` is NOT enough "
               "- the tap does not flow until a capture socket opens it "
               "promiscuously, and operstate reads 'unknown' even when it works, "
               "so gate on rx_packets AFTER tcpdump starts.  Capture for a "
               "DURATION (`timeout 8 tcpdump ...`), never `-c N`: an AAF stream "
               "is ~8000 frames/s, so a few hundred frames is ~50 ms of wire "
               "time and shows no ADP/MRP/AECP at all.  The tap record header "
               "shifts every ether offset by +28, so the SRP filter is "
               "'ether[40:2]=0x22ea or ether[40:2]=0x88f5'.  EXIT: 0 clean, 1 a "
               "FAIL, 2 with --fail-on-skip and any SKIP.")
    ap.add_argument("pcap", nargs="?", help="pcap or pcapng capture")
    ap.add_argument("--self-test", action="store_true",
                    help="run the byte-vector unit tests and exit")
    ap.add_argument("--tap", action="store_true",
                    help="the capture came from a ProfiShark inline tap: a "
                         "28-octet record header before every frame AND the FCS "
                         "present. Every ether offset is +28, so a BPF filter "
                         "reads the EtherType at ether[40:2]")
    ap.add_argument("--tap-header", type=int, default=None,
                    help="record header octets to strip, overriding --tap. Use "
                         "0 for a capture that arrives already stripped - "
                         "assuming a header that is not there decodes to "
                         "nothing, and so does missing one that is")
    ap.add_argument("--strip-fcs", action="store_true")
    ap.add_argument("--talker-stream", action="append", default=[],
                    help="a stream_id (hex) that MUST carry an MSRP Talker "
                         "Advertise declaration, repeatable. Pass the entity's "
                         "WHOLE Stream Output set and the capture answers "
                         "'which of my talkers never declared' - without it the "
                         "check can only see a stream that streams without a "
                         "declaration, never one that is silently undeclared")
    ap.add_argument("--expect-aaf-format", default=None,
                    help="the 8-octet AAF stream_format the controller read "
                         "back (hex), e.g. 0205022001006000")
    ap.add_argument("--expect-crf-format", default=None,
                    help="CRF stream_format hex (default: the Milan Table 7.1 "
                         f"constant {MILAN_CRF_FORMAT:016x})")
    ap.add_argument("--sr-vid", type=int, default=SR_VID_DEFAULT)
    ap.add_argument("--silent-stream", action="append", default=[],
                    help="stream_id (hex) that is bound but unfed - must be "
                         "present AND silent (Milan 5.3.7.3)")
    ap.add_argument("--fed-stream", action="append", default=[],
                    help="stream_id (hex) that must carry non-zero audio")
    ap.add_argument("--adp-entity", action="append", default=[],
                    help="entity_id (hex) that must keep advertising")
    ap.add_argument("--gptp-ref-ns", type=int, default=None,
                    help="gPTP nanoseconds at the capture's FIRST frame; "
                         "without it the class-A transit check SKIPs")
    ap.add_argument("--max-transit-ns", type=int,
                    default=CLASS_A_MAX_TRANSIT_NS)
    ap.add_argument("--jsonl", action="store_true",
                    help="one JSON verdict per line instead of a table")
    ap.add_argument("--fail-on-skip", action="store_true",
                    help="treat SKIP as failure (for a gate that must be "
                         "fully wired)")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if not a.pcap:
        ap.error("a capture is required (or --self-test)")

    hdr = a.tap_header if a.tap_header is not None else (28 if a.tap else 0)
    recs = read_capture(a.pcap, tap_header=hdr,
                        strip_fcs=a.strip_fcs or a.tap)
    exp = Expectation(
        aaf_format=int(a.expect_aaf_format, 16) if a.expect_aaf_format else None,
        crf_format=int(a.expect_crf_format, 16) if a.expect_crf_format else None,
        sr_vid=a.sr_vid,
        silent_stream_ids=tuple(int(s, 16) for s in a.silent_stream),
        fed_stream_ids=tuple(int(s, 16) for s in a.fed_stream),
        adp_entity_ids=tuple(int(s, 16) for s in a.adp_entity),
        talker_stream_ids=tuple(int(s, 16) for s in a.talker_stream),
        gptp_ref_ns=a.gptp_ref_ns, max_transit_ns=a.max_transit_ns)
    verdicts = WireTruth(exp).feed_capture(recs).checks()

    fails = sum(1 for v in verdicts if v.verdict == "FAIL")
    skips = sum(1 for v in verdicts if v.verdict == "SKIP")
    if a.jsonl:
        for v in verdicts:
            print(v.as_json())
    else:
        for v in verdicts:
            print(f"{v.verdict:5s} {v.check}")
            if v.verdict != "PASS":
                print(f"      clause: {v.clause}")
                print(f"      detail: {json.dumps(v.detail, sort_keys=True)}")
        print(f"\n{len(verdicts)} checks: {len(verdicts)-fails-skips} PASS, "
              f"{fails} FAIL, {skips} SKIP")
    if fails:
        return 1
    return 2 if (a.fail_on_skip and skips) else 0


if __name__ == "__main__":
    sys.exit(main())
