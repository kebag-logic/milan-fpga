#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer check of step 3 console-only claims per cycle directory.

PHC steps (TAI_NS change minus build-box send-time change, > 50 ms),
CLKV_TUCNT delta across the cycle, holdover (CLKV_STAT bit 3) spans after the
off, path generation values, RST_EPOCH values, LINKG_STAT edges, and the
CRFT_CTRL licence edges (0x3 idle, other = licensed) after the off, in
seconds after the outlet-off command on the build-box clock.

Usage: r264_step3_console.py <cycle_dir> [...]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r264_console as rc  # noqa: E402
import r264_step3 as s3  # noqa: E402


def cycle(d):
    o = s3.offsets(d)
    ps = s3.strip_times(d)
    off_local = ps["T_OFF_CMD"] - s3.off_at(o["strip"], ps["T_OFF_CMD"] - o["strip"]["before"])
    on_strip = ps["T_ON_CMD"]
    b = rc.parse(os.path.join(d, "console.txt"))
    rel = lambda t: round(t - off_local, 3)
    st = [x for x in b if x["cmd"] == "milan_status" and "TAI_NS" in x["kv"]]
    steps = []
    for x, y in zip(st, st[1:]):
        dt_phc = (int(y["kv"]["TAI_NS"], 16) - int(x["kv"]["TAI_NS"], 16)) / 1e9
        dt_box = y["t"] - x["t"]
        if abs(dt_phc - dt_box) > 0.05:
            steps.append((rel(y["t"]), round(dt_phc - dt_box, 3)))
    hold = []
    prev = None
    for x in st:
        h = (int(x["kv"]["CLKV_STAT"], 16) >> 3) & 1
        if h != prev:
            hold.append((rel(x["t"]), h))
            prev = h
    words = {}
    for x in b:
        if x["addr"] is not None:
            words.setdefault(x["addr"], []).append((rel(x["t"]), x["word"]))
    def edges(a):
        out, pv = [], None
        for t, w in words.get(a, []):
            if w != pv:
                out.append((t, hex(w)))
                pv = w
        return out
    tucnt = words.get(0x90000780, [])
    return dict(cycle=os.path.basename(d.rstrip("/")), on_cmd_strip=on_strip, phc_steps=steps,
                tucnt=[tucnt[0][1], tucnt[-1][1], tucnt[-1][1] - tucnt[0][1]] if tucnt else None,
                holdover_edges=[h for h in hold if h[0] > 0],
                path_gen=sorted({x["kv"].get("AS_PATH_GEN") for x in st}, key=int),
                rst_epoch=sorted({w for t, w in words.get(0x90000720, [])}),
                linkg_edges=[e for e in edges(0x90000774) if e[0] > -1],
                crft_ctrl_edges=[e for e in edges(0x90000750) if e[0] > -1][:8])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    for d in sys.argv[1:]:
        print(json.dumps(cycle(d)))
