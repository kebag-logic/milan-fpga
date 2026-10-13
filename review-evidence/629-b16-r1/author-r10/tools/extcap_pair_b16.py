#!/usr/bin/env python3
"""Lane B16 (new, offline): reduce a private all-channel external-capture grade (tone_points_b16.py extcap) to
the two channels that carry the reference peer's digital output, in lane B15's d-extcap-pair.json form. The
pair's indices are passed on the command line from the private record (lane B15 identified them by content
in its pts2 positive control), so neither this file nor its output states the capture's layout.

usage: extcap_pair_b16.py <all.json> <ch_a> <ch_b> <out.json>
"""
import json
import sys

src, a, b, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
g = json.load(open(src))
rows = {r["channel"]: r for r in g["channels"]}
keep = ("frames", "rms_dbfs", "min", "max", "nonzero", "share_997", "share_9973", "tone_997", "tone_9973")
pair = []
for k, c in enumerate((a, b)):
    r = {x: rows[c][x] for x in keep if x in rows[c]}
    r["pair_channel"] = k
    pair.append(r)
others = [r for c, r in rows.items() if c not in (a, b)]
res = dict(point="extcap",
           note="the two channels of the external capture that carry the reference peer's digital output (lane B15's "
                "identification by content); the capture's layout is withheld",
           frames=g["frames"], seconds=g["seconds"], sha256=g["sha256"], rows=pair,
           other_channels=dict(count_carrying_997=sum(1 for r in others if "tone_997" in r),
                               count_carrying_9973=sum(1 for r in others if "tone_9973" in r)),
           verdict="TONE PRESENT" if any("tone_997" in r or "tone_9973" in r for r in pair) else "TONE ABSENT")
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(dict(verdict=res["verdict"], rows=[(r["rms_dbfs"], r["min"], r["max"], r["nonzero"]) for r in pair],
                      other=res["other_channels"])))
