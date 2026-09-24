#!/usr/bin/env python3
"""Bounded CRF bind window on the reference peer (issue 117, A200, step 4).

Binds exactly one pair: the reference peer's STREAM_INPUT 8 (its primary CRF
media-clock input, clock source NOT selected) to the DUT's STREAM_OUTPUT 1
(its CRF media-clock output), so the DUT's talker is licensed and its AVTP
frames, with their tu bit, appear on the tapped link. It then always unbinds,
on normal exit, on SIGTERM/SIGINT and on any exception, and re-reads the
listener state until it is unbound (three attempts).

It refuses to bind unless the listener input reads unbound first.

usage: crf_bind_window.py <iface> <pre_s> <window_s> <post_s>
"""
import signal
import struct
import sys
import time

sys.path.insert(0, "/tmp/a200")
import avdecc_ro as ro  # noqa: E402

PEER = bytes.fromhex("3cc0c60102030000")
PEER_MAC = bytes.fromhex("3cc0c6010203")
PEER_IN = 8
DUT = bytes.fromhex("020000fffe000001")
DUT_MAC = bytes.fromhex("020000000001")
DUT_OUT = 1
ZERO = b"\x00" * 8
CONNECT_RX, DISCONNECT_RX, GET_TX_STATE, GET_RX_STATE = 6, 8, 4, 10


class Stop(Exception):
    pass


def on_signal(signum, _frame):
    raise Stop(f"signal {signum}")


def acmp_any(a, mt, talker, tuid, listener, luid, timeout=3.0):
    """ACMP command with control_data_length 44 (state-changing types allowed here only)."""
    a.seq = (a.seq + 1) & 0xFFFF
    seq = a.seq
    body = (a.ceid + talker + listener + struct.pack(">HH", tuid, luid) + b"\x00" * 6
            + struct.pack(">HHHHH", 0, seq, 0, 0, 0))
    pdu = struct.pack(">BBH", 0xFC, mt, 44) + b"\x00" * 8 + body
    a.sock.send(ro.eth(ro.AVDECC_MC, a.src, pdu))
    for fr in ro.frames(a.sock, time.monotonic() + timeout):
        p = fr[14:]
        if p[0] == 0xFC and (p[1] & 0x0F) == mt + 1 and struct.unpack(">H", p[48:50])[0] == seq \
                and p[12:20] == a.ceid:
            return dict(status=p[2] >> 3, stream_id=p[4:12].hex(), talker=p[20:28].hex(),
                        listener=p[28:36].hex(), talker_uid=struct.unpack(">H", p[36:38])[0],
                        listener_uid=struct.unpack(">H", p[38:40])[0], dmac=p[40:46].hex(),
                        conn_count=struct.unpack(">H", p[46:48])[0],
                        flags=f"{struct.unpack('>H', p[50:52])[0]:#06x}",
                        vlan=struct.unpack(">H", p[52:54])[0])
    return dict(status="TIMEOUT")


def state(a, tag):
    rx = a.acmp(GET_RX_STATE, ZERO, 0, PEER, PEER_IN)
    tx = a.acmp(GET_TX_STATE, DUT, DUT_OUT, ZERO, 0)
    ro.emit(dict(type="state", tag=tag, peer_rx=rx, dut_tx=tx))
    return rx, tx


def counters(a, tag):
    r = a.aem(PEER, PEER_MAC, 0x0029, struct.pack(">HH", 0x0005, PEER_IN))
    ro.emit(dict(type="peer_counters", tag=tag, **r))


def main():
    iface = sys.argv[1]
    pre, window, post = (float(x) for x in sys.argv[2:5])
    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    a = ro.Aecp(iface)
    ro.emit(dict(type="start", argv=sys.argv[1:], controller_eid=a.ceid.hex()))
    bound = False
    try:
        rx, _ = state(a, "before")
        if rx.get("status") != 0 or rx.get("conn_count") != 0 or rx.get("talker") != "0" * 16:
            ro.emit(dict(type="refused", reason="listener input not unbound before the window"))
            return 3
        counters(a, "before")
        time.sleep(pre)
        r = acmp_any(a, CONNECT_RX, DUT, DUT_OUT, PEER, PEER_IN)
        bound = True
        ro.emit(dict(type="bind", response=r))
        end = time.monotonic() + window
        n = 0
        while time.monotonic() < end:
            state(a, f"bound+{n * 5}s")
            if n % 3 == 0:
                counters(a, f"bound+{n * 5}s")
            n += 1
            time.sleep(max(0.0, min(5.0, end - time.monotonic())))
    except Stop as e:
        ro.emit(dict(type="interrupted", reason=str(e)))
    finally:
        if bound:
            for attempt in range(3):
                r = acmp_any(a, DISCONNECT_RX, DUT, DUT_OUT, PEER, PEER_IN)
                ro.emit(dict(type="unbind", attempt=attempt, response=r))
                rx, _ = state(a, f"after-unbind-{attempt}")
                if rx.get("status") == 0 and rx.get("conn_count") == 0 and rx.get("talker") == "0" * 16:
                    break
                time.sleep(1.0)
    counters(a, "after-unbind")
    t_end = time.monotonic() + post
    while time.monotonic() < t_end:
        time.sleep(min(5.0, max(0.0, t_end - time.monotonic())))
        state(a, "post")
    ro.emit(dict(type="done"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
