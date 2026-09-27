#!/usr/bin/env python3
"""Residual behaviours recorded for suggestions (no pass/fail expectation).
Usage: residual_probe.py <torture_campaign.py>"""
import importlib.util, sys
spec = importlib.util.spec_from_file_location("tc", sys.argv[1]); tc = importlib.util.module_from_spec(spec)
sys.modules["tc"] = tc; spec.loader.exec_module(tc)
H = tc.check_release_tu_history
for r, clear in ((0.001, 0.249), (0.1, 0.15), (0.24, 0.01), (0.24, 0.0099)):
    v, d = H([(0, clear)], [], observation_resolution_s=r, capture_complete=True, gm_changes_s=[0])
    print(f"S2 tu minimum: R={r} GM at 0, tu cleared at {clear} s -> {v}")
v, d = H([(0, 0.1)], [0], observation_resolution_s=0.001, capture_complete=True, gm_changes_s=[])
print(f"R362-1 S4 (retained): GM edge supplied only as a discontinuity, gm_changes_s=[], tu held 0.1 s -> {v}")
pdus = [{"stream_id": "s", "timestamp_s": -1.2 + i * 0.05, "pdu_index": i, "mr": int(i >= 30)} for i in range(40)]
v, d = tc.check_release_mr("s", pdus, [{"stream_id": "s", "timestamp_s": 0.3, "kind": "CRF disruption"}],
                           [{"stream_id": "s", "timestamp_s": 0, "value": 0}, {"stream_id": "s", "timestamp_s": 0.9, "value": 0}],
                           observation_resolution_s=0.001, capture_complete=tc.ReleaseCapture((-2, 2)))
print(f"R362-1 S2 (retained): caused toggle, MEDIA_RESET flat 0 -> 0 -> {v}")
for label, call in (("check_release_tu missing GM history", lambda: tc.check_release_tu((0, 0.3), [0], holdover_bound_s=0.5, observation_resolution_s=0.001, capture_complete=True, gm_changes_s=None)),
                    ("check_release_mr incomplete capture", lambda: tc.check_release_mr("s", pdus, [], [], observation_resolution_s=0.001, capture_complete=False))):
    v, d = call()
    print(f"S1 limit field on early NOT RUN: {label} -> {v}; resolution_limit_s present={'resolution_limit_s' in d}")
