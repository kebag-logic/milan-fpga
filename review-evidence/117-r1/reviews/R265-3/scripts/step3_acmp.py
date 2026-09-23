#!/usr/bin/env python3
"""ACMP frames and first CRF PDU on the DUT link around each bound cycle (4 to 6).

Usage: step3_acmp.py <evidence-root: .../review-evidence/117-r1>
Times: seconds after the outlet-off command, build-box clock (see step3_rederive.py).
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step3_rederive as s  # noqa: E402

ACMP = {0: "CONNECT_TX_COMMAND", 1: "CONNECT_TX_RESPONSE", 2: "DISCONNECT_TX_COMMAND", 3: "DISCONNECT_TX_RESPONSE",
        4: "GET_TX_STATE_COMMAND", 5: "GET_TX_STATE_RESPONSE", 6: "CONNECT_RX_COMMAND", 7: "CONNECT_RX_RESPONSE",
        8: "DISCONNECT_RX_COMMAND", 9: "DISCONNECT_RX_RESPONSE", 10: "GET_RX_STATE_COMMAND", 11: "GET_RX_STATE_RESPONSE"}
root = sys.argv[1]
for c in (4, 5, 6):
    cdir = os.path.join(root, "bench-a202", "bench", f"cycle{c}")
    offs = s.offsets(cdir)
    off_pi = [v for h, v in offs.items() if h.endswith("pi")][0]
    off_srv = [v for h, v in offs.items() if "server" in h][0]
    t_off, t_on = s.strip_times(cdir)
    T0 = t_off - off_pi
    taps, _ = s.tap(cdir, f"tap-c{c}.pcap")
    tp = [(x - off_srv - T0, p, d) for x, p, d in taps]
    con = [(ts - T0, f) for ts, f in s.console(cdir)]
    allgood = None
    for i in range(len(con) - 1, -1, -1):
        f = con[i][1]
        if not (f["GPTP_GM"] == s.GM_SW and f["SYNC"] == "1" and f["ASCAPABLE"] == "1" and f["TU"] == "0"):
            allgood = con[i + 1][0]
            break
    loss = [t for t, f in con if f["SYNC"] == "0"][0]
    ctx = [(t, p) for t, p, d in tp if d.get("acmp_msg") == 0]
    kinds = collections.Counter((ACMP.get(d["acmp_msg"]), "to DUT" if p == 2 else "from DUT") for t, p, d in tp if "acmp_msg" in d)
    between = [t for t, p in ctx if p == 2 and loss - 0.2 < t < allgood]
    after = [t for t, p in ctx if p == 2 and t >= allgood]
    before = [t for t, p in ctx if p == 2 and t < loss]
    crf = [t for t, p, d in tp if p == 3 and d.get("subtype") == 0x04]
    crf_after = [t for t in crf if t > allgood]
    print(f"cycle {c}: loss {loss:.2f} all-good {allgood:.2f}; CONNECT_TX to DUT before loss {len(before)}, between loss-0.2 s and all-good {len(between)}, after {len(after)}; first after return {after[0]:.3f}; first CRF PDU after return {crf_after[0]:.3f}")
    print(f"   ACMP message census on the DUT link: {dict(kinds)}")
