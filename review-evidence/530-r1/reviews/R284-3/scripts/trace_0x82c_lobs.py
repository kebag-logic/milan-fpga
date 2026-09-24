#!/usr/bin/env python3
"""Trace A_STRMW_STATE 0x82C talker bit [2] (lobs) to its source at a revision.

Usage: trace_0x82c_lobs.py <repo> <rev>

Prints, with line numbers, every link of the chain from the snapshot pack to
the processor output, and asserts each link by pattern. Exit 0 when the whole
chain is present as described; the chain shows that index 0 carries source 0's
REGISTERED Listener level (not ACTIVE) and that only N_STREAMS (AAF) indices
reach the window, so the CRF output has no 0x82C talker index.
"""
import re
import subprocess
import sys

LINKS = [
    ("hdl/common/csr/milan_csr.sv", r"i_tlk_lobs_v\[snap_idx_r\[2:0\]\]",
     "0x82C talker pack: bit [2] = i_tlk_lobs_v[idx]"),
    ("hdl/milan/milan_datapath.sv", r"\.i_tlk_lobs_v\s*\(8'\(acmp_lobs_v_w\[N_STREAMS-1:0\]\)\)",
     "only the N_STREAMS AAF indices reach the window (no CRF index)"),
    ("hdl/milan/milan_datapath.sv", r"assign acmp_lobs_v_w\[gj\] = listener_observed_w;",
     "index 0 = listener_observed_w"),
    ("hdl/milan/milan_datapath.sv", r"assign acmp_lobs_v_w\[gj\] = cfg_acmp_lobs \|",
     "index > 0 = cfg_acmp_lobs | (cfg_lwsrp_enable & lwsrp_stream_gate[gj]) (ACTIVE)"),
    ("hdl/milan/milan_datapath.sv", r"wire listener_observed_w = cfg_acmp_lobs \|",
     "listener_observed_w = cfg_acmp_lobs | (cfg_lwsrp_enable & lwsrp_listener_ready)"),
    ("hdl/milan/milan_datapath.sv", r"\(cfg_lwsrp_enable & lwsrp_listener_ready\);",
     "  (continuation)"),
    ("hdl/milan/milan_datapath.sv", r"assign lwsrp_listener_ready =",
     "lwsrp_listener_ready = source 0 registered Ready / Ready Failed"),
    ("hdl/milan/milan_datapath.sv", r"wire \[1:0\]\s+lwsrp_lstn_reg0_w = pp_cd_srp_lstn_reg_state_w\[1:0\];",
     "the registration level of source 0, from the processor's lstn_reg_state"),
    ("hdl/milan/milan_datapath.sv", r"talker lobs pulse with it",
     "the round-2 comment claim under review"),
    ("docs/reference/REGISTER_MAP.md", r"at idx 0 source 0's registered Listener Ready or Ready Failed, at idx > 0 that source's ACTIVE since #530",
     "REGISTER_MAP 0x82C row: idx 0 is the registration, idx > 0 is ACTIVE"),
]


def main():
    repo, rev = sys.argv[1:3]
    ok = True
    for path, pat, what in LINKS:
        src = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                             check=True, capture_output=True, text=True).stdout
        hits = [(i + 1, l) for i, l in enumerate(src.splitlines())
                if re.search(pat, l)]
        print(f"- {what}")
        if not hits:
            print(f"    MISSING in {path}"); ok = False
        for n, l in hits:
            print(f"    {path}:{n}: {l.strip()[:200]}")
    print("RESULT", "CHAIN PRESENT" if ok else "CHAIN BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
