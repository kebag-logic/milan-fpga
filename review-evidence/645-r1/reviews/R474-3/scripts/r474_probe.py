"""Insert the R474 probe into a disposable copy of chmap_capture/sim_main.cpp."""
import sys
from pathlib import Path
src, probe, out = map(Path, sys.argv[1:4])
t = src.read_text()
decl = "  void pin_settle_recentre_centres_the_loop_queues();\n"
call = "  pin_recentre_output_spans();\n\n  printf(\"\\n=====" 
assert t.count(decl) == 1 and t.count(call) == 1, "anchor"
t = t.replace(decl, decl + "  void r474_probes();\n")
t = t.replace(call, "  pin_recentre_output_spans();\n  r474_probes();\n\n  printf(\"\\n=====")
anchor = "// The declaration is in source events, independently for each output."
assert t.count(anchor) == 1
t = t.replace(anchor, probe.read_text() + "\n" + anchor)
out.write_text(t)
