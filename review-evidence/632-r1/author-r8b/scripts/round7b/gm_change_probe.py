#!/usr/bin/env python3
"""Round 7b probe: print every change of the published grandmaster identity
(cfg_adp_gptp_gm, the input of the datapath's GM-change detector) and every
detector pulse (gm_recentre_p_r) on the clean gmstep leg, with the cycle the
harness counts. A disposable copy of milan_datapath.sv gains one display
block after the detector; nothing else changes. Run with the repository's
tb/verilator/milan_dp_gm_steps as cwd.
usage: gm_change_probe.py <out dir>
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
import gmstep_mutants as g  # noqa: E402

out_dir = Path(sys.argv[1]); out_dir.mkdir(parents=True, exist_ok=True)
anchor = "  end : g_gm_recentre\n"
probe = (anchor +
         "  always_ff @(posedge axis_clk) begin : p_gm_probe\n"
         "    if (axis_resetn && (cfg_adp_gptp_gm != gm_recentre_q_r))\n"
         "      $display(\"GMPROBE change from %h to %h\", gm_recentre_q_r, cfg_adp_gptp_gm);\n"
         "    if (axis_resetn && gm_recentre_p_r)\n"
         "      $display(\"GMPROBE detector pulse (now %h)\", gm_recentre_q_r);\n"
         "  end : p_gm_probe\n")
base = g.SOURCES["datapath"].resolve()
text = base.read_text()
print("anchor count", text.count(anchor))
leg = next(c.leg for c in g.CONTROLS if c.name == "the grandmaster change stops the talker for good")
with tempfile.TemporaryDirectory(prefix="gmchange-probe-") as td:
    work = Path(td)
    planted = work / base.name
    planted.write_text(text.replace(anchor, probe))
    sources = {key: path.resolve() for key, path in g.SOURCES.items()}
    sources["datapath"] = planted
    exe = g.build(g.LEGS[leg], sources, work / "obj_p")
    print("built", exe is not None)
    rc, out = g.run_leg(g.LEGS[leg], exe, False)
(out_dir / "leg.log").write_text(out)
print("rc", rc, "verdict", g.verdict(rc, out, None))
for line in out.splitlines():
    if line.startswith("GMPROBE") or "grandmaster" in line or line.startswith("EVENT:") or "baseline: the talker streams" in line:
        print("   ", line.strip()[:200])
