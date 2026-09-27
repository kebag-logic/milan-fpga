#!/usr/bin/env python3
"""Build a scorable copy of the round-1 planner (95bea7cf) for the differential probe run.

Usage (from the review clone): round1_head_shim.py <out/torture_campaign.py>
The round-1 planner has no ReleaseCapture or check_release_tu_history. The appended
REVIEWER SHIM (not planner code) supplies both by delegating to the round-1 oracles, so
probe_r2.py can show which round-2 expectations the round-1 head failed.
"""
import subprocess, sys
src = subprocess.run(["git", "show", "95bea7cf82fcf7cf034c156ef7aa6800ee769e05:tb/tools/torture_campaign.py"],
                     capture_output=True, text=True, check=True).stdout
src += '''

# REVIEWER SHIM (not planner code): lets the round-2 probe score the round-1 head.
from dataclasses import dataclass as _dc
@_dc(frozen=True)
class ReleaseCapture:
    window_s: tuple
    complete: bool = True
_orig_mr = check_release_mr
def check_release_mr(stream_id, pdus, causes, reads, *, observation_resolution_s, capture_complete):
    if isinstance(capture_complete, ReleaseCapture):
        capture_complete = capture_complete.complete
    return _orig_mr(stream_id, pdus, causes, reads, observation_resolution_s=observation_resolution_s,
                    capture_complete=capture_complete)
def check_release_tu_history(intervals, disc, *, observation_resolution_s, capture_complete, gm_changes_s):
    if intervals is None:
        return "NOT RUN", {}
    for iv in intervals:
        v, d = check_release_tu(iv, disc, holdover_bound_s=0.5, observation_resolution_s=observation_resolution_s,
                                capture_complete=capture_complete, gm_changes_s=gm_changes_s)
        if v != "PASS":
            return v, d
    return ("PASS" if gm_changes_s is not None else "NOT RUN"), {}
'''
open(sys.argv[1], "w").write(src)
