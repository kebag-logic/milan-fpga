#!/usr/bin/env python3
"""Plant one gate-1b probe of this round into a tree copy's shipping firmware.

usage: plants_a460.py <tree> <probe>

The same placement as the round-3 review's plants3.py: the statement opens
nvm_boot()'s body after its declarations, and a file-scope line goes just
after (or, for the `before` probes, just before) `static int aem_loaded;`.
The shipping firmware is AEM-first, so a probe gate 1b accepts keeps the
verdict's slot across nvm_boot().

  unit_under_store   this unit stores through a neighbour's pointer carried
                     one int BEFORE the neighbour's start, the offset applied
                     in a register (a local pointer at -O0), so no relocation
                     lands on the verdict
  unit_over_store    this unit stores one byte PAST the end of a four-byte
                     static array declared just before the verdict, through a
                     local pointer
  interior_const     the round-4 control's shape: a neighbour's address minus
                     3, folded into the relocation, handed to sscanf("%c"), so
                     the only reference lands on the verdict's second byte
"""
import sys
from pathlib import Path

tree, kind = Path(sys.argv[1]), sys.argv[2]
fw = tree / "sw/firmware/milan_baremetal/milan_baremetal.c"
text = fw.read_text()
decl = "static int aem_loaded;\n"
opening = "static void nvm_boot(void)\n{\n"
body_first = ("\tuint32_t seq_a;\n\tuint32_t seq_b;\n\tuint32_t chosen;\n"
              "\tuint32_t stat;\n\tunsigned int verdict;\n"
              "\tunsigned int tries = 0;\n\tint loaded = 0;\n"
              "\tint live = 0;\t\t\t/* the window went live */\n\n")
assert text.count(decl) == 1 and text.count(opening + body_first) == 1

AFTER = {
    "unit_under_store": ("static int r460_pad;\n",
                         "\t{\n\t\tint *r460_p = &r460_pad;\n\n"
                         "\t\tr460_p[-1] = 1;\n\t}\n"),
    "unit_over_store": ("", "\t{\n\t\tchar *r460_q = r460_line;\n\n"
                            "\t\tr460_q[4] = 1;\n\t}\n"),
    "interior_const": ("static int r460_next;\n",
                       '\t(void)sscanf("\\001", "%c", (char *)&r460_next - 3);\n'),
}
BEFORE = {"unit_over_store": "static char r460_line[4];\n"}
macro, stmt = AFTER[kind]
text = text.replace(decl, BEFORE.get(kind, "") + decl + macro, 1)
text = text.replace(opening + body_first, opening + body_first + stmt, 1)
fw.write_text(text)
print(f"planted {kind} in {fw}")
