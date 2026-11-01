# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The synthetic counter captures the release audio scenarios grade.

This is the mechanism half of torture_release_steps.py, lifted out whole
when that file passed a thousand lines: the counter layout restated apart
from the planner, the four-channel captures built from it with the planted
arms of issue #396 REQ-VER-06, and the grading calls. The scenarios and their
oracles stay in torture_release_steps.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tb" / "tools"))
import torture_campaign as tp  # noqa: E402


def _counter_capture(extra: list, losses: list | None = None, arms_drop: int = 0) -> tuple:
    """A four-channel capture with the drop, repeat and flip arms at both ends."""
    frames = 4 * 4096
    sites = (200, 400, 600, frames - 800, frames - 500, frames - 200)
    source = [{"kind": "drop", "index": sites[0], "n": 3}, {"kind": "repeat", "index": sites[1], "n": 2},
              {"kind": "flip", "index": sites[2], "channel": 0, "mask": 0x100},
              {"kind": "drop", "index": sites[3], "n": 3}, {"kind": "repeat", "index": sites[4], "n": 2},
              {"kind": "flip", "index": sites[5], "channel": 1, "mask": 0x100}]
    arms = [{"class": "dropped", "index": sites[0], "n": 3}, {"class": "repeated", "index": sites[1], "n": 2},
            {"class": "bit-flip", "index": sites[2], "channel": 0, "mask": 0x100},
            {"class": "dropped", "index": sites[3], "n": 3}, {"class": "repeated", "index": sites[4], "n": 2},
            {"class": "bit-flip", "index": sites[5], "channel": 1, "mask": 0x100}]
    arms += [{"class": "dropped", "index": 9000, "n": arms_drop}] if arms_drop else []
    capture = tp.synthesize_counter_capture(frames, 4, events=source + extra)
    return tp.grade_audio_counter_capture(
        capture, tp.CounterCapture(4, "big", 48000, 0.0, 0.0),
        tp.CounterRunLog(arms, losses or [], 0), required_s=_qualified_s(frames))


def _qualified_s(frames: int) -> float:
    """A clean capture's qualified length: 63 guard samples off each end, at 48 kHz."""
    return (frames - 2 * 63) / 48000


def _counter_word(tag: int, n: int) -> int:
    """REQ-VER-06's counter layout restated here, apart from the planner: channel
    number in sample bits 15:12, n mod 2048 in bits 11:1, and in bit 0 bit n mod 32
    of block n div 2048's code, the block number times 0x9E3779B1 modulo 2^32."""
    code = ((n // 2048) * 0x9E3779B1) % 2**32
    return ((tag << 12) | ((n % 2048) << 1) | ((code >> (n % 32)) & 1)) << 8


def _independent_capture(frames: int, shifts: dict, flips: list) -> bytes:
    """Four big-endian S32 channels; `shifts` moves the source position from an
    index on, and each flip (index, channel, mask) XORs one word."""
    import struct
    rows, shift = [], 0
    for index in range(frames):
        shift += shifts.get(index, 0)
        rows.append([_counter_word(channel + 1, index + shift) for channel in range(4)])
    for index, channel, mask in flips:
        rows[index][channel] ^= mask
    return b"".join(struct.pack(">4I", *row) for row in rows)


#: Arms in the first and the last tenth of an 8192-frame capture.
_ARM_SHIFTS = {100: 3, 300: -2, 7492: 3, 7742: -2}
_ARMS = [{"class": "dropped", "index": 100, "n": 3}, {"class": "repeated", "index": 300, "n": 2},
         {"class": "bit-flip", "index": 500, "mask": 0x100, "channel": 1},
         {"class": "dropped", "index": 7492, "n": 3}, {"class": "repeated", "index": 7742, "n": 2},
         {"class": "bit-flip", "index": 7992, "mask": 0x100, "channel": 3}]


def _with_arms(shifts: dict) -> dict:
    """The arm shifts plus `shifts`, added where both move the same index."""
    merged = dict(_ARM_SHIFTS)
    for index, shift in shifts.items():
        merged[index] = merged.get(index, 0) + shift
    return merged


def _arm_edits() -> list:
    """The two planted flips of the code bit."""
    return [(500, 1, 0x100), (7992, 3, 0x100)]


def _grade_independent(shifts: dict, edits: list, **layout: object) -> tuple:
    capture = _independent_capture(8192, _with_arms(shifts), _arm_edits() + edits)
    return tp.grade_audio_counter_capture(capture, tp.CounterCapture(4, "big", 48000, 0.0, 0.0, **layout),
                                          tp.CounterRunLog(_ARMS, [], 0), required_s=_qualified_s(8192))


def _dut(detail: dict) -> list:
    return sorted((e["channel"], e["capture_index"], e["class"], e.get("n"), e.get("mask"), e.get("partner"))
                  for e in detail.get("events", []) if e["attribution"] == "dut")
