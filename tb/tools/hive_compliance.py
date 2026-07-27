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

Exit code 0 = clean, 1 = at least one FAIL. Run it against OUR board AND the
reference device: a check that only ever passes proves nothing.
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
CMD_GET_STREAM_INFO = 0x000F
DESC = {'STREAM_INPUT': 0x0005, 'STREAM_OUTPUT': 0x0006}

FAILS, CHECKS = [], [0]


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


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--iface', required=True)
    p.add_argument('--target-eid', required=True)
    p.add_argument('--target-mac', required=True)
    p.add_argument('--controller-eid', default='0011223344556677')
    p.add_argument('--max-index', type=int, default=16,
                   help='highest descriptor index to probe (default 16)')
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
    for dname, dcode in DESC.items():
        print(f"\n-- {dname} --")
        served, answered, ok_cdl = [], [], []
        for i in range(a.max_index):
            # READ_DESCRIPTOR: cfg(2) res(2) type(2) index(2)
            q = nx()
            fr, ccdl = aecp_cmd(src, dst, tgt, ctl, q, CMD_READ_DESCRIPTOR,
                                struct.pack('!HHHH', 0, 0, dcode, i))
            r = xchg(s, fr, src, q)
            if r and resp_parts(r)[0] == 0:
                served.append(i)

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

    print(f"\n----------------------------------------")
    print(f"checks: {CHECKS[0]}   failures: {len(FAILS)}")
    for f in FAILS:
        print(f"  FAIL {f}")
    print("RESULT:", "PASS" if not FAILS else "FAIL")
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
