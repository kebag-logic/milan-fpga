#!/usr/bin/env python3
"""Reviewer probe (portable): regrade code-arm captures kept by code_probe.py, with and without the new
Join-interval check, and list each arm's first MSRP/MVRP frames with the cause the grade attributes.

usage: python3 -B probe_regrade.py MILAN_DP_DIR WORK_DIR ARM [ARM ...]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import srptx_grade as g  # noqa: E402

work = Path(sys.argv[2])
for arm in sys.argv[3:]:
    caps = sorted((work / arm).glob("*.json"))
    if not caps:
        print(f"== {arm}: no capture")
        continue
    cap = g.load(caps[0])
    full = g.grade(cap)[0]
    saved = g.JOIN_BOUNDS_MS
    g.JOIN_BOUNDS_MS = (-1e12, 1e12)
    ablated = g.grade(cap)[0]
    g.JOIN_BOUNDS_MS = saved
    new = [f for f in full if "outside JoinTime's range widened by T_svc" in f]
    print(f"== {arm} ({caps[0].name}): {len(full)} finding(s), {len(new)} by the new Join-interval words; "
          f"with the new check removed: {len(ablated)} finding(s)")
    for f in ablated[:3]:
        print("   ablated:", f[:180])
    for proto in g.APPLICATIONS:
        frames = [f for f in cap.mrpdus if f.proto == proto and not f.error and not cap.queued(f)]
        cause = g.causes(cap, proto, frames)
        row = [f"{f.us / 1000:.3f}:{c[0] if c else 'none'}" for f, c in zip(frames[:12], cause[:12])]
        print(f"   {proto} first frames (ms:cause): {' '.join(row)}")
        gaps = [(b.us - a.us) / 1000 for a, b in zip(frames, frames[1:])]
        short = [x for x in gaps if x < g.JOIN_BOUNDS_MS[0]]
        none_n = sum(1 for c in cause if c is None)
        print(f"   {proto}: {len(frames)} frames, {none_n} with no timer cause, {len(short)} gaps under "
              f"{g.JOIN_BOUNDS_MS[0]} ms (any cause), min gap {min(gaps):.3f} ms")
