#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Independent reviewer reading of the step 3 controller-host watcher logs.

Decodes the raw AECP payloads itself (the watcher's own "decoded" fields are
not used) and places every record on the build-box clock in seconds after the
outlet-off command, using the controller-host offset from clock-before/after
and the power-strip log. Prints one JSON object per cycle directory.

GET_AVB_INFO payload: descriptor type/index (4), grandmaster (8), propagation
delay (4), domain (1), flags (1), mapping count (2), mappings.
GET_AS_PATH payload: descriptor index (2), count (2), path (8 each).
GET_COUNTERS payload: descriptor type (2), index (2), counters_valid (4),
32 counters of 4 octets. AVB_INTERFACE: 0 LINK_UP, 1 LINK_DOWN,
5 GPTP_GM_CHANGED. STREAM_OUTPUT: 0 STREAM_START, 1 STREAM_STOP, 2 MEDIA_RESET,
3 TIMESTAMP_UNCERTAIN, 4 FRAMES_TX. STREAM_INPUT: 0 MEDIA_LOCKED,
1 MEDIA_UNLOCKED, 2 STREAM_INTERRUPTED, 11 FRAMES_RX.

Usage: r264_watch.py <cycle_dir> [...]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r264_step3 as s3  # noqa: E402

DUT = "020000fffe000001"
PEER = "3cc0c60102030000"
SW = "3cc0c6fffefe0210"


def counters(p):
    dt = int.from_bytes(p[0:2], "big")
    idx = int.from_bytes(p[2:4], "big")
    vals = [int.from_bytes(p[8 + 4 * i:12 + 4 * i], "big") for i in range((len(p) - 8) // 4)]
    return dt, idx, vals


def cycle(d):
    o = s3.offsets(d)
    ps = s3.strip_times(d)
    off_local = ps["T_OFF_CMD"] - s3.off_at(o["strip"], ps["T_OFF_CMD"] - o["strip"]["before"])
    on_rel = ps["T_ON_CMD"] - ps["T_OFF_CMD"]
    rows = [json.loads(x) for x in open(os.path.join(d, "pw1-watch.jsonl")) if x.strip()]
    rel = lambda t: round(t - s3.off_at(o["ctrl"], t - o["ctrl"]["before"]) - off_local, 3)
    carrier = [(rel(r["t"]), r["value"]) for r in rows if r.get("type") == "carrier"]
    polls = [r for r in rows if r.get("type") == "poll"]
    out = dict(cycle=d.rstrip("/").split("cycle")[-1], carrier=carrier, on_cmd=round(on_rel, 3))
    for tgt, name in ((DUT, "dut"), (PEER, "peer")):
        ai = [(rel(r["t"]), r["status"], bytes.fromhex(r["payload"]) if r.get("payload") else None)
              for r in polls if r["cmd"] == "GET_AVB_INFO" and r["target"] == tgt]
        trans = []
        last = None
        for t, st, p in ai:
            key = (st, p[4:12].hex() if p and st == "SUCCESS" else None, (p[17] & 1) if p and st == "SUCCESS" else None)
            if key != last:
                trans.append((t,) + key)
                last = key
        out[name + "_avb_info_transitions"] = trans
        ap = [(rel(r["t"]), r["status"], bytes.fromhex(r["payload"]) if r.get("payload") else None)
              for r in polls if r["cmd"] == "GET_AS_PATH" and r["target"] == tgt]
        trans = []
        last = None
        for t, st, p in ap:
            if p and st == "SUCCESS":
                n = int.from_bytes(p[2:4], "big")
                key = (st, tuple(p[4 + 8 * i:12 + 8 * i].hex() for i in range(n)))
            else:
                key = (st, None)
            if key != last:
                trans.append((t,) + key)
                last = key
        out[name + "_as_path_transitions"] = trans
        cs = [(rel(r["t"]),) + counters(bytes.fromhex(r["payload"]))
              for r in polls if r["cmd"] == "GET_COUNTERS" and r["target"] == tgt and r["status"] == "SUCCESS"]
        by = {}
        for t, dt, idx, vals in cs:
            by.setdefault((dt, idx), []).append((t, vals))
        summ = {}
        for (dt, idx), seq in by.items():
            first, lastv = seq[0][1], seq[-1][1]
            key = f"dt{dt:#x}/{idx}"
            if dt == 0x0009:  # AVB_INTERFACE
                summ[key] = dict(first=[first[0], first[1], first[5]], last=[lastv[0], lastv[1], lastv[5]])
            elif dt == 0x0006:  # STREAM_OUTPUT
                ts_unc = [(t, v[3], v[0], v[4]) for t, v in seq]
                peaks = []
                for (t1, u1, s1, f1), (t2, u2, s2, f2) in zip(ts_unc, ts_unc[1:]):
                    if s2 != s1:
                        peaks.append(dict(t=t2, start_from=s1, start_to=s2, tsu_before=u1, tsu_after=u2, ftx_before=f1, ftx_after=f2))
                summ[key] = dict(first=dict(start=first[0], stop=first[1], tsu=first[3], ftx=first[4]),
                                 last=dict(start=lastv[0], stop=lastv[1], tsu=lastv[3], ftx=lastv[4]),
                                 max_tsu=max(v[3] for t, v in seq), start_changes=peaks[:12])
            elif dt == 0x0005:  # STREAM_INPUT
                trans = []
                prev = None
                for t, v in seq:
                    k = (v[0], v[1], v[2])
                    if k != prev:
                        trans.append((t, v[0], v[1], v[2], v[11]))
                        prev = k
                summ[key] = dict(transitions=trans[:20])
        out[name + "_counters"] = summ
    adp = [(rel(r["t"]), r["entity_id"], r.get("gptp_gm"), r.get("available_index")) for r in rows if r.get("type") == "adp"]
    for tgt, name in ((DUT, "dut"), (PEER, "peer")):
        a = [x for x in adp if x[1] == tgt]
        tr = []
        last = None
        for t, e, gm, av in a:
            if gm != last:
                tr.append((t, gm, av))
                last = gm
        out[name + "_adp_gm_transitions"] = tr
        out[name + "_adp_avail"] = [a[0][3], a[-1][3]] if a else None
        out[name + "_adp_avail_monotonic"] = all(x[3] < y[3] for x, y in zip(a, a[1:]))
    acmp = [(rel(r["t"]), r.get("tag"), r.get("peer_rx", {}).get("talker"), r.get("peer_rx", {}).get("conn_count"),
             r.get("peer_rx", {}).get("flags")) for r in rows if r.get("type") == "acmp_state"]
    flags = []
    last = None
    for x in acmp:
        if x[4] != last:
            flags.append(x)
            last = x[4]
    out["peer_acmp_flag_transitions"] = flags
    out["peer_acmp_talkers"] = sorted({str(x[2]) for x in acmp})
    out["watch_events"] = [(r["type"], rel(r["t"]), r.get("attempt")) for r in rows if r.get("type") in ("bind", "unbind", "unbound", "interrupted", "done")]
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    for d in sys.argv[1:]:
        print(json.dumps(cycle(d)))
