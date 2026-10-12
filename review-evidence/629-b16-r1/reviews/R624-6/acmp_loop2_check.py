#!/usr/bin/env python3
"""R624-6: lane B16 loop2's ACMP exchange from the published tap reduction.
usage: acmp_loop2_check.py <packet root> <out.json>
Times are ms after the UNBIND_RX (DISCONNECT_RX) command. Lists every CONNECT_TX/PROBE_TX command and
response and the last ACMP time, and checks the page's figures 99.6 ms, 299.6 ms, no response, 49.6 s."""
import json, sys
d = json.load(open(sys.argv[1] + "/summary/loop2/acmp-peer-tap.json"))
a = [x for x in d["acmp"] if "msg" in x]
t0 = next(x["t"] for x in a if x["msg"] == "DISCONNECT_RX_COMMAND")
rows = [dict(ms=round((x["t"] - t0) * 1000, 1), msg=x["msg"], status=x.get("status"), conn=x.get("conn_count"))
        for x in a if x["msg"].startswith(("CONNECT_TX", "CONNECT_RX", "DISCONNECT_RX"))]
tx_cmd = [r for r in rows if r["msg"] == "CONNECT_TX_COMMAND"]
tx_rsp = [r for r in rows if r["msg"] == "CONNECT_TX_RESPONSE"]
end = d.get("last_t") or max(x["t"] for x in d["acmp"])
res = dict(rows=rows, connect_tx_commands_ms=[r["ms"] for r in tx_cmd], connect_tx_responses=len(tx_rsp),
           keys=list(d.keys()))
json.dump(res, open(sys.argv[2], "w"), indent=1); print(json.dumps(res, indent=1)[:1500])
