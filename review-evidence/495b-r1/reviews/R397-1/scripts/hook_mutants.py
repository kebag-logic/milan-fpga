#!/usr/bin/env python3
"""Item 7: reviewer-built ordering mutants of the #395 hooks in the AX7101
platform, each judged by the shipping probe (real elaboration, 1x1 e1 and
8x8 e2). Run with the pinned LiteX interpreter from the probe copy.
Usage: hook_mutants.py <probe-tree> <out-dir>"""
import subprocess, sys
from pathlib import Path
T, OUT = Path(sys.argv[1]), Path(sys.argv[2])
F = T / "sw/litex/platforms/alinx_ax7101.py"
LOOP = ("        for command in configure_commands():\n"
        "            # LiteX formats these strings once while writing the build Tcl.\n"
        "            self.toolchain.pre_placement_commands.append(\n")
REP = '            "kl_timing_grade_reports {build_name}_signoff",\n'
MUT = [
    ("CONTROL", None, None),
    ("H1-configure-dropped", LOOP, LOOP.replace("for command in configure_commands():", "for command in []:")),
    ("H2-configure-after-place", LOOP, LOOP.replace("pre_placement_commands", "post_placement_commands")),
    ("H3-configure-pre-route", LOOP, LOOP.replace("pre_placement_commands", "pre_routing_commands")),
    ("H4-reports-dropped", REP, ""),
    ("H5-reports-duplicated", REP, REP + REP),
    ("H6-reports-pre-route", REP, "", "pre_routing"),
    ("H7-reports-after-place", REP, "", "post_placement"),
]
orig = F.read_text()
rows = []
try:
    for m in MUT:
        name, old, new = m[:3]
        text = orig
        if old is not None:
            assert text.count(old) == 1, name
            text = text.replace(old, new)
            if len(m) == 4:
                anchor = "        self.toolchain.bitstream_commands = ["
                text = text.replace(anchor, f'        self.toolchain.{m[3]}_commands.append("kl_timing_grade_reports {{build_name}}_signoff")\n' + anchor)
        F.write_text(text)
        for config, port in (("ax7101_1x1_tdm8", "e1"), ("ax7101_8x8", "e2")):
            out = OUT / f"{name}-{config}-{port}"
            r = subprocess.run([sys.executable, "-B", str(T / "sw/builder/test_shipping_clock_constraints.py"),
                                "--config", config, "--port", port, "--output-dir", str(out)],
                               cwd=T / "sw/litex", text=True, capture_output=True, timeout=580)
            last = (r.stdout + r.stderr).strip().splitlines()[-1][:220]
            verdict = ("PASS" if r.returncode == 0 else "FAIL") if name == "CONTROL" else ("KILLED" if r.returncode else "SURVIVED")
            print(f"{name} {config} {port}: rc={r.returncode} {verdict} | {last}", flush=True)
            if name == "CONTROL":
                tcl = next(out.rglob("alinx_ax7101.tcl"))
                cmds = [l.strip() for l in tcl.read_text().splitlines() if l.strip() and not l.lstrip().startswith("#")]
                keys = ("synth_design", "opt_design", "place_design", "phys_opt_design", "route_design",
                        "kl_timing_grade", "milan_eth_constraints", "write_bitstream", "source ")
                (OUT.parent / f"control-order-{config}-{port}.txt").write_text(
                    "\n".join(f"{i}: {l[:160]}" for i, l in enumerate(cmds) if l.startswith(keys)) + "\n")
finally:
    F.write_text(orig)
