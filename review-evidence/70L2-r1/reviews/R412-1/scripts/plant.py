#!/usr/bin/env python3
"""Plant one gate-1b probe into a tree copy's shipping firmware.
usage: plant.py <tree> <m_macro_set|m_macro_addr|m_ctrl_direct>"""
import sys
from pathlib import Path

tree, kind = Path(sys.argv[1]), sys.argv[2]
fw = tree / "sw/firmware/milan_baremetal/milan_baremetal.c"
text = fw.read_text()
decl = "static int aem_loaded;\n"
opening = "static void nvm_boot(void)\n{\n"
body_first = "\tuint32_t seq_a;\n\tuint32_t seq_b;\n\tuint32_t chosen;\n\tuint32_t stat;\n\tunsigned int verdict;\n\tunsigned int tries = 0;\n\tint loaded = 0;\n\tint live = 0;\t\t\t/* the window went live */\n\n"
assert text.count(decl) == 1 and text.count(opening + body_first) == 1
if kind == "m_macro_set":
    macro, stmt = "#define NVM_FLAG_SET(flag) ((flag) = 1)\n", "\tNVM_FLAG_SET(aem_loaded);\n"
elif kind == "m_macro_addr":
    macro, stmt = "#define NVM_REF(obj) (&(obj))\n", "\t*NVM_REF(aem_loaded) = 1;\n"
elif kind == "m_ctrl_direct":
    macro, stmt = "", "\taem_loaded = 1;\n"
else:
    raise SystemExit("unknown probe")
text = text.replace(decl, decl + macro, 1)
text = text.replace(opening + body_first, opening + body_first + stmt, 1)
fw.write_text(text)
print(f"planted {kind} in {fw}")
