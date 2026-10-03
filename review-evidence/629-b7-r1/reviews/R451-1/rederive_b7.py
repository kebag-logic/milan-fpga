#!/usr/bin/env python3
"""Independent re-derivation of the lane B7 bench figures from the published packet.

usage: rederive_b7.py <path to review-evidence/629-b7-r1/author>

Reads only the published run records (runs/<case>/events.jsonl, poll-*.jsonl) and the
grades (summary/<case>/grade.json, events.csv, blocks.csv). It decodes the raw DUT CSR
words itself from docs/reference/REGISTER_MAP.md's field layout (0x8F8, 0x8E0, 0x8E4,
0x738, 0x748, 0x8D4, 0x8D8) instead of using the grader's decode, recounts events and
blocks from the CSVs, and re-applies the 48 n + 12 signature test to every capture-path
cluster. Prints one JSON document. Read-only.
"""
import csv
import datetime
import json
import os
import statistics
import sys

ROOT = sys.argv[1]
CEST = datetime.timezone(datetime.timedelta(hours=2))
CASES = ["a0", "a1", "a2", "b0", "bcrf", "baaf"]
STATES = {0: "IDLE", 1: "VERIFY", 2: "REPAIR", 3: "ACQUIRE", 4: "LOCKED", 5: "HOLDOVER", 6: "FAULT"}


def s16(v):
    return v - 0x10000 if v & 0x8000 else v


def s32(v):
    return v - (1 << 32) if v & 0x80000000 else v


def dec(words):
    w = {k: int(v, 16) for k, v in words.items()}
    out = {}
    if "0x8f8" in w:
        v = w["0x8f8"]
        out["servo"] = STATES.get(v & 7, str(v & 7))
        out["drp_mismatch"] = bool(v & 0x10)
        out["trim_ppm"] = s16(v >> 16) / 16.0
    if "0x8e0" in w:
        v = w["0x8e0"]
        out["meter_locked"] = bool(v & 1)
        out["meter_valid"] = bool(v & 2)
        out["meter_enabled"] = bool(v & 4)
        out["meter_restarts"] = (v >> 8) & 0xFF
        out["meter_maxdev_ns"] = v >> 16
    if "0x8e4" in w:
        out["meter_rate_ppm"] = s32(w["0x8e4"]) / 512.0
    if "0x738" in w:
        out["crf_locked"] = bool(w["0x738"] >> 31)
    if "0x748" in w:
        out["crf_rate_ppm"] = s32(w["0x748"]) / 512.0
    if "0x8d4" in w:
        out["slip_lb_dups"] = w["0x8d4"] & 0xFFFF
        out["slip_lb_skips"] = w["0x8d4"] >> 16
    if "0x8d8" in w:
        out["slip_tdm_dups"] = w["0x8d8"] & 0xFFFF
        out["slip_tdm_skips"] = w["0x8d8"] >> 16
    return out


def cest(t):
    return datetime.datetime.fromtimestamp(t, CEST).strftime("%H:%M:%S")


def jl(p):
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else []


def poll_transitions(polls, t_ref):
    """(last non-target, first target) bracket for each state change, seconds after t_ref."""
    tr, prev = [], None
    for p in polls:
        st = dec(p["words"])
        key = (st.get("servo"), st.get("meter_locked"), st.get("meter_valid"))
        if key != prev:
            tr.append(dict(state=key, trim=st.get("trim_ppm"), from_s=None if prev is None else round(last - t_ref, 3),
                           to_s=round(p["t0"] - t_ref, 3)))
            prev = key
        last = p["t0"]
    return tr


res = {}
for c in CASES:
    ev = jl(f"{ROOT}/runs/{c}/events.jsonl")
    g = json.load(open(f"{ROOT}/summary/{c}/grade.json"))
    r = {}
    ws = [e for e in ev if e["kind"] == "window-start"][0]
    we = [e for e in ev if e["kind"] == "window-end"][0]
    r["window_start_cest"] = cest(ws["t"])
    r["window_wall_s"] = round(we["t"] - ws["t"], 2)
    r["window_frames"] = g["window"]["frames"]
    r["window_audio_s"] = round(g["window"]["frames"] / 48000, 2)
    r["sets"] = [dict(who=e["who"], src=e["src"], status=e["status"], readback=e["readback"], tag=e["tag"])
                 for e in ev if e["kind"] == "set-clock"]
    r["binds"] = [dict(t=e["talker"], l=e["listener"], st=e["status"], cc=e["conn_count"]) for e in ev if e["kind"] == "bind"]
    r["unbinds"] = [dict(t=e["talker"], l=e["listener"], st=e["status"], cc=e["conn_count"]) for e in ev if e["kind"] == "unbind"]
    r["format_checks"] = [dict(tag=e["tag"], talker=e["talker_fmt"], listener=e["listener_fmt"],
                               set=(e.get("set") or {}).get("fmt"), rb=e.get("listener_readback", e.get("readback")))
                          for e in ev if e["kind"] == "format-check"]
    r["restore"] = dict(clock_final=[(e["who"], e["source"], e["as_found"]) for e in ev if e["kind"] == "clock-final"],
                        format_final=[(e["key"], e["equal_to_found"]) for e in ev if e["kind"] == "format-final"],
                        rx_final=[(e["who"], e["idx"], e["conn_count"]) for e in ev if e["kind"] == "rx-final"],
                        map_final=[e["readback"] for e in ev if e["kind"] == "map-final"])
    # last bind or set before the window
    pre = [e["t"] for e in ev if e["kind"] in ("bind", "set-clock") and e["t"] < ws["t"]]
    r["window_after_last_bind_or_set_s"] = round(ws["t"] - max(pre), 2)
    # DUT reads, decoded here
    dr = [(e["tag"], dec(e["words"])) for e in ev if e["kind"] == "dut"]
    win = [d for t, d in dr if t.startswith("window-")]
    r["dut_window_reads"] = len(win)
    r["servo_states"] = sorted(set(d["servo"] for d in win))
    r["trim_min_max"] = [min(d["trim_ppm"] for d in win), max(d["trim_ppm"] for d in win)]
    r["drp_mismatch_any"] = any(d["drp_mismatch"] for d in win)
    r["meter_enabled_any"] = any(d["meter_enabled"] for d in win)
    r["meter_locked_valid_all"] = all(d["meter_locked"] and d["meter_valid"] for d in win)
    if r["meter_enabled_any"]:
        r["meter_rate_min_max"] = [min(d["meter_rate_ppm"] for d in win), max(d["meter_rate_ppm"] for d in win)]
        r["meter_restarts_first_last"] = [win[0]["meter_restarts"], win[-1]["meter_restarts"]]
        r["meter_maxdev_max"] = max(d["meter_maxdev_ns"] for d in win)
    r["crf_locked_all"] = all(d["crf_locked"] for d in win)
    lk = [d["crf_rate_ppm"] for d in win if d["crf_locked"]]
    r["crf_rate_when_locked_min_max"] = [min(lk), max(lk)] if lk else None
    r["slip_tdm_first_last"] = [(win[0]["slip_tdm_dups"], win[0]["slip_tdm_skips"]),
                                (win[-1]["slip_tdm_dups"], win[-1]["slip_tdm_skips"])]
    r["slip_lb_first_last"] = [win[0]["slip_lb_dups"], win[-1]["slip_lb_dups"]]
    r["slip_lb_series"] = [d["slip_lb_dups"] for d in win]
    r["dut_reads_meter_enabled_by_tag"] = {t: d.get("meter_enabled") for t, d in dr}
    # CLOCK_DOMAIN and AAF output counters at the marks
    # GET_COUNTERS payloads decoded here: type(2) index(2) valid(4) then 32 x u32
    NAMES = {0x24: ["LOCKED", "UNLOCKED"],
             0x06: ["STREAM_START", "STREAM_STOP", "MEDIA_RESET", "TIMESTAMP_UNCERTAIN", "FRAMES_TX"],
             0x05: ["MEDIA_LOCKED", "MEDIA_UNLOCKED", "STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH", "MEDIA_RESET",
                    "TIMESTAMP_UNCERTAIN", "TIMESTAMP_VALID", "TIMESTAMP_NOT_VALID", "UNSUPPORTED_FORMAT",
                    "LATE_TIMESTAMP", "EARLY_TIMESTAMP", "FRAMES_RX"]}

    def dcnt(h):
        try:
            b = bytes.fromhex(h)
        except ValueError:
            return {"unparsed": h[:40]}
        t = int.from_bytes(b[0:2], "big")
        vals = [int.from_bytes(b[8 + 4 * i:12 + 4 * i], "big") for i in range(len(NAMES.get(t, [])))]
        return dict(zip(NAMES.get(t, []), vals))
    cnt = {e["tag"]: {k: dcnt(v) for k, v in e["payloads"].items() if isinstance(v, str)} for e in ev if e["kind"] == "counters"}
    r["counter_marks"] = list(cnt)
    r["clock_domain"] = {k: (v["dut-0x0024-0"]["LOCKED"], v["dut-0x0024-0"]["UNLOCKED"]) for k, v in cnt.items() if "LOCKED" in v.get("dut-0x0024-0", {})}
    r["dut_aaf_out_media_reset"] = {k: v["dut-0x0006-0"]["MEDIA_RESET"] for k, v in cnt.items() if "dut-0x0006-0" in v}
    r["dut_crf_out_media_reset"] = {k: v["dut-0x0006-1"]["MEDIA_RESET"] for k, v in cnt.items() if "dut-0x0006-1" in v}
    r["peer_in0_media_reset"] = {k: v["peer-0x0005-0"]["MEDIA_RESET"] for k, v in cnt.items() if "peer-0x0005-0" in v}
    r["dut_in0_media_unlocked"] = {k: v["dut-0x0005-0"]["MEDIA_UNLOCKED"] for k, v in cnt.items() if "dut-0x0005-0" in v}
    # set to LOCKED from the raw console polls
    pl = jl(f"{ROOT}/runs/{c}/poll-lock-wait.jsonl")
    sets = [e for e in ev if e["kind"] == "set-clock" and e["tag"] == "case" and e["who"] == "dut"]
    if pl and sets:
        r["lock_wait_transitions"] = poll_transitions(pl, sets[0]["t"])
    # events.csv recount
    rows = list(csv.DictReader(open(f"{ROOT}/summary/{c}/events.csv")))
    causes = {}
    for x in rows:
        causes.setdefault(x["cause"], []).append(x)
    r["events_by_cause"] = {k: len(v) for k, v in causes.items()}
    lst = causes.get("listener", [])
    r["listener_kinds"] = {}
    for x in lst:
        k = f'{x["kind"]} {x["frames"]}'
        r["listener_kinds"][k] = r["listener_kinds"].get(k, 0) + 1
    net = sum(int(x["step"]) for x in rows if x["cause"] != "capture path")
    r["net_steps_non_capture_from_csv"] = net
    r["counted_ppm_recomputed"] = round(net / g["frame_rate_ratio"]["counted"]["observed_frames"] * 1e6, 3)
    r["counted_grade"] = g["frame_rate_ratio"]["counted"]
    # blocks.csv recount
    bl = list(csv.DictReader(open(f"{ROOT}/summary/{c}/blocks.csv")))
    clean = [b for b in bl if int(b["events"]) == 0 and int(b["invalid"]) == 0]
    r["blocks"] = len(bl)
    r["blocks_clean"] = len(clean)
    r["clean_thdn_997_minmax"] = [min(float(b["thdn_db_997"]) for b in clean), max(float(b["thdn_db_997"]) for b in clean)]
    r["clean_thdn_9973_minmax"] = [min(float(b["thdn_db_9973"]) for b in clean), max(float(b["thdn_db_9973"]) for b in clean)]
    r["clean_ppm_maxabs"] = max(max(abs(float(b["ppm_997"])), abs(float(b["ppm_9973"]))) for b in clean)
    r["worst_thdn_all"] = [max(float(b["thdn_db_997"]) for b in bl), max(float(b["thdn_db_9973"]) for b in bl)]
    lb = [b for b in bl if int(b["listener"]) > 0]
    r["worst_thdn_listener_blocks"] = [max(float(b["thdn_db_997"]) for b in lb), max(float(b["thdn_db_9973"]) for b in lb)] if lb else None
    r["blocks_with_capture_only"] = sum(1 for b in bl if int(b["capture_path"]) > 0 and int(b["listener"]) == 0)
    # capture-path clusters: signature and basis, re-applied
    cl = [x for x in g["skip_clusters"]]
    r["clusters"] = len(cl)
    r["clusters_not_capture"] = [x["cluster"] for x in cl if not x["capture_path"]]
    r["cluster_bases"] = sorted(set(x["basis"] for x in cl))
    r["lost_frames_total"] = sum(x["lost_frames"] for x in cl if x["capture_path"])
    bad_rise = [x["cluster"] for x in cl if abs(x["read_rise_ms"] - x["lost_ms"]) > 1.0 + 0.02 * x["lost_ms"]]
    r["clusters_rise_mismatch"] = bad_rise
    off = []
    for x in cl:
        nsk = max(1, sum(1 for s in x["steps"] if s > 0))
        resid = (x["lost_frames"] - 12 * nsk) % 48
        if resid:
            off.append(dict(cluster=x["cluster"], lost=x["lost_frames"], lost_ms=x["lost_ms"], steps=x["steps"],
                            resid_mod48=resid, short_by=48 - resid if resid > 24 else None, long_by=resid if resid <= 24 else None,
                            rise_ms=x["read_rise_ms"]))
    r["clusters_off_signature"] = off
    r["smallest_capture_loss"] = min(x["lost_frames"] for x in cl if x["capture_path"])
    small = [x for x in cl if x["capture_path"] and x["lost_frames"] < 98]
    r["clusters_under_98"] = dict(n=len(small), rise=[min(x["read_rise_ms"] for x in small), max(x["read_rise_ms"] for x in small)] if small else None,
                                  gap_min=min(x["recent_read_gap_ms"] for x in small) if small else None)
    cr = g["capture_reads"]
    r["capture_reads"] = dict(records=cr["records"], stalls=cr["stalls"], stalls_over_15=sum(1 for s in cr["stall_gaps_ms"] if s > 15),
                              max_gap_ms=cr["read_gap_ms_max"])
    mc = g["frame_rate_ratio"]["mcasp_capture"]
    r["timed"] = dict(ppm=round(mc["ratio_ppm"], 2), hw=round(mc["ratio_ppm_halfwidth95"], 2),
                      halves=[round(mc["ratio_ppm_first_half"], 2), round(mc["ratio_ppm_second_half"], 2)],
                      holds_zero=abs(mc["ratio_ppm"]) <= mc["ratio_ppm_halfwidth95"])
    ext = g["frame_rate_ratio"]["external_capture"]
    r["external_capture_rate_hz"] = round(ext["rate"], 3)
    r["capture_deficit_frames_per_s"] = round(48000 - ext["rate"], 3)
    res[c] = r

# lock loss, from the raw polls of the B-AAF run
ev = jl(f"{ROOT}/runs/baaf/events.jsonl")
ub = [e for e in ev if e["kind"] == "unbind" and e["listener"] == "dut-in-0"][0]
rb = [e for e in ev if e["kind"] == "bind" and e["listener"] == "dut-in-0"][-1]
ll = dict(held_s=round(rb["t"] - ub["t"], 2), unbind=dict(st=ub["status"], cc=ub["conn_count"]), rebind=dict(st=rb["status"], cc=rb["conn_count"]))
ll["holdover_transitions"] = poll_transitions(jl(f"{ROOT}/runs/baaf/poll-ll-holdover.jsonl"), ub["t"])
ll["return_transitions"] = poll_transitions(jl(f"{ROOT}/runs/baaf/poll-ll-return.jsonl") + jl(f"{ROOT}/runs/baaf/poll-ll-after.jsonl"), rb["t"])
ll["holdover_trims"] = sorted(set(dec(p["words"])["trim_ppm"] for p in jl(f"{ROOT}/runs/baaf/poll-ll-holdover.jsonl")
                                   if dec(p["words"])["servo"] == "HOLDOVER"))
ll["states_in_holdover_poll_after_unbind"] = sorted(set(dec(p["words"])["servo"] for p in jl(f"{ROOT}/runs/baaf/poll-ll-holdover.jsonl") if p["t0"] > ub["t"] + 0.6))
ll["clock_source"] = [(e["tag"], e["source"]) for e in ev if e["kind"] == "ll-clock"]
g = json.load(open(f"{ROOT}/summary/baaf-lockloss/grade.json"))
ll["tone_segment"] = dict(frames=g["window"]["frames"], s=g["window"]["seconds"], events=g["tone"]["events"], invalid=g["tone"]["invalid"],
                          capture_lost=g["frame_rate_ratio"]["counted"]["capture_lost_frames"], net=g["frame_rate_ratio"]["counted"]["steps_non_capture"])
res["lockloss"] = ll
print(json.dumps(res, indent=1, default=str))
