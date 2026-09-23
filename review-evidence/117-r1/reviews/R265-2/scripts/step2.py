#!/usr/bin/env python3
"""Re-derive the Step 2 and Run B wire facts from the A200 tap captures.

usage: step2.py <bench-a200 dir>
"""
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import tapdec as T  # noqa: E402

RUNS = [("A", "bench/runA/tap-runA.pcap"), ("B", "bench/runB/tap-runB.pcap"),
        ("C", "bench/runC/tap-runC.pcap"), ("final", "bench/final/tap-final.pcap")]


def ivals(ts):
    return [(b - a) / 1e6 for a, b in zip(ts, ts[1:])]


def main():
    root = Path(sys.argv[1])
    tot = {k: [] for k in ("sync", "ann", "preq_sw", "preq_dut")}
    means = {k: [] for k in tot}
    logint = {k: set() for k in tot}
    ex_sw = ex_sw_ok = ex_dut = ex_dut_ok = 0
    ta_sw, fu_sw, cl_sw, dif_sw_med = [], [], [], []
    ta_dut, dif_dut_med, ta_dut_big = [], [], []
    ann_n = 0
    ann_gm, ann_path = set(), set()
    dut_master = 0
    dut_sport = set()
    span = 0.0
    for name, rel in RUNS:
        recs, host = T.tap_records(root / rel)
        span += (recs[-1]["tap_ns"] - recs[0]["tap_ns"]) / 1e9
        d = [(r, T.decode(r["frame"])) for r in recs]
        ptp = [(r, x) for r, x in d if x["et"] == 0x88F7 and "mt" in x]
        sel = {
            "sync": [(r, x) for r, x in ptp if r["port"] == 2 and x["mt"] == 0],
            "ann": [(r, x) for r, x in ptp if r["port"] == 2 and x["mt"] == 0xB],
            "preq_sw": [(r, x) for r, x in ptp if r["port"] == 2 and x["mt"] == 2],
            "preq_dut": [(r, x) for r, x in ptp if r["port"] == 3 and x["mt"] == 2],
        }
        for k, v in sel.items():
            iv = ivals([r["tap_ns"] for r, _ in v])
            tot[k] += iv
            means[k].append(round(st.mean(iv), 2))
            logint[k] |= {x["logint"] for _, x in v}
        ann_n += len(sel["ann"])
        ann_gm |= {x["gm"] for _, x in sel["ann"]}
        ann_path |= {tuple(x["path"]) for _, x in sel["ann"]}
        dut_master += sum(1 for r, x in ptp if r["port"] == 3 and x["mt"] in (0, 8, 0xB))
        dut_sport |= {x["sport"] for r, x in ptp if r["port"] == 3}
        # exchanges
        def pair(req_port, resp_port):
            reqs = [(r, x) for r, x in ptp if r["port"] == req_port and x["mt"] == 2]
            resps = {}
            fus = {}
            for r, x in ptp:
                if r["port"] == resp_port and x["mt"] == 3:
                    resps[(x["seq"], x["reqport"])] = (r, x)
                if r["port"] == resp_port and x["mt"] == 0xA:
                    fus[(x["seq"], x["reqport"])] = (r, x)
            rows = []
            for r, x in reqs:
                key = (x["seq"], x["sport"])
                if key in resps and key in fus:
                    rr, rx = resps[key]
                    fr, fx = fus[key]
                    tap = rr["tap_ns"] - r["tap_ns"]
                    claimed = (fx["ts"] - rx["ts"]) + (fx["corr"] - rx["corr"]) / 65536
                    rows.append((tap, fr["tap_ns"] - rr["tap_ns"], claimed))
                else:
                    rows.append(None)
            return rows
        a = pair(2, 3)
        ex_sw += len(a)
        ok = [x for x in a if x]
        ex_sw_ok += len(ok)
        ta_sw += [x[0] for x in ok]
        fu_sw += [x[1] for x in ok]
        cl_sw += [x[2] for x in ok]
        dif_sw_med.append(round(st.median([x[0] - x[2] for x in ok])))
        b = pair(3, 2)
        ex_dut += len(b)
        ok = [x for x in b if x]
        ex_dut_ok += len(ok)
        ta_dut += [x[0] for x in ok]
        dif_dut_med.append(round(st.median([x[0] - x[2] for x in ok])))
        ta_dut_big += [(name, round(x[0] / 1e6, 2)) for x in ok if x[0] > 5e6]
        print(f"run {name}: records {len(recs)}, host-only records {host}, span "
              f"{(recs[-1]['tap_ns'] - recs[0]['tap_ns']) / 1e9:.1f} s, median turnaround "
              f"switch-req {st.median([x[0] for x in a if x]):.0f} ns")
        if name == "B":
            crf = [(r, x) for r, x in d if r["port"] == 3 and x.get("subtype") == 4]
            tus = {x["tu"] for _, x in crf}
            seqs = [x["avtp_seq"] for _, x in crf]
            gaps = sum(1 for p, q in zip(seqs, seqs[1:]) if (q - p) % 256 != 1)
            ts = [r["tap_ns"] for r, _ in crf]
            bursts, start = [], ts[0]
            pauses = []
            for p, q in zip(ts, ts[1:]):
                if q - p > 50e6:
                    bursts.append((p - start) / 1e9)
                    pauses.append(round((q - p) / 1e6))
                    start = q
            bursts.append((ts[-1] - start) / 1e9)
            vl = {x["vlan"] for _, x in crf}
            print(f"  Run B CRF from DUT: {len(crf)} PDUs, tu values {sorted(tus)}, "
                  f"sequence discontinuities {gaps}, VLAN (PCP,VID) {sorted(vl)}")
            print(f"  bursts (s): {[round(b, 2) for b in bursts]}; pauses (ms): {pauses}")
            print(f"  first/last CRF host time (capture-server UTC s): "
                  f"{crf[0][0]['host_ns'] / 1e9:.3f} {crf[-1][0]['host_ns'] / 1e9:.3f}")
    print(f"tapped span summed: {span:.0f} s")
    for k in tot:
        iv = tot[k]
        within = sum(1 for v in iv if abs(v - (125 if k == 'sync' else 1000)) <= 0.3 * (125 if k == 'sync' else 1000))
        print(f"{k}: intervals {len(iv)}, per-run means {means[k]}, min {min(iv):.3f}, "
              f"max {max(iv):.3f} ms, within 30% {within}, logMessageInterval {sorted(logint[k])}")
    print(f"Announce messages {ann_n}; grandmasterIdentity {sorted(ann_gm)}; PathTrace {sorted(ann_path)}")
    print(f"DUT-sent Sync/Follow_Up/Announce records: {dut_master}; DUT source ports {sorted(dut_sport)}")
    print(f"switch requests, DUT responds: {ex_sw_ok} of {ex_sw} complete; tap req->resp "
          f"{min(ta_sw)}..{max(ta_sw)} ns; resp->FU {min(fu_sw)}..{max(fu_sw)} ns; claimed "
          f"{min(cl_sw):.0f}..{max(cl_sw):.0f} ns; per-run median tap-claimed {dif_sw_med}")
    print(f"DUT requests, switch responds: {ex_dut_ok} of {ex_dut} complete; tap req->resp "
          f"{min(ta_dut) / 1e6:.2f}..{max(t for t in ta_dut if t < 5e6) / 1e6:.2f} ms plus {ta_dut_big}; "
          f"per-run median tap-claimed {dif_dut_med}")


if __name__ == "__main__":
    main()
