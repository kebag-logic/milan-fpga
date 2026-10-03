#!/usr/bin/env python3
"""Add one new hdl/ source file whose module header has a given layout, for
the Yosys gate's census probes. The module holds an instance of an undeclared
module, so any run that elaborates it as a top goes red on it.

usage: plant_census.py <tree> <layout> <ModuleName> [clean]
  layouts: plain split automatic-split comment-block comment-line macromodule
           attr-sameline attr-ownline ifdef
"""
import sys
from pathlib import Path

tree, layout, name = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
clean = len(sys.argv) > 4 and sys.argv[4] == "clean"
body = "" if clean else "  r448_absent_module u_r448_planted ();\n"
head = {
    "plain": f"module {name} (input logic a_i);\n",
    "split": f"module\n  {name} (input logic a_i);\n",
    "automatic-split": f"module automatic\n  {name} (input logic a_i);\n",
    "comment-block": f"module /* r448 */ {name} (input logic a_i);\n",
    "comment-line": f"module // r448\n  {name} (input logic a_i);\n",
    "macromodule": f"macromodule {name} (input logic a_i);\n",
    "attr-sameline": f'(* keep_hierarchy = "yes" *) module {name} (input logic a_i);\n',
    "attr-ownline": f'(* keep_hierarchy = "yes" *)\nmodule {name} (input logic a_i);\n',
    "ifdef": f"`ifdef R448_NOT_DEFINED\nmodule {name} (input logic a_i);\n",
}[layout]
tail = "endmodule\n" + ("`endif\n" if layout == "ifdef" else "")
f = tree / "hdl" / "top" / f"{name}.sv"
f.write_text("// SPDX-License-Identifier: CERN-OHL-W-2.0\n" + head + body + tail)
print(f"planted {f.relative_to(tree)} ({layout}{', clean' if clean else ''})")
