#!/usr/bin/env python3
"""Raw-socket AVDECC (IEEE 1722.1) controller: ADP discovery, READ_DESCRIPTOR,
GET_COUNTERS, GET_STREAM_INFO, GET_AVB_INFO.  No la_avdecc dependency."""
import argparse, binascii, fcntl, json, socket, struct, sys, time
from dataclasses import dataclass

ETH_P_ALL = 0x0003
ETHERTYPE_AVTP = 0x22F0
AVDECC_MCAST = bytes.fromhex('91e0f0010000')

SOL_PACKET = 263
PACKET_ADD_MEMBERSHIP = 1
PACKET_MR_MULTICAST = 0
SIOCGIFHWADDR = 0x8927

SUBTYPE_ADP, SUBTYPE_AECP, SUBTYPE_ACMP = 0xFA, 0xFB, 0xFC

#! Opcodes are IEEE 1722.1-2021 Table 7-140. EVERY entry here is a READ:
#! this tool points at live silicon, so a typo that lands on a mutating
#! opcode changes the device under test instead of reporting on it. That is
#! not hypothetical - GET_AUDIO_MAP was 0x002C here until 2026-08-16, which
#! is ADD_AUDIO_MAPPINGS; the read is 0x002B.
CMD = {
    'ENTITY_AVAILABLE': 0x0002,
    'READ_DESCRIPTOR': 0x0004,
    'GET_CONFIGURATION': 0x0007,
    'GET_STREAM_FORMAT': 0x0009,
    'GET_STREAM_INFO': 0x000F,
    'GET_SAMPLING_RATE': 0x0015,
    'GET_CLOCK_SOURCE': 0x0017,
    'GET_AVB_INFO': 0x0027,
    'GET_AS_PATH': 0x0028,
    'GET_COUNTERS': 0x0029,
    'GET_AUDIO_MAP': 0x002B,
}

DESC = {
    'ENTITY': 0x0000, 'CONFIGURATION': 0x0001, 'AUDIO_UNIT': 0x0002,
    'STREAM_INPUT': 0x0005, 'STREAM_OUTPUT': 0x0006,
    'JACK_INPUT': 0x0007, 'JACK_OUTPUT': 0x0008, 'AVB_INTERFACE': 0x0009,
    'CLOCK_SOURCE': 0x000A, 'MEMORY_OBJECT': 0x000B, 'LOCALE': 0x000C,
    'STRINGS': 0x000D, 'STREAM_PORT_INPUT': 0x000E, 'STREAM_PORT_OUTPUT': 0x000F,
    'AUDIO_CLUSTER': 0x0014, 'AUDIO_MAP': 0x0017, 'CONTROL': 0x001A,
    'CLOCK_DOMAIN': 0x0024,
}
DESC_R = {v: k for k, v in DESC.items()}

STATUS = {0: 'SUCCESS', 1: 'NOT_IMPLEMENTED', 2: 'NO_SUCH_DESCRIPTOR',
          3: 'ENTITY_LOCKED', 4: 'ENTITY_ACQUIRED', 5: 'NOT_AUTHENTICATED',
          6: 'AUTHENTICATION_DISABLED', 7: 'BAD_ARGUMENTS', 8: 'NO_RESOURCES',
          9: 'IN_PROGRESS', 10: 'ENTITY_MISBEHAVING', 11: 'NOT_SUPPORTED',
          12: 'STREAM_IS_RUNNING'}

# counters_valid bit -> name, per descriptor type (IEEE 1722.1-2021 Tab 7-155..7-158,
# Milan 5.3.8.10).  Bit N indexes counters_block word N.
ENTITY_SPECIFIC = {24: 'ENTITY_SPECIFIC_8', 25: 'ENTITY_SPECIFIC_7',
                   26: 'ENTITY_SPECIFIC_6', 27: 'ENTITY_SPECIFIC_5',
                   28: 'ENTITY_SPECIFIC_4', 29: 'ENTITY_SPECIFIC_3',
                   30: 'ENTITY_SPECIFIC_2', 31: 'ENTITY_SPECIFIC_1'}

CTR_BITS = {
    DESC['ENTITY']: dict(ENTITY_SPECIFIC),
    DESC['AVB_INTERFACE']: {0: 'LINK_UP', 1: 'LINK_DOWN', 2: 'FRAMES_TX',
                            3: 'FRAMES_RX', 4: 'RX_CRC_ERROR',
                            5: 'GPTP_GM_CHANGED', **ENTITY_SPECIFIC},
    DESC['CLOCK_DOMAIN']: {0: 'LOCKED', 1: 'UNLOCKED', **ENTITY_SPECIFIC},
    DESC['STREAM_INPUT']: {0: 'MEDIA_LOCKED', 1: 'MEDIA_UNLOCKED',
                           2: 'STREAM_INTERRUPTED', 3: 'SEQ_NUM_MISMATCH',
                           4: 'MEDIA_RESET', 5: 'TIMESTAMP_UNCERTAIN',
                           6: 'TIMESTAMP_VALID', 7: 'TIMESTAMP_NOT_VALID',
                           8: 'UNSUPPORTED_FORMAT', 9: 'LATE_TIMESTAMP',
                           10: 'EARLY_TIMESTAMP', 11: 'FRAMES_RX',
                           12: 'FRAMES_TX', **ENTITY_SPECIFIC},
    DESC['STREAM_OUTPUT']: {0: 'STREAM_START', 1: 'STREAM_STOP',
                            2: 'MEDIA_RESET', 3: 'TIMESTAMP_UNCERTAIN',
                            4: 'FRAMES_TX', **ENTITY_SPECIFIC},
}


def mac_s(b: bytes) -> str:
    """The wire's six bytes as the colon-hex spelling `ip link` prints."""
    return ':'.join('%02x' % x for x in b)


def open_sock(iface: str, timeout: float = 1.0) -> socket.socket:
    """A raw socket on `iface`, joined to the AVDECC control multicast group so
    the entity's responses to 91:e0:f0:01:00:00 reach this process at all."""
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
    s.bind((iface, 0))
    idx = socket.if_nametoindex(iface)
    # PACKET_MR_MULTICAST: join the AVDECC control multicast group
    mreq = struct.pack('IHH8s', idx, PACKET_MR_MULTICAST, 6, AVDECC_MCAST)
    s.setsockopt(SOL_PACKET, PACKET_ADD_MEMBERSHIP, mreq)
    s.settimeout(timeout)
    return s


def my_mac(iface: str) -> bytes:
    """The interface's own MAC, which every command frame is sourced from."""
    # The raw-socket host tool already requires AF_PACKET. Query the same
    # interface descriptor directly instead of coupling it to a pseudo-file.
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        info = fcntl.ioctl(
            probe.fileno(), SIOCGIFHWADDR,
            struct.pack('256s', iface.encode('ascii')[:15]))
    finally:
        probe.close()
    return info[18:24]


def strip_vlan(pkt: bytes) -> tuple[bytes, bytes, int, bytes]:
    """Return (dst, src, ethertype, payload) skipping any 802.1Q tag."""
    dst, src = pkt[0:6], pkt[6:12]
    et = struct.unpack('!H', pkt[12:14])[0]
    off = 14
    while et in (0x8100, 0x88A8):
        et = struct.unpack('!H', pkt[off + 2:off + 4])[0]
        off += 4
    return dst, src, et, pkt[off:]


@dataclass
class Link:
    """One AECP conversation: the raw socket and the four addresses that every
    command on it repeats unchanged.

    Passing these five together is what keeps a command's OWN arguments -
    sequence number, opcode, descriptor type and index - visible at the call
    site instead of buried behind five fixed positional addresses.
    """
    sock: socket.socket
    iface_mac: bytes
    dst_mac: bytes
    target_eid: int
    controller_eid: int


def build_aecp(link: Link, seq: int, command: int, payload: bytes) -> bytes:
    """One AEM_COMMAND frame, padded to the 60-byte Ethernet minimum."""
    cdl = 8 + 8 + 2 + 2 + len(payload)          # target..end of cmd-specific
    b = bytearray()
    b += link.dst_mac + link.iface_mac + struct.pack('!H', ETHERTYPE_AVTP)
    b += bytes([SUBTYPE_AECP, 0x00])            # sv=0 ver=0 msg_type=0 AEM_COMMAND
    b += struct.pack('!H', (0 << 11) | cdl)     # status=0 | control_data_length
    b += struct.pack('!Q', link.target_eid)
    b += struct.pack('!Q', link.controller_eid)
    b += struct.pack('!H', seq)
    b += struct.pack('!H', command)             # u=0
    b += payload
    if len(b) < 60:
        b += b'\x00' * (60 - len(b))
    return bytes(b)


def aecp_xact(link: Link, seq: int, command: int, payload: bytes,
              retries: int = 4, timeout: float = 0.6) -> tuple[int | None, bytes | None]:
    """Send one command and return (status, command-specific payload).

    A response is only accepted when BOTH entity ids, the sequence number and
    the opcode match the command that is outstanding, so another controller's
    traffic on the same wire cannot be read as this device's answer.
    (None, None) means the entity never answered within `retries`.
    """
    frame = build_aecp(link, seq, command, payload)
    for _ in range(retries):
        link.sock.send(frame)
        deadline = time.time() + timeout
        while time.time() < deadline:
            link.sock.settimeout(max(0.01, deadline - time.time()))
            try:
                pkt = link.sock.recv(2048)
            except socket.timeout:
                break
            d, sr, et, p = strip_vlan(pkt)
            if et != ETHERTYPE_AVTP or len(p) < 24 or p[0] != SUBTYPE_AECP:
                continue
            msg_type = p[1] & 0x0F
            if msg_type != 1:                    # AEM_RESPONSE
                continue
            status = (p[2] >> 3) & 0x1F
            teid = struct.unpack('!Q', p[4:12])[0]
            ceid = struct.unpack('!Q', p[12:20])[0]
            rseq = struct.unpack('!H', p[20:22])[0]
            rcmd = struct.unpack('!H', p[22:24])[0] & 0x7FFF
            if teid != link.target_eid or ceid != link.controller_eid \
               or rseq != seq or rcmd != command:
                continue
            cdl = struct.unpack('!H', p[2:4])[0] & 0x07FF
            return status, p[24:4 + cdl]
    return None, None


def do_counters(link: Link, seq: int, dtype: int, dindex: int) -> dict[str, object]:
    """GET_COUNTERS decoded against the descriptor's own bit map. A valid bit
    with no name is reported under `unnamed` rather than dropped: an
    entity-specific counter this table does not know is still evidence."""
    st, pl = aecp_xact(link, seq, CMD['GET_COUNTERS'],
                       struct.pack('!HH', dtype, dindex))
    if st is None:
        return {'error': 'TIMEOUT'}
    if st != 0 or pl is None or len(pl) < 8:
        return {'error': STATUS.get(st, 'STATUS_%d' % st), 'raw_len': len(pl or b'')}
    rtype, rindex = struct.unpack('!HH', pl[0:4])
    valid = struct.unpack('!I', pl[4:8])[0]
    blk = pl[8:8 + 128]
    words = list(struct.unpack('!32I', blk.ljust(128, b'\x00')))
    names = CTR_BITS.get(dtype, {})
    out = {'descriptor': '%s.%d' % (DESC_R.get(rtype, hex(rtype)), rindex),
           'counters_valid': '0x%08X' % valid, 'counters': {}, 'unnamed': {}}
    for bit in range(32):
        if valid & (1 << bit):
            nm = names.get(bit)
            if nm:
                out['counters'][nm] = words[bit]
            else:
                out['unnamed']['bit%d' % bit] = words[bit]
    out['all_words'] = words
    return out


def do_read_desc(link: Link, seq: int, cfg: int, dtype: int,
                 dindex: int) -> tuple[int | None, bytes | None]:
    """READ_DESCRIPTOR of one descriptor, undecoded: (status, payload)."""
    st, pl = aecp_xact(link, seq, CMD['READ_DESCRIPTOR'],
                       struct.pack('!HHHH', cfg, 0, dtype, dindex))
    if st is None:
        return None, None
    return st, pl


def do_stream_info(link: Link, seq: int, dtype: int, dindex: int) -> dict[str, object]:
    """GET_STREAM_INFO decoded: the bound format, stream id, destination MAC
    and the MSRP state that explains a stream which is configured but silent."""
    st, pl = aecp_xact(link, seq, CMD['GET_STREAM_INFO'],
                       struct.pack('!HH', dtype, dindex))
    if st is None or st != 0 or pl is None or len(pl) < 46:
        return {'error': 'TIMEOUT' if st is None else STATUS.get(st, str(st))}
    rtype, rindex = struct.unpack('!HH', pl[0:4])
    flags = struct.unpack('!I', pl[4:8])[0]
    fmt = pl[8:16]
    sid = struct.unpack('!Q', pl[16:24])[0]
    msrp_acc_lat = struct.unpack('!I', pl[24:28])[0]
    dmac = pl[28:34]
    msrp_fail_code = pl[34]
    d = {'descriptor': '%s.%d' % (DESC_R.get(rtype, hex(rtype)), rindex),
         'flags': '0x%08X' % flags, 'stream_format': binascii.hexlify(fmt).decode(),
         'stream_id': '%016X' % sid, 'msrp_accumulated_latency': msrp_acc_lat,
         'stream_dest_mac': mac_s(dmac), 'msrp_failure_code': msrp_fail_code}
    if len(pl) >= 48:
        d['flags_ex'] = '0x%08X' % struct.unpack('!I', pl[44:48])[0] if len(pl) >= 48 else None
    return d


def do_avb_info(link: Link, seq: int, dindex: int) -> dict[str, object]:
    """GET_AVB_INFO decoded: the grandmaster this interface follows, its
    propagation delay, and the asCapable/gPTP/SRP flags behind one flag byte."""
    st, pl = aecp_xact(link, seq, CMD['GET_AVB_INFO'],
                       struct.pack('!HH', DESC['AVB_INTERFACE'], dindex))
    if st is None or st != 0 or pl is None or len(pl) < 20:
        return {'error': 'TIMEOUT' if st is None else STATUS.get(st, str(st))}
    gptp_gm = struct.unpack('!Q', pl[4:12])[0]
    ptp_domain = pl[16]
    flags = pl[17]
    return {'gptp_grandmaster_id': '%016X' % gptp_gm,
            'propagation_delay_ns': struct.unpack('!I', pl[12:16])[0],
            'gptp_domain_number': ptp_domain,
            'flags': '0x%02X' % flags,
            'as_capable': bool(flags & 0x01),
            'gptp_enabled': bool(flags & 0x02),
            'srp_enabled': bool(flags & 0x04)}


def discover(s: socket.socket, seconds: float) -> dict[str, dict[str, object]]:
    """Every entity that ADVERTISED itself within `seconds`, keyed by entity id.
    Nothing is transmitted: an entity absent here never sent an ADP."""
    ents = {}
    end = time.time() + seconds
    while time.time() < end:
        s.settimeout(max(0.05, end - time.time()))
        try:
            pkt = s.recv(2048)
        except socket.timeout:
            break
        d, sr, et, p = strip_vlan(pkt)
        if et != ETHERTYPE_AVTP or len(p) < 68 or p[0] != SUBTYPE_ADP:
            continue
        eid = struct.unpack('!Q', p[4:12])[0]
        emid = struct.unpack('!Q', p[12:20])[0]
        cap = struct.unpack('!I', p[20:24])[0]
        tsrc = struct.unpack('!H', p[24:26])[0]
        tcap = struct.unpack('!H', p[26:28])[0]
        lsink = struct.unpack('!H', p[28:30])[0]
        lcap = struct.unpack('!H', p[30:32])[0]
        ai = struct.unpack('!I', p[36:40])[0]
        gm = struct.unpack('!Q', p[40:48])[0]
        dom = p[48]
        ents['%016X' % eid] = {
            'mac': mac_s(sr), 'entity_model_id': '%016X' % emid,
            'entity_capabilities': '0x%08X' % cap,
            'talker_sources': tsrc, 'talker_caps': '0x%04X' % tcap,
            'listener_sinks': lsink, 'listener_caps': '0x%04X' % lcap,
            'gptp_gm_id': '%016X' % gm, 'gptp_domain': dom,
            'available_index': ai}
    return ents


def main() -> None:
    """Point the controller at live silicon and print one JSON report per mode.
    Every opcode it can send is a READ, so no mode changes the device."""
    ap = argparse.ArgumentParser()
    ap.add_argument('--iface', default='enp6s0')
    ap.add_argument('--controller-eid', default='0x6805CAFFFE95B2FF')
    ap.add_argument('--mode', required=True,
                    choices=['discover', 'counters', 'streaminfo', 'avbinfo',
                             'config', 'sweep', 'rawdesc'])
    ap.add_argument('--target-eid')
    ap.add_argument('--target-mac')
    ap.add_argument('--secs', type=float, default=4.0)
    ap.add_argument('--desc')          # e.g. STREAM_INPUT:0
    ap.add_argument('--n-in', type=int, default=0)
    ap.add_argument('--n-out', type=int, default=0)
    a = ap.parse_args()

    s = open_sock(a.iface)
    mac = my_mac(a.iface)
    ceid = int(a.controller_eid, 16)

    if a.mode == 'discover':
        print(json.dumps(discover(s, a.secs), indent=1))
        return

    teid = int(a.target_eid, 16)
    dst = bytes.fromhex(a.target_mac.replace(':', ''))
    link = Link(s, mac, dst, teid, ceid)
    seq = [int(time.time()) & 0x7FFF]

    def nx() -> int:
        """The next sequence number; a reused one reads as a retransmission."""
        seq[0] = (seq[0] + 1) & 0xFFFF
        return seq[0]

    if a.mode == 'rawdesc':
        dt, di = a.desc.split(':')
        st, pl = do_read_desc(link, nx(), 0,
                              DESC[dt] if dt in DESC else int(dt, 0), int(di))
        print('status=%s len=%s' % (st, len(pl) if pl is not None else None))
        if pl:
            print(binascii.hexlify(pl).decode())
        return

    if a.mode == 'config':
        st, pl = do_read_desc(link, nx(), 0, DESC['CONFIGURATION'], 0)
        if st != 0:
            print(json.dumps({'error': 'READ_DESCRIPTOR CONFIGURATION st=%s' % st}))
            return
        # payload: desc_type(2) desc_index(2) object_name(64) localized(2)
        #          descriptor_counts_count(2) descriptor_counts_offset(2) then pairs
        body = pl[4:]
        cnt = struct.unpack('!H', body[66:68])[0]
        off = struct.unpack('!H', body[68:70])[0]
        # offset is from start of the descriptor (i.e. from body[0]=desc_type)
        base = off - 4 if off >= 4 else off
        res = {'object_name': body[0:64].split(b'\x00')[0].decode('ascii', 'replace'),
               'counts': {}}
        for i in range(cnt):
            dt, dc = struct.unpack('!HH', body[base + 4 * i: base + 4 * i + 4])
            res['counts'][DESC_R.get(dt, hex(dt))] = dc
        print(json.dumps(res, indent=1))
        return

    if a.mode == 'sweep':
        out = {'t_wall': time.time(), 't_iso': time.strftime('%Y-%m-%dT%H:%M:%S')}
        out['ENTITY.0'] = do_counters(link, nx(), DESC['ENTITY'], 0)
        for i in range(2):
            out['AVB_INTERFACE.%d' % i] = do_counters(link, nx(),
                                                      DESC['AVB_INTERFACE'], i)
        out['CLOCK_DOMAIN.0'] = do_counters(link, nx(), DESC['CLOCK_DOMAIN'], 0)
        for i in range(a.n_in):
            out['STREAM_INPUT.%d' % i] = do_counters(link, nx(),
                                                     DESC['STREAM_INPUT'], i)
        for i in range(a.n_out):
            out['STREAM_OUTPUT.%d' % i] = do_counters(link, nx(),
                                                      DESC['STREAM_OUTPUT'], i)
        out['AVB_INFO.0'] = do_avb_info(link, nx(), 0)
        print(json.dumps(out, indent=1))
        return

    if a.mode == 'streaminfo':
        out = {}
        for i in range(a.n_in):
            out['STREAM_INPUT.%d' % i] = do_stream_info(link, nx(),
                                                        DESC['STREAM_INPUT'], i)
        for i in range(a.n_out):
            out['STREAM_OUTPUT.%d' % i] = do_stream_info(link, nx(),
                                                         DESC['STREAM_OUTPUT'], i)
        print(json.dumps(out, indent=1))
        return

    if a.mode == 'avbinfo':
        print(json.dumps(do_avb_info(link, nx(), 0), indent=1))
        return

    if a.mode == 'counters':
        dt, di = a.desc.split(':')
        print(json.dumps(do_counters(link, nx(), DESC[dt], int(di)), indent=1))


if __name__ == '__main__':
    main()
