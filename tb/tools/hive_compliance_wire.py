#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""hive_compliance_wire.py - the wire the Hive-grade checks speak over.

Split out of `hive_compliance.py` because the two halves answer different
questions and only one of them can be read without a device in the room.
THIS half is the transport: the octet offsets and command codes the clauses
fix, the AF_PACKET socket that has joined the AVDECC multicast group, the
frame builders, and the running tally every check records itself in. It
decides nothing. `hive_compliance.py` holds the checks and the CLI; the
network-free predicates and their self-test live in
`hive_compliance_oracle.py`.

The tally is deliberately a pair of MUTABLE module objects rather than a
counter and a string: `FAILS` and `CHECKS` are imported by name into the
checks module and into the CLI, and both bindings must reach the SAME list or
the exit code stops counting what was printed. That is also why this module
exists as a module and is never `__main__` - a script re-imported under its
own name would own a second, empty copy of both.
"""
import socket
import struct
import time
from dataclasses import dataclass

ETH_P_ALL = 0x0003
AVTP = 0x22F0
MCAST = bytes.fromhex('91e0f0010000')
SOL_PACKET, ADD_MEMBERSHIP, MR_MULTICAST = 263, 1, 0
SUBTYPE_ADP, SUBTYPE_AECP = 0xFA, 0xFB

CMD_READ_DESCRIPTOR = 0x0004
CMD_GET_STREAM_FORMAT = 0x0009
#: C12/C13 (re-added 2026-07-28; they landed as C5/C6 in e076647 and were
#: lost to a numbering collision when 3cea0e48's C5/C6 merged first):
#: descriptor geometry for the STREAM current_format field, and the Table
#: 7-156 counter bit positions the wire oracle reads.
DESCRIPTOR_OFF = 4                #: response payload: cfg(2) + reserved(2)
STREAM_CURRENT_FORMAT_OFF = 74    #: 1722.1-2021 7.2.6 Table 7-16
CTR_UNSUPPORTED_FORMAT = 8
CTR_FRAMES_RX = 11
CMD_GET_STREAM_INFO = 0x000F
CMD_GET_NAME = 0x0011
CMD_GET_SAMPLING_RATE = 0x0015
CMD_GET_CLOCK_SOURCE = 0x0017
CMD_GET_AVB_INFO = 0x0027
CMD_GET_AS_PATH = 0x0028
CMD_GET_COUNTERS = 0x0029
CMD_GET_AUDIO_MAP = 0x002B

STATUS_NOT_IMPLEMENTED = 1

DESC = {'STREAM_INPUT': 0x0005, 'STREAM_OUTPUT': 0x0006}
D_AUDIO_UNIT = 0x0002
D_AVB_INTERFACE = 0x0009
D_STREAM_PORT_INPUT = 0x000E
D_STREAM_PORT_OUTPUT = 0x000F
#: 1722.1-2021 Table 7.1: AUDIO_CLUSTER is 0x0014. It read 0x0016 here until
#: 2026-07-28, which is SENSOR_CLUSTER - a type this entity does not have - so
#: every READ_DESCRIPTOR C9 issued for a cluster came back NO_SUCH_DESCRIPTOR,
#: cluster_channels stayed empty and the 7.2.16 cluster_channel bound was
#! never asserted at all. It did not fail; it did not run (methodology R5: a
#: structural zero is not a measurement). Confirmed against the generated ROM:
#: the AX7101 8x8 descriptor set carries types 0x14 and 0x17, no 0x16.
D_AUDIO_CLUSTER = 0x0014
D_CLOCK_DOMAIN = 0x0024
STATUS_NO_SUCH_DESCRIPTOR = 2
STATUS_NOT_SUPPORTED = 11

#: STREAM_PORT descriptor (1722.1-2021 7.2.13) field offsets, counted from the
#: start of the descriptor: type 0, index 2, clock_domain_index 4, port_flags
#: 6, number_of_controls 8, base_control 10, number_of_clusters 12,
#: base_cluster 14, number_of_maps 16, base_map 18.
SP_NUM_CLUSTERS_OFF = 12
SP_BASE_CLUSTER_OFF = 14
SP_NUM_MAPS_OFF = 16
SP_BASE_MAP_OFF = 18
#: AUDIO_MAP descriptor (7.2.19): type(2) index(2) mappings_offset(2)
#: number_of_mappings(2), then number_of_mappings x 8-octet mappings
D_AUDIO_MAP = 0x0017
AM_NUM_MAPPINGS_OFF = 6
AM_ROWS_OFF = 8
#: AUDIO_CLUSTER descriptor (7.2.16): channel_count sits after object_name(64)
#: + localized_description(2) + signal_type(2) + signal_index(2) +
#: signal_output(2) + path_latency(4) + block_latency(4) = offset 84.
AC_CHANNEL_COUNT_OFF = 84
#: a READ_DESCRIPTOR response payload is configuration_index(2) + reserved(2)
#: then the descriptor bytes (7.4.5.2)
RD_DESC_OFF = 4
#: GET_AUDIO_MAP response payload (7.4.44.2): type(2) index(2) map_index(2)
#: number_of_maps(2) number_of_mappings(2) reserved(2) then 8 B per mapping
AM_HDR = 12

#: index used to force an error status - far past any real descriptor count
BAD_INDEX = 90

FAILS, CHECKS = [], [0]

#: every (label, command_type, response frame) this run collected, for the
#: whole-frame checks C7/C8 that apply to EVERY response regardless of command
SEEN = []

#: C3: the target's advertised shape, sniffed OPPORTUNISTICALLY out of every
#: receive the tool does. A fixed listen window at the start is a race - the
#: AX board advertises roughly every 7 s and a 6 s window missed it, which
#: would have SKIPPED C3, and a skipped check proves exactly nothing. The
#: whole run is tens of seconds, so sniffing throughout always catches one.
ADV = {}


def sniff_adp(f: bytes, tgt: bytes) -> None:
    """ADPDU (1722.1-2021 6.2.1): talker_stream_sources at ADPDU octet 24 and
    listener_stream_sinks at octet 28 -> frame bytes 38 and 42 (entity_id is
    at frame byte 18, a recorded bench trap)."""
    if len(f) < 60 or f[12:14] != struct.pack('!H', AVTP):
        return
    if f[14] != SUBTYPE_ADP or f[18:26] != tgt:
        return
    ADV['STREAM_OUTPUT'] = struct.unpack('!H', f[38:40])[0]
    ADV['STREAM_INPUT'] = struct.unpack('!H', f[42:44])[0]

def ck(ok: bool, name: str, detail: str = "") -> None:
    """Record one live check; a red one joins FAILS and decides the exit code."""
    CHECKS[0] += 1
    if not ok:
        FAILS.append(f"{name}: {detail}")
    print(f"  [{'ok  ' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))


# -------------------------------------------------------------- C13 wire ----
#  ACMP transport for the wire oracle, copied from the bench-proven builder
#  in avdecc/milan_controller.py rather than rewritten: the ACMPDU is 70
#  bytes on the wire (14 eth + 4 common + 52) and a 68-byte one is RIGHTLY
#  REJECTED - that cost a bench session once already. IEEE 1722.1-2021 Cl 8.
ACMP_MCAST = bytes.fromhex('91e0f0010000')


@dataclass
class Binding:
    """The ACMP connection identity: who asks, and which talker/listener pair.

    One object rather than five adjacent arguments: `controller`/`talker_eid`/
    `listener_eid` are Entity IDs and the two uids are descriptor indices, and
    a caller that transposed a pair of them would bind the wrong stream and
    then measure it (IEEE 1722.1-2021 Cl 8).
    """
    controller: bytes
    talker_eid: bytes
    listener_eid: bytes
    talker_uid: int
    listener_uid: int


@dataclass
class Peers:
    """The four addresses every AECP command frame carries.

    The same grouping `hive_compliance_clusters.Peers` makes, for the same
    reason: `src`/`dst` are MAC addresses and `target`/`controller` are Entity
    IDs, and a transposed pair builds a frame the device silently ignores.
    """
    src: bytes
    dst: bytes
    target: bytes
    controller: bytes


def acmp(s: socket.socket, src: bytes, msg_type: int, seq: int,
         binding: Binding, timeout: float = 2.0) -> bytes | None:
    """One ACMP exchange (Cl 8): the 70-byte response carrying `seq`, or None."""
    pkt = struct.pack('>BBH', 0xFC, msg_type & 0x0F, 44)
    pkt += b'\x00' * 8                                   # stream_id
    pkt += binding.controller + binding.talker_eid + binding.listener_eid
    pkt += struct.pack('>HH', binding.talker_uid, binding.listener_uid)
    pkt += b'\x00' * 6                                   # stream_dest_mac
    pkt += struct.pack('>HHHHH', 0, seq, 0, 0, 0)        # cnt/seq/flags/vlan/rsv
    s.send(ACMP_MCAST + src + struct.pack('>H', AVTP) + pkt)
    end = time.time() + timeout
    while time.time() < end:
        try:
            f = s.recv(2048)
        except socket.timeout:
            return None
        if len(f) < 70 or f[12:14] != struct.pack('>H', AVTP) or f[14] != 0xFC:
            continue
        if (f[15] & 0x0F) != ((msg_type & 0x0F) | 1):
            continue
        if struct.unpack('>H', f[62:64])[0] != seq:
            continue
        return f
    return None


def peer_counters(s: socket.socket, peers: Peers, seq: int, dtype: int,
                  index: int) -> dict[str, int | None] | None:
    """-> {name: value} for the peer's STREAM_INPUT counters, or None.

    IEEE 1722.1-2021 7.4.42: response payload is descriptor_type(2),
    descriptor_index(2), counters_valid(4), counters_block(32 x 4)."""
    fr, _ = aecp_cmd(peers, seq, CMD_GET_COUNTERS,
                     struct.pack('!HH', dtype, index))
    r = xchg(s, fr, peers.src, seq, tgt=peers.target)
    if not r:
        return None
    st, _, pl = resp_parts(r)
    if st != 0 or len(pl) < 8 + 128:
        return None
    valid = struct.unpack('!I', pl[4:8])[0]
    words = struct.unpack('!32I', pl[8:8 + 128])
    out = {}
    for bit, name in ((CTR_UNSUPPORTED_FORMAT, 'UNSUPPORTED_FORMAT'),
                      (CTR_FRAMES_RX, 'FRAMES_RX')):
        out[name] = words[bit] if (valid >> bit) & 1 else None
    return out


def open_sock(iface: str) -> socket.socket:
    """A raw AF_PACKET socket that has JOINED the AVDECC multicast group."""
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
    s.bind((iface, 0))
    # raw AVDECC tools MUST join the ADP/AECP multicast or responses are
    # NIC-dropped (recorded bench trap)
    s.setsockopt(SOL_PACKET, ADD_MEMBERSHIP,
                 struct.pack("iHH8s", s.if_nametoindex(iface)
                             if hasattr(s, 'if_nametoindex')
                             else socket.if_nametoindex(iface),
                             MR_MULTICAST, len(MCAST), MCAST))
    s.settimeout(1.0)
    return s


def aecp_cmd(peers: Peers, seq: int, cmd: int,
             payload: bytes) -> tuple[bytes, int]:
    """AEM command. The four addresses arrive as one `Peers` record rather
    than four adjacent `bytes` in a row: `src`/`dst` are MAC addresses and
    `target`/`controller` are Entity IDs, every caller already held them
    together, and a transposed pair builds a frame the device silently
    ignores. control_data_length counts the octets FOLLOWING
    target_entity_id (1722.1-2021 9.2.2.6) - controller_entity_id(8) +
    sequence_id(2) + u/command_type(2) + payload = 12 + len(payload).
    The old ``len(body)`` here counted the 8-octet target too; every small
    GET survived only because Ethernet 60-byte padding covered the
    over-declaration, and the A-F14 declared-vs-delivered validator
    (x32p_aslm) silently drops any frame whose payload outgrows that slack
    (first victims: ADD/REMOVE_AUDIO_MAPPINGS, bench 2026-08-02)."""
    body = struct.pack('!8s8sHH', peers.target, peers.controller,
                       seq, cmd) + payload
    cdl = len(body) - 8
    avtp = bytes([SUBTYPE_AECP, 0x00, 0x00 | ((cdl >> 8) & 0x07), cdl & 0xFF])
    return peers.dst + peers.src + struct.pack('!H', AVTP) + avtp + body, cdl


def xchg(s: socket.socket, frame: bytes, src: bytes, seq: int,
         tgt: bytes | None = None, timeout: float = 1.5) -> bytes | None:
    """Send one AECP frame and return the response carrying `seq`, or None;
    every ADPDU seen while waiting feeds the advertised shape (C3)."""
    s.send(frame)
    end = time.time() + timeout
    while time.time() < end:
        try:
            f = s.recv(2048)
        except socket.timeout:
            return None
        if tgt is not None:
            sniff_adp(f, tgt)
        if len(f) < 26 or f[12:14] != struct.pack('!H', AVTP):
            continue
        if f[14] != SUBTYPE_AECP or f[0:6] != src:
            continue
        if struct.unpack('!H', f[34:36])[0] != seq:
            continue
        return f
    return None


def resp_parts(f: bytes) -> tuple[int, int, bytes]:
    """-> (status, control_data_length, payload_bytes_after_cmd)"""
    status = (f[16] >> 3) & 0x1F
    cdl = ((f[16] & 0x07) << 8) | f[17]
    return status, cdl, f[38:]


@dataclass
class Probe:
    """The live conversation every block of checks below runs over.

    The socket, the four addresses each frame repeats, the parsed arguments
    and the sequence counter travel as one object, so each group of checks is
    a function of its own rather than another two hundred lines of `main`.
    `do` is the single recorded exchange: every response it sees joins SEEN,
    which is what makes C7 and C8 whole-session checks.
    """
    sock: object
    src: bytes
    dst: bytes
    tgt: bytes
    ctl: bytes
    args: object
    seq: int = 0x7000

    def peers(self) -> Peers:
        """The four addresses every frame of this conversation repeats."""
        return Peers(self.src, self.dst, self.tgt, self.ctl)

    def nx(self) -> int:
        """The next sequence_id for this run, wrapping at sixteen bits."""
        self.seq = (self.seq + 1) & 0xFFFF
        return self.seq

    def do(self, label: str, cmd: int,
           payload: bytes) -> tuple[bytes | None, int]:
        """one command/response exchange, recorded for C7/C8"""
        q = self.nx()
        fr, ccdl = aecp_cmd(self.peers(), q, cmd, payload)
        r = xchg(self.sock, fr, self.src, q, self.tgt)
        if r is not None:
            SEEN.append((label, cmd, ccdl, r))
        return r, ccdl
