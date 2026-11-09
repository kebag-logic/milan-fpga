#!/usr/bin/env python3
"""Compare the leave-all-omission plant's capture with an independent probe's and with the unplanted capture.

usage: compare_omission_frames.py SPLIT.json PLANTED.json PROBE.json
Prints each frame index whose bytes differ from the unplanted capture, in each, and whether the plant and
the probe are byte-identical frame for frame.
"""
import json
import sys

base, plant, probe = (json.load(open(p)) for p in sys.argv[1:4])
for name, doc in (("plant", plant), ("probe", probe)):
    diffs = [(i, e["ms"]) for i, (e, b) in enumerate(zip(doc["frames"], base["frames"])) if e["hex"] != b["hex"]]
    print(f"{name}: {len(doc['frames'])} frames ({len(base['frames'])} unplanted), changed {diffs}")
    for i, _ in diffs:
        print(f"  unplanted {len(base['frames'][i]['hex'])//2} bytes, {name} {len(doc['frames'][i]['hex'])//2} bytes")
same = [a["hex"] == b["hex"] for a, b in zip(plant["frames"], probe["frames"])]
print(f"plant == probe frame for frame: {all(same) and len(plant['frames']) == len(probe['frames'])}")
