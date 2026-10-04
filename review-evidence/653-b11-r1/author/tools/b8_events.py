#!/usr/bin/env python3
"""Lane B8: the switch, lock-loss and power-cycle observations from run_b8.py's and pc_b8.py's
records, read-only analysis; nothing here touches the bench.

usage: b8_events.py <packet_dir> <raw_root>

Reads runs/{sw,crfll,pc}/events.jsonl in the packet, and from <raw_root>/<run>/ the console
poll (poll-run.jsonl), the full grades (grade-full.json, grade-lockloss-full.json) and the boot
record (pc/boot-console.jsonl). Writes:
  summary/sw/switches.json       per clock-source set: the set's answer and read-back, every
                                 change the poll saw from 2 s before the set to the next set
                                 (servo state and trim, AAF meter, CRF sink lock, SLIP_LB,
                                 SLIP_TDM, RENDER_STAT's prefill, converged and rail count),
                                 the GET_COUNTERS marks decoded, GET_CLOCK_SOURCE at each read,
                                 and the tone-path discontinuities by phase;
  summary/crfll/lockloss.json    the same around the unbind and the rebind of the CRF talker;
  summary/pc/pc.json             the power cycle: the NVM reads, the clock source, RX state and
                                 counters before and after, the boot record's milestones;
  summary/<run>/grade*.json      each full grade without its per-block and per-event lists;
  summary/tables.md              the tables the findings page carries.
Times are seconds on this host's CLOCK_MONOTONIC_RAW after the named event; a poll interval
(lo, hi) runs from the end of the poll before the change to the end of the poll that saw it.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b7_decode as X  # noqa: E402

pkt, raw = Path(sys.argv[1]), Path(sys.argv[2])
STATES = X.STATES


def load(p):
    return [json.loads(l) for l in open(p) if l.startswith("{")]


def dec(w):
    """One poll's words, decoded; None when a word is missing."""
    try:
        sv = X.servo(w["0x8f8"])
        m = X.meter(w["0x8e0"], w["0x8e4"])
        lb, td, rs = int(w["0x8d4"], 16), int(w["0x8d8"], 16), int(w["0x8dc"], 16)
        crf = int(w["0x738"], 16) >> 31
        rate = X.s32(int(w["0x748"], 16)) / 512
    except (KeyError, TypeError, ValueError):
        return None
    return dict(servo=sv["state"], trim_ppm=sv["trim_ppm"], meter_locked=m["locked"], meter_rate_valid=m["rate_valid"],
                meter_enabled=m["enabled"], meter_restarts=m["restarts"], meter_max_dev_ns=m["max_dev_ns"],
                meter_rate_ppm=m["rate_ppm"] if m["rate_valid"] else None, crf_locked=bool(crf),
                crf_rate_ppm=rate if crf else None, slip_lb=[lb & 0xFFFF, lb >> 16], slip_tdm=[td & 0xFFFF, td >> 16],
                render_fill=rs & 0xFF, render_prefill=rs >> 8 & 1, render_converged=rs >> 9 & 1, render_rails=rs >> 16)


KEYS = ("servo", "meter_locked", "meter_rate_valid", "meter_enabled", "meter_restarts", "crf_locked", "slip_lb",
        "slip_tdm", "render_prefill", "render_converged", "render_rails")


def changes(polls, t0, t_from, t_to):
    """Every change of KEYS in polls between raw times t_from and t_to; times after t0."""
    out, prev, prev_end, bad = [], None, None, []
    for p in polls:
        if p["raw1"] < t_from or p["raw0"] > t_to:
            if p["raw1"] < t_from:
                d = dec(p["words"])
                if d is not None:
                    prev, prev_end = d, p["raw1"]
            continue
        d = dec(p["words"])
        if d is None:
            bad.append(p["n"])
            continue
        if prev is None or any(d[k] != prev[k] for k in KEYS):
            row = dict(s_lo=None if prev_end is None else round((prev_end - t0) / 1e9, 3), s_hi=round((p["raw1"] - t0) / 1e9, 3),
                       poll=p["n"])
            row.update({k: d[k] for k in KEYS if prev is None or d[k] != prev[k]})
            row["trim_ppm"] = d["trim_ppm"]
            out.append(row)
        prev, prev_end = d, p["raw1"]
    return out, bad


def at(polls, t):
    """The decoded words of the last good poll that ended at or before raw time t."""
    best = None
    for p in polls:
        if p["raw1"] <= t:
            d = dec(p["words"])
            if d is not None:
                best = d
    return best


def span_stats(polls, t_from, t_to):
    ds = [dec(p["words"]) for p in polls if t_from <= p["raw0"] and p["raw1"] <= t_to]
    ds = [d for d in ds if d is not None]
    if not ds:
        return None
    tr = [d["trim_ppm"] for d in ds]
    mr = [d["meter_rate_ppm"] for d in ds if d["meter_rate_ppm"] is not None]
    cr = [d["crf_rate_ppm"] for d in ds if d["crf_rate_ppm"] is not None]
    return dict(polls=len(ds), servo_states=sorted(set(d["servo"] for d in ds)),
                trim_ppm=[min(tr), max(tr)], meter_rate_ppm=[min(mr), max(mr)] if mr else None,
                crf_rate_ppm=[min(cr), max(cr)] if cr else None,
                slip_lb_first_last=[ds[0]["slip_lb"], ds[-1]["slip_lb"]],
                slip_tdm_first_last=[ds[0]["slip_tdm"], ds[-1]["slip_tdm"]],
                render_rails_first_last=[ds[0]["render_rails"], ds[-1]["render_rails"]],
                render_fill_min_max=[min(d["render_fill"] for d in ds), max(d["render_fill"] for d in ds)],
                meter_restarts_first_last=[ds[0]["meter_restarts"], ds[-1]["meter_restarts"]],
                meter_max_dev_ns_last=ds[-1]["meter_max_dev_ns"])


CNAMES = {"dut-0x0024-0": ("DUT CLOCK_DOMAIN 0", ("LOCKED", "UNLOCKED")),
          "dut-0x0006-0": ("DUT STREAM_OUTPUT 0 (AAF talker)", ("STREAM_START", "STREAM_STOP", "MEDIA_RESET")),
          "dut-0x0006-1": ("DUT STREAM_OUTPUT 1 (CRF talker)", ("STREAM_START", "STREAM_STOP", "MEDIA_RESET")),
          "peer-0x0005-0": ("Peer STREAM_INPUT 0 (the DUT's AAF as received)",
                            ("MEDIA_LOCKED", "MEDIA_UNLOCKED", "STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH", "MEDIA_RESET")),
          "dut-0x0005-0": ("DUT STREAM_INPUT 0 (AAF listener)",
                           ("MEDIA_LOCKED", "MEDIA_UNLOCKED", "STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH", "MEDIA_RESET",
                            "TIMESTAMP_UNCERTAIN", "LATE_TIMESTAMP", "EARLY_TIMESTAMP")),
          "dut-0x0005-1": ("DUT STREAM_INPUT 1 (CRF listener)",
                           ("MEDIA_LOCKED", "MEDIA_UNLOCKED", "STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH", "MEDIA_RESET",
                            "TIMESTAMP_UNCERTAIN", "LATE_TIMESTAMP", "EARLY_TIMESTAMP")),
          "peer-0x0006-0": ("Peer STREAM_OUTPUT 0 (AAF talker)", ("STREAM_START", "STREAM_STOP", "MEDIA_RESET"))}


def counter_table(events):
    out = {}
    for tag, d in X.counters(events).items():
        row = {}
        for k, v in d.items():
            if k in CNAMES and isinstance(v, dict):
                row[k] = {n: v["counters"].get(n) for n in CNAMES[k][1]}
            elif k in CNAMES:
                row[k] = v
        out[tag] = row
    return out


def tone_events(grade, marks):
    """The grade's discontinuities with the phase each falls in (marks: (name, capture frame))."""
    out = []
    for e in grade.get("events_list", []):
        f = e["capture_frame"]
        ph = None
        for nm, fr in marks:
            if fr is not None and f >= fr:
                ph = nm
        out.append(dict(capture_frame=f, step=e["step"], kind=e["kind"], cause=e["cause"], phase=ph))
    return out


def reduced(g):
    return {k: v for k, v in g.items() if k not in ("blocks_list", "events_list")}


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, default=float) + "\n")


summ = {}
# ---- item 2: the switch case ---------------------------------------------------------------
ev = load(pkt / "runs/sw/events.jsonl")
polls = load(raw / "sw/poll-run.jsonl")
g = json.load(open(raw / "sw/grade-full.json"))
write(pkt / "summary/sw/grade.json", reduced(g))
sw_ev = [e for e in ev if e["kind"] == "switch"]
sets = {e["tag"]: e for e in ev if e["kind"] == "set-clock"}
locks = {e["tag"]: e for e in ev if e["kind"] == "servo-state"}
binds_end = next(e for e in ev if e["kind"] == "binds-end")
restore = sets["restore"]
phases = []
bounds = [e["mono_raw_ns"] for e in sw_ev] + [restore["mono_raw_ns"]]
for k, e in enumerate(sw_ev):
    tag = e["tag"]
    t0, t1 = e["mono_raw_ns"], bounds[k + 1]
    ch, bad = changes(polls, t0, t0 - 2_000_000_000, t1)
    st = sets[tag]
    lk = locks.get(tag, {})
    t_lock = t0 + int((lk.get("s_hi") or 0) * 1e9)
    phases.append(dict(tag=tag, from_source=[0, 2, 1][k], to_source=e["src"], set_status=st["status"], readback=st["readback"],
                       set_answer_ms_after_switch=round((st["mono_raw_ns"] - t0) / 1e6, 3),
                       set_to_locked_s=[lk.get("s_lo"), lk.get("s_hi")],
                       clock_reads=[dict(tag=x["tag"], source=x["source"]) for x in ev
                                    if x["kind"] == "clock-read" and x["tag"].startswith(tag)],
                       before_set=at(polls, t0), after_lock=span_stats(polls, t_lock, t1), changes=ch, bad_polls=bad))
ct = counter_table(ev)
marks = [("binds", binds_end["frame"])] + [(e["tag"], e["frame"]) for e in sw_ev] + [("restore", None)]
sw_out = dict(case="SW", binds_end_s_before_first_set=round((sw_ev[0]["mono_raw_ns"] - binds_end["mono_raw_ns"]) / 1e9, 3),
              phases=phases, restore=dict(status=restore["status"], readback=restore["readback"],
                                          changes=changes(polls, restore["mono_raw_ns"], restore["mono_raw_ns"] - 1_000_000_000,
                                                          polls[-1]["raw1"])[0]),
              from_binds=changes(polls, binds_end["mono_raw_ns"], binds_end["mono_raw_ns"] - 3_000_000_000, sw_ev[0]["mono_raw_ns"])[0],
              counters=ct, tone_events=tone_events(g, marks),
              tone=dict(window=g["window"], tone=g["tone"], attribution=g["attribution"],
                        counted=g["frame_rate_ratio"]["counted"],
                        timed_ppm=g["frame_rate_ratio"]["mcasp_capture"].get("ratio_ppm"),
                        timed_halfwidth95_ppm=g["frame_rate_ratio"]["mcasp_capture"].get("ratio_ppm_halfwidth95"),
                        capture_reads=g["capture_reads"], clusters=g["skip_clusters"]),
              polls=len(polls), polls_missing_a_word=[p["n"] for p in polls if dec(p["words"]) is None])
write(pkt / "summary/sw/switches.json", sw_out)
summ["sw"] = sw_out

# ---- item 3: the CRF lock loss -------------------------------------------------------------
ev = load(pkt / "runs/crfll/events.jsonl")
polls = load(raw / "crfll/poll-run.jsonl")
g = json.load(open(raw / "crfll/grade-full.json"))
gl = json.load(open(raw / "crfll/grade-lockloss-full.json"))
write(pkt / "summary/crfll/grade.json", reduced(g))
write(pkt / "summary/crfll/grade-lockloss.json", reduced(gl))
E = {e["kind"]: e for e in ev if e["kind"] in ("switch", "window-start", "window-end", "lockloss-begin", "ll-unbind",
                                               "ll-rebind", "lockloss-end")}
st = next(e for e in ev if e["kind"] == "set-clock" and e["tag"] == "case")
lk = next(e for e in ev if e["kind"] == "servo-state" and e["tag"] == "crf")
t_unb, t_reb = E["ll-unbind"]["mono_raw_ns"], E["ll-rebind"]["mono_raw_ns"]
unb = next(e for e in ev if e["kind"] == "unbind" and e["mono_raw_ns"] >= t_unb)
reb = next(e for e in ev if e["kind"] == "bind" and e["mono_raw_ns"] >= t_reb)
ll = dict(case="CRFLL", set=dict(status=st["status"], readback=st["readback"], set_to_locked_s=[lk["s_lo"], lk["s_hi"]]),
          window=span_stats(polls, E["window-start"]["mono_raw_ns"], E["window-end"]["mono_raw_ns"]),
          window_clock_reads=[dict(tag=x["tag"], source=x["source"]) for x in ev
                              if x["kind"] == "clock-read" and x["tag"].startswith("window")],
          unbind=dict(status=unb["status"], conn_count=unb["conn_count"],
                      answer_ms_after_mark=round((unb["mono_raw_ns"] - t_unb) / 1e6, 3)),
          rebind=dict(status=reb["status"], conn_count=reb["conn_count"],
                      answer_ms_after_mark=round((reb["mono_raw_ns"] - t_reb) / 1e6, 3)),
          held_s=round((t_reb - t_unb) / 1e9, 3),
          after_unbind=changes(polls, t_unb, t_unb - 2_000_000_000, t_reb)[0],
          after_rebind=changes(polls, t_reb, t_reb - 500_000_000, E["lockloss-end"]["mono_raw_ns"])[0],
          holdover=span_stats(polls, t_unb + 1_000_000_000, t_reb),
          servo_states=[{k: e.get(k) for k in ("tag", "state", "s_lo", "s_hi")} for e in ev if e["kind"] == "servo-state"],
          clock_reads=[dict(tag=x["tag"], source=x["source"]) for x in ev if x["kind"] == "clock-read"],
          counters=counter_table(ev),
          tone_window=dict(window=g["window"], tone=g["tone"], attribution=g["attribution"],
                           counted=g["frame_rate_ratio"]["counted"],
                           timed_ppm=g["frame_rate_ratio"]["mcasp_capture"].get("ratio_ppm"),
                           timed_halfwidth95_ppm=g["frame_rate_ratio"]["mcasp_capture"].get("ratio_ppm_halfwidth95"),
                           capture_reads=g["capture_reads"], clusters=g["skip_clusters"]),
          tone_lockloss=dict(window=gl["window"], tone=gl["tone"], attribution=gl["attribution"],
                             counted=gl["frame_rate_ratio"]["counted"]),
          polls=len(polls), polls_missing_a_word=[p["n"] for p in polls if dec(p["words"]) is None])
write(pkt / "summary/crfll/lockloss.json", ll)
summ["crfll"] = ll

# ---- item 4: the power cycle ---------------------------------------------------------------
ev = load(pkt / "runs/pc/events.jsonl")
boot = load(raw / "pc/boot-console.jsonl")
txt, first_t, prompt_t, lines = b"", None, None, []
for r in boot[1:]:
    b = bytes.fromhex(r["hex"])
    if first_t is None and b:
        first_t = r["t"]
    txt += b
    if prompt_t is None and b"litex" in txt[-200:] and txt.rstrip().endswith(b">"):
        prompt_t = r["t"]
for ln in txt.decode("ascii", "replace").replace("\r", "").split("\n"):
    if ln.startswith("Milan") or "BIOS CRC" in ln:
        lines.append(ln.strip())
pc = dict(case="PC",
          nvm=[{k: e.get(k) for k in ("stage", "tag", "slot_a", "seq_a", "slot_b", "seq_b", "authoritative", "image_seq",
                                      "dirty", "commit_busy", "pend", "commits_ok", "commits_failed", "verdict", "version")}
               for e in ev if e["kind"] == "nvm"],
          clock=[dict(stage=e["stage"], tag=e["tag"], source=e["source"]) for e in ev if e["kind"] == "clock-read"],
          sets=[dict(stage=e["stage"], tag=e["tag"], src=e["src"], status=e["status"], readback=e["readback"])
                for e in ev if e["kind"] == "set-clock"],
          rx=[{k: e.get(k) for k in ("stage", "tag", "idx", "status", "conn_count", "talker_is_peer", "flags")}
              for e in ev if e["kind"] == "rx-state"],
          formats=[{k: e.get(k) for k in ("stage", "kind", "fmt", "as_found", "equal")} for e in ev
                   if e["kind"] in ("format-post-boot", "format-final")],
          polls=[{k: e.get(k) for k in ("stage", "tag", "rc", "polls", "locked_s", "state_changes")}
                 for e in ev if e["kind"] == "poll-end"],
          relock=[{k: e.get(k) for k in ("locked_s", "rebind_needed")} for e in ev if e["kind"] == "relock"],
          counters={f"{e['stage']}-{t}": v for e in ev if e["kind"] == "counters"
                    for t, v in [(e["tag"], counter_table([e])[e["tag"]])]},
          boot=dict(listen_start=boot[0]["start"], first_byte=first_t, prompt=prompt_t,
                    first_byte_to_prompt_s=round(prompt_t - first_t, 3) if first_t and prompt_t else None,
                    bytes=len(txt), milestone_lines=lines),
          post_first_command_t=next(e["t"] for e in ev if e["stage"] == "post" and e["kind"] == "clock-read"))
write(pkt / "summary/pc/pc.json", pc)
summ["pc"] = pc
(pkt / "runs/pc/boot-console.txt").write_text(
    "".join(ch for ch in txt.decode("ascii", "replace").replace("\r", "") if ch == "\n" or ch >= " ")
    .replace("[1m", "").replace("[0m", "").replace("[92;1m", ""))
print(json.dumps({k: (len(json.dumps(v, default=float))) for k, v in summ.items()}))
