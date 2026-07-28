#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""hive_compliance.py - check an ATDECC entity the way Hive checks it.

    sudo ./hive_compliance.py --iface enp6s0 --target-eid 020000FFFE000001 \
                              --target-mac 02:00:00:00:00:01

WHY THIS EXISTS. On 2026-07-27 every one of our own gates was green - 57/57
Verilator suites, yosys 48/48, behave 113/113, lint at ratchet - while Hive
called our entity "not fully Milan compliant" fifteen times. Our raw-socket
tools (avdecc_ctl.py, avdecc_l2.py) missed it because they read the STATUS
byte and moved on; Hive also validates the RESPONSE FRAME ITSELF. Two tools
written from the same reading of the spec share the same blind spots, so this
one deliberately re-implements the checks a real controller stack makes:

  C1 PAYLOAD SIZE ON NON-SUCCESS RESPONSES.  A non-success AEM response must
     be the SAME SIZE as a SUCCESS response for that command - the status
     changes, the frame shape does not.  The rule is CALIBRATED per device
     from a real SUCCESS response rather than hardcoded, because the first
     version of this check asserted "echoes the COMMAND" and the negative
     control refuted it: the Milan-validated reference device answers a
     non-existent descriptor with 68 bytes (its GET_STREAM_INFO response
     size), not with the 24-byte command, and Hive accepts that. We answer
     with 16 - truncated - which is what Hive rejects.  Hive reported
     "Received an invalid non-success GET_STREAM_INFO AEM response (Incorrect
     payload size)" 15 times against us and only kept going because it was
     built with IGNORE_INVALID_NON_SUCCESS_AEM_RESPONSES; a strict controller
     DROPS the response and the entity looks dead rather than incomplete.
  C2 DESCRIPTOR SELF-CONSISTENCY.  Every descriptor READ_DESCRIPTOR serves
     must also answer its dynamic-info command.  We served STREAM_OUTPUT.4
     byte-for-byte and then returned NO_SUCH_DESCRIPTOR for GET_STREAM_INFO on
     the same index - the device contradicting itself between two commands.
  C3 ADVERTISED SHAPE == ADDRESSABLE SHAPE.  ADP talker_stream_sources /
     listener_stream_sinks must equal the number of descriptors that actually
     answer.  Advertising 9 and answering 1 is the 0x0015 defect's next layer.
  C4 MILAN RESERVED BITS.  Milan v1.2 5.4.2.10.1: StreamInfoFlags bit 24 is
     reserved and shall be 0 (this is the check Hive raised against the
     reference device, not against us - keep it so we never regress into it).
  C5 THE FORMAT IS ONE FORMAT.  A STREAM_OUTPUT states its current format in
     TWO places - the STREAM descriptor's current_format field
     (IEEE 1722.1-2021 7.2.6, Table 7-16, octets 74..81 of the descriptor) and
     the GET_STREAM_FORMAT (0x0009) response - and they must agree.  Same
     class as C2: a device contradicting itself between two commands.  A
     controller picks whichever it read first, and Milan 5.5.1.2's format
     compatibility check is run against ONE of them, so a disagreement is a
     bind that succeeds against a format the talker will not send.
  C6 ADVERTISED == EMITTED, ON THE WIRE (opt-in, --wire-*).  THE CHECK THAT
     WOULD HAVE CAUGHT 2026-07-27.  Every other check here, and every static
     gate in this repo, compares a declaration against another declaration.
     This one binds a REAL listener to the talker and reads that listener's
     counters: IEEE 1722.1-2021 Table 7-156 UNSUPPORTED_FORMAT must stay at 0
     while FRAMES_RX advances.  The AX7101 8x8 talkers advertised
     0x0205022002006000 (AAF, IEEE 1722-2016 7.3.3 channels_per_frame = 8),
     passed Milan 5.5.1.2, returned ACMP SUCCESS - and the reference device
     counted UNSUPPORTED_FORMAT on 296,294 of 296,294 frames because the
     framer emitted 2.  Non-success is not the signal; the COUNTER is.

LEVEL / ORACLE (docs/testing/methodology.md).  C1-C5 are LEVEL 4: what an
INDEPENDENT controller sees, oracle = a foreign implementation (Hive, and the
reference device's own answers, which is why C1 is calibrated per device rather
than hardcoded).  C6 is LEVEL 5: the wire, on hardware, oracle = a QUALIFIED
REFERENCE DEVICE's counters.  No check here reads our own RTL.

Exit code 0 = clean, 1 = at least one FAIL. Run it against OUR board AND the
reference device: a check that only ever passes proves nothing.

CALIBRATION STATUS (2026-07-28): C1-C4 are calibrated - the reference device
reads 22 checks / 0 failures.  C5 and C6 are NEW and NOT YET RUN against the
reference device.  If either fails there, the C1 precedent applies: assume the
CHECK is the invention and fix it here, do not "fix" the reference device.
"""
import argparse
import socket
import struct
import sys
import time

ETH_P_ALL = 0x0003
AVTP = 0x22F0
MCAST = bytes.fromhex('91e0f0010000')
SOL_PACKET, ADD_MEMBERSHIP, MR_MULTICAST = 263, 1, 0
SUBTYPE_ADP, SUBTYPE_AECP = 0xFA, 0xFB

CMD_READ_DESCRIPTOR = 0x0004
CMD_GET_STREAM_FORMAT = 0x0009
CMD_GET_STREAM_INFO = 0x000F
CMD_GET_COUNTERS = 0x0029
DESC = {'STREAM_INPUT': 0x0005, 'STREAM_OUTPUT': 0x0006}

#! IEEE 1722.1-2021 7.2.6 Table 7-16: octet offsets inside a STREAM descriptor
STREAM_CURRENT_FORMAT_OFF = 74
#! a READ_DESCRIPTOR response payload is configuration_index(2) + reserved(2)
#! before the descriptor itself (1722.1-2021 7.4.5.2)
DESCRIPTOR_OFF = 4

#! IEEE 1722.1-2021 Table 7-156 STREAM_INPUT counters_valid bit -> block word.
#! Only the two this check needs; avdecc_ctl.py carries the full table.
CTR_UNSUPPORTED_FORMAT = 8
CTR_FRAMES_RX = 11

FAILS, CHECKS = [], [0]


def aaf_channels(fmt):
    """channels_per_frame of an AAF stream_format qword (IEEE 1722-2016 7.3.3;
    the field a listener validates, and the one that was wrong). None for a
    non-AAF format - CRF (subtype 4) carries no channel count."""
    if ((fmt >> 56) & 0x7F) != 0x02:
        return None
    return (fmt >> 22) & 0x3FF


def ck(ok, name, detail=""):
    CHECKS[0] += 1
    if not ok:
        FAILS.append(f"{name}: {detail}")
    print(f"  [{'ok  ' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))


def open_sock(iface):
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


def aecp_cmd(src, dst, target, ctrlr, seq, cmd, payload):
    """AEM command. control_data_length counts from target_entity_id on."""
    body = struct.pack('!8s8sHH', target, ctrlr, seq, cmd) + payload
    cdl = len(body)
    avtp = bytes([SUBTYPE_AECP, 0x00, 0x00 | ((cdl >> 8) & 0x07), cdl & 0xFF])
    return dst + src + struct.pack('!H', AVTP) + avtp + body, cdl


def xchg(s, frame, src, seq, timeout=1.5):
    s.send(frame)
    end = time.time() + timeout
    while time.time() < end:
        try:
            f = s.recv(2048)
        except socket.timeout:
            return None
        if len(f) < 26 or f[12:14] != struct.pack('!H', AVTP):
            continue
        if f[14] != SUBTYPE_AECP or f[0:6] != src:
            continue
        if struct.unpack('!H', f[34:36])[0] != seq:
            continue
        return f
    return None


def resp_parts(f):
    """-> (status, control_data_length, payload_bytes_after_cmd)"""
    status = (f[16] >> 3) & 0x1F
    cdl = ((f[16] & 0x07) << 8) | f[17]
    return status, cdl, f[38:]


# --------------------------------------------------------------- C6 wire ----
#  ACMP transport, copied from the bench-proven builder in
#  avdecc/milan_controller.py rather than rewritten: the ACMPDU is 70 bytes on
#  the wire (14 eth + 4 common + 52) and a 68-byte one is RIGHTLY REJECTED -
#  that cost a bench session once already.  IEEE 1722.1-2021 Clause 8.
ACMP_MCAST = bytes.fromhex('91e0f0010000')


def acmp(s, src, msg_type, seq, ctlr, talker_eid, listener_eid,
         talker_uid, listener_uid, timeout=2.0):
    pkt = struct.pack('>BBH', 0xFC, msg_type & 0x0F, 44)
    pkt += b'\x00' * 8                                   # stream_id
    pkt += ctlr + talker_eid + listener_eid
    pkt += struct.pack('>HH', talker_uid, listener_uid)
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


def get_counters(s, src, dst, tgt, ctl, seq, dtype, index):
    """-> {name: value} for the STREAM_INPUT counters we care about, or None.

    IEEE 1722.1-2021 7.4.42: response payload is descriptor_type(2),
    descriptor_index(2), counters_valid(4), counters_block(32 x 4)."""
    fr, _ = aecp_cmd(src, dst, tgt, ctl, seq, CMD_GET_COUNTERS,
                     struct.pack('!HH', dtype, index))
    r = xchg(s, fr, src, seq)
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


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--iface', required=True)
    p.add_argument('--target-eid', required=True)
    p.add_argument('--target-mac', required=True)
    p.add_argument('--controller-eid', default='0011223344556677')
    p.add_argument('--max-index', type=int, default=16,
                   help='highest descriptor index to probe (default 16)')
    # C6: opt-in, because it needs a SECOND Milan device to bind to and it
    # changes the bench state (it connects and disconnects a stream).
    p.add_argument('--wire-peer-eid',
                   help='EID of a listener to bind to (PEER: '
                        '3CC0C60102030000). Enables C6.')
    p.add_argument('--wire-peer-mac', default='3c:c0:c6:01:02:03')
    p.add_argument('--wire-talker', type=int, default=0,
                   help='our STREAM_OUTPUT index to bind (default 0)')
    p.add_argument('--wire-sink', type=int, default=4,
                   help="peer STREAM_INPUT index. It must ACCEPT the format "
                        "we advertise or the test measures nothing: the PEER "
                        "map is 0,1 = 2ch, 2,3 = 4ch, 4-7 = 8ch, 8,9 = CRF "
                        "(default 4 = 8-channel)")
    p.add_argument('--wire-seconds', type=float, default=5.0,
                   help='counter integration window (default 5 s; at 8000 '
                        'PDU/s that is ~40,000 frames)')
    a = p.parse_args()

    tgt = bytes.fromhex(a.target_eid)
    ctl = bytes.fromhex(a.controller_eid)
    dst = bytes.fromhex(a.target_mac.replace(':', ''))
    s = open_sock(a.iface)
    src = s.getsockname()[4][:6]
    seq = [0x7000]

    def nx():
        seq[0] = (seq[0] + 1) & 0xFFFF
        return seq[0]

    print(f"=== hive_compliance {a.target_eid} on {a.iface} ===")
    fmts = {}                       # dname -> {index: current_format}
    for dname, dcode in DESC.items():
        print(f"\n-- {dname} --")
        served, answered, ok_cdl = [], [], []
        for i in range(a.max_index):
            # READ_DESCRIPTOR: cfg(2) res(2) type(2) index(2)
            q = nx()
            fr, ccdl = aecp_cmd(src, dst, tgt, ctl, q, CMD_READ_DESCRIPTOR,
                                struct.pack('!HHHH', 0, 0, dcode, i))
            r = xchg(s, fr, src, q)
            desc_fmt = None
            if r and resp_parts(r)[0] == 0:
                served.append(i)
                pl = resp_parts(r)[2]
                o = DESCRIPTOR_OFF + STREAM_CURRENT_FORMAT_OFF
                if len(pl) >= o + 8:
                    desc_fmt = struct.unpack('!Q', pl[o:o + 8])[0]
                    fmts.setdefault(dname, {})[i] = desc_fmt

            # C5: the descriptor's current_format (1722.1-2021 7.2.6) and the
            # GET_STREAM_FORMAT (0x0009) answer are the SAME fact stated twice.
            if desc_fmt is not None:
                q = nx()
                fr, _ = aecp_cmd(src, dst, tgt, ctl, q, CMD_GET_STREAM_FORMAT,
                                 struct.pack('!HH', dcode, i))
                r = xchg(s, fr, src, q)
                if r and resp_parts(r)[0] == 0 and len(resp_parts(r)[2]) >= 12:
                    gsf = struct.unpack('!Q', resp_parts(r)[2][4:12])[0]
                    nch = aaf_channels(desc_fmt)
                    ck(gsf == desc_fmt,
                       f"C5 {dname}.{i} descriptor current_format == "
                       f"GET_STREAM_FORMAT",
                       f"descriptor=0x{desc_fmt:016X} "
                       f"GET_STREAM_FORMAT=0x{gsf:016X}"
                       + (f" ({nch}ch AAF)" if nch is not None else " (non-AAF)"))

            # GET_STREAM_INFO: type(2) index(2)
            q = nx()
            fr, ccdl = aecp_cmd(src, dst, tgt, ctl, q, CMD_GET_STREAM_INFO,
                                struct.pack('!HH', dcode, i))
            r = xchg(s, fr, src, q)
            if not r:
                continue
            st, rcdl, pl = resp_parts(r)
            if st == 0:
                answered.append(i)
                ok_cdl.append(rcdl)
                # C4: Milan 5.4.2.10.1 - StreamInfoFlags bit 24 reserved = 0
                if len(pl) >= 8:
                    flags = struct.unpack('!I', pl[4:8])[0]
                    ck(((flags >> 24) & 1) == 0,
                       f"C4 {dname}.{i} StreamInfoFlags bit24 reserved=0",
                       f"flags=0x{flags:08X}")
            else:
                # C1: a NON-SUCCESS response must still echo the command's
                # control_data_length. This is the check our own tools skipped
                # and Hive flagged 15 times.
                want = ok_cdl[0] if ok_cdl else None
                if want is None:
                    print(f"  [skip] C1 {dname}.{i}: no SUCCESS response yet "
                          f"to calibrate the expected size against")
                else:
                    ck(rcdl == want,
                       f"C1 {dname}.{i} non-success size == success size",
                       f"status={st} resp_cdl={rcdl} success_cdl={want}")

        # C2: anything READ_DESCRIPTOR serves must answer GET_STREAM_INFO
        missing = [i for i in served if i not in answered]
        ck(not missing, f"C2 {dname} every served descriptor answers "
                        f"GET_STREAM_INFO",
           f"served={len(served)} answered={len(answered)} missing={missing}")
        print(f"     served={served}")
        print(f"     answered={answered}")

    # ------------------------------------------------------------- C6 ------
    if a.wire_peer_eid:
        print(f"\n-- C6 ADVERTISED == EMITTED (bind + counters) --")
        peid = bytes.fromhex(a.wire_peer_eid)
        pmac = bytes.fromhex(a.wire_peer_mac.replace(':', ''))
        fmt = fmts.get('STREAM_OUTPUT', {}).get(a.wire_talker)
        nch = aaf_channels(fmt) if fmt is not None else None
        if nch is None:
            ck(False, f"C6 talker {a.wire_talker} advertises an AAF format",
               f"current_format={'none' if fmt is None else hex(fmt)} - cannot "
               f"tell how many channels a listener should expect")
        else:
            print(f"     talker {a.wire_talker} advertises 0x{fmt:016X} "
                  f"= {nch}-channel AAF (IEEE 1722-2016 7.3.3)")
            print(f"     binding peer {a.wire_peer_eid} sink {a.wire_sink} "
                  f"-> expect UNSUPPORTED_FORMAT to stay 0")
            # DISCONNECT first: a sink left bound by an earlier run reports
            # counters for the OLD stream and every number below would be a
            # measurement of the previous experiment.
            acmp(s, src, 0x02, nx(), ctl, tgt, peid, a.wire_talker, a.wire_sink)
            r = acmp(s, src, 0x00, nx(), ctl, tgt, peid,
                     a.wire_talker, a.wire_sink)
            st = None if r is None else (r[16] >> 3) & 0x1F
            ck(st == 0, f"C6 ACMP CONNECT_RX talker {a.wire_talker} -> peer "
                        f"sink {a.wire_sink} returns SUCCESS",
               f"status={st}")
            if st == 0:
                c0 = get_counters(s, src, pmac, peid, ctl, nx(),
                                  DESC['STREAM_INPUT'], a.wire_sink)
                time.sleep(a.wire_seconds)
                c1 = get_counters(s, src, pmac, peid, ctl, nx(),
                                  DESC['STREAM_INPUT'], a.wire_sink)
                if not c0 or not c1:
                    ck(False, "C6 peer answered GET_COUNTERS on its sink",
                       f"before={c0} after={c1}")
                else:
                    rx = (c1['FRAMES_RX'] or 0) - (c0['FRAMES_RX'] or 0)
                    uf = (c1['UNSUPPORTED_FORMAT'] or 0) - \
                         (c0['UNSUPPORTED_FORMAT'] or 0)
                    ck(rx > 0, "C6 peer FRAMES_RX advances (the talker emits)",
                       f"+{rx} frames in {a.wire_seconds}s")
                    # THE MEASUREMENT. 2026-07-27 baseline for this exact
                    # binding: 296,294 of 296,294 frames UNSUPPORTED_FORMAT.
                    ck(uf == 0,
                       f"C6 peer UNSUPPORTED_FORMAT == 0 for the "
                       f"{nch}-channel format we advertise",
                       f"+{uf} unsupported of +{rx} received - the fabric is "
                       f"not emitting the channels_per_frame the entity "
                       f"advertises (IEEE 1722-2016 7.3.3)")
            acmp(s, src, 0x02, nx(), ctl, tgt, peid, a.wire_talker, a.wire_sink)

    print(f"\n----------------------------------------")
    print(f"checks: {CHECKS[0]}   failures: {len(FAILS)}")
    for f in FAILS:
        print(f"  FAIL {f}")
    print("RESULT:", "PASS" if not FAILS else "FAIL")
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
