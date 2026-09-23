#!/usr/bin/env python3
"""Independent re-derivation of the #117 Step 2 wire statistics and the Run B
CRF `tu` count from the A200 tap captures, on the tap clock only.

usage: rederive_step2.py <bench-a200 root>
"""
import os
import statistics
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rederive_step3 import ptp_records  # noqa: E402

RUNS = ["runA/tap-runA.pcap", "runB/tap-runB.pcap", "runC/tap-runC.pcap", "final/tap-final.pcap"]


def parse(recs):
    out = []
    for t, port, fr in recs:
        et = struct.unpack(">H", fr[12:14])[0]
        off = 14
        if et == 0x8100:
            et = struct.unpack(">H", fr[16:18])[0]
            off = 18
        p = fr[off:]
        if et == 0x88F7 and len(p) >= 34:
            out.append({"t": t, "port": port, "kind": "ptp", "mt": p[0] & 0xF, "seq": struct.unpack(">H", p[30:32])[0],
                        "src": p[20:30].hex(), "lmi": struct.unpack("b", p[33:34])[0], "p": p})
        elif et == 0x22F0 and p and (p[0] & 0x7F) == 0x04:
            out.append({"t": t, "port": port, "kind": "crf", "tu": p[1] & 1, "seq": p[2]})
    return out


def ivals(ts):
    return [b - a for a, b in zip(ts, ts[1:])]


def main():
    root = sys.argv[1]
    agg = {k: [] for k in ("sync", "ann", "preq_sw", "preq_dut")}
    means = {k: [] for k in agg}
    lmi = {}
    turn_dut, turn_sw, span = [], [], 0.0
    exch_dut = [0, 0]
    exch_sw = [0, 0]
    for r in RUNS:
        M = parse(ptp_records(os.path.join(root, "bench", r)))
        ptp = [m for m in M if m["kind"] == "ptp"]
        if ptp:
            span += ptp[-1]["t"] - ptp[0]["t"]
        sel = {
            "sync": [m for m in ptp if m["port"] == 2 and m["mt"] == 0],
            "ann": [m for m in ptp if m["port"] == 2 and m["mt"] == 0xB],
            "preq_sw": [m for m in ptp if m["port"] == 2 and m["mt"] == 2],
            "preq_dut": [m for m in ptp if m["port"] == 3 and m["mt"] == 2],
        }
        for k, v in sel.items():
            iv = ivals([m["t"] for m in v])
            agg[k] += iv
            if iv:
                means[k].append(statistics.mean(iv))
            lmi.setdefault(k, set()).update(m["lmi"] for m in v)
        # turnaround: request seen on one port, response with the same seq on the other
        resp = {(m["port"], m["seq"]): m for m in ptp if m["mt"] == 3}
        fu = {(m["port"], m["seq"]) for m in ptp if m["mt"] == 0xA}
        for m in sel["preq_sw"]:
            exch_sw[1] += 1
            rr = resp.get((3, m["seq"]))
            if rr:
                turn_dut.append(rr["t"] - m["t"])
                if (3, m["seq"]) in fu:
                    exch_sw[0] += 1
        for m in sel["preq_dut"]:
            exch_dut[1] += 1
            rr = resp.get((2, m["seq"]))
            if rr:
                turn_sw.append(rr["t"] - m["t"])
                if (2, m["seq"]) in fu:
                    exch_dut[0] += 1
        if r.startswith("runB"):
            crf = [m for m in M if m["kind"] == "crf" and m["port"] == 3]
            seqgap = sum(1 for a, b in zip(crf, crf[1:]) if (a["seq"] + 1) & 0xFF != b["seq"])
            print(f"Run B CRF PDUs from the DUT: {len(crf)}, with tu=1: {sum(m['tu'] for m in crf)}, sequence gaps: {seqgap}")
    ms = lambda x: round(x * 1e3, 1)
    for k, v in agg.items():
        print(f"{k}: intervals {len(v)}, per-run mean ms {[ms(x) for x in means[k]]}, min {ms(min(v))} ms, max {ms(max(v))} ms, "
              f"within 30%: {sum(1 for x in v if abs(x - (0.125 if k == 'sync' else 1.0)) <= 0.3 * (0.125 if k == 'sync' else 1.0))}, logMessageInterval {sorted(lmi[k])}")
    print(f"switch requests, DUT responds: {exch_sw[0]} of {exch_sw[1]} complete; request-to-response ns min {min(turn_dut) * 1e9:.0f} max {max(turn_dut) * 1e9:.0f}")
    big = sorted(x for x in turn_sw if x > 0.015)
    print(f"DUT requests, switch responds: {exch_dut[0]} of {exch_dut[1]} complete; response ms min {min(turn_sw) * 1e3:.2f} max(<15ms) {max(x for x in turn_sw if x <= 0.015) * 1e3:.2f}; over 15 ms: {[round(x * 1e3, 2) for x in big]}")
    print(f"PTP span summed over the four captures: {span:.1f} s")


if __name__ == "__main__":
    main()
