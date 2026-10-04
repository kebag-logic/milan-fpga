"""Lane B7 decoders for grade_b7.py: the DUT's servo and AAF meter words, the set-to-LOCKED
timing, GET_COUNTERS payloads and the B-AAF lock-loss observation. Read-only analysis of
files run_b7.py wrote; nothing here touches the bench.

Word layouts (docs/reference/REGISTER_MAP.md at dev bbf704ec):
  MCSRV_STAT 0x8F8: [2:0] state (0 IDLE, 1 VERIFY, 2 REPAIR, 3 ACQUIRE, 4 LOCKED, 5 HOLDOVER,
                    6 FAULT), [3] DRP config verified, [4] DRP config mismatch, [5] MMCM
                    locked, [15:10] discarded rate windows, [31:16] signed trim, 1/16 ppm
  AAFM_STAT  0x8E0: [0] locked, [1] rate valid, [2] enabled, [7:4] followed listener,
                    [15:8] data-caused history restarts, [31:16] largest deviation, ns
  AAFM_RATE  0x8E4: signed ns per 512 ms, 1 ppm = 512 units (as CRF_RATE 0x748)
  CRF_CTRL   0x738: [31] locked
  SLIP_LB    0x8D4: [15:0] loopback-ring dups, [31:16] skips
  SLIP_TDM   0x8D8: [15:0] TDM-junction dups, [31:16] skips
GET_COUNTERS (protocol-processor 06_aecp_engine.md, F06.15): counters_valid mask bit k is the
quadlet at counters_block offset 4 k. STREAM_INPUT k = 0 MEDIA_LOCKED, 1 MEDIA_UNLOCKED,
2 STREAM_INTERRUPTED, 3 SEQ_NUM_MISMATCH, 4 MEDIA_RESET, 5 TIMESTAMP_UNCERTAIN,
6 TIMESTAMP_VALID, 7 TIMESTAMP_NOT_VALID (IEEE 1722.1-2021 Table 7-157), 8 UNSUPPORTED_FORMAT, 9 LATE_TIMESTAMP, 10 EARLY_TIMESTAMP, 11 FRAMES_RX; STREAM_OUTPUT
(Milan Table 5.17) 0 STREAM_START, 1 STREAM_STOP, 2 MEDIA_RESET, 3 TIMESTAMP_UNCERTAIN,
4 FRAMES_TX; CLOCK_DOMAIN 0 LOCKED, 1 UNLOCKED; AVB_INTERFACE 0 LINK_UP, 1 LINK_DOWN,
5 GPTP_GM_CHANGED.
"""
import json
from pathlib import Path

import numpy as np

STATES = {0: "IDLE", 1: "VERIFY", 2: "REPAIR", 3: "ACQUIRE", 4: "LOCKED", 5: "HOLDOVER", 6: "FAULT"}
CTR_NAMES = {
    0x0005: {0: "MEDIA_LOCKED", 1: "MEDIA_UNLOCKED", 2: "STREAM_INTERRUPTED", 3: "SEQ_NUM_MISMATCH",
             4: "MEDIA_RESET", 5: "TIMESTAMP_UNCERTAIN", 6: "TIMESTAMP_VALID", 7: "TIMESTAMP_NOT_VALID",
             8: "UNSUPPORTED_FORMAT", 9: "LATE_TIMESTAMP", 10: "EARLY_TIMESTAMP", 11: "FRAMES_RX"},
    0x0006: {0: "STREAM_START", 1: "STREAM_STOP", 2: "MEDIA_RESET", 3: "TIMESTAMP_UNCERTAIN", 4: "FRAMES_TX"},
    0x0024: {0: "LOCKED", 1: "UNLOCKED"},
    0x0009: {0: "LINK_UP", 1: "LINK_DOWN", 5: "GPTP_GM_CHANGED"},
}


def s16(x):
    return x - (1 << 16) if x >= 1 << 15 else x


def s32(x):
    return x - (1 << 32) if x >= 1 << 31 else x


def servo(word):
    w = int(word, 16)
    return dict(state=STATES.get(w & 7, w & 7), verified=bool(w >> 3 & 1), drp_mismatch=bool(w >> 4 & 1),
                mmcm_locked=bool(w >> 5 & 1), discarded=w >> 10 & 63, trim_ppm=s16(w >> 16) / 16)


def meter(stat, rate):
    w = int(stat, 16)
    return dict(locked=bool(w & 1), rate_valid=bool(w >> 1 & 1), enabled=bool(w >> 2 & 1),
                listener=w >> 4 & 15, restarts=w >> 8 & 255, max_dev_ns=w >> 16,
                rate_ppm=s32(int(rate, 16)) / 512 if rate else None)


def word_row(t, words):
    r = dict(t=t)
    if words.get("0x8f8"):
        r["servo"] = servo(words["0x8f8"])
    if words.get("0x8e0"):
        r["meter"] = meter(words["0x8e0"], words.get("0x8e4"))
    if words.get("0x738"):
        r["crf_locked"] = bool(int(words["0x738"], 16) >> 31)
    if words.get("0x748"):
        r["crf_rate_ppm"] = s32(int(words["0x748"], 16)) / 512
    if words.get("0x8d8"):
        w = int(words["0x8d8"], 16)
        r["slip_tdm_dups"], r["slip_tdm_skips"] = w & 0xFFFF, w >> 16
    if words.get("0x8d4"):
        w = int(words["0x8d4"], 16)
        r["slip_lb_dups"], r["slip_lb_skips"] = w & 0xFFFF, w >> 16
    return r


def servo_window(wreads):
    rows = [word_row(e["t"], e["words"]) for e in wreads]
    out = dict(reads=len(rows), rows=rows)
    if rows:
        sv = [r["servo"]["state"] for r in rows if "servo" in r]
        out["servo_states"] = sorted(set(sv))
        out["servo_locked_at_every_read"] = bool(sv) and all(s == "LOCKED" for s in sv)
        tr = [r["servo"]["trim_ppm"] for r in rows if "servo" in r]
        out["trim_ppm_min_max"] = [min(tr), max(tr)] if tr else None
        mt = [r["meter"] for r in rows if "meter" in r]
        if mt:
            out["meter_locked_every_read"] = all(m["locked"] for m in mt)
            out["meter_rate_valid_every_read"] = all(m["rate_valid"] for m in mt)
            out["meter_restarts_first_last"] = [mt[0]["restarts"], mt[-1]["restarts"]]
            out["meter_max_dev_ns_last"] = mt[-1]["max_dev_ns"]
            rp = [m["rate_ppm"] for m in mt if m["rate_valid"]]
            out["meter_rate_ppm_min_max"] = [min(rp), max(rp)] if rp else None
        crf = [r["crf_rate_ppm"] for r in rows if r.get("crf_locked")]
        out["crf_rate_ppm_min_max_when_locked"] = [min(crf), max(crf)] if crf else None
        out["slip_tdm_dups_first_last"] = [rows[0].get("slip_tdm_dups"), rows[-1].get("slip_tdm_dups")]
        out["slip_tdm_skips_first_last"] = [rows[0].get("slip_tdm_skips"), rows[-1].get("slip_tdm_skips")]
        out["slip_lb_dups_first_last"] = [rows[0].get("slip_lb_dups"), rows[-1].get("slip_lb_dups")]
        out["slip_lb_skips_first_last"] = [rows[0].get("slip_lb_skips"), rows[-1].get("slip_lb_skips")]
    return out


def read_poll(path):
    if not Path(path).exists():
        return []
    return [json.loads(l) for l in open(path) if l.startswith("{")]


def transitions(polls, t0_raw):
    """First-seen times (s after t0_raw, as an interval from the previous poll's end to this
    poll's end) of each servo state and of the meter's lock and rate validity."""
    out = []
    prev_s = prev_m = None
    prev_end = None
    for p in polls:
        w = p["words"]
        s = servo(w["0x8f8"])["state"] if w.get("0x8f8") else None
        m = meter(w["0x8e0"], w.get("0x8e4")) if w.get("0x8e0") else None
        mk = (m["locked"], m["rate_valid"], m["restarts"]) if m else None
        if s != prev_s or mk != prev_m:
            out.append(dict(after_s_from=None if prev_end is None else round((prev_end - t0_raw) / 1e9, 3),
                            after_s_to=round((p["raw1"] - t0_raw) / 1e9, 3), servo=s,
                            trim_ppm=servo(w["0x8f8"])["trim_ppm"] if w.get("0x8f8") else None, meter=m))
            prev_s, prev_m = s, mk
        prev_end = p["raw1"]
    return out


def lock_timing(events, run_dir):
    sets = [e for e in events if e["kind"] == "set-clock" and e.get("tag") == "case"]
    polls = read_poll(Path(run_dir) / "poll-lock-wait.jsonl")
    if not sets or not polls:
        return None
    t0 = sets[0]["mono_raw_ns"]
    tr = transitions(polls, t0)
    first_locked = next((x for x in tr if x["servo"] == "LOCKED"), None)
    return dict(set_event_t=sets[0]["t"], polls=len(polls), poll_period_s=0.5,
                note="the set time is the set-clock event, logged after the SET_CLOCK_SOURCE answer and its read-back",
                transitions=tr,
                set_to_locked_s=[first_locked["after_s_from"], first_locked["after_s_to"]] if first_locked else None)


def decode_counters(payload):
    if not isinstance(payload, str) or len(payload) < 16 + 256:
        return payload
    dt, idx = int(payload[0:4], 16), int(payload[4:8], 16)
    valid = int(payload[8:16], 16)
    names = CTR_NAMES.get(dt, {})
    vals = {}
    for k in range(32):
        if valid >> k & 1:
            vals[names.get(k, f"k{k}")] = int(payload[16 + 8 * k:24 + 8 * k], 16)
    return dict(valid=f"{valid:#010x}", counters=vals)


def counters(events):
    return {e["tag"]: {k: decode_counters(v) for k, v in e["payloads"].items()}
            for e in events if e["kind"] == "counters"}


def lock_loss(events, run_dir, c0f, c1f, TF, TRAW, w1):
    import b6_thdn as A
    import b6_tone as T
    ev = {e["kind"]: e for e in events if e["kind"] in ("lockloss-begin", "ll-unbind", "ll-rebind", "lockloss-end")}
    if "ll-unbind" not in ev:
        return None
    t_unb = ev["ll-unbind"]["mono_raw_ns"]
    t_reb = ev.get("ll-rebind", {}).get("mono_raw_ns")
    hold = read_poll(Path(run_dir) / "poll-ll-holdover.jsonl")
    ret = read_poll(Path(run_dir) / "poll-ll-return.jsonl")
    after = read_poll(Path(run_dir) / "poll-ll-after.jsonl")
    out = dict(holdover_transitions=transitions(hold, t_unb),
               return_transitions=transitions(ret + after, t_reb) if t_reb else None,
               clock_source=[dict(tag=e["tag"], source=e["source"]) for e in events if e["kind"] == "ll-clock"],
               unbind=[dict(status=e.get("status"), conn_count=e.get("conn_count")) for e in events
                       if e["kind"] == "unbind" and e.get("talker") == "peer-out-0" and e["t"] < ev["ll-unbind"]["t"] + 10],
               rebind=[dict(status=e.get("status"), conn_count=e.get("conn_count")) for e in events
                       if e["kind"] == "bind" and e.get("talker") == "peer-out-0" and t_reb and e["mono_raw_ns"] >= t_reb])
    # the tone path from the window's end to the observation's end (the capture kept running)
    a = int(w1)
    z = int(min(ev.get("lockloss-end", {}).get("frame", len(c0f)), len(c0f)))
    if z - a > 48000:
        ordn = T.decode(c0f[a:z], c1f[a:z], T.table())
        st = A.steps(ordn)
        f_unb = ev["ll-unbind"]["frame"] - a
        f_reb = (ev["ll-rebind"]["frame"] - a) if "ll-rebind" in ev else None
        evs = []
        for e in st["events"]:
            j = int(np.searchsorted(TF, a + e["frame"], side="left"))
            gap = float((TRAW[j] - TRAW[j - 1]) / 1e6) if 0 < j < len(TRAW) else None
            evs.append(dict(frame=e["frame"], s_after_unbind=round((e["frame"] - f_unb) / 48000, 3), step=e["step"],
                            kind=e["kind"], invalid_between=e["invalid_between"],
                            read_gap_ms_at=round(gap, 3) if gap is not None else None))
        out["tone_path"] = dict(frames=z - a, seconds=round((z - a) / 48000, 3), unbind_at_s=round(f_unb / 48000, 3),
                                rebind_at_s=round(f_reb / 48000, 3) if f_reb is not None else None,
                                invalid=st["invalid"], events=evs)
    return out
