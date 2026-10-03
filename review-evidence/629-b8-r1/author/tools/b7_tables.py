#!/usr/bin/env python3
"""Render the findings section's per-case tables and verdicts from the grades (lane B7).

usage: b7_tables.py <summary_dir> <case>=<grade.json>:<events.jsonl> [...]

Lane B6's b6_tables.py, extended: the DUT's SLIP_TDM from the window's own reads, the servo
and AAF meter through the window, the set-to-LOCKED time, and every case's verdict computed
from the criteria fixed before any case ran (HANDOFF.md, "Grading criteria"). Writes
<summary_dir>/tables.md and <summary_dir>/verdicts.json and prints the tables. Every figure
comes from a file named on the command line; nothing is typed by hand.
"""
import json
import sys
from pathlib import Path

out_dir = Path(sys.argv[1])
cases = []
for a in sys.argv[2:]:
    c, f = a.split("=", 1)
    gf, ef = f.split(":", 1)
    cases.append((c, json.load(open(gf)), [json.loads(l) for l in open(ef)]))


def n(x, d=0):
    return f"{x:,.{d}f}"


def ppm(x, d=3):
    return f"{x:+.{d}f}"


def clk_ctr(g, tag):
    c = (g.get("counters") or {}).get(tag, {}).get("dut-0x0024-0")
    return c["counters"] if isinstance(c, dict) else None


def verdict(c, g, evs):
    chk = []

    def add(name, ok, value):
        chk.append(dict(check=name, ok=bool(ok), value=value))

    li = g["attribution"].get("listener", {})
    n_li = li.get("events", 0)
    tone = g["tone"]
    dev = max(tone.get("ch0_clean_max_dev_from_floor_db") or 0, tone.get("ch1_clean_max_dev_from_floor_db") or 0)
    clean = g["blocks"]["clean"]
    off = max(clean["ch0"]["ppm_maxabs"], clean["ch1"]["ppm_maxabs"]) if clean["ch0"] else None
    cr = g["frame_rate_ratio"]["counted"]["ppm"]
    m = g["frame_rate_ratio"].get("mcasp_capture", {})
    sets = [e for e in evs if e["kind"] == "set-clock" and e.get("tag") == "case"]
    sw = g.get("servo_window") or {}
    slip = g.get("slip_tdm_window") or {}
    if c == "A0":
        lo = g["effective_offset_ppm"]["listener_only"]
        add("listener net rate beyond 2 ppm", abs(lo) > 2, round(lo, 3))
        add("blocks free of discontinuities at the floor within 0.01 dB", tone["clean_blocks"] > 0 and dev <= 0.01,
            dict(clean_blocks=tone["clean_blocks"], max_dev_db=dev))
        kind = "control"
    elif c in ("A1", "A2"):
        add("0 listener discontinuities", n_li == 0, n_li)
        add("blocks free of discontinuities at the floor within 0.01 dB", tone["clean_blocks"] > 0 and dev <= 0.01,
            dict(clean_blocks=tone["clean_blocks"], max_dev_db=dev))
        add("fitted offset on those blocks under 0.001 ppm", off is not None and off < 0.001, off)
        add("clock source set and read back", sets and all(e["ok"] for e in sets),
            [dict(who=e["who"], src=e["src"], readback=e["readback"]) for e in sets])
        kind = "case"
    elif c == "B0":
        add("counted ratio beyond 2 ppm", abs(cr) > 2, round(cr, 3))
        kind = "control"
    else:
        add("servo LOCKED at every DUT read in the window", sw.get("servo_locked_at_every_read"), sw.get("servo_states"))
        add("counted ratio within 0.5 ppm of zero", abs(cr) <= 0.5, round(cr, 3))
        hold = "ratio_ppm" in m and abs(m["ratio_ppm"]) <= m["ratio_ppm_halfwidth95"]
        add("timed ratio's interval holds zero", hold,
            dict(ratio_ppm=m.get("ratio_ppm"), halfwidth=m.get("ratio_ppm_halfwidth95")))
        add("0 listener discontinuities on the tone path", n_li == 0, n_li)
        add("clock source set and read back", sets and all(e["ok"] for e in sets),
            [dict(who=e["who"], src=e["src"], readback=e["readback"]) for e in sets])
        if c == "BAAF":
            lt = g.get("lock_timing") or {}
            s2l = lt.get("set_to_locked_s")
            add("servo LOCKED within 15 s of the set", s2l is not None and s2l[1] <= 15.0, s2l)
            c0, c2 = clk_ctr(g, "window-mark-0"), clk_ctr(g, "window-mark-2")
            add("CLOCK_DOMAIN LOCKED and UNLOCKED unchanged across the window", c0 is not None and c0 == c2,
                dict(first=c0, last=c2))
            add("SLIP_TDM static", slip.get("slip_tdm_delta") == 0
                and sw.get("slip_tdm_skips_first_last", [0, 1])[0] == sw.get("slip_tdm_skips_first_last", [0, 1])[1],
                dict(dups=sw.get("slip_tdm_dups_first_last"), skips=sw.get("slip_tdm_skips_first_last")))
            r = sw.get("meter_restarts_first_last")
            add("meter history-restart count unchanged across the window", r is not None and r[0] == r[1], r)
        kind = "case"
    ok = all(x["ok"] for x in chk)
    label = ("PASS as a control" if ok else "FAIL as a control") if kind == "control" else ("PASS" if ok else "FAIL")
    return dict(case=c, verdict=label, checks=chk)


lines = []
T = lines.append
verdicts = [verdict(c, g, e) for c, g, e in cases]
V = {v["case"]: v["verdict"] for v in verdicts}
T("<!-- b7-thdn -->")
T("| Case | Tone | Blocks | Blocks at the floor | THD+N there, dB (median / worst) | SNR there, dB (median / worst) "
  "| Worst THD+N, a block with a listener discontinuity, dB | Worst THD+N, all blocks, dB |")
T("|---|---|---|---|---|---|---|---|")
for c, g, _ in cases:
    for ch, tone in (("ch0", "997 Hz"), ("ch1", "9,973 Hz")):
        b = g["blocks"]
        cl = b["clean"][ch]
        li = b["listener"][ch]
        al = b["all"][ch]
        lw = "None" if li is None else f"{li['thdn_db_worst']:+.2f}"
        cls = "-" if cl is None else f"{cl['thdn_db_median']:.2f} / {cl['thdn_db_worst']:.2f}"
        sns = "-" if cl is None else f"{cl['snr_db_median']:.2f} / {cl['snr_db_worst']:.2f}"
        T(f"| {c} | {tone} | {g['tone']['blocks']} | {g['tone']['clean_blocks']} | {cls} | {sns} | {lw} | "
          f"{al['thdn_db_worst']:+.2f} |")
T("")
T("<!-- b7-offset -->")
T("| Case | Fitted offset, blocks at the floor, ppm (largest magnitude, either tone) | Listener drops (frames) "
  "| Listener repeats | Listener silent inserts | DUT beat repeats | Tone offset, listener only, ppm "
  "| Counted McASP0 to peer ratio, ppm |")
T("|---|---|---|---|---|---|---|---|")
for c, g, _ in cases:
    b = g["blocks"]["clean"]
    off = "-" if b["ch0"] is None else f"{max(b['ch0']['ppm_maxabs'], b['ch1']['ppm_maxabs']):.1e}"
    a = g["attribution"]
    li = a.get("listener", {})
    be = a.get("DUT beat", {})
    eo = g["effective_offset_ppm"]
    cr = g["frame_rate_ratio"]["counted"]
    T(f"| {c} | {off} | {li.get('skips', 0)} ({n(li.get('skipped_frames', 0))}) | {li.get('repeats', 0)} | "
      f"{li.get('silent_inserts', 0)} | {be.get('repeats', 0)} | {ppm(eo['listener_only'])} | "
      f"{ppm(cr['ppm'])} (1 frame = {cr['resolution_ppm']:.3f}) |")
T("")
T("<!-- b7-discontinuities -->")
T("| Case | Window of captured audio, s | DUT `SLIP_TDM` dups in the window (reads, s) | Capture-path losses: events, "
  "clusters, frames | Torn frames | Result |")
T("|---|---|---|---|---|---|")
for c, g, _ in cases:
    cp = g["attribution"].get("capture path", {})
    s = g.get("slip_tdm_window") or {}
    sl = "-" if not s else f"{s['slip_tdm_delta']} ({s['slip_tdm_seconds']:.0f} s)"
    T(f"| {c} | {g['window']['seconds']:.2f} | {sl} | {cp.get('events', 0)}, {cp.get('clusters', 0)}, "
      f"{n(cp.get('lost_frames', 0))} | {g['tone']['torn']} | {V[c]} |")
T("")
T("<!-- b7-ratio -->")
T("| Case | Counted ratio, ppm | Timed ratio, McASP0 capture, ppm (95 % half-width) | Window halves, timed, ppm "
  "| McASP0 capture rate on the board's clock, Hz | External capture reads | Capture read stalls over 15 ms |")
T("|---|---|---|---|---|---|---|")
for c, g, _ in cases:
    r = g["frame_rate_ratio"]
    m = r.get("mcasp_capture", {})
    if "ratio_ppm" in m:
        tm = f"{ppm(m['ratio_ppm'], 2)} (+-{m['ratio_ppm_halfwidth95']:.2f})"
        hv = f"{ppm(m['ratio_ppm_first_half'], 2)} / {ppm(m['ratio_ppm_second_half'], 2)}"
        rb = f"{m['rate_board']:,.3f}"
    else:
        tm, hv, rb = m.get("error", "-"), "-", "-"
    T(f"| {c} | {ppm(r['counted']['ppm'])} | {tm} | {hv} | {rb} | {n(r['external_capture']['reads'])} | "
      f"{g['capture_reads']['stalls']} |")
T("")
T("<!-- b7-servo -->")
T("| Case | DUT reads in the window | Servo state at every read | Trim, ppm (min / max) | AAF meter: locked, rate valid "
  "at every read | Meter rate, ppm (min / max) | Meter restarts (first / last) | Meter largest deviation, ns "
  "| CRF sink rate, ppm (min / max) | Set to LOCKED, s | CLOCK_DOMAIN LOCKED/UNLOCKED, window start -> end |")
T("|---|---|---|---|---|---|---|---|---|---|---|")
for c, g, _ in cases:
    sw = g.get("servo_window") or {}
    tr = sw.get("trim_ppm_min_max")
    mr = sw.get("meter_rate_ppm_min_max")
    cf = sw.get("crf_rate_ppm_min_max_when_locked")
    lt = (g.get("lock_timing") or {}).get("set_to_locked_s")
    c0, c2 = clk_ctr(g, "window-mark-0"), clk_ctr(g, "window-mark-2")
    cc = "-" if not c0 else f"{c0.get('LOCKED')}/{c0.get('UNLOCKED')} -> {c2.get('LOCKED')}/{c2.get('UNLOCKED')}"
    sel = any(r.get("meter", {}).get("enabled") for r in sw.get("rows", []))
    mlv = "not selected" if not sel else \
        f"{'yes' if sw['meter_locked_every_read'] else 'no'}, {'yes' if sw['meter_rate_valid_every_read'] else 'no'}"
    T(f"| {c} | {sw.get('reads', 0)} | {', '.join(sw.get('servo_states', []))} | "
      f"{'-' if not tr else f'{tr[0]:+.2f} / {tr[1]:+.2f}'} | {mlv} | {'-' if not mr else f'{mr[0]:+.3f} / {mr[1]:+.3f}'} | "
      f"{'-' if not sel else ' / '.join(map(str, sw['meter_restarts_first_last']))} | "
      f"{'-' if not sel else sw.get('meter_max_dev_ns_last')} | {'-' if not cf else f'{cf[0]:+.3f} / {cf[1]:+.3f}'} | "
      f"{'-' if not lt else f'{lt[0]:.1f} to {lt[1]:.1f}'} | {cc} |")
txt = "\n".join(lines) + "\n"
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "tables.md").write_text(txt)
json.dump(verdicts, open(out_dir / "verdicts.json", "w"), indent=1, default=float)
print(txt)
for v in verdicts:
    print(v["case"], v["verdict"], [(x["check"], x["ok"]) for x in v["checks"] if not x["ok"]])
