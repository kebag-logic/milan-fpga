#!/usr/bin/env python3
"""Software AAF talker for the DOUT direction (controller host, under sudo).

usage: aaf_talker.py <iface> <seconds> <out_jsonl> <dut_ppm> [<phc_dev>]

Advertises one talker entity over ADP, answers the DUT listener's PROBE_TX
(ACMP CONNECT_TX_COMMAND) for it, and sends 8-channel INT32 48 kHz AAF, six
frames per PDU, untagged and unicast to the DUT. Sample for channel c (0..7)
of frame ordinal n: 24-bit ((c + 1) << 16) | (n & 0xffff), left-justified in
the 32-bit big-endian word. The PDU cadence is the DUT's media grid as seen
from gPTP time: the PHC (disciplined by a slave-only ptp4l) is read directly,
and the frame rate is 48 kHz scaled by (1 + dut_ppm * 1e-6). avtp_timestamp
is PHC time of the PDU's first frame + 2 ms. Nothing is detached; SIGINT or
the deadline ends it, and it sends ENTITY_DEPARTING on exit.
"""
import gc
import json
import os
import select
import signal
import socket
import struct
import sys
import threading
import time

ETH_AVTP = 0x22F0
ADP_MC = bytes.fromhex("91e0f0010000")
DUT_MAC = bytes.fromhex("020000000001")
# entity and model ids derive from the NIC address at start (see main)
TALKER_EID = MODEL_ID = None
GM_ID = bytes.fromhex(os.environ.get("GM_ID", "0000000000000000"))  # advertised grandmaster
SPF, CH, RATE = 6, 8, 48000
PRES_NS = 2_000_000

stop = threading.Event()


def emit(f, obj):
    obj.setdefault("t", round(time.time(), 6))
    f.write(json.dumps(obj, separators=(",", ":")) + "\n")
    f.flush()


def adp(src, msg_type, avail_index):
    # AEM_SUPPORTED | CLASS_A_SUPPORTED | GPTP_SUPPORTED; one audio talker source
    body = (TALKER_EID + MODEL_ID + struct.pack(">I", 0x00000508)
            + struct.pack(">HHHH", 1, 0x4001, 0, 0) + struct.pack(">I", 0)
            + struct.pack(">I", avail_index) + GM_ID + bytes(4)
            + struct.pack(">HH", 0, 0) + bytes(8) + bytes(4))
    assert len(body) == 64
    pdu = struct.pack(">BBH", 0xFA, msg_type, (5 << 11) | 56) + body
    return ADP_MC + src + struct.pack(">H", ETH_AVTP) + pdu


def control(iface, src, sid, log, deadline, parent):
    # AVTP only, and never our own transmitted frames: a raw socket otherwise
    # also receives a copy of every outgoing AAF PDU and drops the probes.
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_AVTP))
    s.setsockopt(263, 23, 1)            # SOL_PACKET, PACKET_IGNORE_OUTGOING
    s.bind((iface, ETH_AVTP))
    mreq = struct.pack("iHH8s", socket.if_nametoindex(iface), 0, 6, ADP_MC + b"\x00\x00")
    s.setsockopt(263, 1, mreq)
    idx, nxt = 0, 0.0
    while not stop.is_set() and time.monotonic() < deadline and os.getppid() == parent:
        if time.monotonic() >= nxt:
            s.send(adp(src, 0, idx))
            idx += 1
            nxt = time.monotonic() + 2.0
        r, _, _ = select.select([s], [], [], 0.2)
        if not r:
            continue
        fr = s.recv(2048)
        if len(fr) < 70 or struct.unpack(">H", fr[12:14])[0] != ETH_AVTP:
            continue
        p = fr[14:]
        if p[0] != 0xFC or (p[1] & 0x0F) != 0 or p[20:28] != TALKER_EID:
            continue
        seq = struct.unpack(">H", p[48:50])[0]
        body = (sid + p[12:20] + TALKER_EID + p[28:36] + p[36:38] + p[38:40] + DUT_MAC
                + struct.pack(">HHHHH", 1, seq, 0, 0, 0))
        rsp = struct.pack(">BBH", 0xFC, 1, 44) + body
        s.send(ADP_MC + src + struct.pack(">H", ETH_AVTP) + rsp)
        emit(log, dict(kind="probe-answer", listener=p[28:36].hex(), luid=struct.unpack(">H", p[38:40])[0],
                       seq=seq, stream_id=sid.hex()))
    s.send(adp(src, 1, idx))
    s.close()


def main():
    iface, seconds, out, ppm = sys.argv[1], float(sys.argv[2]), sys.argv[3], float(sys.argv[4])
    phc = sys.argv[5] if len(sys.argv) > 5 else None
    log = open(out, "w")
    src = bytes.fromhex(open(f"/sys/class/net/{iface}/address").read().strip().replace(":", ""))
    global TALKER_EID, MODEL_ID
    TALKER_EID = src[:3] + b"\xff\xfe" + src[3:4] + b"\xa4\x03"
    MODEL_ID = src[:3] + b"\xff\xfe" + src[3:4] + b"\x00\x00"
    sid = src + b"\xa4\x03"
    clk = time.CLOCK_REALTIME
    if phc:
        clk = ((~os.open(phc, os.O_RDONLY)) << 3) | 3
    signal.signal(signal.SIGINT, lambda *a: stop.set())
    signal.signal(signal.SIGTERM, lambda *a: stop.set())
    emit(log, dict(kind="start", iface_mac=src.hex(), stream_id=sid.hex(), talker=TALKER_EID.hex(),
                   dut_ppm=ppm, clock="phc" if phc else "realtime", seconds=seconds))
    pid = os.fork()
    if pid == 0:                        # control loop in its own process (no shared interpreter lock)
        signal.signal(signal.SIGINT, lambda *a: stop.set())
        signal.signal(signal.SIGTERM, lambda *a: stop.set())
        control(iface, src, sid, log, time.monotonic() + seconds + 15, os.getppid())
        log.close()
        os._exit(0)
    # one pattern period: lcm(6, 65536) frames, so PDU payloads tile exactly
    nfr = 196608
    words = []
    for n in range(nfr):
        base = n & 0xFFFF
        words.extend((((c + 1) << 16) | base) << 8 for c in range(CH))
    pattern = struct.pack(f">{len(words)}I", *words)
    del words
    gc.collect()
    gc.disable()
    try:                                # best effort: one CPU, raised priority (no RT class:
        os.sched_setaffinity(0, {3})    # a busy-spinning FIFO task would be RT-throttled)
        os.nice(-15)
        rt = True
    except OSError:
        rt = False
    emit(log, dict(kind="sched", pinned_nice=rt))
    late_log = []
    tx = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    tx.bind((iface, 0))
    hdr = bytearray(DUT_MAC + src + struct.pack(">H", ETH_AVTP) + bytes(24))
    hdr[14] = 0x02
    hdr[15] = 0x81                      # sv=1, version 0, mr=0, tv=1
    hdr[18:26] = sid
    hdr[30:34] = bytes((0x02, 0x50, 0x08, 0x20))  # INT32, nsr 48 kHz, 8 channels, 32 bit
    struct.pack_into(">H", hdr, 34, SPF * CH * 4)
    period = SPF * 1e9 / (RATE * (1.0 + ppm * 1e-6))
    t_start = time.clock_gettime_ns(clk) + 50_000_000
    t_stop = t_start + int(seconds * 1e9)
    n = 0
    late_hist = [0] * 8                 # <50us, <125, <250, <500, <1ms, <5ms, <25ms, >=25ms
    edges = [50_000, 125_000, 250_000, 500_000, 1_000_000, 5_000_000, 25_000_000]
    max_late = 0
    plen = len(pattern)
    while not stop.is_set():
        target = t_start + int(n * period)
        if target >= t_stop:
            break
        now = time.clock_gettime_ns(clk)
        while now < target:
            if target - now > 300_000:
                time.sleep((target - now - 200_000) / 1e9)
            now = time.clock_gettime_ns(clk)
        late = now - target
        max_late = max(max_late, late)
        i = 0
        while i < 7 and late >= edges[i]:
            i += 1
        late_hist[i] += 1
        if late >= 150_000 and len(late_log) < 5000:
            late_log.append((n, (n * SPF) & 0xFFFF, late))
        hdr[16] = n & 0xFF
        struct.pack_into(">I", hdr, 26, (target + PRES_NS) & 0xFFFFFFFF)
        off = (n * SPF * CH * 4) % plen
        tx.send(bytes(hdr) + pattern[off:off + SPF * CH * 4])
        n += 1
        if n % 80000 == 0:
            emit(log, dict(kind="progress", pdus=n, max_late_ns=max_late, hist=late_hist))
    stop.set()
    os.kill(pid, signal.SIGTERM)
    os.waitpid(pid, 0)
    emit(log, dict(kind="late-pdus", threshold_ns=150_000, entries=late_log))
    emit(log, dict(kind="end", pdus=n, frames=n * SPF, first_target_ns=t_start,
                   last_target_ns=t_start + int((n - 1) * period), max_late_ns=max_late,
                   late_hist_edges_ns=edges, late_hist=late_hist))
    log.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
