#!/usr/bin/env python3
"""DUT PHC against grandmaster time on the tap's hardware clock (issue 387, A249). Offline.

Input: a tap capture of the DUT link (wire_summary.py decoder, unchanged, imported from this
directory). Port 2 carries the far end (the bench AVB switch, which is the grandmaster) toward
the DUT; port 3 carries the DUT's frames.

Grandmaster samples. Each switch Sync (two-step) passes the tap at tap time T_s; its Follow_Up
carries preciseOriginTimestamp POT and a correctionField. G(T) is grandmaster time at the
switch's timestamp plane, interpolated linearly between the two Syncs that bracket T:
G(T_s) = POT + correction(Sync) + correction(Follow_Up).

DUT samples, two per second:
  o2 = t2 - G(T_q): t2 is the DUT's requestReceiptTimestamp (its Pdelay_Resp) for the switch's
       Pdelay_Req that passed the tap at T_q (matched by sequenceId and requesting port).
  o3 = t3 - G(T_r): t3 is the DUT's responseOriginTimestamp (its Pdelay_Resp_Follow_Up plus that
       message's correctionField) for the Pdelay_Resp that passed the tap at T_r.
With a = switch-to-tap and b = tap-to-DUT one-way delays (b both ways):
  DUT - GM offset = o2 - (a + b) = o3 - a + b, so o2 - o3 = 2b, and with a + b = the measured
  mean link delay d, offset = o2 - d. Only the variation of o2/o3 is free of path assumptions;
  the absolute value assumes a symmetric link and equal tap port latencies, as gPTP itself does.

A PHC step (20 us at link-up, above 100 us once locked) or a 100 us slew would show as a jump
or an excursion of o2/o3 many orders above their jitter. Every consecutive-sample jump above
--jump-ns (default 1000 ns) is listed.

Rates: least-squares slopes of G, t3 and the offsets against tap time (tap oscillator is the
reference; only differences between them are meaningful to the ppb).

usage: a249_gptp_wire.py <tap.pcap> [--pdelay-ns 385] [--jump-ns 1000] [--json out.json]
"""
import json
import os
import statistics as st
import sys
from bisect import bisect_right
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wire_summary as ws  # noqa: E402


def lsq(xs, ys):
    mx, my = st.fmean(xs), st.fmean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    return b, my - b * mx


def pct(v, p):
    s = sorted(v)
    k = (len(s) - 1) * p
    lo = int(k)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def stats(v):
    return (f"n={len(v)} median={st.median(v):.1f} mean={st.fmean(v):.1f} stdev={st.pstdev(v):.1f} "
            f"p1={pct(v, 0.01):.1f} p99={pct(v, 0.99):.1f} min={min(v):.1f} max={max(v):.1f} "
            f"p2p={max(v) - min(v):.1f}")


def main():
    a = sys.argv[1:]
    path = a[0]
    pdelay = float(a[a.index("--pdelay-ns") + 1]) if "--pdelay-ns" in a else 385.0
    jump = float(a[a.index("--jump-ns") + 1]) if "--jump-ns" in a else 1000.0
    js = a[a.index("--json") + 1] if "--json" in a else None
    recs = sorted((ws.decode(r) for r in ws.records(path)), key=lambda d: d["tap_ns"])
    t0 = recs[0]["tap_ns"]
    span = (recs[-1]["tap_ns"] - t0) / 1e9
    print(f"file: {os.path.basename(path)}  tapped records {len(recs)}  host-generated excluded "
          f"{ws.HOST_RECORDS[0]}  tap span {span:.3f} s")

    # tap time -> capture-server UTC: LSQ through per-5 s minima of (host - tap), as A237 did
    buckets = defaultdict(list)
    for r in recs:
        buckets[(r["tap_ns"] - t0) // 5_000_000_000].append((r["tap_ns"], r["host_ns"] - r["tap_ns"]))
    mins = [min(v, key=lambda x: x[1]) for v in buckets.values()]
    sl, ic = lsq([m[0] - t0 for m in mins], [m[1] for m in mins])

    def utc(tap_ns):
        from datetime import datetime, timezone
        h = tap_ns + ic + sl * (tap_ns - t0)
        return datetime.fromtimestamp(h / 1e9, timezone.utc).strftime("%H:%M:%S.%f") + "Z"

    print(f"tap->UTC fit over {len(mins)} 5 s minima: slope {sl * 1e6:+.3f} ppm; first record {utc(t0)}")

    ptp = [r for r in recs if "ptp" in r]
    kinds = Counter((r["port"], r["src"], r["kind"]) for r in recs)
    print("\n== frames by (tap port, source, kind)")
    for k, n in sorted(kinds.items()):
        print(f"  port {k[0]} {k[1]} {k[2]:28s} {n}")

    # grandmaster samples
    syncs = {(r["ptp"]["src_port_id"], r["ptp"]["seq"]): r for r in ptp if r["port"] == 2 and r["ptp"]["mt"] == 0}
    fups = {(r["ptp"]["src_port_id"], r["ptp"]["seq"]): r for r in ptp if r["port"] == 2 and r["ptp"]["mt"] == 8}
    gm = []
    for k, s in syncs.items():
        f = fups.get(k)
        if f is None:
            continue
        gm.append((s["tap_ns"], f["ptp"]["body_ts"] + s["ptp"]["corr_ns"] + f["ptp"]["corr_ns"]))
    gm.sort()
    print(f"\n== grandmaster samples: Syncs {len(syncs)}, Follow_Ups {len(fups)}, matched {len(gm)}")
    sync_seq = sorted(k[1] for k in syncs)
    gaps = sum(((b - a) & 0xFFFF) != 1 for a, b in zip(sync_seq, sync_seq[1:]))
    iv = ws.intervals_ms([g[0] for g in gm])
    print(f"   Sync intervals ms: {ws.fmt_stats(iv)}; sequence gaps {gaps}")
    corr = Counter(round(f["ptp"]["corr_ns"], 3) for f in fups.values())
    print(f"   Follow_Up correctionField ns values: {dict(corr.most_common(5))}")
    csro = Counter(f["ptp"].get("csro") for f in fups.values())
    tbi = Counter(f["ptp"].get("gm_time_base") for f in fups.values())
    print(f"   Follow_Up cumulativeScaledRateOffset {dict(csro)}; gmTimeBaseIndicator {dict(tbi)}")
    ann = Counter((r["ptp"].get("gm_id"), r["ptp"].get("gm_prio1"), r["ptp"].get("steps_removed"))
                  for r in ptp if r["ptp"]["mt"] == 0xB)
    print(f"   Announce (port, GM id, priority1, stepsRemoved) counts: "
          f"{ {(k[0], k[1], k[2]): n for k, n in ann.items()} } by port "
          f"{dict(Counter(r['port'] for r in ptp if r['ptp']['mt'] == 0xB))}")
    gx = [g[0] for g in gm]
    g_rate, _ = lsq([(x - gx[0]) for x in gx], [g[1] - gm[0][1] for g in gm])
    g_res = [(g[1] - gm[0][1]) - g_rate * (g[0] - gx[0]) for g in gm]
    print(f"   GM time per tap ns: {g_rate:.12f} ({(g_rate - 1) * 1e9:+.3f} ppb vs the tap oscillator); "
          f"residual ns: min {min(g_res):+.1f} max {max(g_res):+.1f} stdev {st.pstdev(g_res):.1f}")

    def G(t):
        i = bisect_right(gx, t)
        if i == 0 or i >= len(gx):
            return None
        (x0, y0), (x1, y1) = gm[i - 1], gm[i]
        if x1 - x0 > 400_000_000:  # do not bridge a missing-Sync hole wider than 0.4 s
            return None
        return y0 + (y1 - y0) * (t - x0) / (x1 - x0)

    # DUT samples
    reqs = {(r["ptp"]["src_port_id"], r["ptp"]["seq"]): r for r in ptp if r["port"] == 2 and r["ptp"]["mt"] == 2}
    resp = {(r["ptp"]["req_port_id"], r["ptp"]["seq"]): r for r in ptp if r["port"] == 3 and r["ptp"]["mt"] == 3}
    rfu = {(r["ptp"]["req_port_id"], r["ptp"]["seq"]): r for r in ptp if r["port"] == 3 and r["ptp"]["mt"] == 0xA}
    o2, o3, rows = [], [], []
    for k, q in sorted(reqs.items(), key=lambda kv: kv[1]["tap_ns"]):
        rp, fu = resp.get(k), rfu.get(k)
        if rp is None or fu is None:
            continue
        g2, g3 = G(q["tap_ns"]), G(rp["tap_ns"])
        if g2 is None or g3 is None:
            continue
        t2 = rp["ptp"]["body_ts"] + rp["ptp"]["corr_ns"]
        t3 = fu["ptp"]["body_ts"] + fu["ptp"]["corr_ns"]
        a2, a3 = t2 - g2, t3 - g3
        o2.append(a2)
        o3.append(a3)
        rows.append(dict(seq=k[1], tq=q["tap_ns"], tr=rp["tap_ns"], o2=a2, o3=a3, t3=t3))
    print(f"\n== DUT samples: switch Pdelay_Req {len(reqs)}, DUT Pdelay_Resp {len(resp)}, "
          f"Resp_Follow_Up {len(rfu)}, usable {len(rows)}")
    if not rows:
        return 1
    tsec = [(r["tq"] - t0) / 1e9 for r in rows]
    print(f"   span {tsec[0]:.3f} to {tsec[-1]:.3f} s tap ({utc(rows[0]['tq'])} to {utc(rows[-1]['tq'])})")
    print(f"   o2 = t2 - G(T_req) ns: {stats(o2)}")
    print(f"   o3 = t3 - G(T_resp) ns: {stats(o3)}")
    b2 = [x - y for x, y in zip(o2, o3)]
    print(f"   o2 - o3 = 2 x tap-to-DUT delay ns: {stats(b2)}")
    off = [x - pdelay for x in o2]
    print(f"   offset estimate o2 - d (d = {pdelay:.0f} ns, the DUT's published peer delay) ns: {stats(off)}")
    for name, v in (("o2", o2), ("o3", o3)):
        d = [y - x for x, y in zip(v, v[1:])]
        big = [(round(tsec[i + 1], 3), utc(rows[i + 1]["tq"]), round(d[i], 1)) for i in range(len(d)) if abs(d[i]) > jump]
        print(f"   consecutive {name} change ns: {stats(d)}; |change| > {jump:.0f} ns: {len(big)} {big[:20]}")
        dev = [x - st.median(v) for x in v]
        print(f"   {name} deviation from its median ns: max |dev| {max(abs(x) for x in dev):.1f}")
    for name, v in (("o2", o2), ("o3", o3)):
        rate, _ = lsq(tsec, v)
        print(f"   {name} drift over the span: {rate:+.3f} ns/s = {rate:+.3f} ppb (DUT minus GM frequency)")
    t3x = [r["tr"] - rows[0]["tr"] for r in rows]
    d_rate, _ = lsq(t3x, [r["t3"] - rows[0]["t3"] for r in rows])
    print(f"   DUT PHC per tap ns: {d_rate:.12f} ({(d_rate - 1) * 1e9:+.3f} ppb vs the tap oscillator); "
          f"DUT minus GM {(d_rate - g_rate) * 1e9:+.3f} ppb")
    print("   per-60 s windows (tap s from first record): o2 median, o2 min..max, o2 stdev, drift ppb")
    w = defaultdict(list)
    for s, x in zip(tsec, o2):
        w[int(s // 60)].append((s, x))
    for k in sorted(w):
        v = [x for _, x in w[k]]
        rate = lsq([s for s, _ in w[k]], v)[0] if len(v) > 2 else float("nan")
        print(f"     [{k * 60:5d},{k * 60 + 60:5d}) n={len(v):3d} median {st.median(v):8.1f} "
              f"range {min(v):8.1f}..{max(v):8.1f} stdev {st.pstdev(v):6.1f} drift {rate:+7.3f}")
    # DUT as requester: the switch's answers
    dreq = {(r["ptp"]["src_port_id"], r["ptp"]["seq"]): r for r in ptp if r["port"] == 3 and r["ptp"]["mt"] == 2}
    sresp = {(r["ptp"]["req_port_id"], r["ptp"]["seq"]): r for r in ptp if r["port"] == 2 and r["ptp"]["mt"] == 3}
    sfu = {(r["ptp"]["req_port_id"], r["ptp"]["seq"]): r for r in ptp if r["port"] == 2 and r["ptp"]["mt"] == 0xA}
    done = sum(1 for k in dreq if k in sresp and k in sfu)
    print(f"\n== DUT as Pdelay requester: requests {len(dreq)}, answered with Resp+Resp_FU {done}")
    di = ws.intervals_ms(sorted(r["tap_ns"] for r in dreq.values()))
    print(f"   DUT Pdelay_Req intervals ms: {ws.fmt_stats(di)}")
    if js:
        with open(js, "w") as f:
            json.dump(dict(t0=t0, rows=rows, gm_rate=g_rate, dut_rate=d_rate), f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
