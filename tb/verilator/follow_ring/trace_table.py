#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Decimate one follow_ring run's traces into the table its mechanism reads.

  trace_table.py <run.log> <pdu.csv> <servo.csv> [--step-s S] [--from-s A] [--to-s B]
                 [--csv OUT]

One row per step of S seconds, times relative to the first CLOCK_SOURCE set
(or --origin-s, which can name the hold for the pull-in case):
  ring margin  the loopback ring's margin range in the step, in media ticks
               (16 entries, target 11 at PDU end: nominal margin (5, 6])
  slips        recorded duplicate plus skip frames, from counter events
  skips        the skip subset of slips
  recentres    declared settle pulses, counted separately from slips
  event_trace  complete when the log covers the whole bin; partial at its
               end; unavailable on older logs without RING-EVENTS records
  render       the render stage's fill range at PDU ends and first-event
               delay range, in ticks (the law: 14, and (8, 9])
  servo        the last window's state, PI run flag, error (ns per 512 ms),
               trim (ppm) and the meter's rate validity before the step's end
RING-EVENT lines carry absolute times from the harness's counter and pulse
observations. Bins are [start, end). Counts never derive from margin jumps,
and a recentre never masks a simultaneous slip. Run with --trace to emit
these records. On older logs, zero recorded events does not prove zero slips;
event_trace explicitly marks the missing evidence.
"""

import argparse
import csv
import math
import re
import sys
from pathlib import Path

STATES = {0: "IDLE", 1: "VERIFY", 2: "REPAIR", 3: "ACQUIRE", 4: "LOCKED", 5: "HOLDOVER", 6: "FAULT"}


def instants(log: str) -> dict[str, list[float]]:
    """Read absolute event times, independently of PDU margin changes."""
    out: dict[str, list[float]] = {"set": [], "dup": [], "skip": [], "recentre": [], "end": []}
    for m in re.finditer(r"t=([0-9.]+) s  CLOCK_SOURCE <- (\d+)", log):
        out["set"].append(float(m.group(1)))
    for m in re.finditer(r"^RING-EVENT: (dup|skip|recentre) ([0-9.]+)$", log, re.MULTILINE):
        out[m.group(1)].append(float(m.group(2)))
    for m in re.finditer(r"^RING-EVENTS: complete through ([0-9.]+) s$", log, re.MULTILINE):
        out["end"].append(float(m.group(1)))
    return out


def main() -> int:
    """Print (and optionally write) the decimated table."""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("log", type=Path)
    ap.add_argument("pdus", type=Path)
    ap.add_argument("servo", type=Path)
    ap.add_argument("--step-s", type=float, default=0.5)
    ap.add_argument("--from-s", type=float, default=None)
    ap.add_argument("--to-s", type=float, default=None)
    ap.add_argument("--origin-s", type=float, default=None, help="time zero (default: the first set)")
    ap.add_argument("--csv", type=Path, default=None)
    a = ap.parse_args()
    if not math.isfinite(a.step_s) or a.step_s <= 0:
        ap.error("--step-s must be finite and positive")
    marks = instants(a.log.read_text())
    origin = a.origin_s if a.origin_s is not None else (marks["set"][0] if marks["set"] else 0.0)
    t0 = origin + (a.from_s if a.from_s is not None else -2.0)
    t1 = origin + (a.to_s if a.to_s is not None else 60.0)
    if not all(math.isfinite(t) for t in (origin, t0, t1)) or t1 <= t0:
        ap.error("the time range must be finite and increasing")
    nbin = max(1, int(math.ceil((t1 - t0) / a.step_s)))
    bins = [{"mlo": math.inf, "mhi": -math.inf, "slips": 0, "skips": 0, "recentres": 0,
             "flo": 99, "fhi": -1,
             "dlo": math.inf, "dhi": -math.inf} for _ in range(nbin)]
    for kind in ("dup", "skip", "recentre"):
        for t in marks[kind]:
            if t0 <= t < t1:
                b = bins[int((t - t0) / a.step_s)]
                if kind == "recentre":
                    b["recentres"] += 1
                else:
                    b["slips"] += 1
                    b["skips"] += int(kind == "skip")
    with a.pdus.open() as fh:
        for r in csv.DictReader(fh):
            t = float(r["arrive_s"])
            m = float(r["ring_margin_ticks"])
            if not (t0 <= t < t1):
                continue
            b = bins[int((t - t0) / a.step_s)]
            if not math.isnan(m):
                b["mlo"] = min(b["mlo"], m)
                b["mhi"] = max(b["mhi"], m)
            f = int(r["render_fill"])
            d = float(r["render_delay_ticks"])
            if f >= 0:
                b["flo"] = min(b["flo"], f)
                b["fhi"] = max(b["fhi"], f)
            if not math.isnan(d):
                b["dlo"] = min(b["dlo"], d)
                b["dhi"] = max(b["dhi"], d)
    windows = []
    with a.servo.open() as fh:
        for r in csv.DictReader(fh):
            windows.append((float(r["t_s"]), int(r["state"]), int(r["pi_run"]), int(r["ew_ns"]),
                            float(r["trim_ppm"]), int(r["meter_valid"])))
    rows = []
    hdr = ("t_s", "ring_margin_ticks", "slips", "skips", "recentres", "event_trace",
           "render_fill", "render_delay_ticks", "servo",
           "pi", "e_ns", "trim_ppm", "rate_valid")
    for i, b in enumerate(bins):
        te = min(t1, t0 + (i + 1) * a.step_s)
        coverage = "unavailable"
        if marks["end"]:
            coverage = "complete" if t0 + i * a.step_s >= 0 and te <= marks["end"][-1] else "partial"
        last = [w for w in windows if w[0] <= te]
        w = last[-1] if last else (0.0, 0, 0, 0, 0.0, 0)
        rows.append((f"{te - origin:+.2f}",
                     f"{b['mlo']:+.3f}..{b['mhi']:+.3f}" if b["mhi"] > -math.inf else "-",
                     str(b["slips"]), str(b["skips"]), str(b["recentres"]), coverage,
                     f"{b['flo']}..{b['fhi']}" if b["fhi"] >= 0 else "-",
                     f"{b['dlo']:.3f}..{b['dhi']:.3f}" if b["dhi"] > -math.inf else "-",
                     STATES.get(w[1], str(w[1])), str(w[2]), str(w[3]), f"{w[4]:+.3f}", str(w[5])))
    print("| " + " | ".join(hdr) + " |")
    print("|" + "---|" * len(hdr))
    for r in rows:
        print("| " + " | ".join(r) + " |")
    if a.csv:
        with a.csv.open("w", newline="") as fh:
            wr = csv.writer(fh)
            wr.writerow(hdr)
            wr.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
