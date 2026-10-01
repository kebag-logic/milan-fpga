#!/usr/bin/env python3
"""A2 and A0 details behind the capture-path section: the 'other ten' skips,
the beat repeats with a read-time rise over 1.05 ms and their distance to the
13.3 s stall, and the 48n+13 skips' clusters.  Usage: a2_detail.py <summary-dir>"""
import csv, json, os, sys
root = sys.argv[1]
for c, ids in (("a2", (13, 15, 36, 46, 55, 56)), ("a0", (0,)), ("a1", (13, 18)), ("bcrf", (5,))):
    g = json.load(open(os.path.join(root, c, "grade.json")))
    ev = list(csv.DictReader(open(os.path.join(root, c, "events.csv"))))
    print("==", c)
    for k in g["skip_clusters"]:
        if k["cluster"] in ids:
            tot = k["net_step"]
            print(f"  cluster {k['cluster']}: steps {k['steps']} net {tot} net%48={tot % 48} loops+{k['whole_loops_added']} "
                  f"lost {k['lost_frames']} lost%48000%48={(k['lost_frames'] % 48000) % 48} rise {k['read_rise_ms']} "
                  f"lost_ms {k['lost_ms']} gap {k['recent_read_gap_ms']} basis {k['basis']!r} first {k['first_frame']}")
    if c == "a2":
        stall = [k for k in g["skip_clusters"] if (k["recent_read_gap_ms"] or 0) > 13000]
        print("  clusters after the 13.3 s stall:", [(k["cluster"], k["first_frame"], k["recent_read_gap_ms"]) for k in stall])
        big = [k for k in g["skip_clusters"] if (k["recent_read_gap_ms"] or 0) > 10000]
        for e in ev:
            if e["cause"] == "DUT beat" and e["read_jump_ms"] not in ("", "None") and abs(float(e["read_jump_ms"])) > 1.05:
                cf = int(e["capture_frame"])
                d = [(k["cluster"], round((cf - k["first_frame"]) / 48000, 3)) for k in big]
                print(f"  beat with rise {e['read_jump_ms']} ms at capture_frame {cf}: offset to long-stall clusters (s) {d}")
