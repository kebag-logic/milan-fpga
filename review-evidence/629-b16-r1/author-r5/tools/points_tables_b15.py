#!/usr/bin/env python3
"""Lane B15 (new): render the per-point tables from the grades and run records (offline).

usage: points_tables_b15.py <packet_dir> <out.md> <ext_summary_dir>

Reads summary/<run>/*.json (tone_points_b15.py, align_b15.py) and runs/<run>/events.jsonl, and the
external capture's reduced rows (<ext_summary_dir>/<run>-d.json: the two channels that carry the
reference peer's listener output, written by this tool's caller from the private all-channel grade).
Times are CEST (UTC+2).
"""
import json
import sys
import time
from pathlib import Path

P = Path(sys.argv[1])
OUT = sys.argv[2]
EXT = Path(sys.argv[3])
W = ["MEDIA_LOCKED", "MEDIA_UNLOCKED", "STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH", "MEDIA_RESET", "TIMESTAMP_UNCERTAIN",
     "TIMESTAMP_VALID", "TIMESTAMP_NOT_VALID", "UNSUPPORTED_FORMAT", "LATE_TIMESTAMP", "EARLY_TIMESTAMP", "FRAMES_RX"]


def cest(t):
    return time.strftime("%H:%M:%S", time.gmtime(t + 7200)) + f".{int((t % 1) * 10)}"


def counters(payload):
    b = bytes.fromhex(payload)
    v = [int.from_bytes(b[8 + 4 * i:12 + 4 * i], "big") for i in range(12)]
    return dict(zip(W, v))


def cell(r, t):
    if f"tone_{t}" in r:
        m = r[f"tone_{t}"]["median"]
        return (f"present: {m['level_dbfs']:.2f} dBFS, {m['f_hz']:.4f} Hz ({m['ppm']:+.3f} ppm), "
                f"SNR {m['snr_db']:.2f} dB, THD+N {m['thdn_db']:.2f} dB")
    return f"absent ({100 * r.get(f'share_{t}', 0):.3f} % of the power within 5 Hz)"


lines = []
for run in ("pts1", "pts2"):
    ev = [json.loads(x) for x in (P / "runs" / run / "events.jsonl").read_text().splitlines()]
    st = next(e for e in ev if e["kind"] == "captures-started")["started"]
    done = {e["what"]: e["seconds"] for e in ev if e["kind"] == "capture-done"}
    lines.append(f"## {run}\n")
    lines.append(f"captures: tap {cest(st['tap'])} for {done['tap']} s; external {cest(st['extcap'])} for {done['extcap']} s; "
                 f"McASP0 {cest(st['mcasp'])} for {done['mcasp']} s\n")
    pts = [("(a) the peer's link tap, the peer's talker", "a-peer-tap.json"),
           ("(b) the DUT's link tap, the peer's talker", "b-dut-tap.json"),
           ("(c) the DUT's TDM output, McASP0", "c-mcasp.json")]
    if (P / "summary" / run / "ctl-peer-tap-dut-talker.json").exists():
        pts += [("control: the peer's link tap, the DUT's talker", "ctl-peer-tap-dut-talker.json"),
                ("control: the DUT's link tap, the DUT's talker", "ctl-dut-tap-dut-talker.json")]
    lines.append("| Point | Frames | Channel | Level, dBFS RMS | Range, LSB | 997 Hz | 9,973 Hz | SHA-256 |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for label, f in pts:
        g = json.loads((P / "summary" / run / f).read_text())
        for r in g["channels"][:4] if "tap" in f and "dut-talker" not in f else g["channels"][:2] if "dut-talker" in f else g["channels"][:4]:
            lines.append(f"| {label} | {g['frames']:,} | {r['channel']} | {r['rms_dbfs']} | {r['min']} to {r['max']} | "
                         f"{cell(r, 997)} | {cell(r, 9973)} | `{g['sha256'][:16]}...` |")
    d = json.loads((EXT / f"{run}-d.json").read_text())
    for r in d["rows"]:
        lines.append(f"| (d) the external capture, the peer's digital output | {d['frames']:,} | {r['pair_channel']} | "
                     f"{r['rms_dbfs']} | {r['min']} to {r['max']} | {cell(r, 997)} | {cell(r, 9973)} | `{d['sha256'][:16]}...` |")
    lines.append("")
    a = json.loads((P / "summary" / run / "align-b-c.json").read_text())
    lines.append(f"align (b) vs (c): {a['verdict']}, {a['compared_equal']:,} of {a['mcasp_frames']:,} frames equal, "
                 f"first window matched {a['matches_of_first_window']} offset(s), slips {a['slips']}, differing {a['frames_differing']}\n")
    for e in ev:
        if e["kind"] == "counters":
            c = counters(e["payload"])
            lines.append(f"counters {e['tag']} {e['who']} STREAM_INPUT 0: " + ", ".join(f"{k} {v}" for k, v in c.items()))
    lines.append("")
    for e in ev:
        if e["kind"] in ("format-check", "bind", "unbind", "rebind-as-found", "format-restore"):
            lines.append(f"- {e['kind']}: " + json.dumps({k: v for k, v in e.items() if k not in ('t', 'kind')}))
    fin = next(e for e in ev if e["kind"] == "final")
    lines.append(f"- final: equal_to_found={fin['equal_to_found']} differ={fin['differ']}")
    lines.append("")
Path(OUT).write_text("\n".join(lines) + "\n")
print("\n".join(lines))
