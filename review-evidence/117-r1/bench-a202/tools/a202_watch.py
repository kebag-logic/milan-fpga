#!/usr/bin/env python3
"""Controller-host watcher for one GM loss/return cycle (issue 117, A202, step 3).

Runs under sudo on the controller host, next to avdecc_ro.py (A200, unchanged)
in /tmp/a202. It prints one JSON object per line, stamped with the host's NTP
time:

  carrier   every change of the AVB port's carrier (sampled every 0.1 s); the
            controller host sits on switch port 8, so this is the switch's
            own link edge
  adp       every ADP advertisement heard (entity, gptp_grandmaster_id,
            available_index), so each entity's published GM is timed
  poll      every <period_s>, while the carrier is up: GET_AVB_INFO and
            GET_AS_PATH on the DUT and the reference peer, GET_COUNTERS on
            both AVB_INTERFACE 0; with --bind also the peer's STREAM_INPUT 8
            counters, the DUT's STREAM_OUTPUT 1 counters, and the ACMP
            listener and talker state of the bound pair

--bind binds exactly one pair, the reference peer's STREAM_INPUT 8 (primary
CRF input; its clock source is not touched) to the DUT's STREAM_OUTPUT 1 (CRF
output), as A200's crf_bind_window.py did. It refuses unless the input reads
unbound first. It always unbinds: at the end of the window, on SIGTERM/SIGINT
and on any exception (signals only set a stop flag), retrying every 2 s until the input reads unbound or
<unbind_deadline_s> has passed (the switch may still be booting).

usage: a202_watch.py <iface> <duration_s> <period_s> [--bind] [--unbind-deadline <s>]
"""
import signal
import struct
import sys
import time

sys.path.insert(0, "/tmp/a202")
import avdecc_ro as ro  # noqa: E402

PEER = bytes.fromhex("3cc0c60102030000")
PEER_MAC = bytes.fromhex("3cc0c6010203")
PEER_IN = 8
DUT = bytes.fromhex("020000fffe000001")
DUT_MAC = bytes.fromhex("020000000001")
DUT_OUT = 1
ZERO = b"\x00" * 8
CONNECT_RX, DISCONNECT_RX, GET_TX_STATE, GET_RX_STATE = 6, 8, 4, 10
AECP_TIMEOUT = 0.5


STOP = []


def on_signal(signum, _frame):
    # a flag, not an exception: sudo and timeout both relay SIGTERM, and a
    # repeated signal must never cut the unbind retries short
    if not STOP:
        STOP.append(signum)


class Carrier:
    def __init__(self, iface):
        self.path = f"/sys/class/net/{iface}/carrier"
        self.value = None

    def read(self):
        try:
            with open(self.path) as f:
                v = int(f.read().strip())
        except OSError:
            v = 0
        if v != self.value:
            ro.emit(dict(type="carrier", value=v, prev=self.value))
            self.value = v
        return v


def acmp_any(a, mt, talker, tuid, listener, luid, timeout=3.0):
    """ACMP command, control_data_length 44 (CONNECT_RX/DISCONNECT_RX are used here only)."""
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
        log_adp(fr)
    return dict(status="TIMEOUT")


def log_adp(fr):
    e = ro.parse_adp(fr)
    if e:
        ro.emit(dict(type="adp", **e))


def counters(pl):
    b = bytes.fromhex(pl)
    if len(b) < 136:
        return {}
    valid = struct.unpack(">I", b[4:8])[0]
    vals = struct.unpack(">32I", b[8:136])
    return dict(valid=f"{valid:#010x}", c={i: vals[i] for i in range(32) if valid >> i & 1})


def aem(a, tgt, mac, cmd, payload, tag, decoder=None):
    r = a.aem(tgt, mac, cmd, payload, timeout=AECP_TIMEOUT, on_other=log_adp)
    if r.get("status") == "SUCCESS" and decoder is not None:
        r["decoded"] = decoder(r["payload"])
    r.update(type="poll", what=tag, target=tgt.hex())
    ro.emit(r)
    return r


def rx_state(a, tag):
    rx = a.acmp(GET_RX_STATE, ZERO, 0, PEER, PEER_IN, timeout=1.0)
    ro.emit(dict(type="acmp_state", tag=tag, peer_rx=rx))
    return rx


def unbound(rx):
    return rx.get("status") == 0 and rx.get("conn_count") == 0 and rx.get("talker") == "0" * 16


def poll_round(a, car, bind):
    for tgt, mac in ((DUT, DUT_MAC), (PEER, PEER_MAC)):
        if not car.read():
            return
        aem(a, tgt, mac, 0x0027, struct.pack(">HH", 0x0009, 0), "avb_info", ro.decode_avb_info)
        if not car.read():
            return
        aem(a, tgt, mac, 0x0028, struct.pack(">HH", 0, 0), "as_path", ro.decode_as_path)
        if not car.read():
            return
        aem(a, tgt, mac, 0x0029, struct.pack(">HH", 0x0009, 0), "avb_counters", counters)
    if bind and car.read():
        aem(a, PEER, PEER_MAC, 0x0029, struct.pack(">HH", 0x0005, PEER_IN), "peer_in_counters", counters)
        aem(a, DUT, DUT_MAC, 0x0029, struct.pack(">HH", 0x0006, DUT_OUT), "dut_out_counters", counters)
        rx_state(a, "poll")
        tx = a.acmp(GET_TX_STATE, DUT, DUT_OUT, ZERO, 0, timeout=1.0)
        ro.emit(dict(type="acmp_state", tag="poll", dut_tx=tx))


def main():
    iface = sys.argv[1]
    duration, period = float(sys.argv[2]), float(sys.argv[3])
    bind = "--bind" in sys.argv
    deadline_s = float(sys.argv[sys.argv.index("--unbind-deadline") + 1]) if "--unbind-deadline" in sys.argv else 120.0
    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    a = ro.Aecp(iface)
    car = Carrier(iface)
    ro.emit(dict(type="start", argv=sys.argv[1:], controller_eid=a.ceid.hex()))
    bound = False
    rc = 0
    try:
        car.read()
        if bind:
            rx = rx_state(a, "before")
            if not unbound(rx):
                ro.emit(dict(type="refused", reason="listener input not unbound before the window"))
                bind = False
                rc = 3
            else:
                r = acmp_any(a, CONNECT_RX, DUT, DUT_OUT, PEER, PEER_IN)
                bound = True
                ro.emit(dict(type="bind", response=r))
        end = time.monotonic() + duration
        nxt = time.monotonic()
        while time.monotonic() < end and not STOP:
            if car.read():
                poll_round(a, car, bind)
            nxt += period
            # between rounds: sample the carrier every 0.1 s and log ADP heard meanwhile
            while time.monotonic() < min(nxt, end) and not STOP:
                for fr in ro.frames(a.sock, min(time.monotonic() + 0.1, nxt, end)):
                    log_adp(fr)
                car.read()
            if nxt < time.monotonic():
                nxt = time.monotonic()
        if STOP:
            ro.emit(dict(type="interrupted", reason=f"signal {STOP[0]}"))
    finally:
        if bound:
            t_stop = time.monotonic() + deadline_s
            attempt = 0
            while True:
                if car.read():
                    r = acmp_any(a, DISCONNECT_RX, DUT, DUT_OUT, PEER, PEER_IN)
                    ro.emit(dict(type="unbind", attempt=attempt, response=r))
                    rx = rx_state(a, f"after-unbind-{attempt}")
                    if unbound(rx):
                        ro.emit(dict(type="unbound", attempt=attempt))
                        break
                attempt += 1
                if time.monotonic() > t_stop:
                    ro.emit(dict(type="unbind_failed", attempts=attempt))
                    rc = 4
                    break
                time.sleep(2.0)
            aem(a, PEER, PEER_MAC, 0x0029, struct.pack(">HH", 0x0005, PEER_IN), "peer_in_counters_final", counters)
    ro.emit(dict(type="done", rc=rc))
    return rc


if __name__ == "__main__":
    sys.exit(main())
