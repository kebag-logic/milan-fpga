#!/usr/bin/env python3
"""R298-1 A4 (no round restart on invalidation) re-anchored to the round-2 text,
which also clears pend_acc_r. Same intent: keep the grant retire, drop the restart.
Uses the unchanged round-1 runner's run()/SUITES. Usage: <head> <vl> <work> <out>"""
import sys
from pathlib import Path
script = Path(__file__).resolve().parent.parent / "r298-1" / "mutants_r298.py"
sys.argv = [str(script)] + sys.argv[1:5]
ns = {"__name__": "r298_a4", "__file__": str(script)}
exec(compile(script.read_text(), str(script), "exec"), ns)
old = ("        aidx_r     <= '0;\n        acc_r      <= 32'd0;\n        over_acc_r <= 1'b0;\n"
       "        pend_acc_r <= 1'b0;\n        wgrant_r   <= '0;\n        wgslope_r  <= '0;\n"
       "      end else if (round_w) begin")
ns["MUTANTS"][:] = [("A4r2-no-round-restart", ns["ADM"], old, "      end else if (round_w) begin",
                     ["adm2", "adm8", "srp_top"])]
ns["main"]()
