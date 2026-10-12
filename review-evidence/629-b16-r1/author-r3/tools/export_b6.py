#!/usr/bin/env python3
"""Copy one case's grade into the lane packet in reviewable sizes (lane B6).

usage: export_b6.py <grade-full.json> <packet_summary_case_dir>

Writes grade.json (the full grade without the per-event list), events.csv (every
discontinuity in the window with its attribution evidence) and blocks.csv (per
one-second block: start frame, events by cause, THD+N, SNR and fitted offset per tone).
"""
import csv
import json
import sys
from pathlib import Path

g = json.load(open(sys.argv[1]))
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
evl = g.pop("events_list")
blocks = g.pop("blocks_list", None)
json.dump(g, open(out / "grade.json", "w"), indent=1, default=float)
cols = ["capture_frame", "frame", "kind", "frames", "step", "cause", "cluster", "read_jump_ms", "read_gap_ms",
        "size_48n_plus_12", "invalid_between"]
with open(out / "events.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(cols)
    for e in evl:
        w.writerow([e.get(c, "") for c in cols])
if blocks:
    with open(out / "blocks.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["block", "start", "events", "invalid", "listener", "dut_beat", "capture_path",
                    "thdn_db_997", "snr_db_997", "ppm_997", "thdn_db_9973", "snr_db_9973", "ppm_9973"])
        for b in blocks:
            bc = b["by_cause"]
            w.writerow([b["block"], b["start"], b["events"], b["invalid"], bc["listener"], bc["DUT beat"],
                        bc["capture path"],
                        f"{b['ch0']['thdn_db']:.3f}", f"{b['ch0']['snr_db']:.3f}", f"{b['ch0']['ppm']:.6g}",
                        f"{b['ch1']['thdn_db']:.3f}", f"{b['ch1']['snr_db']:.3f}", f"{b['ch1']['ppm']:.6g}"])
print(json.dumps({p.name: p.stat().st_size for p in out.iterdir()}))
