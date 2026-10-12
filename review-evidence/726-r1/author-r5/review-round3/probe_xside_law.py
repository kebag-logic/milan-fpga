#!/usr/bin/env python3
"""Show how the bench grader's cross-device stream-counter helpers grade the
ruled per-AVTPDU law versus a regression to one count per interval.
Usage: python3 -I -B probe_xside_law.py <clone>"""
import importlib.util, json, sys
from pathlib import Path
clone = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("tc", clone / "tb/tools/torture_campaign.py")
tc = importlib.util.module_from_spec(spec); sys.modules["tc"] = tc; spec.loader.exec_module(tc)
W = 4.0
cases = {
    "ruled: DUT talker FRAMES_TX and peer listener FRAMES_RX both per AVTPDU (8000/s)": (32000, 32000),
    "regression: DUT talker FRAMES_TX one per interval, peer listener per AVTPDU": (4, 32000),
    "regression: both sides one per interval": (4, 4),
}
for name, (t, l) in cases.items():
    v, d = tc.interval_ticks_agree(t, l, window_s=W)
    print(json.dumps({"case": name, "talker": t, "listener": l, "verdict": v,
                      "talker_semantics": d.get("talker_semantics"),
                      "listener_semantics": d.get("listener_semantics"),
                      "peer_findings": [(f["role"], f["counter"]) for f in d.get("peer_findings", [])],
                      "why": d.get("why")}))
for src in ("stream_output", "stream_input"):
    try:
        tc.assert_frame_accurate(src); print(json.dumps({"assert_frame_accurate": src, "result": "accepted"}))
    except tc.CounterSemanticError as e:
        print(json.dumps({"assert_frame_accurate": src, "result": "CounterSemanticError", "msg": str(e)[:160]}))
print(json.dumps({"grade_counter_semantics FRAMES_RX 4/4s flowing": tc.grade_counter_semantics("FRAMES_RX", 4, 4.0, stream_flowing=True)[0],
                  "grade_counter_semantics FRAMES_RX 32000/4s flowing": tc.grade_counter_semantics("FRAMES_RX", 32000, 4.0, stream_flowing=True)[0]}))
print(json.dumps({"A_XSIDE_INTERVAL_AGREE": tc.A_XSIDE_INTERVAL_AGREE.name, "in LICENSED_STREAMING_ASSERTS": tc.A_XSIDE_INTERVAL_AGREE in tc.LICENSED_STREAMING_ASSERTS}))
