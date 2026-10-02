#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R433-3 reviewer probes on KL_aaf_clock_meter's largest-deviation level.

Disposable copies only: each probe applies exact replacements (each anchor
must occur exactly once) to a scratch copy of the RTL, builds the meter
harness with METER_RTL/MDIR overrides and runs the `rates` case.
CAUGHT = build ok, exit 1 and at least one [FAIL]; SURVIVED = exit 0.
Usage: r433_3_meter_probes.py <copy of the head> <workdir>
"""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
suite = repo / "tb/verilator/aaf_clock_meter"
rtl = (repo / "hdl/ieee1722/crf/KL_aaf_clock_meter.sv").read_text()
CLEAR = "        mr_toggle_p_o <= 1'b0;\n        max_dev_r     <= '0;\n"
PROBES = {
    "clean_control": [],
    # a data-caused history restart also clears the largest deviation
    "max_dev_cleared_by_data_restart": [
        ("      if (pdu_restart_r) begin\n        restart_cnt_r <= restart_cnt_r + 8'd1;\n",
         "      if (pdu_restart_r) begin\n        restart_cnt_r <= restart_cnt_r + 8'd1;\n"
         "        max_dev_r     <= '0;\n")],
    # cleared only while not following: no era start clears it
    "max_dev_cleared_only_when_disabled": [
        (CLEAR, "        mr_toggle_p_o <= 1'b0;\n"),
        ("      if (!en_w) disrupt_p_o <= 1'b0;\n",
         "      if (!en_w) disrupt_p_o <= 1'b0;\n      if (!en_w) max_dev_r <= '0;\n")],
    # every era start clears it except the 100 ms timeout
    "max_dev_not_cleared_by_timeout": [
        (CLEAR, "        mr_toggle_p_o <= 1'b0;\n        if (!tout_fire_w) max_dev_r <= '0;\n")],
    # the saturation bound moved up by one (65,536 wraps to 0)
    "max_dev_saturation_bound_plus_one": [
        ("if (s2_abs_w > 32'd65535)", "if (s2_abs_w > 32'd65536)")],
}


def run(name):
    src = rtl
    for anchor, repl in PROBES[name]:
        n = src.count(anchor)
        if n != 1:
            return name, f"ANCHOR x{n}", ""
        src = src.replace(anchor, repl)
    d = work / name
    d.mkdir(parents=True, exist_ok=True)
    f = d / "KL_aaf_clock_meter.sv"
    f.write_text(src)
    b = subprocess.run(["make", "-s", "-C", str(suite), "build", f"METER_RTL={f}",
                        f"MDIR={d}/obj"], capture_output=True, text=True)
    if b.returncode:
        return name, "BUILD-FAIL", b.stderr[-1500:]
    r = subprocess.run([str(d / "obj/Vmeter_sim"), "rates"], capture_output=True,
                       text=True, cwd=str(suite))
    (d / "run.log").write_text(r.stdout + r.stderr)
    fails = [ln for ln in r.stdout.splitlines() if "[FAIL]" in ln]
    if name == "clean_control":
        verdict = "PASS(clean)" if r.returncode == 0 else "UNEXPECTED-FAIL"
    else:
        verdict = ("CAUGHT" if r.returncode == 1 and fails
                   else "SURVIVED" if r.returncode == 0 else f"EXIT{r.returncode}")
    return name, verdict, "\n".join(fails[:8])


with ThreadPoolExecutor(max_workers=5) as ex:
    for name, verdict, detail in ex.map(run, PROBES):
        print(f"{verdict:12s} {name}")
        if detail:
            print("    " + detail.replace("\n", "\n    "))
