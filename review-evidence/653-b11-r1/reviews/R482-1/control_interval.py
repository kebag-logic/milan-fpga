#!/usr/bin/env python3
"""C0: intervals from the probe's own GET_COUNTERS answer to the UNBIND_RX command and
to the UNBIND_RX response, rebuilt from the provided decoder's output (swapped words)
and compared with the grader's own_rsp_to_cmd_us. usage: control_interval.py <author_dir>"""
import json, sys
from pathlib import Path
A = Path(sys.argv[1])
L = (A / "summary/decode/b11-a535-s0b-C0.decode.txt").read_text().splitlines()
t = lambda key: next(float(l.split(" ms ")[0]) for l in L if key(l))
own = t(lambda l: "AECP RSP GET_COUNTERS" in l and "UNSOL" not in l)
cmd = t(lambda l: "ACMP UNBIND_RX_CMD" in l); rsp = t(lambda l: "ACMP UNBIND_RX_RESP" in l)
us = lambda a, b: (round((b - a) * 1e6 / 2**32) % 2**32) / 1e3
g = json.loads((A / "summary/o653-grade.json").read_text())["s0b/C0"]["wire"]["control"]
print(f"own answer -> UNBIND_RX command : {us(own, cmd):.1f} us (grader own_rsp_to_cmd_us = {g['own_rsp_to_cmd_us']})")
print(f"own answer -> UNBIND_RX response: {us(own, rsp):.1f} us")
print("page line 237-238: 'The response came 1,629.8 us after the probe's own GET_COUNTERS answer.'")
ok = round(us(own, cmd), 1) == 1629.8 and round(us(own, rsp), 1) != 1629.8
print("RESULT: the 1,629.8 us figure is the command's interval, not the response's" if ok else "RESULT: page figure matches the response")
