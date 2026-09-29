#!/usr/bin/env python3
"""Insert the R400-1 probe scenarios into a scratch copy of tb/maap/sim_main.cpp."""
import sys
from pathlib import Path

sim = Path(sys.argv[1])
probes = (Path(__file__).resolve().parent / "release_probes.cpp").read_text()
src = sim.read_text()
decl_anchor = "  void announce_during_probe_yields_without_tie_break();\n"
decls = ("  void p1_release_mid_redraw_rearms_the_seed();\n"
         "  void p2_release_inside_the_tx_path();\n"
         "  void p3_bounce_inside_the_defend_path();\n"
         "  void p4_release_during_a_fitting_draw();\n"
         "  void p5_outage_while_the_lane_is_stalled();\n")
run_anchor = "int MaapAnnexBSuite::run() {"
call_anchor = "  announce_during_probe_yields_without_tie_break();\n\n  printf("
calls = ("  announce_during_probe_yields_without_tie_break();\n"
         "  p1_release_mid_redraw_rearms_the_seed();\n"
         "  p2_release_inside_the_tx_path();\n"
         "  p3_bounce_inside_the_defend_path();\n"
         "  p4_release_during_a_fitting_draw();\n"
         "  p5_outage_while_the_lane_is_stalled();\n\n  printf(")
for anchor in (decl_anchor, run_anchor, call_anchor):
    if src.count(anchor) != 1:
        sys.exit(f"anchor not unique: {anchor!r}")
src = src.replace(decl_anchor, decl_anchor + decls)
src = src.replace(run_anchor, probes + "\n" + run_anchor)
src = src.replace(call_anchor, calls)
sim.write_text(src)
