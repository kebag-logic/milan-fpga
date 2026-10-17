"""Count the DUT stream's AAF packets on the peer-link tap between each received CONNECT_RX_COMMAND
and its CONNECT_RX_RESPONSE, and between each DISCONNECT_RX_RESPONSE + 0.5 s and the next command.
usage: probe_aaf_between.py <author_tools_pr2_dir> <rA peer-link pcap>"""
import sys
import numpy as np
sys.path.insert(0, sys.argv[1])
import b21_restart_bound as b
acmp, t, n = b.tap(sys.argv[2])
cmd = [m["t"] for m in acmp if m["mt"] == 6 and m["port"] == 2]
rsp = [m["t"] for m in acmp if m["mt"] == 7 and m["port"] == 3]
dsc = [m["t"] for m in acmp if m["mt"] == 9 and m["port"] == 3]
print("aaf packets", len(t), "cmd", len(cmd), "rsp", len(rsp), "dsc", len(dsc))
for i, d in enumerate(dsc):
    tc = min(x for x in cmd if x > d); tr = min(x for x in rsp if x > d)
    between = int(((t > tc) & (t < tr)).sum()); hold = int(((t > d + int(0.5e9)) & (t < tc)).sum())
    last_before = int(t[t < tc].max()) if (t < tc).any() else None
    print(i + 1, "aaf_between_cmd_rsp", between, "aaf_in_hold_after_0.5s", hold,
          "last_aaf_after_disc_ms", round((last_before - d) / 1e6, 2) if last_before else None)
