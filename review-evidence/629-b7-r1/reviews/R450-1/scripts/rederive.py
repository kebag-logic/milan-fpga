#!/usr/bin/env python3
"""Re-derive the lane-B7 case figures of PR #644 from the published evidence packet.

Usage: rederive.py <packet-author-dir>
Reads only summary/<case>/{events,blocks}.csv, summary/<case>/grade.json (ratio,
window and counter fields), runs/<case>/dut-*.txt (raw console register dumps)
and runs/<case>/poll-*.jsonl (raw register words). Prints one JSON object.
"""
import csv, glob, json, os, re, statistics, sys

ROOT = sys.argv[1]
CASES = ["a0", "a1", "a2", "b0", "bcrf", "baaf"]
STATES = {0: "IDLE", 1: "VERIFY", 2: "REPAIR", 3: "ACQUIRE", 4: "LOCKED", 5: "HOLDOVER", 6: "FAULT"}


def s16(v):
    return v - 0x10000 if v & 0x8000 else v


def s32(v):
    return v - (1 << 32) if v & 0x80000000 else v


def dump_words(text):
    """Map address -> list of little-endian 32-bit words from every mem_read block."""
    out = {}
    for m in re.finditer(r"cmd='mem_read (0x[0-9a-f]+) (\d+)'.*?Memory dump:\n(.*?)\n\S*litex", text, re.S):
        base, n = int(m.group(1), 16), int(m.group(2))
        by = []
        for ln in m.group(3).splitlines():
            mm = re.match(r"0x[0-9a-f]+\s+((?:[0-9a-f]{2} )+)", ln)
            if mm:
                by += [int(x, 16) for x in mm.group(1).split()]
        by = by[:n]
        for i in range(0, n, 4):
            out[base + i] = int.from_bytes(bytes(by[i:i + 4]), "little")
    return out


def decode(w):
    st = w[0x900008F8]
    am = w[0x900008E0]
    return dict(
        servo=STATES.get(st & 7, st & 7), drp_mismatch=bool(st >> 4 & 1), trim_ppm=s16(st >> 16) / 16,
        meter_locked=bool(am & 1), meter_valid=bool(am >> 1 & 1), meter_enabled=bool(am >> 2 & 1),
        meter_restarts=am >> 8 & 0xFF, meter_maxdev_ns=am >> 16, meter_rate_ppm=s32(w[0x900008E4]) / 512,
        crf_locked=bool(w[0x90000738] >> 31), crf_rate_ppm=s32(w[0x90000748]) / 512,
        slip_lb_dups=w[0x900008D4] & 0xFFFF, slip_lb_skips=w[0x900008D4] >> 16,
        slip_tdm_dups=w[0x900008D8] & 0xFFFF, slip_tdm_skips=w[0x900008D8] >> 16)


NAMES = {0x0024: ["LOCKED", "UNLOCKED"],
         0x0006: ["STREAM_START", "STREAM_STOP", "MEDIA_RESET", "TIMESTAMP_UNCERTAIN", "FRAMES_TX"],
         0x0005: ["MEDIA_LOCKED", "MEDIA_UNLOCKED", "STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH", "MEDIA_RESET",
                  "TIMESTAMP_UNCERTAIN", "TIMESTAMP_VALID", "TIMESTAMP_NOT_VALID", "UNSUPPORTED_FORMAT",
                  "LATE_TIMESTAMP", "EARLY_TIMESTAMP", "FRAMES_RX"]}


def counters(hexpayload):
    """Decode a GET_COUNTERS payload: type, index, counters_valid, 32 quadlets (IEEE 1722.1-2021 7.4.42)."""
    if not all(ch in "0123456789abcdef" for ch in hexpayload):
        return hexpayload
    b = bytes.fromhex(hexpayload)
    dt = int.from_bytes(b[0:2], "big")
    valid = int.from_bytes(b[4:8], "big")
    q = [int.from_bytes(b[8 + 4 * i:12 + 4 * i], "big") for i in range(32)]
    return {n: q[i] for i, n in enumerate(NAMES.get(dt, [])) if valid >> i & 1}


def case(c):
    r = {}
    d = os.path.join(ROOT, "runs", c)
    wins = sorted(glob.glob(os.path.join(d, "dut-window-*.txt")), key=lambda p: int(re.findall(r"(\d+)\.txt", p)[0]))
    rows = [decode(dump_words(open(p).read())) for p in wins]
    r["dut_reads"] = len(rows)
    r["servo_states"] = sorted(set(x["servo"] for x in rows))
    r["trim_ppm"] = [min(x["trim_ppm"] for x in rows), max(x["trim_ppm"] for x in rows)]
    r["drp_mismatch_any"] = any(x["drp_mismatch"] for x in rows)
    r["meter_enabled_any"] = any(x["meter_enabled"] for x in rows)
    if r["meter_enabled_any"]:
        r["meter_locked_all"] = all(x["meter_locked"] for x in rows)
        r["meter_valid_all"] = all(x["meter_valid"] for x in rows)
        r["meter_restarts"] = [rows[0]["meter_restarts"], rows[-1]["meter_restarts"]]
        r["meter_maxdev_ns"] = max(x["meter_maxdev_ns"] for x in rows)
        r["meter_rate_ppm"] = [min(x["meter_rate_ppm"] for x in rows), max(x["meter_rate_ppm"] for x in rows)]
    lk = [x for x in rows if x["crf_locked"]]
    r["crf_locked_reads"] = len(lk)
    if lk:
        r["crf_rate_ppm"] = [min(x["crf_rate_ppm"] for x in lk), max(x["crf_rate_ppm"] for x in lk)]
    r["slip_tdm_first_last"] = [(rows[0]["slip_tdm_dups"], rows[0]["slip_tdm_skips"]), (rows[-1]["slip_tdm_dups"], rows[-1]["slip_tdm_skips"])]
    r["slip_lb_first_last"] = [(rows[0]["slip_lb_dups"], rows[0]["slip_lb_skips"]), (rows[-1]["slip_lb_dups"], rows[-1]["slip_lb_skips"])]
    s = os.path.join(ROOT, "summary", c)
    ev = list(csv.DictReader(open(os.path.join(s, "events.csv"))))
    lis = [e for e in ev if e["cause"] == "listener"]
    cap = [e for e in ev if e["cause"] == "capture path"]
    beat = [e for e in ev if e["cause"] not in ("listener", "capture path")]
    r["listener"] = dict(drops=sum(1 for e in lis if e["kind"] == "skip"), inserts=sum(1 for e in lis if e["kind"] == "insert"),
                         repeats=sum(1 for e in lis if e["kind"] == "repeat"),
                         sizes=sorted(set(int(e["frames"]) for e in lis)), net_step=sum(int(e["step"]) for e in lis))
    r["dut_beat_events"] = len(beat)
    clusters = {}
    for e in cap:
        clusters.setdefault(int(e["cluster"]), []).append(int(e["step"]))
    r["capture_events"] = len(cap)
    r["capture_clusters"] = len(clusters)
    off = []
    for k, steps in sorted(clusters.items()):
        bad = [st for st in steps if st % 48 != 12]
        if bad:
            off.append(dict(cluster=k, steps=steps, net=sum(steps), net_mod48=sum(steps) % 48,
                            expected_mod48=(12 * len(steps)) % 48,
                            frames_off=((sum(steps) - 12 * len(steps) + 24) % 48) - 24))
    r["clusters_with_off_signature_step"] = off
    g = json.load(open(os.path.join(s, "grade.json")))
    win = g["window"]
    r["window_s"], r["window_frames"] = win["seconds"], win["frames"]
    non_cap = sum(int(e["step"]) for e in ev if e["cause"] != "capture path")
    r["counted_ratio_ppm_rederived"] = round(non_cap / g["frame_rate_ratio"]["counted"]["observed_frames"] * 1e6, 4)
    r["counted_ratio_ppm_grade"] = g["frame_rate_ratio"]["counted"]["ppm"]
    r["observed_frames"] = g["frame_rate_ratio"]["counted"]["observed_frames"]
    r["capture_lost_frames_grade"] = g["frame_rate_ratio"]["counted"]["capture_lost_frames"]
    m = g["frame_rate_ratio"]["mcasp_capture"]
    r["timed_ratio_ppm"] = [round(m["ratio_ppm"], 2), round(m["ratio_ppm_halfwidth95"], 2), round(m["ratio_ppm_first_half"], 2), round(m["ratio_ppm_second_half"], 2)]
    r["external_capture_rate"] = g["frame_rate_ratio"]["external_capture"]["rate"]
    r["external_capture_deficit_fps"] = round(48000 - g["frame_rate_ratio"]["external_capture"]["rate"], 3)
    r["capture_reads"] = g["capture_reads"]["records"]
    r["read_stalls"] = g["capture_reads"]["stalls"]
    r["read_gap_max_ms"] = g["capture_reads"]["read_gap_ms_max"]
    bl = list(csv.DictReader(open(os.path.join(s, "blocks.csv"))))
    clean = [b for b in bl if int(b["events"]) == 0 and int(b["invalid"]) == 0]
    r["blocks"], r["clean_blocks"] = len(bl), len(clean)
    r["blocks_with_listener_event"] = sum(1 for b in bl if int(b["listener"]) > 0)
    for t in ("997", "9973"):
        th = [float(b["thdn_db_" + t]) for b in clean]
        r["clean_thdn_" + t] = [min(th), max(th)] if th else None
        pp = [abs(float(b["ppm_" + t])) for b in clean]
        r["clean_ppm_maxabs_" + t] = max(pp) if pp else None
        r["worst_thdn_all_" + t] = max(float(b["thdn_db_" + t]) for b in bl)
    lb = [b for b in bl if int(b["listener"]) > 0]
    r["worst_thdn_listener_block"] = [max(float(b["thdn_db_997"]) for b in lb), max(float(b["thdn_db_9973"]) for b in lb)] if lb else None
    r["clean_thdn_median"] = [statistics.median(float(b["thdn_db_997"]) for b in clean), statistics.median(float(b["thdn_db_9973"]) for b in clean)]
    r["clean_snr"] = [min(float(b["snr_db_997"]) for b in clean), min(float(b["snr_db_9973"]) for b in clean)]
    r["blocks_capture_path_only_positive_thdn"] = all(int(b["capture_path"]) > 0 for b in bl if max(float(b["thdn_db_997"]), float(b["thdn_db_9973"])) > 0)
    r["torn"] = g["tone"]["torn"]
    r["invalid"] = g["tone"]["invalid"]
    r["slip_tdm_window_grade"] = g["slip_tdm_window"]
    r["counters_marks"] = {}
    for pf in sorted(glob.glob(os.path.join(d, "poll-*.jsonl"))):
        polls = [json.loads(l) for l in open(pf)]
        seq = []
        for p in polls:
            w = {k: int(v, 16) for k, v in p["words"].items()}
            seq.append(dict(n=p["n"], t0=p["t0"], t1=p["t1"], servo=STATES[w["0x8f8"] & 7], trim=s16(w["0x8f8"] >> 16) / 16,
                            mlock=bool(w["0x8e0"] & 1), mvalid=bool(w["0x8e0"] >> 1 & 1), restarts=w["0x8e0"] >> 8 & 0xFF))
        r["poll_" + os.path.basename(pf)[5:-6]] = seq
    for l in open(os.path.join(d, "events.jsonl")):
        e = json.loads(l)
        if e["kind"] == "set-clock" and e.get("tag") == "case":
            r["set_event_t"] = e["t"]
            r["set_clock"] = dict(who=e["who"], src=e["src"], status=e["status"], readback=e["readback"])
        if e["kind"] == "unbind" and e["listener"] == "dut-in-0" and "window_start_t" in r and "ll_unbind_t" not in r:
            r["ll_unbind_t"] = e["t"]
        if e["kind"] == "bind" and e["listener"] == "dut-in-0" and "ll_unbind_t" in r and "ll_rebind_t" not in r:
            r["ll_rebind_t"] = e["t"]
        if e["kind"] == "counters":
            r["counters_marks"][e["tag"]] = {k: counters(v) for k, v in e["payloads"].items()}
        if e["kind"] == "window-start":
            r["window_start_t"] = e["t"]
    return r


out = {c: case(c) for c in CASES}
# set-to-LOCKED and lock-loss timing from the raw poll words
for c in ("bcrf", "baaf"):
    r = out[c]
    t = r["set_event_t"]
    seq = r["poll_lock-wait"]
    first = next(i for i, x in enumerate(seq) if x["servo"] == "LOCKED")
    r["set_to_locked_s"] = [round(seq[first - 1]["t1"] - t, 3), round(seq[first]["t1"] - t, 3)]
    def first_true(pred):
        i = next((i for i, x in enumerate(seq) if pred(x)), None)
        return None if i is None else [round(seq[i - 1]["t1"] - t, 3) if i else None, round(seq[i]["t1"] - t, 3)]
    r["set_to_meter_locked_s"] = first_true(lambda x: x["mlock"])
    r["set_to_meter_valid_s"] = first_true(lambda x: x["mvalid"])
    r["set_to_acquire_s"] = first_true(lambda x: x["servo"] in ("ACQUIRE", "LOCKED"))
r = out["baaf"]
def rel(seq, t, pred):
    i = next((i for i, x in enumerate(seq) if x["t1"] > t and pred(x)), None)
    prev = max((x["t1"] for x in seq[:i] if True), default=None) if i else None
    return None if i is None else [round(seq[i - 1]["t1"] - t, 3) if i and seq[i - 1]["t1"] > t else None, round(seq[i]["t1"] - t, 3)]
hold = r["poll_ll-holdover"]
ret = r["poll_ll-return"]
r["ll_held_s"] = round(r["ll_rebind_t"] - r["ll_unbind_t"], 2)
r["ll_unbind_to_holdover_s"] = rel(hold, r["ll_unbind_t"], lambda x: x["servo"] == "HOLDOVER")
r["ll_holdover_states"] = sorted(set(x["servo"] for x in hold if x["t1"] > r["ll_unbind_t"]))
r["ll_holdover_trims"] = sorted(set(x["trim"] for x in hold))
r["ll_rebind_to_meter_locked_s"] = rel(ret, r["ll_rebind_t"], lambda x: x["mlock"])
r["ll_rebind_to_meter_valid_s"] = rel(ret, r["ll_rebind_t"], lambda x: x["mvalid"])
r["ll_rebind_to_locked_s"] = rel(ret, r["ll_rebind_t"], lambda x: x["servo"] == "LOCKED")
r["window_start_after_set_s"] = round(r["window_start_t"] - r["set_event_t"], 2)
out["bcrf"]["window_start_after_set_s"] = round(out["bcrf"]["window_start_t"] - out["bcrf"]["set_event_t"], 2)
for c in out:
    for k in [k for k in out[c] if k.startswith("poll_")]:
        seq = out[c][k]
        out[c][k] = dict(n=len(seq), states=[(round(x["t1"] - seq[0]["t1"], 3), x["servo"], x["trim"], x["mlock"], x["mvalid"], x["restarts"]) for i, x in enumerate(seq) if i == 0 or (x["servo"], x["mlock"], x["mvalid"]) != (seq[i - 1]["servo"], seq[i - 1]["mlock"], seq[i - 1]["mvalid"])])
json.dump(out, sys.stdout, indent=1, default=str)
