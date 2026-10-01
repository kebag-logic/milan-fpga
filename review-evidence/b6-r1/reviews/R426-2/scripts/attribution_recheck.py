#!/usr/bin/env python3
"""Re-derive the page's attribution statements from the published grades only
(summary/<case>/events.csv and grade.json; the raw read times are not published).
Usage: attribution_recheck.py <author/summary dir>"""
import csv, json, os, statistics, sys
S = sys.argv[1]
CASES = ["a0", "a1", "a2", "bint", "bcrf"]
def load(c):
    ev = list(csv.DictReader(open(os.path.join(S, c, "events.csv"))))
    for e in ev:
        for k in ("capture_frame", "frame", "frames", "step", "invalid_between"):
            e[k] = int(e[k])
        e["read_jump_ms"] = float(e["read_jump_ms"]) if e["read_jump_ms"] else None
    return ev, json.load(open(os.path.join(S, c, "grade.json")))
for c in CASES:
    ev, g = load(c)
    print(f"===== {c}: events {len(ev)}")
    cp = [e for e in ev if e["cause"] == "capture path"]
    skips = [e for e in cp if e["kind"] == "skip"]
    off = [(e["frames"], e["frames"] % 48, e["cluster"]) for e in skips if e["frames"] % 48 != 12]
    print(f"capture-path skips {len(skips)}; not 48n+12: {off}")
    print(f"capture-path skips at 48n+13: {[e['frames'] for e in skips if e['frames'] % 48 == 13]}; at 48n+11: {[e['frames'] for e in skips if e['frames'] % 48 == 11]}")
    print(f"capture-path repeats: {[(e['frames'], e['cluster']) for e in cp if e['kind'] != 'skip']}")
    cl = g["skip_clusters"]
    bases = {}
    for x in cl:
        bases.setdefault(x["basis"], []).append(x)
    for b, xs in bases.items():
        print(f"basis '{b}': {len(xs)} clusters; capture_path={[x['capture_path'] for x in xs].count(True)}")
        if b != "read-time rise":
            for x in xs:
                print(f"   cluster {x['cluster']} steps {x['steps']} rise {x['read_rise_ms']} gap {x['recent_read_gap_ms']} sig {x['size_signature']} mod48 {[s % 48 for s in x['steps'] if s > 0]}")
    rise_ok = [x for x in cl if x["basis"] == "read-time rise" and x["capture_path"]]
    rs = [s for x in rise_ok for s in x["steps"] if s > 0]
    print(f"skips in rise-matched clusters {len(rs)}; 48n+12 {sum(1 for s in rs if s % 48 == 12)}; others {[s for s in rs if s % 48 != 12]}")
    small = [x for x in cl if x["capture_path"] and x["lost_frames"] < 98]
    print(f"capture clusters lost<98: {len(small)}: " + "; ".join(f"c{x['cluster']} steps {x['steps']} lost {x['lost_frames']} rise {x['read_rise_ms']} gap {x['recent_read_gap_ms']} basis {x['basis']}" for x in small))
    print(f"smallest capture-cluster loss {min(x['lost_frames'] for x in cl if x['capture_path'])}; smallest capture skip {min(e['frames'] for e in skips)}")
    print(f"non-capture clusters: {[x['cluster'] for x in cl if not x['capture_path']]}")
    # one-frame events and causes
    kinds = {}
    for e in ev:
        kinds[(e["cause"], e["kind"], e["frames"] if e["frames"] < 3 else '>=3')] = kinds.get((e["cause"], e["kind"], e["frames"] if e["frames"] < 3 else '>=3'), 0) + 1
    print("cause/kind/size counts:", dict(sorted(kinds.items(), key=str)))
    for cause in ("listener", "DUT beat"):
        xs = [e for e in ev if e["cause"] == cause]
        m = [e["read_jump_ms"] for e in xs if e["read_jump_ms"] is not None]
        if xs:
            print(f"{cause}: {len(xs)} events, measurable rise {len(m)}; median {statistics.median(m) if m else None}; "
                  f"max |rise| {max(abs(v) for v in m) if m else None}; |rise|>1.01 ms: {sorted(round(v,4) for v in m if abs(v) > 1.01)}")
