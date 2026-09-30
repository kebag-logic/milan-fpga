#!/usr/bin/env python3
"""Plant one gate-1b probe into a tree copy's shipping firmware (round 2).

usage: plants2.py <tree> <probe>

Every probe puts its statement first in nvm_boot()'s body (after its
declarations) and, where it needs one, a file-scope line just after
`static int aem_loaded;`.  The shipping firmware is already AEM-first, so a
probe the gate accepts leaves the verdict's slot kept across nvm_boot().

Round-1 spellings re-run: plain_write, splice_write, paste_write,
m_macro_set, m_macro_addr, m_macro_addr_sscanf.
Round-2 spellings: alias_write (a store through a GCC alias of the verdict),
alias_addr (the alias's address handed to sscanf()), alias_decl_only (the
global alias declared, no statement: another unit or the BIOS can name it),
static_alias_write (a file-local alias) and static_alias_addr (its address
handed to sscanf()).
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

ALIAS = 'extern int aem_view __attribute__((alias("aem_loaded")));\n'
PROBES = {
    "plain_write": ("", "\taem_loaded = 1;\n"),
    "splice_write": ("", "\taem_\\\nloaded = 1;\n"),
    "paste_write": ("#define R412_JOIN(a, b) a##b\n",
                    "\tR412_JOIN(aem_, loaded) = 1;\n"),
    "m_macro_set": ("#define NVM_FLAG_SET(flag) ((flag) = 1)\n",
                    "\tNVM_FLAG_SET(aem_loaded);\n"),
    "m_macro_addr": ("#define NVM_REF(obj) (&(obj))\n",
                     "\t*NVM_REF(aem_loaded) = 1;\n"),
    "m_macro_addr_sscanf": ("#define NVM_REF(obj) (&(obj))\n",
                            "\t(void)sscanf(\"1\", \"%d\", NVM_REF(aem_loaded));\n"),
    "alias_write": (ALIAS, "\taem_view = 1;\n"),
    "alias_addr": (ALIAS, "\t(void)sscanf(\"1\", \"%d\", &aem_view);\n"),
    "alias_decl_only": (ALIAS, ""),
    "static_alias_addr": (
        'static int aem_view __attribute__((alias("aem_loaded")));\n',
        "\t(void)sscanf(\"1\", \"%d\", &aem_view);\n"),
    "static_alias_write": (
        'static int aem_view __attribute__((alias("aem_loaded")));\n',
        "\taem_view = 1;\n"),
}
macro, stmt = PROBES[kind]
text = text.replace(decl, decl + macro, 1)
text = text.replace(opening + body_first, opening + body_first + stmt, 1)
fw.write_text(text)
print(f"planted {kind} in {fw}")
