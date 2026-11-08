"""cut_rtl.py <integrated.tcl> <rtl.tcl>: the recipe's RTL elaboration, the integrated script cut after synth_design
with -rtl -rtl_skip_mlo added (docs/testing/PP_SHADOW_BASELINE_RECIPE.md, Standalone measurements)."""
import sys

out = []
for line in open(sys.argv[1]).read().splitlines():
    if line.lstrip().startswith("synth_design"):
        out.append(line.rstrip() + " -rtl -rtl_skip_mlo")
        break
    out.append(line)
else:
    sys.exit("no synth_design line")
out.append("quit")
open(sys.argv[2], "w").write("\n".join(out) + "\n")
