#!/usr/bin/env python3
"""Issue 530 exact-image check, supplementary quantities (A258, offline, read-only).

Reads the tap capture of the DUT link with wire_summary.records (tap port 3 = frames
the DUT sent, tap port 2 = frames the bench switch sent) and the a237_analyze.py JSON
of the same capture. Everything is on the tap hardware clock, seconds from the first
record, exactly as a237_analyze.py reports it. It adds what that tool does not split out:

  1. the LeaveAll MRPDUs of each side inside the streaming interval (first to last
     CRF PDU), with their spacing;
  2. the switch's Listener re-declaration after each DUT LeaveAll that falls while a
     Listener registration exists (after the first Listener Ready), and the DUT's
     TalkerAdvertise re-declaration after each switch LeaveAll in the streaming interval;
  3. CRF PDUs from the DUT before the first Listener Ready (whole capture) and between
     the first probe answer and that Ready;
  4. every GET_COUNTERS response for DUT Stream Output 1 seen on the tap (hardware time),
     and a check of FRAMES_TX against Milan v1.2 5.3.7.7 Table 5.4 as the repository
     documents it: +1 at the end of each 1 s observation interval that carried at least
     one transmitted PDU, reset at STREAM_START. For every tick phase phi (a tick
     boundary at phi + k seconds of tap time), the expected value at a response time r is
     the number of boundaries in (first PDU, min(r, last-PDU interval end)]. The script
     reports the phases, on a 1 ms grid, for which every response agrees.

usage: a258_supplement.py <tap.pcap> <analysis.json>
"""
import json
import math
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wire_summary as ws  # noqa: E402
import a237_analyze as an  # noqa: E402

DUT_EID = bytes.fromhex("020000fffe000001")
SO_NAMES = ["STREAM_START", "STREAM_STOP", "MEDIA_RESET", "TIMESTAMP_UNCERTAIN", "FRAMES_TX"]


def stats(xs):
    return an.stats(xs)


def main():
    pcap, aj = sys.argv[1], sys.argv[2]
    A = json.load(open(aj))
    acc = A["acceptance"]
    recs = sorted(ws.records(pcap), key=lambda r: r["tap_ns"])
    t0 = recs[0]["tap_ns"]
    T = lambda ns: (ns - t0) / 1e9  # noqa: E731

    crf, msrp, so1 = [], [], []
    for r in recs:
        d = ws.decode(r)
        k = d.get("kind")
        if k == "CRF" and r["port"] == 3:
            crf.append(T(r["tap_ns"]))
        elif k == "MSRP":
            msrp.append(dict(t=T(r["tap_ns"]), port=r["port"], vec=an.msrp_decode(r["frame"])))
        elif k == "AECP" and r["port"] == 3:
            p = r["frame"][14:]
            if len(p) >= 32 and (p[1] & 0x0F) == 1 and p[4:12] == DUT_EID:
                ct = struct.unpack(">H", p[22:24])[0] & 0x7FFF
                if ct == 0x0029:
                    dt, di, valid = struct.unpack(">HHI", p[24:32])
                    if dt == 6 and di == 1:
                        blk = p[32:]
                        vals = {n: struct.unpack(">I", blk[4 * i:4 * i + 4])[0]
                                for i, n in enumerate(SO_NAMES) if valid & (1 << i) and 4 * i + 4 <= len(blk)}
                        so1.append((T(r["tap_ns"]), p[2] >> 3, vals))

    tb, tu = acc["bind_t"], acc["unbind_t"]
    f_pdu, l_pdu = acc["first_pdu_t"], acc["last_pdu_t"]
    lr = acc["first_listener_ready_t"]
    print(f"bound window {tb:.6f} .. {tu:.6f} ({tu - tb:.3f} s); streaming {f_pdu:.6f} .. {l_pdu:.6f} "
          f"({l_pdu - f_pdu:.3f} s); first Listener Ready {lr:.6f}")

    # 1. LeaveAlls in the streaming interval
    print("\n== 1. LeaveAll MRPDUs inside the streaming interval (first .. last CRF PDU)")
    la = {p: [x["t"] for x in A["leaveall"][str(p)]] for p in (2, 3)}
    for p, name in ((2, "switch"), (3, "DUT")):
        inb = [t for t in la[p] if tb <= t <= tu]
        ins = [t for t in la[p] if f_pdu <= t <= l_pdu]
        pre = [round(t, 6) for t in la[p] if tb <= t < f_pdu]
        print(f"{name}: bound {len(inb)}, streaming {len(ins)}, bound but before the first PDU {pre}; "
              f"streaming spacing s {stats([ins[k] - ins[k - 1] for k in range(1, len(ins))])}; "
              f"first {ins[0]:.6f} last {ins[-1]:.6f}; first after first PDU {ins[0] - f_pdu:.3f} s, "
              f"last before last PDU {l_pdu - ins[-1]:.3f} s")

    # declarations for the CRF stream
    sw_l, dut_ta = [], []
    for m in msrp:
        for v in m["vec"]:
            for sid, ev, ld in an.sid_values(v):
                if sid != an.DUT_SID:
                    continue
                e = dict(t=m["t"], ev=ev, ld=ld, la=v["la"], attr=v["attr"])
                if m["port"] == 2 and v["attr"] == "Listener":
                    sw_l.append(e)
                elif m["port"] == 3 and v["attr"] == "TalkerAdvertise":
                    dut_ta.append(e)

    def next_join(evs, t):
        return next((e for e in evs if e["t"] > t and e["ev"] != "Lv"), None)

    print("\n== 2. Re-declarations across LeaveAll")
    rl, miss_l = [], []
    for t in la[3]:
        if lr < t <= tu:
            e = next_join(sw_l, t)
            (rl if e else miss_l).append((t, e["t"] - t if e else None))
    print(f"switch Listener after each DUT LeaveAll with a Listener registered (after the first Ready, "
          f"to the unbind): n={len(rl)} {stats([d for _, d in rl])}, missing {len(miss_l)}")
    print("   slowest five:", sorted(((round(d, 6), round(t, 6)) for t, d in rl), reverse=True)[:5])
    rt, miss_t = [], []
    for t in la[2]:
        if f_pdu <= t <= l_pdu:
            e = next_join(dut_ta, t)
            (rt if e else miss_t).append((t, e["t"] - t if e else None))
    print(f"DUT TalkerAdvertise after each switch LeaveAll in the streaming interval: n={len(rt)} "
          f"{stats([d for _, d in rt])}, missing {len(miss_t)}")
    pre_first = [la3 for la3 in la[3] if tb <= la3 < lr]
    print(f"DUT LeaveAlls bound but before the first Listener Ready (no Listener to re-declare yet): "
          f"{[round(x, 6) for x in pre_first]}")

    # 3. PDUs before the first Listener Ready
    print("\n== 3. CRF emission against the first Listener Ready")
    probes = acc["probe_responses"]
    before = [t for t in crf if t < lr]
    fp = probes[0][0]
    between = [t for t in crf if fp <= t < lr]
    print(f"CRF PDUs from the DUT in the whole capture before the first Listener Ready: {len(before)}")
    print(f"first probe answer {probes[0]} ; CRF PDUs between it and the first Ready ({lr - fp:.3f} s): {len(between)}")
    print(f"first PDU - first Ready = {(crf[0] - lr) * 1e3:.3f} ms; switch Listener messages before the first PDU: "
          f"{[(round(e['t'], 6), e['ev'], e['ld']) for e in sw_l if e['t'] < crf[0]]}")
    ta_before = [(round(e["t"], 6), ("LA " if e["la"] else "") + e["ev"]) for e in dut_ta if tb <= e["t"] < lr]
    print(f"DUT TalkerAdvertise between the bind and the first Ready: {len(ta_before)}; first three {ta_before[:3]}")
    gaps = [(crf[k] - crf[k - 1]) * 1e3 for k in range(1, len(crf))]
    print(f"inter-PDU interval over the whole stream: {stats(gaps)}; PDUs after the unbind: "
          f"{sum(1 for t in crf if t > tu)} (last {crf[-1] - tu:.6f} s after it)")

    # 4. FRAMES_TX against the documented semantics
    print("\n== 4. DUT Stream Output 1 GET_COUNTERS responses on the tap (hardware time)")
    print(f"responses {len(so1)}; status not SUCCESS {sum(1 for _, s, _ in so1 if s != 0)}")
    prev = None
    for t, _, v in so1:
        k = tuple(v.get(n) for n in SO_NAMES[:4])
        if k != prev:
            print(f"   {t:.6f} {v}")
            prev = k
    ft = [(t, v["FRAMES_TX"]) for t, _, v in so1 if "FRAMES_TX" in v]
    ft_stream = [(t, x) for t, x in ft if t > f_pdu]
    steps = {}
    for k in range(1, len(ft_stream)):
        dlt = ft_stream[k][1] - ft_stream[k - 1][1]
        steps[dlt] = steps.get(dlt, 0) + 1
    print(f"FRAMES_TX before the first PDU: {sorted({x for t, x in ft if t < f_pdu})}; after it: first "
          f"{ft_stream[:2]}, final {ft[-1]}; read-to-read steps {steps}")

    def expected(phi, r):
        # boundaries at phi + k; count those in (f_pdu, min(r, end_of_last_interval)]
        end = math.floor(l_pdu - phi) + 1 + phi
        hi = min(r, end)
        return max(0, math.floor(hi - phi) - math.floor(f_pdu - phi))

    good = [ms for ms in range(1000) if all(expected(ms / 1000, r) == x for r, x in ft_stream)]
    n_int = {ms: expected(ms / 1000, 1e9) for ms in range(1000)}
    print(f"intervals touched by the stream, by tick phase: {sorted(set(n_int.values()))} "
          f"(= ceil or floor+1 of {l_pdu - f_pdu:.3f} s)")
    if good:
        runs, s = [], good[0]
        for a, b in zip(good, good[1:] + [None]):
            if b != a + 1:
                runs.append((s, a))
                s = b
        rel = [((lo / 1000 - f_pdu) % 1, (hi / 1000 - f_pdu) % 1) for lo, hi in runs]
        print(f"tick phases (tap s mod 1, 1 ms grid) for which all {len(ft_stream)} responses match the "
              f"semantics: {runs} ms; as the first boundary after the first PDU: "
              f"{[(round(a, 3), round(b, 3)) for a, b in rel]} s later")
        print(f"final FRAMES_TX {ft[-1][1]} = intervals touched at those phases: "
              f"{sorted({n_int[ms] for ms in good})}")
    else:
        print("no tick phase reproduces every response: FRAMES_TX does NOT match the documented semantics")
    return 0


if __name__ == "__main__":
    sys.exit(main())
