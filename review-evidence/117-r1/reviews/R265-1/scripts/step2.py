#!/usr/bin/env python3
"""Re-derive the Step 2 numbers of the #117 findings page from the tap pcaps.

Usage: step2.py <bench-a200 dir>
Runs over runA, runB, runC and final tap captures. Prints per-run and
summed cadence, Pdelay exchange pairing and timings, Announce field sets,
the DUT-sent message census, and the Run B CRF tu census.
"""
import os, statistics as st, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tapdec

base = sys.argv[1]
runs = [("A", "bench/runA/tap-runA.pcap"), ("B", "bench/runB/tap-runB.pcap"),
        ("C", "bench/runC/tap-runC.pcap"), ("final", "bench/final/tap-final.pcap")]
SW = "3cc0c6fffefe02100001"
DUT = "020000fffe0000010001"
tot = defaultdict(list)
pair_tot = {"sw_req": [], "dut_req": []}
span_tot = 0.0


def iv(ts):
    return [(b - a) / 1e6 for a, b in zip(ts, ts[1:])]


def within30(v, nom):
    return sum(1 for x in v if abs(x - nom) <= 0.3 * nom)


for name, rel in runs:
    recs, stats = tapdec.load(os.path.join(base, rel))
    span = (recs[-1]["tap_ns"] - recs[0]["tap_ns"]) / 1e9
    span_tot += span
    role = {"020000000001": "DUT", "3cc0c6fe0210": "switch", "3cc0c6fe0211": "switch-port1",
            "3cc0c6010203": "reference-peer"}
    ports = Counter((r["port"], role.get(r["src"], "other-host")) for r in recs)
    print(f"== run {name}: tapped {stats['tapped']} host-only {stats['host_only']} span {span:.3f} s")
    print("   port/src:", dict(ports))
    ptp = [r for r in recs if r["kind"] == "ptp"]
    # which messages each side sends
    cen = Counter((r["port"], r["spid"], r["mt"]) for r in ptp)
    print("   ptp census (port, spid, msgtype): ", sorted(cen.items()))
    for label, port, mt, nom in (("sync sw->dut", 2, 0, 125.0), ("announce sw->dut", 2, 0xB, 1000.0),
                                 ("pdreq sw->dut", 2, 2, 1000.0), ("pdreq dut->sw", 3, 2, 1000.0),
                                 ("followup sw->dut", 2, 8, 125.0)):
        rows = [r for r in ptp if r["port"] == port and r["mt"] == mt]
        v = iv([r["tap_ns"] for r in rows])
        tot[label] += v
        li = sorted({r["logi"] for r in rows})
        sp = sorted({r["spid"] for r in rows})
        dom = sorted({r["domain"] for r in rows})
        if v:
            print(f"   {label}: msgs {len(rows)} intervals {len(v)} mean {st.fmean(v):.3f} min {min(v):.3f} "
                  f"max {max(v):.3f} within30% {within30(v, nom)}/{len(v)} logi {li} spid {sp} domain {dom}")
    ann = [r for r in ptp if r["mt"] == 0xB]
    print("   announce field sets:", Counter((r["port"], r["gm"], r["p1"], r["cls"], hex(r["acc"]), hex(r["var"]),
                                             r["p2"], r["steps"], hex(r["tsrc"]), tuple(r["path"] or [])) for r in ann))
    # Pdelay pairing
    for label, rq_port, rs_port, rq_spid in (("sw_req", 2, 3, SW), ("dut_req", 3, 2, DUT)):
        reqs = [r for r in ptp if r["port"] == rq_port and r["mt"] == 2 and r["spid"] == rq_spid]
        resp = {(r["seq"], r["reqpid"]): r for r in ptp if r["port"] == rs_port and r["mt"] == 3}
        fu = {(r["seq"], r["reqpid"]): r for r in ptp if r["port"] == rs_port and r["mt"] == 0xA}
        comp = 0
        rows = []
        for q in reqs:
            k = (q["seq"], q["spid"])
            if k in resp and k in fu:
                comp += 1
                rs, f = resp[k], fu[k]
                tap_rt = rs["tap_ns"] - q["tap_ns"]
                r2f = f["tap_ns"] - rs["tap_ns"]
                # IEEE 1588 two-step: turnaround = (t3 - t2) + corr(Resp) + corr(Resp_FU)
                claimed = (f["ts"] - rs["ts"]) + (rs["corr"] + f["corr"]) / 65536.0
                rows.append((tap_rt, r2f, claimed, tap_rt - claimed))
        pair_tot[label] += rows
        if rows:
            a = [x[0] for x in rows]; b = [x[1] for x in rows]; c = [x[2] for x in rows]; d = [x[3] for x in rows]
            print(f"   pdelay {label}: complete {comp}/{len(reqs)} tap_req->resp ns [{min(a):.0f},{max(a):.0f}] "
                  f"median {st.median(a):.0f}; resp->fu ns [{min(b):.0f},{max(b):.0f}]; claimed ns "
                  f"[{min(c):.1f},{max(c):.1f}]; tap-claimed median {st.median(d):.1f} [{min(d):.1f},{max(d):.1f}]")
            big = sorted(x for x in a if x > 5e6)
            if big:
                print(f"     over 5 ms: {[round(x / 1e6, 3) for x in big]} ms")
    crf = [r for r in recs if r["kind"] == "crf"]
    if crf:
        tus = Counter((r["port"], r["sid"], r["tu"], r["vlan"]) for r in crf)
        seqs = [r["seq"] for r in crf if r["port"] == 3]
        gaps = sum(1 for a, b in zip(seqs, seqs[1:]) if (b - a) % 256 != 1)
        print(f"   CRF: {len(crf)} PDUs {dict(tus)} seq discontinuities {gaps}")
        t = [r["tap_ns"] for r in crf if r["port"] == 3]
        bursts, start = [], t[0]
        for a, b in zip(t, t[1:]):
            if b - a > 50e6:
                bursts.append(((a - start) / 1e9, (b - a) / 1e6))
                start = b
        bursts.append(((t[-1] - start) / 1e9, None))
        print(f"   CRF bursts (length s, pause ms after): {[(round(x, 3), None if y is None else round(y, 1)) for x, y in bursts]}")
        print(f"   CRF first/last host time: {min(r['host_ns'] for r in crf)/1e9:.3f} {max(r['host_ns'] for r in crf)/1e9:.3f}")
    adp = [r for r in recs if r["kind"] == "adp" and r["port"] == 3]
    if adp:
        print("   DUT ADP gm ids:", Counter(r["gm"] for r in adp))

print("== summed over runs, span", round(span_tot, 1), "s")
for label, v in tot.items():
    print(f"   {label}: intervals {len(v)} min {min(v):.3f} max {max(v):.3f} within30% "
          f"{within30(v, 125.0 if 'sync' in label or 'follow' in label else 1000.0)}/{len(v)}")
for label, rows in pair_tot.items():
    a = [x[0] for x in rows]; d = [x[3] for x in rows]
    print(f"   pdelay {label}: complete {len(rows)} tap_req->resp max {max(a):.0f} ns; tap-claimed [{min(d):.1f},{max(d):.1f}]")
