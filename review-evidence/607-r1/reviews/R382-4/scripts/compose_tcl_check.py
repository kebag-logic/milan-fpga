#!/usr/bin/env python3
"""Grade the composed #395/#607 hook order and report names in an emitted build Tcl.

Usage: compose_tcl_check.py <gateware dir>...   (dirs holding alinx_ax7101.tcl/.xdc)
"""
import re, sys
from pathlib import Path

def first(cmds, prefix):
    hits = [i for i, c in enumerate(cmds) if c.startswith(prefix)]
    return hits

ok = True
for d in map(Path, sys.argv[1:]):
    tcl = (d / "alinx_ax7101.tcl").read_text()
    xdc = (d / "alinx_ax7101.xdc").read_text()
    cmds = [l.strip() for l in tcl.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    pos = {k: first(cmds, k) for k in (
        "synth_design ", "source {", "kl_quasi_static_constraints", "milan_eth_constraints ",
        "opt_design", "kl_timing_grade_configure ", "place_design", "route_design",
        "kl_timing_grade_reports ", "report_clock_interaction ", "report_exceptions ",
        "write_bitstream ")}
    print(f"== {d}")
    for k, v in pos.items():
        print(f"  {k.strip():28s} {v}")
    one = lambda k: len(pos[k]) == 1
    checks = {
        "each hook once": all(one(k) for k in ("synth_design ", "milan_eth_constraints ", "kl_quasi_static_constraints",
                                                "kl_timing_grade_configure ", "kl_timing_grade_reports ",
                                                "report_clock_interaction ", "report_exceptions ", "write_bitstream ")),
        "synth < eth < first opt": pos["synth_design "][0] < pos["milan_eth_constraints "][0] < pos["opt_design"][0],
        "synth < quasi_static < first opt": pos["synth_design "][0] < pos["kl_quasi_static_constraints"][0] < pos["opt_design"][0],
        "grade_configure < place": pos["kl_timing_grade_configure "][0] < pos["place_design"][0],
        "grade_configure after eth": pos["milan_eth_constraints "][0] < pos["kl_timing_grade_configure "][0],
        "route < grade_reports < write_bitstream": pos["route_design"][-1] < pos["kl_timing_grade_reports "][0] < pos["write_bitstream "][0],
        "route < 607 reports < write_bitstream": pos["route_design"][-1] < min(pos["report_clock_interaction "][0], pos["report_exceptions "][0]) and max(pos["report_clock_interaction "][0], pos["report_exceptions "][0]) < pos["write_bitstream "][0],
        "no mr_ff in XDC": not any("mr_ff" in l and not l.lstrip().startswith("#") for l in xdc.splitlines()),
        "no if in XDC": not any(re.match(r"\s*if\b", l) for l in xdc.splitlines()),
        "no crg_clkout hand name in XDC": not re.search(r"get_clocks \{+crg_", xdc),
    }
    # Report-name collision: #395 writes <prefix>_signoff_*; #607 writes <build>_clock_interaction/_exceptions
    grade = cmds[pos["kl_timing_grade_reports "][0]].split()[1]
    ours = [re.search(r"-file (\S+)", cmds[pos[k][0]]).group(1) for k in ("report_clock_interaction ", "report_exceptions ")]
    theirs = [f"{grade}_{s}" for s in ("grade.txt", "all_timing.rpt", "clock_interaction.rpt", "cdc.rpt", "check_timing.rpt")]
    theirs += [f"{grade}_{c}_{t}C_{s}" for c in ("Slow", "Fast") for t in (0, 85) for s in ("operating.rpt", "timing.rpt", "negative.rpt")]
    other_files = re.findall(r"-file (\S+)", tcl)
    checks["607 report names disjoint from 395 set (17)"] = len(theirs) == 17 and not set(ours) & set(theirs)
    checks["607 report names unique in Tcl"] = all(other_files.count(o) == 1 for o in ours)
    print(f"  395 prefix={grade}; 607 files={ours}")
    for k, v in checks.items():
        print(f"  {'PASS' if v else 'FAIL'} {k}")
        ok &= v
print("COMPOSITION", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
