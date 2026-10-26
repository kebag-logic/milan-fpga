"""Time grade_audio_counter_capture's clean fast path on a streamed capture.

Usage: grader_throughput.py <repository-root> [minutes]
"""
import struct
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "tb" / "tools"))
import torture_campaign as tp  # noqa: E402

channels, minutes = 8, int(sys.argv[2]) if len(sys.argv) > 2 else 2
frame = struct.Struct(">" + "I" * channels)
period = b"".join(frame.pack(*[tp.audio_counter_word(c + 1, k) for c in range(channels)])
                  for k in range(tp.AUDIO_COUNTER_MODULUS))
blocks = 48000 * 60 * minutes // tp.AUDIO_COUNTER_MODULUS
start = time.perf_counter()
verdict, detail = tp.grade_audio_counter_capture(
    (period for _ in range(blocks)), tp.CounterCapture(channels, "big", 48000, 0.0, 0.0),
    tp.CounterRunLog([], [], 0))
elapsed = time.perf_counter() - start
print(f"frames={detail['frames']} channels={channels} elapsed_s={elapsed:.3f} "
      f"capture_minutes_per_s={detail['frames'] / 48000 / 60 / elapsed:.1f}")
print(f"verdict={verdict} why={detail['why']} events={len(detail['events'])}")
