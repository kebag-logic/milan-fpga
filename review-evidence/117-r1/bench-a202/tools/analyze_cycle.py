#!/usr/bin/env python3
"""Analyze one GM loss/return cycle (issue 117, A202, steps 3 and 4).

usage: analyze_cycle.py <cycle_dir> [--json <out.json>]

Inputs in <cycle_dir> (written by run_cycle.sh): console.txt (0.1 s console
poll, build-box time), powerstrip.txt (power-strip host time), pw1-watch.jsonl
(controller-host time), clock-before/after.jsonl (remote-minus-local offsets),
tap-c<N>.pcap (inline tap on the DUT link) and pw1-c<N>.pcap (controller-host
port).

Every time is converted to the build-box clock ("local"). NTP hosts are
shifted by their measured offset (mean of before and after). Tap records are
placed on the capture host's clock by the lower envelope of (pcap host time -
tap hardware time), fitted per 5 s window, which removes the USB batching
delay; intervals keep the tap's own clock. Printed times are seconds relative
to the outlet-off command (T_off = 0). Prints facts; asserts nothing.
"""
import json
import re
import statistics as st
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wire_summary as ws  # noqa: E402

SWITCH_GM = "3cc0c6fffefe0210"
DUT_CLOCK = "020000fffe000001"
DUT_EID = "020000fffe000001"
PEER_EID = "3cc0c60102030000"
PEER_CLOCK0 = "3cc0c6fffe010203"
STATUS_RE = re.compile(
    r"GPTP_GM=(?P<gm>[0-9a-f]{16}) GPTP_PARENT=(?P<parent>[0-9a-f]{16}) PDELAY_NS=(?P<pdelay>\d+) "
    r"AS_PATH_COUNT=(?P<pc>\d+) AS_PATH_GEN=(?P<pg>\d+) CLKV_STAT=(?P<clkv>[0-9a-f]{8}) "
    r"SYNC=(?P<sync>\d) ASCAPABLE=(?P<asc>\d) TU=(?P<tu>\d) GPTP_LAT=(?P<lat>[0-9a-f]{8})")
TAI_RE = re.compile(r"TAI_NS=0x(?P<tai>[0-9a-f]+)")
MEM_RE = re.compile(r"^0x(?P<addr>[0-9a-f]{8})\s+(?P<b>(?:[0-9a-f]{2} ){4})", re.M)
HDR_RE = re.compile(r"^### (?P<ts>\S+)Z cmd='(?P<cmd>[^']*)' elapsed=(?P<el>[0-9.]+)s", re.M)
NAMES = {0x90000780: "tucnt", 0x90000774: "linkg", 0x90000720: "epoch", 0x90000750: "crft_ctrl",
         0x90000764: "crft_count"}
PS_RE = re.compile(r"(T_[A-Z_]+) (\d+\.\d+)")


def offsets(d):
    out = {}
    for name in ("clock-before.jsonl", "clock-after.jsonl"):
        for line in (d / name).read_text().splitlines():
            if line.startswith("{"):
                r = json.loads(line)
                out.setdefault(r["host"], []).append(r["offset_s"])
    return {h: st.fmean(v) for h, v in out.items()}


def parse_console(path):
    text = path.read_text(errors="replace")
    heads = list(HDR_RE.finditer(text))
    samples, cur = [], None
    for i, h in enumerate(heads):
        body = text[h.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        t = datetime.strptime(h["ts"], "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc).timestamp()
        if h["cmd"] == "milan_status":
            m = STATUS_RE.search(body)
            cur = dict(t=t, el=float(h["el"]), **(m.groupdict() if m else {"parse": "FAILED"}))
            ta = TAI_RE.search(body)
            if ta:
                cur["tai"] = int(ta["tai"], 16)
            if m:
                cur["hold"] = (int(m["clkv"], 16) >> 3) & 1
            samples.append(cur)
        elif h["cmd"].startswith("mem_read") and cur is not None:
            m = MEM_RE.search(body)
            if m:
                a = int(m["addr"], 16)
                cur[NAMES.get(a, hex(a))] = int.from_bytes(bytes.fromhex(m["b"].replace(" ", "")), "little")
    return samples


def tap_records(pcap, off_server):
    recs = sorted((ws.decode(r) for r in ws.records(str(pcap))), key=lambda d: d["tap_ns"])
    if not recs:
        return [], None
    # lower envelope of host - tap per 5 s window (windows with at least 30
    # records only, since a sparse window's minimum need not reach the USB
    # floor), then a least-squares line through the minima, refitted twice
    # without minima more than 2 ms above or below the line
    t0 = recs[0]["tap_ns"]
    wins = {}
    for r in recs:
        k = (r["tap_ns"] - t0) // 5_000_000_000
        dlt = r["host_ns"] - r["tap_ns"]
        w = wins.setdefault(k, [0, None])
        w[0] += 1
        if w[1] is None or dlt < w[1][1]:
            w[1] = (r["tap_ns"], dlt)
    pts = [w[1] for w in wins.values() if w[0] >= 30]

    def line(pp):
        xs = [v[0] for v in pp]
        ys = [v[1] for v in pp]
        if len(xs) < 2:
            return ys[0], 0.0
        mx, my = st.fmean(xs), st.fmean(ys)
        b_ = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
        return my - b_ * mx, b_

    a, b = line(pts)
    kept = pts
    for _ in range(2):
        kept = [v for v in pts if abs(v[1] - (a + b * v[0])) <= 2_000_000] or pts
        a, b = line(kept)
    resid = [v[1] - (a + b * v[0]) for v in kept]
    for r in recs:
        r["local"] = (r["tap_ns"] + a + b * r["tap_ns"]) / 1e9 - off_server
    fit = dict(windows=len(wins), windows_used=len(kept), windows_dense=len(pts), slope_ppm=round(b * 1e6, 3),
               resid_ms_max=round(max(abs(x) for x in resid) / 1e6, 3))
    return recs, fit


def first(seq, pred):
    for x in seq:
        if pred(x):
            return x
    return None


def last(seq, pred):
    for x in reversed(seq):
        if pred(x):
            return x
    return None


def good(s):
    return (s.get("gm") == SWITCH_GM and s.get("sync") == "1" and s.get("asc") == "1" and s.get("tu") == "0")


def main():
    d = Path(sys.argv[1])
    jout = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
    n = d.name.replace("cycle", "")
    off = offsets(d)
    res = dict(cycle=n, offsets_s={h: round(v, 6) for h, v in off.items()})
    ps = dict(PS_RE.findall((d / "powerstrip.txt").read_text()))
    t_off = float(ps["T_OFF_CMD"]) - off["<bench-host-prefix>pi"]
    t_off_done = float(ps["T_OFF_DONE"]) - off["<bench-host-prefix>pi"]
    t_on = float(ps["T_ON_CMD"]) - off["<bench-host-prefix>pi"]
    t_on_done = float(ps["T_ON_DONE"]) - off["<bench-host-prefix>pi"]

    def rel(t):
        return None if t is None else round(t - t_off, 3)

    res["power"] = dict(off_cmd=0.0, off_done=rel(t_off_done), on_cmd=rel(t_on), on_done=rel(t_on_done),
                        hold_s=round(t_on - t_off, 3), t_off_local_utc=datetime.fromtimestamp(t_off, timezone.utc).isoformat())
    print(f"== cycle {n}: outlet off at {res['power']['t_off_local_utc']} (build-box clock); "
          f"offsets {res['offsets_s']}")
    print(f"   power: off done {rel(t_off_done)} s, on cmd {rel(t_on)} s, on done {rel(t_on_done)} s")

    # ---------------- controller host: carrier, ADP, polls ----------------
    rows = [json.loads(x) for x in (d / "pw1-watch.jsonl").read_text().splitlines() if x.startswith("{")]
    for r in rows:
        r["local"] = r["t"] - off["<bench-host-prefix>pw1"]
    car = [r for r in rows if r["type"] == "carrier"]
    car_down = first(car, lambda r: r["value"] == 0 and r["local"] > t_off - 1)
    car_up = first(car, lambda r: r["value"] == 1 and car_down and r["local"] > car_down["local"])
    res["pw1_carrier"] = dict(down=rel(car_down and car_down["local"]), up=rel(car_up and car_up["local"]))
    print(f"   controller-host port carrier: down {res['pw1_carrier']['down']} s, up {res['pw1_carrier']['up']} s")
    adp = [r for r in rows if r["type"] == "adp"]
    res["adp"] = {}
    for eid in (DUT_EID, PEER_EID):
        seq = [r for r in adp if r["entity_id"] == eid and r["interface_index"] == 0]
        trans, prev = [], None
        for r in seq:
            if r["gptp_gm"] != prev:
                trans.append((rel(r["local"]), r["gptp_gm"], r["available_index"]))
                prev = r["gptp_gm"]
        ai = [r["available_index"] for r in seq]
        mono = all(b >= a for a, b in zip(ai, ai[1:]))
        res["adp"][eid] = dict(transitions=trans, available_index_first=ai[0] if ai else None,
                               available_index_last=ai[-1] if ai else None, monotonic=mono, count=len(seq))
        print(f"   ADP heard at the controller host from {eid}: {len(seq)} adverts, available_index "
              f"{ai[0] if ai else None} -> {ai[-1] if ai else None} monotonic={mono}; gm transitions {trans}")
    polls = [r for r in rows if r["type"] == "poll"]
    res["poll"] = {}
    for eid in (DUT_EID, PEER_EID):
        ai = [r for r in polls if r["target"] == eid and r["what"] == "avb_info"]
        trans, prev = [], "start"
        for r in ai:
            dec = r.get("decoded", {})
            key = (r["status"], dec.get("gm"), dec.get("as_capable"))
            if key != prev:
                trans.append((rel(r["local"]),) + key)
                prev = key
        ctr = [r for r in polls if r["target"] == eid and r["what"] == "avb_counters" and r.get("decoded")]
        c0 = ctr[0]["decoded"]["c"] if ctr else {}
        c1 = ctr[-1]["decoded"]["c"] if ctr else {}
        delta = {k: c1.get(k, 0) - c0.get(k, 0) for k in c1}
        res["poll"][eid] = dict(avb_info_transitions=trans, counters_first=c0, counters_last=c1,
                                counters_delta=delta)
        print(f"   GET_AVB_INFO {eid} (status, gm, as_capable) transitions: {trans}")
        print(f"   AVB_INTERFACE counters {eid}: first {c0} last {c1} delta {delta} "
              f"(0 LINK_UP, 1 LINK_DOWN, 5 GPTP_GM_CHANGED)")
        ap = [r for r in polls if r["target"] == eid and r["what"] == "as_path"]
        ptrans, prev = [], "start"
        for r in ap:
            key = (r["status"], json.dumps(r.get("decoded", {}).get("path")))
            if key != prev:
                ptrans.append((rel(r["local"]),) + key)
                prev = key
        res["poll"][eid]["as_path_transitions"] = ptrans
        print(f"   GET_AS_PATH {eid} transitions: {ptrans}")
    for what in ("peer_in_counters", "dut_out_counters"):
        cs = [r for r in polls if r["what"] == what and r.get("decoded")]
        if cs:
            traj, prev = [], None
            for r in cs:
                c = r["decoded"]["c"]
                if c != prev:
                    traj.append((rel(r["local"]), c))
                    prev = c
            res[what] = traj
            print(f"   {what} changes (t, counters): {len(traj)}")
            for t, c in traj:
                print(f"      {t} {c}")
    acmp = [r for r in rows if r["type"] == "acmp_state" and "peer_rx" in r]
    if acmp:
        trans, prev = [], None
        for r in acmp:
            p = r["peer_rx"]
            key = (p.get("status"), p.get("talker"), p.get("conn_count"), p.get("flags"))
            if key != prev:
                trans.append((rel(r["local"]), r["tag"]) + key)
                prev = key
        res["peer_rx_transitions"] = trans
        print(f"   peer STREAM_INPUT 8 ACMP state transitions: {trans}")
    for typ in ("bind", "unbind", "unbound", "unbind_failed", "refused", "interrupted", "done"):
        for r in rows:
            if r["type"] == typ:
                print(f"   watcher {typ} at {rel(r['local'])} s: "
                      f"{ {k: v for k, v in r.items() if k not in ('t', 'local', 'type')} }")
                res.setdefault("watcher_events", []).append((typ, rel(r["local"])))

    # ---------------- console ----------------
    cs = parse_console(d / "console.txt")
    for s in cs:
        s["rel"] = rel(s["t"])
    res["console"] = dict(samples=len(cs), first=cs[0]["rel"], last=cs[-1]["rel"],
                          epoch_values=sorted({s.get("epoch") for s in cs if "epoch" in s}),
                          id_version_parse_failures=sum(1 for s in cs if s.get("parse") == "FAILED"))
    gaps = [b["t"] - a["t"] for a, b in zip(cs, cs[1:])]
    res["console"]["max_gap_s"] = round(max(gaps), 3)
    print(f"   console: {len(cs)} samples from {cs[0]['rel']} to {cs[-1]['rel']} s, max gap "
          f"{res['console']['max_gap_s']} s, RST_EPOCH values {res['console']['epoch_values']}")
    keys = ("gm", "parent", "pc", "pg", "clkv", "sync", "asc", "tu", "hold", "linkg", "tucnt", "crft_ctrl")
    trans, prev = [], None
    for s in cs:
        key = tuple(s.get(k) for k in keys)
        if key != prev:
            trans.append((s["rel"],) + key)
            prev = key
    res["console"]["transitions"] = trans
    print("   console transitions (t, gm, parent, path count, path gen, CLKV_STAT, sync, asCapable, tu, "
          "holdover, LINKG_STAT, CLKV_TUCNT, CRFT_CTRL):")
    for t in trans:
        print("      " + " ".join(str(x) if not isinstance(x, int) or x < 256 else hex(x) for x in t))
    pre = [s for s in cs if s["t"] < t_off]
    res["console"]["pre_all_good"] = all(good(s) for s in pre)
    res["console"]["pre_samples"] = len(pre)
    # loss declaration
    after_off = [s for s in cs if s["t"] >= t_off]
    loss = {}
    for name, pred in (("asCapable_0", lambda s: s.get("asc") == "0"),
                       ("sync_0", lambda s: s.get("sync") == "0"),
                       ("tu_1", lambda s: s.get("tu") == "1"),
                       ("gm_changed", lambda s: s.get("gm") != SWITCH_GM)):
        f = first(after_off, pred)
        if f:
            i = cs.index(f)
            loss[name] = dict(first_seen=f["rel"], previous_sample=cs[i - 1]["rel"], value=f.get(name.split("_")[0] if name != "gm_changed" else "gm"))
        else:
            loss[name] = None
    res["dut_loss"] = loss
    print(f"   DUT loss declaration (first sample after T_off, previous sample): {loss}")
    # absent window: between off and the first switch frame after on (filled below from the tap)
    recs, fit = tap_records(d / f"tap-c{n}.pcap", off["<bench-host-prefix>ubuntu-server"])
    res["tap_fit"] = fit
    print(f"   tap: {len(recs)} records, host-generated excluded {ws.HOST_RECORDS[0]}, "
          f"clock fit {fit}")
    sw = [r for r in recs if r["port"] == 2]
    dut = [r for r in recs if r["port"] == 3]
    last_sw = last(sw, lambda r: r["local"] < t_off + 5)
    first_sw_after = first(sw, lambda r: r["local"] > t_off + 1.0)
    last_dut_before = last(dut, lambda r: r["local"] < (first_sw_after["local"] if first_sw_after else 1e20))
    res["tap"] = dict(last_far_end_frame=rel(last_sw and last_sw["local"]),
                      last_far_end_kind=last_sw and last_sw["kind"],
                      first_far_end_frame_after=rel(first_sw_after and first_sw_after["local"]),
                      first_far_end_kind=first_sw_after and first_sw_after["kind"])
    gp = {}
    for kind in ("gPTP Announce", "gPTP Sync", "gPTP Follow_Up", "gPTP Pdelay_Req", "gPTP Pdelay_Resp"):
        lb = last(sw, lambda r, k=kind: r["kind"] == k and r["local"] < t_off + 5)
        fa = first(sw, lambda r, k=kind: r["kind"] == k and r["local"] > t_off + 1.0)
        gp[kind] = dict(last_before=rel(lb and lb["local"]), first_after=rel(fa and fa["local"]))
        if kind == "gPTP Announce" and fa:
            gp[kind]["first_after_gm"] = fa["ptp"]["gm_id"]
            gp[kind]["first_after_prio1"] = fa["ptp"]["gm_prio1"]
            gp[kind]["first_after_path"] = fa["ptp"]["tlvs"]
    anns = [r for r in sw if r["kind"] == "gPTP Announce" and r["local"] > t_off + 1.0][:3]
    gp["gPTP Announce"]["first_three_after"] = [rel(r["local"]) for r in anns]
    res["tap"]["switch_gptp"] = gp
    print(f"   tap far end (switch side): last frame {res['tap']['last_far_end_frame']} s "
          f"({res['tap']['last_far_end_kind']}), first frame after {res['tap']['first_far_end_frame_after']} s "
          f"({res['tap']['first_far_end_kind']})")
    for k, v in gp.items():
        print(f"      {k:18s} last before {v['last_before']}  first after {v['first_after']}"
              + (f" gm {v.get('first_after_gm')} prio1 {v.get('first_after_prio1')} tlvs {v.get('first_after_path')}"
                 if "first_after_gm" in v else ""))
    # what the DUT sent on the wire, per phase
    t_ret = min(x for x in (gp["gPTP Announce"]["first_after"], gp["gPTP Sync"]["first_after"]) if x is not None) \
        if any(gp[k]["first_after"] is not None for k in ("gPTP Announce", "gPTP Sync")) else None
    res["t_return"] = t_ret
    phases = (("before off", -1e9, 0.0),
              ("off to first far-end frame", 0.0, res["tap"]["first_far_end_frame_after"] or 1e9),
              ("far-end link to switch Announce/Sync", res["tap"]["first_far_end_frame_after"] or 1e9, t_ret or 1e9),
              ("after switch Announce/Sync", t_ret or 1e9, 1e9))
    res["dut_wire"] = {}
    for name, a, b in phases:
        sel = [r for r in dut if a <= rel(r["local"]) < b]
        kinds = Counter(r["kind"] for r in sel)
        ann = [r for r in sel if r["kind"] == "gPTP Announce"]
        adpd = [r for r in sel if r["kind"] == "ADP"]
        info = dict(kinds=dict(kinds))
        if ann:
            info["announce_gm"] = dict(Counter(r["ptp"]["gm_id"] for r in ann))
            info["announce_first_last"] = (rel(ann[0]["local"]), rel(ann[-1]["local"]))
            info["announce_prio1"] = sorted({r["ptp"]["gm_prio1"] for r in ann})
        syn = [r for r in sel if r["kind"] == "gPTP Sync"]
        if syn:
            info["sync_first_last"] = (rel(syn[0]["local"]), rel(syn[-1]["local"]))
        if adpd:
            info["adp_gm"] = dict(Counter(r["adp"]["gm_id"] for r in adpd))
        res["dut_wire"][name] = info
        print(f"   DUT-sent frames, {name}: {info}")
    far_ann = [r for r in sw if r["kind"] == "gPTP Announce"]
    print(f"   far-end Announce GM identities over the capture: {dict(Counter(r['ptp']['gm_id'] for r in far_ann))}")
    # DUT ADP gm on the wire, transitions
    trans, prev = [], None
    for r in dut:
        if r["kind"] == "ADP":
            if r["adp"]["gm_id"] != prev:
                trans.append((rel(r["local"]), r["adp"]["gm_id"], r["adp"]["avail_index"]))
                prev = r["adp"]["gm_id"]
    res["dut_adp_wire_transitions"] = trans
    print(f"   DUT ADPDU gptp_grandmaster_id on the wire, transitions: {trans}")
    trans, prev = [], None
    for r in sw:
        if r["kind"] == "ADP" and r["adp"]["entity_id"] == PEER_EID and r["adp"]["interface_index"] == 0:
            if r["adp"]["gm_id"] != prev:
                trans.append((rel(r["local"]), r["adp"]["gm_id"], r["adp"]["avail_index"]))
                prev = r["adp"]["gm_id"]
    res["peer_adp_wire_transitions"] = trans
    print(f"   peer ADPDU (interface 0) gptp_grandmaster_id on the DUT link, transitions: {trans}")
    # CRF on the wire
    crf = [r for r in dut if r["kind"] == "CRF"]
    if crf:
        bursts, cur_b = [], None
        for r in crf:
            if cur_b and r["local"] - cur_b["end"] < 0.1:
                cur_b["end"] = r["local"]
                cur_b["n"] += 1
                cur_b["tu"][r["avtp"]["tu"]] += 1
            else:
                cur_b = dict(start=r["local"], end=r["local"], n=1, tu=[0, 0])
                cur_b["tu"][r["avtp"]["tu"]] += 1
                bursts.append(cur_b)
        res["crf_bursts"] = [(rel(b["start"]), rel(b["end"]), b["n"], b["tu"][0], b["tu"][1]) for b in bursts]
        tu_edges, prev = [], None
        for r in crf:
            if r["avtp"]["tu"] != prev:
                tu_edges.append((rel(r["local"]), r["avtp"]["tu"]))
                prev = r["avtp"]["tu"]
        res["crf_tu_edges"] = tu_edges
        print(f"   CRF bursts from the DUT (start, end, PDUs, tu=0, tu=1): {res['crf_bursts']}")
        print(f"   CRF tu edges on the wire: {tu_edges}")
    # during absence: console values
    t_first_far = res["tap"]["first_far_end_frame_after"]
    absent = [s for s in cs if 0 <= s["rel"] < (t_ret if t_ret is not None else 1e9)]
    res["console_absent"] = {k: dict(Counter(str(s.get(k)) for s in absent)) for k in
                             ("gm", "parent", "sync", "asc", "tu", "hold", "pc", "linkg")}
    print(f"   console values from T_off to the switch's first Announce/Sync: {res['console_absent']}")
    # recovery
    if t_ret is not None:
        post = [s for s in cs if s["rel"] >= t_ret]
        rec = None
        for i, s in enumerate(post):
            if good(s) and all(good(x) for x in post[i:]):
                rec = s
                break
        res["recovery"] = {}
        if rec is not None:
            i = cs.index(rec)
            res["recovery"]["all_good_first"] = rec["rel"]
            res["recovery"]["all_good_prev_sample"] = cs[i - 1]["rel"]
            res["recovery"]["from_first_announce_s"] = round(rec["rel"] - gp["gPTP Announce"]["first_after"], 3) \
                if gp["gPTP Announce"]["first_after"] is not None else None
            res["recovery"]["from_first_sync_s"] = round(rec["rel"] - gp["gPTP Sync"]["first_after"], 3) \
                if gp["gPTP Sync"]["first_after"] is not None else None
            res["recovery"]["from_return_s"] = round(rec["rel"] - t_ret, 3)
            res["recovery"]["from_first_far_end_frame_s"] = round(rec["rel"] - t_first_far, 3) if t_first_far else None
            res["recovery"]["from_on_cmd_s"] = round(rec["rel"] - rel(t_on), 3)
        for name, pred in (("asCapable_1", lambda s: s.get("asc") == "1"), ("sync_1", lambda s: s.get("sync") == "1"),
                           ("tu_0", lambda s: s.get("tu") == "0"), ("gm_switch", lambda s: s.get("gm") == SWITCH_GM),
                           ("holdover_seen", lambda s: s.get("hold") == 1)):
            f = first([s for s in cs if s["rel"] >= (t_first_far or t_ret)], pred)
            res["recovery"][name] = f["rel"] if f else None
        tu_post = [s for s in cs if s["rel"] >= 0]
        res["recovery"]["tucnt_start_end"] = (cs[0].get("tucnt"), cs[-1].get("tucnt"))
        res["recovery"]["pg_start_end"] = (cs[0].get("pg"), cs[-1].get("pg"))
        print(f"   recovery (s relative to T_off unless named): {res['recovery']}")
        _ = tu_post
    # PHC continuity: TAI step between successive samples vs build-box elapsed
    steps = []
    for a, b in zip(cs, cs[1:]):
        if "tai" in a and "tai" in b:
            dd = (b["tai"] - a["tai"]) / 1e9 - (b["t"] - a["t"])
            if abs(dd) > 0.05:
                steps.append((a["rel"], round(dd, 3)))
    res["phc_steps"] = steps
    print(f"   PHC steps seen by the console (> 50 ms against the build-box clock): {steps}")
    if jout:
        Path(jout).write_text(json.dumps(res, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
