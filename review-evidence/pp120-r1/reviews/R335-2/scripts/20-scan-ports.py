#!/usr/bin/env python3
"""Run the parent's own port parser (check_port_contracts.scan_ports and
sv_ports.declarations, parent 7eb3b0d4) over PR-touched donor files at the
source base, the round-2 head and the round-3 head, reading blobs straight
from the donor object store (no checkout involved).

Usage: 20-scan-ports.py <parent-checkout> <donor-git-dir>
"""
import subprocess
import sys

PARENT, DONOR = sys.argv[1], sys.argv[2]
sys.path.insert(0, PARENT + "/scripts")
import check_port_contracts as cpc  # noqa: E402

REVS = {
    "base 0922e434": "0922e43408f891fc0b84a84691df86b4fd0f1c0d",
    "r2   a9b7874d": "a9b7874d415d935949becd7ccfd58799927efb08",
    "r3   83c84b19": "83c84b19e09d397ed2eb6f5ace337686ce0ef86b",
}
FILES = [
    "tb/pp_top/pp_top_wrap.sv",
    "hdl/top/protocol_processor_top.sv",
    "hdl/aecp/KL_aecp_engine.sv",
    "hdl/aecp/KL_aecp_desc_store.sv",
    "tb/desc_mem_guard/wrap.sv",
]
WATCH = ["aecp_name_wr_o", "dbg_name_live_we_o", "dbg_dyn_writes_o",
         "aecp_nvm_stb_o", "aecp_nvm_mark_o", "dbg_notify_enq_o"]


def blob(rev, path):
    """File text at a revision."""
    return subprocess.run(["git", "--git-dir", DONOR, "show", f"{rev}:{path}"],
                          check=True, capture_output=True, text=True).stdout


def main():
    """Print per-file totals and the six watched harness ports' doc state."""
    print("parent HEAD:", subprocess.run(["git", "-C", PARENT, "rev-parse", "HEAD"],
                                         capture_output=True, text=True).stdout.strip())
    for path in FILES:
        for label, rev in REVS.items():
            total, undoc = cpc.scan_ports(blob(rev, path))
            print(f"{path:38s} {label}: total={total} undocumented={len(undoc)}")
    print()
    for label, rev in REVS.items():
        text = blob(rev, "tb/pp_top/pp_top_wrap.sv")
        docs = {name: doc for _m, name, doc, _mb, kind in cpc.declarations(text)
                if kind != "param"}
        print(f"pp_top_wrap.sv {label}:")
        for name in WATCH:
            if name not in docs:
                print(f"  {name:20s} ABSENT")
                continue
            d = " ".join(docs[name].split())
            state = "documented" if d else "UNDOCUMENTED"
            print(f"  {name:20s} {state:12s} {d[:70]!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
