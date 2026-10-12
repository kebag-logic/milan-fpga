#!/usr/bin/env python3
"""Lane B16, round 2: B16b's B0 figures, recomputed from the packet's published files only.

usage: r2_b0_receipt.py <packet-root> <out.json>

Reads summary/b0-2/{c-b9-grade,align-a-c,align-b-c,a-peer-tap}.json, runs/b0-2/events.jsonl and
tools/run_b16.py, and writes:

- the floor medians of each tone at (c), and the degraded event-free blocks as runs;
- the recording frames each tap's sample comparison covers, the whole one-second blocks inside the
  overlap of both, the degraded blocks inside it and beyond it, and the worst block of each tone
  inside and beyond it; (a)'s own blocks and worst blocks;
- the binds, the McASP0 capture command and the recording's start: the command plus the 2 s the
  board plays the loop before it records in this mode, checked against run_b16.py's own text.

Every input is in the packet, so anyone can run it; its inputs' SHA-256 are in the output.
"""
import datetime
import hashlib
import json
import sys
from pathlib import Path

CEST = datetime.timezone(datetime.timedelta(hours=2))
FS = 48000


def runs(blocks):
    out = []
    for b in sorted(blocks):
        if out and b == out[-1][1] + 1:
            out[-1][1] = b
        else:
            out.append([b, b])
    return out


def hms(t):
    return datetime.datetime.fromtimestamp(t, CEST).strftime("%H:%M:%S.%f")[:-5]


def main() -> int:
    root, out_p = Path(sys.argv[1]), Path(sys.argv[2])
    files = {k: root / v for k, v in dict(grade="summary/b0-2/c-b9-grade.json", align_a="summary/b0-2/align-a-c.json",
                                          align_b="summary/b0-2/align-b-c.json", tap_a="summary/b0-2/a-peer-tap.json",
                                          events="runs/b0-2/events.jsonl", run_tool="tools/run_b16.py").items()}
    g = json.loads(files["grade"].read_text())
    al = json.loads(files["align_a"].read_text())
    bl = json.loads(files["align_b"].read_text())
    ta = json.loads(files["tap_a"].read_text())
    s = g["summary"]
    deg = s["degraded_event_free_blocks"]
    cov = min(al["covered_recording_frames"][1], bl["covered_recording_frames"][1])
    assert al["covered_recording_frames"][0] == 0 and bl["covered_recording_frames"][0] == 0
    whole = cov // FS
    inside = [b for b in deg if b < whole]
    partial = [b for b in deg if b * FS < cov < (b + 1) * FS]
    beyond = [b for b in deg if b * FS >= cov]
    blk = {b["block"]: b for b in g["blocks"]}

    def worst(sel, ch):
        b = max(sel, key=lambda k: blk[k][ch]["thdn_db"])
        return dict(block=b, thdn_db=round(blk[b][ch]["thdn_db"], 2))

    tones = {}
    for ch, key, name in (("ch0", "tone_997", "997 Hz"), ("ch1", "tone_9973", "9,973 Hz")):
        a = next(c[key] for c in ta["channels"] if key in c)
        tones[name] = dict(floor_median_db=s[f"{ch}_floor"]["thdn_db_median"], all_median_db=s[f"{ch}_all"]["thdn_db_median"],
                           worst_inside=worst(inside, ch), worst_beyond=worst(beyond, ch),
                           worst_all_db=s[f"{ch}_all"]["thdn_db_worst"],
                           a_blocks=a["blocks"], a_worst_db=round(a["worst_thdn_db"], 2))
    ev = [json.loads(line) for line in files["events"].read_text().splitlines() if line.strip()]
    binds = [e["t"] for e in ev if e.get("kind") == "bind"]
    cap = next(e for e in ev if e.get("kind") == "captures-started")["started"]
    tool = files["run_tool"].read_text()
    lead_in_tool = "AP=$!; sleep 2;" in tool and "started 2 s before the recording" in tool
    rec_start = cap["mcasp"] + 2.0
    out = dict(
        tool="r2_b0_receipt.py", inputs={k: hashlib.sha256(p.read_bytes()).hexdigest() for k, p in files.items()},
        blocks=s["blocks"], blocks_at_floor=s["blocks_at_floor"], degraded=len(deg), degraded_runs=runs(deg),
        tones=tones,
        overlap=dict(frames_a=al["covered_recording_frames"][1], frames_b=bl["covered_recording_frames"][1],
                     seconds=round(cov / FS, 4), whole_blocks=[0, whole - 1], partial_degraded=partial,
                     degraded_inside=len(inside), degraded_inside_runs=runs(inside),
                     degraded_beyond=len(beyond), degraded_beyond_runs=runs(beyond)),
        timing=dict(last_bind=hms(max(binds)), tap_start=hms(cap["tap"]), mcasp_command=hms(cap["mcasp"]),
                    playback_lead_s=2.0, playback_lead_in_run_tool=lead_in_tool, recording_start=hms(rec_start),
                    command_after_binds_s=round(cap["mcasp"] - max(binds), 1),
                    recording_after_binds_s=round(rec_start - max(binds), 1)))
    out_p.write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(dict(floor=[t["floor_median_db"] for t in tones.values()], inside=len(inside), beyond=len(beyond),
                          timing=out["timing"])))
    return 0 if lead_in_tool else 1


if __name__ == "__main__":
    sys.exit(main())
