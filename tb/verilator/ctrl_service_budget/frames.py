# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Untagged control frames for the budget's stimulus, each built from its clause.

Every frame is the wire order KL_mbx's ingress takes: destination MAC, source
MAC, EtherType, payload, no FCS. Layouts:
  ADPDU  IEEE 1722.1-2021 6.2.1, 68 bytes after the Ethernet header;
  ACMPDU IEEE 1722.1-2021 8.2.1 at Milan v1.2 5.5.2.2's 56 bytes;
  AECPDU IEEE 1722.1-2021 9.2.1 (AEM, 9.2.1.2) and Milan v1.2 5.4.3 (MVU);
  MAAP   IEEE 1722-2016 B.2, 28 bytes after the Ethernet header;
  MRPDU  IEEE 802.1Q-2018 10.8.1 with MSRP's attributes of 35.2.2.
"""
from __future__ import annotations

from dataclasses import dataclass

ETH_AVTP = 0x22F0
ETH_MSRP = 0x22EA
ETH_MVRP = 0x88F5
ADP_ACMP_DA = 0x91E0F0010000      # IEEE 1722.1-2021 Table B.1
MAAP_DA = 0x91E0F000FF00          # IEEE 1722-2016 Table B.10
MSRP_DA = 0x0180C200000E          # IEEE 802.1Q-2018 35.2.2.1, the Nearest Bridge group address
MVRP_DA = 0x0180C2000021          # IEEE 802.1Q-2018 Table 10-1

ADP_AVAILABLE, ADP_DEPARTING, ADP_DISCOVER = 0, 1, 2           # IEEE 1722.1-2021 Table 6-1
ACMP = dict(PROBE_TX=0, PROBE_TX_RESPONSE=1, DISCONNECT_TX=2, DISCONNECT_TX_RESPONSE=3,
            GET_TX_STATE=4, GET_TX_STATE_RESPONSE=5, BIND_RX=6, BIND_RX_RESPONSE=7,
            UNBIND_RX=8, UNBIND_RX_RESPONSE=9, GET_RX_STATE=10, GET_RX_STATE_RESPONSE=11,
            GET_TX_CONNECTION=12, GET_TX_CONNECTION_RESPONSE=13)   # Table 8-1; Milan v1.2 5.5.2
MAAP_PROBE, MAAP_DEFEND, MAAP_ANNOUNCE = 1, 2, 3                 # IEEE 1722-2016 Table B.4


def be(value: int, size: int) -> bytes:
    """Big-endian, the wire order of every field here."""
    return value.to_bytes(size, 'big')


def ethernet(da: int, sa: int, ethertype: int, payload: bytes) -> bytes:
    """An untagged frame, padded to the 60-byte minimum before the FCS."""
    frame = be(da, 6) + be(sa, 6) + be(ethertype, 2) + payload
    return frame.ljust(60, b'\0')


def control_header(subtype: int, message_type: int, status_or_valid: int, length: int,
                   stream_or_entity: int) -> bytes:
    """The 12-byte AVTP control header: subtype, sv 0, version 0, type, status, length, id."""
    return (bytes((subtype, message_type & 0xF)) + be((status_or_valid << 11) | length, 2)
            + be(stream_or_entity, 8))


@dataclass(frozen=True)
class Adp:
    """The ADPDU fields after entity_id (6.2.1), each defaulting to 0 but valid_time."""
    valid_time: int = 10
    model: int = 0
    caps: int = 0
    talker_sources: int = 0
    talker_caps: int = 0
    listener_sinks: int = 0
    listener_caps: int = 0
    available_index: int = 0
    gm_id: int = 0
    domain: int = 0
    configuration: int = 0
    interface_index: int = 0


def adp(message_type: int, entity_id: int, sa: int, fields: Adp | None = None) -> bytes:
    """An ADPDU (6.2.1): control_data_length 56, entity_id in the header.

    After gptp_domain_number come reserved0 (8 bits), current_configuration_index,
    identify_control_index, interface_index, association_id and reserved1.
    """
    v = fields or Adp()
    body = (be(v.model, 8) + be(v.caps, 4) + be(v.talker_sources, 2) + be(v.talker_caps, 2)
            + be(v.listener_sinks, 2) + be(v.listener_caps, 2) + be(0, 4) + be(v.available_index, 4)
            + be(v.gm_id, 8) + be(v.domain, 1) + bytes(1) + be(v.configuration, 2) + be(0, 2)
            + be(v.interface_index, 2) + be(0, 8) + bytes(4))
    assert len(body) == 56
    return ethernet(ADP_ACMP_DA, sa, ETH_AVTP,
                    control_header(0xFA, message_type, v.valid_time, 56, entity_id) + body)


@dataclass(frozen=True)
class Acmp:
    """The ACMPDU fields (8.2.1), each defaulting to 0; the destination is the ADP/ACMP group."""
    status: int = 0
    stream_id: int = 0
    controller: int = 0
    talker: int = 0
    listener: int = 0
    talker_uid: int = 0
    listener_uid: int = 0
    dest_mac: int = 0
    count: int = 0
    sequence: int = 0
    flags: int = 0
    vlan: int = 0
    da: int = ADP_ACMP_DA


def acmp(message_type: int, sa: int, fields: Acmp) -> bytes:
    """An ACMPDU (8.2.1) at Milan's 56 bytes: control_data_length 44."""
    v = fields
    body = (be(v.controller, 8) + be(v.talker, 8) + be(v.listener, 8) + be(v.talker_uid, 2)
            + be(v.listener_uid, 2) + be(v.dest_mac, 6) + be(v.count, 2) + be(v.sequence, 2)
            + be(v.flags, 2) + be(v.vlan, 2) + bytes(2))
    assert len(body) == 44
    return ethernet(v.da, sa, ETH_AVTP, control_header(0xFC, message_type, v.status, 44, v.stream_id) + body)


@dataclass(frozen=True)
class Aem:
    """An AECP command's addressing: target and controller entity, source and destination MAC, sequence_id."""
    target: int
    controller: int
    sa: int
    da: int
    sequence: int


def aem_command(to: Aem, command_type: int, payload: bytes = b'') -> bytes:
    """An AEM_COMMAND (9.2.1.2): message_type 0; control_data_length counts from controller_entity_id."""
    body = be(to.controller, 8) + be(to.sequence, 2) + be(command_type & 0x7FFF, 2) + payload
    return ethernet(to.da, to.sa, ETH_AVTP, control_header(0xFB, 0, 0, len(body), to.target) + body)


def read_descriptor(to: Aem, descriptor_type: int, descriptor_index: int, configuration: int = 0) -> bytes:
    """READ_DESCRIPTOR (IEEE 1722.1-2021 7.4.5.1), command_type 0x0004."""
    return aem_command(to, 0x0004,
                       be(configuration, 2) + bytes(2) + be(descriptor_type, 2) + be(descriptor_index, 2))


def mvu_command(to: Aem, command_type: int, payload: bytes = b'') -> bytes:
    """A Milan MVU command (Milan v1.2 5.4.3.1): message_type 6, the Milan protocol identifier."""
    protocol_id = 0x001BC50AC100
    body = be(to.controller, 8) + be(to.sequence, 2) + be(protocol_id, 6) + be(command_type, 2) + payload
    return ethernet(to.da, to.sa, ETH_AVTP, control_header(0xFB, 6, 0, len(body), to.target) + body)


def maap(message_type: int, sa: int, requested: tuple[int, int], conflict: tuple[int, int] = (0, 0),
         da: int = MAAP_DA) -> bytes:
    """A MAAPDU (B.2): maap_version 1, control_data_length 16, stream_id 0; (start, count) ranges."""
    body = be(requested[0], 6) + be(requested[1], 2) + be(conflict[0], 6) + be(conflict[1], 2)
    return ethernet(da, sa, ETH_AVTP, control_header(0xFE, message_type, 1, 16, 0) + body)


def mrp_message(attribute_type: int, first_value: bytes, events: list[int],
                four_packed: list[int] | None = None, leave_all: bool = False,
                list_length: bool = True) -> bytes:
    """One MRP Message (10.8.1.2) with one VectorAttribute of len(events) values.

    events are AttributeEvents (10.8.1.2: 0 New, 1 JoinIn, 2 In, 3 JoinMt, 4 Mt, 5 Lv),
    packed three per byte (ThreePackedEvents, 10.8.2.10); four_packed carries
    MSRP's FourPackedEvents for Listener declarations (35.2.2.7).
    """
    three = b''
    for i in range(0, len(events), 3):
        chunk = (events[i:i + 3] + [0, 0])[:3]
        three += bytes((chunk[0] * 36 + chunk[1] * 6 + chunk[2],))
    four = b''
    if four_packed is not None:
        for i in range(0, len(four_packed), 4):
            chunk = (four_packed[i:i + 4] + [0, 0, 0])[:4]
            four += bytes(((chunk[0] << 6) | (chunk[1] << 4) | (chunk[2] << 2) | chunk[3],))
    header = be((0x2000 if leave_all else 0) | len(events), 2)
    vector = header + first_value + three + four + b'\0\0'
    out = bytes((attribute_type, len(first_value)))
    return out + (be(len(vector), 2) if list_length else b'') + vector


def msrp(sa: int, messages: list[bytes]) -> bytes:
    """An MSRP MRPDU (35.2.2): ProtocolVersion 0, its Messages, the PDU EndMark."""
    return ethernet(MSRP_DA, sa, ETH_MSRP, b'\0' + b''.join(messages) + b'\0\0')


def domain_value(sr_class_id: int, priority: int, vid: int) -> bytes:
    """The Domain FirstValue (35.2.2.8.6): SRclassID, SRclassPriority, SRclassVID."""
    return bytes((sr_class_id, priority)) + be(vid, 2)


def hexed(frame: bytes) -> str:
    """The stimulus script's form of a frame."""
    return frame.hex()
