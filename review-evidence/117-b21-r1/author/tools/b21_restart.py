#!/usr/bin/env python3
"""Lane B21 round 3: grade the Direction A restarts (offline).

usage: b21_restart.py <peer_link_pcap> <dut_link_pcap> <ext_raw_dir> <out_json>

On the peer-link tap (one clock for everything): the peer's DISCONNECT_RX_RESPONSE and
CONNECT_RX_RESPONSE (ACMP, IEEE 1722.1-2021 8.2: message_type 9 and 7, port 3 = sent by the peer) and
every AAF packet of DUT STREAM_OUTPUT 0 the peer receives (port 2). Per cycle:
  stop      the last AAF packet after the DISCONNECT_RX_RESPONSE, and whether any packet arrives from
            0.5 s after it to the CONNECT_RX_RESPONSE (a restart counts only when none does, lane B5's rule);
  restart   CONNECT_RX_RESPONSE to the first AAF packet the peer receives (wire restart);
  first     whether the first 480 frames after the restart are valid pattern frames in order.
The DUT-link tap gives the same per cycle for the packets the DUT sends (port 3).
The external capture (lane B5's reader, hardware-clocked at the peer's output): per cycle, the silence
between the last valid frame before the stop and the first valid frame of the next run of 480; with G
the wire gap (last packet before to first packet after, peer-link tap) and S the captured silence in
frames, the output restarts S/48000 - G later than the wire does, so the restart at the peer's output is
the wire restart plus S/48000 - G plus the steady wire-to-output latency (constant, not measured).
"""
import json
import struct
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b21_aaf  # noqa: E402

SID = bytes.fromhex("0200000000010000")


def scan(pcap):
    acmp, aaf = [], []
    for tap_ns, port, fr, _h in b21_aaf.records(pcap):
        a = b21_aaf.avtp(fr)
        if a is None or len(a) < 24:
            continue
        if a[0] == 0xFC and len(a) >= 56:
            acmp.append(dict(t=tap_ns, port=port, mt=a[1] & 0x0F, status=a[2] >> 3, seq=struct.unpack(">H", a[48:50])[0],
                             talker=a[20:28].hex(), listener=a[28:36].hex()))
        elif a[0] == 0x02 and a[4:12] == SID:
            body = a[24:24 + 192]
            w = np.frombuffer(body, dtype=">u4").astype(np.uint32).reshape(6, 8)
            aaf.append((tap_ns, port, w))
    return acmp, aaf


def frames_valid(ws):
    S = np.concatenate(ws)
    tags = (S >> 24) & 0xFF
    n = (S >> 8) & 0xFFFF
    ok = np.all(tags == np.arange(1, 9, dtype=np.uint32)[None, :], axis=1) & np.all(n == n[:, :1], axis=1) & np.all((S & 0xFF) == 0, axis=1)
    d = np.diff(n[:, 0].astype(np.int64)) % 65536
    return bool(ok.all() and np.all(d == 1))


def per_link(acmp, aaf, port_resp, port_aaf):
    t_aaf = np.array([t for t, p, _ in aaf if p == port_aaf], dtype=np.int64)
    w_aaf = [w for t, p, w in aaf if p == port_aaf]
    disc = [m for m in acmp if m["mt"] == 9 and m["port"] == port_resp]
    conn = [m for m in acmp if m["mt"] == 7 and m["port"] == port_resp]
    return t_aaf, w_aaf, disc, conn


def main(peer_pcap, dut_pcap, ext_dir, out):
    res = dict()
    for link, pc, port_resp, port_aaf in (("peerlink", peer_pcap, 3, 2), ("dutlink", dut_pcap, 2, 3)):
        acmp, aaf = scan(pc)
        t_aaf, w_aaf, disc, conn = per_link(acmp, aaf, port_resp, port_aaf)
        cyc = []
        for k, d in enumerate(disc):
            nxt = [c for c in conn if c["t"] > d["t"]]
            if not nxt:
                break
            c = nxt[0]
            i_last = int(np.searchsorted(t_aaf, d["t"] + int(0.5e9))) - 1
            before = t_aaf[t_aaf <= d["t"] + int(0.5e9)]
            in_hold = int(((t_aaf > d["t"] + int(0.5e9)) & (t_aaf < c["t"])).sum())
            j = int(np.searchsorted(t_aaf, c["t"]))
            if j >= len(t_aaf):
                break
            first_ok = frames_valid(w_aaf[j:j + 80]) if j + 80 <= len(w_aaf) else None
            last_before = int(before[-1]) if len(before) else None
            cyc.append(dict(cycle=k + 1, disconnect_resp_status=d["status"], connect_resp_status=c["status"],
                            last_after_disconnect_s=round((last_before - d["t"]) / 1e9, 6) if last_before else None,
                            packets_in_hold=in_hold, hold_s=round((c["t"] - d["t"]) / 1e9, 4),
                            restart_s=round((int(t_aaf[j]) - c["t"]) / 1e9, 6),
                            wire_gap_s=round((int(t_aaf[j]) - last_before) / 1e9, 6) if last_before else None,
                            first_480_frames_valid_in_order=first_ok))
        r = np.array([c["restart_s"] for c in cyc]) if cyc else np.array([])
        res[link] = dict(acmp_messages=len(acmp), disconnect_responses=len(disc), connect_responses=len(conn),
                         cycles=cyc, restart_s=dict(n=int(len(r)), min=float(r.min()), median=float(np.median(r)),
                                                    max=float(r.max()), under_1s=int((r < 1).sum())) if len(r) else None)
    # external capture
    raw = Path(ext_dir)
    b = np.fromfile(raw / "cap-lr.raw", dtype=np.uint8)
    n = len(b) // 6
    w = b[:n * 6].reshape(n, 2, 3).astype(np.int64)
    w = w[:, :, 0] | (w[:, :, 1] << 8) | (w[:, :, 2] << 16)
    valid = ((w[:, 0] >> 16) == 1) & ((w[:, 1] >> 16) == 2) & ((w[:, 0] & 0xFFFF) == (w[:, 1] & 0xFFFF))
    idx = np.flatnonzero(valid)
    gaps = np.flatnonzero(np.diff(idx) > 2400)        # silences over 50 ms
    ts = np.fromfile(raw / "cap-ts.bin", dtype=np.dtype([("f", "<i8"), ("rt", "<f8"), ("mono", "<i8")]))
    gi = np.diff(ts["mono"]) / 1e6
    ext = []
    for g in gaps:
        a, b_ = int(idx[g]), int(idx[g + 1])
        seg = valid[b_:b_ + 480]
        between = slice(a + 1, b_)
        zeros = int(((w[between, 0] == 0) & (w[between, 1] == 0)).sum())
        ext.append(dict(last_valid=a, first_valid=b_, silence_frames=b_ - a - 1, silence_zero_frames=zeros,
                        first_run_480_valid=bool(seg.all()),
                        step_across=int((w[b_, 0] & 0xFFFF) - (w[a, 0] & 0xFFFF)) % 65536))
    # inside every run, frames are in order (no repeat or skip)
    nn = w[idx, 0] & 0xFFFF
    d = np.diff(nn) % 65536
    inrun = np.diff(idx) == 1
    res["external"] = dict(frames=int(n), valid=int(len(idx)), silences_over_50ms=len(ext),
                           in_run_steps_not_1=int(((d != 1) & inrun).sum()), stalls_over_15ms=int((gi > 15).sum()),
                           silences=ext)
    cyc = res["peerlink"]["cycles"]
    if len(ext) == len(cyc):
        out_r = []
        for c, e in zip(cyc, ext):
            out_r.append(round(c["restart_s"] + e["silence_frames"] / 48000 - c["wire_gap_s"], 6))
        res["output_restart_less_latency_s"] = dict(values=out_r, min=min(out_r), median=float(np.median(out_r)), max=max(out_r),
                                                    under_1s=sum(1 for v in out_r if v < 1))
    else:
        res["output_restart_less_latency_s"] = f"not paired: {len(ext)} captured silences, {len(cyc)} wire cycles"
    json.dump(res, open(out, "w"), indent=1)
    s = {k: (v if k not in ("peerlink", "dutlink", "external") else {kk: vv for kk, vv in v.items() if kk not in ("cycles", "silences")}) for k, v in res.items()}
    print(json.dumps(s, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:5])
