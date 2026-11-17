#!/usr/bin/env python3
"""talker_traces.py <milan_dp-dir> <fabric.json> <split.json>: every MSRP Talker attribute (Advertise or Failed) each
half declares, by type and full FirstValue, with its event runs, and each half's Talker messages with their times;
read through the twin's own decoder."""
import sys
from pathlib import Path
here = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(here))
import twin_compare as tc  # noqa: E402
import twin_decode as td  # noqa: E402
import twin_mrp  # noqa: E402
for name, path in (("all-fabric", sys.argv[2]), ("split", sys.argv[3])):
    cap = td.load(Path(path))
    frames = cap.frames.get("MSRP", [])
    attrs = tc.msrp_attributes(frames)
    talkers = {k: v for k, v in attrs.items() if k[0] in (1, 2)}
    print(f"{name}: {len(talkers)} Talker attribute(s)")
    for (kind, value), events in sorted(talkers.items()):
        print(f"  type {kind} ({td.MSRP_TYPES.get(kind)}) value {value}: {td.run_length(events)}")
        for key, seen in twin_mrp.observations(cap, "MSRP").items():
            if key[0] == kind and key[1] == value:
                ms = [(o.ms, o.sent) for o in seen if o.sent is not None]
                print(f"    first {ms[:1]} last {ms[-1:]} messages {len(ms)}")
