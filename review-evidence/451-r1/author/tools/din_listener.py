#!/usr/bin/env python3
"""Software SRP listener for the DIN direction (controller host, under sudo,
inside with_gptp.py so the port is gPTP-capable and inside the SRP domain).

usage: din_listener.py <iface> <seconds> <pcap> <out_jsonl>

1. ACMP CONNECT_TX_COMMAND (a Milan PROBE_TX) to DUT STREAM_OUTPUT 0 from one
   software listener entity; the response names the stream, DMAC and VLAN.
2. Every 0.5 s, and at once on every MRP PDU from the bridge (so a LeaveAll
   is answered immediately): MSRP Domain
   (class A, priority 3, the response VLAN) JoinIn, MSRP Listener Ready JoinIn
   for the stream, MVRP JoinIn for the VLAN.
3. tcpdump records every frame from the DUT MAC for <seconds>.
4. At the end: MSRP/MVRP Leave, ACMP DISCONNECT_TX_COMMAND, tcpdump stopped.
Nothing is detached.
"""
import json
import select
import signal
import socket
import struct
import subprocess
import sys
import time

ETH_AVTP, ETH_MSRP, ETH_MVRP = 0x22F0, 0x22EA, 0x88F5
ACMP_MC = bytes.fromhex("91e0f0010000")
MSRP_MC = bytes.fromhex("0180c200000e")
MVRP_MC = bytes.fromhex("0180c2000021")
DUT_EID = bytes.fromhex("020000fffe000001")
LISTENER_EID = None                     # derived from the NIC address at start (see main)
JOIN_IN, LV = 1, 5
READY = 2
stop = False


def emit(f, obj):
    obj.setdefault("t", round(time.time(), 6))
    f.write(json.dumps(obj, separators=(",", ":")) + "\n")
    f.flush()


def acmp(sock, src, mt, seq, ctrl):
    body = (bytes(8) + ctrl + DUT_EID + LISTENER_EID + struct.pack(">HH", 0, 0) + bytes(6)
            + struct.pack(">HHHHH", 0, seq, 0, 0, 0))
    sock.send(ACMP_MC + src + struct.pack(">H", ETH_AVTP) + struct.pack(">BBH", 0xFC, mt, 44) + body)


def pad(fr):
    return fr + bytes(max(0, 60 - len(fr)))


def msrp_pdu(src, sid, vid, ev):
    dom = struct.pack(">H", 1) + bytes((6, 3)) + struct.pack(">H", vid) + bytes((ev * 36,))
    lis = struct.pack(">H", 1) + sid + bytes((ev * 36, READY << 6))
    body = (b"\x00"
            + bytes((4, 4)) + struct.pack(">H", len(dom) + 2) + dom + b"\x00\x00"
            + bytes((3, 8)) + struct.pack(">H", len(lis) + 2) + lis + b"\x00\x00"
            + b"\x00\x00")
    return pad(MSRP_MC + src + struct.pack(">H", ETH_MSRP) + body)


def mvrp_pdu(src, vid, ev):
    body = b"\x00" + bytes((1, 2)) + struct.pack(">H", 1) + struct.pack(">H", vid) + bytes((ev * 36,)) + b"\x00\x00\x00\x00"
    return pad(MVRP_MC + src + struct.pack(">H", ETH_MVRP) + body)


def main():
    global stop
    iface, seconds, pcap, out = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]
    log = open(out, "w")
    src = bytes.fromhex(open(f"/sys/class/net/{iface}/address").read().strip().replace(":", ""))
    global LISTENER_EID
    ctrl = src[:3] + b"\xff\xfe" + src[3:]
    LISTENER_EID = src[:3] + b"\xff\xfe" + src[3:4] + b"\xa4\x03"

    def on_sig(*a):
        global stop
        stop = True
    signal.signal(signal.SIGINT, on_sig)
    signal.signal(signal.SIGTERM, on_sig)
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    s.setsockopt(263, 23, 1)            # PACKET_IGNORE_OUTGOING
    s.bind((iface, 0x0003))
    for mc in (ACMP_MC, MSRP_MC, MVRP_MC):
        s.setsockopt(263, 1, struct.pack("iHH8s", socket.if_nametoindex(iface), 0, 6, mc + b"\x00\x00"))
    td = subprocess.Popen(["timeout", str(int(seconds + 20)), "tcpdump", "-n", "-U", "-B", "65536", "-i", iface,
                           "-w", pcap, "ether src 02:00:00:00:00:01"], stderr=subprocess.PIPE, text=True)
    time.sleep(1.0)
    # a Milan talker answers the first probe TALKER_DEST_MAC_FAIL while it
    # allocates its MAAP address: probe again (1 s apart) until SUCCESS
    seq = 0x4403
    sid, vid, dmac = None, 2, None
    for attempt in range(12):
        seq += 1
        acmp(s, src, 0, seq, ctrl)
        emit(log, dict(kind="probe-sent", seq=seq, attempt=attempt))
        t_end = time.monotonic() + 1.0
        status = None
        while time.monotonic() < t_end and status is None:
            r, _, _ = select.select([s], [], [], 0.1)
            if not r:
                continue
            fr = s.recv(2048)
            if struct.unpack(">H", fr[12:14])[0] != ETH_AVTP:
                continue
            p = fr[14:]
            if p[0] == 0xFC and (p[1] & 0x0F) == 1 and struct.unpack(">H", p[48:50])[0] == seq:
                status = p[2] >> 3
                emit(log, dict(kind="probe-response", status=status, stream_id=p[4:12].hex(), dmac=p[40:46].hex(),
                               vlan=struct.unpack(">H", p[52:54])[0], conn_count=struct.unpack(">H", p[46:48])[0],
                               flags=f"{struct.unpack('>H', p[50:52])[0]:#06x}"))
                if status == 0:
                    sid, dmac = p[4:12], p[40:46]
                    vid = struct.unpack(">H", p[52:54])[0] or 2
        if sid is not None:
            break
        time.sleep(max(0.0, t_end - time.monotonic()))
    if sid is None:
        sid = bytes.fromhex("0200000000010000")
        emit(log, dict(kind="probe-timeout", fallback_stream_id=sid.hex()))
    t_stop = time.monotonic() + seconds
    nxt = 0.0
    counts = dict(declare=0, msrp_rx=0, mvrp_rx=0)
    first_ta = None
    while not stop and time.monotonic() < t_stop:
        now = time.monotonic()
        if now >= nxt:
            s.send(msrp_pdu(src, sid, vid, JOIN_IN))
            s.send(mvrp_pdu(src, vid, JOIN_IN))
            counts["declare"] += 1
            nxt = now + 0.5
        r, _, _ = select.select([s], [], [], 0.05)
        if not r:
            continue
        fr = s.recv(2048)
        et = struct.unpack(">H", fr[12:14])[0]
        if et not in (ETH_MSRP, ETH_MVRP):
            continue
        counts["msrp_rx" if et == ETH_MSRP else "mvrp_rx"] += 1
        # re-declare on every bridge MRP PDU, so a LeaveAll is answered at once
        if et == ETH_MSRP and first_ta is None and sid in fr:
            first_ta = time.time()
            emit(log, dict(kind="bridge-msrp-names-stream", hex=fr[14:].hex()[:240]))
        s.send(msrp_pdu(src, sid, vid, JOIN_IN))
        s.send(mvrp_pdu(src, vid, JOIN_IN))
        counts["redeclare_on_rx"] = counts.get("redeclare_on_rx", 0) + 1
    s.send(msrp_pdu(src, sid, vid, LV))
    s.send(mvrp_pdu(src, vid, LV))
    time.sleep(0.3)
    s.send(msrp_pdu(src, sid, vid, LV))
    s.send(mvrp_pdu(src, vid, LV))
    acmp(s, src, 2, seq + 1, ctrl)      # DISCONNECT_TX_COMMAND
    emit(log, dict(kind="withdrawn", **counts))
    td.send_signal(signal.SIGINT)
    try:
        _, err = td.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        td.kill()
        _, err = td.communicate()
    emit(log, dict(kind="tcpdump", rc=td.returncode, stderr=err.strip().splitlines()[-3:]))
    s.close()
    log.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
