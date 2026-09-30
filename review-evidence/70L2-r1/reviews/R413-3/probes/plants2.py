#!/usr/bin/env python3
"""Two adversarial plants the gate's own controls don't spell, to test the
ruling's premise that a %lo-on-addi is the escape the pins must catch:
  asm_hilo_sscanf : lui/addi %hi/%lo(aem_loaded) in inline asm -> the address
                    in a register via a REAL R_RISCV_LO12_I on an addi, no C &.
  addend_store    : a store to aem_loaded reached as (&decoy)[k] so the reloc
                    is on a DIFFERENT symbol with an addend whose target lands
                    on aem_loaded's bytes -- tests reference-by-address."""
import sys, os
from pathlib import Path
HEAD = Path(os.environ.get("R413_HEAD_TREE","$REVIEWS/r413-3-70L2"))/"sw/firmware/milan_baremetal/milan_baremetal.c"
tree = Path(sys.argv[1]); name = sys.argv[2]
orig = HEAD.read_text()
fw = tree/"sw/firmware/milan_baremetal/milan_baremetal.c"
TAIL = "\tset_idle_hook(nvm_service);\n}\n\nstatic void configure_fabric(void)"
DECL = "static int aem_loaded;\n"
assert orig.count(TAIL)==1 and orig.count(DECL)==1
def at_tail(stmt, macro=""):
    base = orig.replace(DECL, DECL+macro) if macro else orig
    return base.replace(TAIL, stmt+TAIL)
PLANTS = {
  "none": orig,
  "asm_hilo_sscanf": at_tail(
     '\t{\n\t\tint *milan_r413_p;\n'
     '\t\t__asm__ volatile("lui %0,%%hi(aem_loaded)\\n\\t"\n'
     '\t\t                 "addi %0,%0,%%lo(aem_loaded)" : "=r"(milan_r413_p));\n'
     '\t\t(void)sscanf("1", "%d", milan_r413_p);\n\t}\n'),
}
text = PLANTS[name]
assert name=="none" or text!=orig
fw.write_text(text)
import hashlib; print("planted", name, hashlib.sha256(text.encode()).hexdigest()[:16])
