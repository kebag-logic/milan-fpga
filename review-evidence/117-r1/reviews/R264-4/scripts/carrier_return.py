#!/usr/bin/env python3
"""Switch port 8 carrier return (controller-host watcher, NTP) after the ON
command (power-strip host, NTP), and the switch's first frame on the DUT link
after that carrier return. usage: carrier_return.py <bench-a202 root>"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rederive_step3 import offsets, ptp_records  # noqa: E402

root = os.path.join(sys.argv[1], "bench")
for c in range(1, 7):
    d = os.path.join(root, f"cycle{c}")
    ps = open(os.path.join(d, "powerstrip.txt")).read()
    t_on = float(re.search(r"T_ON_CMD (\S+)", ps).group(1))
    t_off = float(re.search(r"T_OFF_CMD (\S+)", ps).group(1))
    off = offsets(os.path.join(d, "clock-before.jsonl"))
    srv = [v for k, v in off.items() if k.startswith("ubuntu")][0]
    car = [json.loads(l) for l in open(os.path.join(d, "pw1-watch.jsonl")) if '"carrier"' in l]
    back = next(x["t"] for x in car if x["value"] == 1 and x["t"] > t_on)
    lost = next(x["t"] for x in car if x["value"] == 0 and x["t"] > t_off)
    # tap times are on the capture server (NTP) clock after ptp_records' fit
    first = min(t for t, port, fr in ptp_records(os.path.join(d, f"tap-c{c}.pcap")) if port == 2 and t > t_on)
    print(f"cycle {c}: carrier lost {lost - t_off:.2f} s after OFF; carrier back {back - t_on:.2f} s after ON; switch first frame on DUT link {first - back:.2f} s after carrier")
