#!/usr/bin/env python3
"""Reviewer re-derivation of the lane-B2 page tables from the archived packet.

usage: rederive.py <packet author dir> <606 page> <608 page>

Independent of the author's summary/page tools: MSRP and ACMP timing, registrar
classification, LeaveAll/re-declaration bounds and counters are derived here from
msrp.tsv, acmp.tsv and the raw GET_COUNTERS payload bytes. Fields that need the
raw captures (valid-PDU times, which are not published) are taken from each
capture's analysis.json and checked for internal consistency only; this is
stated in the report as a limit.
"""
import json, math, re, statistics, sys
from pathlib import Path

A = Path(sys.argv[1]); P606 = Path(sys.argv[2]).read_text(); P608 = Path(sys.argv[3]).read_text()
SID = "0200000000010001"; DECL = ("New", "JoinIn", "JoinMt")
LEAVETIME = 7.5
fails = []


def check(cond, msg):
    print(("OK   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


def tsv(p):
    lines = p.read_text().splitlines()
    head = lines[0].split("\t")
    return [dict(zip(head, l.split("\t"))) for l in lines[1:]]


def msrp(d):
    ev = tsv(d / "msrp.tsv")
    for i, e in enumerate(ev):
        e["t"] = float(e["t_s"]); e["i"] = i
    return ev


def acmp(d):
    rows = tsv(d / "acmp.tsv")
    for r in rows:
        r["t"] = float(r["t_s"]); r["mt"] = int(r["mt"]); r["status"] = int(r["status"]); r["seq"] = int(r["seq"])
    return rows


def ss_counters(d, which):
    """STREAM_OUTPUT 1 START/STOP decoded from the raw GET_COUNTERS payload bytes."""
    for l in (d / f"snapshot-{which}.jsonl").read_text().splitlines():
        x = json.loads(l)
        if x.get("role") == "dut" and x.get("what") == "counter-6-1":
            b = bytes.fromhex(x["response"]["payload"])
            assert b[0:4] == bytes.fromhex("00060001"), "descriptor"
            valid = int.from_bytes(b[4:8], "big")
            c = [int.from_bytes(b[8 + 4 * k:12 + 4 * k], "big") for k in range(32)]
            assert valid & 3 == 3
            return c[0], c[1], x["t"]
    raise KeyError


def pdus(ev):
    """Group events into MRPDUs by (time, sender) in file order."""
    out, key = [], None
    for e in ev:
        k = (e["t_s"], e["sender"])
        if k != key:
            out.append(dict(t=e["t"], sender=e["sender"], ev=[])); key = k
        out[-1]["ev"].append(e)
    return out


def fmt6(x):
    return f"{x:.6f}"


# ------------------------------------------------------------------ cycles
cyc = {}
for n in range(1, 101):
    d = A / "cycles" / f"cycle-{n:03d}"
    ev, ac, an, res = msrp(d), acmp(d), json.loads((d / "analysis.json").read_text()), json.loads((d / "result.json").read_text())
    dcmd = next(r for r in ac if r["mt"] == 8 and r["status"] == 0 and r["talker"] == "020000fffe000001")
    D = next(r for r in ac if r["mt"] == 9 and r["status"] == 0 and r["seq"] == dcmd["seq"])["t"]
    ccmd = next(r for r in ac if r["mt"] == 6 and r["t"] > D)
    C = ccmd["t"]
    R = next(r for r in ac if r["mt"] == 7 and r["status"] == 0 and r["seq"] == ccmd["seq"])["t"]
    lv = next((e for e in ev if D <= e["t"] < R and e["sender"] == "bridge" and e["type"] == "Listener" and e["stream_id"] == SID and e["event"] == "Lv"), None)
    assert lv, n
    pre = ev[:lv["i"]]
    la = next((e for e in reversed(pre) if e["event"] == "LeaveAll" and e["type"] == "Listener"), None)
    lo = la["i"] + 1 if la else 0
    reg = [e for e in ev[lo:lv["i"]] if e["sender"] == "bridge" and e["type"] == "Listener" and e["stream_id"] == SID and e["event"] in DECL]
    own = [e for e in ev if e["sender"] == "DUT" and e["type"] == "Listener" and e["event"] == "LeaveAll"]
    near = min(own, key=lambda e: abs(e["t"] - lv["t"]), default=None)
    own_after_1ms = near is not None and 0 <= near["t"] - lv["t"] < 0.001
    if (la and not reg and lv["t"] - la["t"] < LEAVETIME) or own_after_1ms:
        klass = "LV"
    elif reg:
        klass = "IN (observed)"
    else:
        klass = "IN (inferred)"
    any_la_before = any(e["event"] == "LeaveAll" for e in pre)
    ta_decl_hold = sum(D <= e["t"] < C and e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["stream_id"] == SID and e["event"] in DECL for e in ev)
    s0, s1, _ = ss_counters(d, "before"); a0, a1, _ = ss_counters(d, "after")
    cyc[n] = dict(D=D, C=C, R=R, lv=lv["t"] - D, lv_abs=lv["t"], klass=klass, la=la, reg=len(reg), near=(near["t"] - lv["t"]) if near else None,
                  any_la_before=any_la_before, ta_decl_hold=ta_decl_hold, before=(s0, s1), after=(a0, a1), delta=(a0 - s0, a1 - s1),
                  an=an, res=res, ev=ev, span=an["capture_span_s"])
    # consistency with the replay's own fields
    check(abs(an["bridge_lv_after_disconnect_s"] - (lv["t"] - D)) < 2e-9 and abs(an["disconnect_response_s"] - D) < 2e-9 and abs(an["response_s"] - R) < 2e-9,
          f"cycle {n}: D/R/Lv times agree with the replay")
    want = {"LV": "LV", "IN (observed)": "IN", "IN (inferred)": "UNDETERMINED"}[klass]
    check(an["registrar_at_lv"] == want, f"cycle {n}: registrar class {klass} matches replay {an['registrar_at_lv']}")
    check(an["msrp_malformed"] == [] and an["target_invalid_or_misdirected"] == 0 and an["reversals"] == 0, f"cycle {n}: no malformed MSRP, no invalid target PDU, no tap-clock reversal")
    check(an["dut_out1_start_stop_delta"] == list(cyc[n]["delta"]), f"cycle {n}: counter delta {cyc[n]['delta']} decoded from raw payload")
    # internal consistency of the PDU-derived fields
    stop608 = an["pdus_after_lv_plus_period"] == 0
    check(stop608 == (an["last_pdu_after_lv_s"] <= 0.002), f"cycle {n}: stop flag consistent with last PDU minus Lv")
    check(an["stopped"] == (an["settled_pdus"] == 0) and an["demonstrated_restart"] == bool(an["stopped"] and an["restart_s"] is not None and an["restart_s"] >= 0),
          f"cycle {n}: stopped/demonstrated flags consistent")
    check(an["restart_s"] == res["latency_s"], f"cycle {n}: replayed restart equals live latency")
    check(an["first_pair_progresses"] is True, f"cycle {n}: first restarted PDU pair progresses")
    check(res["errors"] == [] and res["capture_rc"] == 0, f"cycle {n}: live run clean")

print("\n# #608 registrar classes and stops")
classes = {k: sum(c["klass"] == k for c in cyc.values()) for k in ("IN (observed)", "IN (inferred)", "LV")}
print(classes)
check(classes == {"IN (observed)": 42, "IN (inferred)": 57, "LV": 1}, "42 IN observed, 57 IN inferred, 1 LV")
inf_ok = all(not c["any_la_before"] for c in cyc.values() if c["klass"] == "IN (inferred)")
check(inf_ok, "every IN-inferred cycle has no LeaveAll of any type before its Lv in the capture")
stops = [n for n, c in cyc.items() if c["an"]["pdus_after_lv_plus_period"] == 0]
in_cycles = [n for n, c in cyc.items() if c["klass"] != "LV"]
check(len(stops) == 99 and set(stops) == set(in_cycles), f"99 stops within one PDU, exactly the {len(in_cycles)} IN-registrar cycles")
lvc = [n for n, c in cyc.items() if c["klass"] == "LV"]
check(lvc == [22], f"the only LV cycle is {lvc}")
c22 = cyc[22]
check(c22["la"]["sender"] == "DUT" and abs((c22["lv_abs"] - c22["la"]["t"]) - 0.001390731) < 1e-8,
      f"cycle 22: last Listener LeaveAll before Lv is the DUT's own, {1e3 * (c22['lv_abs'] - c22['la']['t']):.6f} ms before the bridge Lv")
check(c22["reg"] == 0, "cycle 22: no bridge re-declaration between that LeaveAll and the Lv")
check(c22["an"]["hold_pdus"] == 1005 and c22["delta"] == (0, 0) and c22["an"]["stopped"] is False, "cycle 22: 1005 hold PDUs, START/STOP +0/+0, not stopped")
# cycle 22 event table
ev22 = c22["ev"]; D22 = c22["D"]
bla = [e for e in ev22 if e["sender"] == "bridge" and e["event"] == "LeaveAll" and e["type"] == "Listener" and e["t"] < c22["lv_abs"]][-1]
bjm = [e for e in ev22 if e["t_s"] == bla["t_s"] and e["sender"] == "bridge" and e["type"] == "Listener" and e["stream_id"] == SID]
ola = c22["la"]
ota = [e for e in ev22 if e["t_s"] == ola["t_s"] and e["sender"] == "DUT"]
ac22 = acmp(A / "cycles" / "cycle-022")
tab22 = {
    "bridge LeaveAll": round(bla["t"] - D22, 6), "own LeaveAll": round(ola["t"] - D22, 6), "Lv": round(c22["lv_abs"] - D22, 6),
    "CONNECT_RX command": round(c22["C"] - D22, 6), "CONNECT_RX response": round(c22["R"] - D22, 6),
    "probe": round(next(r for r in ac22 if r["mt"] == 0 and r["t"] > c22["R"])["t"] - D22, 6),
    "probe resp": round(next(r for r in ac22 if r["mt"] == 1 and r["t"] > c22["R"])["t"] - D22, 6),
    "bridge New": round(next(e for e in ev22 if e["t"] > c22["R"] and e["sender"] == "bridge" and e["event"] == "New")["t"] - D22, 6),
}
print(tab22, "bridge JoinMt in LeaveAll PDU:", [e["event"] for e in bjm], "own LeaveAll PDU:", sorted({(e['type'], e['event']) for e in ota}))
page22 = {"bridge LeaveAll": -0.391721, "own LeaveAll": 0.009401, "Lv": 0.010791, "CONNECT_RX command": 2.000278, "CONNECT_RX response": 2.008674,
          "probe": 2.008700, "probe resp": 2.008708, "bridge New": 2.020318}
for k, v in page22.items():
    check(abs(tab22[k] - v) <= 1.5e-6, f"cycle 22 table: {k} page {v} vs derived {tab22[k]}")
check([e["event"] for e in bjm] == ["JoinMt"], "cycle 22: bridge LeaveAll MRPDU carries its Listener JoinMt for the stream")
check({("Listener", "LeaveAll"), ("TalkerAdvertise", "LeaveAll"), ("TalkerFailed", "LeaveAll"), ("Domain", "LeaveAll"), ("TalkerAdvertise", "JoinMt")} <= {(e['type'], e['event']) for e in ota},
      "cycle 22: own LeaveAll MRPDU carries all four types and the TA JoinMt")

# near-LeaveAll table
near = {n: c["near"] for n, c in cyc.items() if c["near"] is not None and abs(c["near"]) <= 0.25}
print("own LeaveAll within 0.25 s of Lv:", {n: round(v, 6) for n, v in near.items()})
page_near = {20: 0.202894, 21: 0.118613, 22: -0.001391, 35: -0.099666, 45: -0.242494, 60: -0.191188, 73: -0.091847, 88: 0.199699}
check(set(near) == set(page_near) and all(abs(near[k] - v) < 1.5e-6 for k, v in page_near.items()), "near-LeaveAll table rows and values")
for k in (35, 45, 60, 73):
    check(cyc[k]["klass"] == "IN (observed)" and cyc[k]["la"] is not None and cyc[k]["la"]["sender"] == "DUT" and cyc[k]["reg"] > 0,
          f"cycle {k}: own LeaveAll before Lv, then bridge re-declared before the Lv")

# withdrawal ranges
lvs = [c["lv"] for c in cyc.values()]
check(abs(min(lvs) - 0.008466) < 1e-6 and abs(max(lvs) - 0.098486) < 1e-6, f"bridge Lv after disconnect {min(lvs):.6f}-{max(lvs):.6f}")
st = [cyc[n]["an"] for n in stops]
lp = [a["last_pdu_after_lv_s"] for a in st]
check(abs(min(lp) + 0.001974) < 1e-6 and abs(max(lp) - 0.000001) < 1e-6, f"stopped: last PDU minus Lv {1e3 * min(lp):.3f}..{1e3 * max(lp):.3f} ms")
ld = [a["last_pdu_after_disconnect_s"] for a in st]
check(abs(min(ld) - 0.006858) < 1e-6 and abs(max(ld) - 0.097036) < 1e-6 and abs(statistics.median(ld) - 0.008363) < 1e-6,
      f"stopped: last PDU after disconnect {min(ld):.6f}-{max(ld):.6f}, median {statistics.median(ld):.6f}")
no_dtx = all(not any(r["mt"] == 4 for r in acmp(A / "cycles" / f"cycle-{n:03d}")) for n in cyc)
check(no_dtx, "no DISCONNECT_TX (mt 4) crossed the tap in any cycle")
pre_lv = [c["lv_abs"] for c in cyc.values()]
check(round(min(pre_lv), 3) >= 2.743, f"every cycle capture holds >= 2.743 s before its Lv at printed precision (exact min {min(pre_lv):.6f} s)")

# re-declaration bound after Listener-type LeaveAlls while registered
own_n = br_n = 0; worst = 0.0; unanswered = []
for n, c in cyc.items():
    ev = c["ev"]
    ready = next((e for e in ev if e["t"] > c["R"] and e["sender"] == "bridge" and e["type"] == "Listener" and e["stream_id"] == SID and e["event"] in DECL), None)
    for e in ev:
        if not (e["event"] == "LeaveAll" and e["type"] == "Listener"):
            continue
        registered = e["t"] < c["lv_abs"] or (ready is not None and e["t"] > ready["t"])
        if not registered:
            continue
        nxt = next((x for x in ev[e["i"] + 1:] if x["sender"] == "bridge" and x["type"] == "Listener" and x["stream_id"] == SID and x["event"] in DECL), None)
        if nxt is None or (e["t"] < c["lv_abs"] and nxt["t"] > c["lv_abs"]):
            unanswered.append((n, e["sender"], round(e["t"], 6))); continue
        if e["sender"] == "DUT":
            own_n += 1
        else:
            br_n += 1
        worst = max(worst, nxt["t"] - e["t"])
print(f"Listener LeaveAlls while registered: own {own_n}, bridge {br_n}, worst re-declaration {worst:.6f} s, unanswered {unanswered}")
check(own_n + br_n == 110 and own_n == 53 and br_n == 57 and worst <= 0.088 + 5e-7 and len(unanswered) == 1 and unanswered[0][0] == 22,
      "110 registered LeaveAlls (53 own, 57 bridge) answered within 0.088 s; the only unanswered one is cycle 22's own (answered by Lv)")

# ------------------------------------------------------------------ #75 restarts
print("\n# #75 restarts")
demo = {n: c["an"]["restart_s"] for n, c in cyc.items() if c["an"]["demonstrated_restart"]}
check(len(demo) == 99 and 22 not in demo, "99 demonstrated restarts, cycle 22 excluded")
check(all(c["an"]["restart_s"] is not None and c["an"]["restart_s"] < 1 for c in cyc.values()),
      "all 100 reconnects had a valid PDU within 1 s of the response (cycle 22: stream never stopped)")


def pstats(v):
    v = sorted(v)
    return min(v), statistics.median(v), v[math.ceil(0.95 * len(v)) - 1], max(v)


mn, md, p95, mx = pstats(demo.values())
print("demonstrated:", fmt6(mn), fmt6(md), fmt6(p95), fmt6(mx))
check((fmt6(mn), fmt6(md), fmt6(p95), fmt6(mx)) == ("0.011239", "0.013195", "0.081912", "0.139247") and all(v < 1 for v in demo.values()),
      "distribution min/median/p95(nearest rank)/max")
held = [v for n, v in demo.items() if cyc[n]["ta_decl_hold"] > 0]; wd = {n: v for n, v in demo.items() if cyc[n]["ta_decl_hold"] == 0}
check(len(held) == 96 and sorted(wd) == [1, 4, 44], f"TA held in hold: {len(held)}; withdrawn: {sorted(wd)}")
h = pstats(held); w = pstats(wd.values())
check((fmt6(h[0]), fmt6(h[1]), fmt6(h[3])) == ("0.011239", "0.013143", "0.101353") and (fmt6(w[0]), fmt6(w[1]), fmt6(w[3])) == ("0.105876", "0.126519", "0.139247"),
      f"subgroup stats held {fmt6(h[0])}/{fmt6(h[1])}/{fmt6(h[3])} withdrawn {fmt6(w[0])}/{fmt6(w[1])}/{fmt6(w[3])}")
# OLS slope and Student t 95% interval, t quantile by bisection on the regularized incomplete beta


def betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, dd = 1.0, 1 - qab * x / qap
    dd = 1 / dd; hh = dd
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        dd = 1 / (1 + aa * dd); c = 1 + aa / c; hh *= dd * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        dd = 1 / (1 + aa * dd); c = 1 + aa / c; de = dd * c; hh *= de
        if abs(de - 1) < 1e-15:
            break
    return hh


def ibeta(a, b, x):
    if x <= 0 or x >= 1:
        return 0.0 if x <= 0 else 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x))
    return bt * betacf(a, b, x) / a if x < (a + 1) / (a + b + 2) else 1 - bt * betacf(b, a, 1 - x) / b


def t_cdf(t, df):
    x = df / (df + t * t)
    p = 0.5 * ibeta(df / 2, 0.5, x)
    return 1 - p if t > 0 else p


def t_q(p, df):
    lo, hi = 0.0, 50.0
    for _ in range(200):
        mid = (lo + hi) / 2
        (lo, hi) = (mid, hi) if t_cdf(mid, df) < p else (lo, mid)
    return (lo + hi) / 2


xs = sorted(demo); ys = [demo[k] for k in xs]; nn = len(xs)
mx_, my_ = sum(xs) / nn, sum(ys) / nn
sxx = sum((x - mx_) ** 2 for x in xs); sxy = sum((x - mx_) * (y - my_) for x, y in zip(xs, ys))
b1 = sxy / sxx; b0 = my_ - b1 * mx_
sse = sum((y - b0 - b1 * x) ** 2 for x, y in zip(xs, ys)); df = nn - 2
se = math.sqrt(sse / df / sxx); tq = t_q(0.975, df)
lo, hi = b1 - tq * se, b1 + tq * se
print(f"slope {b1:.9f} se {se:.9f} t {tq:.6f} df {df} CI [{lo:+.9f}, {hi:+.9f}]")
check(f"{b1:.9f}" == "-0.000082801" and f"{lo:+.9f}" == "-0.000234887" and f"{hi:+.9f}" == "+0.000069285" and df == 97 and lo < 0 < hi,
      "OLS slope and 95% interval reproduce and include zero")
f10 = statistics.median(ys[:10]); l10 = statistics.median(ys[-10:])
check((fmt6(f10), fmt6(l10)) == ("0.013168", "0.013255"), f"first/last ten medians {fmt6(f10)} {fmt6(l10)}")
# Spearman rank correlation as a distribution-free cross-check of no growth
rk = lambda v: {i: r for r, i in enumerate(sorted(range(len(v)), key=lambda i: v[i]))}
rx, ry = rk(xs), rk(ys)
rho = 1 - 6 * sum((rx[i] - ry[i]) ** 2 for i in range(nn)) / (nn * (nn * nn - 1))
print(f"Spearman rho restart vs cycle: {rho:+.4f}")
# blocks
page_blocks = {1: ("0.013168", "0.126519", "1.914"), 11: ("0.013282", "0.014413", "2.023"), 21: ("0.013361", "0.014128", "1.887"),
               31: ("0.012941", "0.013640", "1.947"), 41: ("0.013580", "0.139247", "2.068"), 51: ("0.013396", "0.081912", "1.900"),
               61: ("0.012278", "0.015254", "2.025"), 71: ("0.013289", "0.015567", "1.933"), 81: ("0.012856", "0.014272", "1.764"),
               91: ("0.013255", "0.101353", "2.037")}
for s0, (pm, px, prate) in page_blocks.items():
    v = [demo[k] for k in range(s0, s0 + 10) if k in demo]
    npdu = sum(len(pdus(cyc[k]["ev"])) for k in range(s0, s0 + 10)); span = sum(cyc[k]["span"] for k in range(s0, s0 + 10))
    rate = npdu / span
    check((fmt6(statistics.median(v)), fmt6(max(v))) == (pm, px) and f"{rate:.3f}" == prate,
          f"block {s0}-{s0 + 9}: n={len(v)} median {fmt6(statistics.median(v))} max {fmt6(max(v))} MSRP {rate:.3f}/s")
    check(all(sum(1 for _ in pdus(cyc[k]["ev"])) == cyc[k]["an"]["msrp_pdus"] for k in range(s0, s0 + 10)), f"block {s0}: MRPDU grouping equals replay msrp_pdus")

# rows rebuilt from derived values must appear verbatim in the 608 page
print("\n# 608 summary rows rebuilt from derived values")
rows_expected = []
for s0 in range(1, 101, 10):
    v = [demo[k] for k in range(s0, s0 + 10) if k in demo]
    npdu = sum(len(pdus(cyc[k]["ev"])) for k in range(s0, s0 + 10)); span = sum(cyc[k]["span"] for k in range(s0, s0 + 10))
    rows_expected.append(f"| {s0}-{s0 + 9} | {len(v)} | {fmt6(statistics.median(v))} | {fmt6(max(v))} | {npdu / span:.3f} |")
for n, v in sorted(near.items()):
    stop = cyc[n]["an"]["pdus_after_lv_plus_period"] == 0
    rows_expected.append(f"| {n} | {v:+.6f} | {cyc[n]['klass']} | {'stop within one PDU' if stop else 'non-stop hold'} |")
rows_expected.append(f"| Demonstrated restarts | {len(demo)} | {sum(v < 1 for v in demo.values())} | {fmt6(mn)} | {fmt6(md)} | {fmt6(p95)} | {fmt6(mx)} |")
rows_expected.append(f"| DUT Talker Advertise held through the hold | {len(held)} | {sum(v < 1 for v in held)} | {fmt6(h[0])} | {fmt6(h[1])} | - | {fmt6(h[3])} |")
rows_expected.append(f"| DUT Talker Advertise withdrawn in the hold | {len(wd)} | {sum(v < 1 for v in wd.values())} | {fmt6(w[0])} | {fmt6(w[1])} | - | {fmt6(w[3])} |")
rows_expected.append(f"| {fmt6(f10)} | {fmt6(l10)} | {b1:.9f} | [{lo:+.9f}, {hi:+.9f}] | {df} |")
sec22 = P608[P608.index("## Cycle 22"):P608.index("## Restart distribution")]
for k, v in tab22.items():
    rows_expected.append(("c22", k, f"{v:+.6f}"))
for r in rows_expected:
    if isinstance(r, tuple):
        check(r[2] in sec22, f"cycle-22 table carries {r[1]} at {r[2]}")
    else:
        check(r in P608, f"608 page row present: {r}")
check(f"{c22['an']['hold_pdus']:,} valid PDUs" in sec22 and "1.390 ms" in sec22, "cycle-22 prose: hold PDU count and 1.390 ms")

# ------------------------------------------------------------------ per-cycle page table
print("\n# per-cycle table")
rows = re.findall(r"^\| (\d+) \| ([0-9.]+) \| ([^|]+) \| ([+-][0-9.]+) \| (\d+) \| \+(\d) / \+(\d) \| (yes|no) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$", P608, re.M)
check(len(rows) == 100, f"page has 100 per-cycle rows ({len(rows)})")
for r in rows:
    n = int(r[0]); c = cyc[n]; an = c["an"]
    ok = (r[1] == fmt6(c["lv"]) and r[2].strip() == c["klass"] and f"{1e3 * an['last_pdu_after_lv_s']:+.3f}" == r[3]
          and int(r[4]) == an["hold_pdus"] and (int(r[5]), int(r[6])) == c["delta"] and (r[7] == "yes") == (c["ta_decl_hold"] > 0))
    if n in demo:
        ok = ok and r[8].strip() == fmt6(demo[n]) and r[9].strip() == "PASS" and r[10].strip() == "PASS"
    else:
        ok = ok and r[8].strip().startswith("none") and r[10].strip() == "NOT RESTART"
    check(ok, f"page row cycle {n}")

# counters chain across every action in time order
print("\n# counters chain")
acts = []
for d in sorted((A / "bind").iterdir()) + sorted((A / "cycles").iterdir()):
    if (d / "snapshot-before.jsonl").exists():
        b0_, b1_, tb = ss_counters(d, "before"); a0_, a1_, ta = ss_counters(d, "after")
        acts.append((tb, d.name, (b0_, b1_), (a0_, a1_)))
acts.sort()
chain = all(acts[k][3] == acts[k + 1][2] for k in range(len(acts) - 1))
check(chain, "each action's after-counters equal the next action's before-counters")
print("first action", acts[0][1], acts[0][2], "last action", acts[-1][1], acts[-1][3])
tot = {}
for _, name, b, a in acts:
    kind = "cycle" if name.startswith("cycle") else ("bind" if re.match(r"bind-\d", name) else ("unbind" if re.match(r"unbind-\d", name) else name))
    t = tot.setdefault(kind, [0, 0]); t[0] += a[0] - b[0]; t[1] += a[1] - b[1]
print(tot)
check(tot["bind"] == [5, 0] and tot["unbind"] == [0, 4] and tot["cycle"] == [99, 99] and tot["unbind-restore"] == [0, 1], "counter reconciliation +5/+0, +0/+4, +99/+99, +0/+1")
start = [a for a in acts if a[1] not in ("baseline",)][0][2]
check(acts[-1][3] == (115, 115), f"end 115/115 (start of first bind {start})")

# ------------------------------------------------------------------ binds
print("\n# #606 binds")
# the per-bind table, parsed from the 606 page itself
page_b = {}
for m in re.finditer(r"^\| (\d) \| [^|]+ \| ([0-9.]+) \| (\d) / 0 \| SUCCESS \| ([0-9.]+) \(JoinMt\) \| ([0-9.]+), Listener New \| ([0-9.]+) \| ([0-9.]+) \| PASS \|$", P606, re.M):
    check(m[5] == m[6], f"606 page bind {m[1]}: first bridge MRPDU time equals Ready time")
    page_b[int(m[1])] = (float(m[2]), int(m[3]), m[4], m[5], m[7])
check(sorted(page_b) == [1, 2, 3, 4, 5], f"606 page per-bind table parsed ({sorted(page_b)})")
lat = []
for n, (pw, nla, pta, pbr, pfv) in page_b.items():
    d = A / "bind" / f"bind-{n}"
    ev, ac, an = msrp(d), acmp(d), json.loads((d / "analysis.json").read_text())
    cmd = next(r for r in ac if r["mt"] == 6); R = next(r for r in ac if r["mt"] == 7 and r["status"] == 0 and r["seq"] == cmd["seq"])["t"]
    pre = [e for e in ev if e["t"] < cmd["t"]]
    la_pdus = len({e["t_s"] for e in pre if e["sender"] == "DUT" and e["event"] == "LeaveAll"})
    ta_decl = [e for e in pre if e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["event"] in DECL]
    ta_any_sid = sorted({e["event"] for e in pre if e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["stream_id"] == SID})
    br_decl = [e for e in pre if e["sender"] == "bridge" and e["type"] == "Listener" and e["stream_id"] == SID and e["event"] in DECL]
    # DUT LeaveAll followed by no TA declaration: re-declaration would have come within the window
    last_dut_la = max((e["t"] for e in pre if e["sender"] == "DUT" and e["event"] == "LeaveAll"), default=None)
    probe_resp = next(r for r in ac if r["mt"] == 1 and r["sender"] == "DUT" and r["t"] >= cmd["t"])
    probe_cmd = next(r for r in ac if r["mt"] == 0 and r["t"] >= cmd["t"])
    ta = next(e for e in ev if e["t"] >= cmd["t"] and e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["stream_id"] == SID and e["event"] in DECL)
    bp = next(p for p in pdus(ev) if p["sender"] == "bridge" and p["t"] >= R)
    content = sorted({(e["type"], e["event"], e["stream_id"], e["listener"]) for e in bp["ev"]})
    ok = (f"{cmd['t']:.3f}" == f"{pw:.3f}" and la_pdus == nla and not ta_decl and not br_decl and ta_any_sid in ([], ["Mt"])
          and probe_resp["status"] == 0 and probe_resp["seq"] == probe_cmd["seq"] and 27 <= round(1e6 * (probe_cmd["t"] - R)) <= 83
          and abs((probe_resp["t"] - probe_cmd["t"]) - 7e-6) < 1e-6
          and fmt6(ta["t"] - R) == pta and ta["event"] == "JoinMt" and fmt6(bp["t"] - R) == pbr
          and content == [("Listener", "New", SID, "2")] and fmt6(an["latency_s"]) == pfv and an["result"] == "PASS" and an["fresh"] is True
          and an["first_pdu_dmac_ok"] and an["first_pdu_src_ok"] and an["first_pair_progresses"] and an["target_invalid_or_misdirected"] == 0
          and 0.0005 <= an["ready_to_first_pdu_s"] <= 0.0019 and an["dut_out1_start_stop_delta"] == [1, 0] and cmd["t"] >= 16)
    print(f"bind {n}: pre {cmd['t']:.3f} s, DUT LeaveAll PDUs {la_pdus}, DUT TA events for stream {ta_any_sid}, TA decl any stream {len(ta_decl)}, bridge decl {len(br_decl)}, "
          f"probe {1e6 * (probe_cmd['t'] - R):.1f} us status {probe_resp['status']}, first TA {fmt6(ta['t'] - R)} {ta['event']}, first bridge MRPDU {fmt6(bp['t'] - R)} {content}, "
          f"latency {an['latency_s']}, last DUT LeaveAll {cmd['t'] - last_dut_la:.3f} s before command")
    check(ok, f"bind {n} row reproduces; pre-bind window fresh")
    lat.append(an["latency_s"])
check(fmt6(min(lat)) == "0.059352" and fmt6(max(lat)) == "0.229360" and max(lat) < 1, "first-bind latency 0.059-0.229 s, all < 1 s")

print("\n# unbinds")
page_u = {}
for m in re.finditer(r"^\| (\d) \| [0-9.]+ \| ([0-9.]+) \| ([0-9.]+) \| 0 \| ([0-9.]+) \| ([0-9.]+) \| \+0 / \+1 \|$", P606, re.M):
    page_u[int(m[1])] = (m[2], m[3], m[4], m[5])
check(sorted(page_u) == [1, 2, 3, 4], f"606 page unbind table parsed ({sorted(page_u)})")
for n, (plv, plast, ptalv, pq) in page_u.items():
    d = A / "bind" / f"unbind-{n}"
    ev, ac, an = msrp(d), acmp(d), json.loads((d / "analysis.json").read_text())
    dc = next(r for r in ac if r["mt"] == 8 and r["talker"] == "020000fffe000001"); D = next(r for r in ac if r["mt"] == 9 and r["status"] == 0 and r["seq"] == dc["seq"])["t"]
    lv = next(e for e in ev if e["t"] >= D and e["sender"] == "bridge" and e["type"] == "Listener" and e["stream_id"] == SID and e["event"] == "Lv")
    talv = next(e for e in ev if e["t"] >= D and e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["stream_id"] == SID and e["event"] == "Lv")
    after = [e for e in ev if e["t"] > talv["t"] and e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["stream_id"] == SID and e["event"] in DECL]
    ok = (fmt6(lv["t"] - D) == plv and fmt6(an["last_valid_pdu_after_response_s"]) == plast and f"{talv['t'] - D:.3f}" == ptalv
          and f"{an['settle_after_ta_lv_s']:.1f}" == pq and an["pdus_after_lv_plus_period"] == 0 and not after and an["dut_out1_start_stop_delta"] == [0, 1])
    print(f"unbind {n}: Lv {fmt6(lv['t'] - D)}, last PDU {an['last_valid_pdu_after_response_s']}, TA Lv {talv['t'] - D:.3f}, quiet {an['settle_after_ta_lv_s']:.2f}, TA decl after Lv {len(after)}")
    check(ok, f"unbind {n} row reproduces")
    nb = A / "bind" / f"bind-{n + 1}"
    pw = json.loads((nb / "analysis.json").read_text())["pre_window_s"]
    check(an["settle_after_ta_lv_s"] + pw >= 26, f"bind {n + 1}: CONNECT_RX at least {an['settle_after_ta_lv_s'] + pw:.1f} s after the DUT TA Lv (>= 26 s)")

print("\nFAILURES:", len(fails))
for f in fails:
    print("  ", f)
