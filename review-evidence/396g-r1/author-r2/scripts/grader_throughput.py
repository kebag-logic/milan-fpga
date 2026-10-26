#!/usr/bin/env python3
"""Throughput of grade_audio_counter_capture on synthetic 8-channel captures.

Usage: python3 -I grader_throughput.py <path-to-tb/tools>

Grades 60 s at 48 kHz, fed as 1 MiB chunks, for three shapes: clean, one
channel offset by 7 samples from frame 100 on (the shape the round-1 fast
path could not take), and a capture whose channel 2 carries no counter.
Prints capture-minutes graded per second and the 24-hour projection.
"""
import importlib.util
import sys
import time

spec = importlib.util.spec_from_file_location("tc", sys.argv[1] + "/torture_campaign.py")
tc = importlib.util.module_from_spec(spec)
sys.modules["tc"] = tc
spec.loader.exec_module(tc)

RATE, SECONDS, CHANNELS = 48000, 60, 8
frames = RATE * SECONDS
clean = tc.synthesize_counter_capture(frames, CHANNELS)
shifted = bytearray(clean)
other = tc.synthesize_counter_capture(frames, CHANNELS, events=[{"kind": "drop", "index": 100, "n": 7}])
for index in range(100, frames):
    at = 4 * (index * CHANNELS + 3)
    shifted[at:at + 4] = other[at:at + 4]
for name, capture, tags in (("clean", clean, None), ("one-channel-offset", bytes(shifted), None),
                            ("channel-2-no-counter", clean, tuple(None if c == 2 else c + 1
                                                                  for c in range(CHANNELS)))):
    chunks = [capture[i:i + (1 << 20)] for i in range(0, len(capture), 1 << 20)]
    start = time.monotonic()
    verdict, detail = tc.grade_audio_counter_capture(
        chunks, tc.CounterCapture(CHANNELS, "big", RATE, 0.0, 0.0, tags=tags), tc.CounterRunLog([], [], 0))
    took = time.monotonic() - start
    minutes_per_s = SECONDS / 60 / took
    events = [(e["channel"], e["capture_index"], e["class"], e.get("n")) for e in detail["events"]]
    print(f"{name}: verdict {verdict} ({detail['why']}), events {events}, {took:.3f} s for {SECONDS} s: "
          f"{minutes_per_s:.1f} capture-minutes per second; 24 h in {24 * 60 / minutes_per_s / 60:.1f} min")
