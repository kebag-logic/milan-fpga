#!/usr/bin/env python3
"""Grade an 8-channel S32_LE capture taken on the host's USB Audio card
against the first-light pattern (offline, no bench access).

usage: grade_usb.py <raw> [<json_out>]

1. The strict rule is decode_capture.py's (first-light packet 451-a403): tag
   t (1..8) in bits 31:24, a 16-bit frame ordinal in bits 23:8, a zero low
   byte, SoC channel c carrying tag c + 1, and one ordinal per frame.
2. Where the strict rule fails, this tool explains how. Each non-zero word is
   read as tag t = bits 31:24 and a fractional ordinal x = bits 23:0 / 256, so
   a word that a resampler interpolated between two pattern words reads as a
   fraction instead of failing outright. The low byte is reported as a
   histogram.
3. Each non-silent frame is classified by its tags: aligned (channel c
   carries tag c + 1), rotated by k words (channel c carries tag
   ((c + k) mod 8) + 1, k = 1..7), or other (a zero word, a tag outside 1..8,
   or tags that are not a rotation). In a rotated frame the k channels that
   wrapped carry the next frame, so 1 is subtracted from their ordinal.
4. For aligned and rotated frames the spread of the corrected ordinals across
   the eight channels is measured (one sample instant: spread < 1), and the
   frame ordinal is their mean. Consecutive frames of one class form a
   segment; inside a segment the step between frame ordinals is classified
   (+1 within 0.5, repeat, skip, other), and every segment boundary is listed
   with the class change and the ordinal jump across it.
"""
import array
import collections
import hashlib
import json
import sys


def wrap(d):
    d %= 65536.0
    return d - 65536.0 if d >= 32768.0 else d


def main():
    path = sys.argv[1]
    data = open(path, "rb").read()
    w = array.array("I")
    w.frombytes(data)
    if sys.byteorder != "little":
        w.byteswap()
    frames = len(w) // 8
    res = dict(file=path.split("/")[-1], bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), frames=frames,
               nominal_seconds=frames / 48000)
    strict_valid = strict_torn = 0
    low = collections.Counter()
    words = collections.Counter()
    cls_count = collections.Counter()
    spread_hist = collections.Counter()
    segs = []
    cur = None
    prev_x = None
    steps = collections.Counter()
    for f in range(frames):
        fr = w[f * 8:(f + 1) * 8]
        if not any(fr):
            cls, fx = "silent", None
        else:
            if all(v != 0 and (v & 0xFF) == 0 and (v >> 24) == c + 1 for c, v in enumerate(fr)):
                strict_valid += 1
                if len({(v >> 8) & 0xFFFF for v in fr}) != 1:
                    strict_torn += 1
            tags, xs = [], []
            ok = True
            for v in fr:
                t = v >> 24
                if v == 0 or not 1 <= t <= 8:
                    words["zero" if v == 0 else "tag_outside_1_8"] += 1
                    ok = False
                    tags.append(0)
                    xs.append(None)
                    continue
                b = v & 0xFF
                low["0x00" if b == 0 else "0x01-0x3f" if b < 0x40 else "0x40-0x7f" if b < 0x80
                    else "0x80-0xbf" if b < 0xC0 else "0xc0-0xff"] += 1
                words["tag_1_8"] += 1
                tags.append(t)
                xs.append((v & 0xFFFFFF) / 256.0)
            cls, fx = "other", None
            if ok:
                k = (tags[0] - 1) % 8
                if all(tags[c] == ((c + k) % 8) + 1 for c in range(8)):
                    cls = "aligned" if k == 0 else f"rot{k}"
                    corr = [xs[c] - (1.0 if (k and c >= 8 - k) else 0.0) for c in range(8)]
                    ref = corr[0]
                    rel = [wrap(x - ref) for x in corr]
                    spread = max(rel) - min(rel)
                    spread_hist["<0.25" if spread < 0.25 else "<0.5" if spread < 0.5 else "<1" if spread < 1.0
                                else ">=1"] += 1
                    fx = (ref + sum(rel) / 8.0) % 65536.0
        cls_count[cls] += 1
        if cur is None or cur["class"] != cls:
            if cur is not None:
                segs.append(cur)
            cur = dict(**{"class": cls}, first_frame=f, last_frame=f, frames=0, first_ordinal=fx, last_ordinal=fx,
                       steps=collections.Counter())
            prev_x = None
        cur["frames"] += 1
        cur["last_frame"] = f
        if fx is not None:
            if prev_x is not None:
                d = wrap(fx - prev_x)
                key = "+1" if abs(d - 1) < 0.5 else "0" if abs(d) < 0.5 else "+2" if abs(d - 2) < 0.5 else "other"
                cur["steps"][key] += 1
                steps[key] += 1
            prev_x = fx
            cur["last_ordinal"] = fx
    segs.append(cur)
    for s in segs:
        s["steps"] = dict(s["steps"])
        for k in ("first_ordinal", "last_ordinal"):
            if s[k] is not None:
                s[k] = round(s[k], 3)
    res["strict"] = dict(valid_frames=strict_valid, torn_valid_frames=strict_torn,
                         failing_or_silent_frames=frames - strict_valid)
    res["words"] = dict(words)
    res["low_byte_histogram"] = dict(sorted(low.items()))
    res["frame_classes"] = dict(sorted(cls_count.items()))
    res["channel_spread_in_aligned_or_rotated_frames"] = dict(spread_hist)
    res["within_segment_steps"] = dict(steps)
    res["segments"] = len(segs)
    res["class_changes"] = len(segs) - 1
    sil = [s for s in segs if s["class"] == "silent"]
    res["silent_stretches"] = len(sil)
    res["silent_stretch_frames_max"] = max((s["frames"] for s in sil), default=0)
    non_silent = [s for s in segs if s["class"] != "silent"]
    res["first_non_silent_frame"] = non_silent[0]["first_frame"] if non_silent else None
    for name in ("aligned",):
        best = max((s for s in segs if s["class"] == name), key=lambda s: s["frames"], default=None)
        res[f"longest_{name}_segment"] = {k: best[k] for k in ("first_frame", "last_frame", "frames", "steps")} if best else None
    best = max((s for s in segs if s["class"] not in ("silent", "other")), key=lambda s: s["frames"], default=None)
    res["longest_aligned_or_rotated_segment"] = {k: best[k] for k in ("class", "first_frame", "last_frame", "frames", "steps")} if best else None
    joins = []
    last = None
    for s in segs:
        if s["first_ordinal"] is None:
            continue
        if last is not None:
            joins.append(dict(at_frame=s["first_frame"], from_class=last["class"], to_class=s["class"],
                              gap_frames=s["first_frame"] - last["last_frame"] - 1,
                              ordinal_jump=round(wrap(s["first_ordinal"] - last["last_ordinal"]), 3)))
        last = s
    res["joins_between_ordinal_segments"] = len(joins)
    res["joins_with_unit_step"] = sum(1 for j in joins if abs(j["ordinal_jump"] - 1 - j["gap_frames"]) < 0.5)
    # rotation runs: the word rotation k of consecutive aligned-or-rotated
    # segments, skipping "other" and "silent" segments between them (a
    # resampler rings for a few frames at the pattern's 65,536-frame ordinal
    # wrap, which reads as "other" without any change of rotation)
    runs = []
    for s in segs:
        if s["class"] in ("silent", "other"):
            if runs:
                runs[-1]["interruptions"].append(s["class"])
            continue
        k = 0 if s["class"] == "aligned" else int(s["class"][3:])
        if runs and runs[-1]["k"] == k:
            runs[-1]["last_frame"] = s["last_frame"]
            runs[-1]["frames"] += s["frames"]
            continue
        runs.append(dict(k=k, first_frame=s["first_frame"], last_frame=s["last_frame"], frames=s["frames"],
                         interruptions=[]))
    res["rotation_runs"] = len(runs)
    res["rotation_changes"] = max(0, len(runs) - 1)
    res["rotation_changes_after_silence"] = sum(1 for a in runs[:-1] if "silent" in a["interruptions"])
    res["rotation_frames_by_k"] = {str(k): sum(r["frames"] for r in runs if r["k"] == k) for k in range(8)}
    spans = sorted(r["last_frame"] - r["first_frame"] + 1 for r in runs)
    res["rotation_run_span_frames"] = dict(min=spans[0], median=spans[len(spans) // 2], max=spans[-1]) if spans else None
    res["ordinal_wraps_expected"] = frames // 65536
    res["rotation_run_list"] = [{k: r[k] for k in ("k", "first_frame", "last_frame", "frames")} for r in runs]
    res["segment_list"] = segs
    res["joins"] = joins
    s = json.dumps(res, indent=1)
    if len(sys.argv) > 2:
        open(sys.argv[2], "w").write(s + "\n")
    print(json.dumps({k: v for k, v in res.items() if k not in ("segment_list", "joins", "rotation_run_list")}, indent=1))


if __name__ == "__main__":
    main()
