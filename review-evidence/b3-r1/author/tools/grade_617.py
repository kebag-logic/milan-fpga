#!/usr/bin/env python3
"""#617 acceptance 4 grade of one DIN recording (offline, no bench access).

usage: grade_617.py <pcap> <stream_id_hex> [<json_out>]

Framing and pattern rule are decode_din_pairs.py's (first-light packet
451-a403): stream channel c carries tag c + 1 in bits 31:24, a 16-bit frame
ordinal in bits 23:8 and a zero low byte. #617 defines a torn AAF frame as a
frame carrying samples from two TDM frames. Under the pattern that is a frame
whose valid words do not all carry the same ordinal. This tool reports:

- torn frames over the whole recording and inside the playback region (first
  to last frame in which all eight channels carry their own tag);
- the per-frame ordinal-offset state of pairs 1..3 against pair 0 and of each
  pair's right channel against its left (the #451 first-light shape);
- per channel, every non-+1 ordinal step with its frame index, and whether all
  eight channels step at the same frames (a whole-frame repeat or skip);
- the outside-region word census (idle words, zero words, transition frames).
"""
import collections
import hashlib
import json
import struct
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from decode_din_pairs import frames_of, own, sgn  # noqa: E402


def main():
    path, sid = sys.argv[1], bytes.fromhex(sys.argv[2])
    frames, meta = frames_of(path, sid)
    res = dict(file=path.split("/")[-1], bytes=meta["bytes"], sha256=meta["sha256"], stream_id=sid.hex(),
               pdus=meta["pdus"], frames=len(frames), sequence_gaps=meta["seq_gaps"],
               header_mismatch=meta["hdr_err"])
    full = [i for i, (_, w) in enumerate(frames) if all(own(w[c], c) for c in range(8))]
    a, b = full[0], full[-1]
    res["region"] = dict(first_frame=a, last_frame=b, frames=b - a + 1, seconds_at_48k=round((b - a + 1) / 48000, 3))

    def torn(w):
        ords = {(v >> 8) & 0xFFFF for v in w if v != 0 and (v & 0xFF) == 0 and 1 <= (v >> 24) <= 8}
        return len(ords) > 1

    torn_all = [i for i, (_, w) in enumerate(frames) if torn(w)]
    res["torn_frames_whole_recording"] = len(torn_all)
    res["torn_frames_in_region"] = sum(1 for i in torn_all if a <= i <= b)
    res["torn_frame_indices_first"] = torn_all[:20]
    states = collections.Counter()
    lr = [0] * 4
    invalid = 0
    for i in range(a, b + 1):
        w = frames[i][1]
        if not all(own(w[c], c) for c in range(8)):
            invalid += 1
            continue
        o = [(w[c] >> 8) & 0xFFFF for c in range(8)]
        for p in range(4):
            lr[p] += o[2 * p] != o[2 * p + 1]
        states[json.dumps([sgn(o[2 * p] - o[0]) for p in range(1, 4)])] += 1
    res["invalid_frames_in_region"] = invalid
    res["left_right_mismatch_per_pair"] = lr
    res["pair_offset_vs_pair0"] = dict(states)
    steps = []
    for c in range(8):
        ev = []
        prev = None
        for i in range(a, b + 1):
            v = frames[i][1][c]
            o = (v >> 8) & 0xFFFF
            if prev is not None:
                d = sgn(o - prev)
                if d != 1:
                    ev.append((i, d))
            prev = o
        steps.append(ev)
    same = all(steps[c] == steps[0] for c in range(8))
    res["steps_identical_in_all_channels"] = same
    kinds = collections.Counter(d for _, d in steps[0])
    res["channel0_non_unit_steps"] = {str(k): v for k, v in sorted(kinds.items())}
    idx = [i for i, _ in steps[0]]
    gaps = [q - p for p, q in zip(idx, idx[1:])]
    res["step_frames"] = idx
    res["step_gap_min"] = min(gaps) if gaps else None
    res["step_gap_max"] = max(gaps) if gaps else None
    # outside the region: word census and the frames next to its edges
    cen = collections.Counter()
    for i in list(range(0, a)) + list(range(b + 1, len(frames))):
        for v in frames[i][1]:
            cen["zero" if v == 0 else f"{v:08x}" if v in (0xFFFFFF00,) else "pattern" if (v & 0xFF) == 0 and 1 <= (v >> 24) <= 8 else "other"] += 1
    res["outside_region_words"] = dict(cen)
    res["edge_frames"] = {str(i): [f"{v:08x}" for v in frames[i][1]] for i in
                          sorted(set([max(0, a - 2), max(0, a - 1), a, b, min(len(frames) - 1, b + 1),
                                      min(len(frames) - 1, b + 2)]))}
    zero_after = 0
    for i in range(b + 1, len(frames)):
        if any(frames[i][1]):
            if all(v == 0 or v == 0xFFFFFF00 for v in frames[i][1]) and not all(v == 0xFFFFFF00 for v in frames[i][1]):
                zero_after += 1
                continue
            break
        zero_after += 1
    res["frames_after_region_before_idle"] = zero_after
    s = json.dumps(res, indent=1)
    print(s)
    if len(sys.argv) > 3:
        open(sys.argv[3], "w").write(s + "\n")


if __name__ == "__main__":
    main()
