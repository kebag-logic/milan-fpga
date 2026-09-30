#!/usr/bin/env python3
"""Check the round-2 page claims that rest on published packet data.

usage: check_r2_claims.py <evidence-root>

<evidence-root> is an extraction of review-evidence/b3-r1 (branch
b3-review-evidence). Offline; reads only published files.

S1  (617 page :105-112, :158-167) outside-region census: the outside words sum
    to the outside frames x 8, none is a pattern word, the zero-word count is
    frame 45,587's six plus the 777 transition frames', and the region bounds.
S3  (617 page :239-252) PP_STAT and PP_NVM_STAT at the start and end of the
    lane: only PP_STAT bit 11 and PP_NVM_STAT bit 22 move, together, with
    pend 0 -> 1, dirty 0, VD_OK, commits 0 -> 6, seq 229/230 -> 235/236.
S4  (451 page :140-143, :156) frame 1,632's words: one ordinal, tags 1..8 in
    order, low bytes 0x20..0xc0, previous frame silent.
"""
import json
import os
import re
import sys


def is_pattern(w):
    return w != 0 and (w & 0xFF) == 0 and 1 <= (w >> 24) <= 8


def main():
    root = sys.argv[1]
    bad = 0

    def check(name, ok, detail):
        nonlocal bad
        bad += not ok
        print(f"{'OK' if ok else 'FAIL'} {name}: {detail}")

    g = json.load(open(os.path.join(root, "author/runs/din-long/grade.json")))
    r = g["region"]
    outside = g["frames"] - r["frames"]
    w = g["outside_region_words"]
    check("S1 region bounds", (r["first_frame"], r["last_frame"], r["frames"]) == (45588, 3405623, 3360036),
          f"first {r['first_frame']} last {r['last_frame']} frames {r['frames']}")
    check("S1 outside frames", outside == 1191588, f"{g['frames']} - {r['frames']} = {outside}")
    check("S1 outside words sum", sum(w.values()) == outside * 8, f"{w} sum {sum(w.values())} = {outside} x 8")
    edge = {int(k): [int(x, 16) for x in v] for k, v in g["edge_frames"].items()}
    others = [x for x in edge[45587] if x not in (0, 0xFFFFFF00)]
    check("S1 the one 'other' word is frame 45,587's and is not a pattern word",
          w.get("other") == 1 and len(others) == 1 and not is_pattern(others[0]), f"{[hex(x) for x in others]}")
    zeros_expected = edge[45587].count(0) + 776 * 8 + 3
    check("S1 zero words = frame 45,587's + 776 all-zero + 3", w.get("zero") == zeros_expected,
          f"{w.get('zero')} vs {zeros_expected}; frames_after_region_before_idle {g['frames_after_region_before_idle']}")
    check("S1 no pattern word outside the region", set(w) <= {"ffffff00", "zero", "other"},
          "census classes are only ffffff00, zero and the one non-pattern other")
    check("S1 torn counts", g["torn_frames_whole_recording"] == 0 and g["torn_frames_in_region"] == 0,
          "0 whole recording, 0 region")

    def nvm(p):
        t = open(os.path.join(root, p)).read()
        pp = int(re.search(r"PP_STAT=([0-9a-f]{8})", t).group(1), 16)
        ns = int(re.search(r"PP_NVM_STAT=([0-9a-f]{8})", t).group(1), 16)
        kv = dict(re.findall(r"\b(pend|dirty|backed|stale|verdict)=(\w+)", t))
        seq = re.search(r"slot A \w+ seq (\d+), slot B \w+ seq (\d+)", t).groups()
        ok = re.search(r"commits ok=(\d+)", t).group(1)
        return pp, ns, kv, seq, ok

    a, b = nvm("author/restore/dut-start.txt"), nvm("author/restore/dut-end.txt")
    check("S3 PP_STAT delta is bit 11 only", a[0] ^ b[0] == 1 << 11 and b[0] >> 11 & 1,
          f"{a[0]:08x} -> {b[0]:08x}")
    check("S3 PP_NVM_STAT delta is bit 22 only", a[1] ^ b[1] == 1 << 22 and b[1] >> 22 & 1,
          f"{a[1]:08x} -> {b[1]:08x}")
    check("S3 console pend matches both bits", a[2]["pend"] == "0" and b[2]["pend"] == "1",
          f"pend {a[2]['pend']} -> {b[2]['pend']}")
    check("S3 end state", b[2]["dirty"] == "0" and b[2]["verdict"] == "VD_OK" and b[2]["backed"] == "1"
          and b[2]["stale"] == "0", f"{b[2]}")
    check("S3 commits and slots", (a[4], b[4], a[3], b[3]) == ("0", "6", ("229", "230"), ("235", "236")),
          f"commits {a[4]} -> {b[4]}, seq {a[3]} -> {b[3]}")

    f = json.load(open(os.path.join(root, "author-r2/packet/summary/usb-long-frame-1632.json")))
    words = [int(x["word"], 16) for x in f["words"]]
    check("S4 frame and file", f["frame"] == 1632 and f["sha256"].startswith("7995b44a")
          and f["previous_frame_silent"], f"frame {f['frame']} sha {f['sha256'][:8]} prev silent")
    check("S4 tags in slot order, one ordinal",
          [x >> 24 for x in words] == list(range(1, 9)) and len({(x >> 8) & 0xFFFF for x in words}) == 1,
          f"ordinal {(words[0] >> 8) & 0xffff:04x}")
    low = [x & 0xFF for x in words]
    check("S4 low bytes rise 0x20 .. 0xc0", low[0] == 0x20 and low[-1] == 0xC0 and low == sorted(low),
          " ".join(f"{x:02x}" for x in low))
    print(f"{bad} failure(s)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
