#!/usr/bin/env python3
"""Self-test of census_textual_cone.py: with the case-label and function-return
escapes of census_cone_probe.py planted (in memory), the textual cone must
report the planted status read as leaving its class.
Usage: python3 -I census_textual_cone_selftest.py <tree>"""
import runpy
import sys
from dataclasses import replace
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
here = Path(__file__).resolve().parent
sys.path.insert(0, str(tree / "sw/mailbox"))
import publication_census as pc  # noqa: E402

ANCHOR = "  wire crft_class_a_w ="
SINK = "  KL_probe_sink u_probe_sink (.a_i(probe_q));\n"
PLANTS = {
    "case label": "  logic probe_q;\n  always_comb begin\n    case (1'b1)\n      lwsrp_res_active: probe_q = 1'b1;\n"
                  "      default: probe_q = 1'b0;\n    endcase\n  end\n" + SINK,
    "function return": "  function automatic logic probe_f(input logic x);\n    return lwsrp_res_active;\n"
                       "  endfunction\n  wire probe_q = probe_f(1'b0);\n" + SINK,
}
real_load = pc.load
failed = 0
for what, text in PLANTS.items():
    pc.load = lambda d, w, t=text: replace(real_load(d, w), datapath=real_load(d, w).datapath.replace(ANCHOR, t + ANCHOR, 1))
    sys.argv = ["census_textual_cone.py", str(tree)]
    try:
        runpy.run_path(str(here / "census_textual_cone.py"), run_name="__main__")
        rc = 0
    except SystemExit as e:
        rc = e.code
    print(f"[{'ok' if rc == 1 else 'BAD'}] planted {what}: textual cone rc {rc} (1 expected)")
    failed += rc != 1
print(f"selftest: {failed} of {len(PLANTS)} failed")
sys.exit(1 if failed else 0)
