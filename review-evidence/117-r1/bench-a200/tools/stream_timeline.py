#!/usr/bin/env python3
"""Stream/SRP/ACMP event timeline from a tap capture (issue 117, A200).

usage: stream_timeline.py <pcap>
Prints CRF/AAF emission start/stop (a gap over 10 ms ends a burst), ACMP
bind/probe traffic, and MSRP TalkerAdvertise/Listener declarations other than
steady-state refreshes, in tap-hardware-time order.
"""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wire_summary as ws  # noqa: E402

EV = ["New", "JoinIn", "In", "JoinMt", "Mt", "Lv"]
LD = ["Ignore", "AskingFailed", "Ready", "ReadyFailed"]
ACMPN = {0: "CONNECT_TX(probe)", 1: "CONNECT_TX_RESP", 6: "CONNECT_RX(bind)", 7: "CONNECT_RX_RESP",
         8: "DISCONNECT_RX(unbind)", 9: "DISCONNECT_RX_RESP"}


def msrp_evs(fr):
    p = fr[14:]
    i, out = 1, []
    while i + 4 <= len(p):
        at, al = p[i], p[i + 1]
        if at == 0:
            break
        ll = struct.unpack(">H", p[i + 2:i + 4])[0]
        body = p[i + 4:i + 4 + ll]
        j = 0
        while j + 2 <= len(body):
            vh = struct.unpack(">H", body[j:j + 2])[0]
            if vh == 0:
                break
            nv, la = vh & 0x1FFF, vh >> 13
            j += 2 + al
            nb = (nv + 2) // 3
            ev = []
            for b in body[j:j + nb]:
                ev += [EV[b // 36], EV[(b // 6) % 6], EV[b % 6]]
            j += nb
            ev = ev[:nv] or ["?"]
            d = ""
            if at == 3:
                n4 = (nv + 3) // 4
                ld = []
                for b in body[j:j + n4]:
                    ld += [LD[(b >> 6) & 3], LD[(b >> 4) & 3], LD[(b >> 2) & 3], LD[b & 3]]
                j += n4
                d = "/" + (ld[0] if ld else "?")
            name = {1: "TalkerAdvertise", 2: "TalkerFailed", 3: "Listener", 4: "Domain"}.get(at, str(at))
            out.append((name, ("LeaveAll " if la else "") + ev[0] + d))
        i += 4 + ll
    return out


def main():
    recs = []
    for raw in ws.records(sys.argv[1]):
        d = ws.decode(raw)
        d["frame"] = raw["frame"]
        recs.append(d)
    recs.sort(key=lambda d: d["tap_ns"])
    t0 = recs[0]["tap_ns"]
    print("t_tap_s     host_utc_s      port event")
    streaming, last = False, None
    for r in recs:
        t, h = (r["tap_ns"] - t0) / 1e9, r["host_ns"] / 1e9
        if r["kind"] in ("CRF", "AAF"):
            if not streaming:
                print(f"{t:10.6f} {h:.3f} p3 {r['kind']} emission starts (seq {r['avtp']['seq']}, tu={r['avtp']['tu']})")
                streaming = True
            last = r
            continue
        if streaming and r["tap_ns"] - last["tap_ns"] > 10e6:
            print(f"{(last['tap_ns'] - t0) / 1e9:10.6f} {last['host_ns'] / 1e9:.3f} p3 {last['kind']} "
                  f"emission stops (seq {last['avtp']['seq']})")
            streaming = False
        if r["kind"] == "ACMP" and r["acmp"]["msg"] in ACMPN:
            print(f"{t:10.6f} {h:.3f} p{r['port']} ACMP {ACMPN[r['acmp']['msg']]} status={r['acmp']['status']}")
        if r["kind"] == "MSRP":
            for a, e in msrp_evs(r["frame"]):
                steady = e.startswith(("JoinMt", "JoinIn", "In", "Mt")) and "LeaveAll" not in e
                if a in ("TalkerAdvertise", "Listener") and not steady or "LeaveAll" in e:
                    print(f"{t:10.6f} {h:.3f} p{r['port']} MSRP {a} {e}")
    if streaming:
        print(f"{(last['tap_ns'] - t0) / 1e9:10.6f} {last['host_ns'] / 1e9:.3f} p3 {last['kind']} "
              f"last frame in capture (seq {last['avtp']['seq']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
