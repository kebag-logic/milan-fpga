#!/usr/bin/env python3
"""Classify r3_cluster_probe.py deviations by what went wrong.

Usage: python3 -I r3_classify.py <r3_cluster_probe.log>
"""
import collections
import json
import sys

out = collections.Counter()
examples = {}
for line in open(sys.argv[1]):
    if line.startswith("SUMMARY"):
        continue
    pid, tag, obs = line.split(" ", 2)
    v, why, missed, events = json.loads(obs)
    group = pid.split("-")[0]
    if tag != "DEVIATION":
        out[(group, "OK")] += 1
        continue
    kinds = []
    if v != "FAIL":
        kinds.append(f"verdict {v}: {why}")
    if group in ("FB", "SB"):
        at = 3000 + int(pid.rsplit("+", 1)[1])
        ch2 = [e for e in events if e["channel"] == 2]
        if group == "FB" and not any(e["class"] == "bit-flip" and e["capture_index"] == 3000 and e["n"] == 1
                                     for e in ch2):
            kinds.append("the one-word corruption is not reported at its sample")
        big = [e for e in events if e.get("n") in (2048, 4096, 8192)]
        bad_loc = [e for e in big if not (e.get("located_within", [e["capture_index"]] * 2)[0] <= at
                                          <= e.get("located_within", [e["capture_index"]] * 2)[1])]
        if bad_loc:
            kinds.append("a whole-block slip is placed outside its stated location")
        if len(big) < 4:
            kinds.append("the whole-block slip is not reported whole on every channel")
        if any(e["class"] == "bit-flip" and e["capture_index"] != 3000 for e in ch2):
            kinds.append("phantom code-bit corruptions")
    if group == "CF":
        if any(e["class"] in ("dropped", "repeated") for e in events):
            kinds.append("the constant-mask excursion reads as slips")
        else:
            kinds.append("other")
    if group == "CB":
        kinds.append("the code-bit excursion reads as slips")
    key = (group, "; ".join(kinds) or "other")
    out[key] += 1
    examples.setdefault(key, pid)
for key, count in sorted(out.items()):
    print(count, key, examples.get(key, ""))
