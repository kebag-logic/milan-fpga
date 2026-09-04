#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""avtp_wire_truth_wire.py - THE WIRE: the capture reader, the constants
the standards fix, and the decoders that turn octets into fields.

Everything here answers "what do these bytes say", and nothing here has an
opinion about whether the answer is acceptable - that is
`avtp_wire_truth_checks.py`.  Split out of `avtp_wire_truth.py`, which remains
the CLI and re-exports every name below, so the analyser, its byte-vector
fixtures and its self-test can each be opened on their own.

The clause each constant and each decoder is written from is quoted at the
constant or in the decoder's docstring; the tool-level argument for reading the
wire at all is in `avtp_wire_truth.py`'s module docstring."""
from __future__ import annotations

import json
import struct
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterator, Optional


# ----------------------------------------------------------------- constants --
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
        """The verdict flattened for serialisation and for the behave steps."""
        return asdict(self)

    def as_json(self) -> str:
        """One JSONL line, keys sorted: two mornings' runs diff line-for-line
        instead of drowning the real change in re-ordered keys."""
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


def read_capture(path: str | Path, tap_header: int = 0,
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
        """The AVTP subtype octet, or None when this frame is not AVTP."""
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
        """Whether this value is DECLARED on the wire: Lv and Mt withdraw it,
        so an attribute seen in a capture is not the same as one in force."""
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
        """The Table 9 format name, or `reserved(0x..)` for a code the standard
        does not define - named as unknown rather than guessed."""
        return AAF_FORMAT_NAMES.get(self.fmt, f"reserved({self.fmt:#x})")

    @property
    def sample_bits(self) -> Optional[int]:
        """Sample width for this format code, or None when it has none - which
        is what makes every payload-arithmetic check below undecidable."""
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
    """The common AVTP control header (ADP/AECP/ACMP), or None when the PDU is
    shorter than one or carries a subtype that is not a control subtype."""
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
        """The declared nsr as Hz, or None for "user specified" (Table 11),
        which carries no rate - so no rate is invented for it here."""
        return NSR_HZ.get(self.nsr)


def parse_aaf_stream_format(qword: int | str) -> Optional[AafStreamFormat]:
    """The Annex I.2.4 AAF stream_format qword decoded, or None when its
    subtype is not AAF.  A hex STRING is accepted as well as an int, because a
    controller readback and a feature step both spell the qword as text."""
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


def parse_crf_stream_format(qword: int | str) -> Optional[CrfStreamFormat]:
    """The Annex I.2.6 CRF stream_format qword decoded, or None when its
    subtype is not CRF.  Hex strings accepted, as for the AAF qword."""
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
