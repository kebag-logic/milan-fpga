#!/usr/bin/env python3
"""Plant one verdict override into a SCRATCH tree's firmware (argv[1] = tree,
argv[2] = plant name, 'none' restores the head bytes). Every plant except
'none' makes aem_loaded hold 1 after nvm_boot() returns, whatever
load_aem_image() handed back, so the entity-enable choke point would be
entered with a verdict the verifier never produced. Original bytes come from
the review clone at the exact head (943a3dac).

Round-1 plants: plain_write, splice_write, paste_write, alias_write.
Assignment plants: m_macro_set, m_macro_addr (address through a macro, then
a store through the pointer), m_macro_addr_sscanf (library write).
Round-2 escape candidates, each forming the static's ADDRESS in compiled
code without a C-level `&aem_loaded`, then handing it to sscanf() so no
store to it appears in the unit:
  asm_label_sscanf    an extern whose assembler name is "aem_loaded"
  inline_asm_la       inline asm `la %0, aem_loaded`
  alias_sscanf        a GNU alias of the static, its address taken
  weakref_sscanf      a static weakref to "aem_loaded", its address taken
  block_extern_sscanf a block-scope `extern int aem_loaded;` redeclaration
"""
import hashlib, sys
from pathlib import Path
import os
HEAD = Path(os.environ.get("R413_HEAD_TREE", "$REVIEWS/r413-2-70L2")) / "sw/firmware/milan_baremetal/milan_baremetal.c"
tree = Path(sys.argv[1]); name = sys.argv[2]
orig = HEAD.read_text()
fw = tree / "sw/firmware/milan_baremetal/milan_baremetal.c"
TAIL = "\tset_idle_hook(nvm_service);\n}\n\nstatic void configure_fabric(void)"
DECL = "static int aem_loaded;\n"
assert orig.count(TAIL) == 1 and orig.count(DECL) == 1

def at_tail(stmt, macro=""):
    base = orig.replace(DECL, DECL + macro) if macro else orig
    return base.replace(TAIL, stmt + TAIL)

SSCANF = '\t(void)sscanf("1", "%d", {});\n'
PLANTS = {
    "none": orig,
    "plain_write": at_tail("\taem_loaded = 1;\n"),
    "splice_write": at_tail("\taem_\\\nloaded = 1;\n"),
    "paste_write": at_tail("\tMILAN_R413_JOIN(aem_, loaded) = 1;\n",
                           "#define MILAN_R413_JOIN(a, b) a##b\n"),
    "alias_write": at_tail("\tmilan_r413_alias = 1;\n",
                           'extern int milan_r413_alias __attribute__((alias("aem_loaded")));\n'),
    "m_macro_set": at_tail("\tMILAN_R413_SET(aem_loaded);\n",
                           "#define MILAN_R413_SET(flag) ((flag) = 1)\n"),
    "m_macro_addr": at_tail("\t{ volatile int *milan_r413_p = MILAN_R413_REF(aem_loaded); *milan_r413_p = 1; }\n",
                            "#define MILAN_R413_REF(obj) (&(obj))\n"),
    "m_macro_addr_sscanf": at_tail(SSCANF.format("MILAN_R413_REF(aem_loaded)"),
                                   "#define MILAN_R413_REF(obj) (&(obj))\n"),
    "asm_label_sscanf": at_tail(SSCANF.format("&milan_r413_other"),
                                'extern int milan_r413_other __asm__("aem_loaded");\n'),
    "inline_asm_la": at_tail('\t{ int *milan_r413_p; __asm__ volatile("la %0, aem_loaded" : "=r"(milan_r413_p));\n'
                             '\t  (void)sscanf("1", "%d", milan_r413_p); }\n'),
    "alias_sscanf": at_tail(SSCANF.format("&milan_r413_alias"),
                            'extern int milan_r413_alias __attribute__((alias("aem_loaded")));\n'),
    "weakref_sscanf": at_tail(SSCANF.format("&milan_r413_ref"),
                              'static int milan_r413_ref __attribute__((weakref("aem_loaded")));\n'),
    "block_extern_sscanf": at_tail('\t{ extern int aem_loaded; (void)sscanf("1", "%d", &aem_loaded); }\n'),
}
text = PLANTS[name]
assert name == "none" or text != orig
fw.write_text(text)
print("planted", name, "firmware sha256", hashlib.sha256(text.encode()).hexdigest())
