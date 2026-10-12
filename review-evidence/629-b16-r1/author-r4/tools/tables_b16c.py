#!/usr/bin/env python3
"""Lane B16c (new): the B16c findings tables, rendered from the packet's own files (offline, read-only).

Reads summary/<run>/{a-peer-tap,b-dut-tap,c-mcasp,c-b9-grade,align-a-c,align-b-c,d-extcap-pair,d-loop-decode}.json
and runs/<run>/events.jsonl for the runs named, and prints Markdown rows: the four points (per-block median and
worst of tone_points_b16.py), lane B9's grade at (c) (b9_thdn.py), (c) against (a) and (b) (align_b16.py), (d)
(dloop_b16.py), and the following record (the clock-source sets and read-backs, the servo poll's spans, the
window marks' GET_COUNTERS and GET_CLOCK_SOURCE, the tone monitor). Nothing is computed that the files do not hold;
the formatting is the only work.

usage: tables_b16c.py <packet_dir> <run> [<run> ...]
"""
import json
import sys
from pathlib import Path

P = Path(sys.argv[1])
RUNS = sys.argv[2:]


def j(run, name):
    f = P / "summary" / run / name
    return json.load(open(f)) if f.exists() else None


def events(run):
    return [json.loads(x) for x in open(P / "runs" / run / "events.jsonl")]


def n(x):
    return f"{x:,}"


def ppm(x, d=3):
    v = round(x, d)
    return f"{0.0:.{d}f}" if v == 0 else f"{v:+.{d}f}"


def tone_cells(ch, key):
    t = ch.get(key)
    if not t:
        return ["-", "-", "-"]
    m = t["median"]
    return [f"{m['f_hz']:,.4f} Hz, {ppm(m['ppm'])} ppm", f"{m['thdn_db']:.2f} ({t['worst_thdn_db']:.2f})", f"{m['snr_db']:.2f}"]


print("<!-- four points: Run | Point | Frames | Level, dBFS | 997 Hz: frequency, offset | THD+N, dB | SNR, dB |"
      " 9,973 Hz: frequency, offset | THD+N, dB | SNR, dB -->")
for run in RUNS:
    for pt, name in (("(a)", "a-peer-tap.json"), ("(b)", "b-dut-tap.json"), ("(c)", "c-mcasp.json")):
        d = j(run, name)
        if not d:
            continue
        tc = d["tone_channels"]
        c0 = d["channels"][tc["997"][0]]
        c1 = d["channels"][tc["9973"][0]]
        if d["point"] == "tap":
            fr = f"{n(d['frames'])}; {n(d['info']['pdus'])} PDUs, {d['info']['seq_gaps']} gaps"
        else:
            fr = n(d["frames"])
        lvl = c0["tone_997"]["median"]["level_dbfs"]
        print(f"| `{run}` | {pt} | {fr} | {lvl:.4f} | " + " | ".join(tone_cells(c0, "tone_997") + tone_cells(c1, "tone_9973")) + " |")

print("\n<!-- lane B9's grade at (c): Run | Tone | Blocks | Discontinuities | Blocks at the path's floor | THD+N at the floor,"
      " dB, median (worst) | SNR at the floor, dB | THD+N, all blocks, dB, median (worst) | Level | Offset, ppm, median"
      " (largest block) -->")
for run in RUNS:
    g = j(run, "c-b9-grade.json")
    if not g:
        continue
    s = g["summary"]
    for tone, k in (("997 Hz, channel 0", "ch0"), ("9,973 Hz, channel 1", "ch1")):
        fl, al = s[f"{k}_floor"], s[f"{k}_all"]
        print(f"| `{run}` | {tone} | {s['blocks']} | {s['events']} | {s['blocks_at_floor']} | {fl['thdn_db_median']:.2f} "
              f"({fl['thdn_db_worst']:.2f}) | {fl['snr_db_median']:.2f} | {al['thdn_db_median']:.2f} ({al['thdn_db_worst']:.2f}) | "
              f"{al['level_dbfs_median']:.2f} dBFS | {ppm(al['ppm_median'], 4)} ({abs(al['ppm_maxabs']):.3f}) |")
    print(f"<!-- `{run}`: skips {s['skips']}, repeats {s['repeats']}, inserts {s['inserts']}, glitches {s['glitches']}, "
          f"silent {s['silent_frames']}, effective offset {s['effective_offset_ppm']} ppm, phase net {s['phase_net_frames']:.7f} frames -->")

print("\n<!-- (c) against (a) and (b): Run | (c) against (b) | (c) against (a) -->")
for run in RUNS:
    cells = []
    for name in ("align-b-c.json", "align-a-c.json"):
        a = j(run, name)
        if not a:
            cells.append("-")
            continue
        cells.append(f"{a['verdict']} over {n(a['compared_equal'])} recorded frames, {a['compared_equal'] / 48000:.1f} s, "
                     f"{a['frames_differing']} differing, {len(a['slips'])} slips")
    print(f"| `{run}` | " + " | ".join(cells) + " |")

print("\n<!-- (d): Run | decoded | invalid (before the loop) | skips | repeats | net steps | torn | level, THD+N -->")
for run in RUNS:
    d = j(run, "d-loop-decode.json")
    p = j(run, "d-extcap-pair.json")
    if not d:
        continue
    rows = (p or {}).get("rows") or []
    lv = "; ".join(f"{t['median']['level_dbfs']:.2f} dBFS, {t['median']['thdn_db']:.2f} ({t['worst_thdn_db']:.2f}) dB, "
                   f"{t['blocks']} blocks" for r in rows for t in (r.get("tone_997"), r.get("tone_9973")) if t)
    print(f"| `{run}` | {n(d['decoded'])} | {n(d['invalid'])} | {d['skips']} | {d['repeats']} | {d['net_step_frames']} | "
          f"{d['torn']} | {lv} |")

print("\n<!-- following record -->")
for run in RUNS:
    ev = events(run)
    sets = [e for e in ev if e["kind"] == "set-clock"]
    lock = [e for e in ev if e["kind"] == "servo-state"]
    marks = {e["tag"]: e for e in ev if e["kind"] == "mark"}
    ps = next((e for e in ev if e["kind"] == "poll-summary"), None)
    tone = next((e for e in ev if e["kind"] == "tone-summary"), None)
    fin = next((e for e in ev if e["kind"] == "final"), None)
    music = [e["closed"] for e in ev if e["kind"] == "music-check"]
    print(f"<!-- `{run}` -->")
    for e in sets:
        print(f"- set-clock {e['tag']}: {e['who']} to {e['src']}, {e['status']}, read back {e['readback']}")
    for e in lock:
        print(f"- servo {e['state']} {e['s_lo']} to {e['s_hi']} s after the DUT's set")
    for t in ("before-peer-set", "after-peer-set", "window-mark-0", "window-mark-1", "window-mark-2", "after-captures",
              "after-restore"):
        m = marks.get(t)
        if m:
            c = m["counters"]
            print(f"- mark {t}: clock {m['clock']}; DUT CLOCK_DOMAIN LOCKED/UNLOCKED {c['dut-0x0024-0'][:2]}; "
                  f"peer CLOCK_DOMAIN {c['peer-0x0024-0'][:2]}; DUT in 0 MEDIA_LOCKED/UNLOCKED {c['dut-0x0005-0'][:2]}; "
                  f"DUT in 1 {c['dut-0x0005-1'][:2]}; peer in 0 {c['peer-0x0005-0'][:2]}")
    if ps:
        for k, v in ps["spans"].items():
            w = {x: (v["first"][x], v["last"][x], v["distinct"][x]) for x in sorted(v["first"])}
            print(f"- poll span {k}: {v['polls']} polls, servo {v['servo']}, failed {v['failed']}; words (first, last, distinct) {w}")
    if tone:
        print(f"- tone monitor: {tone['reads']} reads, states {tone['states']}, trigger times {tone['trigger_times']}, "
              f"hw_ptr monotonic {tone['hw_ptr_monotonic']}")
    print(f"- music checks closed: {music}")
    if fin:
        print(f"- final read-back equal to the start: {fin['equal_to_found']} {fin['differ']}")
