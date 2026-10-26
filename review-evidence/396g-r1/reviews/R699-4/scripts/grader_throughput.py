#!/usr/bin/env python3
"""Throughput of the #396 audio grader on clean and degraded captures.

Usage: python3 -I grader_throughput.py <path-to-tb/tools>
Eight channels, 48 kHz, big-endian, 1 MiB chunks. Prints JSON lines.
"""
import importlib.util
import json
import struct
import sys
import time

spec = importlib.util.spec_from_file_location("tc", sys.argv[1] + "/torture_campaign.py")
tc = importlib.util.module_from_spec(spec)
sys.modules["tc"] = tc
spec.loader.exec_module(tc)

CH, RATE = 8, 48000


def word(tag, counter):
    return ((tag << 12) | (counter & 0xFFF)) << 8


def capture(seconds, offset_channel=None):
    period = []
    for k in range(4096):
        words = [word(c + 1, k) for c in range(CH)]
        if offset_channel is not None:
            words[offset_channel] = word(offset_channel + 1, k + 7)
        period.append(struct.pack(">" + "I" * CH, *words))
    frames = seconds * RATE
    body = b"".join(period)
    reps, rest = divmod(frames, 4096)
    return body * reps + b"".join(period[:rest]), frames


def chunks(data, size=1 << 20):
    return [data[i:i + size] for i in range(0, len(data), size)]


for name, seconds, off in (("clean", 60, None), ("one-channel-offset", 10, 3)):
    data, frames = capture(seconds, off)
    t0 = time.monotonic()
    verdict, detail = tc.grade_audio_counter_capture(
        chunks(data), tc.CounterCapture(CH, "big", RATE, 0.0, 0.0), tc.CounterRunLog([], [], 0))
    dt = time.monotonic() - t0
    print(json.dumps({"case": name, "verdict": verdict, "frames_graded": detail.get("frames"),
                      "frames_expected": frames, "audio_s": seconds, "grade_s": round(dt, 3),
                      "capture_minutes_per_s": round(seconds / 60 / dt, 2),
                      "hours_for_24h": round(86400 / (seconds / dt) / 3600, 2),
                      "dut_events": len([e for e in detail.get("events", []) if e["attribution"] == "dut"])}))
