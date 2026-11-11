#!/usr/bin/env python3
"""Reviewer probe: plant an MVRP leavealltimer outside Milan v1.2 Table 4.3's
9.5 to 15.5 s in a processor copy and run the crflic leg through the
campaign's own run_pp_mutant(); [MVRPLA]'s gap check must fail by name.
usage: <repo> <long|short> [work-dir]"""
import sys, tempfile
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "tb/verilator/milan_dp"))
import crflic_mutants as cm  # noqa: E402
LINE = "            cad_dl_r[CAD_LA_MVRP_C]   <= now_ms_i + {16'd0, draw_ms_i};\n"
REPL = {
    "long": "            cad_dl_r[CAD_LA_MVRP_C]   <= now_ms_i + {16'd0, draw_ms_i} + 32'd5000;\n",
    "short": "            cad_dl_r[CAD_LA_MVRP_C]   <= now_ms_i + {17'd0, draw_ms_i[15:1]};\n",
}
kind = sys.argv[2]
mut = (f"reviewer probe: MVRP leavealltimer {kind} (outside 9.5 to 15.5 s)",
       [("srp/KL_srp_top.sv", LINE, REPL[kind])],
       "MVRP, nothing declared: each LeaveAll 9.5 to 15.5 s after its timer's last start")
print(f"probe {kind}: must fail {mut[2]!r}", flush=True)
with tempfile.TemporaryDirectory(prefix=f"r831-mvrpla-{kind}-",
                                 dir=sys.argv[3] if len(sys.argv) > 3 else None) as td:
    caught = cm.run_pp_mutant(mut, Path(td))
print("RESULT:", "CAUGHT" if caught else "NOT CAUGHT", flush=True)
sys.exit(0 if caught else 1)
