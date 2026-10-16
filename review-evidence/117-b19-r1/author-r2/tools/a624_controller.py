"""Bounded bench controller actions for lane B19; the caller holds the bench lock.

Lane B1's a438_controller.py with the lane B19 stream set: the as-found bindings
are the DUT's AAF talker to the peer's input 0, the peer's AAF talker to the
DUT's input 0 (the music bindings) and the DUT's CRF talker (output 1) to the
peer's CRF input 8, which is the peer's selected media clock source.

modes:
  census                 read-only state of both entities (lane B1's census)
  snapshot               one poll round (GET_AVB_INFO, GET_COUNTERS, ACMP states)
  watch <s> <pairs>      carrier every 0.1 s, a snapshot each second while the
                         carrier is up, ADP throughout; <pairs> is "all" or
                         "music" (the CRF pair not polled while it is unbound)
  crf <bind|unbind>      the one CRF pair (DUT output 1 -> peer input 8) only;
                         bind refuses unless the input reads unbound, unbind
                         retries until it reads unbound; then GET_RX_STATE
No clock source, stream format, map or register is written. AEM REBOOT is never sent.
"""
import sys, struct, json, time, threading
from pathlib import Path
import avdecc_ro as ro
D = bytes.fromhex("020000fffe000001"); DM = bytes.fromhex("020000000001")
P = bytes.fromhex("3cc0c60102030000"); PM = bytes.fromhex("3cc0c6010203")
Z = bytes(8)
MUSIC = [(D, 0, P, 0), (P, 0, D, 0)]
CRF = (D, 1, P, 8)


def emit(role, what, r):
    ro.emit(dict(role=role, what=what, response=r))


def aem(a, role, cmd, payload, what):
    target, mac = (D, DM) if role == "dut" else (P, PM)
    r = a.aem(target, mac, cmd, payload, timeout=.8)
    if cmd == 0x29 and r.get("status") == "SUCCESS":
        b = bytes.fromhex(r["payload"]); valid = int.from_bytes(b[4:8], "big"); v = struct.unpack(">32I", b[8:136])
        r["counters"] = {str(i): v[i] for i in range(32) if valid >> i & 1}; r["valid"] = hex(valid)
    if cmd == 0x27 and r.get("status") == "SUCCESS":
        r["decoded"] = ro.decode_avb_info(r["payload"])
    emit(role, what, r); return r


def state(a, role, kind, i):
    e = D if role == "dut" else P
    r = a.acmp(10, Z, 0, e, i, timeout=.8) if kind == 5 else a.acmp(4, e, i, Z, 0, timeout=.8)
    emit(role, f"state-{kind}-{i}", r); return r


def census(a):
    for role, ni, no in [("dut", 2, 2), ("peer", 10, 4)]:
        for i in range(ni): state(a, role, 5, i)
        for i in range(no): state(a, role, 6, i)
        for cmd, payload, what in [(0x17, "00240000", "clock"), (7, "00000000", "config"), (0x15, "00020000", "sample-rate"), (0x27, "00090000", "avb")]:
            aem(a, role, cmd, bytes.fromhex(payload), what)
        for kind, inds in [(9, [0]), (5, range(ni)), (6, range(no)), (0x24, [0])]:
            for i in inds: aem(a, role, 0x29, struct.pack(">HH", kind, i), f"counter-{kind}-{i}")


def pair_state(a, t, ti, l, li):
    r = a.acmp(10, Z, 0, l, li, timeout=.8); emit("dut" if l == D else "peer", f"state-5-{li}", r); return r


def snapshot(a, pairs):
    for role in ["dut", "peer"]:
        aem(a, role, 0x27, bytes.fromhex("00090000"), "avb")
        for kind, i in [(9, 0), (5, 0), (6, 0), (6, 1), (0x24, 0)] if role == "dut" else [(9, 0), (5, 0), (5, 8), (6, 0), (0x24, 0)]:
            aem(a, role, 0x29, struct.pack(">HH", kind, i), f"counter-{kind}-{i}")
    for pair in pairs: pair_state(a, *pair)


def crf(a, op):
    t, ti, l, li = CRF
    if op == "bind":
        r = pair_state(a, *CRF); assert r.get("status") == 0 and r.get("conn_count") == 0, r
        r = a.acmp(6, t, ti, l, li, timeout=4); emit("peer", "acmp-6", r); assert r.get("status") == 0, r
    else:
        for attempt in range(3):
            r = pair_state(a, *CRF)
            if r.get("status") == 0 and r.get("conn_count") == 0: break
            r = a.acmp(8, t, ti, l, li, timeout=4); emit("peer", "acmp-8", r)
    time.sleep(.5)
    r = pair_state(a, *CRF)
    assert r.get("status") == 0 and r.get("conn_count") == (1 if op == "bind" else 0), r


def main():
    a = ro.Aecp(sys.argv[1]); mode = sys.argv[2]
    try:
        if mode == "census": census(a)
        elif mode == "snapshot": snapshot(a, MUSIC + [CRF])
        elif mode == "crf": crf(a, sys.argv[3])
        elif mode == "watch":
            end = time.monotonic() + float(sys.argv[3]); done = threading.Event()
            pairs = MUSIC + [CRF] if sys.argv[4] == "all" else MUSIC
            def carrier_watch():
                prev = None
                while time.monotonic() < end and not done.is_set():
                    value = int(Path("/sys/class/net/" + sys.argv[1] + "/carrier").read_text())
                    if value != prev: ro.emit(dict(type="carrier", value=value)); prev = value
                    done.wait(.1)
            thread = threading.Thread(target=carrier_watch); thread.start()
            try:
                while time.monotonic() < end:
                    t = time.monotonic()
                    carrier = int(Path("/sys/class/net/" + sys.argv[1] + "/carrier").read_text())
                    if carrier: snapshot(a, pairs)
                    while time.monotonic() < min(t + 1, end):
                        for fr in ro.frames(a.sock, min(t + 1, end, time.monotonic() + .1)):
                            e = ro.parse_adp(fr)
                            if e: ro.emit(dict(type="adp", **e))
            finally: done.set(); thread.join()
        else: raise SystemExit("unknown mode " + mode)
    finally: a.sock.close()


if __name__ == "__main__": main()
