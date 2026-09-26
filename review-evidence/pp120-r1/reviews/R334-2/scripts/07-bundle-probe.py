#!/usr/bin/env python3
"""Disposable text probe of the head wrapper under the parent's parser: head as
published; head without the blank line it added before the effect bundle (is the
blank line load-bearing?); and head with the bundle's //! run deleted (the parser
must then report the four effect ports undocumented, i.e. the probe can fail).
No tracked file is modified."""
import os, subprocess, sys
from pathlib import Path
PK = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(PK / "scratch/parent-scripts"))
import check_port_contracts as ports  # noqa: E402
C = os.environ.get("CLONE", "$REVIEWS/r334-2-pp120")
head = subprocess.run(["git", "-C", C, "show", "83c84b19e09d397ed2eb6f5ace337686ce0ef86b:tb/pp_top/pp_top_wrap.sv"],
                      capture_output=True, text=True, check=True).stdout
gap = "    output logic        dbg_name_live_we_o,\n\n    //! the SET_CLOCK_SOURCE"
assert head.count(gap) == 1
no_gap = head.replace(gap, gap.replace(",\n\n", ",\n"))
s = head.index("    //! the SET_CLOCK_SOURCE refusal contract"); e = head.index("    output logic [15:0] dbg_dyn_writes_o,")
no_doc = head[:s] + head[e:]
G = ("aecp_name_wr_o", "dbg_name_live_we_o", "dbg_dyn_writes_o", "aecp_nvm_stb_o", "aecp_nvm_mark_o", "dbg_notify_enq_o")
for name, text in (("head as published", head), ("head, blank line removed", no_gap), ("head, bundle //! run deleted (negative control)", no_doc)):
    total, undoc = ports.scan_ports(text)
    print(f"{name}: ports {total}, undocumented {len(undoc)}; undocumented among effect/name ports: {[p for p in G if p in undoc]}")
