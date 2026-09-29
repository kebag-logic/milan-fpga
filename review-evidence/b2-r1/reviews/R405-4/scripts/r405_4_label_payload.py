#!/usr/bin/env python3
"""R405-4: for every AECP GET_COUNTERS / READ_DESCRIPTOR record in the archived
controller transcripts (snapshot.jsonl copies excluded), check that the
descriptor named by the controller's request label ("counter-T-I", "desc-T-I")
equals the descriptor echoed in the response payload.
Usage: r405_4_label_payload.py <author-dir>"""
import collections, glob, json, os, sys
root = sys.argv[1]; agree = collections.Counter(); bad = []
for p in sorted(glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True)):
    if os.path.basename(p) == "snapshot.jsonl": continue
    for line in open(p, encoding="utf-8"):
        if not line.startswith("{"): continue
        d = json.loads(line); r = d.get("response") or {}
        w = str(d.get("what", "")); c = r.get("cmd")
        if c not in ("GET_COUNTERS", "READ_DESCRIPTOR") or not w.startswith(("counter-", "desc-")): continue
        pl = bytes.fromhex(r["payload"]); o = 0 if c == "GET_COUNTERS" else 4
        got = (int.from_bytes(pl[o:o+2], "big"), int.from_bytes(pl[o+2:o+4], "big"))
        want = tuple(int(x) for x in w.split("-")[1:3])
        agree[(c, got == want)] += 1
        if got != want: bad.append((os.path.relpath(p, root), w, got))
print("label vs response descriptor:", dict(agree)); print("disagreements:", bad[:10])
sys.exit(1 if bad else 0)
