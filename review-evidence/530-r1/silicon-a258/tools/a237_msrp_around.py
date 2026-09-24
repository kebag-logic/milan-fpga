#!/usr/bin/env python3
"""Dump every MSRP MRPDU on the DUT link within +-W s of a tap time (issue 530, A237, read-only).

usage: a237_msrp_around.py <tap.pcap> <t_tap_s> [<W_s>]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a237_analyze as an  # noqa: E402
import wire_summary as ws  # noqa: E402


def main():
    pcap, tc = sys.argv[1], float(sys.argv[2])
    w = float(sys.argv[3]) if len(sys.argv) > 3 else 1.5
    recs = sorted(ws.records(pcap), key=lambda r: r["tap_ns"])
    t0 = recs[0]["tap_ns"]
    last_crf = None
    for r in recs:
        t = (r["tap_ns"] - t0) / 1e9
        k = ws.decode(r).get("kind")
        if k == "CRF" and r["port"] == 3:
            if tc - w <= t <= tc + w and last_crf is not None and t - last_crf > 0.0021:
                print(f"{t:.6f} CRF gap {1e3 * (t - last_crf):.3f} ms")
            last_crf = t
        if k != "MSRP" or not (tc - w <= t <= tc + w):
            continue
        who = "DUT   " if r["port"] == 3 else "switch"
        print(f"{t:.6f} {who} MRPDU len {len(r['frame'])}")
        for v in an.msrp_decode(r["frame"]):
            print(f"      {v['attr']:15} LA={v['la']} nv={v['nv']} first={v['first']} ev={v['ev']} ld={v['ld']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
