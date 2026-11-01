#!/usr/bin/env python3
"""Drive b8_ctl.py's agent on the controller host for one stream connection, peer STREAM_OUTPUT 0 to the Arty's STREAM_INPUT 0. Only the Arty's listener format is set. usage: connect.py <hold_s>; prints the agent's JSON."""
import json, subprocess, sys, time
hold = float(sys.argv[1]); fmt = sys.argv[2]
PEER = "3cc0c60102030000"; DUT = "020000fffe000002"
p = subprocess.Popen(["ssh", "-o", "BatchMode=yes", "<bench-host-prefix>pw1", "cd a725b; sudo -n python3 -u b8_ctl.py agent <host-iface> 3cc0c60102030000 3c:c0:c6:01:02:03"], stdin=subprocess.PIPE, text=True)
def op(**q):
    p.stdin.write(json.dumps(q) + "\n"); p.stdin.flush(); time.sleep(0.4)
try:
    time.sleep(1.5)
    op(op="fmt", who="peer", dir="out", idx=0)
    op(op="fmt", who="dut", dir="in", idx=0)
    op(op="counters", who="dut", dtype=5, idx=0)
    op(op="counters", who="peer", dtype=6, idx=0)
    op(op="setfmt", who="dut", idx=0, fmt=fmt)
    op(op="fmt", who="dut", dir="in", idx=0)
    op(op="bind", t=PEER, tu=0, l=DUT, lu=0)
    op(op="tx", who="peer", idx=0)
    t = time.time()
    while time.time() - t < hold:
        time.sleep(min(10, hold))
        op(op="rx", who="dut", idx=0)
        op(op="counters", who="dut", dtype=5, idx=0)
        op(op="counters", who="dut", dtype=0x24, idx=0)
    op(op="counters", who="peer", dtype=6, idx=0)
    op(op="tx", who="peer", idx=0)
    op(op="unbind", t=PEER, tu=0, l=DUT, lu=0)
    op(op="tx", who="peer", idx=0)
    op(op="rx", who="dut", idx=0)
    op(op="counters", who="dut", dtype=5, idx=0)
    op(op="quit")
finally:
    p.stdin.close(); p.wait(timeout=20)
