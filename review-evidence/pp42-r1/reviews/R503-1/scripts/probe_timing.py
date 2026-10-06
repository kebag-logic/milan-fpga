#!/usr/bin/env python3
"""Observe RX EOF, feed return and TX EOF without changing stimulus or checks."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
dest = packet / "scratch/timing-probe"
receipts = packet / "receipts"
os.environ["PINNED_VERILATOR"] = str(Path(sys.argv[2]).resolve())
os.environ["TMPDIR"] = str(packet / "scratch")
for directory in ("hdl", "tb/common", "tb/pp_top"):
    shutil.copytree(root / directory, dest / directory,
                    ignore=shutil.ignore_patterns("obj*", "*.hex", "__pycache__"))
p = dest / "tb/pp_top/notify_phases.hpp"
text = p.read_text()
old = "      io.d->rx_last_i = (i + 1 == f.size()) ? 1 : 0;\n      tick();\n"
new = old + ('      if (i + 1 == f.size()) printf("R503_RX_LAST type=%02x%02x t=%llu\\n", '
             'f[12], f[13], (unsigned long long)io.t);\n')
assert text.count(old) == 1
text = text.replace(old, new)
old = "    const auto at = watch(from);\n    unsigned avb = 0;"
new = ('    printf("R503_STIMULUS tag=%s t0=%llu\\n", tag, (unsigned long long)t0);\n'
       '    const auto at = watch(from);\n'
       '    for (size_t i : at) {\n'
       '      printf("R503_TX tag=%s t=%llu bytes=", tag, (unsigned long long)seen[i].t);\n'
       '      for (uint8_t b : seen[i].f) printf("%02x", unsigned(b));\n'
       '      printf("\\n");\n'
       '    }\n'
       '    unsigned avb = 0;')
assert text.count(old) == 1
text = text.replace(old, new)
p.write_text(text)
cwd = dest / "tb/pp_top"
with (receipts / "timing-probe-build.log").open("w") as log:
    rc = subprocess.run(["make", "-j16", "gsi-build", "VERILATOR=" + str(packet / "scripts/bounded_verilator.py")],
                        cwd=cwd, stdout=log, stderr=subprocess.STDOUT).returncode
(receipts / "timing-probe-build.rc").write_text(str(rc) + "\n")
assert rc == 0
with (receipts / "timing-probe.log").open("w") as log:
    rc = subprocess.run(["./obj_dir/Vpp_top_sim", "--domain-notify-only"],
                        cwd=cwd, stdout=log, stderr=subprocess.STDOUT).returncode
(receipts / "timing-probe.rc").write_text(str(rc) + "\n")
assert rc == 0
last_rx = None
stimuli = {}
records = []
for line in (receipts / "timing-probe.log").read_text().splitlines():
    m = re.fullmatch(r"R503_RX_LAST type=22ea t=(\d+)", line)
    if m:
        last_rx = int(m[1])
    m = re.fullmatch(r"R503_STIMULUS tag=(\w+) t0=(\d+)", line)
    if m:
        stimuli[m[1]] = int(m[2])
    m = re.fullmatch(r"R503_TX tag=(\w+) t=(\d+) bytes=([0-9a-f]+)", line)
    if m and m[1] in ("DN1b", "DN2b"):
        t0, tx = stimuli[m[1]], int(m[2])
        records.append({"tag": m[1], "rx_last": last_rx, "feed_return": t0, "tx_last": tx,
                        "trailing_feed_clocks": t0 - last_rx, "printed_latency": tx - t0,
                        "rx_last_to_tx_last": tx - last_rx, "frame_hex": m[3]})
assert len(records) == 2
assert all((r["trailing_feed_clocks"], r["printed_latency"], r["rx_last_to_tx_last"]) == (4, 495, 499) for r in records)
(receipts / "timing-probe.json").write_text(json.dumps(records, indent=2) + "\n")
print(json.dumps(records, indent=2))
