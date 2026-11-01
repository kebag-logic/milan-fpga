#!/usr/bin/env python3
"""Hand two stated-limit plants of milan_datapath.sv to the conversion the portability gate runs.

Usage: limit_probe.py <clone> <work dir>; the conversion is `sv2v --top=milan_datapath` over the
record syn/yosys/run.sh --emit states, with the planted file in the datapath's place.
"""
import subprocess
import sys
from pathlib import Path

clone, work = Path(sys.argv[1]), Path(sys.argv[2])
rec = subprocess.run(["bash", str(clone / "syn/yosys/run.sh"), "--emit", "milan_datapath"],
                     capture_output=True, text=True, check=True).stdout.splitlines()
pick = lambda key: [l.split("=", 1)[1] for l in rec if l.startswith(key + "=")]
dp = clone / "hdl/milan/milan_datapath.sv"
rtl = dp.read_text()
plane = "    KL_gptp_shadow #(\n"
at = rtl.index("u_gptp_shadow (")
close = rtl.index("\n    );", at)
dead = (rtl[:close] + "\n    );\n    end" + rtl[close + 7:]).replace(
    plane, "    if (1'b0) begin : g_dead\n" + plane)
plants = {"shipped": rtl,
          "defparam": rtl.replace(plane, "    defparam u_gptp_shadow.ETH_TICK_NS_P = 8;\n" + plane),
          "dead arm": dead}
for name, text in plants.items():
    path = work / name.replace(" ", "_") / "milan_datapath.sv"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    srcs = [str(path) if s == str(dp) else s for s in pick("src")]
    cmd = ["sv2v", "--top=milan_datapath", *(f"-D{d}" for d in pick("define")),
           "-I", str(clone / "hdl/milan"), *(a for i in pick("incdir") for a in ("-I", i)), *srcs]
    out = subprocess.run(cmd, capture_output=True, text=True)
    body = out.stdout
    print(f"{name}: sv2v rc {out.returncode}; output has u_gptp_shadow: {'u_gptp_shadow' in body}; "
          f"has KL_gptp_shadow module use: {'KL_gptp_shadow' in body}; stderr: {out.stderr[:200]!r}")
