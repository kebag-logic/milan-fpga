#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
Real IEEE 1722 / 1722.1 wire codecs for the field campaign.

These layouts are the ones the silicon-proven testbenches and the deployed
boards use (`tb/verilator/aecp/sim_main.cpp`, `tb/verilator/acmp*`,
`tb/verilator/adp*`), NOT the tsn-gen model layout — see the caveat in
`tsn_model.py`: the tsn-gen 1722.1 models omit the `sv`+`version` nibble, so
model-encoded bytes are 4 bits off the wire. tsn-gen supplies the field
VALUES and their spec constraints; this module puts them on the wire.

Common AVTPDU framing for every PDU below (offsets are FRAME offsets, i.e.
including the 14-byte Ethernet header):

    0..5    dst MAC          6..11  src MAC        12..13  ethertype 0x22F0
    14      subtype          (0xFA ADP, 0xFB AECP, 0xFC ACMP, 0x02 AAF)
    15      sv(1) version(3) message_type(4)
    16..17  status(5)/valid_time(5) + control_data_length(11)
    18..    per-PDU body

`control_data_length` counts the octets AFTER the first 8-byte id field
(IEEE 1722-2016 §5.4), which for AECP makes the invariant used everywhere in
this campaign: **CDL == frame_len - 26** on an unpadded frame.
"""
import struct

ETHERTYPE_AVTP = 0x22F0
SUBTYPE_ADP = 0xFA
SUBTYPE_AECP = 0xFB
SUBTYPE_ACMP = 0xFC
SUBTYPE_AAF = 0x02

#: bench identities (mirror tb/verilator/aecp/sim_main.cpp and the board CSRs)
ENTITY_MAC = bytes.fromhex("020000fffe01")
CTRLR_MAC = bytes.fromhex("6805ca95b2d1")
CTRLR2_MAC = bytes.fromhex("aabbccddee02")
ENTITY_ID = 0x020000FFFE000001
CTRLR_ID = 0x6805CA95B2D10000
CTRLR2_ID = 0xAABBCCDDEEFF0002

MSG_AEM_COMMAND = 0
MSG_AEM_RESPONSE = 1
MSG_VU_COMMAND = 6
MSG_VU_RESPONSE = 7

STATUS = {0: "SUCCESS", 1: "NOT_IMPLEMENTED", 2: "NO_SUCH_DESCRIPTOR",
          3: "ENTITY_LOCKED", 4: "ENTITY_ACQUIRED", 5: "NOT_AUTHENTICATED",
          6: "AUTHENTICATION_DISABLED", 7: "BAD_ARGUMENTS", 8: "NO_RESOURCES",
          9: "IN_PROGRESS", 10: "ENTITY_MISBEHAVING", 11: "NOT_SUPPORTED",
          12: "STREAM_IS_RUNNING"}


def _eth(dst, src, subtype, byte15, word16, body):
    return (dst + src + struct.pack(">H", ETHERTYPE_AVTP)
            + struct.pack(">BBH", subtype, byte15, word16) + body)


# --------------------------------------------------------------------- AECP
def aecp_cmd(command_type, payload=b"", seq=0x1001, msg_type=MSG_AEM_COMMAND,
             target=ENTITY_ID, controller=CTRLR_ID, dst=ENTITY_MAC,
             src=CTRLR_MAC, u=0, status=0, cdl=None, pad60=False):
    """Build an AECP AEM command frame (the layout sim_main.cpp validates).

    `cdl=None` derives the spec value (12 + payload); pass an int to inject a
    deliberately wrong length for the length-validation probes. `u` is 0 on a
    command — the unsolicited bit is a RESPONSE flag (1722.1 §7.5.2).
    """
    body = (struct.pack(">Q", target) + struct.pack(">Q", controller)
            + struct.pack(">H", seq & 0xFFFF)
            + struct.pack(">H", ((u & 1) << 15) | (command_type & 0x7FFF))
            + payload)
    real_cdl = 12 + len(payload) if cdl is None else cdl
    word16 = ((status & 0x1F) << 11) | (real_cdl & 0x7FF)
    f = _eth(dst, src, SUBTYPE_AECP, msg_type & 0x0F, word16, body)
    if pad60 and len(f) < 60:
        f += b"\x00" * (60 - len(f))
    return f


def aecp_vu_cmd(vu_command, payload=b"", seq=0x1001, protocol_id=b"\x00\x1b\xc5\x0a\xc1\x00",
                target=ENTITY_ID, controller=CTRLR_ID, dst=ENTITY_MAC, src=CTRLR_MAC):
    """Milan Vendor-Unique (MVU) command frame."""
    body = (struct.pack(">Q", target) + struct.pack(">Q", controller)
            + struct.pack(">H", seq & 0xFFFF) + protocol_id
            + struct.pack(">HH", vu_command & 0xFFFF, 0) + payload)
    cdl = 10 + len(protocol_id) + 4 + len(payload)
    return _eth(dst, src, SUBTYPE_AECP, MSG_VU_COMMAND, cdl & 0x7FF, body)


class AecpResp:
    """Field view over an AECP response frame (wire offsets, no copies)."""

    def __init__(self, b):
        self.raw = bytes(b)

    def __len__(self):
        return len(self.raw)

    def __bool__(self):
        return len(self.raw) > 18

    def _be(self, off, n):
        return int.from_bytes(self.raw[off:off + n], "big") if len(self.raw) >= off + n else -1

    subtype = property(lambda s: s.raw[14] if len(s.raw) > 14 else -1)
    message_type = property(lambda s: (s.raw[15] & 0x0F) if len(s.raw) > 15 else -1)
    sv = property(lambda s: ((s.raw[15] >> 7) & 1) if len(s.raw) > 15 else -1)
    version = property(lambda s: ((s.raw[15] >> 4) & 7) if len(s.raw) > 15 else -1)
    status = property(lambda s: ((s.raw[16] >> 3) & 0x1F) if len(s.raw) > 16 else -1)
    cdl = property(lambda s: (((s.raw[16] & 7) << 8) | s.raw[17]) if len(s.raw) > 17 else -1)
    target_entity_id = property(lambda s: s._be(18, 8))
    controller_entity_id = property(lambda s: s._be(26, 8))
    sequence_id = property(lambda s: s._be(34, 2))
    u = property(lambda s: ((s.raw[36] >> 7) & 1) if len(s.raw) > 36 else -1)
    command_type = property(lambda s: (((s.raw[36] & 0x7F) << 8) | s.raw[37])
                            if len(s.raw) > 37 else -1)
    payload = property(lambda s: s.raw[38:])
    #: the PDU as tsn-gen wants it for an independent decode (from byte 15)
    pdu = property(lambda s: s.raw[15:])

    @property
    def cdl_ok(self):
        """IEEE 1722-2016 §5.4 on an unpadded sim frame: CDL == len - 26."""
        return len(self.raw) > 26 and self.cdl == len(self.raw) - 26

    def status_name(self):
        return STATUS.get(self.status, "status_%d" % self.status)


# --------------------------------------------------------------------- ACMP
ACMP_CONNECT_TX_COMMAND = 0
ACMP_CONNECT_TX_RESPONSE = 1
ACMP_DISCONNECT_TX_COMMAND = 2
ACMP_DISCONNECT_TX_RESPONSE = 3
ACMP_GET_TX_STATE_COMMAND = 4
ACMP_CONNECT_RX_COMMAND = 6
ACMP_CONNECT_RX_RESPONSE = 7
ACMP_DISCONNECT_RX_COMMAND = 8
ACMP_DISCONNECT_RX_RESPONSE = 9
ACMP_GET_RX_STATE_COMMAND = 10

ACMP_MCAST_MAC = bytes.fromhex("91e0f0010000")


def acmp_pdu(message_type, stream_id=0, controller=CTRLR_ID, talker=ENTITY_ID,
             listener=ENTITY_ID, talker_unique=0, listener_unique=0,
             dest_mac=b"\x91\xe0\xf0\x00\x3a\x99", connection_count=0, seq=1,
             flags=0, vlan=2, status=0, cdl=44, reserved=0,
             dst=ACMP_MCAST_MAC, src=CTRLR_MAC):
    """Build an ACMPDU frame — 70 bytes on the wire (1722.1 §8.2.1).

    The 70-byte length is load-bearing: controllers that emit 68-byte ACMPDUs
    are rightly rejected by the length check (see the acmp-listener-deaf
    finding), so length-probing is part of the campaign.
    """
    body = (struct.pack(">Q", stream_id) + struct.pack(">Q", controller)
            + struct.pack(">Q", talker) + struct.pack(">Q", listener)
            + struct.pack(">HH", talker_unique & 0xFFFF, listener_unique & 0xFFFF)
            + bytes(dest_mac)
            + struct.pack(">HHHHH", connection_count & 0xFFFF, seq & 0xFFFF,
                          flags & 0xFFFF, vlan & 0xFFFF, reserved & 0xFFFF))
    word16 = ((status & 0x1F) << 11) | (cdl & 0x7FF)
    return _eth(dst, src, SUBTYPE_ACMP, message_type & 0x0F, word16, body)


class AcmpResp(AecpResp):
    """Field view over an ACMPDU (shares the AVTPDU header offsets)."""
    stream_id = property(lambda s: s._be(18, 8))
    controller_entity_id = property(lambda s: s._be(26, 8))
    talker_entity_id = property(lambda s: s._be(34, 8))
    listener_entity_id = property(lambda s: s._be(42, 8))
    talker_unique_id = property(lambda s: s._be(50, 2))
    listener_unique_id = property(lambda s: s._be(52, 2))
    stream_dest_mac = property(lambda s: s.raw[54:60])
    connection_count = property(lambda s: s._be(60, 2))
    sequence_id = property(lambda s: s._be(62, 2))
    flags = property(lambda s: s._be(64, 2))
    stream_vlan_id = property(lambda s: s._be(66, 2))


# ---------------------------------------------------------------------- ADP
ADP_ENTITY_AVAILABLE = 0
ADP_ENTITY_DEPARTING = 1
ADP_ENTITY_DISCOVER = 2

ADP_MCAST_MAC = bytes.fromhex("91e0f0010000")


def adp_pdu(message_type=ADP_ENTITY_AVAILABLE, valid_time=10, entity_id=CTRLR_ID,
            entity_model_id=0, entity_caps=0, talker_sources=0, talker_caps=0,
            listener_sinks=0, listener_caps=0, controller_caps=0, available_index=0,
            gptp_gm=0, gptp_domain=0, reserved0=0, current_config=0,
            identify_control=0, interface_index=0, association_id=0, reserved1=0,
            cdl=56, dst=ADP_MCAST_MAC, src=CTRLR_MAC):
    """Build an ADPDU frame — 68-byte PDU, 82 bytes on the wire.

    The 82-byte frame length is load-bearing: the ADP census sweeps only
    trust LENGTH-validating decoders (AVTP shares ethertype 0x22F0, so
    ether[14]==0xFA is the discriminator). entity_id sits at wire byte 18.
    """
    body = (struct.pack(">QQ", entity_id, entity_model_id)
            + struct.pack(">I", entity_caps & 0xFFFFFFFF)
            + struct.pack(">HHHH", talker_sources & 0xFFFF, talker_caps & 0xFFFF,
                          listener_sinks & 0xFFFF, listener_caps & 0xFFFF)
            + struct.pack(">II", controller_caps & 0xFFFFFFFF,
                          available_index & 0xFFFFFFFF)
            + struct.pack(">Q", gptp_gm)
            + struct.pack(">BB", gptp_domain & 0xFF, reserved0 & 0xFF)
            + struct.pack(">HHH", current_config & 0xFFFF, identify_control & 0xFFFF,
                          interface_index & 0xFFFF)
            + struct.pack(">Q", association_id)
            + struct.pack(">I", reserved1 & 0xFFFFFFFF))
    word16 = ((valid_time & 0x1F) << 11) | (cdl & 0x7FF)
    return _eth(dst, src, SUBTYPE_ADP, message_type & 0x0F, word16, body)


class AdpResp(AecpResp):
    """Field view over an ADPDU."""
    valid_time = property(lambda s: ((s.raw[16] >> 3) & 0x1F) if len(s.raw) > 16 else -1)
    entity_id = property(lambda s: s._be(18, 8))
    entity_model_id = property(lambda s: s._be(26, 8))
    entity_capabilities = property(lambda s: s._be(34, 4))
    talker_stream_sources = property(lambda s: s._be(38, 2))
    talker_capabilities = property(lambda s: s._be(40, 2))
    listener_stream_sinks = property(lambda s: s._be(42, 2))
    listener_capabilities = property(lambda s: s._be(44, 2))
    controller_capabilities = property(lambda s: s._be(46, 4))
    available_index = property(lambda s: s._be(50, 4))
    gptp_grandmaster_id = property(lambda s: s._be(54, 8))
    gptp_domain_number = property(lambda s: s.raw[62] if len(s.raw) > 62 else -1)
    current_configuration_index = property(lambda s: s._be(64, 2))
    identify_control_index = property(lambda s: s._be(66, 2))
    interface_index = property(lambda s: s._be(68, 2))
    association_id = property(lambda s: s._be(70, 8))


# ------------------------------------------------------------------ AAF/AVTP
def aaf_pdu(stream_id=0x0200000000010000, sequence_num=0, avtp_timestamp=0,
            tv=1, mr=0, tu=0, sv=0, version=0, gv=0,
            nsr=2, channels_per_frame=2, bit_depth=24, aaf_format=2,
            stream_data_length=48, sparse=0, evt=0, payload=None,
            dst=b"\x91\xe0\xf0\x00\x3a\x99", src=ENTITY_MAC, vlan=None):
    """Build an AAF (1722-2016 §7) stream PDU.

    byte15 = sv(1) version(3) mr(1) r(1) gv(1) tv(1); the format-specific
    words carry {format, nsr, channels_per_frame, bit_depth} and
    {sparse, evt} exactly as `KL_aaf_rx_depacketizer` parses them.
    """
    if payload is None:
        payload = bytes(stream_data_length)
    b15 = ((sv & 1) << 7) | ((version & 7) << 4) | ((mr & 1) << 3) | ((gv & 1) << 1) | (tv & 1)
    hdr = struct.pack(">BB", SUBTYPE_AAF, b15)
    hdr += struct.pack(">BB", sequence_num & 0xFF, tu & 0x7F)
    hdr += struct.pack(">Q", stream_id)
    hdr += struct.pack(">I", avtp_timestamp & 0xFFFFFFFF)
    # format(8) nsr(4)/rsv(4) channels_per_frame(10) bit_depth(8) -> 4 bytes
    fsd = ((aaf_format & 0xFF) << 24) | ((nsr & 0x0F) << 20) \
        | ((channels_per_frame & 0x3FF) << 8) | (bit_depth & 0xFF)
    hdr += struct.pack(">I", fsd)
    hdr += struct.pack(">H", stream_data_length & 0xFFFF)
    hdr += struct.pack(">H", ((sparse & 1) << 12) | (evt & 0x0F))
    tag = b"" if vlan is None else struct.pack(">HH", 0x8100, vlan & 0x0FFF)
    if tag:
        return dst + src + tag + struct.pack(">H", ETHERTYPE_AVTP) + hdr + payload
    return dst + src + struct.pack(">H", ETHERTYPE_AVTP) + hdr + payload


# ----------------------------------------------------------------- 802.1AS
# The gPTP plane's wire layouts (802.1AS-2011 clause 11.4). Unlike the
# 1722.1 layouts above these are NOT offset by tsn-gen's missing-nibble
# defect: the 8021as_* models declare the full header from
# transport_specific down, so the model layout and the wire layout agree
# (the fuzz_ptp campaign cross-decodes to prove it every run). Offsets are
# FRAME offsets: Ethernet header 0..13, PTP common header 14..47 — the
# same map KL_gptp_rx_parser.sv walks.
ETHERTYPE_GPTP = 0x88F7
GPTP_MCAST_MAC = bytes.fromhex("0180c200000e")   # 802.1AS-2011 11.3.4 / Table 11-1
#: bench identities (mirror tb/verilator/gptp_shadow/sim_main.cpp and the
#: engine ucode default --mac 0x02A1B2C3D4E5)
GPTP_OUR_CID = 0x02A1B2FFFEC3D4E5
GPTP_PEER_MAC = bytes.fromhex("0080e1112233")
GPTP_PEER_CID = 0x0080E1FFFE112233
GPTP_PEER2_MAC = bytes.fromhex("0080e1445566")
GPTP_PEER2_CID = 0x0080E1FFFE445566

PTP_SYNC = 0x0
PTP_PDELAY_REQ = 0x2
PTP_PDELAY_RESP = 0x3
PTP_FOLLOW_UP = 0x8
PTP_PDELAY_RESP_FU = 0xA
PTP_ANNOUNCE = 0xB
PTP_SIGNALING = 0xC


def ts80(ns=0, seconds=None):
    """A 10-byte PTP timestamp. ns alone splits into {sec, ns} like the RTL."""
    if seconds is None:
        seconds, ns = divmod(int(ns), 1_000_000_000)
    return struct.pack(">HII", (seconds >> 32) & 0xFFFF,
                       seconds & 0xFFFFFFFF, ns & 0xFFFFFFFF)


def ptp_frame(message_type, body=b"", *, transport_specific=1, reserved0=0,
              version_ptp=2, message_length=None, domain_number=0, reserved1=0,
              flags=0, correction_field=0, reserved2=0,
              source_clock_identity=GPTP_PEER_CID, source_port_number=1,
              sequence_id=0, control=0x05, log_message_interval=0x7F,
              dst=GPTP_MCAST_MAC, src=GPTP_PEER_MAC, ethertype=ETHERTYPE_GPTP):
    """One 802.1AS frame: every header field individually probe-able.

    `message_length=None` derives the spec value (34 + body); pass an int to
    inject a wrong length. Field names match the tsn-gen 8021as_* models so
    the campaign can map oracle probes onto builder kwargs by name.
    """
    if message_length is None:
        message_length = 34 + len(body)
    hdr = struct.pack(">BBH",
                      ((transport_specific & 0xF) << 4) | (message_type & 0xF),
                      ((reserved0 & 0xF) << 4) | (version_ptp & 0xF),
                      message_length & 0xFFFF)
    hdr += struct.pack(">BBH", domain_number & 0xFF, reserved1 & 0xFF,
                       flags & 0xFFFF)
    hdr += struct.pack(">Q", correction_field & 0xFFFFFFFFFFFFFFFF)
    hdr += struct.pack(">I", reserved2 & 0xFFFFFFFF)
    hdr += struct.pack(">QH", source_clock_identity, source_port_number & 0xFFFF)
    hdr += struct.pack(">HBB", sequence_id & 0xFFFF, control & 0xFF,
                       log_message_interval & 0xFF)
    return dst + src + struct.pack(">H", ethertype) + hdr + body


def ptp_sync(sequence_id=0, **kw):
    """Two-step Sync (44 B PDU): origin zero, the Follow_Up carries time."""
    kw.setdefault("flags", 0x0208)                 # twoStep | ptpTimescale
    kw.setdefault("control", 0x00)
    kw.setdefault("log_message_interval", 0xFD)    # Milan Table 4.1: 125 ms
    return ptp_frame(PTP_SYNC, ts80(0), sequence_id=sequence_id, **kw)


def ptp_follow_up(sequence_id=0, origin_ns=0, tlv=True, tlv_type=0x0003,
                  cumulative_scaled_rate_offset=0, gm_time_base_indicator=0,
                  **kw):
    """Follow_Up: precise origin + (default) the information TLV (76 B PDU).

    `tlv=False` builds the 44-octet shape that omits the TLV Table 11-9 makes
    a field of the message; `tlv_type` injects a wrong tlvType (11.4.4.3.2
    fixes it at 0x3). Both are refusal probes, not legal frames.
    """
    kw.setdefault("flags", 0x0008)                 # ptpTimescale
    kw.setdefault("control", 0x02)
    kw.setdefault("log_message_interval", 0xFD)
    body = ts80(origin_ns)
    if tlv:
        body += struct.pack(">HH", tlv_type, 28)   # information TLV
        body += b"\x00\x80\xc2" + b"\x00\x00\x01"  # org id + org subtype 1
        body += struct.pack(">IH",
                            cumulative_scaled_rate_offset & 0xFFFFFFFF,
                            gm_time_base_indicator & 0xFFFF)
        body += bytes(12) + bytes(4)               # lastGmPhase / scaledFreq
    return ptp_frame(PTP_FOLLOW_UP, body, sequence_id=sequence_id, **kw)


def ptp_pdelay_req(sequence_id=0, **kw):
    """Pdelay_Req (54 B PDU): two reserved 10-byte fields."""
    kw.setdefault("control", 0x05)
    kw.setdefault("log_message_interval", 0x00)    # Milan Table 4.1: 1 s
    return ptp_frame(PTP_PDELAY_REQ, bytes(20), sequence_id=sequence_id, **kw)


def ptp_pdelay_resp(sequence_id=0, t2_ns=0, requesting_clock_identity=GPTP_OUR_CID,
                    requesting_port_number=1, **kw):
    """Pdelay_Resp (54 B PDU): t2 + the requester's port identity."""
    kw.setdefault("flags", 0x0200)                 # twoStep
    kw.setdefault("control", 0x05)
    body = ts80(t2_ns) + struct.pack(">QH", requesting_clock_identity,
                                     requesting_port_number & 0xFFFF)
    return ptp_frame(PTP_PDELAY_RESP, body, sequence_id=sequence_id, **kw)


def ptp_pdelay_resp_fu(sequence_id=0, t3_ns=0, requesting_clock_identity=GPTP_OUR_CID,
                       requesting_port_number=1, **kw):
    """Pdelay_Resp_Follow_Up (54 B PDU): t3 + the requester's port identity."""
    kw.setdefault("flags", 0x0000)
    kw.setdefault("control", 0x05)
    body = ts80(t3_ns) + struct.pack(">QH", requesting_clock_identity,
                                     requesting_port_number & 0xFFFF)
    return ptp_frame(PTP_PDELAY_RESP_FU, body, sequence_id=sequence_id, **kw)


def ptp_announce(sequence_id=0, gm_identity=0, gm_priority1=248, gm_priority2=248,
                 gm_clock_quality=0xF8FE436A, current_utc_offset=0,
                 steps_removed=0, time_source=0xA0, path_trace=None, **kw):
    """Announce (64 B PDU + path trace TLV).

    802.1AS-2011 10.5.3.3 REQUIRES the path trace TLV; `path_trace=None`
    defaults to the one-hop [gm_identity]. Pass `path_trace=[]` for the
    TLV-less shape the fabric bench uses (the parser accepts it).
    """
    kw.setdefault("flags", 0x0008)                 # ptpTimescale
    kw.setdefault("control", 0x05)
    kw.setdefault("log_message_interval", 0x00)    # Milan Table 4.1: 1 s
    if path_trace is None:
        path_trace = [gm_identity]
    body = bytes(10)                               # originTimestamp: reserved
    body += struct.pack(">hB", current_utc_offset, 0)
    body += struct.pack(">BIB", gm_priority1 & 0xFF, gm_clock_quality & 0xFFFFFFFF,
                        gm_priority2 & 0xFF)
    body += struct.pack(">QHB", gm_identity, steps_removed & 0xFFFF,
                        time_source & 0xFF)
    if path_trace:
        body += struct.pack(">HH", 0x0008, 8 * len(path_trace))
        for cid in path_trace:
            body += struct.pack(">Q", cid)
    return ptp_frame(PTP_ANNOUNCE, body, sequence_id=sequence_id, **kw)


class PtpMsg:
    """Field view over an 802.1AS frame (frame offsets, no copies)."""

    def __init__(self, b):
        self.raw = bytes(b)

    def __len__(self):
        return len(self.raw)

    def __bool__(self):
        return len(self.raw) >= 48 and self.ethertype == ETHERTYPE_GPTP

    def _be(self, off, n):
        return int.from_bytes(self.raw[off:off + n], "big") \
            if len(self.raw) >= off + n else -1

    dst = property(lambda s: s.raw[0:6])
    src = property(lambda s: s.raw[6:12])
    ethertype = property(lambda s: s._be(12, 2))
    transport_specific = property(lambda s: (s.raw[14] >> 4) & 0xF
                                  if len(s.raw) > 14 else -1)
    message_type = property(lambda s: s.raw[14] & 0xF if len(s.raw) > 14 else -1)
    reserved0 = property(lambda s: (s.raw[15] >> 4) & 0xF if len(s.raw) > 15 else -1)
    version_ptp = property(lambda s: s.raw[15] & 0xF if len(s.raw) > 15 else -1)
    message_length = property(lambda s: s._be(16, 2))
    domain_number = property(lambda s: s.raw[18] if len(s.raw) > 18 else -1)
    reserved1 = property(lambda s: s.raw[19] if len(s.raw) > 19 else -1)
    flags = property(lambda s: s._be(20, 2))
    correction_field = property(lambda s: s._be(22, 8))
    reserved2 = property(lambda s: s._be(30, 4))
    source_clock_identity = property(lambda s: s._be(34, 8))
    source_port_number = property(lambda s: s._be(42, 2))
    sequence_id = property(lambda s: s._be(44, 2))
    control = property(lambda s: s.raw[46] if len(s.raw) > 46 else -1)
    log_message_interval = property(lambda s: s.raw[47] if len(s.raw) > 47 else -1)
    #: 10-byte timestamp position (sync origin / fu precise / pdelay t2, t3)
    ts_seconds = property(lambda s: s._be(48, 6))
    ts_ns = property(lambda s: s._be(54, 4))

    @property
    def ts_total_ns(self):
        return self.ts_seconds * 1_000_000_000 + self.ts_ns \
            if len(self.raw) >= 58 else -1

    requesting_clock_identity = property(lambda s: s._be(58, 8))
    requesting_port_number = property(lambda s: s._be(66, 2))
    # announce body
    current_utc_offset = property(lambda s: s._be(58, 2))
    gm_priority1 = property(lambda s: s.raw[61] if len(s.raw) > 61 else -1)
    gm_clock_quality = property(lambda s: s._be(62, 4))
    gm_priority2 = property(lambda s: s.raw[66] if len(s.raw) > 66 else -1)
    gm_identity = property(lambda s: s._be(67, 8))
    steps_removed = property(lambda s: s._be(75, 2))
    time_source = property(lambda s: s.raw[77] if len(s.raw) > 77 else -1)
    # follow-up information TLV
    fu_tlv_type = property(lambda s: s._be(58, 2))
    fu_csro = property(lambda s: s._be(68, 4))
    #: the PDU as an independent decoder wants it (from the header byte)
    pdu = property(lambda s: s.raw[14:])


# ------------------------------------------------------------------ self-test
def _selftest():
    """Pin the codecs against vectors the RTL testbenches already validate."""
    ok = True

    f = aecp_cmd(4, struct.pack(">HHHH", 0, 0, 0x0000, 0), seq=0x1001)
    exp = ("020000fffe016805ca95b2d122f0fb000014020000fffe0000016805ca95"
           "b2d10000100100040000000000000000")
    if f.hex() != exp:
        print("  [FAIL] AECP READ_DESCRIPTOR vector\n    got %s\n    exp %s" % (f.hex(), exp))
        ok = False
    r = AecpResp(f)
    for name, got, want in (("subtype", r.subtype, 0xFB), ("msg_type", r.message_type, 0),
                            ("cdl", r.cdl, 20), ("cmd", r.command_type, 4),
                            ("seq", r.sequence_id, 0x1001),
                            ("target", r.target_entity_id, ENTITY_ID),
                            ("len", len(f), 46)):
        if got != want:
            print("  [FAIL] AECP accessor %s: %s != %s" % (name, got, want))
            ok = False
    if not r.cdl_ok:
        print("  [FAIL] AECP CDL invariant (len-26)")
        ok = False

    a = acmp_pdu(ACMP_CONNECT_RX_COMMAND, stream_id=0x0200000000010000)
    if len(a) != 70:
        print("  [FAIL] ACMPDU length %d != 70 (1722.1 §8.2.1)" % len(a))
        ok = False
    ar = AcmpResp(a)
    if ar.subtype != 0xFC or ar.message_type != 6 or ar.cdl != 44:
        print("  [FAIL] ACMP header: subtype=%02x mt=%d cdl=%d"
              % (ar.subtype, ar.message_type, ar.cdl))
        ok = False
    if ar.stream_id != 0x0200000000010000 or ar.stream_vlan_id != 2:
        print("  [FAIL] ACMP body accessors")
        ok = False

    d = adp_pdu(entity_id=ENTITY_ID, valid_time=10)
    if len(d) != 82 or len(d) - 14 != 68:
        print("  [FAIL] ADP frame %d != 82 (68-byte PDU + 14 eth)" % len(d))
        ok = False
    dr = AdpResp(d)
    if dr.subtype != 0xFA or dr.entity_id != ENTITY_ID or dr.valid_time != 10 or dr.cdl != 56:
        print("  [FAIL] ADP accessors: entity_id at byte 18 / valid_time / cdl")
        ok = False

    p = aaf_pdu(stream_data_length=48)
    if len(p) != 14 + 24 + 48:
        print("  [FAIL] AAF frame length %d != 86" % len(p))
        ok = False
    if p[14] != 0x02:
        print("  [FAIL] AAF subtype")
        ok = False

    # 802.1AS: pin the shapes the fabric bench proves on the RTL
    # (tb/verilator/gptp_shadow/sim_main.cpp: pdreq 68 B, sync 58 B, and the
    # parser's absolute offsets OFF_TYPE 14 / OFF_SEQ0 44 / OFF_RQID_END 65)
    q = ptp_pdelay_req(sequence_id=0x1234)
    if len(q) != 68 or q[14] != 0x12 or q[15] != 0x02:
        print("  [FAIL] Pdelay_Req shape: len=%d hdr=%02x%02x" % (len(q), q[14], q[15]))
        ok = False
    qm = PtpMsg(q)
    for name, got, want in (("etype", qm.ethertype, ETHERTYPE_GPTP),
                            ("mtype", qm.message_type, PTP_PDELAY_REQ),
                            ("tspec", qm.transport_specific, 1),
                            ("ver", qm.version_ptp, 2),
                            ("len", qm.message_length, 54),
                            ("seq", qm.sequence_id, 0x1234),
                            ("logmi", qm.log_message_interval, 0),
                            ("srcid", qm.source_clock_identity, GPTP_PEER_CID)):
        if got != want:
            print("  [FAIL] PTP accessor %s: %s != %s" % (name, got, want))
            ok = False

    s = ptp_sync(sequence_id=7)
    if len(s) != 58 or PtpMsg(s).message_length != 44 or PtpMsg(s).flags != 0x0208:
        print("  [FAIL] Sync shape: len=%d ml=%d" % (len(s), PtpMsg(s).message_length))
        ok = False

    fu = ptp_follow_up(sequence_id=7, origin_ns=1_000_000_123,
                       cumulative_scaled_rate_offset=0x0BADF00D)
    fm = PtpMsg(fu)
    if len(fu) != 90 or fm.message_length != 76 or fm.fu_tlv_type != 0x0003 \
            or fm.ts_seconds != 1 or fm.ts_ns != 123 \
            or fm.fu_csro != 0x0BADF00D:
        print("  [FAIL] Follow_Up shape: len=%d ml=%d tlv=%04x ts=%d.%d csro=%08x"
              % (len(fu), fm.message_length, fm.fu_tlv_type, fm.ts_seconds,
                 fm.ts_ns, fm.fu_csro))
        ok = False

    r = ptp_pdelay_resp(sequence_id=9, t2_ns=5_000_000_000,
                        requesting_clock_identity=GPTP_OUR_CID)
    rm = PtpMsg(r)
    if len(r) != 68 or rm.requesting_clock_identity != GPTP_OUR_CID \
            or rm.requesting_port_number != 1 or rm.ts_seconds != 5 \
            or rm.flags != 0x0200:
        print("  [FAIL] Pdelay_Resp shape/accessors")
        ok = False

    an = ptp_announce(sequence_id=3, gm_identity=0x00AACCFFFE010203,
                      gm_priority1=100)
    am = PtpMsg(an)
    if len(an) != 90 or am.message_length != 76 \
            or am.gm_identity != 0x00AACCFFFE010203 or am.gm_priority1 != 100 \
            or am.gm_clock_quality != 0xF8FE436A or am.time_source != 0xA0:
        print("  [FAIL] Announce shape/accessors (with 1-hop path trace)")
        ok = False
    an0 = ptp_announce(sequence_id=3, gm_identity=1, path_trace=[])
    if len(an0) != 78 or PtpMsg(an0).message_length != 64:
        print("  [FAIL] Announce TLV-less shape: len=%d" % len(an0))
        ok = False

    print("  [ ok ] wire codecs match the RTL-testbench vectors" if ok else "  WIRE SELFTEST FAILED")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if _selftest() else 1)
