#!/usr/bin/env python3
"""Lane B11 (#653, new): render the findings page's per-cycle table and capture-hash table from
summary/o653-grade.json, so every figure on the page comes from the grade. Offline.

usage: o653_tables.py <grade.json> <out.md>
"""
import json
import sys

g = json.load(open(sys.argv[1]))
rows, hashes, ranges = [], [], {}


def rng(key, v):
    if v is None:
        return
    lo, hi = ranges.get(key, (v, v))
    ranges[key] = (min(lo, v), max(hi, v))


for k, v in g.items():
    if k.endswith("/_session"):
        continue
    c, w = v["library"], v["wire"]
    kind = "CRF" if c["listener"] == 1 else "AAF"
    name = v["tag"] + (" (control)" if c["control"] else "")
    up = w.get("unlock_push", {})
    lu = c.get("lib_unlock_update") or {}
    post = c.get("post", {}).get("counters", {})
    flags = "none" if not c.get("library_flagged") else "yes"
    rows.append(f"| {name} | {kind}, {c['listener']} | {c.get('lock_ms')} | {c['hold_ms']} | {w.get('cmd_to_rsp_us')} | "
                f"{w.get('rsp_to_push_us'):,} | {w.get('order')} | {up.get('ML')}/{up.get('MU')}/{up.get('SI')} | "
                f"{w.get('stream_frames_after_cmd'):,} | {lu.get('lib_conn')} | {flags} | "
                f"{post.get('ML')}/{post.get('MU')}/{post.get('SI')} | `{w['sha256'][:12]}` |")
    hashes.append(f"| `{w['capture']}` | {w['bytes']:,} | `{w['sha256']}` |")
    rng(f"{kind}-cmd_to_rsp_us", w.get("cmd_to_rsp_us"))
    rng(f"{kind}-rsp_to_push_us", w.get("rsp_to_push_us"))
    rng(f"{kind}-frames_after_cmd", w.get("stream_frames_after_cmd"))
    rng(f"{kind}-last_frame_ms", w.get("last_stream_frame_after_cmd_ms"))
    rng(f"{kind}-lib_unlock_after_unbind_ms", c.get("lib_unlock_after_unbind_ms"))
    rng(f"{kind}-lib_held_ms", c.get("lib_held_1_0_after_unbind_ms"))
    rng(f"{kind}-lock_ms", c.get("lock_ms"))
    if "control" in w:
        ranges["control"] = w["control"]
    ranges.setdefault("orders", {}).setdefault(w.get("order"), 0)
    ranges["orders"][w.get("order")] += 1
    ranges.setdefault("decoder_orders", {}).setdefault(w.get("decoder_order"), 0)
    ranges["decoder_orders"][w.get("decoder_order")] += 1
    ranges.setdefault("between", {}).setdefault(" / ".join(w.get("frames_between", [])), 0)
    ranges["between"][" / ".join(w.get("frames_between", []))] += 1
    ranges.setdefault("monotonic", set()).add(w.get("tap_time_monotonic_in_file_order"))
hdr = ("| Cycle | Stream, DUT input | MEDIA_LOCKED reported after bind (ms) | Hold (ms) | UNBIND_RX command to response (µs) | "
       "Response to the unlock's GET_COUNTERS (µs) | Order at the DUT's port | Pushed LOCKED/UNLOCKED/INTERRUPTED | "
       "Stream frames after the command | Library: input state at that update | Library flags | Library pair after | Capture |")
sep = "|" + "|".join(["---"] * (hdr.count("|") - 1)) + "|"
out = ["<!-- per-cycle -->", hdr, sep] + rows + ["", "<!-- hashes -->", "| Capture | Bytes | SHA-256 |", "|---|---|---|"] + hashes
ranges["monotonic"] = sorted(ranges["monotonic"])
out += ["", "<!-- ranges -->", "```", json.dumps(ranges, indent=1), "```"]
open(sys.argv[2], "w").write("\n".join(out) + "\n")
print("\n".join(out))
