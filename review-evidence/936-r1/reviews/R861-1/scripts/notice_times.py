"""Print the send millisecond and recipient of each unsolicited GET_STREAM_INFO notice of STREAM_OUTPUT 0 in the
twin's two captures, side by side, with the split's lag behind the fabric's.

usage: python3 -I notice_times.py <milan_dp dir at the reviewed head> <fabric.json> <split.json>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import twin_plants  # noqa: E402  (the head's own capture readers)


def rows(doc: dict) -> list[tuple[int, str]]:
    out = []
    for e in twin_plants.output_notices(doc):
        f = twin_plants.aecp_doc_frame(e)
        out.append((e["ms"], f"{getattr(f, 'controller', 0):016x}"))
    return out


fabric = rows(json.loads(Path(sys.argv[2]).read_text()))
split = rows(json.loads(Path(sys.argv[3]).read_text()))
print(f"fabric notices: {len(fabric)}  split notices: {len(split)}")
for k in range(max(len(fabric), len(split))):
    a = fabric[k] if k < len(fabric) else None
    b = split[k] if k < len(split) else None
    lag = (b[0] - a[0]) if a and b else None
    print(f"{k}: fabric {a}  split {b}  split-minus-fabric ms {lag}")
