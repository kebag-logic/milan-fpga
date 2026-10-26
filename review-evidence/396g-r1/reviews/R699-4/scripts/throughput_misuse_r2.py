#!/usr/bin/env python3
"""Grader throughput when the stated byte order is wrong (no channel ever acquires).

Usage: python3 -I throughput_misuse_r2.py <path-to-tb/tools> <dir holding grader_probe_r2.py>
Eight channels, 48 kHz, a clean little-endian capture declared big-endian, 1 MiB chunks.
"""
import contextlib
import io
import json
import sys
import time

tools, here = sys.argv[1], sys.argv[2]
sys.path.insert(0, here)
sys.argv = [sys.argv[0], tools]
with contextlib.redirect_stdout(io.StringIO()):
    import grader_probe_r2 as gp  # noqa: E402
tc = gp.tc
for seconds in (1, 2):
    frames = 48000 * seconds
    cap = gp.pack(gp.build(frames, 8, []), "little")
    t0 = time.monotonic()
    v, d = tc.grade_audio_counter_capture([cap[i:i + (1 << 20)] for i in range(0, len(cap), 1 << 20)],
                                          tc.CounterCapture(8, "big", 48000, 0.0, 0.0),
                                          tc.CounterRunLog([], [], 0))
    dt = time.monotonic() - t0
    print(json.dumps({"seconds_audio": seconds, "verdict": v, "why": d.get("why"), "events": len(d.get("events", [])),
                      "grade_s": round(dt, 2), "x_realtime": round(seconds / dt, 3),
                      "projected_24h_grade_hours": round(24 * 3600 / (seconds / dt) / 3600, 1)}), flush=True)
