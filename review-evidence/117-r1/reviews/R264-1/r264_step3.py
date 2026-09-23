#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Independent reviewer re-derivation of the issue 117 step 3 cycle table.

For one cycle directory of the step 3 packet it reads only raw inputs:
  powerstrip.txt          T_OFF_CMD / T_ON_CMD on the power-strip host clock
  clock-before/after      offsets of the three NTP hosts against the build box
                          (records in the tool's fixed order: capture server,
                          controller host, power-strip host)
  console.txt             0.1 s milan_status poll, build-box send times
  tap-cN.pcap             inline tap on the DUT link

and places every event on the build-box clock, in seconds after the
outlet-off command. The tap is placed on the capture server clock by a least
squares line through the per-5 s minima of (pcap host time - tap time), the
lower envelope of the host receive latency, then moved to the build box with
the capture server offset. Outputs one JSON object per cycle.

With --robust the line is refitted after dropping every bin whose minimum
sits more than 1 ms above it (a lower-envelope fit), repeated to a fixed
point; the default keeps every bin.

Usage: r264_step3.py [--robust] <cycle_dir> [...]
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r264_console as rc  # noqa: E402
import r264_wire as rw  # noqa: E402

DUT = "020000fffe000001"
SW = "3cc0c6fffefe0210"


def offsets(d):
    recs = []
    for name in ("clock-before.jsonl", "clock-after.jsonl"):
        rows = [json.loads(x) for x in open(os.path.join(d, name)) if x.strip()]
        if len(rows) != 3:
            raise SystemExit(f"{d}/{name}: expected 3 host records")
        recs.append(rows)
    # role index: 0 capture server, 1 controller host, 2 power-strip host
    out = {}
    for i, role in enumerate(("server", "ctrl", "strip")):
        b, a = recs[0][i], recs[1][i]
        out[role] = dict(before=b["offset_s_median_best5"], after=a["offset_s_median_best5"],
                         tb=b["local_t"], ta=a["local_t"])
    return out


def off_at(o, t_local):
    # linear interpolation of the offset between the two brackets
    f = (t_local - o["tb"]) / (o["ta"] - o["tb"])
    return o["before"] + f * (o["after"] - o["before"])


def strip_times(d):
    v = {}
    for line in open(os.path.join(d, "powerstrip.txt")):
        p = line.split()
        if p and p[0] in ("T_OFF_CMD", "T_ON_CMD", "T_STATUS_BEFORE", "T_STATUS_AFTER"):
            v[p[0]] = float(p[1])
    return v


ROBUST = False


def fit_tap(recs):
    bins = {}
    for tns, host, port, fr in recs:
        k = int(tns // 5e9)
        dv = host - tns / 1e9
        if k not in bins or dv < bins[k][1]:
            bins[k] = (tns / 1e9, dv)
    pts = sorted(bins.values())
    while True:
        n = len(pts)
        mx = sum(p[0] for p in pts) / n
        my = sum(p[1] for p in pts) / n
        sxx = sum((p[0] - mx) ** 2 for p in pts)
        sxy = sum((p[0] - mx) * (p[1] - my) for p in pts)
        slope = sxy / sxx if sxx else 0.0
        icpt = my - slope * mx
        resid = [p[1] - (icpt + slope * p[0]) for p in pts]
        if not ROBUST:
            break
        keep = [p for p, r in zip(pts, resid) if r <= 0.001]
        if len(keep) == len(pts) or len(keep) < 3:
            break
        pts = keep
    return (lambda tns: tns / 1e9 + icpt + slope * (tns / 1e9)), dict(bins=n, slope_ppm=slope * 1e6,
                                                                    max_abs_resid_ms=max(abs(r) for r in resid) * 1e3)


def good(kv):
    return (kv.get("GPTP_GM") == SW and kv.get("SYNC") == "1" and kv.get("ASCAPABLE") == "1"
            and kv.get("TU") == "0")


def cycle(d):
    n = os.path.basename(d.rstrip("/")).replace("cycle", "")
    o = offsets(d)
    ps = strip_times(d)
    # power-strip host time -> build box
    off_local = ps["T_OFF_CMD"] - off_at(o["strip"], ps["T_OFF_CMD"] - o["strip"]["before"])
    on_local = ps["T_ON_CMD"] - off_at(o["strip"], ps["T_ON_CMD"] - o["strip"]["before"])
    rel = lambda t: round(t - off_local, 3)

    st = [b for b in rc.parse(os.path.join(d, "console.txt")) if b["cmd"] == "milan_status" and "CLKV_STAT" in b["kv"]]
    pre = [b for b in st if b["t"] < off_local]
    post = [b for b in st if b["t"] >= off_local]

    def first(pred, seq):
        for b in seq:
            if pred(b["kv"]):
                return b
        return None

    c_sync0 = first(lambda kv: kv["SYNC"] == "0", post)
    c_tu1 = first(lambda kv: kv["TU"] == "1", post)
    c_gm_self = first(lambda kv: kv["GPTP_GM"] == DUT, post)
    c_asc0 = first(lambda kv: kv["ASCAPABLE"] == "0", post)
    after_self = [b for b in post if b["t"] >= c_gm_self["t"]]
    after_asc0 = [b for b in post if b["t"] >= c_asc0["t"]]
    c_asc1 = first(lambda kv: kv["ASCAPABLE"] == "1", after_asc0)
    c_gm_sw = first(lambda kv: kv["GPTP_GM"] == SW, after_self)
    # all-good: first sample from which every later sample is good
    allgood = None
    for i in range(len(post) - 1, -1, -1):
        if good(post[i]["kv"]):
            allgood = post[i]
        else:
            break
    sample_before_allgood = None
    idx = post.index(allgood)
    if idx > 0:
        sample_before_allgood = post[idx - 1]
    pre_all_good = all(good(b["kv"]) for b in pre)
    c_tu0 = first(lambda kv: kv["TU"] == "0", [b for b in post if b["t"] >= c_gm_sw["t"]])
    gaps = [b2["t"] - b1["t"] for b1, b2 in zip(st, st[1:])]

    pcap = glob.glob(os.path.join(d, "tap-c*.pcap"))[0]
    recs, excluded = rw.tapped(pcap)
    to_server, fitinfo = fit_tap(recs)
    ev = []
    for tns, host, port, fr in recs:
        kind, f = rw.decode(fr)
        t_server = to_server(tns)
        t_local = t_server - off_at(o["server"], t_server - o["server"]["before"])
        ev.append((t_local, port, kind, f))
    sw = [e for e in ev if e[1] == 2]
    sw_before = [e for e in sw if e[0] < on_local]
    sw_after = [e for e in sw if e[0] > on_local]
    isptp = lambda e, mt: e[2] == "ptp" and e[3]["mt"] == mt
    last_sync = max(e[0] for e in sw_before if isptp(e, 0))
    last_ann = max(e[0] for e in sw_before if isptp(e, 0xB))
    last_frame = max(e[0] for e in sw_before)
    last_presp = max(e[0] for e in sw_before if isptp(e, 3))
    first_frame = min(e[0] for e in sw_after)
    first_ann_e = min((e for e in sw_after if isptp(e, 0xB)), key=lambda e: e[0])
    first_ann = first_ann_e[0]
    first_sync = min(e[0] for e in sw_after if isptp(e, 0))
    anns_after = sorted(e[0] for e in sw_after if isptp(e, 0xB))
    # DUT-sent master traffic on return
    dut_after = [e for e in ev if e[1] == 3 and e[0] > on_local]
    dut_sync = [e for e in dut_after if isptp(e, 0)]
    dut_ann = [e for e in dut_after if isptp(e, 0xB)]
    dut_adp = [e for e in ev if e[1] == 3 and e[2] == "adp"]
    dut_adp_self = [e for e in dut_adp if e[3]["gm"] == DUT]
    dut_adp_after = [e for e in dut_adp if e[0] > on_local]
    # silence window on the tap (any direction)
    allt = sorted(e[0] for e in ev)
    big = max(zip(allt, allt[1:]), key=lambda p: p[1] - p[0])
    crf = [e for e in ev if e[1] == 3 and e[2] == "crf"]
    crf_loss = [e for e in crf if off_local <= e[0] < on_local]
    crf_after = [e for e in crf if e[0] > on_local]
    recovery_from = min(first_ann, first_sync)
    r = dict(
        cycle=int(n), tap_excluded=excluded, tap_fit=fitinfo,
        off_for=round(ps["T_ON_CMD"] - ps["T_OFF_CMD"], 2),
        pre_samples=len(pre), pre_all_good=pre_all_good, samples=len(st), max_sample_gap=round(max(gaps), 3),
        dut_sync0=rel(c_sync0["t"]), dut_tu1=rel(c_tu1["t"]), dut_gm_self=rel(c_gm_self["t"]), dut_asc0=rel(c_asc0["t"]),
        sw_last_sync=rel(last_sync), sw_last_ann=rel(last_ann), sw_last_frame=rel(last_frame), sw_last_presp=rel(last_presp),
        sync0_minus_last_sync=round(c_sync0["t"] - last_sync, 3),
        gmself_minus_last_ann=round(c_gm_self["t"] - last_ann, 3),
        asc0_minus_last_presp=round(c_asc0["t"] - last_presp, 3),
        tap_silence=[rel(big[0]), rel(big[1])],
        sw_first_frame=rel(first_frame), sw_first_ann=rel(first_ann), sw_first_sync=rel(first_sync),
        sw_second_ann=rel(anns_after[1]) if len(anns_after) > 1 else None,
        dut_asc1=rel(c_asc1["t"]), dut_gm_sw=rel(c_gm_sw["t"]), dut_allgood=rel(allgood["t"]),
        sample_before_allgood=dict(t=rel(sample_before_allgood["t"]), good=good(sample_before_allgood["kv"])) if sample_before_allgood else None,
        dut_tu0_after_adopt=round(c_tu0["t"] - c_gm_sw["t"], 3) if c_tu0 else None,
        recovery=round(allgood["t"] - recovery_from, 2),
        recovery_from_first_frame=round(allgood["t"] - first_frame, 2),
        on_to_allgood=round(allgood["t"] - on_local, 2),
        first_ann_before_asc1=first_ann < c_asc1["t"],
        gmsw_minus_first_ann=round(c_gm_sw["t"] - first_ann, 3),
        dut_master_syncs=len(dut_sync), dut_master_anns=[dict(t=rel(e[0]), gm=e[3]["gm"], prio1=e[3]["prio1"]) for e in dut_ann],
        dut_adp_total=len(dut_adp), dut_adp_naming_self=len(dut_adp_self),
        dut_first_adp_after=dict(t=rel(dut_adp_after[0][0]), gm=dut_adp_after[0][3]["gm"]) if dut_adp_after else None,
        crf_total=len(crf), crf_tu1=sum(e[3]["tu"] for e in crf),
        crf_first_tu1=rel(min(e[0] for e in crf if e[3]["tu"])) if any(e[3]["tu"] for e in crf) else None,
        crf_tu1_in_loss=sum(e[3]["tu"] for e in crf_loss), crf_last_in_loss=rel(max(e[0] for e in crf_loss)) if crf_loss else None,
        crf_after_first=rel(crf_after[0][0]) if crf_after else None, crf_after_tu1=sum(e[3]["tu"] for e in crf_after),
    )
    return r


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--robust":
        ROBUST = True
        args = args[1:]
    if not args:
        raise SystemExit(__doc__)
    for d in args:
        print(json.dumps(cycle(d)))
