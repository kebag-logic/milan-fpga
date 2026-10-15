#!/usr/bin/env python3
"""Lane B17 round 2: the peer's AAF stream on the DUT's link around each cycle's unbind and bind (offline, read-only).

usage: peer_gap_b17.py <tools_dir> <out.json> <capture.pcap>...
Uses ana_b17.py's reader. Times are seconds from the bind's CONNECT_RX_COMMAND on the tap clock; the unbind is
the last DISCONNECT_RX_COMMAND before it. Per capture: every frame the reader yields, and for each graded stream
(the peer's AAF, the DUT's AAF and CRF) its PDU count and its runs without a pause over 50 ms. Any other AVTP
stream is counted under its direction and subtype, without its identifier.
"""
import json
import sys

sys.path.insert(0, sys.argv[1])
from ana_b17 import segments, tap_analysis  # noqa: E402

out = {}
for path in sys.argv[3:]:
    n, streams, acmp = tap_analysis(path)
    cmd = [x for x in acmp if x["msg"] == "CONNECT_RX_COMMAND" and x["port"] == 2][-1]["ns"]
    dcmd = [x for x in acmp if x["msg"] == "DISCONNECT_RX_COMMAND" and x["port"] == 2 and x["ns"] < cmd][-1]["ns"]
    rel = lambda t: (t - cmd) / 1e9
    row = dict(frames=n, unbind_s=rel(dcmd), streams={})
    for (port, sub, _sid), s in streams.items():
        name = {(2, 0x02): "peer-aaf", (3, 0x02): "dut-aaf", (3, 0x04): "dut-crf"}.get((port, sub), f"other-port{port}-{sub:#04x}")
        segs = segments(s["seq"], s["ns"])
        row["streams"][name] = dict(pdus=len(s["ns"]), runs=[dict(first_s=rel(s["ns"][a]), last_s=rel(s["ns"][b - 1]), pdus=b - a) for a, b in segs])
    peer = row["streams"]["peer-aaf"]["runs"]
    row["peer_last_before_bind_s"] = max(x["last_s"] for x in peer if x["last_s"] < 0)
    row["peer_first_after_bind_s"] = min(x["first_s"] for x in peer if x["first_s"] > 0)
    row["peer_pdus_before_bind"] = sum(x["pdus"] for x in peer if x["last_s"] < 0)
    out[path.rsplit("/", 1)[-1].removesuffix(".pcap").removeprefix("645-b17-")] = row
open(sys.argv[2], "w").write(json.dumps(out, indent=1) + "\n")
