#!/usr/bin/env python3
"""figures.py: each new piece's provisional figure, from its parent leg's hosted figure and the local walls.

A new leg of a suite dealt into a multiple of its old leg count holds a subset of one old leg's cases (round-robin:
names[k::T] is inside names[k % t::t] when t divides T), so on one runner its window is at most that leg's. Its
figure is the old leg's figure times local wall(new) / local wall(old), both measured on equal 4-CPU bookings with
hosted budgets and no compiler cache, rounded up. A leg not measured keeps the old leg's figure (the subset bound).
A newly divided suite (follow_ring, media_phase) scales its whole figure by its piece's wall over the whole suite's.
"""
import math

MEAS = "/data-2/milan/tmp/cicd-a839/r5/meas"
SMOKE = "/data-2/milan/tmp/cicd-a839/r5/smoke"


def wall(path):
    return float(open(path).read().split()[0])


def m(tag):
    return wall(f"{MEAS}/{tag}/time")


rows = []


def scaled(piece, figure, new, old, how):
    value = math.ceil(figure * new / old)
    rows.append((piece, value, f"{figure} x {new:.1f} / {old:.1f} ({how})"))
    return value


def bound(piece, figure, how):
    rows.append((piece, figure, f"{figure}, the old leg's figure ({how})"))
    return figure


mdp = []  # filled below, as capture_coherence's
fr_whole = m("A-make_follow_ring_clean_run")
fr = [scaled(f"follow_ring__{k}", 1493, wall(f"{SMOKE}/{a}/follow_ring__{k}.time"), fr_whole, "piece over whole")
      for k, a in ((0, "F"), (1, "E"))]
mp_whole = m("A-make_media_phase_clean_run")
mp = [scaled(f"media_phase__{k}", 1400, wall(f"{SMOKE}/{a}/media_phase__{k}.time"), mp_whole, "piece over whole")
      for k, a in ((0, "F"), (1, "F"), (2, "E"))]
cc = []
import os


def done(d):
    path = f"{MEAS}/{d}/time"
    return os.path.exists(path) and os.path.getsize(path) > 0


def eight(suite, short, olds_figures, out):
    for k in range(8):
        old = olds_figures[k % 4]
        new_tag, old_tag = f"{short}_{k}_8", f"{short}_{k % 4}_4"
        news = [d for d in os.listdir(MEAS) if d.endswith("-" + new_tag)]
        olds = [d for d in os.listdir(MEAS) if d.endswith("-" + old_tag) and done(d)]
        if news and olds and done(news[0]):
            # where the old leg was measured twice, its faster run: the larger ratio, the larger figure
            out.append(scaled(f"{suite}__{k}", old, m(news[0]), min(m(d) for d in olds),
                              f"{k}/8 over {k % 4}/4, the faster of {len(olds)} reference run(s)"))
        else:
            out.append(bound(f"{suite}__{k}", old, f"subset of old leg {k % 4}"))


eight("milan_dp", "mdp", (1309, 1313, 275, 399), mdp)
eight("capture_coherence", "cc", (1618, 1204, 695, 724), cc)
for piece, value, how in rows:
    print(f"{piece:22} {value:5}  {how}")
print("milan_dp", tuple(mdp))
print("capture_coherence", tuple(cc))
print("follow_ring", tuple(fr))
print("media_phase", tuple(mp))
