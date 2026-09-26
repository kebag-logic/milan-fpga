#!/usr/bin/env python3
"""Summarize an audit receipt into the quantities the reference page states.

Usage: summarize_audit.py <receipt.json>
Prints per-configuration descriptor/field summaries for manual comparison.
"""
import json
import sys
from collections import Counter

NAMES = {0: "ENTITY", 1: "CONFIGURATION", 2: "AUDIO_UNIT", 5: "STREAM_INPUT", 6: "STREAM_OUTPUT",
         9: "AVB_INTERFACE", 10: "CLOCK_SOURCE", 14: "STREAM_PORT_INPUT", 15: "STREAM_PORT_OUTPUT",
         20: "AUDIO_CLUSTER", 23: "AUDIO_MAP", 26: "CONTROL", 36: "CLOCK_DOMAIN"}
CRF = "0x041060010000BB80"


def main() -> None:
    report = json.load(open(sys.argv[1]))
    for cfg in report["configurations"]:
        rows = cfg["rows"]
        counts = Counter(NAMES.get(r["type"], hex(r["type"])) for r in rows)
        print("==", cfg["config"], "descriptors", len(rows), "bytes", cfg["image_bytes"], "sha", cfg["sha256"])
        print("   counts", dict(counts))
        print("   model_id", cfg["model_id"], "adp", cfg["adp"])
        lengths = {}
        for r in rows:
            lengths.setdefault(NAMES.get(r["type"], hex(r["type"])), set()).add(r["length"])
        print("   lengths", {k: sorted(v) for k, v in lengths.items()})
        for r in rows:
            t, f = r["type"], r["fields"]
            if t == 0:
                print("   ENTITY", f)
            elif t == 1:
                print("   CONFIGURATION len", r["length"], f)
            elif t == 2:
                print("   AUDIO_UNIT off", r["image_offset"], "len", r["length"],
                      {k: f[k] for k in ("rates_offset", "rates_count", "rates", "current_rate")})
            elif t == 36:
                print("   CLOCK_DOMAIN off", r["image_offset"], "len", r["length"], f)
            elif t == 10:
                print("   CLOCK_SOURCE", r["index"], "len", r["length"], f)
            elif t in (5, 6):
                kind = "CRF" if f["formats"] == [CRF] else "AAF"
                print("  ", NAMES[t], r["index"], kind, "len", r["length"],
                      {k: f[k] for k in ("formats_offset", "formats_count", "flags", "buffer_ns",
                                         "redundant_offset", "redundant_count", "timing")},
                      "cur==first", f["current_format"] == f["formats"][0], f["formats"])
            elif t == 9:
                print("   AVB_INTERFACE", r["index"], "len", r["length"], f)
            elif t == 26:
                print("   CONTROL", r["index"], "len", r["length"], f)
            elif t in (14, 15):
                print("  ", NAMES[t], r["index"], "len", r["length"], f)
            elif t == 23:
                print("   AUDIO_MAP", r["index"], "len", r["length"], "off", f["mappings_offset"],
                      "n", f["mappings_count"], f["mappings"])
        chans = Counter(r["fields"]["channel_count"] for r in rows if r["type"] == 20)
        clen = Counter(r["length"] for r in rows if r["type"] == 20)
        print("   AUDIO_CLUSTER channel_count", dict(chans), "lengths", dict(clen))


if __name__ == "__main__":
    main()
