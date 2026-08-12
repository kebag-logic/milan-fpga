#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Print the milan_datapath source list, one absolute path per line.

THE POINT IS THAT THERE IS NO SECOND COPY. The authoritative list is the
"milan_datapath|..." entry in syn/yosys/run.sh — the one the portability gate
proves elaborates on every run. A hand-maintained duplicate in a Vivado .tcl
would drift the first time a module lands, and the drift would show up as a
synthesis result quietly missing a block. So the .tcl execs this instead.

Used by syn/ooc/milan_datapath_ooc.tcl.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))


def main() -> int:
    run_sh = os.path.join(REPO, "syn", "yosys", "run.sh")
    with open(run_sh) as fh:
        s = fh.read()

    m = re.search(r'"milan_datapath\|(.*?)"\n', s, re.S)
    if not m:
        print("dp_srcs: no milan_datapath top in run.sh", file=sys.stderr)
        return 2
    srcs = m.group(1)

    # the two collected lists that entry references
    for var in ("AECP_SRCS", "LWSRP_SRCS"):
        mv = re.search(r'%s="(.*?)"' % var, s, re.S)
        if not mv:
            print("dp_srcs: %s not found in run.sh" % var, file=sys.stderr)
            return 2
        srcs = srcs.replace("$" + var, mv.group(1))

    env = {
        "R": REPO,
        "A": os.path.join(REPO, "third_party/verilog-axis/rtl"),
        "C": os.path.join(REPO, "hdl/common"),
        "Q": os.path.join(REPO, "hdl/ieee8021q/ts"),
        "P": os.path.join(REPO, "hdl/ieee8021as/ptp_timestamp"),
        "E": os.path.join(REPO, "hdl/common/eth_event_counter"),
        "D": os.path.join(REPO, "hdl/ieee17221/adp"),
        "K": os.path.join(REPO, "hdl/ieee17221/aecp"),
        "M": os.path.join(REPO, "hdl/ieee17221/acmp"),
        "S": os.path.join(REPO, "hdl/ieee8021q/srp"),
        "F": os.path.join(REPO, "hdl/ieee8021q/filtering"),
    }
    for k, v in env.items():
        srcs = srcs.replace("$" + k + "/", v + "/")

    files = [f for f in srcs.split() if f.endswith((".sv", ".v"))]
    missing = [f for f in files if not os.path.exists(f)]
    if missing:
        print("dp_srcs: missing sources:\n  " + "\n  ".join(missing), file=sys.stderr)
        return 1

    print("\n".join(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
