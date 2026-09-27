#!/usr/bin/env python3
"""[R362] round-2: re-run the UNCHANGED round-1 oracle probe with spanning captures.

Usage: python3 -B round1_span_shim.py <repo-checkout>

Round 2 (item 7) makes check_release_mr return NOT RUN unless the capture spans
[first read - 1 s - R, last read]. The round-1 probe's short synthetic traces
pass capture_complete=True, so every mr case now reads NOT RUN. This shim
executes probes/round1/oracle_probe.py unchanged, except that after the planner
is loaded, check_release_mr is wrapped: when capture_complete is exactly True
and the stream's records are well formed, it becomes
ReleaseCapture((min(first read - 1 - R, first PDU), max(last read, last PDU))).
Every other call, including all malformed/fuzz inputs, passes through untouched.
"""
from __future__ import annotations

import sys
from pathlib import Path

HOOK = '''
_orig_mr = tc.check_release_mr
def _spanning_mr(stream_id, pdus, causes, media_reset_reads, *, observation_resolution_s, capture_complete):
    try:
        if capture_complete is True:
            rs = [r for r in media_reset_reads if r["stream_id"] == stream_id]
            ps = [p["timestamp_s"] for p in pdus if p["stream_id"] == stream_id]
            lo = rs[0]["timestamp_s"] - 1 - observation_resolution_s - 1e-9
            hi = rs[-1]["timestamp_s"]
            if ps:
                lo, hi = min(lo, min(ps)), max(hi, max(ps))
            capture_complete = tc.ReleaseCapture((lo, hi))
    except Exception:
        pass
    return _orig_mr(stream_id, pdus, causes, media_reset_reads,
                    observation_resolution_s=observation_resolution_s, capture_complete=capture_complete)
tc.check_release_mr = _spanning_mr
'''


def main() -> None:
    probe = Path(__file__).resolve().parent / "round1" / "oracle_probe.py"
    source = probe.read_text(encoding="utf-8")
    anchor = "spec.loader.exec_module(tc)\n"
    assert source.count(anchor) == 1
    code = compile(source.replace(anchor, anchor + HOOK), str(probe), "exec")
    sys.argv = [str(probe)] + sys.argv[1:]
    exec(code, {"__name__": "__main__", "__file__": str(probe)})


if __name__ == "__main__":
    main()
