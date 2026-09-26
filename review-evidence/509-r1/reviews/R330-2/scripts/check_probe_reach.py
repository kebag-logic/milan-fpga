#!/usr/bin/env python3
"""Check that each accepted YAML probe's mutation is visible in its decoded packed rows."""
import json
import sys

r = json.load(open(sys.argv[1]))
probes = {p["probe"]: p for p in r["config_probes"]}


def rows(label, t):
    return [x for x in probes[label]["rows"] if x["type"] == t]


print("buffer:", [x["fields"]["buffer_ns"] for x in rows("buffer one ns below floor", 5)])
print("crf word in:", [x["fields"]["formats"] for x in rows("non-Milan CRF word", 5)],
      "out:", [x["fields"]["formats"] for x in rows("non-Milan CRF word", 6)])
print("48 out formats:", [(x["fields"]["formats_count"], x["length"]) for x in rows("48 AAF output formats", 6)])
print("mixed out:", [x["fields"]["formats"] for x in rows("mixed output format families", 6)])
l6 = probes["outputs without INTERNAL"]
print("L6 sources:", [(x["index"], x["fields"]) for x in rows("outputs without INTERNAL", 10)],
      "domain:", [x["fields"] for x in rows("outputs without INTERNAL", 36)],
      "stream outputs:", len(rows("outputs without INTERNAL", 6)))
for lab in ("zero model ID pin", "all-ones model ID pin"):
    print(lab, rows(lab, 0)[0]["fields"]["model_id"])
