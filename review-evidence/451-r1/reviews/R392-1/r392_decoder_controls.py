#!/usr/bin/env python3
"""Planted controls for r392_decode.py: each mutation must move the decode."""
import json, subprocess, sys, os
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
src, work = sys.argv[1], sys.argv[2]
base = np.fromfile(src, dtype="<u4").reshape(-1, 8)
def run(w, name):
    p = os.path.join(work, name + ".raw"); w.astype("<u4").tofile(p)
    r = json.loads(subprocess.run([sys.executable, os.path.join(here, "r392_decode.py"), "raw", p],
                                  check=True, capture_output=True, text=True).stdout)
    os.remove(p); return r
res = {}
r = run(base, "clean"); res["clean"] = (r["region_torn_frames"], r["region_invalid_words"], r["per_channel"][0]["tag_hist"])
w = np.roll(base, 1, axis=1); r = run(w, "rotated")
res["slot_rotation_detected"] = r["own_tag_region"] is None
w = base.copy(); w[70000, 5] = (w[70000, 5] + (1 << 8)) & 0xFFFFFFFF; r = run(w, "torn")
res["one_torn_frame_detected"] = r["region_torn_frames"] == 1
w = base.copy(); w[70000, 3] |= 0x01; r = run(w, "lowbyte")
res["low_byte_violation_detected"] = r["own_tag_region"] is not None and (r["region_invalid_words"] >= 1 or r["own_tag_region"] != [0, base.shape[0]-1])
w = np.delete(base, 90000, axis=0); r = run(w, "drop")
res["single_drop_counted"] = r["frame_continuity_ch0"]["total_dropped"] == run(base, "c2")["frame_continuity_ch0"]["total_dropped"] + 1
ok = all(v for k, v in res.items() if k != "clean")
res["all_controls_fired"] = ok
json.dump(res, sys.stdout, indent=1); print()
sys.exit(0 if ok else 1)
