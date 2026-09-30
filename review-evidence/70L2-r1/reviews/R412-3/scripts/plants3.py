#!/usr/bin/env python3
"""Plant one gate-1b probe into a tree copy's shipping firmware (round 3).

usage: plants3.py <tree> <probe>

Every probe puts its statement first in nvm_boot()'s body (after its
declarations) and, where it needs one, a file-scope line just after
`static int aem_loaded;`.  The shipping firmware is already AEM-first, so a
probe the gate accepts leaves the verdict's slot kept across nvm_boot().

Rounds 1-2 spellings re-run: plain_write, splice_write, paste_write,
m_macro_set, m_macro_addr, m_macro_addr_sscanf, alias_write, alias_sscanf,
alias_decl_only, static_alias_sscanf, static_alias_write; weakref_sscanf.

Round-3 spellings (this round's own):
  nbr_after_sscanf / nbr_before_sscanf: a NEIGHBOUR static's address, one
      object past (or before) it, handed to sscanf(); no relocation lands on
      the verdict's bytes, only on the neighbour's (out-of-bounds pointer
      arithmetic, undefined in C, compiled as written at -O0);
  nbr_memset: memset() of 8 bytes over a 4-byte neighbour;
  arr_overrun_sscanf: "%s" into a 4-byte static array, the classic overrun;
  nbr_runtime_sscanf: the neighbour's address with a RUNTIME offset of -1
      (a volatile local), so no addend folds onto the verdict;
  nbr_runtime_store: the same address stored through IN the unit (the
      resolver's own standing model, for comparison);
  nbr_byte_sscanf: one byte written by sscanf("%c") at the neighbour's
      address minus 3, a constant the compiler folds into the relocation, so
      it lands INSIDE the verdict's bytes but not on its first byte;
  pre_overrun_sscanf: "%s" of five characters into a 4-byte static array
      declared just BEFORE the verdict, the classic overrun onto it;
  pie_write: `aem_loaded = 1;` under `#ifndef __PIE__` (the gate's own
      control shape, run through the WHOLE gate);
  optimize_write: `aem_loaded = 1;` under `#ifdef __OPTIMIZE__`, set by the
      product's -Os and by neither census compile;
  bcp_write: `aem_loaded = 1;` under `__builtin_constant_p()` of a local,
      false at the census's -O0 and foldable at the product's -Os;
  block_extern_sscanf: a block-scope `extern int aem_loaded;` whose address
      is handed to sscanf().
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
SCAN = '\t(void)sscanf("1", "%d", {});\n'
PROBES = {
    "base": ("", ""),
    "plain_write": ("", "\taem_loaded = 1;\n"),
    "splice_write": ("", "\taem_\\\nloaded = 1;\n"),
    "paste_write": ("#define R412_JOIN(a, b) a##b\n",
                    "\tR412_JOIN(aem_, loaded) = 1;\n"),
    "m_macro_set": ("#define NVM_FLAG_SET(flag) ((flag) = 1)\n",
                    "\tNVM_FLAG_SET(aem_loaded);\n"),
    "m_macro_addr": ("#define NVM_REF(obj) (&(obj))\n",
                     "\t*NVM_REF(aem_loaded) = 1;\n"),
    "m_macro_addr_sscanf": ("#define NVM_REF(obj) (&(obj))\n",
                            SCAN.format("NVM_REF(aem_loaded)")),
    "alias_write": (ALIAS, "\taem_view = 1;\n"),
    "alias_sscanf": (ALIAS, SCAN.format("&aem_view")),
    "alias_decl_only": (ALIAS, ""),
    "static_alias_sscanf": (
        'static int aem_view __attribute__((alias("aem_loaded")));\n',
        SCAN.format("&aem_view")),
    "static_alias_write": (
        'static int aem_view __attribute__((alias("aem_loaded")));\n',
        "\taem_view = 1;\n"),
    "weakref_sscanf": (
        'static int aem_wref __attribute__((weakref("aem_loaded")));\n',
        SCAN.format("&aem_wref")),
    "block_extern_sscanf": (
        "", "\t{\n\t\textern int aem_loaded;\n\n"
            "\t\t(void)sscanf(\"1\", \"%d\", &aem_loaded);\n\t}\n"),
    "nbr_after_sscanf": ("static int r412_pad;\n",
                         SCAN.format("&r412_pad + 1")),
    "nbr_before_sscanf": ("static int r412_pad;\n",
                          SCAN.format("&r412_pad - 1")),
    "nbr_memset": ("static int r412_pad;\n",
                   "\tmemset(&r412_pad, 0x01, 8);\n"),
    "arr_overrun_sscanf": ("static char r412_word[4];\n",
                           '\t(void)sscanf("abcd\\001", "%s", r412_word);\n'),
    "nbr_runtime_sscanf": ("static int r412_pad;\n",
                           "\t{\n\t\tvolatile int r412_k = -1;\n\n"
                           "\t\t(void)sscanf(\"1\", \"%d\", &r412_pad + r412_k);\n\t}\n"),
    "nbr_runtime_store": ("static int r412_pad;\n",
                          "\t{\n\t\tvolatile int r412_k = -1;\n\n"
                          "\t\t(&r412_pad)[r412_k] = 1;\n\t}\n"),
    "nbr_byte_sscanf": ("static int r412_pad;\n",
                        '\t(void)sscanf("\\001", "%c", (char *)&r412_pad - 3);\n'),
    "pre_overrun_sscanf": ("", '\t(void)sscanf("abcd\\001", "%s", r412_line);\n'),
    "pie_write": ("", "#ifndef __PIE__\n\taem_loaded = 1;\n#endif\n"),
    "optimize_write": ("", "#ifdef __OPTIMIZE__\n\taem_loaded = 1;\n#endif\n"),
    "bcp_write": ("", "\t{\n\t\tint r412_k = 1;\n\n"
                      "\t\tif (__builtin_constant_p(r412_k))\n"
                      "\t\t\taem_loaded = 1;\n\t}\n"),
}
#: Probes whose file-scope line goes just BEFORE the verdict's declaration,
#: so the object is placed below it in the unit's .sbss.
BEFORE = {"pre_overrun_sscanf": "static char r412_line[4];\n"}
macro, stmt = PROBES[kind]
text = text.replace(decl, BEFORE.get(kind, "") + decl + macro, 1)
text = text.replace(opening + body_first, opening + body_first + stmt, 1)
fw.write_text(text)
print(f"planted {kind} in {fw}")
