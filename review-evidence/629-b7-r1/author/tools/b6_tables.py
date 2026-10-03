#!/usr/bin/env python3
"""Render the findings page's per-case tables from the grades (lane B6).

usage: b6_tables.py <summary_dir> <case>=<grade.json> [...]

Writes <summary_dir>/tables.md and prints it. Every figure in a table comes from a grade
file named on the command line; nothing is typed by hand.
"""
import json
import sys
from pathlib import Path

out_dir = Path(sys.argv[1])
cases = []
for a in sys.argv[2:]:
    c, f = a.split("=", 1)
    cases.append((c, json.load(open(f))))


def n(x, d=0):
    return f"{x:,.{d}f}"


def ppm(x, d=3):
    return f"{x:+.{d}f}"


lines = []
T = lines.append
T("<!-- thdn -->")
T("| Case | Tone | Blocks | Clean blocks | THD+N, clean, dB (median / worst) | SNR, clean, dB (median / worst) "
  "| Worst THD+N, a block with a listener discontinuity, dB | Worst THD+N, a block with a DUT beat only, dB |")
T("|---|---|---|---|---|---|---|---|")
for c, g in cases:
    for ch, tone in (("ch0", "997 Hz"), ("ch1", "9,973 Hz")):
        b = g["blocks"]
        cl = b["clean"][ch]
        li = b["listener"][ch]
        db = b["dut_beat_only"][ch]
        lw = "none" if li is None else f"{li['thdn_db_worst']:.2f}"
        dw = "none" if db is None else f"{db['thdn_db_worst']:.2f}"
        T(f"| {c} | {tone} | {g['tone']['blocks']} | {g['tone']['clean_blocks']} | "
          f"{cl['thdn_db_median']:.2f} / {cl['thdn_db_worst']:.2f} | {cl['snr_db_median']:.2f} / {cl['snr_db_worst']:.2f} | "
          f"{lw} | {dw} |")
T("")
T("<!-- offset -->")
T("| Case | Fitted offset, clean blocks, 997 Hz, ppm (max magnitude) | Fitted offset, clean blocks, 9,973 Hz, ppm (max magnitude) "
  "| Tone offset over the window, listener only, ppm | DUT beat, ppm | Counted McASP0 to peer ratio, ppm |")
T("|---|---|---|---|---|---|")
for c, g in cases:
    b = g["blocks"]["clean"]
    eo = g["effective_offset_ppm"]
    beat = eo["without_capture_path"] - eo["listener_only"]
    cr = g["frame_rate_ratio"]["counted"]
    T(f"| {c} | {b['ch0']['ppm_maxabs']:.1e} | {b['ch1']['ppm_maxabs']:.1e} | {ppm(eo['listener_only'])} | {ppm(beat)} | "
      f"{ppm(cr['ppm'])} (1 frame = {cr['resolution_ppm']:.3f}) |")
T("")
T("<!-- discontinuities -->")
T("| Case | Window, s | Listener drops (frames) | Listener repeats | Listener silent inserts | DUT beat repeats | "
  "Beat comb: period, frames; teeth expected | DUT SLIP_TDM, per s | Capture-path losses: events, clusters, frames lost | Torn frames |")
T("|---|---|---|---|---|---|---|---|---|---|")
for c, g in cases:
    a = g["attribution"]
    li = a.get("listener", {})
    be = a.get("DUT beat", {})
    cp = a.get("capture path", {})
    bc = g.get("beat_comb") or {}
    comb = "-" if not bc else f"{bc['period_frames']:,.2f}; {bc['teeth_in_window']:.1f}"
    slip = "-" if "slip_tdm_per_s" not in bc else f"{bc['slip_tdm_per_s']:.4f}"
    T(f"| {c} | {g['window']['seconds']:.2f} | {li.get('skips', 0)} ({n(li.get('skipped_frames', 0))}) | "
      f"{li.get('repeats', 0)} | {li.get('silent_inserts', 0)} | {be.get('repeats', 0)} | {comb} | {slip} | "
      f"{cp.get('events', 0)}, {cp.get('clusters', 0)}, {n(cp.get('lost_frames', 0))} | {g['tone']['torn']} |")
T("")
T("<!-- ratio -->")
T("| Case | Counted ratio, ppm | Timed ratio, McASP0 capture, ppm (95 % half-width) | Halves, ppm | McASP0 capture rate on the board's clock, Hz "
  "| External capture reads | Capture read stalls over 15 ms |")
T("|---|---|---|---|---|---|---|")
for c, g in cases:
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
txt = "\n".join(lines) + "\n"
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "tables.md").write_text(txt)
print(txt)
