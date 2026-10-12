#!/usr/bin/env python3
"""Analyse per-notification times (NOTE,type,index,recipient,cycle) printed by the
reviewer-instrumented fixture copy. 1 s = 1,000,000 cycles. Reports, per row,
the times, the five fixed-window bins, and whether an empty window follows a
steady (<= 1000 ms + service) gap, i.e. a window-edge drift crossing."""
import sys, collections
SEC = 1_000_000
def main(path):
    rows = collections.defaultdict(list)
    for line in open(path):
        if line.startswith("NOTE,"):
            _, ty, s, r, at = line.strip().split(",")
            rows[(int(ty), int(s), int(r))].append(int(at))
    print("type,index,recipient,bins,times_s,empty_windows_between_notifications,min_edge_margin_ms_graded")
    crossings = 0
    for key in sorted(rows):
        t = rows[key]
        bins = [0]*5
        for a in t:
            if a // SEC < 5: bins[a // SEC] += 1
        empty_between = [w for w in range(5) if bins[w] == 0 and any(a < w*SEC for a in t) and any(a >= (w+1)*SEC for a in t)]
        crossings += len(empty_between)
        margin = min((min(a % SEC, SEC - a % SEC) for a in t if 2 <= a // SEC < 5), default=None)
        print(f"{key[0]},{key[1]},{key[2]},{'/'.join(map(str,bins))},{' '.join(f'{a/SEC:.6f}' for a in t)},{empty_between},{margin/1000 if margin is not None else ''}")
    print(f"TOTAL rows={len(rows)} empty-window-between-notifications={crossings}")
main(sys.argv[1])
