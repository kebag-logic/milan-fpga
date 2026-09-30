#!/usr/bin/env python3
"""Plant one verdict-override into the scratch firmware (argv[1] = tree,
argv[2] = plant name, or 'none' to restore). Each plant makes the entity
enable independent of the AEM verifier: after nvm_boot() returns, aem_loaded
holds 1 whatever load_aem_image() handed back. The original bytes are taken
from the review clone at the exact head."""
import sys
from pathlib import Path
tree = Path(sys.argv[1]); name = sys.argv[2]
orig = Path("$REVIEWS/r413-1-70L2/sw/firmware/milan_baremetal/milan_baremetal.c").read_text()
fw = tree / "sw/firmware/milan_baremetal/milan_baremetal.c"
TAIL = "\tset_idle_hook(nvm_service);\n}\n\nstatic void configure_fabric(void)"
assert orig.count(TAIL) == 1
DECL = "static int aem_loaded;\n"
assert orig.count(DECL) == 1, orig.count(DECL)
def at_tail(stmt): return orig.replace(TAIL, stmt + TAIL)
PLANTS = {
  "none": orig,
  # the control: a plain second write, which pin 1 must refuse
  "plain_write": at_tail("\taem_loaded = 1;\n"),
  # a phase-2 line splice inside nvm_boot(), outside the six boot-path bodies
  "splice_write": at_tail("\taem_\\\nloaded = 1;\n"),
  # a ## paste through a macro no boot-path body names
  "paste_write": orig.replace(DECL, DECL + "#define MILAN_R413_JOIN(a, b) a##b\n").replace(
      TAIL, "\tMILAN_R413_JOIN(aem_, loaded) = 1;\n" + TAIL),
  # a GNU alias of the static, written by its other name
  "alias_write": orig.replace(DECL, DECL + 'extern int milan_r413_alias __attribute__((alias("aem_loaded")));\n').replace(
      TAIL, "\tmilan_r413_alias = 1;\n" + TAIL),
}
text = PLANTS[name]
assert name == "none" or text != orig
fw.write_text(text)
import hashlib
print("planted", name, "firmware sha256", hashlib.sha256(text.encode()).hexdigest())
