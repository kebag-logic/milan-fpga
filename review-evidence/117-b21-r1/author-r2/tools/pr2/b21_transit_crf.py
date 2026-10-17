#!/usr/bin/env python3
"""Lane B21 PR round 2: Direction A transit between the taps, and the CRF stream on both taps (offline).

usage: b21_transit_crf.py <dut_link_pcap> <peer_link_pcap> <out_json>

Transit: every AAF packet of DUT STREAM_OUTPUT 0 (stream 0200000000010000) sent by the DUT (DUT-link
tap, port 3) and received by the peer (peer-link tap, port 2), paired by (sequence number,
avtp_timestamp), as b21_grade.py wire pairs them. dt = peer-tap time - DUT-tap time. The two taps run
on independent clocks, so dt drifts with their rate difference: a least-squares line in DUT-tap time
gives that rate (ppm); the residual is the transit's variation, not an absolute latency.

CRF: every packet of DUT STREAM_OUTPUT 1 (stream 0200000000010001, AVTP subtype 0x04) in the same
directions: packets, sequence-number breaks, seconds and rate on each tap's clock.
"""
import json
import struct
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b21_aaf  # noqa: E402

AAF_SID = bytes.fromhex("0200000000010000")
CRF_SID = bytes.fromhex("0200000000010001")


def scan(pcap, port):
    aaf, crf = [], []
    for tap_ns, p, fr, _h in b21_aaf.records(pcap):
        if p != port:
            continue
        a = b21_aaf.avtp(fr)
        if a is None or len(a) < 24:
            continue
        if a[0] == 0x02 and a[4:12] == AAF_SID:
            aaf.append((tap_ns, a[2], struct.unpack(">I", a[12:16])[0]))
        elif a[0] == 0x04 and a[4:12] == CRF_SID:
            crf.append((tap_ns, a[2]))
    return np.array(aaf, dtype=np.int64).reshape(-1, 3), np.array(crf, dtype=np.int64).reshape(-1, 2)


def crf_grade(c):
    sq = np.diff(c[:, 1]) % 256
    sec = (c[-1, 0] - c[0, 0]) / 1e9
    return dict(packets=int(len(c)), seq_breaks=int((sq != 1).sum()), seconds_tap=round(float(sec), 3),
                rate_pps=round((len(c) - 1) / sec, 3))


def main(dut_pcap, peer_pcap, out):
    da, dc = scan(dut_pcap, 3)
    pa, pc = scan(peer_pcap, 2)
    key = {}
    for i, (s, t) in enumerate(zip(da[:, 1].tolist(), da[:, 2].tolist())):
        key.setdefault((s, t), i)
    # first peer packet present on the DUT tap; then pair by position, as b21_grade.py wire does
    j0 = next(j for j in range(len(pa)) if (int(pa[j, 1]), int(pa[j, 2])) in key)
    i0 = key[(int(pa[j0, 1]), int(pa[j0, 2]))]
    m = min(len(da) - i0, len(pa) - j0)
    A, B = da[i0:i0 + m], pa[j0:j0 + m]
    same = (A[:, 1] == B[:, 1]) & (A[:, 2] == B[:, 2])
    x = (A[:, 0] - A[0, 0]) / 1e9
    dt = (B[:, 0] - A[:, 0]).astype(np.float64)
    slope, icpt = np.polyfit(x, dt, 1)
    r = dt - (slope * x + icpt)
    res = dict(inputs=[Path(dut_pcap).name, Path(peer_pcap).name],
               transit=dict(pairs=int(m), pairs_same_seq_and_timestamp=int(same.sum()), dut_first=int(i0), peer_first=int(j0),
                            span_s=round(float(x[-1]), 3), rate_difference_ppm=round(float(slope) / 1e3, 6),
                            residual_us=dict(min=round(float(r.min()) / 1e3, 3), p50=round(float(np.median(r)) / 1e3, 3),
                                             max=round(float(r.max()) / 1e3, 3)),
                            undetrended_minus_median_us=dict(min=round(float((dt - np.median(dt)).min()) / 1e3, 3),
                                                             max=round(float((dt - np.median(dt)).max()) / 1e3, 3)),
                            note="tap clocks independent: the rate difference and the residual are relative, not absolute latency"),
               crf=dict(dutlink_sent_by_dut=crf_grade(dc), peerlink_received_by_peer=crf_grade(pc)))
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:4])
