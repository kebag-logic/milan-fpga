#!/usr/bin/env python3
"""Print every endpoint's record figures, notes and per-scope LUT/RAMB from a resource baseline JSON."""
import json, sys
d = json.load(open(sys.argv[1]))
for ep, e in d["endpoints"].items():
    print("==", ep, "keys:", sorted(e.keys()))
    for k, v in e.items():
        if k != "record":
            print("  ", k, "=", json.dumps(v)[:400])
    r = e["record"]
    print("  record keys:", sorted(r.keys()))
    for k, v in r.items():
        if k not in ("scopes", "identity"):
            print("  rec.", k, "=", json.dumps(v)[:600])
    print("  identity:", json.dumps(r.get("identity"))[:1500])
    for s, f in sorted(r.get("scopes", {}).items()):
        print("   scope %-45s LUT %6s FF %6s R36 %s R18 %s DSP %s" % (s, f.get("LUT"), f.get("FF"), f.get("RAMB36"), f.get("RAMB18"), f.get("DSP")))
