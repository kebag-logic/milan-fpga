#!/usr/bin/env python3
"""Cycle-22 event timeline, bind PROBE timing, baseline/final captures.
Usage: cycle22_and_binds.py <packet author dir>"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import replay_b2 as R
pkt = Path(sys.argv[1])


def sid(v):
    """Print the DUT's synthetic stream IDs; mask any other (peer) identity."""
    return v if v in ("None", "") or v.startswith("020000") else "<peer-stream-id>"


d = pkt / "cycles" / "cycle-022"
m = R.tsv(d / "msrp.tsv"); a = R.tsv(d / "acmp.tsv"); an = json.load(open(d / "analysis.json"))
disc = an["disconnect_response_s"]
print("cycle 22, seconds after DISCONNECT_RX response:")
for r in m:
    if -0.5 < r["t"] - disc < 2.1:
        print(f"  MSRP {r['t'] - disc:+.6f} {r['sender']} {r['type']} {r['event']} {sid(r['stream_id'])}")
for r in a:
    print(f"  ACMP {r['t'] - disc:+.6f} {r['sender']} mt={r['mt']} status={r['status']}")
own = [r["t"] for r in m if r["sender"] == "DUT" and r["event"] == "LeaveAll" and abs(r["t"] - disc) < 0.1]
lv = disc + an["bridge_lv_after_disconnect_s"]
types = sorted({r["type"] for r in m if r["sender"] == "DUT" and r["event"] == "LeaveAll" and r["t"] == own[0]})
print("  own LeaveAll minus Lv, ms:", round((own[0] - lv) * 1e3, 6), "types", types)
print("  hold_pdus", an["hold_pdus"], "stopped", an["stopped"], "START/STOP delta", an["dut_out1_start_stop_delta"])
print("bind PROBE timing after CONNECT_RX response (us):")
for b in range(1, 6):
    an = json.load(open(pkt / "bind" / f"bind-{b}" / "analysis.json"))
    pe = an["probe_exchanges"]
    print(f"  bind {b}: cmd {pe[0]['after_response_s']*1e6:.1f} us, resp {pe[1]['after_response_s']*1e6:.1f} us "
          f"(+{(pe[1]['after_response_s']-pe[0]['after_response_s'])*1e6:.1f}), status {pe[1]['status']}, "
          f"ready->pdu {an['ready_to_first_pdu_s']*1e3:.3f} ms, dmac {an['settled_listener_state']['dmac']}")
for name in ("baseline", "final"):
    d = pkt / "bind" / name
    an = json.load(open(d / "analysis.json"))
    m = R.tsv(d / "msrp.tsv")
    dut = sorted({r["t"] for r in m if r["sender"] == "DUT"})
    gaps = [round(y - x, 4) for x, y in zip(dut, dut[1:])]
    ta = {}
    for r in m:
        if r["sender"] == "DUT" and r["type"] == "TalkerAdvertise":
            ta[r["event"]] = ta.get(r["event"], 0) + 1
    keys = [k for k in an if "pdu" in k.lower() or "crf" in k.lower() or "target" in k.lower()]
    print(f"{name}: span {an['capture_span_s']:.3f} s, DUT PDU spacing min/max {min(gaps)}/{max(gaps)}, "
          f"DUT TA events {ta}, " + ", ".join(f"{k}={an[k]}" for k in keys))
