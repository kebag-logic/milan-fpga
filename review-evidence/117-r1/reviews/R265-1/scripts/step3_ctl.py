#!/usr/bin/env python3
"""Re-derive the controller-host (AECP/ACMP/ADP) claims of Step 3/4.

Usage: step3_ctl.py <bench-a202 dir>
Counter indices follow IEEE 1722.1-2021 Clause 7.4.42 counter tables as the
watcher records them in order: AVB_INTERFACE 0 LINK_UP, 1 LINK_DOWN,
5 GPTP_GM_CHANGED; STREAM_INPUT 0 MEDIA_LOCKED, 1 MEDIA_UNLOCKED,
2 STREAM_INTERRUPTED, 5 TIMESTAMP_UNCERTAIN, 6 TIMESTAMP_VALID, 11 FRAMES_RX;
STREAM_OUTPUT 0 STREAM_START, 1 STREAM_STOP, 3 TIMESTAMP_UNCERTAIN, 4 FRAMES_TX.
Times are seconds after the cycle's off command (same timebase as step3.py).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step3

DUT = "020000fffe000001"
PEER = "3cc0c60102030000"
SW = "3cc0c6fffefe0210"


def cnt(p, i):
    x = bytes.fromhex(p["payload"])
    return int.from_bytes(x[8 + 4 * i:12 + 4 * i], "big")


def main():
    base = sys.argv[1]
    for n in range(1, 7):
        cdir = os.path.join(base, "bench", f"cycle{n}")
        off, _ = step3.offsets(cdir)
        ps = step3.powerstrip(cdir)
        t0 = ps["T_OFF_CMD"] - off["ps"](ps["T_OFF_CMD"])
        W = [json.loads(l) for l in open(os.path.join(cdir, "pw1-watch.jsonl"))]
        for w in W:
            w["r"] = w["t"] - off["ctl"](w["t"]) - t0
        car = [(round(w["r"], 2), w["value"]) for w in W if w.get("type") == "carrier"]
        up = [r for r, v in car if v == 1 and r > 0][0]
        ok = lambda what, tgt: [w for w in W if w.get("type") == "poll" and w.get("what") == what
                                 and w.get("target") == tgt and w.get("status") == "SUCCESS"]
        print(f"===== cycle {n}: carrier {car}")
        for tgt, name in ((DUT, "DUT"), (PEER, "peer")):
            ai = ok("avb_info", tgt)
            post = [w for w in ai if w["r"] > up]
            pre = [w for w in ai if w["r"] < 0]
            f = post[0]
            gm0 = f["decoded"]["gm"]
            firstsw = next((w["r"] for w in post if w["decoded"]["gm"] == SW), None)
            asc_while_self = [round(w["r"], 2) for w in post if w["decoded"]["gm"] != SW and w["decoded"]["as_capable"]]
            ap = [w for w in ok("as_path", tgt) if w["r"] > up]
            ac = ok("avb_counters", tgt)
            gmc = [cnt(w, 5) for w in ac]
            lu = sorted({(cnt(w, 0), cnt(w, 1)) for w in ac})
            print(f"  {name}: first reachable AVB_INFO {f['r']:.2f} gm {gm0} asCapable {f['decoded']['as_capable']}; "
                  f"names switch at {firstsw if firstsw is None else round(firstsw, 2)}; asCapable while GM not switch at {asc_while_self[:4]}")
            print(f"        first reachable AS_PATH {ap[0]['r']:.2f} {ap[0]['decoded']['path']}; last {ap[-1]['decoded']['path']}; "
                  f"GPTP_GM_CHANGED {gmc[0]} -> {gmc[-1]} (+{gmc[-1] - gmc[0]}); (LINK_UP, LINK_DOWN) {lu}; pre-off all switch {all(w['decoded']['gm'] == SW for w in pre)}")
        adp = [w for w in W if w.get("type") == "adp"]
        pa = [w for w in adp if w["entity_id"] == PEER]
        da = [w for w in adp if w["entity_id"] == DUT]
        pa_post = [w for w in pa if w["r"] > up]
        print(f"  ADP peer after return: {[(round(w['r'], 2), w['gptp_gm'][-6:]) for w in pa_post[:4]]}; avail {pa[0]['available_index']} -> {pa[-1]['available_index']}")
        print(f"  ADP DUT after return: {[(round(w['r'], 2), w['gptp_gm'][-6:]) for w in da if w['r'] > up][:3]}; "
              f"DUT ADP naming itself: {sum(1 for w in da if w['gptp_gm'] == DUT)}")
        pin = ok("peer_in_counters", PEER)
        dout = ok("dut_out_counters", DUT)
        if pin:
            post = [w for w in pin if w["r"] > up]
            pre = [w for w in pin if w["r"] < 0]
            v = lambda w: {k: cnt(w, i) for k, i in (("LOCK", 0), ("UNLOCK", 1), ("INTR", 2), ("TSU", 5), ("RX", 11))}
            print(f"  peer IN last pre-off {v(pre[-1])}")
            print(f"  peer IN first post-return {post[0]['r']:.2f} {v(post[0])}")
            relock = next((w for w in post if cnt(w, 0) > cnt(post[0], 0) or (cnt(w, 0) >= 1 and cnt(w, 1) == 0)), None)
            locks = [(round(w["r"], 2), v(w)) for w in post if w["r"] < post[0]["r"] + 8]
            print("  peer IN post-return polls:", locks[:10])
            fl = [(round(w["r"], 2), w["peer_rx"]["flags"], w["peer_rx"]["conn_count"], w["peer_rx"]["talker"][-6:])
                  for w in W if w.get("type") == "acmp_state" and "peer_rx" in w]
            odd = [x for x in fl if x[1] != "0x0000"]
            talkers = sorted({(x[2], x[3]) for x in fl if x[0] > -28 and x[0] < 100})
            print(f"  ACMP flags != 0: {odd}; (conn_count, talker) seen in bound window: {talkers}")
            vo = lambda w: {k: cnt(w, i) for k, i in (("START", 0), ("STOP", 1), ("TSU", 3), ("FTX", 4))}
            dpre = [w for w in dout if w["r"] < 1]
            dpost = [w for w in dout if w["r"] > up]
            print(f"  DUT OUT last pre-loss {vo(dpre[-1])}; first post-return {vo(dpost[0])}; "
                  f"first with START+1: {next(((round(w['r'], 2), vo(w)) for w in dpost if cnt(w, 0) > cnt(dpost[0], 0)), None)}")
        for w in W:
            if w.get("type") in ("bind", "unbind", "unbound", "interrupted", "done"):
                print(f"  {w['type']} at {w['r']:.2f}")


if __name__ == "__main__":
    main()
